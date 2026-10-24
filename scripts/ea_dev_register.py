#!/usr/bin/env python3
"""Validate and render EA-DEV observations; never evaluate runtime authority.

Stdlib only. No network, credentials, CP writes or approval decisions. A valid
register is source-reporting evidence, not proof of the assertions it links.
"""
from __future__ import annotations

import argparse
from datetime import date
import json
from pathlib import Path
import re
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
REGISTER = ROOT / "docs/architecture/ea-dev-implementation-register.json"
VIEW = REGISTER.with_suffix(".md")
PACKAGE_IDS = {f"DEV-{i:02d}" for i in range(16)}
IDENTITY_CASES = {
    "issuer-issuance-and-readback", "current-cp-principal-and-link",
    "wrong-audience-denial", "wrong-tenant-denial", "issuer-revocation-before-expiry",
    "cp-principal-deactivation", "complete-teardown",
}
CMS_CASES = {
    "published-home-nav-footer", "wrong-audience-token", "wrong-credential",
    "disabled-caller", "expired-caller-token", "revoked-caller-token", "missing-grant",
    "wrong-owner-or-context", "neighbour-tenant", "draft-or-preview", "withdrawn-content",
    "dependency-outage-and-restoration", "validator-negatives", "teardown",
}
SHA = re.compile(r"[0-9a-f]{40}")
PROGRESS = {"NOT_ASSESSED", "NOT_STARTED", "SOURCE_IN_PROGRESS", "SOURCE_MERGED",
            "LOCAL_TESTED", "REAL_COMPONENT_SYNTHETIC_DATA"}
ASSESSMENTS = {"IMPLEMENTED_PENDING_REVIEW", "PARTIAL_SOURCE_RUNTIME_UNPROVEN",
               "NOT_AUDITED", "NOT_IMPLEMENTED", "IMPLEMENTED_NOT_TESTED",
               "RUNTIME_FAILED", "MISSING_EXTERNAL_INPUT", "NOT_APPROVED", "ACCEPTED"}
BLOCKERS = {"NOT_REVIEWED", "NOT_APPROVED", "IMPLEMENTED_NOT_TESTED",
            "NOT_ASSESSED", "NOT_IMPLEMENTED", "RUNTIME_FAILED", "MISSING_EXTERNAL_INPUT"}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def fields(value: dict, names: str) -> None:
    require(isinstance(value, dict) and set(value) == set(names.split()),
            f"closed record fields required: {names}")


def unique_object(pairs: list[tuple[str, object]]) -> dict:
    """Duplicate JSON fields must not silently replace an earlier observation."""
    result = {}
    for key, value in pairs:
        require(key not in result, "duplicate JSON field")
        result[key] = value
    return result


def text(value: str) -> bool:
    return isinstance(value, str) and bool(value.strip())


def day(value: str) -> date:
    require(isinstance(value, str), "date must be ISO date text")
    parsed = date.fromisoformat(value)
    require(parsed.isoformat() == value, "date must be YYYY-MM-DD")
    return parsed


def github_url(value: str, repo: str | None = None) -> bool:
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    prefix = f"/baobab-platform/{repo}/" if repo else "/baobab-platform/"
    return (parsed.scheme == "https" and parsed.netloc == "github.com"
            and parsed.path.startswith(prefix) and not parsed.query and not parsed.fragment)


def local_file(path: str, root: Path) -> Path:
    require(isinstance(path, str), "local document path required")
    resolved = (root / path).resolve()
    require(resolved.is_relative_to(root.resolve()) and resolved.is_file(),
            "document missing or outside repository")
    return resolved


