#!/usr/bin/env python3
"""Buyer commitment valuation (trade/v2, ADR-SHARED-042 section 14, Decision 7).

Static boundary plus the reference model of what JSON Schema cannot express:
the amount is the sum of its components, a discount is a negative component
and tender is never one, a FINAL basis has only final components, and the
valuation digest is the canonical SHA-256 of the binding fields. Trade's
valuation must agree with this model.
"""
import copy
import hashlib
import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[2]
CONTRACTS = ROOT / "contracts"
SCHEMA_ID = "https://contracts.baobab-platform.com/trade/v2/buyer-commitment-valuation.schema.json"
EXAMPLES = CONTRACTS / "trade/v2/examples"
VALUATION = json.loads((EXAMPLES / "buyer-commitment-valuation-order-commit.json").read_text())
CONTEXT = json.loads((EXAMPLES / "buyer-execution-context-order-commit-allow.json").read_text())
RECEIPT = json.loads((EXAMPLES / "buyer-authority-receipt-order-commit.json").read_text())
SCHEMA = json.loads((CONTRACTS / "trade/v2/buyer-commitment-valuation.schema.json").read_text())


def registry():
    result = Registry()
    for path in CONTRACTS.rglob("*.json"):
        doc = json.loads(path.read_text())
        if isinstance(doc, dict) and isinstance(doc.get("$id"), str):
            result = result.with_resource(doc["$id"], Resource.from_contents(doc))
    return result


REGISTRY = registry()


def errors(document, definition="BuyerCommitmentValuation"):
    validator = Draft202012Validator({"$ref": f"{SCHEMA_ID}#/$defs/{definition}"}, registry=REGISTRY,
                                     format_checker=FormatChecker())
    return list(validator.iter_errors(document))


