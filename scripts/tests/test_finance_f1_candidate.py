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

    def test_candidate_document_is_never_a_canonical_contract_source(self):
        # The historical design can coexist with separately reviewed DRAFT
        # catalogue entries. Its proposal path/ID must never be indexed.
        canonical = CATALOGUE.read_text(encoding="utf-8")
        self.assertNotIn("finance-f1-candidate", canonical)
        self.assertNotIn("proposals/", canonical)
        self.assertIn("/proposals/", self.schema["$id"])

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




# Real schema validation catches semantic holes which key-presence tests
# cannot see. These synthetic fixtures establish wire behaviour only.
from jsonschema import Draft202012Validator, FormatChecker


class FinanceF1CandidateValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = json.loads(CANDIDATE.read_text())
        Draft202012Validator.check_schema(cls.schema)

    def valid(self, definition, value):
        schema = {**self.schema, '$ref': '#/$defs/' + definition}
        return Draft202012Validator(schema, format_checker=FormatChecker()).is_valid(value)

    def test_journal_line_has_one_positive_side_and_zero_counterpart(self):
        for debit, credit in [('10.25','0'),('0.00','10.25'),('0.00000001','0')]:
            self.assertTrue(self.valid('journalLine', {'account_ref':'acct_cash','debit':debit,'credit':credit}))
        for debit, credit in [('0','0'),('1','2'),('-1','0'),('0','-1'),('1e3','0'),(1,'0'),('1\n','0')]:
            self.assertFalse(self.valid('journalLine', {'account_ref':'acct_cash','debit':debit,'credit':credit}))
        self.assertFalse(self.valid('journalLine', {'account_ref':'acct_cash','debit':'1'}))

    def test_ledger_rows_follow_the_echoed_view(self):
        base={'completeness':'complete','scope':{'period':{'start':'2026-01-01','end':'2026-01-31'},
              'as_of':'2026-02-01T00:00:00Z','currency':'ZAR'},'observed_at':'2026-02-01T00:00:00Z','data_version':'synthetic-1'}
        rows={'chart_of_accounts':{'account_ref':'acct_cash','account_code':'1000','name':'Synthetic cash',
                  'account_type':'ASSET','normal_balance':'DEBIT','postable':True},
              'balances':{'account_ref':'acct_cash','account_code':'1000','balance':{'amount':'10.25','currency':'ZAR'}},
              'entries':{'entry_ref':'entry_a','journal_ref':'journal_a','account_ref':'acct_cash','account_code':'1000',
                  'posting_date':'2026-01-15','posting_state':'POSTED','debit':'10.25','credit':'0'}}
        for view,row in rows.items():
            with self.subTest(view=view):
                self.assertTrue(self.valid('readResponse',{**base,'view':view,'rows':[row]}))
                for other,wrong in rows.items():
                    if other!=view:
                        self.assertFalse(self.valid('readResponse',{**base,'view':view,'rows':[wrong]}))
                self.assertFalse(self.valid('readResponse',{**base,'view':view,'rows':[{**row,'AD_Org_ID':1}]}))
        self.assertFalse(self.valid('readResponse',{**base,'rows':[]}))


if __name__ == "__main__":
    unittest.main()
