#!/usr/bin/env python3
"""Contract consumer lock validation and drift reporting (EA Plan v2.0 EA-01).

A consumer's contracts.lock.yaml pins the baobab-platform/shared commit it is
built against and lists the Shared contracts it consumes (EA-01A; schema
.baobab/contract-consumer-lock.schema.json). Two commands, both run by
Foundation against a full-history checkout of Shared:

  check --repository-root DIR --shared-repo DIR [--baseline REF] [--mode M]
      EA-01C. An active engine must carry a lock. A lock that exists must
      match the canonical schema; its pinned commit must exist and be
      reachable from the approved baseline (Shared main), so a branch or
      unmerged commit is not a pin; every listed contract must exist and
      parse at the pin; and no consumed contract may have been removed by
      the baseline, which is incompatible drift by definition. --mode warn
      reports findings as annotations and passes; enforce fails; auto
      enforces for a repository with the `engine` trait and warns for any
      other (EA-01 Gate 3: Digital Estates stay frozen until the EA
      Unfreeze Gate, so their legacy locks are reported, not failed).

  drift --repository-root DIR --shared-repo DIR [--baseline REF] [--format F]
      EA-01D. Reports the pin, the approved baseline, how many Shared
      revisions the pin is behind, and for each consumed contract whether it
      is unchanged, changed or removed since the pin. It never fails: being
      behind is not a release failure, and a changed contract needs review
      (and the consumer's own compatibility tests) rather than a verdict
      from a text diff. The classification is CURRENT, BEHIND_UNCHANGED,
      BEHIND_CHANGED or INCOMPATIBLE (a consumed contract was removed); an
      unusable lock or pin is UNKNOWN.

Setup (same dependencies as the Foundation fixture suite):
  python3 -m pip install -r .github/foundation-tests/requirements.txt
  python3 scripts/contract_lock.py check --repository-root ../baobab-payments --shared-repo .
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / ".baobab/contract-consumer-lock.schema.json").read_text())
VALIDATOR = Draft202012Validator(SCHEMA)
LOCK_PATH = "contracts.lock.yaml"
REPOSITORY_CONTRACT_PATH = ".baobab/repository.yaml"
MODES = ("warn", "enforce", "auto")
CLASSIFICATIONS = ("CURRENT", "BEHIND_UNCHANGED", "BEHIND_CHANGED", "INCOMPATIBLE", "UNKNOWN")


class Shared:
    """Read-only view of a Shared git repository with the history the pins need."""

    def __init__(self, path: Path):
        self.path = path

    def _git(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(["git", "-C", str(self.path), *args], capture_output=True, text=True)

    def resolve(self, ref: str) -> str | None:
        result = self._git("rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}")
        return result.stdout.strip() if result.returncode == 0 else None

    def is_ancestor(self, commit: str, descendant: str) -> bool:
        return self._git("merge-base", "--is-ancestor", commit, descendant).returncode == 0

    def behind(self, commit: str, baseline: str) -> int:
        return int(self._git("rev-list", "--count", f"{commit}..{baseline}").stdout.strip() or 0)

    def blob(self, commit: str, path: str) -> str | None:
        result = self._git("rev-parse", "--verify", "--quiet", f"{commit}:{path}")
        return result.stdout.strip() if result.returncode == 0 else None

    def read(self, commit: str, path: str) -> str:
        return self._git("show", f"{commit}:{path}").stdout


def load_yaml(path: Path) -> object | None:
    return yaml.safe_load(path.read_text()) if path.is_file() else None


def is_engine(repository_contract: object) -> bool:
    """A repository that consumes Shared contracts as a platform runtime: an engine, or the Control Plane.

    The control-plane trait (ADR-0020 amendment, 2026-10-01) is not an engine: it provides no
    resolvable capability. It consumes and serves Shared contracts, so the lock rules apply to it.
    """
    traits = repository_contract.get("capabilities") or [] if isinstance(repository_contract, dict) else []
    return "engine" in traits or "control-plane" in traits


def effective_mode(mode: str, repository_root: Path) -> str:
    if mode != "auto":
        return mode
    return "enforce" if is_engine(load_yaml(repository_root / REPOSITORY_CONTRACT_PATH)) else "warn"


def lock_required(repository_contract: object) -> bool:
    if not isinstance(repository_contract, dict):
        return False
    lifecycle = (repository_contract.get("repository") or {}).get("lifecycle")
    return lifecycle == "active" and is_engine(repository_contract)


def schema_findings(lock: object) -> list[str]:
    return [
        f"{LOCK_PATH}: {'/'.join(str(p) for p in error.absolute_path) or '(root)'}: {error.message}"
        for error in sorted(VALIDATOR.iter_errors(lock), key=lambda e: list(map(str, e.absolute_path)))
    ]


def parse_error(path: str, text: str) -> str | None:
    try:
        if path.endswith(".json"):
            json.loads(text)
        elif path.endswith((".yaml", ".yml")):
            yaml.safe_load(text)
    except (ValueError, yaml.YAMLError) as error:
        return str(error).splitlines()[0]
    return None


def check(repository_root: Path, shared: Shared, baseline_ref: str) -> list[str]:
    lock = load_yaml(repository_root / LOCK_PATH)
    if lock is None:
        if lock_required(load_yaml(repository_root / REPOSITORY_CONTRACT_PATH)):
            return [f"{LOCK_PATH} is missing: an active engine must pin the Shared contracts it consumes (EA-01A)"]
        return []
    findings = schema_findings(lock)
    if findings:
        return findings
    baseline = shared.resolve(baseline_ref)
    if baseline is None:
        return [f"Shared baseline {baseline_ref!r} does not resolve in {shared.path}"]
    commit = lock["source"]["commit"]
    if shared.resolve(commit) is None:
        return [f"{LOCK_PATH}: source.commit {commit} does not exist in baobab-platform/shared"]
    if not shared.is_ancestor(commit, baseline):
        findings.append(f"{LOCK_PATH}: source.commit {commit} is not on Shared main (not reachable from {baseline[:12]})")
    for path in lock["contracts"]:
        if shared.blob(commit, path) is None:
            findings.append(f"{LOCK_PATH}: {path} does not exist at {commit[:12]}")
            continue
        error = parse_error(path, shared.read(commit, path))
        if error:
            findings.append(f"{LOCK_PATH}: {path} does not parse at {commit[:12]}: {error}")
        elif shared.blob(baseline, path) is None:
            findings.append(f"{LOCK_PATH}: {path} was removed from Shared by {baseline[:12]} (incompatible drift)")
    return findings


def drift(repository_root: Path, shared: Shared, baseline_ref: str) -> dict:
    report: dict = {"lock": LOCK_PATH, "pin": None, "baseline": shared.resolve(baseline_ref), "behind": None,
                    "contracts": [], "classification": "UNKNOWN"}
    lock = load_yaml(repository_root / LOCK_PATH)
    if lock is None or schema_findings(lock) or report["baseline"] is None:
        report["reason"] = "no lock" if lock is None else ("baseline unresolved" if report["baseline"] is None
                                                            else "lock does not match the canonical schema")
        return report
    commit = lock["source"]["commit"]
    report["pin"] = commit
    if shared.resolve(commit) is None or not shared.is_ancestor(commit, report["baseline"]):
        report["reason"] = "pin is not on Shared main"
        return report
    report["behind"] = shared.behind(commit, report["baseline"])
    for path in lock["contracts"]:
        pinned, current = shared.blob(commit, path), shared.blob(report["baseline"], path)
        status = "removed" if current is None else ("missing at pin" if pinned is None else
                                                    ("unchanged" if pinned == current else "changed"))
        report["contracts"].append({"path": path, "status": status})
    statuses = {entry["status"] for entry in report["contracts"]}
    if "removed" in statuses:
        report["classification"] = "INCOMPATIBLE"
    elif "missing at pin" in statuses:
        report["reason"] = "a listed contract does not exist at the pin"
    elif report["behind"] == 0:
        report["classification"] = "CURRENT"
    else:
        report["classification"] = "BEHIND_CHANGED" if "changed" in statuses else "BEHIND_UNCHANGED"
    return report


def render_markdown(report: dict) -> str:
    short = lambda sha: f"`{sha[:12]}`" if sha else "—"  # noqa: E731
    lines = [
        "### Shared contract drift (EA-01D)",
        "",
        "| Pin | Approved baseline | Revisions behind | Classification |",
        "|---|---|---:|---|",
        f"| {short(report['pin'])} | {short(report['baseline'])} | "
        f"{'—' if report['behind'] is None else report['behind']} | **{report['classification']}** |",
    ]
    if report.get("reason"):
        lines += ["", f"Not assessed: {report['reason']}."]
    changed = [entry for entry in report["contracts"] if entry["status"] != "unchanged"]
    if changed:
        lines += ["", "| Consumed contract | Since the pin |", "|---|---|"]
        lines += [f"| `{entry['path']}` | {entry['status']} |" for entry in changed]
    if report["contracts"]:
        lines += ["", f"{len(report['contracts']) - len(changed)} of {len(report['contracts'])} consumed contracts unchanged."]
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    commands = parser.add_subparsers(dest="command", required=True)
    for name, help_text in (("check", "validate a consumer lock against Shared (EA-01C)"),
                            ("drift", "report a consumer's Shared drift (EA-01D)")):
        command = commands.add_parser(name, help=help_text)
        command.add_argument("--repository-root", type=Path, default=Path("."), help="consumer repository root")
        command.add_argument("--shared-repo", type=Path, required=True, help="a Shared git checkout with main's history")
        command.add_argument("--baseline", default="HEAD", help="approved Shared baseline ref (default: HEAD)")
    commands.choices["check"].add_argument("--mode", choices=MODES, default="enforce",
                                           help="warn reports findings and passes; enforce fails on any finding; "
                                                "auto enforces for engines and warns otherwise")
    commands.choices["drift"].add_argument("--format", choices=("markdown", "json"), default="markdown")
    args = parser.parse_args(argv)
    shared = Shared(args.shared_repo)

    if args.command == "drift":
        report = drift(args.repository_root, shared, args.baseline)
        print(json.dumps(report, indent=2) if args.format == "json" else render_markdown(report), end="")
        return 0
    findings = check(args.repository_root, shared, args.baseline)
    if effective_mode(args.mode, args.repository_root) == "warn":
        for finding in findings:
            print(f"::warning title=Contract consumer lock (EA-01)::{finding}")
        print(f"contract consumer lock: {len(findings)} finding(s), reported as warnings")
        return 0
    for finding in findings:
        print(f"FAIL: {finding}", file=sys.stderr)
    if findings:
        print(f"{len(findings)} failure(s)", file=sys.stderr)
        return 1
    print("contract consumer lock passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
