"""Fixtures for scripts/foundation/org_conformance.py (the organisation drift guard).

Builds an in-memory snapshot of a small organisation and checks that each
conformance rule fires exactly where it should.

Run from repository root:
  python3 .github/foundation-tests/test_org_conformance.py
"""
from __future__ import annotations

import datetime as dt
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "foundation"))
import org_conformance  # noqa: E402

LATEST = "a" * 40
PREVIOUS = "b" * 40
OLD = "c" * 40
SUPERSEDED = "d" * 40
CANDIDATE = "e" * 40
TODAY = dt.date(2026, 9, 24)

CONFIG = {
    "organisation": "acme",
    "foundation_repository": "shared",
    "max_minor_lag": 1,
    "superseded_tags": ["v2.0.0"],
    "removed_inputs": {"legacy_metadata_enabled": "v2.3.0"},
    "deprecated_inputs": ["advanced_security_enabled"],
    "deferred": {
        "later": {"reason": "Deferred by the platform owner", "approved_by": "@owner", "expires": "2026-12-31"},
        "lapsed": {"reason": "Deferral that ran out", "approved_by": "@owner", "expires": "2026-09-01"},
    },
}
TAGS = {"v2.0.0": SUPERSEDED, "v2.1.0": OLD, "v2.2.0": PREVIOUS, "v2.3.0": LATEST, "v2.3.0-rc.1": CANDIDATE}

CONTRACT = yaml.safe_dump({"schema_version": 1, "security": {"sast_provider": "fallback"}})
PERMISSIONS = {"contents": "read", "packages": "read", "actions": "read", "security-events": "write"}


def caller(ref: str = LATEST, *, foundation_ref: str | None = None, permissions: dict | None = None, **extra) -> str:
    inputs = {"foundation_ref": foundation_ref if foundation_ref is not None else ref, **extra}
    if foundation_ref == "":
        inputs.pop("foundation_ref")
    document = {
        "name": "Foundation",
        "on": {"pull_request": None},
        "permissions": PERMISSIONS if permissions is None else permissions,
        "jobs": {"foundation": {"uses": f"acme/shared/.github/workflows/foundation-repository-gates.yml@{ref}", "with": inputs}},
    }
    return yaml.safe_dump(document, sort_keys=False)


def repo(name: str, *, workflows: dict | None = None, contract: str | None = CONTRACT, **extra) -> dict:
    default = {".github/workflows/foundation.yml": caller()}
    return {"name": name, "visibility": "public", "workflows": default if workflows is None else workflows,
            "repository_yaml": contract, **extra}


REPOSITORIES = [
    repo("conformant"),
    repo("shared", workflows={".github/workflows/foundation.yml": "jobs: {foundation: {uses: ./.github/workflows/foundation-repository-gates.yml}}"}),
    repo("stale", workflows={".github/workflows/foundation.yml": caller(PREVIOUS)}),
    repo("very-stale", workflows={".github/workflows/foundation.yml": caller(OLD)}),
    repo("superseded", workflows={".github/workflows/foundation.yml": caller(SUPERSEDED)}),
    repo("candidate", workflows={".github/workflows/foundation.yml": caller(CANDIDATE)}),
    repo("mismatch", workflows={".github/workflows/foundation.yml": caller(foundation_ref=PREVIOUS)}),
    repo("no-ref", workflows={".github/workflows/foundation.yml": caller(foundation_ref="")}),
    repo("thin-permissions", workflows={".github/workflows/foundation.yml": caller(permissions={"contents": "read"})}),
    repo("legacy-on-latest", workflows={".github/workflows/foundation.yml": caller(legacy_metadata_enabled=False)}),
    repo("legacy-on-previous", workflows={".github/workflows/foundation.yml": caller(PREVIOUS, legacy_metadata_enabled=False)}),
    repo("deprecated", workflows={".github/workflows/foundation.yml": caller(advanced_security_enabled=True)}),
    repo("no-caller", workflows={".github/workflows/ci.yml": "name: CI\non: push\njobs: {}\n"}),
    repo("no-contract", contract=None),
    repo("undeclared", contract=yaml.safe_dump({"schema_version": 1})),
    repo("private-review", visibility="private",
         workflows={".github/workflows/foundation.yml": caller(dependency_review_enabled=True)}),
    repo("private-review-approved", visibility="private",
         workflows={".github/workflows/foundation.yml": caller(dependency_review_enabled=True)},
         contract=yaml.safe_dump({"schema_version": 1, "security": {"sast_provider": "fallback", "ghas": {
             "approved_by": "@owner", "reason": "GHAS licensed here", "expires": "2027-01-01"}}})),
    repo("renamed-uses", workflows={
        ".github/workflows/foundation.yml": caller(),
        ".github/workflows/old.yml": "jobs:\n  scan:\n    uses: nabhold/shared/.github/workflows/security-secrets-scan.yml@" + OLD + "\n",
    }),
    repo("renamed-mention", workflows={
        ".github/workflows/foundation.yml": caller(),
        ".github/workflows/greet.yml": "# See https://github.com/nabhold/baobab for the guide\nname: greet\n",
    }),
    repo("later", workflows={".github/workflows/foundation.yml": caller(OLD)}),
    repo("lapsed", workflows={".github/workflows/foundation.yml": caller(OLD)}),
    {"name": "archived", "archived": True},
    {"name": "unreadable", "error": "could not read repository contents: HTTP Error 403"},
]

