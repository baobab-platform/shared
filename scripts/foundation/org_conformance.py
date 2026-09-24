#!/usr/bin/env python3
"""Organisation-wide Foundation conformance report (drift guard).

Reads every repository in the organisation through the GitHub REST API and
reports the drift that the 2026-09-23 conformance audit had to find by hand:

  High    nabhold-reference            a workflow uses: or image: line still points at the pre-rename nabhold/ path
  Medium  nabhold-mention              a workflow mentions nabhold/ elsewhere (comments, links, other values)
  High    missing-repository-contract  no .baobab/repository.yaml on the default branch
  High    missing-foundation-caller    no workflow calls foundation-repository-gates.yml
  High    foundation-ref-mismatch      foundation_ref is missing or differs from the uses: SHA
  High    missing-caller-permissions   the caller does not grant the permissions Foundation needs
  High    removed-input                the caller passes an input its pinned Foundation release no longer accepts
  Medium  removed-input                the caller passes an input it must drop when it repins to a newer release
  High    superseded-pin               the pin is a superseded release, or too many minors behind
  High    private-dependency-review    private repo enables dependency review with no GHAS record or exception
  High    expired-deferral             a deferral in the configuration has expired
  Medium  stale-pin                    the pin is a promoted release, but not the latest
  Medium  unreleased-pin               the pin is not a promoted release (for example a pilot candidate)
  Medium  deprecated-input             the caller passes a deprecated input
  Medium  unreadable                   the repository could not be read with the available token
  Low     undeclared-sast-provider     .baobab/repository.yaml does not declare security.sast_provider

Repositories listed under `deferred` in the configuration are still reported,
but their findings do not fail the run until the deferral expires. The run
fails when any non-deferred High finding exists.

Usage:
  org_conformance.py --config .baobab/org-conformance.yaml [--snapshot snapshot.json]
                     [--report report.json] [--summary summary.md] [--write-snapshot out.json]

Without --snapshot the script calls the GitHub API using GITHUB_TOKEN (or
GH_TOKEN). The evaluation itself (`evaluate`) is a pure function over a
snapshot so it can be tested without network access.
"""
from __future__ import annotations

import argparse
import base64
import datetime as dt
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

import yaml

SEVERITY_ORDER = {"High": 0, "Medium": 1, "Low": 2}
REQUIRED_PERMISSIONS = {
    "contents": "read",
    "packages": "read",
    "actions": "read",
    "security-events": "write",
}
PERMISSION_RANK = {"none": 0, "read": 1, "write": 2}
ENTRYPOINT = "foundation-repository-gates.yml"
USES_PATTERN = re.compile(
    r"^(?P<owner>[^/\s]+)/(?P<repo>[^/\s]+)/\.github/workflows/"
    + re.escape(ENTRYPOINT)
    + r"@(?P<ref>\S+)$"
)
SEMVER = re.compile(r"^v(\d+)\.(\d+)\.(\d+)$")
NABHOLD_PATH = re.compile(r"\bnabhold/[A-Za-z0-9_.-]+")
EXECUTABLE_LINE = re.compile(r"^\s*(?:-\s*)?(?:uses|image):")


# --------------------------------------------------------------------------
# Evaluation (pure)
# --------------------------------------------------------------------------


def parse_release(tag: str) -> tuple[int, int, int] | None:
    match = SEMVER.match(tag)
    return tuple(int(part) for part in match.groups()) if match else None


def releases(tags: dict[str, str], superseded: set[str]) -> tuple[dict[str, str], str | None]:
    """Map peeled SHA -> tag for promoted releases, and return the latest tag."""
    promoted = {tag: sha for tag, sha in tags.items() if parse_release(tag) and tag not in superseded}
    latest = max(promoted, key=parse_release, default=None)
    return {sha: tag for tag, sha in promoted.items()}, latest


def load_yaml(text: str) -> Any:
    try:
        return yaml.safe_load(text)
    except yaml.YAMLError:
        return None


def workflow_on(document: dict) -> Any:
    # PyYAML parses the bare key `on` as boolean True.
    return document.get("on", document.get(True))


def permission_gaps(workflow: dict, job: dict) -> list[str]:
    """Permissions the Foundation caller job lacks (job-level overrides workflow-level)."""
    granted = job.get("permissions", workflow.get("permissions"))
    if granted in ("write-all",):
        return []
    if not isinstance(granted, dict):
        # read-all, missing, or empty: the org default may be read-only.
        granted = {}
    gaps = []
    for scope, needed in REQUIRED_PERMISSIONS.items():
        have = str(granted.get(scope, "none"))
        if PERMISSION_RANK.get(have, 0) < PERMISSION_RANK[needed]:
            gaps.append(f"{scope}: {needed}")
    return gaps