def digest(valuation):
    """The canonical valuation digest (reference implementation)."""
    binding = {
        "basis": valuation["basis"],
        "buyer_commitment_amount_minor": valuation["buyer_commitment_amount_minor"],
        "components": sorted(
            ({k: c[k] for k in ("component_kind", "amount_minor", "determination", "source_reference")}
             for c in valuation["components"]),
            key=lambda c: (c["component_kind"], c["source_reference"])),
        "currency": valuation["currency"],
        "maximum_commitment_reference": valuation.get("maximum_commitment_reference"),
        "resource_id": valuation["resource_id"],
        "resource_version": valuation["resource_version"],
        "transaction_digest": valuation["transaction_digest"],
    }
    canonical = json.dumps(binding, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return "sha256:" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def coherent(valuation):
    """Semantic rules beyond the schema."""
    components = valuation["components"]
    if sum(c["amount_minor"] for c in components) != valuation["buyer_commitment_amount_minor"]:
        return False
    if not any(c["component_kind"] == "MERCHANDISE" for c in components):
        return False
    if valuation["basis"] == "FINAL_PRICED" and any(c["determination"] != "FINAL" for c in components):
        return False
    return valuation["valuation_digest"] == digest(valuation)


def valued(components, **change):
    result = copy.deepcopy(VALUATION)
    result["components"] = components
    result["buyer_commitment_amount_minor"] = sum(c["amount_minor"] for c in components)
    result.update(change)
    result["valuation_digest"] = digest(result)
    return result


def component(kind, amount, ref, determination="FINAL"):
    return {"component_kind": kind, "amount_minor": amount, "determination": determination, "source_reference": ref}


class BuyerCommitmentValuation(unittest.TestCase):
    def test_example_is_valid_coherent_and_bound_everywhere(self):
        self.assertEqual([], errors(VALUATION))
        self.assertTrue(coherent(VALUATION))
        for document in (CONTEXT, RECEIPT):
            with self.subTest(document=document.get("receipt_id", "context")):
                self.assertEqual(document["valuation_digest"], VALUATION["valuation_digest"])
                self.assertEqual(document["amount_minor"], VALUATION["buyer_commitment_amount_minor"])
                self.assertEqual(document["currency"], VALUATION["currency"])
                self.assertEqual(document["transaction_digest"], VALUATION["transaction_digest"])
                self.assertEqual(document["resource_version"], VALUATION["resource_version"])

    def test_the_ruling_example_reserves_the_whole_obligation(self):
        # Decision 7: R40,000 merchandise, R2,000 discount, R2,000 shipping and handling and
        # R6,000 VAT commit R46,000, even if only R10,000 is paid now (tender is no component).
        zar = valued([
            component("MERCHANDISE", 4_000_000, "line_synthetic_coffee"),
            component("ORDER_DISCOUNT", -200_000, "adjustment_synthetic_volume"),
            component("SHIPPING", 150_000, "shipping_synthetic_road"),
            component("HANDLING", 50_000, "shipping_synthetic_handling"),
            component("TAX", 600_000, "tax_synthetic_vat"),
        ], currency="ZAR")
        self.assertEqual([], errors(zar))
        self.assertTrue(coherent(zar))
        self.assertEqual(4_600_000, zar["buyer_commitment_amount_minor"])
        subtotal_only = copy.deepcopy(zar)
        subtotal_only["buyer_commitment_amount_minor"] = 4_000_000
        self.assertFalse(coherent(subtotal_only))

    def test_tender_is_never_a_component(self):
        for kind in ("GIFT_CARD", "STORE_CREDIT", "WALLET", "PAYMENT_ON_ACCOUNT", "DEPOSIT_COLLECTED", "CREDIT_TERMS"):
            with self.subTest(kind=kind):
                tendered = valued(VALUATION["components"] + [component(kind, -100, "tender_synthetic")])
                self.assertNotEqual([], errors(tendered))

    def test_signs_are_fixed_by_kind(self):
        for bad in (component("ORDER_DISCOUNT", 1, "adjustment_x"), component("ITEM_DISCOUNT", 5, "adjustment_y"),
                    component("TAX", -1, "tax_x"), component("SHIPPING", -1, "shipping_x"),
                    component("MERCHANDISE", 1.5, "line_x")):
            with self.subTest(bad=bad):
                self.assertNotEqual([], errors(valued(VALUATION["components"] + [bad])))

    def test_an_estimate_or_unbounded_amount_never_authorises(self):
        estimate = copy.deepcopy(VALUATION)
        estimate["components"][0]["determination"] = "ESTIMATED"
        self.assertNotEqual([], errors(estimate))
        bounded = valued(VALUATION["components"][:1] + [component("TAX", 150_000, "tax_cap", "GOVERNED_MAXIMUM")])
        self.assertFalse(coherent(bounded))  # FINAL_PRICED with a maximum component
        governed = valued(bounded["components"], basis="GOVERNED_MAXIMUM", maximum_commitment_reference="mpc_synthetic01")
        self.assertEqual([], errors(governed))
        self.assertTrue(coherent(governed))
        missing = copy.deepcopy(governed)
        missing.pop("maximum_commitment_reference")
        self.assertNotEqual([], errors(missing))
        self.assertNotEqual([], errors(changed_ref(VALUATION)))

    def test_any_material_change_is_a_new_digest(self):
        base = digest(VALUATION)
        for change in ({"currency": "ZAR"}, {"resource_version": VALUATION["resource_version"] + 1},
                       {"transaction_digest": "sha256:" + "b" * 64}):
            with self.subTest(change=change):
                self.assertNotEqual(base, digest({**VALUATION, **change}))
        repriced = copy.deepcopy(VALUATION)
        repriced["components"][0]["amount_minor"] += 1
        repriced["buyer_commitment_amount_minor"] += 1
        self.assertNotEqual(base, digest(repriced))
        reordered = copy.deepcopy(VALUATION)
        reordered["components"].reverse()
        self.assertEqual(base, digest(reordered))
        self.assertFalse(coherent({**VALUATION, "valuation_digest": "sha256:" + "0" * 64}))

    def test_amount_must_be_the_component_sum(self):
        self.assertFalse(coherent({**VALUATION, "buyer_commitment_amount_minor": VALUATION["buyer_commitment_amount_minor"] - 1}))
        self.assertFalse(coherent(valued([component("SHIPPING", 1000, "shipping_only")])))
        self.assertNotEqual([], errors({**VALUATION, "buyer_commitment_amount_minor": 0}))


def changed_ref(valuation):
    result = copy.deepcopy(valuation)
    result["maximum_commitment_reference"] = "mpc_synthetic01"
    return result


if __name__ == "__main__":
    unittest.main()
