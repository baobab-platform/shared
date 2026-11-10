#!/usr/bin/env python3
"""ADR-SHARED-033 source admission gate, not certification of Finance/accounting.

The 10 Nov 2026 census accepts 12 names. It admits only 3 F1 DRAFT contract
definitions; F2/F3 must follow individual ADR §11 admission with source/schema
and negative fixtures. Do not treat Shared registration as a provider claim.
"""
from pathlib import Path
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[2]
CAPABILITY = ROOT / "contracts/capability/v1"
F1 = {
    "finance.ledger.read",
    "finance.journal.manage",
    "finance.statement.read",
}
F2 = {
    "finance.payable.manage",
    "finance.receivable.manage",
    "finance.bank-reconciliation.manage",
    "finance.cash-position.read",
    "finance.expense.manage",
    "finance.budget.manage",
}
F3 = {
    "finance.reporting-export.create",
    "finance.project-cost.read",
    "finance.consolidation.run",
}
EXISTING = "finance.order-consequence.process"


def load(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


class AdmittedFinanceTranches(unittest.TestCase):
    def test_exact_tranche_census_and_domain(self):
        self.assertEqual(12, len(F1 | F2 | F3))
        self.assertFalse(F1 & F2 or F1 & F3 or F2 & F3)
        registry = load(CAPABILITY / "namespace-registry.yaml")
        self.assertIn("finance", {domain["key"] for domain in registry["domains"]})

    def test_only_f1_has_canonical_definitions_today(self):
        catalogue = load(CAPABILITY / "catalogue.yaml")
        definitions = load(ROOT / "contracts/finance/v1/capabilities.yaml")
        finance_index = {
            x["capability_key"]: x for x in catalogue["capabilities"]
            if x["capability_key"].startswith("finance.")
        }
        # Historical ERP order consequence remains separate; its ownership
        # and provider status must never be silently overwritten by F1.
        self.assertEqual(F1 | {EXISTING}, set(finance_index))
        self.assertEqual(F1, {x["capability_key"] for x in definitions["capabilities"]})
        for definition in definitions["capabilities"]:
            key = definition["capability_key"]
            with self.subTest(key=key):
                self.assertEqual("finance", definition["domain"])
                self.assertEqual("baobab-erp", definition["owner"])
                self.assertEqual("DRAFT", definition["lifecycle"])
                self.assertEqual("EXPERIMENTAL", definition["maturity"])
                self.assertEqual("RESTRICTED", definition["data_classification"])
                self.assertEqual("baobab-erp", finance_index[key]["owner"])
                self.assertEqual("../../finance/v1/capabilities.yaml", finance_index[key]["source"])
                self.assertEqual(1, len(definition["contracts"]))
                entry = definition["contracts"][0]
                for ref in ("request_schema", "response_schema", "error_schema"):
                    self.assertTrue(entry.get(ref), "all F1 wire/error schemas are required")

    def test_f2_f3_are_census_only_and_not_in_transitional_provider_bundles(self):
        catalogue = load(CAPABILITY / "catalogue.yaml")
        registered = {x["capability_key"] for x in catalogue["capabilities"]}
        self.assertFalse((F2 | F3) & registered, "F2/F3 require individual §11 admission, not bulk activation")
        bundles = load(CAPABILITY / "registration-bundles.yaml")
        self.assertFalse(any(b["engine_id"] == "baobab-erp" for b in bundles["bundles"]),
                         "Shared must not invent an ERP F1 provider registration")
        # The absence of an ERP bundle is NOT proof of absence of all external
        # CP/engine registrations. Live provider/readiness must be audited there.

    def test_accepted_architecture_does_not_qualify_native_f1(self):
        adr = next((ROOT / "docs/adr").glob("ADR-SHARED-033*.md")).read_text(encoding="utf-8")
        self.assertIn("**Status:** **Accepted", adr)
        acceptance = load(ROOT / "docs/architecture/finance-f1-provider-acceptance.yaml")
        self.assertEqual("REQUIRED_NOT_EXECUTED", acceptance["status"])
        self.assertFalse(acceptance["source_validation_is_provider_acceptance"])
        self.assertEqual([f"F1-P{i:02d}" for i in range(1, 12)],
                         [row["id"] for row in acceptance["required_cases"]])


if __name__ == "__main__":
    unittest.main()