def evaluate(snapshot: dict, config: dict, today: dt.date) -> dict:
    organisation = config["organisation"]
    foundation_repo = config.get("foundation_repository", "shared")
    max_minor_lag = int(config.get("max_minor_lag", 1))
    superseded = set(config.get("superseded_tags", []))
    # input name -> first release that no longer accepts it
    removed_inputs = {name: parse_release(str(tag)) for name, tag in (config.get("removed_inputs") or {}).items()}
    assert all(removed_inputs.values()), "removed_inputs values must be release tags such as v2.3.0"
    deprecated_inputs = set(config.get("deprecated_inputs", []))
    deferred = config.get("deferred", {}) or {}

    by_sha, latest = releases(snapshot.get("tags", {}), superseded)
    latest_version = parse_release(latest) if latest else None
    superseded_shas = {sha for tag, sha in snapshot.get("tags", {}).items() if tag in superseded}

    findings: list[dict] = []

    def add(repo: str, severity: str, check: str, detail: str, path: str | None = None) -> None:
        findings.append({"repository": repo, "severity": severity, "check": check, "detail": detail, "path": path})

    for name, deferral in deferred.items():
        expires = deferral.get("expires")
        expiry = expires if isinstance(expires, dt.date) else dt.date.fromisoformat(str(expires))
        if expiry < today:
            add(name, "High", "expired-deferral", f"deferral approved by {deferral.get('approved_by')} expired on {expiry}")

    for repo in sorted(snapshot.get("repositories", []), key=lambda item: item["name"]):
        name = repo["name"]
        if repo.get("archived"):
            continue
        if repo.get("error"):
            add(name, "Medium", "unreadable", repo["error"])
            continue

        workflows: dict[str, str] = repo.get("workflows", {})
        for path, text in sorted(workflows.items()):
            executable, mentions = set(), set()
            for line in text.splitlines():
                hits = NABHOLD_PATH.findall(line)
                (executable if EXECUTABLE_LINE.match(line) else mentions).update(hits)
            if executable:
                add(name, "High", "nabhold-reference", f"uses {', '.join(sorted(executable))}", path)
            if mentions:
                add(name, "Medium", "nabhold-mention", f"mentions {', '.join(sorted(mentions))}", path)

        contract_text = repo.get("repository_yaml")
        contract = load_yaml(contract_text) if contract_text else None
        if contract is None:
            add(name, "High", "missing-repository-contract", ".baobab/repository.yaml is missing or unreadable")
            contract = {}

        security = contract.get("security") or {}
        if contract and not security.get("sast_provider"):
            add(name, "Low", "undeclared-sast-provider", "declare security.sast_provider (codeql | fallback | disabled)")

        if name == foundation_repo:
            continue  # the self-consumer calls the orchestrator by local path

        callers = []
        for path, text in sorted(workflows.items()):
            document = load_yaml(text)
            if not isinstance(document, dict):
                continue
            for job_id, job in (document.get("jobs") or {}).items():
                if not isinstance(job, dict):
                    continue
                match = USES_PATTERN.match(str(job.get("uses", "")))
                if match and match["owner"] == organisation and match["repo"] == foundation_repo:
                    callers.append((path, document, job_id, job, match["ref"]))

        if not callers:
            add(name, "High", "missing-foundation-caller", f"no workflow calls {organisation}/{foundation_repo}/.github/workflows/{ENTRYPOINT}")
            continue

        for path, document, job_id, job, ref in callers:
            inputs = job.get("with") or {}
            foundation_ref = str(inputs.get("foundation_ref", "")).strip()
            if not foundation_ref:
                add(name, "High", "foundation-ref-mismatch", f"job {job_id} does not pass foundation_ref", path)
            elif foundation_ref != ref:
                add(name, "High", "foundation-ref-mismatch", f"job {job_id} pins {ref[:12]} but foundation_ref is {foundation_ref[:12]}", path)

            gaps = permission_gaps(document, job)
            if gaps:
                add(name, "High", "missing-caller-permissions", f"job {job_id} lacks {', '.join(gaps)}", path)

            pinned_version = parse_release(by_sha[ref]) if ref in by_sha else None
            for key in sorted(set(inputs) & set(removed_inputs)):
                removed_in = removed_inputs[key]
                removed_tag = "v" + ".".join(map(str, removed_in))
                # An unreleased pin may already lack the input, so treat it as breaking.
                if pinned_version is None or pinned_version >= removed_in:
                    add(name, "High", "removed-input", f"job {job_id} passes {key}, which Foundation {removed_tag} and later reject", path)
                else:
                    add(name, "Medium", "removed-input", f"job {job_id} passes {key}; drop it when repinning to {removed_tag} or later", path)
            for key in sorted(set(inputs) & deprecated_inputs):
                add(name, "Medium", "deprecated-input", f"job {job_id} passes deprecated {key}", path)

            if ref in superseded_shas:
                add(name, "High", "superseded-pin", f"job {job_id} pins a superseded release ({ref[:12]})", path)
            elif ref in by_sha:
                tag = by_sha[ref]
                if tag != latest:
                    version = parse_release(tag)
                    lag = (latest_version[0] - version[0]) * 1000 + (latest_version[1] - version[1])
                    if lag > max_minor_lag:
                        add(name, "High", "superseded-pin", f"job {job_id} pins {tag}; latest is {latest} (more than {max_minor_lag} minor behind)", path)
                    else:
                        add(name, "Medium", "stale-pin", f"job {job_id} pins {tag}; latest is {latest}", path)
            else:
                add(name, "Medium", "unreleased-pin", f"job {job_id} pins {ref[:12]}, which is not a promoted release (latest is {latest})", path)

            if inputs.get("dependency_review_enabled") is True and repo.get("visibility") == "private":
                exceptions = contract.get("exceptions") or {}
                if not security.get("ghas") and "dependency-review" not in exceptions:
                    add(name, "High", "private-dependency-review", f"job {job_id} enables dependency review on a private repository without security.ghas or a dependency-review exception", path)

    for finding in findings:
        deferral = deferred.get(finding["repository"])
        finding["deferred"] = bool(deferral) and finding["check"] != "expired-deferral" and not any(
            item["repository"] == finding["repository"] and item["check"] == "expired-deferral" for item in findings
        )

    findings.sort(key=lambda item: (item["deferred"], SEVERITY_ORDER[item["severity"]], item["repository"], item["check"]))
    blocking = [item for item in findings if item["severity"] == "High" and not item["deferred"]]
    counts = {level: sum(1 for item in findings if item["severity"] == level and not item["deferred"]) for level in SEVERITY_ORDER}
    return {
        "schema_version": 1,
        "organisation": organisation,
        "generated_on": today.isoformat(),
        "latest_release": latest,
        "latest_release_sha": snapshot.get("tags", {}).get(latest) if latest else None,
        "repositories_scanned": sorted(repo["name"] for repo in snapshot.get("repositories", []) if not repo.get("archived")),
        "counts": counts,
        "deferred_findings": sum(1 for item in findings if item["deferred"]),
        "passed": not blocking,
        "findings": findings,
    }


