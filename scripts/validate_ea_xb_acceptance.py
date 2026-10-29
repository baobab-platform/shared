#!/usr/bin/env python3
"""Validate the EA-XB business-outcome *design inventory*, not runtime evidence.

This check prevents structural regressions, deletion/relabelling of mandatory
XBE cases and promotion of a design receipt into a fake execution PASS. Actual
L4 receipts, provider runs, legal truth, customs status and production approval
remain independently evidenced by their owners.
"""
from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ARCH = ROOT / "docs" / "architecture"
MANIFEST = ARCH / "ea-xb-cross-border-acceptance-matrix.json"
PLAN = ARCH / "EA-implementation-plan-v2.3-2026-10-20.md"
PROGRAMME = ARCH / "ea-v2.3-cross-border-business-execution-2026-10-29.md"
MATRIX = ARCH / "ea-v2.3-acceptance-and-adoption-matrix.md"
DASHBOARD = ARCH / "ea-dashboard.md"
INDEX = ROOT / "docs" / "adr" / "README.md"
L4 = ARCH / "ea-v2.2-integration-acceptance-matrix.md"

CASE_IDS = tuple(f"XBE-{n:02d}" for n in range(1, 19))
OWNERS = frozenset({
    "Shared", "Infrastructure", "CP", "IAM", "Subscriptions", "Trade",
    "baobab-erp", "Regulations", "Trade Docs", "TMS", "Payments",
})
REQUIRED_OWNER_COVERAGE = frozenset({
    "CP", "IAM", "Trade", "baobab-erp", "Regulations", "Trade Docs",
    "TMS", "Payments", "Infrastructure",
})


def validate_manifest(data: dict[str, Any]) -> list[str]:
    """Validate a parsed design inventory without requiring network/CI runtime."""
    errors: list[str] = []

    def require(cond: bool, problem: str) -> None:
        if not cond:
            errors.append(problem)

    require(data.get("schema") == "ea-xb-acceptance-design.v1", "unsupported manifest schema")
    require(data.get("programme") == "EA-XB", "programme must be EA-XB")
    require(data.get("evidence_class") == "DESIGN_ONLY", "design is not runtime evidence")
    require(data.get("run_status") == "NOT_EXECUTED", "design cannot claim a runtime run")
    require(data.get("canonical_l4_registry") == "docs/architecture/ea-v2.2-integration-acceptance-matrix.md",
            "the original canonical L4 registry must remain authoritative")

    policy = data.get("release_policy")
    require(isinstance(policy, dict), "release_policy missing")
    if isinstance(policy, dict):
        for flag in (
            "all_mandatory", "implementation_state_separate_from_contracts_and_production",
            "protected_production_approval_requires_independent_acceptance",
            "synthetic_legal_and_provider_fixtures_cannot_assert_external_compliance",
            "canonical_l4_ids_unchanged",
        ):
            require(policy.get(flag) is True, f"release policy {flag} must be true")
        require(policy.get("admission") == "NO_AGGREGATE_PASS_WHEN_REQUIRED_CASE_NOT_PASS",
                "all mandatory cases must pass, no skip/fallback")

    topology = data.get("scenario_topology")
    require(isinstance(topology, dict), "missing scenario_topology")
    if isinstance(topology, dict):
        exporter, importer = topology.get("exporter"), topology.get("importer")
        require(isinstance(exporter, dict), "missing exporter")
        require(isinstance(importer, dict), "missing importer")
        if isinstance(exporter, dict):
            require(exporter.get("platform_relationship") == "EXTERNAL_CLIENT",
                    "exporter must be unrelated external customer")
            require(exporter.get("subscription") == "COMMERCIAL", "exporter must be commercial")
            require(exporter.get("digital_estate_required") is False,
                    "external customer must not require a DigitalEstate")
            require(exporter.get("market") == "ZA", "reference exporter must be South African")
            require(exporter.get("synthetic") is True, "reference exporter is synthetic")
        if isinstance(importer, dict):
            require(importer.get("market") == "UG", "reference importer must be Ugandan")
            require(importer.get("synthetic") is True, "reference importer is synthetic")
            require(importer.get("variant") == [
                "EXTERNAL_COUNTERPARTY_NO_TENANT", "INDEPENDENT_EXTERNAL_CLIENT_TENANT"
            ], "both tenant and non-tenant buyer scenarios are mandatory")
        corridor = topology.get("corridor")
        require(isinstance(corridor, dict), "missing corridor")
        if isinstance(corridor, dict):
            require(corridor.get("origin_market") == "ZA"
                    and corridor.get("destination_market") == "UG",
                    "corridor must remain ZA to UG")
            for field in ("tariff_code", "origin_preference", "incoterm", "customs_approval"):
                require(corridor.get(field) is None, f"{field} must not be fabricated in design")

    cases = data.get("cases")
    require(isinstance(cases, list), "cases must be an array")
    if not isinstance(cases, list):
        return errors
    ids = [c.get("id") if isinstance(c, dict) else None for c in cases]
    require(ids == list(CASE_IDS), "XBE-01..18 are exact, ordered, unique and mandatory")
    covered_owners: set[str] = set()
    for item in cases:
        if not isinstance(item, dict):
            errors.append("malformed case entry")
            continue
        cid = item.get("id", "?")
        require(item.get("required") is True, f"{cid} must remain mandatory")
        require(item.get("status") == "NOT_RUN", f"{cid}: design must not claim PASS/FAIL")
        require(item.get("evidence") is None, f"{cid}: no runtime evidence in design")
        for field in ("name", "positive", "negative", "required_evidence"):
            value = item.get(field)
            require(isinstance(value, str) and len(value.strip()) >= 25
                    if field != "name" else isinstance(value, str) and len(value.strip()) >= 8,
                    f"{cid}: {field} must be substantive")
        owners = item.get("owners")
        require(isinstance(owners, list) and 2 <= len(owners) <= 5
                and len(owners) == len(set(owners)), f"{cid}: valid distinct responsible owners required")
        if isinstance(owners, list):
            require(set(owners) <= OWNERS, f"{cid}: unknown owner")
            covered_owners.update(x for x in owners if isinstance(x, str))
    require(REQUIRED_OWNER_COVERAGE <= covered_owners, "required cross-repository owners are missing")
    return errors