def validate(data: dict, root: Path = ROOT) -> None:
    """Reject incomplete/circular inventories and promotion unsupported by receipts.

    External URLs are references, not verified receipts: final-head review must
    inspect them before any reported claim is accepted by the owning authority.
    """
    fields(data, "schema observed_on purpose programme canonical_matrix reconciliation "
           "observation_scope freshness_days baselines packages")
    require(data["schema"] == "ea-dev-implementation-register.v1", "unsupported version")
    require(data["purpose"] == "READ_MODEL_NOT_AUTHORITY", "not an authority surface")
    observed = day(data["observed_on"])
    require(type(data["freshness_days"]) is int and 1 <= data["freshness_days"] <= 30,
            "bounded freshness policy required")
    require(text(data["observation_scope"]), "observation limits required")
    programme = local_file(data["programme"], root).read_text(encoding="utf-8")
    matrix = local_file(data["canonical_matrix"], root).read_text(encoding="utf-8")
    local_file(data["reconciliation"], root)
    baseline_keys = set()
    require(isinstance(data["baselines"], list) and data["baselines"], "baselines required")
    for baseline in data["baselines"]:
        fields(baseline, "key repo sha pr scope reviewed_head_sha ci_status ci_urls")
        require(text(baseline["key"]) and baseline["key"] not in baseline_keys,
                "duplicate or empty baseline")
        baseline_keys.add(baseline["key"])
        require(re.fullmatch(r"[a-z0-9-]+", baseline["repo"]) is not None, "invalid repository")
        require(all(isinstance(baseline[k], str) and SHA.fullmatch(baseline[k])
                    for k in ("sha", "reviewed_head_sha")), "immutable source/head SHA required")
        require(type(baseline["pr"]) is int and baseline["pr"] > 0, "PR reference required")
        require(text(baseline["scope"]), "baseline evidence limits required")
        require(baseline["ci_status"] == "SUCCESS" and isinstance(baseline["ci_urls"], list)
                and baseline["ci_urls"] and all(
                    github_url(url, baseline["repo"]) and re.search(r"/actions/runs/[0-9]+$", url)
                    for url in baseline["ci_urls"]), "successful observed CI needs owning run links")
    packages = data["packages"]
    require(isinstance(packages, list) and len(packages) == 16, "all sixteen packages required")
    ids = [p.get("id") for p in packages]
    require(set(ids) == PACKAGE_IDS and len(set(ids)) == len(ids), "closed unique DEV roster required")
    graph = {}
    for package in packages:
        fields(package, "id title owner dependencies dependency_scope progress assessment source_baselines "
               "source_note observed_on target_date actual_completion_date mandatory_ci environment "
               "evidence_class runtime blockers next_action protected_staging_accepted "
               "external_certification_accepted production_accepted rollback")
        key = package["id"]
        require(f"**{key} — {package['title']} (" in programme, "package differs from Accepted plan")
        require(all(text(package[k]) for k in ("owner", "dependency_scope", "source_note",
                                              "next_action", "rollback")), "owner/handoff required")
        dependencies = package["dependencies"]
        require(isinstance(dependencies, list) and len(dependencies) == len(set(dependencies))
                and set(dependencies) <= PACKAGE_IDS and key not in dependencies, "invalid dependencies")
        graph[key] = dependencies
        require(package["progress"] in PROGRESS and package["assessment"] in ASSESSMENTS,
                "unknown progress or assessment")
        require(day(package["observed_on"]) <= observed, "package observation exceeds snapshot")
        for name in ("target_date", "actual_completion_date"):
            if package[name] is not None:
                parsed = day(package[name])
                require(name != "actual_completion_date" or parsed <= observed,
                        "future completion is not observed")
        require(isinstance(package["source_baselines"], list)
                and set(package["source_baselines"]) <= baseline_keys, "unresolved baseline")
        require(package["mandatory_ci"] in {"PENDING_THIS_PR", "BASELINE_ONLY", "NOT_ASSESSED", "SUCCESS"},
                "unknown CI state")
        if package["progress"] in {"SOURCE_MERGED", "LOCAL_TESTED", "REAL_COMPONENT_SYNTHETIC_DATA"}:
            require(package["source_baselines"] and package["mandatory_ci"] == "SUCCESS"
                    and package["assessment"] != "NOT_AUDITED", "source milestone needs reviewed baseline/CI")
        require(package["environment"] in {"NO_RUNTIME_OBSERVED", "ISOLATED_DEVELOPMENT"},
                "explicit development environment observation required")
        require(package["evidence_class"] in {"SOURCE", "LOCAL_TESTED", "REAL_COMPONENT_SYNTHETIC_DATA"},
                "development evidence class required")
        require(all(package[k] is False for k in ("protected_staging_accepted",
                    "external_certification_accepted", "production_accepted")),
                "protected acceptance belongs to separate protected records")
        runtime = package["runtime"]
        fields(runtime, "status canonical_scenarios evidence_urls cleanup cases")
        require(runtime["status"] in {"NOT_OBSERVED", "BLOCKED", "FAIL", "PASS"}, "unknown runtime state")
        require(runtime["cleanup"] in {"NOT_OBSERVED", "FAIL", "COMPLETE"}, "unknown cleanup state")
        require(isinstance(runtime["canonical_scenarios"], list) and all(
            text(case) and re.search(r"(?<![A-Z0-9-])" + re.escape(case) + r"(?![A-Z0-9-])", matrix)
            for case in runtime["canonical_scenarios"]), "scenario absent from canonical matrix")
        require(isinstance(runtime["evidence_urls"], list) and all(
            github_url(url) for url in runtime["evidence_urls"]), "invalid runtime receipt URL")
        require(isinstance(runtime["cases"], list), "case inventory required")
        names = []
        for case in runtime["cases"]:
            fields(case, "case result evidence_urls reason")
            require(text(case["case"]) and text(case["reason"]), "case identity/reason required")
            names.append(case["case"])
            require(case["result"] in {"BLOCKED", "FAIL", "PASS"}, "no skipped mandatory cases")
            require(isinstance(case["evidence_urls"], list) and all(
                github_url(url) for url in case["evidence_urls"]), "invalid case evidence")
            if case["result"] == "PASS":
                require(case["evidence_urls"] and package["evidence_class"] == "REAL_COMPONENT_SYNTHETIC_DATA",
                        "case PASS requires real-component receipt")
        require(len(names) == len(set(names)), "duplicate case")
        if key in {"DEV-04", "DEV-05"}:
            require(set(names) == (IDENTITY_CASES if key == "DEV-04" else CMS_CASES),
                    "seven INT-03C and fourteen NAB-03 obligations cannot change")
        if (runtime["status"] == "PASS" or package["progress"] == "REAL_COMPONENT_SYNTHETIC_DATA"
                or package["evidence_class"] == "REAL_COMPONENT_SYNTHETIC_DATA"):
            require(runtime["status"] == "PASS" and runtime["evidence_urls"] and names
                    and all(c["result"] == "PASS" for c in runtime["cases"])
                    and runtime["cleanup"] == "COMPLETE"
                    and package["evidence_class"] == "REAL_COMPONENT_SYNTHETIC_DATA"
                    and package["environment"] == "ISOLATED_DEVELOPMENT", "runtime PASS lacks proof/cleanup")
        if package["actual_completion_date"] is not None:
            require(package["source_baselines"] and package["mandatory_ci"] == "SUCCESS"
                    and package["progress"] not in {"NOT_ASSESSED", "NOT_STARTED", "SOURCE_IN_PROGRESS"}
                    and not package["blockers"], "completion requires reviewed source/CI and no blockers")
            require(key == "DEV-00" or runtime["status"] == "PASS", "runtime package not complete")
        require(isinstance(package["blockers"], list), "blocker list required")
        for blocker in package["blockers"]:
            fields(blocker, "kind detail")
            require(blocker["kind"] in BLOCKERS and text(blocker["detail"]), "explicit blocker category required")
    visited, visiting = set(), set()

    def visit(key: str) -> None:
        require(key not in visiting, "dependency cycle")
        if key not in visited:
            visiting.add(key)
            for dependency in graph[key]:
                visit(dependency)
            visiting.remove(key)
            visited.add(key)

    for key in graph:
        visit(key)