def render_summary(report: dict) -> str:
    lines = ["## Foundation organisation conformance", ""]
    lines.append(f"Organisation: **{report['organisation']}** · latest promoted release: **{report['latest_release'] or 'none'}**")
    lines.append(f"Repositories scanned: {len(report['repositories_scanned'])}")
    counts = report["counts"]
    lines.append(
        f"Findings: **{counts['High']} High**, {counts['Medium']} Medium, {counts['Low']} Low"
        f" (plus {report['deferred_findings']} in deferred repositories)"
    )
    lines.append("")
    lines.append("**Result: passed**" if report["passed"] else "**Result: failed** — resolve the High findings below")
    active = [item for item in report["findings"] if not item["deferred"]]
    deferred = [item for item in report["findings"] if item["deferred"]]
    for title, items in (("Findings", active), ("Deferred repositories", deferred)):
        if not items:
            continue
        lines += ["", f"### {title}", "", "| Severity | Repository | Check | Detail |", "|---|---|---|---|"]
        for item in items:
            where = f" (`{item['path']}`)" if item.get("path") else ""
            detail = item["detail"].replace("|", "\\|")
            lines.append(f"| {item['severity']} | {item['repository']} | `{item['check']}` | {detail}{where} |")
    return "\n".join(lines) + "\n"


# --------------------------------------------------------------------------
# Snapshot collection (GitHub REST API)
# --------------------------------------------------------------------------


