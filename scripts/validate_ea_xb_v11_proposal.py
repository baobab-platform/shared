#!/usr/bin/env python3
"""Structural check of a PROPOSED EA-XB v1.1 programme profile.

The immutable v1.0 XBE design remains subject to its pre-existing validator.
This checks completeness, independent applicability, bidirectional readiness
boundaries, CRM inclusion and non-invented execution evidence. It is NOT an
operation, regulatory evaluation, provider certification or merge approval.
"""
from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ARCH = ROOT / "docs" / "architecture"
PROPOSAL_PATH = ARCH / "ea-xb-v1.1-proposed-acceptance-profiles.json"
HISTORICAL_PATH = ARCH / "ea-xb-cross-border-acceptance-matrix.json"
DOCUMENT_PATH = ARCH / "ea-xb-v1.1-enterprise-corrective-architecture-2026-10-29.md"

EXPECTED = {
    "XB-CORE": tuple(f"XBC-{i:02d}" for i in range(1, 11)),
    "XB-AGR": tuple(f"XBA-{i:02d}" for i in range(1, 6)),
    "XB-MFG": tuple(f"XBM-{i:02d}" for i in range(1, 5)),
    "XB-NET": tuple(f"XBN-{i:02d}" for i in range(1, 8)),
    "XB-LOG": tuple(f"XBL-{i:02d}" for i in range(1, 5)),
}
LEGACY_IDS = tuple(f"XBE-{i:02d}" for i in range(1, 19))
CASES = frozenset(x for group in EXPECTED.values() for x in group)
REQUIRED_SCENARIOS = {
    "AGR-COFFEE-UG-ZA": (["XB-CORE", "XB-AGR", "XB-LOG"], "EXTERNAL_OR_QUALIFIED_AS_EVIDENCED"),
    "MFG-PUMPS-ZA-UG-EXTERNAL": (["XB-CORE", "XB-MFG", "XB-LOG"], "NON_TENANT"),
    "MFG-PUMPS-ZA-UG-DUAL": (["XB-CORE", "XB-MFG", "XB-NET", "XB-LOG"], "DUAL_QUALIFIED_TENANT"),
    "COOPERATIVE-TO-TENANT": (["XB-NET"], "IDENTITY_CONTINUITY_ONLY"),
    "AGR-COOPERATIVE-NET-EXPORT": (["XB-CORE", "XB-AGR", "XB-NET", "XB-LOG"], "DUAL_QUALIFIED_TENANT"),
}


