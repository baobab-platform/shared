#!/usr/bin/env python3
"""Buyer operation assurance policy (identity/v1, ADR-SHARED-042 CAA-03).

Pins the static boundary and a reference reading of the evaluation rules:
exact acr matching with no ordering, every listed method required, freshness
when bounded, and a canonical operation-to-profile mapping no policy can
downgrade. Whether a verified token is current, and which values IAM can
actually issue, remain runtime and IAM obligations.
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
SCHEMA_ID = "https://contracts.baobab-platform.com/identity/v1/assurance-policy.schema.json"
SCHEMA = json.loads((CONTRACTS / "identity/v1/assurance-policy.schema.json").read_text())
CONTEXT = json.loads((CONTRACTS / "trade/v2/buyer-execution-context.schema.json").read_text())
POLICY = json.loads((CONTRACTS / "identity/v1/examples/assurance-policy-synthetic.json").read_text())
NOW = datetime.fromisoformat("2026-10-22T12:00:00+00:00")


def registry():
    result = Registry()
    for path in CONTRACTS.rglob("*.json"):
        doc = json.loads(path.read_text())
        if isinstance(doc, dict) and isinstance(doc.get("$id"), str):
            result = result.with_resource(doc["$id"], Resource.from_contents(doc))
    return result


VALIDATOR = Draft202012Validator({"$ref": SCHEMA_ID}, registry=registry(), format_checker=FormatChecker())


def errors(document):
    return list(VALIDATOR.iter_errors(document))


def satisfies(policy, operation, claims, now=NOW):
    """Reference reading of ProfileRequirement for one verified token's claims."""
    if policy["status"] != "APPROVED" or claims.get("iss") != policy["issuer"]:
        return False
    requirement = policy["profiles"][policy["operation_profiles"][operation]]
    if claims.get("acr") not in requirement["accepted_acr_values"]:
        return False
    if not set(requirement.get("required_methods", [])) <= set(claims.get("amr", [])):
        return False
    age = requirement.get("max_authentication_age_seconds")
    if age is not None:
        if "auth_time" not in claims:
            return False
        authenticated = datetime.fromtimestamp(claims["auth_time"], NOW.tzinfo)
        if authenticated > now or now - authenticated > timedelta(seconds=age):
            return False
    return True


def approved():
    return dict(copy.deepcopy(POLICY), status="APPROVED", approval_reference="security-approval:synthetic")


def claims(**change):
    document = {"iss": POLICY["issuer"], "acr": "urn:example.test:acr:synthetic-strong", "amr": ["hwk"],
                "auth_time": int((NOW - timedelta(seconds=60)).timestamp())}
    document.update(change)
    return {k: v for k, v in document.items() if v is not None}


class AssurancePolicy(unittest.TestCase):
    def test_example_is_valid_and_synthetic(self):
        self.assertEqual([], errors(POLICY))
        self.assertEqual("DRAFT", POLICY["status"])
        self.assertTrue(POLICY["issuer"].endswith(".test"))

    def test_mapping_covers_every_buyer_operation_canonically(self):
        operations = set(CONTEXT["$defs"]["buyerOperation"]["enum"])
        properties = SCHEMA["$defs"]["BuyerAssurancePolicy"]["properties"]["operation_profiles"]
        self.assertEqual(operations, set(properties["required"]))
        self.assertEqual(operations, set(properties["properties"]))
        self.assertEqual({k: v["const"] for k, v in properties["properties"].items()},
                         SCHEMA["$defs"]["canonicalOperationProfiles"]["const"])
        for operation in ["trade.order.commit", "trade.draft-order.finalize", "trade.purchase-approval.decide"]:
            downgraded = copy.deepcopy(POLICY)
            downgraded["operation_profiles"][operation] = "BUYER_SESSION"
            with self.subTest(operation=operation):
                self.assertNotEqual([], errors(downgraded))
        missing = copy.deepcopy(POLICY)
        missing["operation_profiles"].pop("trade.order.commit")
        self.assertNotEqual([], errors(missing))
        unknown = copy.deepcopy(POLICY)
        unknown["operation_profiles"]["trade.everything"] = "BUYER_SESSION"
        self.assertNotEqual([], errors(unknown))

    def test_no_wildcard_ordering_or_unbounded_step_up(self):
        for change in [{"accepted_acr_values": []}, {"accepted_acr_values": None}, {"minimum_acr": "1"},
                       {"step_up_required": True, "max_authentication_age_seconds": None}]:
            policy = copy.deepcopy(POLICY)
            requirement = policy["profiles"]["BUYER_COMMITMENT"]
            for key, value in change.items():
                if value is None:
                    requirement.pop(key, None)
                else:
                    requirement[key] = value
            with self.subTest(change=change):
                self.assertNotEqual([], errors(policy))

    def test_policy_is_scoped_to_one_issuer_and_trade(self):
        for change in [{"audience": "baobab-control-plane"}, {"issuer": "not a uri"}, {"approval_reference": ""},
                       {"status": "ACTIVE"}, {"policy_version": 0}]:
            with self.subTest(change=change):
                self.assertNotEqual([], errors(dict(copy.deepcopy(POLICY), **change)))

    def test_reference_evaluation_fails_closed(self):
        policy = approved()
        self.assertTrue(satisfies(policy, "trade.order.commit", claims()))
        self.assertTrue(satisfies(policy, "trade.buyer-context.resolve",
                                  claims(acr="urn:example.test:acr:synthetic-session", amr=None, auth_time=None)))
        for change, operation in [({"acr": "urn:example.test:acr:synthetic-session"}, "trade.order.commit"),
                                  ({"acr": "urn:example.test:acr:synthetic-strong-ish"}, "trade.order.commit"),
                                  ({"acr": None}, "trade.buyer-context.resolve"),
                                  ({"amr": None}, "trade.order.commit"),
                                  ({"amr": ["pwd"]}, "trade.order.commit"),
                                  ({"auth_time": None}, "trade.order.commit"),
                                  ({"auth_time": int((NOW - timedelta(seconds=901)).timestamp())}, "trade.order.commit"),
                                  ({"auth_time": int((NOW + timedelta(seconds=30)).timestamp())}, "trade.order.commit"),
                                  ({"iss": "https://other.example.test"}, "trade.buyer-context.resolve")]:
            with self.subTest(change=change, operation=operation):
                self.assertFalse(satisfies(policy, operation, claims(**change)))
        self.assertFalse(satisfies(POLICY, "trade.buyer-context.resolve", claims()))  # DRAFT is never enforced

    def test_failures_map_to_execution_context_reasons(self):
        reasons = CONTEXT["$defs"]["decisionReason"]["enum"]
        self.assertIn("ASSURANCE_INSUFFICIENT", reasons)
        self.assertIn("OPERATION_NOT_ACTIVATED", reasons)
        self.assertIn("OPERATION_NOT_ACTIVATED", SCHEMA["description"])


if __name__ == "__main__":
    unittest.main()
