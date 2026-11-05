#!/usr/bin/env python3
"""DEV-07 bounded observer validator mutation regressions.

All observations here are invented test vectors, not runtime receipts.
"""
import copy
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location(
    "dev07_transaction_gate", ROOT / "scripts/dev07_transaction_gate.py")
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)

SHA = "a" * 40
DIGEST = "sha256:" + "b" * 64
SELLER = "11111111-1111-4111-8111-111111111111"
BUYER = "22222222-2222-4222-8222-222222222222"
RESERVATION = "33333333-3333-4333-8333-333333333333"
EVENT = "44444444-4444-4444-8444-444444444444"


def vector():
    order = {
        "id": "order_dev07_test", "tenant_id": "tn_dev07_test",
        "buyer_organisation_id": "org_test_buyer",
        "seller_legal_entity_id": "le_test_seller",
        "operation_reference": "trade/trade.order.commit/cart_dev07_test/1/1",
        "txid": "8735", "draft": False, "status": "PLACED", "count": 1,
        "amount_minor": 32400, "currency": "USD",
    }
    negatives = {}
    for key in gate.NEGATIVE_IDS:
        negatives[key] = {
            "status": "PASS", "prohibited_effect_count": 0,
            "eligible_effect_count": int(key in gate.RECOVERY_CASES),
            "retry_count": 1, "retry_limit": 3,
        }
    return {
        "schema_version": "baobab.dev07.transaction-readback.v1",
        "evidence_class": "SCHEMA_TEST_VECTOR",
        "scenario": "DEV-07/INT-05",
        "source_revisions": dict.fromkeys(("trade", "cp", "iam", "infrastructure", "erp"), SHA),
        "observer": {
            "kind": "SCHEMA_TEST_VECTOR",
            "artifact_url": "https://github.com/baobab-platform/infrastructure/actions/runs/12345",
            "artifact_sha256": DIGEST,
        },
        "positive_status": "OBSERVED",
        "observations": {
            "readback_source": "POSTGRESQL_INDEPENDENT_READER",
            "order": order,
            "seller": {
                "receipt_id": SELLER, "order_id": order["id"],
                "operation_reference": order["operation_reference"], "txid": order["txid"], "count": 1,
            },
            "buyer": {
                "receipt_id": BUYER, "order_id": order["id"],
                "operation_reference": order["operation_reference"], "txid": order["txid"], "count": 1,
            },
            "spend": {
                "reservation_id": RESERVATION, "order_id": order["id"],
                "txid": order["txid"], "status": "COMMITTED", "count": 1,
                "amount_minor": order["amount_minor"], "currency": order["currency"],
            },
            "outbox": {
                "event_id": EVENT, "order_id": order["id"], "txid": order["txid"],
                "event_type": "com.baobab-platform.trade.order.placed.v1",
                "payload_sha256": DIGEST, "idempotency_key": "order_dev07_1",
                "count": 1, "immutable_readback": True,
            },
        },
        "downstream": {
            "status": "OBSERVED", "event_id": EVENT, "payload_sha256": DIGEST,
            "publisher_confirmed": True, "broker_delivered": True,
            "erp_inbox_durable": True, "erp_native_effect_count": 1,
            "exported_trace_observed": True,
        },
        "negatives": negatives,
        "claims": {
            "int05_qualified": False, "provider_qualified": False,
            "protected_acceptance": False, "production_authorized": False,
        },
    }


