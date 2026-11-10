#!/usr/bin/env python3
"""Validate the first-party legal-entity registry (ADR-SHARED-001/003).

This validates governance declarations only. Passing does not establish the
incorporation, tenant mapping, legal mandate or ProductSubscription in CP.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]


def validate(registry: dict, tenancy: dict, contract: dict, cp_domain: dict) -> list[str]:
    """Return deterministic contract violations without mutating the input."""
    Draft202012Validator.check_schema(contract)
    problems = [
        f"{'/'.join(map(str, e.absolute_path)) or '<root>'}: {e.message}"
        for e in Draft202012Validator(contract, format_checker=FormatChecker()).iter_errors(registry)
    ]
    if problems:
        return sorted(problems)

    entities = registry["entities"]
    ids = [item["id"] for item in entities]
    if len(ids) != len(set(ids)):
        problems.append("duplicate first-party canonical legal-entity ID")
    aliases = [alias for item in entities for alias in item.get("legacy_aliases", [])]
    if len(aliases) != len(set(aliases)):
        problems.append("duplicate legacy legal-entity alias")
    if set(ids) & set(aliases):
        problems.append("legacy aliases must not collide with canonical IDs")
    canonical = cp_domain["$defs"]["canonicalLegalEntityId"]
    product = cp_domain["$defs"]["productId"]
    for item in entities:
        identity = item["id"]
        if not re.fullmatch(canonical["pattern"].strip("^$"), identity):
            problems.append(f"{identity}: invalid canonical legal entity ID")
        declared = [p["product"] for p in item["baobab_products"]]
        if len(declared) != len(set(declared)):
            problems.append(f"{identity}: duplicate product-consumption intent")
        if item["baobab_tenant"] and not declared:
            problems.append(f"{identity}: tenant intent without a declared product")
        for name in declared:
            if not re.fullmatch(product["pattern"].strip("^$"), name):
                problems.append(f"{identity}: product ID disagrees with CP")
        if item["identity_class"] == "OPERATING_BUSINESS" and item["incorporation_claim"] == "REGISTERED_EVIDENCED":
            problems.append(f"{identity}: unincorporated operating business cannot assert registered incorporation")
        if item["incorporation_claim"] == "REGISTERED_EVIDENCED":
            for key in ("jurisdiction", "registration_identifier", "registration_effective_date", "legal_evidence_ref"):
                if not item.get(key):
                    problems.append(f"{identity}: registered incorporation lacks {key}")
    cross = [p["product"] for p in registry["cross_cutting_products"]]
    if len(cross) != len(set(cross)):
        problems.append("duplicate cross-cutting product intent")
    d = tenancy["tenant_definition"]
    if set(ids) != set(d["first_party_identities"]):
        problems.append("first-party registry does not match tenancy's first_party_identities")
    if d["first_party_registry_source"] != "shared/contracts/legal-entity/registry.yaml":
        problems.append("first-party registry authority path drift")
    if d["runtime_mapping_authority"] != "baobab-platform/baobab-cp":
        problems.append("tenant mapping authority must remain with CP")
    for key, expected in (
        ("digital_estate_confers_tenancy", False),
        ("legal_entity_is_tenant_synonym", False),
        ("product_consumption_requires_tenant", True),
        ("organisation_is_primary_boundary", True),
        ("requires_default_legal_entity_registry_entry", False),
    ):
        if d.get(key) is not expected:
            problems.append(f"tenant_definition.{key} must be {expected}")
    return sorted(problems)


def main() -> None:
    registry = yaml.safe_load((ROOT / "contracts/legal-entity/registry.yaml").read_text())
    tenancy = yaml.safe_load((ROOT / "contracts/tenancy/tenancy.yaml").read_text())
    contract = json.loads((ROOT / "contracts/legal-entity/registry.schema.json").read_text())
    domain = json.loads((ROOT / "contracts/control-plane/v1/domain.schema.json").read_text())
    problems = validate(registry, tenancy, contract, domain)
    if problems:
        raise SystemExit("Legal-entity governance contract failed:\n- " + "\n- ".join(problems))
    print("ADR-SHARED-001/003 first-party registry and separation guard passed (source contracts only)")


if __name__ == "__main__":
    main()
