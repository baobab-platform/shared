#!/usr/bin/env python3
"""Negative fixtures for ADR-SHARED-001/003 first-party registry guard."""
from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("legal_entity_registry_validator", ROOT / "scripts/validate-legal-entity-registry.py")
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
validate = MODULE.validate

REGISTRY = yaml.safe_load((ROOT / "contracts/legal-entity/registry.yaml").read_text())
TENANCY = yaml.safe_load((ROOT / "contracts/tenancy/tenancy.yaml").read_text())
SCHEMA = json.loads((ROOT / "contracts/legal-entity/registry.schema.json").read_text())
DOMAIN = json.loads((ROOT / "contracts/control-plane/v1/domain.schema.json").read_text())


class FirstPartyRegistryConformance(unittest.TestCase):
    def violations(self, registry=None, tenancy=None):
        return validate(
            REGISTRY if registry is None else registry,
            TENANCY if tenancy is None else tenancy,
            SCHEMA, DOMAIN,
        )

    def test_real_repository_contracts(self):
        self.assertEqual([], self.violations())

    def test_types_are_not_coerced_into_authority(self):
        for field, value in (("baobab_tenant", "false"), ("identity_class", "LEGAL_ENTITY"),
                             ("incorporation_claim", True)):
            with self.subTest(field=field):
                registry = copy.deepcopy(REGISTRY)
                registry["entities"][0][field] = value
                self.assertTrue(self.violations(registry))
        registry = copy.deepcopy(REGISTRY)
        registry["entities"][0]["baobab_products"][0]["confirmed"] = "false"
        self.assertTrue(self.violations(registry))
        registry = copy.deepcopy(REGISTRY)
        registry["cross_cutting_products"][0]["confirmed"] = "false"
        self.assertTrue(self.violations(registry))

    def test_registry_cannot_mint_cp_or_runtime_authority(self):
        for field, value in (("tenant_id", "tn_fictional"), ("organisation_id", "org_fake"),
                             ("entitlement_active", True), ("db_connection", "postgres://secret")):
            with self.subTest(field=field):
                registry = copy.deepcopy(REGISTRY)
                registry["entities"][0][field] = value
                self.assertTrue(self.violations(registry))

    def test_uniqueness_and_first_party_scope(self):
        registry = copy.deepcopy(REGISTRY)
        registry["entities"][1]["id"] = registry["entities"][0]["id"]
        self.assertTrue(self.violations(registry))
        registry = copy.deepcopy(REGISTRY)
        registry["entities"][1]["baobab_products"].append(copy.deepcopy(registry["entities"][1]["baobab_products"][0]))
        self.assertTrue(self.violations(registry))
        registry = copy.deepcopy(REGISTRY)
        registry["entities"][2]["legacy_aliases"] = ["zuribeans_za"]
        self.assertTrue(self.violations(registry))
        tenancy = copy.deepcopy(TENANCY)
        tenancy["tenant_definition"]["first_party_identities"].append("EXTERNAL-CUSTOMER")
        self.assertTrue(self.violations(tenancy=tenancy))

    def test_website_or_group_does_not_create_tenancy(self):
        for key, value in (
            ("digital_estate_confers_tenancy", True),
            ("legal_entity_is_tenant_synonym", True),
            ("organisation_is_primary_boundary", False),
            ("product_consumption_requires_tenant", False),
            ("requires_default_legal_entity_registry_entry", True),
        ):
            with self.subTest(key=key):
                tenancy = copy.deepcopy(TENANCY)
                tenancy["tenant_definition"][key] = value
                self.assertTrue(self.violations(tenancy=tenancy))

    def test_unincorporated_business_does_not_claim_verified_legal_person(self):
        registry = copy.deepcopy(REGISTRY)
        registry["entities"][1]["incorporation_claim"] = "REGISTERED_EVIDENCED"
        self.assertTrue(self.violations(registry))
        registry = copy.deepcopy(REGISTRY)
        registry["entities"][0]["legal_evidence_ref"] = ""
        self.assertTrue(self.violations(registry))


if __name__ == "__main__":
    unittest.main()
