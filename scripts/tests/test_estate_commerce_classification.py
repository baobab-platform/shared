#!/usr/bin/env python3
"""Estate commerce profile and native commitment classification (ADR-SHARED-042 section 14, Decision 8).

Static boundary plus a reference model of the commit fence's classification
step: CP alone classifies the Digital Estate, Trade alone classifies the
native commitment from a current CP attestation and its own verified buyer
relationship, and the fence selects the B2B or B2C regime from that record.
No known classification means no native order commitment.
"""
import copy
from datetime import datetime, timedelta
import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource
import yaml

ROOT = Path(__file__).resolve().parents[2]
CONTRACTS = ROOT / "contracts"
CP_ID = "https://contracts.baobab-platform.com/control-plane/v1/estate-commerce-profile.schema.json"
TRADE_ID = "https://contracts.baobab-platform.com/trade/v2/native-commitment-classification.schema.json"
CP_SCHEMA = json.loads((CONTRACTS / "control-plane/v1/estate-commerce-profile.schema.json").read_text())
TRADE_SCHEMA = json.loads((CONTRACTS / "trade/v2/native-commitment-classification.schema.json").read_text())
API = yaml.safe_load((CONTRACTS / "control-plane/v1/estate-commerce-profile.openapi.yaml").read_text())
SCOPES = {s["name"]: s for s in yaml.safe_load((CONTRACTS / "authorization/v1/scope-registry.yaml").read_text())["scopes"]}
WORKLOADS = yaml.safe_load((CONTRACTS / "identity/v1/workload-registry.yaml").read_text())
PROFILE = json.loads((CONTRACTS / "control-plane/v1/examples/estate-commerce-profile-b2b.json").read_text())
ATTESTATION = json.loads((CONTRACTS / "control-plane/v1/examples/estate-commerce-profile-attestation.json").read_text())
CLASSIFICATION = json.loads((CONTRACTS / "trade/v2/examples/native-commitment-classification-b2b-cart.json").read_text())
CONTEXT = json.loads((CONTRACTS / "trade/v2/examples/buyer-execution-context-order-commit-allow.json").read_text())
PATH = "/internal/estate/v1/commerce-profiles/resolve"


def registry():
    result = Registry()
    for path in CONTRACTS.rglob("*.json"):
        doc = json.loads(path.read_text())
        if isinstance(doc, dict) and isinstance(doc.get("$id"), str):
            result = result.with_resource(doc["$id"], Resource.from_contents(doc))
    return result


REGISTRY = registry()


