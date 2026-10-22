#!/usr/bin/env python3
"""TradeBuyerExecutionContext (trade/v2, ADR-SHARED-042 section 7, CAA-01).

Static boundary only: a schema-valid context is never authority by itself.
Trade must derive every field from verified IAM, CP and Trade facts at
evaluation time, and buyer ALLOW never executes without the seller decision
and a native fence.
"""
import copy
from datetime import datetime, timedelta
import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[2]
CONTRACTS = ROOT / "contracts"
SCHEMA_ID = "https://contracts.baobab-platform.com/trade/v2/buyer-execution-context.schema.json"
EXAMPLES = CONTRACTS / "trade/v2/examples"
ALLOW = json.loads((EXAMPLES / "buyer-execution-context-order-commit-allow.json").read_text())
APPROVAL = json.loads((EXAMPLES / "buyer-execution-context-approval-required.json").read_text())


def registry():
    result = Registry()
    for path in CONTRACTS.rglob("*.json"):
        doc = json.loads(path.read_text())
        if isinstance(doc, dict) and isinstance(doc.get("$id"), str):
            result = result.with_resource(doc["$id"], Resource.from_contents(doc))
    return result


CONTEXT_REASONS = json.loads((CONTRACTS / "trade/v2/buyer-execution-context.schema.json").read_text())["$defs"]["decisionReason"]["enum"]
VALIDATOR = Draft202012Validator({"$ref": SCHEMA_ID}, registry=registry(), format_checker=FormatChecker())


def errors(document):
    return list(VALIDATOR.iter_errors(document))


def changed(**change):
    document = copy.deepcopy(ALLOW)
    for key, value in change.items():
        if value is None:
            document.pop(key, None)
        else:
            document[key] = value
    return document


def lifetime_ok(document):
    """The 60-second ceiling JSON Schema cannot express (section 7)."""
    parse = lambda value: datetime.fromisoformat(value.replace("Z", "+00:00"))
    evaluated, expires = parse(document["evaluated_at"]), parse(document["expires_at"])
    return evaluated < expires <= evaluated + timedelta(seconds=60)


class BuyerExecutionContext(unittest.TestCase):
    def test_examples_are_valid_and_bounded(self):
        for document in (ALLOW, APPROVAL):
            with self.subTest(outcome=document["decision"]["outcome"]):
                self.assertEqual([], errors(document))
                self.assertTrue(lifetime_ok(document))

    def test_only_a_verified_human_actor_is_defined(self):
        for change in [{"actor_type": "WORKLOAD"}, {"actor_type": "human"}, {"actor_principal_id": "cus_01"},
                       {"actor_principal_id": None}, {"external_identity_id": None}]:
            with self.subTest(change=change):
                self.assertNotEqual([], errors(changed(**change)))

    def test_no_identity_shortcut_or_unknown_field_is_accepted(self):
        for key, value in [("customer_id", "cus_01"), ("email", "buyer@example.test"), ("medusa_token", "x"),
                           ("iam_organisation", "acme"), ("permissions", ["*"])]:
            with self.subTest(key=key):
                self.assertNotEqual([], errors(changed(**{key: value})))

    def test_membership_and_organisation_binding_are_required(self):
        for key in ["canonical_organisation_id", "buyer_organisation_id", "buyer_membership_id", "membership_revision",
                    "tenant_id", "cp_context_id", "policy_revision", "evidence_references"]:
            with self.subTest(missing=key):
                self.assertNotEqual([], errors(changed(**{key: None})))
        self.assertNotEqual([], errors(changed(buyer_organisation_id="2c8e4f6a-1b3d-4e5f-8a7c-9d0e1f2a3b4c")))
        self.assertNotEqual([], errors(changed(canonical_organisation_id="b2borg_synthetic01")))

    def test_order_commitment_binds_market_transaction_and_seller(self):
        for key in ["market_id", "resource_id", "resource_version", "transaction_digest", "amount_minor", "currency",
                    "seller_legal_entity_id", "seller_binding_reference"]:
            with self.subTest(missing=key):
                self.assertNotEqual([], errors(changed(**{key: None})))
        self.assertNotEqual([], errors(changed(transaction_digest="md5:abc")))

    def test_a_read_needs_no_transaction_facts(self):
        read = changed(operation="trade.private-catalogue.view", resource_id=None, resource_version=None,
                       transaction_digest=None, amount_minor=None, currency=None, seller_legal_entity_id=None,
                       seller_binding_reference=None, market_id=None)
        self.assertEqual([], errors(read))

    def test_decision_outcomes_and_reasons_are_closed_and_consistent(self):
        for decision in [{"outcome": "ALLOW", "reasons": ["SPEND_LIMIT_EXCEEDED"]},
                         {"outcome": "DENY", "reasons": []},
                         {"outcome": "PERMIT", "reasons": []},
                         {"outcome": "DENY", "reasons": ["CUSTOMER_IS_VIP"]},
                         {"outcome": "ALLOW"}]:
            with self.subTest(decision=decision):
                self.assertNotEqual([], errors(changed(decision=decision)))
        for decision in [{"outcome": "SELECTION_REQUIRED", "reasons": ["ORGANISATION_SELECTION_REQUIRED"]},
                         {"outcome": "UNAVAILABLE", "reasons": ["SOURCE_UNAVAILABLE"]},
                         {"outcome": "DENY", "reasons": ["SEPARATION_OF_DUTIES"]}]:
            with self.subTest(decision=decision):
                self.assertEqual([], errors(changed(decision=decision)))

    def test_missing_policy_is_distinct_from_an_exceeded_one(self):
        # ADR-SHARED-042 section 14, CAA-05 ruling: an absent spend or approver
        # limit is never unlimited authority, and is reported apart from an
        # applicable limit that the amount exceeds.
        reasons = CONTEXT_REASONS
        for missing, exceeded in (("SPEND_POLICY_NOT_CONFIGURED", "SPEND_LIMIT_EXCEEDED"),
                                  ("APPROVAL_AUTHORITY_NOT_CONFIGURED", "APPROVAL_THRESHOLD_EXCEEDED")):
            self.assertIn(missing, reasons)
            self.assertIn(exceeded, reasons)
            self.assertEqual([], errors(changed(decision={"outcome": "DENY", "reasons": [missing]})))
            self.assertNotEqual([], errors(changed(decision={"outcome": "ALLOW", "reasons": [missing]})))

    def test_lifetime_ceiling_is_sixty_seconds(self):
        self.assertFalse(lifetime_ok(changed(expires_at="2026-10-21T12:01:01Z")))
        self.assertFalse(lifetime_ok(changed(expires_at="2026-10-21T12:00:00Z")))


if __name__ == "__main__":
    unittest.main()