report = org_conformance.evaluate({"tags": TAGS, "repositories": REPOSITORIES}, CONFIG, TODAY)


def found(repository: str) -> set[tuple[str, str]]:
    return {(item["severity"], item["check"]) for item in report["findings"] if item["repository"] == repository}


expected = {
    "conformant": set(),
    "shared": set(),
    "stale": {("Medium", "stale-pin")},
    "very-stale": {("High", "superseded-pin")},
    "superseded": {("High", "superseded-pin")},
    "candidate": {("Medium", "unreleased-pin")},
    "mismatch": {("High", "foundation-ref-mismatch")},
    "no-ref": {("High", "foundation-ref-mismatch")},
    "thin-permissions": {("High", "missing-caller-permissions")},
    "legacy-on-latest": {("High", "removed-input")},
    "legacy-on-previous": {("Medium", "removed-input"), ("Medium", "stale-pin")},
    "deprecated": {("Medium", "deprecated-input")},
    "no-caller": {("High", "missing-foundation-caller")},
    "no-contract": {("High", "missing-repository-contract")},
    "undeclared": {("Low", "undeclared-sast-provider")},
    "private-review": {("High", "private-dependency-review")},
    "private-review-approved": set(),
    "renamed-uses": {("High", "nabhold-reference")},
    "renamed-mention": {("Medium", "nabhold-mention")},
    "later": {("High", "superseded-pin")},
    "lapsed": {("High", "superseded-pin"), ("High", "expired-deferral")},
    "archived": set(),
    "unreadable": {("Medium", "unreadable")},
}
for name, wanted in expected.items():
    actual = found(name)
    assert actual == wanted, f"{name}: expected {sorted(wanted)}, got {sorted(actual)}"

assert report["latest_release"] == "v2.3.0", report["latest_release"]
assert "archived" not in report["repositories_scanned"]
# The pre-release tag is not a promoted release.
assert "v2.3.0-rc.1" != report["latest_release"]

# A valid deferral hides the repository's findings from the verdict; an
# expired one does not.
deferred = {item["repository"]: item["deferred"] for item in report["findings"]}
assert deferred["later"] is True
assert deferred["lapsed"] is False
assert report["passed"] is False  # several non-deferred High findings above

# A clean organisation passes, and a deferred-only failure still passes.
clean = org_conformance.evaluate(
    {"tags": TAGS, "repositories": [repo("conformant"), repo("later", workflows={".github/workflows/foundation.yml": caller(OLD)})]},
    {**CONFIG, "deferred": {"later": CONFIG["deferred"]["later"]}}, TODAY,
)
assert clean["passed"] is True, clean["findings"]
assert clean["deferred_findings"] == 1

summary = org_conformance.render_summary(report)
assert "### Findings" in summary and "### Deferred repositories" in summary and "**Result: failed**" in summary

# The shipped configuration is well formed and names only real controls.
shipped = yaml.safe_load((ROOT / ".baobab/org-conformance.yaml").read_text())
assert shipped["organisation"] == "baobab-platform"
for name, deferral in shipped["deferred"].items():
    assert deferral["approved_by"].startswith("@"), name
    assert len(deferral["reason"]) >= 12, name
    dt.date.fromisoformat(str(deferral["expires"]))
for tag in shipped["removed_inputs"].values():
    assert org_conformance.parse_release(tag), tag
org_conformance.evaluate({"tags": {}, "repositories": []}, shipped, TODAY)

print("Organisation conformance fixtures passed")