def errors(schema_id, definition, document):
    validator = Draft202012Validator({"$ref": f"{schema_id}#/$defs/{definition}"}, registry=REGISTRY,
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


def bounded(attestation):
    """expires_at is within 60 seconds and never after the profile stops being effective."""
    issued, expires = at(attestation["issued_at"]), at(attestation["expires_at"])
    ceiling = issued + timedelta(seconds=60)
    if "profile_effective_until" in attestation:
        ceiling = min(ceiling, at(attestation["profile_effective_until"]))
    return issued < expires <= ceiling


B2C = changed(CLASSIFICATION, commerce_model="B2C", buyer_account_model="CONSUMER", consumer_reference="consumer_synthetic01",
              buyer_organisation_id=None, buyer_membership_id=None)


def fence(classification, *, profile, cp_available=True, original_model=None, buyer_authority=True, seller_receipt=True):
    """Reference model of the fence's classification step. Returns the regime or a refusal."""
    if classification is None or classification["status"] != "ACTIVE":
        return "CLASSIFICATION_ABSENT"
    if not cp_available:
        return "PROFILE_UNAVAILABLE"
    if (profile is None or profile["status"] != "ACTIVE"
            or profile["commerce_profile_id"] != classification["commerce_profile_id"]
            or profile["revision"] < classification["profile_revision"]):
        return "PROFILE_NOT_ACTIVE"
    if profile["commerce_model"] != classification["commerce_model"]:
        return "CLASSIFICATION_CONFLICT"
    if original_model is not None and original_model != classification["commerce_model"]:
        return "CLASSIFICATION_CHANGED"
    if not seller_receipt:
        return "SELLER_AUTHORITY_ABSENT"
    if classification["commerce_model"] == "B2B":
        return "B2B_REGIME" if buyer_authority else "BUYER_AUTHORITY_ABSENT"
    return "B2C_REGIME"


class EstateCommerceClassification(unittest.TestCase):
    def test_examples_are_valid_and_consistent(self):
        self.assertEqual([], errors(CP_ID, "EstateCommerceProfile", PROFILE))
        self.assertEqual([], errors(CP_ID, "EstateCommerceProfileAttestation", ATTESTATION))
        self.assertEqual([], errors(TRADE_ID, "NativeCommitmentClassification", CLASSIFICATION))
        self.assertEqual([], errors(TRADE_ID, "NativeCommitmentClassification", B2C))
        for key in ("commerce_profile_id", "digital_estate_id", "tenant_id", "commerce_model"):
            self.assertEqual(ATTESTATION[key], PROFILE[key])
        self.assertEqual(ATTESTATION["profile_revision"], PROFILE["revision"])
        self.assertEqual(ATTESTATION["attestation_id"], CLASSIFICATION["profile_attestation_id"])
        for key in ("digital_estate_id", "tenant_id", "market_id", "buyer_organisation_id", "buyer_membership_id",
                    "seller_binding_reference", "resource_id"):
            self.assertEqual(CLASSIFICATION[key], CONTEXT[key])

    def test_attestation_is_short_lived_estate_context_only(self):
        issued, expires = at(ATTESTATION["issued_at"]), at(ATTESTATION["expires_at"])
        self.assertTrue(issued < expires <= issued + timedelta(seconds=60))
        self.assertTrue(bounded(ATTESTATION))
        ending = changed(ATTESTATION, profile_effective_until="2026-10-21T12:00:10Z")
        self.assertEqual([], errors(CP_ID, "EstateCommerceProfileAttestation", ending))
        self.assertFalse(bounded(ending))  # expires_at 12:00:50 outlives the profile
        self.assertTrue(bounded(changed(ending, expires_at="2026-10-21T12:00:10Z")))
        for key in CP_SCHEMA["$defs"]["EstateCommerceProfileAttestation"]["required"]:
            with self.subTest(missing=key):
                self.assertNotEqual([], errors(CP_ID, "EstateCommerceProfileAttestation", changed(ATTESTATION, **{key: None})))
        for change in ({"commerce_model": "MIXED"}, {"outcome": "ACTIVE"}, {"status": "ACTIVE"}, {"buyer_organisation_id": "b2borg_x"}):
            with self.subTest(change=change):
                self.assertNotEqual([], errors(CP_ID, "EstateCommerceProfileAttestation", changed(ATTESTATION, **change)))

    def test_profile_is_governed_and_has_no_mixed_or_default_model(self):
        for change in ({"commerce_model": "MIXED"}, {"commerce_model": None}, {"status": "PENDING"}, {"revision": 0},
                       {"market_scope": []}, {"approval_reference": None}, {"tenant_id": "tenant-1"}):
            with self.subTest(change=change):
                self.assertNotEqual([], errors(CP_ID, "EstateCommerceProfile", changed(PROFILE, **change)))
        self.assertEqual(["B2B", "B2C"], CP_SCHEMA["$defs"]["commerceModel"]["enum"])

    def test_the_caller_cannot_choose_the_model_tenant_or_profile(self):
        request = {"digital_estate_id": PROFILE["digital_estate_id"], "engine_instance_id": PROFILE["trade_engine_instance_id"],
                   "market_id": PROFILE["market_scope"][0], "correlation_id": "0b6f2c1e-6d0a-4f43-9c1a-2f1d6b1e9a40",
                   "estate_provenance": {"kind": "ESTATE_CLIENT_BINDING", "reference": "estate-binding-attestation:synthetic"}}
        self.assertEqual([], errors(CP_ID, "EstateCommerceProfileResolveRequest", request))
        for extra in ({"commerce_model": "B2C"}, {"tenant_id": "tn_other01"}, {"commerce_profile_id": PROFILE["commerce_profile_id"]},
                      {"revision": 9}):
            with self.subTest(extra=extra):
                self.assertNotEqual([], errors(CP_ID, "EstateCommerceProfileResolveRequest", {**request, **extra}))
        self.assertNotEqual([], errors(CP_ID, "EstateCommerceProfileResolveRequest", changed(request, estate_provenance=None)))
        self.assertNotEqual([], errors(CP_ID, "EstateCommerceProfileResolveRequest",
                                       {**request, "estate_provenance": {"kind": "SALES_CHANNEL", "reference": "zuribeans"}}))

    def test_conversions_and_replacements_name_their_parent(self):
        parent = {"parent_classification_id": "0d9c8b7a-6f5e-4d3c-8b2a-1f0e9d8c7b6a", "relation": "CONVERTED_FROM"}
        converted = changed(CLASSIFICATION, resource_type="order", resource_id="order_synthetic01", origin="CONVERTED", lineage=parent)
        self.assertEqual([], errors(TRADE_ID, "NativeCommitmentClassification", converted))
        replacement = changed(converted, origin="REPLACEMENT", lineage={**parent, "relation": "REPLACES"})
        self.assertEqual([], errors(TRADE_ID, "NativeCommitmentClassification", replacement))
        for document in (changed(converted, lineage=None), changed(replacement, lineage=None),
                         changed(converted, lineage={**parent, "relation": "REPLACES"}),
                         changed(replacement, lineage=parent),
                         changed(CLASSIFICATION, lineage=parent),  # a direct commitment names no parent
                         changed(CLASSIFICATION, origin=None), changed(CLASSIFICATION, origin="IMPORTED")):
            with self.subTest(origin=document.get("origin"), lineage=document.get("lineage")):
                self.assertNotEqual([], errors(TRADE_ID, "NativeCommitmentClassification", document))

    def test_b2b_and_b2c_are_positively_established_never_inferred(self):
        refused = [
            changed(CLASSIFICATION, buyer_membership_id=None),
            changed(CLASSIFICATION, buyer_organisation_id=None),
            changed(CLASSIFICATION, buyer_account_model="CONSUMER"),
            changed(CLASSIFICATION, consumer_reference="consumer_synthetic01"),
            changed(CLASSIFICATION, machine_mandate_reference="mandate_synthetic01"),  # both membership and mandate
            changed(B2C, consumer_reference=None),  # no Organisation is not proof of B2C
            changed(B2C, buyer_organisation_id=CLASSIFICATION["buyer_organisation_id"]),
            changed(B2C, buyer_account_model="BUYER_ORGANISATION"),
            changed(CLASSIFICATION, commerce_model="MIXED"),
            changed(CLASSIFICATION, resource_type="sales_channel"),
        ]
        for document in refused:
            with self.subTest(document={k: document.get(k) for k in ("commerce_model", "buyer_account_model")}):
                self.assertNotEqual([], errors(TRADE_ID, "NativeCommitmentClassification", document))
        mandate = changed(CLASSIFICATION, buyer_membership_id=None, machine_mandate_reference="mandate_synthetic01")
        self.assertEqual([], errors(TRADE_ID, "NativeCommitmentClassification", mandate))

    def test_fence_decision_table(self):
        suspended, revoked = changed(PROFILE, status="SUSPENDED"), changed(PROFILE, status="REVOKED")
        b2c_profile = changed(PROFILE, commerce_model="B2C")
        cases = [
            ("B2B_REGIME", dict(classification=CLASSIFICATION, profile=PROFILE)),
            ("B2C_REGIME", dict(classification=B2C, profile=b2c_profile)),
            ("CLASSIFICATION_ABSENT", dict(classification=None, profile=PROFILE)),
            ("CLASSIFICATION_ABSENT", dict(classification=changed(CLASSIFICATION, status="QUARANTINED"), profile=PROFILE)),
            ("PROFILE_NOT_ACTIVE", dict(classification=CLASSIFICATION, profile=suspended)),
            ("PROFILE_NOT_ACTIVE", dict(classification=CLASSIFICATION, profile=revoked)),
            ("PROFILE_NOT_ACTIVE", dict(classification=CLASSIFICATION, profile=None)),
            ("PROFILE_NOT_ACTIVE", dict(classification=CLASSIFICATION, profile=changed(PROFILE, revision=1))),
            ("CLASSIFICATION_CONFLICT", dict(classification=CLASSIFICATION, profile=b2c_profile)),
            ("CLASSIFICATION_CHANGED", dict(classification=CLASSIFICATION, profile=PROFILE, original_model="B2C")),
            ("PROFILE_UNAVAILABLE", dict(classification=CLASSIFICATION, profile=PROFILE, cp_available=False)),
            ("BUYER_AUTHORITY_ABSENT", dict(classification=CLASSIFICATION, profile=PROFILE, buyer_authority=False)),
            ("SELLER_AUTHORITY_ABSENT", dict(classification=B2C, profile=b2c_profile, seller_receipt=False)),
        ]
        for expected, arguments in cases:
            with self.subTest(expected=expected):
                self.assertEqual(expected, fence(**arguments))
        # A B2B commitment without buyer authority is never re-read as B2C.
        self.assertNotEqual("B2C_REGIME", fence(CLASSIFICATION, profile=b2c_profile, buyer_authority=False))

    def test_refusals_are_closed_and_mapped(self):
        self.assertEqual({"CLASSIFICATION_ABSENT", "PROFILE_NOT_ACTIVE", "CLASSIFICATION_CONFLICT", "CLASSIFICATION_CHANGED",
                          "PROFILE_UNAVAILABLE", "BUYER_AUTHORITY_ABSENT"},
                         set(TRADE_SCHEMA["$defs"]["classificationRefusal"]["enum"]))
        codes = CP_SCHEMA["$defs"]["EstateCommerceProfileDenialCode"]["enum"]
        responses = API["paths"][PATH]["post"]["responses"]
        self.assertIn("PROFILE_AMBIGUOUS", codes)
        self.assertIn("PROFILE_AMBIGUOUS", responses["409"]["description"])
        self.assertLessEqual({"200", "400", "401", "403", "404", "409", "503"}, set(responses))

    def test_operation_is_a_scoped_unallocated_control_plane_surface(self):
        operation = API["paths"][PATH]["post"]
        self.assertEqual([{"EstateCommerceWorkload": ["estate:commerce-profile:resolve"]}], operation["security"])
        scope = SCOPES["estate:commerce-profile:resolve"]
        self.assertEqual((["baobab-control-plane"], ["workload"], False),
                         (scope["audience"], scope["allowed_actors"], scope["grants_authority"]))
        for client_id, entry in WORKLOADS["workloads"].items():
            with self.subTest(workload=client_id):
                self.assertNotIn("estate:commerce-profile:resolve", entry.get("allowed_scopes", []))


if __name__ == "__main__":
    unittest.main()
