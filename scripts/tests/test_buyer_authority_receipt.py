#!/usr/bin/env python3
"""Buyer-authority receipt and its single consumption (trade/v2, ADR-SHARED-042 sections 9 and 12).

Static boundary plus a reference model of the rules JSON Schema cannot
express: a receipt is derived only from an ALLOW buyer execution context for
a committing operation, it lives at most 60 seconds and never outlives its
context, and a native commit fence consumes it at most once, only together
with a seller receipt for the same operation reference and only while every
bound fact still equals the native record. Trade's fence must agree with this
model; a schema-valid receipt is never authority by itself.
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
SCHEMA_ID = "https://contracts.baobab-platform.com/trade/v2/buyer-authority-receipt.schema.json"
EXAMPLES = CONTRACTS / "trade/v2/examples"
CONTEXT = json.loads((EXAMPLES / "buyer-execution-context-order-commit-allow.json").read_text())
RECEIPT = json.loads((EXAMPLES / "buyer-authority-receipt-order-commit.json").read_text())
CONSUMPTION = json.loads((EXAMPLES / "buyer-authority-consumption.json").read_text())

# Facts a receipt copies from its context and that must still equal the native record.
BOUND = (
    "context_id", "decision_id", "correlation_id", "operation", "actor_principal_id", "tenant_id",
    "canonical_organisation_id", "buyer_organisation_id", "buyer_membership_id", "membership_revision",
    "market_id", "resource_id", "resource_version", "transaction_digest", "amount_minor", "currency",
    "policy_revision", "seller_legal_entity_id", "seller_binding_reference",
)
NATIVE = ("resource_id", "resource_version", "transaction_digest", "amount_minor", "currency", "market_id")


def registry():
    result = Registry()
    for path in CONTRACTS.rglob("*.json"):
        doc = json.loads(path.read_text())
        if isinstance(doc, dict) and isinstance(doc.get("$id"), str):
            result = result.with_resource(doc["$id"], Resource.from_contents(doc))
    return result


REGISTRY = registry()


def errors(definition, document):
    validator = Draft202012Validator({"$ref": f"{SCHEMA_ID}#/$defs/{definition}"}, registry=REGISTRY,
                                     format_checker=FormatChecker())
    return list(validator.iter_errors(document))


def changed(document, **change):
    result = copy.deepcopy(document)
    for key, value in change.items():
        if value is None:
            result.pop(key, None)
        else:
            result[key] = value
    return result


def at(text):
    return datetime.fromisoformat(text.replace("Z", "+00:00"))


def issuable(context, receipt):
    """A receipt may exist only for an ALLOW, committing context and must copy it exactly."""
    if context["decision"]["outcome"] != "ALLOW":
        return False
    if context["operation"] not in ("trade.order.commit", "trade.draft-order.finalize"):
        return False
    if any(receipt.get(k) != context.get(k) for k in BOUND):
        return False
    evaluated, expires = at(receipt["evaluated_at"]), at(receipt["expires_at"])
    return evaluated < expires <= evaluated + timedelta(seconds=60) and expires <= at(context["expires_at"])


class Fence:
    """Reference model of the native commit fence's buyer side."""

    def __init__(self):
        self.consumed = {}

    def consume(self, receipt, *, now, native, seller_receipt, reservation, membership_revision, organisation_id):
        if receipt["buyer_organisation_id"] != organisation_id:
            return "FOREIGN_RECEIPT"
        if receipt["receipt_id"] in self.consumed:
            return "RECEIPT_CONSUMED"
        if now >= at(receipt["expires_at"]):
            return "RECEIPT_EXPIRED"
        if membership_revision != receipt["membership_revision"]:
            return "MEMBERSHIP_REVISED"
        if any(native[k] != receipt[k] for k in NATIVE):
            return "TRANSACTION_MISMATCH"
        if seller_receipt is None or seller_receipt["operation_reference"] != receipt["operation_reference"]:
            return "SELLER_RECEIPT_ABSENT"
        if (reservation is None or reservation["id"] != receipt["spend_reservation_id"]
                or reservation["status"] != "ACTIVE" or now >= reservation["expires_at"]):
            return "RESERVATION_NOT_CURRENT"
        if reservation["hold_revision"] != receipt["spend_hold_revision"]:
            return "TRANSACTION_MISMATCH"
        self.consumed[receipt["receipt_id"]] = now
        return "CONSUMED"