def freshness(data: dict, as_of: date) -> str:
    observed = day(data["observed_on"])
    require(as_of >= observed, "as-of date precedes observation")
    dates = [observed] + [day(package["observed_on"]) for package in data["packages"]]
    return "STALE" if any((as_of - d).days > data["freshness_days"] for d in dates) else "WITHIN_OBSERVATION_WINDOW"


def render(data: dict) -> str:
    """Deterministic view; never change observation dates during a CI check."""
    lines = ["# EA-DEV implementation register", "",
             "Generated from [the JSON register](ea-dev-implementation-register.json); edit JSON and run `python3 scripts/ea_dev_register.py --write-view`.", "",
             f"**Observed:** {data['observed_on']}. **Evidence:** SOURCE reporting only. **Protected staging, external certification and production:** not accepted.", "",
             data["observation_scope"], "",
             f"Observations become STALE after {data['freshness_days']} days; compare the observation date with today. CI validates structure and does not refresh evidence.", "",
             "[Decision precedence, CI policy and closure rules](ea-dev-00-gate-reconciliation.md). NOT_ASSESSED means no new progress claim. Baseline CI does not qualify a current composed runtime.", "",
             "| Package | Accountable team | Dependencies | Progress / assessment | Observed | CI / runtime | Next action |",
             "| --- | --- | --- | --- | --- | --- | --- |"]
    for p in data["packages"]:
        values = [f"**{p['id']}** — {p['title']}", p["owner"], ", ".join(p["dependencies"]) or "None",
                  f"{p['progress']} / {p['assessment']}", p["observed_on"],
                  f"{p['mandatory_ci']} / {p['runtime']['status']}", p["next_action"]]
        lines.append("| " + " | ".join(v.replace("|", "\\|").replace("\n", " ") for v in values) + " |")
    lines += ["", "## Verified source baselines", "",
              "| Baseline | Merge/source | Reviewed head | Evidence limits / CI |", "| --- | --- | --- | --- |"]
    for b in data["baselines"]:
        prefix = f"https://github.com/baobab-platform/{b['repo']}"
        ci = ", ".join(f"[run {i + 1}]({url})" for i, url in enumerate(b["ci_urls"]))
        lines.append(f"| {b['key']} | [{b['sha']}]({prefix}/commit/{b['sha']}) ([PR #{b['pr']}]({prefix}/pull/{b['pr']})) | `{b['reviewed_head_sha']}` | {b['scope']}; {ci} |")
    lines += ["", "## Case obligations requiring runtime evidence", "",
              "Descriptive labels preserve the existing INT-03C obligations and NAB-03 subcases; they do not create canonical scenario IDs.", "",
              "| Package | Case | Result | Reason |", "| --- | --- | --- | --- |"]
    for p in data["packages"]:
        for c in p["runtime"]["cases"]:
            lines.append(f"| {p['id']} | {c['case']} | {c['result']} | {c['reason']} |")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--check", action="store_true")
    action.add_argument("--write-view", action="store_true")
    parser.add_argument("--as-of", type=date.fromisoformat, default=date.today())
    args = parser.parse_args()
    try:
        data = json.loads(REGISTER.read_text(encoding="utf-8"), object_pairs_hook=unique_object)
        validate(data)
        state = freshness(data, args.as_of)
        view = render(data)
        if args.write_view:
            VIEW.write_text(view, encoding="utf-8")
        else:
            require(VIEW.read_text(encoding="utf-8") == view, "generated view drift; run --write-view")
        print(f"VALID_REGISTER_SOURCE_ONLY; observed={data['observed_on']}; {state}; runtime not qualified")
        return 0
    except (ValueError, TypeError, KeyError, OSError) as error:
        raise SystemExit(f"EA-DEV register invalid: {error}") from error


if __name__ == "__main__":
    raise SystemExit(main())
