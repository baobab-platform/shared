#!/usr/bin/env python3
"""Real wire-schema regressions for F1; no fake proof of ERP financial policy.

Exercise valid fixtures and negative mutations through Draft 2020-12, including
cross-file canonical references. Native accounting/CP/SoD/idempotency lifecycle
checks remain required in ERP; passing here never qualifies a provider.
"""
from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import unittest

from referencing.exceptions import Unresolvable

ROOT = Path(__file__).resolve().parents[2]
PACKAGE = ROOT / "contracts/finance/v1"
spec = importlib.util.spec_from_file_location("finance_contracts", ROOT / "scripts/validate-finance-contracts.py")
finance = importlib.util.module_from_spec(spec)
spec.loader.exec_module(finance)


def fixture(name):
    return json.loads((PACKAGE / "examples" / (name + ".json")).read_text())


class FinanceF1ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.resources = finance.registry()
        cls.validators = {name: finance.validator(name + ".schema.json", cls.resources)
                          for name in ("journal-manage-request", "journal-manage-response", "ledger-read-request",
                                       "ledger-read-response", "statement-read-request", "statement-read-response")}

    def accepts(self, name, value):
        return self.validators[name].is_valid(value)

    def test_every_published_schema_reference_and_example_is_checked(self):
        self.assertGreaterEqual(finance.validate_package(), 26)

    def test_no_operation_can_omit_its_payload_or_target_version(self):
        for operation in ("CREATE_DRAFT", "SUBMIT", "APPROVE", "POST", "REVERSE"):
            valid = fixture("journal-" + operation.lower() + "-request")
            self.assertTrue(self.accepts("journal-manage-request", valid))
            required = ["draft"] if operation == "CREATE_DRAFT" else ["journal_ref", "expected_version"]
            if operation == "REVERSE":
                required += ["reason", "reversal_date"]
            for key in ["operation", "idempotency_key", *required]:
                changed = copy.deepcopy(valid); changed.pop(key)
                with self.subTest(operation=operation, missing=key):
                    self.assertFalse(self.accepts("journal-manage-request", changed))

    def test_create_and_transition_payloads_cannot_be_mixed(self):
        draft = fixture("journal-create_draft-request")
        post = fixture("journal-post-request")
        for extra in ({"journal_ref": "erp_journalsynth"}, {"expected_version": 1}, {"reversal_date": "2026-01-16"}):
            self.assertFalse(self.accepts("journal-manage-request", {**draft, **extra}))
        self.assertFalse(self.accepts("journal-manage-request", {**post, "draft": draft["draft"]}))
        self.assertFalse(self.accepts("journal-manage-request", {**post, "reversal_date": "2026-01-16"}))
        self.assertFalse(self.accepts("journal-manage-request", {**post, "expected_version": 0}))
        self.assertFalse(self.accepts("journal-manage-request", {**fixture("journal-reverse-request"), "reason": "  "}))

    def test_positive_zero_journal_sides_use_exact_decimal_strings(self):
        body = fixture("journal-create_draft-request")
        for debit, credit in (("1", "0"), ("0.00", "0.000000000001")):
            changed = copy.deepcopy(body); changed["draft"]["lines"][0].update(debit=debit, credit=credit)
            self.assertTrue(self.accepts("journal-manage-request", changed))
        for debit, credit in (("0", "0"), ("1", "2"), ("-1", "0"), ("0", "-1"),
                              (1, "0"), ("1e3", "0"), ("01", "0"), ("1\n", "0"), ("NaN", "0")):
            changed = copy.deepcopy(body); changed["draft"]["lines"][0].update(debit=debit, credit=credit)
            with self.subTest(debit=debit, credit=credit):
                self.assertFalse(self.accepts("journal-manage-request", changed))
        for side in ("debit", "credit"):
            changed = copy.deepcopy(body); changed["draft"]["lines"][0].pop(side)
            self.assertFalse(self.accepts("journal-manage-request", changed))

    def test_currency_scale_is_not_fixed_at_two_or_eight_places(self):
        body = fixture("journal-create_draft-request")
        body["draft"]["lines"][0]["debit"] = "1.123456789012"
        body["draft"]["lines"][1]["credit"] = "1.123456789012"
        self.assertTrue(self.accepts("journal-manage-request", body))
        # The wire format preserves precision; ERP's approved baseline
        # determines whether that precision is legal for this book/currency.
        body["draft"]["lines"][0]["debit"] = "1" * 65
        self.assertFalse(self.accepts("journal-manage-request", body))

    def test_mutation_keys_match_canonical_idempotency_policy(self):
        body = fixture("journal-post-request")
        for key in ("short", "a" * 129, "a" * 16 + "\n", "has space in key", "!invalid-start-key"):
            self.assertFalse(self.accepts("journal-manage-request", {**body, "idempotency_key": key}))

    def test_queries_require_explicit_book_period_as_of_and_currency(self):
        for name, example in (("ledger-read-request", "ledger-entries-request"),
                              ("statement-read-request", "statement-trial_balance-request")):
            body = fixture(example)
            for key in body["scope"]:
                changed = copy.deepcopy(body); changed["scope"].pop(key)
                self.assertFalse(self.accepts(name, changed), key)
            for key,value in (("currency", "zar"), ("currency", "ZAR\n"),
                              ("period_start", "2026-02-30"), ("as_of", "not-a-timestamp")):
                changed = copy.deepcopy(body); changed["scope"][key] = value
                self.assertFalse(self.accepts(name, changed), key)

    def test_continuation_requires_a_snapshot_and_bounded_page_size(self):
        body = fixture("ledger-entries-request")
        for extra in ({"cursor": "next"}, {"snapshot_id": "snapshot"}, {"page_size": 0}, {"page_size": 1001}):
            self.assertFalse(self.accepts("ledger-read-request", {**body, **extra}))
        self.assertTrue(self.accepts("ledger-read-request", fixture("ledger-next-page-request")))

    def test_each_ledger_view_has_a_representable_and_exclusive_row_shape(self):
        for view in ("chart_of_accounts", "balances", "entries"):
            body = fixture("ledger-" + view + "-response")
            self.assertTrue(self.accepts("ledger-read-response", body))
            for other in ("chart_of_accounts", "balances", "entries"):
                if view != other:
                    self.assertFalse(self.accepts("ledger-read-response", {**body, "view": other}))
            missing = copy.deepcopy(body); missing.pop("view")
            self.assertFalse(self.accepts("ledger-read-response", missing))

    def test_entry_accounting_date_is_distinct_from_native_posting_time(self):
        body = fixture("ledger-entries-response")
        body["items"][0].pop("posted_at")
        self.assertFalse(self.accepts("ledger-read-response", body))
        body["items"][0]["posting_state"] = "DRAFT"
        body["posting_state"] = "DRAFT"
        self.assertTrue(self.accepts("ledger-read-response", body))
        body["items"][0]["posted_at"] = "2026-01-15T12:00:00Z"
        self.assertFalse(self.accepts("ledger-read-response", body))

    def test_signed_native_correction_history_remains_representable(self):
        entry = fixture("ledger-entries-response")
        entry["items"][0]["debit"] = "-100"
        self.assertTrue(self.accepts("ledger-read-response", entry))
        balance = fixture("ledger-balances-response")
        balance["items"][0]["debit_total"]["amount"] = "-100"
        self.assertTrue(self.accepts("ledger-read-response", balance))
        # A manual CREATE_DRAFT still uses positive magnitudes, with the
        # side explicitly chosen. Reads never reinterpret historic facts.
        draft = fixture("journal-create_draft-request")
        draft["draft"]["lines"][0]["debit"] = "-100"
        self.assertFalse(self.accepts("journal-manage-request", draft))

    def test_historical_snapshots_can_name_multiple_baseline_versions(self):
        body = fixture("ledger-entries-response")
        historic = copy.deepcopy(body["finance_baselines"][0])
        historic["version"] += 1
        historic["digest"] = "sha256:" + "a" * 64
        historic["effective_from"] = "2026-01-20"
        body["finance_baselines"].append(historic)
        self.assertTrue(self.accepts("ledger-read-response", body))
        body["items"][0].pop("finance_baseline")
        self.assertFalse(self.accepts("ledger-read-response", body))

    def test_trial_balance_and_policy_statement_lines_are_distinct(self):
        trial = fixture("statement-trial_balance-response")
        for kind in ("income_statement", "balance_sheet", "cash_flow"):
            policy = fixture("statement-" + kind + "-response")
            self.assertTrue(self.accepts("statement-read-response", policy))
            self.assertFalse(self.accepts("statement-read-response", {**trial, "lines": policy["lines"]}))
            self.assertFalse(self.accepts("statement-read-response", {**policy, "lines": trial["lines"]}))

    def test_complete_statements_require_reconciliation_lineage(self):
        body = fixture("statement-trial_balance-response")
        for status in ("UNRECONCILED", "UNAVAILABLE"):
            self.assertFalse(self.accepts("statement-read-response", {**body, "reconciliation": {"status": status}}))
        for key in ("trial_balance_data_version", "policy_ref"):
            changed = copy.deepcopy(body); changed["reconciliation"].pop(key)
            self.assertFalse(self.accepts("statement-read-response", changed))
        self.assertTrue(self.accepts("statement-read-response", {**body, "completeness": "partial",
                         "reconciliation": {"status": "UNAVAILABLE"}}))

    def test_withheld_results_do_not_carry_financial_rows_or_continuation(self):
        ledger = fixture("ledger-balances-response")
        self.assertFalse(self.accepts("ledger-read-response", {**ledger, "completeness": "withheld"}))
        withheld = {**ledger, "completeness": "withheld", "items": []}
        self.assertTrue(self.accepts("ledger-read-response", withheld))
        self.assertFalse(self.accepts("ledger-read-response", {**withheld, "next_cursor": "next"}))
        statement = fixture("statement-trial_balance-response")
        self.assertFalse(self.accepts("statement-read-response", {**statement, "completeness": "withheld"}))

    def test_responses_require_provenance_and_erp_owned_baseline(self):
        for name, file in (("ledger-read-response", "ledger-balances-response"),
                           ("statement-read-response", "statement-trial_balance-response")):
            body = fixture(file)
            for key in ("finance_baselines", "data_version", "snapshot_id", "observed_at", "completeness"):
                changed = copy.deepcopy(body); changed.pop(key)
                self.assertFalse(self.accepts(name, changed))
            changed = copy.deepcopy(body); changed["finance_baselines"][0]["authority"]["engine_id"] = "baobab-cp"
            self.assertFalse(self.accepts(name, changed))

    def test_caller_authority_and_native_ids_are_rejected_at_each_input_boundary(self):
        fields = ("tenant_id", "organisation_id", "legal_entity_id", "principal_id", "approved_by", "AD_Client_ID", "AD_Org_ID")
        for field in fields:
            for name,file in (("ledger-read-request", "ledger-entries-request"),
                              ("statement-read-request", "statement-trial_balance-request"),
                              ("journal-manage-request", "journal-create_draft-request")):
                body = fixture(file)
                self.assertFalse(self.accepts(name, {**body, field: "forged"}))
                nested = "draft" if name == "journal-manage-request" else "scope"
                changed = copy.deepcopy(body); changed[nested][field] = "forged"
                self.assertFalse(self.accepts(name, changed))
            changed = fixture("journal-create_draft-request"); changed["draft"]["lines"][0][field] = "forged"
            self.assertFalse(self.accepts("journal-manage-request", changed))

    def test_journal_response_echo_and_reversal_reference(self):
        body = fixture("journal-post-response")
        self.assertFalse(self.accepts("journal-manage-response", {**body, "status": "DRAFT"}))
        body = fixture("journal-reverse-response"); body.pop("reversal_journal_ref")
        self.assertFalse(self.accepts("journal-manage-response", body))

    def test_unknown_cross_schema_urls_fail_offline(self):
        with self.assertRaises(Unresolvable):
            self.resources.resolver().lookup("https://untrusted.invalid/finance.schema.json")


if __name__ == "__main__":
    unittest.main()