class BuyerAuthorityReceipt(unittest.TestCase):
    def native(self, **change):
        return {**{k: RECEIPT[k] for k in NATIVE}, **change}

    def consume(self, fence, receipt=RECEIPT, **change):
        arguments = {
            "now": at(RECEIPT["evaluated_at"]) + timedelta(seconds=10),
            "native": self.native(),
            "seller_receipt": {"operation_reference": RECEIPT["operation_reference"]},
            "reservation": {"id": RECEIPT["spend_reservation_id"], "status": "ACTIVE", "hold_revision": 1,
                            "expires_at": at(RECEIPT["evaluated_at"]) + timedelta(days=1)},
            "membership_revision": RECEIPT["membership_revision"],
            "organisation_id": RECEIPT["buyer_organisation_id"],
        }
        arguments.update(change)
        return fence.consume(receipt, **arguments)

    def test_examples_are_valid_and_derived_from_the_context(self):
        self.assertEqual([], errors("BuyerAuthorityReceipt", RECEIPT))
        self.assertEqual([], errors("BuyerAuthorityConsumption", CONSUMPTION))
        self.assertTrue(issuable(CONTEXT, RECEIPT))
        self.assertEqual(CONSUMPTION["receipt_id"], RECEIPT["receipt_id"])
        self.assertEqual(CONSUMPTION["operation_reference"], RECEIPT["operation_reference"])

    def test_only_committing_operations_with_a_reservation_carry_a_receipt(self):
        for change in ({"operation": "trade.rfq.submit"}, {"operation": "trade.purchase-approval.decide"},
                       {"spend_reservation_id": None}, {"spend_reservation_id": "res_1"},
                       {"spend_hold_revision": None}, {"spend_hold_revision": 0},
                       {"amount_minor": 0}, {"seller_binding_reference": None}, {"operation_reference": None},
                       {"transaction_digest": "md5:abc"}, {"outcome": "ALLOW"}):
            with self.subTest(change=change):
                self.assertNotEqual([], errors("BuyerAuthorityReceipt", changed(RECEIPT, **change)))
        for change in ({"seller_receipt_id": None}, {"spend_reservation_id": None}, {"commitment_reference": ""}):
            with self.subTest(change=change):
                self.assertNotEqual([], errors("BuyerAuthorityConsumption", changed(CONSUMPTION, **change)))

    def test_no_receipt_without_an_allow_context_or_with_a_divergent_fact(self):
        approval = changed(CONTEXT, decision={"outcome": "APPROVAL_REQUIRED", "reasons": ["APPROVAL_THRESHOLD_EXCEEDED"]})
        self.assertFalse(issuable(approval, RECEIPT))
        self.assertFalse(issuable(changed(CONTEXT, operation="trade.cart.modify"), changed(RECEIPT, operation="trade.cart.modify")))
        for key in ("amount_minor", "resource_version", "membership_revision"):
            with self.subTest(key=key):
                self.assertFalse(issuable(CONTEXT, changed(RECEIPT, **{key: RECEIPT[key] + 1})))

    def test_lifetime_is_bounded_by_sixty_seconds_and_the_context(self):
        self.assertFalse(issuable(CONTEXT, changed(RECEIPT, expires_at="2026-10-21T12:01:01Z")))
        self.assertFalse(issuable(CONTEXT, changed(RECEIPT, expires_at="2026-10-21T12:00:31Z")))
        self.assertFalse(issuable(CONTEXT, changed(RECEIPT, expires_at=RECEIPT["evaluated_at"])))

    def test_a_receipt_is_consumed_once_and_only_with_its_seller_receipt(self):
        fence = Fence()
        self.assertEqual("SELLER_RECEIPT_ABSENT", self.consume(fence, seller_receipt=None))
        self.assertEqual("SELLER_RECEIPT_ABSENT",
                         self.consume(fence, seller_receipt={"operation_reference": "trade/trade.order.commit/cart_other/4/1"}))
        self.assertEqual("CONSUMED", self.consume(fence))
        self.assertEqual("RECEIPT_CONSUMED", self.consume(fence))

    def test_a_stale_or_changed_purchase_is_refused(self):
        late = at(RECEIPT["expires_at"])
        cases = {
            "RECEIPT_EXPIRED": {"now": late},
            "MEMBERSHIP_REVISED": {"membership_revision": RECEIPT["membership_revision"] + 1},
            "TRANSACTION_MISMATCH": {"native": self.native(amount_minor=RECEIPT["amount_minor"] + 1)},
            "RESERVATION_NOT_CURRENT": {"reservation": None},
            "FOREIGN_RECEIPT": {"organisation_id": "b2borg_foreign01"},
        }
        for expected, change in cases.items():
            with self.subTest(expected=expected):
                self.assertEqual(expected, self.consume(Fence(), **change))
        rolled = {"id": RECEIPT["spend_reservation_id"], "status": "ACTIVE", "hold_revision": 2,
                  "expires_at": late + timedelta(days=1)}
        self.assertEqual("TRANSACTION_MISMATCH", self.consume(Fence(), reservation=rolled))
        expired_hold = {"id": RECEIPT["spend_reservation_id"], "status": "ACTIVE", "hold_revision": 1,
                        "expires_at": at(RECEIPT["evaluated_at"])}
        self.assertEqual("RESERVATION_NOT_CURRENT", self.consume(Fence(), reservation=expired_hold))
        committed = {"id": RECEIPT["spend_reservation_id"], "status": "COMMITTED", "hold_revision": 1,
                     "expires_at": late + timedelta(days=1)}
        self.assertEqual("RESERVATION_NOT_CURRENT", self.consume(Fence(), reservation=committed))

    def test_every_refusal_is_a_registered_reason(self):
        schema = json.loads((CONTRACTS / "trade/v2/buyer-authority-receipt.schema.json").read_text())
        refusals = set(schema["$defs"]["consumptionRefusal"]["enum"])
        self.assertEqual({"RECEIPT_EXPIRED", "RECEIPT_CONSUMED", "MEMBERSHIP_REVISED", "TRANSACTION_MISMATCH",
                          "SELLER_RECEIPT_ABSENT", "RESERVATION_NOT_CURRENT", "FOREIGN_RECEIPT"}, refusals)
        reasons = set(json.loads((CONTRACTS / "trade/v2/buyer-execution-context.schema.json").read_text())
                      ["$defs"]["decisionReason"]["enum"])
        for reason in ("CONTEXT_NOT_USABLE", "TRANSACTION_CHANGED", "SELLER_AUTHORITY_ABSENT", "BUYER_NOT_AUTHORISED"):
            self.assertIn(reason, reasons)


if __name__ == "__main__":
    unittest.main()