class GitHub:
    def __init__(self, token: str | None, api: str = "https://api.github.com") -> None:
        self.token = token
        self.api = api.rstrip("/")

    def get(self, path: str, params: dict | None = None) -> Any:
        url = f"{self.api}{path}"
        if params:
            url += "?" + urllib.parse.urlencode(params)
        request = urllib.request.Request(url, headers={
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "baobab-foundation-org-conformance",
            **({"Authorization": f"Bearer {self.token}"} if self.token else {}),
        })
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.load(response)

    def paginate(self, path: str, params: dict | None = None) -> list:
        items, page = [], 1
        while True:
            batch = self.get(path, {**(params or {}), "per_page": 100, "page": page})
            items += batch
            if len(batch) < 100:
                return items
            page += 1

    def file(self, repo: str, path: str, ref: str) -> str | None:
        try:
            data = self.get(f"/repos/{repo}/contents/{urllib.parse.quote(path)}", {"ref": ref})
        except urllib.error.HTTPError as error:
            if error.code == 404:
                return None
            raise
        return base64.b64decode(data["content"]).decode("utf-8", errors="replace")


def collect(client: GitHub, organisation: str, foundation_repo: str, names: list[str] | None = None) -> dict:
    tags: dict[str, str] = {}
    for ref in client.get(f"/repos/{organisation}/{foundation_repo}/git/matching-refs/tags/v"):
        tag = ref["ref"].removeprefix("refs/tags/")
        if not parse_release(tag):
            continue
        target = ref["object"]
        while target["type"] == "tag":  # peel annotated tags
            target = client.get(f"/repos/{organisation}/{foundation_repo}/git/tags/{target['sha']}")["object"]
        tags[tag] = target["sha"]

    if names:
        listing = []
        for name in names:
            try:
                listing.append(client.get(f"/repos/{organisation}/{name}"))
            except urllib.error.HTTPError as error:
                listing.append({"name": name, "error": f"repository metadata unreadable (HTTP {error.code})"})
    else:
        listing = client.paginate(f"/orgs/{organisation}/repos", {"type": "all"})
    repositories = []
    for item in listing:
        entry = {"name": item["name"], "visibility": item.get("visibility"), "archived": item.get("archived", False)}
        if item.get("error"):
            entry["error"] = item["error"]
            repositories.append(entry)
            continue
        if entry["archived"]:
            repositories.append(entry)
            continue
        full = f"{organisation}/{item['name']}"
        branch = item.get("default_branch", "main")
        try:
            workflows = {}
            try:
                listing = client.get(f"/repos/{full}/contents/.github/workflows", {"ref": branch})
            except urllib.error.HTTPError as error:
                if error.code != 404:
                    raise
                listing = []
            for file in listing:
                if file.get("type") == "file" and file["name"].endswith((".yml", ".yaml")):
                    workflows[f".github/workflows/{file['name']}"] = client.file(full, file["path"], branch) or ""
            entry["workflows"] = workflows
            entry["repository_yaml"] = client.file(full, ".baobab/repository.yaml", branch)
        except (urllib.error.URLError, KeyError, ValueError) as error:
            entry["error"] = f"could not read repository contents: {error}"
        repositories.append(entry)
    return {"tags": tags, "repositories": repositories}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--config", required=True)
    parser.add_argument("--snapshot", help="evaluate a saved snapshot instead of calling the API")
    parser.add_argument("--write-snapshot", help="save the collected snapshot to this path")
    parser.add_argument("--report", default="org-conformance-report.json")
    parser.add_argument("--summary", default=os.environ.get("GITHUB_STEP_SUMMARY"))
    parser.add_argument("--today", help="evaluation date (YYYY-MM-DD); defaults to today")
    parser.add_argument("--repositories", help="comma-separated names to scan instead of listing the organisation")
    args = parser.parse_args(argv)

    with open(args.config, encoding="utf-8") as handle:
        config = yaml.safe_load(handle)
    if args.snapshot:
        with open(args.snapshot, encoding="utf-8") as handle:
            snapshot = json.load(handle)
    else:
        token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
        names = [name.strip() for name in args.repositories.split(",") if name.strip()] if args.repositories else None
        snapshot = collect(GitHub(token), config["organisation"], config.get("foundation_repository", "shared"), names)
    if args.write_snapshot:
        with open(args.write_snapshot, "w", encoding="utf-8") as handle:
            json.dump(snapshot, handle, indent=2)

    today = dt.date.fromisoformat(args.today) if args.today else dt.date.today()
    report = evaluate(snapshot, config, today)
    with open(args.report, "w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2)
    summary = render_summary(report)
    print(summary)
    if args.summary:
        with open(args.summary, "a", encoding="utf-8") as handle:
            handle.write(summary)
    for item in report["findings"]:
        if item["severity"] == "High" and not item["deferred"]:
            location = f" ({item['path']})" if item.get("path") else ""
            print(f"::error::{item['repository']}: {item['check']}: {item['detail']}{location}")
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
