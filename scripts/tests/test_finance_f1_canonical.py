#!/usr/bin/env python3
"""Contract-shape regression checks; not a substitute for ERP/iDempiere integration."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
FIN = ROOT / "contracts/finance/v1"
CAT = ROOT / "contracts/capability/v1/catalogue.yaml"

class FinanceF1ContractTests(unittest.TestCase):
    def test_six_schemas_are_valid_json_objects(self):
        for name in ("ledger-read", "journal-manage", "statement-read"):
            for suffix in ("request", "response"):
                schema = json.loads((FIN / f"{name}-{suffix}.schema.json").read_text())
                self.assertEqual(schema["type"], "object")
                self.assertFalse(schema["additionalProperties"])
                self.assertTrue(schema["required"])
                self.assertTrue(schema["$id"].endswith(f"{name}-{suffix}.schema.json"))

    def test_catalogue_indexes_tranche_once(self):
        text = CAT.read_text()
        for key in ("finance.ledger.read","finance.journal.manage","finance.statement.read"):
            self.assertEqual(text.count("capability_key: "+key+"\n"), 1)

    def test_no_authority_in_request_body(self):
        for name in ("ledger-read", "journal-manage", "statement-read"):
            schema = json.loads((FIN / f"{name}-request.schema.json").read_text())
            for field in ("tenant_id","legal_entity_id","organisation_id","ad_client","ad_org"):
                self.assertNotIn(field,schema["properties"])

    def test_journal_mutations_are_idempotent(self):
        req = json.loads((FIN / "journal-manage-request.schema.json").read_text())
        self.assertIn("idempotency_key", req["required"])
        self.assertEqual(req["properties"]["operation"]["enum"],
                         ["CREATE_DRAFT","SUBMIT","APPROVE","POST","REVERSE"])
        self.assertIn("expected_version",req["properties"])

    def test_responses_include_completeness(self):
        for name in ("ledger-read","statement-read"):
            schema=json.loads((FIN / f"{name}-response.schema.json").read_text())
            self.assertIn("completeness",schema["required"])
            self.assertIn("observed_at",schema["required"])

if __name__=="__main__":
    unittest.main()