def validate_publication(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    files = {
        "plan": root / PLAN.relative_to(ROOT),
        "programme": root / PROGRAMME.relative_to(ROOT),
        "matrix": root / MATRIX.relative_to(ROOT),
        "dashboard": root / DASHBOARD.relative_to(ROOT),
        "index": root / INDEX.relative_to(ROOT),
        "l4": root / L4.relative_to(ROOT),
    }
    for key, file in files.items():
        if not file.is_file():
            errors.append(f"required {key} file missing: {file}")
    if errors:
        return errors
    content = {key: p.read_text(encoding="utf-8") for key, p in files.items()}
    for key in ("plan", "matrix", "dashboard", "index"):
        if "ea-v2.3-cross-border-business-execution-2026-10-29.md" not in content[key]:
            errors.append(f"{key} does not link EA-XB programme")
    if "ea-xb-cross-border-acceptance-matrix.json" not in content["programme"]:
        errors.append("programme does not link exact acceptance inventory")
    if "INT-07" not in content["l4"] or "INT-08" not in content["l4"]:
        errors.append("canonical L4 scope unexpectedly missing")
    if "XBE-01..XBE-18" not in content["programme"]:
        errors.append("programme must preserve the complete acceptance series")
    return errors


def validate(path: Path = MANIFEST, root: Path = ROOT) -> list[str]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return [f"cannot parse EA-XB manifest: {exc}"]
    if not isinstance(data, dict):
        return ["manifest root must be an object"]
    return validate_manifest(data) + validate_publication(root)


if __name__ == "__main__":
    failures = validate()
    if failures:
        for issue in failures:
            print(f"EA-XB INVALID: {issue}", file=sys.stderr)
        sys.exit(1)
    print("EA-XB: 18 mandatory design cases validated; no runtime/production acceptance asserted")
