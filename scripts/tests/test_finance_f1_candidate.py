#!/usr/bin/env python3
"""Offline structural tests for the review-only F1 draft.

This deliberately does NOT test ERP posting, financial approvals, CP authority, or
provider certification. It asserts the candidate wire schema stays isolated from
the canonical catalogue and retains explicit scope / decimal-string protections.
"""
import json
import pathlib
import re
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
CANDIDATE = ROOT / "docs/architecture/proposals/finance-f1-candidate.schema.json"
CATALOGUE = ROOT / "contracts/capability/v1/catalogue.yaml"


class FinanceF1DraftContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = json.loads(CANDIDATE.read_text(encoding="utf-8"))
        cls.defs = cls.schema["$defs"]

    def test_candidate_is_not_a_canonical_capability(self):
        canonical = CATALOGUE.read_text(encoding="utf-8")
        for key in ("finance.ledger.read", "finance.journal.manage", "finance.statement.read"):
            self.assertNotIn("capability_key: " + key, canonical)

    def test_all_requests_reject_payload_authority(self):
        for key in ("scope", "ledgerReadRequest", "statementReadRequest",
                    "journalDraftRequest", "journalTransitionRequest"):
            shape = self.defs[key]
            self.assertFalse(shape.get("additionalProperties", True), key)
            keys = shape.get("properties", {})
            for forbidden in ("tenant_id", "legal_entity_id", "organisation_id",
                              "ad_client", "ad_org"):
                self.assertNotIn(forbidden, keys)

    def test_read_contract_has_explicit_scoping(self):
        scope = self.defs["scope"]
        self.assertEqual(set(scope["required"]), {"period", "as_of", "currency"})
        for name in ("ledgerReadRequest", "statementReadRequest"):
            self.assertIn("scope", self.defs[name]["required"])

    def test_money_is_decimal_string(self):
        decimal = self.defs["decimal"]
        self.assertEqual(decimal["type"], "string")
        pattern = re.compile(decimal["pattern"])
        for valid in ("0", "12.30", "-12.30"):
            self.assertTrue(pattern.fullmatch(valid))
        for invalid in ("1e3", "01.2", "12.", "NaN", "Infinity"):
            self.assertIsNone(pattern.fullmatch(invalid))

    def test_responses_must_disclose_completeness(self):
        response = self.defs["readResponse"]
        self.assertIn("completeness", response["required"])
        self.assertEqual(set(self.defs["completeness"]["enum"]),
                         {"complete", "partial", "stale", "withheld"})

    def test_journal_commands_require_idempotency_and_concurrency(self):
        draft = self.defs["journalDraftRequest"]
        transition = self.defs["journalTransitionRequest"]
        self.assertIn("idempotency_key", draft["required"])
        self.assertTrue({"idempotency_key", "expected_version"}.issubset(transition["required"]))
        self.assertEqual(transition["properties"]["expected_version"]["minimum"], 1)


if __name__ == "__main__":
    unittest.main()