def check_manifest(doc: dict[str, Any], historical: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    def need(ok: bool, message: str) -> None:
        if not ok:
            errors.append(message)

    need(doc.get("schema") == "ea-xb-profile-proposal.v1", "unknown proposal schema")
    need(doc.get("status") == "PROPOSED_FOR_REVIEW", "proposal cannot claim acceptance")
    need(doc.get("design_evidence_class") == "DESIGN_ONLY", "proposal cannot claim runtime")
    need(doc.get("execution_status") == "NOT_EXECUTED", "no executed profile evidence")
    need(doc.get("predecessor") == "docs/architecture/ea-xb-cross-border-acceptance-matrix.json",
         "historical baseline reference changed")
    need(doc.get("canonical_l4_registry") == historical.get("canonical_l4_registry"),
         "historical canonical L4 registry must not change")
    governance = doc.get("governance")
    need(isinstance(governance, dict), "governance object absent")
    if isinstance(governance, dict):
        for flag in (
            "historical_xbe_immutable", "independent_owner_approval_before_merge",
            "all_applicable_cases_must_pass", "non_applicable_profile_must_be_declared_before_run",
            "non_tenant_foreign_ledger_unobservable",
            "qualified_dual_erp_proof_only_when_both_are_authorised",
            "no_automatic_provider_or_legal_approval", "no_auto_activated_capability_keys",
        ):
            need(governance.get(flag) is True, "governance obligation disabled: " + flag)

    profiles = doc.get("profiles")
    need(isinstance(profiles, dict) and set(profiles) == set(EXPECTED),
         "profile set must be exact CORE/AGR/MFG/NET/LOG")
    if not isinstance(profiles, dict):
        return errors
    for name, wanted in EXPECTED.items():
        profile = profiles.get(name)
        if not isinstance(profile, dict):
            errors.append("missing profile: " + name)
            continue
        need(tuple(profile.get("case_ids", [])) == wanted, name + " case IDs incomplete/reordered")
        need(profile.get("domain") == name[3:], name + " wrong domain")
        need(profile.get("mandatory_for_cross_border") is (name == "XB-CORE"),
             name + " incorrect universal applicability")

    items = doc.get("cases")
    need(isinstance(items, list) and len(items) == len(CASES), "expected 30 proposed mandatory cases")
    if not isinstance(items, list):
        return errors
    case_index: dict[str, dict[str, Any]] = {}
    for item in items:
        if not isinstance(item, dict):
            errors.append("invalid case object")
            continue
        cid = item.get("id", "?")
        need(cid not in case_index, "duplicate case " + str(cid))
        case_index[cid] = item
        need(cid in CASES, "unknown proposed case ID " + str(cid))
        need(item.get("required") is True, str(cid) + " mandatory obligation missing")
        need(item.get("status") == "NOT_RUN" and item.get("evidence") is None,
             str(cid) + " fabricated execution evidence")
        if isinstance(cid, str) and cid in CASES:
            need(item.get("profile") == next(
                key[3:] for key, value in EXPECTED.items() if cid in value),
                str(cid) + " profile mismatch")
        owners = item.get("owners")
        need(isinstance(owners, list) and len(owners) >= 2 and all(
            isinstance(s, str) and s.strip() for s in owners),
            str(cid) + " owner source incomplete")
        for field in ("title", "positive", "negative", "required_evidence"):
            value = item.get(field)
            need(isinstance(value, str) and len(value.strip()) > (12 if field == "title" else 35),
                 str(cid) + " missing substantive " + field)
    need(set(case_index) == CASES, "proposed case inventory incomplete")

    old_cases = historical.get("cases")
    old_ids = [item.get("id") for item in old_cases] if isinstance(old_cases, list) else []
    need(tuple(old_ids) == LEGACY_IDS, "accepted historical XBE design changed or absent")
    mapping = doc.get("legacy_xbe_crosswalk")
    need(isinstance(mapping, list), "missing historical case crosswalk")
    if isinstance(mapping, list):
        mids = [x.get("original_case_id") for x in mapping if isinstance(x, dict)]
        need(tuple(mids) == LEGACY_IDS, "all historical XBE-01..18 must map once, in order")
        for item in mapping:
            if not isinstance(item, dict):
                errors.append("malformed crosswalk item")
                continue
            source = item.get("original_case_id")
            refs = item.get("proposed_case_ids")
            need(isinstance(refs, list) and bool(refs) and set(refs) <= CASES,
                 str(source) + " maps to missing proposed case")
            need(item.get("legacy_status") == "NOT_RUN", str(source) + " false historical PASS")
            need(item.get("approval_required") is True, str(source) + " silent supersession")
        xbe15 = next((x for x in mapping if x.get("original_case_id") == "XBE-15"), {})
        need(xbe15.get("proposed_case_ids") == ["XBC-07", "XBN-04"],
             "XBE-15 must split seller accounting vs qualified bilateral accounting")
        need(xbe15.get("disposition") == "SPLIT_EXTERNAL_EVIDENCE_AND_QUALIFIED_BILATERAL_ACCOUNTING",
             "XBE-15 external buyer correction missing")

    scenarios = doc.get("reference_scenarios")
    need(isinstance(scenarios, list) and len(scenarios) == len(REQUIRED_SCENARIOS),
         "required reference variants absent")
    if isinstance(scenarios, list):
        names: set[str] = set()
        for x in scenarios:
            if not isinstance(x, dict):
                errors.append("invalid scenario")
                continue
            sid = x.get("id")
            need(sid not in names, str(sid) + " duplicate scenario")
            names.add(sid)
            expect = REQUIRED_SCENARIOS.get(sid)
            need(expect is not None, "unexpected scenario " + str(sid))
            if expect:
                need(x.get("required_profiles") == expect[0], str(sid) + " incorrect profile scope")
                need(x.get("buyer_variant") == expect[1], str(sid) + " buyer evidence variant changed")
            need(x.get("status") == "NOT_RUN", str(sid) + " cannot claim live run")
        need(names == set(REQUIRED_SCENARIOS), "missing reference scenarios")
    return errors


def validate() -> list[str]:
    try:
        doc = json.loads(PROPOSAL_PATH.read_text(encoding="utf-8"))
        historical = json.loads(HISTORICAL_PATH.read_text(encoding="utf-8"))
    except (ValueError, OSError) as exc:
        return ["cannot read proposal/baseline manifest: " + str(exc)]
    if not isinstance(doc, dict) or not isinstance(historical, dict):
        return ["expected JSON object roots"]
    errors = check_manifest(doc, historical)
    if not DOCUMENT_PATH.is_file():
        errors.append("missing corrective document")
    else:
        body = DOCUMENT_PATH.read_text(encoding="utf-8")
        for required in ("**Status:** PROPOSED", "XB-CORE", "XB-AGR", "XB-MFG",
                         "XB-NET", "XB-LOG", "XBE-15", "baobab-crm", "ERP #116",
                         "explicitly approved"):
            if required not in body:
                errors.append("document absent requirement " + required)
    return errors


if __name__ == "__main__":
    failures = validate()
    if failures:
        for failure in failures:
            print("EA-XB v1.1 PROPOSAL INVALID: " + failure, file=sys.stderr)
        sys.exit(1)
    print("EA-XB v1.1: 30 design cases, 18 historic XBE mappings and 5 scenario variants validated. NO RUN OR APPROVAL CLAIMED.")
