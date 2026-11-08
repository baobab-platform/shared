#!/usr/bin/env python3
"""Schema and governance regression negatives for Accepted ADR-SHARED-045."""
from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import unittest

from jsonschema import ValidationError

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("people_contract_gate", ROOT / "scripts/validate-people-contracts.py")
gate = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(gate)
EX = ROOT / "contracts/people/v1/examples"


def fixture(name):
    return json.loads((EX / (name + ".json")).read_text())


class ProviderNeutralPeopleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.resources = gate.schema_registry()

    def valid(self, schema, data):
        gate.validate_schema(schema + ".schema.json", data, self.resources)

    def rejects(self, schema, data):
        with self.assertRaises(ValidationError):
            self.valid(schema, data)

    def test_manifest_contracts_and_gates(self):
        self.assertEqual(gate.validate_package(), 9)

    def test_caller_cannot_assert_tenant_employer_provider_or_principal(self):
        for filename, schema in [
            ("employment-read-request", "employment-read-request"),
            ("payroll-run-read-request", "payroll-run-read-request"),
            ("employment-manage-request", "employment-manage-request"),
            ("payroll-evidence-attest-request", "payroll-evidence-attest-request"),
        ]:
            for unsafe in ("tenant_id", "legal_employer_id", "provider_id", "principal_ref", "source_selection", "approval_granted"):
                data = fixture(filename)
                data[unsafe] = "forged_ref"
                with self.subTest(filename=filename, field=unsafe):
                    self.rejects(schema, data)

    def test_employment_correction_cannot_skip_version_fence(self):
        x = fixture("employment-manage-request")
        del x["expected_version"]
        self.rejects("employment-manage-request", x)
        x = fixture("employment-manage-request")
        x["operation"] = "PROPOSE_VERSION"
        self.rejects("employment-manage-request", x)
        x = fixture("employment-manage-response")
        x["state"] = "APPROVED"
        self.rejects("employment-manage-response", x)

    def test_incomplete_or_withheld_data_cannot_claim_complete_receipt(self):
        x = fixture("employment-read-response")
        x["data_state"] = "WITHHELD"
        self.rejects("employment-read-response", x)
        x = fixture("payroll-run-read-response")
        x["data_state"] = "PARTIAL"
        self.rejects("payroll-run-read-response", x)
        x = fixture("payroll-run-read-response")
        x["run_state"] = "DRAFT"
        del x["signed_result_receipt_ref"]
        del x["rule_pack_sha256"]
        self.valid("payroll-run-read-response", x)
        x["run_state"] = "FINALISED"
        self.rejects("payroll-run-read-response", x)

    def test_verified_evidence_needs_receipt_but_is_not_payment(self):
        x = fixture("payroll-evidence-attest-response")
        x["verification_status"] = "VERIFIED"
        self.rejects("payroll-evidence-attest-response", x)
        x["verified_receipt_ref"] = "verified_synthetic01"
        self.valid("payroll-evidence-attest-response", x)
        x["payment_released"] = True
        self.rejects("payroll-evidence-attest-response", x)

    def test_provider_selection_cannot_embed_vendor_native_ids_or_wildcard_scope(self):
        x = fixture("provider-selection")
        x["selection"]["vendor_employee_id"] = "internal_123"
        self.rejects("provider-selection", x)
        x = fixture("provider-selection")
        x["selection"]["tenant_id"] = "*"
        self.rejects("provider-selection", x)
        x = fixture("provider-selection")
        x["selection"]["source_of_record"] = "AUTO_FALLBACK"
        self.rejects("provider-selection", x)
        x = fixture("provider-selection")
        x["portability_enabled"] = False
        self.rejects("provider-selection", x)

    def test_restricted_employee_pii_not_in_any_accepted_example(self):
        forbidden = {"person_name", "salary", "bank_account", "tax_id", "national_id",
                     "employee_name", "ssn", "raw_payslip", "native_employee_id"}
        def keys(node):
            if isinstance(node, dict):
                for key, child in node.items():
                    yield key
                    yield from keys(child)
            elif isinstance(node, list):
                for child in node:
                    yield from keys(child)

        for file in EX.glob("*.json"):
            self.assertFalse(forbidden.intersection(keys(json.loads(file.read_text()))), file.name)


if __name__ == "__main__":
    unittest.main()