class Dev07ReadbackGate(unittest.TestCase):
    def test_clean_vector_can_never_be_runtime_acceptance(self):
        self.assertEqual(("TEST_VECTOR_ONLY", []), gate.disposition(vector()))
        altered = vector()
        altered["evidence_class"] = "REAL_COMPONENT_SYNTHETIC_DATA"
        altered["observer"]["kind"] = "INDEPENDENT_READBACK"
        self.assertEqual(("CANDIDATE_INDEPENDENT_REVIEW", []), gate.disposition(altered))

    def test_blocked_is_not_success_even_with_an_observer(self):
        altered = vector()
        altered["evidence_class"] = "REAL_COMPONENT_SYNTHETIC_DATA"
        altered["observer"]["kind"] = "INDEPENDENT_READBACK"
        altered["positive_status"] = "BLOCKED"
        altered["observations"] = None
        altered["downstream"] = {
            "status": "BLOCKED", "event_id": None, "payload_sha256": None,
            "publisher_confirmed": False, "broker_delivered": False,
            "erp_inbox_durable": False, "erp_native_effect_count": 0,
            "exported_trace_observed": False,
        }
        altered["negatives"]["ambiguous_erp_outcome"]["status"] = "BLOCKED"
        self.assertEqual(("BLOCKED", []), gate.disposition(altered))

    def test_every_native_fact_must_share_transaction_and_order(self):
        for name in ("seller", "buyer", "spend", "outbox"):
            for field, value in (("txid", "8766"), ("order_id", "foreign_order")):
                with self.subTest(fact=name, field=field):
                    altered = vector()
                    altered["observations"][name][field] = value
                    self.assertEqual("INVALID", gate.disposition(altered)[0])

    def test_buyer_and_seller_operation_and_receipts_cannot_be_reused(self):
        for name in ("buyer", "seller"):
            altered = vector()
            altered["observations"][name]["operation_reference"] = "trade/foreign/cart/1"
            self.assertEqual("INVALID", gate.disposition(altered)[0])
        altered = vector()
        altered["observations"]["buyer"]["receipt_id"] = SELLER
        self.assertEqual("INVALID", gate.disposition(altered)[0])

    def test_outbox_cannot_be_forged_or_multiplied(self):
        for change in (("count", 2), ("immutable_readback", False),
                       ("event_type", "com.baobab-platform.trade.order.changed.v1")):
            altered = vector()
            altered["observations"]["outbox"][change[0]] = change[1]
            self.assertEqual("INVALID", gate.disposition(altered)[0])
        altered = vector()
        altered["downstream"]["payload_sha256"] = "sha256:" + "c" * 64
        self.assertEqual("INVALID", gate.disposition(altered)[0])
        altered = vector()
        altered["downstream"]["event_id"] = SELLER
        self.assertEqual("INVALID", gate.disposition(altered)[0])

    def test_spend_equals_full_order_obligation(self):
        for field, value in (("amount_minor", 1), ("currency", "ZAR"), ("count", 2)):
            altered = vector()
            altered["observations"]["spend"][field] = value
            self.assertEqual("INVALID", gate.disposition(altered)[0])

    def test_all_security_failures_and_recovery_cases_are_mandatory(self):
        for name in gate.NEGATIVE_IDS:
            with self.subTest(case=name):
                altered = vector()
                altered["negatives"].pop(name)
                self.assertEqual("INVALID", gate.disposition(altered)[0])
                altered = vector()
                altered["negatives"][name]["status"] = "BLOCKED"
                self.assertEqual("TEST_VECTOR_ONLY", gate.disposition(altered)[0])
                altered["evidence_class"] = "REAL_COMPONENT_SYNTHETIC_DATA"
                altered["observer"]["kind"] = "INDEPENDENT_READBACK"
                self.assertEqual("BLOCKED", gate.disposition(altered)[0])
                altered["negatives"][name]["status"] = "FAIL"
                self.assertEqual("INVALID", gate.disposition(altered)[0])

    def test_negative_prohibited_and_duplicate_effects_are_rejected(self):
        for name in gate.NEGATIVE_IDS:
            with self.subTest(case=name):
                altered = vector()
                altered["negatives"][name]["prohibited_effect_count"] = 1
                self.assertEqual("INVALID", gate.disposition(altered)[0])
                altered = vector()
                altered["negatives"][name]["eligible_effect_count"] = 2
                self.assertEqual("INVALID", gate.disposition(altered)[0])
                altered = vector()
                altered["negatives"][name]["retry_count"] = 4
                self.assertEqual("INVALID", gate.disposition(altered)[0])

    def test_broker_erp_and_trace_cannot_disappear_from_success(self):
        for field, value in (("publisher_confirmed", False), ("broker_delivered", False),
                             ("erp_inbox_durable", False), ("erp_native_effect_count", 0),
                             ("exported_trace_observed", False)):
            altered = vector()
            altered["downstream"][field] = value
            self.assertEqual("INVALID", gate.disposition(altered)[0])

    def test_no_private_payload_or_false_protected_promotion(self):
        for field, value in (("access_token", "secret"), ("order_price", 3.5),
                             ("production_authorized", True)):
            altered = vector()
            if field == "production_authorized":
                altered["claims"][field] = value
            else:
                altered[field] = value
            self.assertEqual("INVALID", gate.disposition(altered)[0])
        altered = vector()
        altered["source_revisions"]["trade"] = "latest"
        self.assertEqual("INVALID", gate.disposition(altered)[0])


if __name__ == "__main__":
    unittest.main()
