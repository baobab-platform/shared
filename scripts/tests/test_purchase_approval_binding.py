"""Shape checks for the proposed Trade purchase approval binding."""

import copy
import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

CONTRACTS = Path(__file__).resolve().parents[2] / "contracts"
SCHEMA_PATH = "trade/v2/purchase-approval-binding.schema.json"
SCHEMA = json.loads((CONTRACTS / SCHEMA_PATH).read_text())
SOURCES = (
    "control-plane/v1/domain.schema.json",
    "organisation/v2/domain.schema.json",
    "trade/v2/buyer-execution-context.schema.json",
)
REGISTRY = Registry()
for source in SOURCES:
    dependency = json.loads((CONTRACTS / source).read_text())
    REGISTRY = REGISTRY.with_resource(dependency["$id"], Resource.from_contents(dependency))
VALIDATOR = Draft202012Validator(SCHEMA, registry=REGISTRY, format_checker=FormatChecker())

BINDING = {
    "operation": "trade.purchase-approval.decide",
    "intended_decision": "APPROVED",
    "attempt_id": "0b6f2c1e-6d0a-4f43-9c1a-2f1d6b1e9a40",
    "authentication_binding": "sha256:" + "a" * 64,
    "approver_principal_id": "019a0915-a8c0-7000-8000-000000000001",
    "initiator_principal_id": "019a0915-a8c0-7000-8000-000000000002",
    "tenant_id": "tn_synthetic01",
    "seller_legal_entity_id": "SYNTHETIC-LE-01",
    "canonical_organisation_id": "2c8e4f6a-1b3d-4e5f-8a7c-9d0e1f2a3b4c",
    "market_id": "zuribeans_ug",
    "approval_id": "b2bapr_synthetic01",
    "approval_revision": 1,
    "purchase": {"kind": "QUOTATION", "id": "quote_synthetic01", "version": 4},
    "amount_minor": 1250000,
    "currency": "UGX",
    "transaction_digest": "sha256:" + "b" * 64,
    "step_up_rule": {
        "policy_revision": "synthetic:1",
        "threshold_minor": 1000000,
        "comparison": "AT_OR_ABOVE",
    },
    "authority_digest": "sha256:" + "c" * 64,
}


class PurchaseApprovalBindingTests(unittest.TestCase):
    def test_closed_versioned_shape_and_supported_purchase_sources(self):
        Draft202012Validator.check_schema(SCHEMA)
        self.assertTrue(VALIDATOR.is_valid(BINDING))
        cart = {"kind": "CART", "id": "cart_synthetic01", "version": 2}
        self.assertTrue(VALIDATOR.is_valid(dict(BINDING, purchase=cart)))

    def test_every_binding_fact_is_required(self):
        for key in BINDING:
            with self.subTest(key=key):
                incomplete = dict(BINDING)
                del incomplete[key]
                self.assertFalse(VALIDATOR.is_valid(incomplete))

    def test_rejects_wrong_operation_and_unbound_claims(self):
        for changes in (
            {"operation": "trade.order.commit"},
            {"operation": "HIGH_VALUE_APPROVAL"},
            {"intended_decision": "REJECTED"},
            {"browser_amount": 1},
            {"access_token": "raw"},
            {"authentication_binding": "opaque-session"},
            {"seller_legal_entity_id": "legacy_alias"},
            {"currency": "ugx"},
            {"approval_revision": 0},
            {"amount_minor": 9007199254740992},
        ):
            with self.subTest(changes=changes):
                self.assertFalse(VALIDATOR.is_valid(dict(BINDING, **changes)))

    def test_rejects_missing_quote_version_and_missing_threshold_rule(self):
        for container, key in (("purchase", "version"), ("step_up_rule", "threshold_minor"),
                               ("step_up_rule", "comparison")):
            with self.subTest(container=container, key=key):
                incomplete = copy.deepcopy(BINDING)
                del incomplete[container][key]
                self.assertFalse(VALIDATOR.is_valid(incomplete))


if __name__ == "__main__":
    unittest.main()
