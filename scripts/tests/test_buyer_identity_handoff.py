#!/usr/bin/env python3
"""Buyer identity handoff (identity/v1): what Trade may accept from an estate BFF.

Schema validity is necessary, never sufficient: signature, issuer metadata,
expiry, client allowlisting, canonical Principal resolution and Trade buyer
membership remain runtime obligations. These tests pin the static boundary.
"""
import copy
import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource
import yaml

ROOT = Path(__file__).resolve().parents[2]
CONTRACTS = ROOT / "contracts"
SCHEMA_ID = "https://contracts.baobab-platform.com/identity/v1/buyer-identity-handoff.schema.json"
EXAMPLE = json.loads((CONTRACTS / "identity/v1/examples/buyer-identity-handoff.json").read_text())


def registry():
    result = Registry()
    for path in CONTRACTS.rglob("*.json"):
        doc = json.loads(path.read_text())
        if isinstance(doc, dict) and isinstance(doc.get("$id"), str):
            result = result.with_resource(doc["$id"], Resource.from_contents(doc))
    return result


REGISTRY = registry()
VALIDATOR = Draft202012Validator({"$ref": SCHEMA_ID}, registry=REGISTRY, format_checker=FormatChecker())


def errors(document):
    return list(VALIDATOR.iter_errors(document))


def changed(path, value):
    """The example with one field replaced (value None deletes it)."""
    document = copy.deepcopy(EXAMPLE)
    *parents, key = path
    target = document
    for parent in parents:
        target = target[parent]
    if value is None:
        del target[key]
    else:
        target[key] = value
    return document


class BuyerIdentityHandoff(unittest.TestCase):
    def test_example_is_valid(self):
        self.assertEqual([], errors(EXAMPLE))

    def test_token_must_be_a_human_trade_audience_token_for_trade_buy(self):
        for path, value in [
            (("access_token_claims", "aud"), "baobab-control-plane"),
            (("access_token_claims", "aud"), ["baobab-control-plane", "baobab-erp"]),
            (("access_token_claims", "scope"), "openid context:resolve"),
            (("access_token_claims", "scope"), "trade:buyer"),
            (("access_token_claims", "actor_type"), "workload"),
            (("access_token_claims", "azp"), None),
            (("access_token_claims", "sub"), None),
            (("access_token_claims", "jti"), None),
            (("access_token_claims", "exp"), None),
        ]:
            with self.subTest(path=path, value=value):
                self.assertNotEqual([], errors(changed(path, value)))

    def test_audience_and_scope_forms_that_are_valid(self):
        for path, value in [
            (("access_token_claims", "aud"), "baobab-trade"),
            (("access_token_claims", "aud"), ["baobab-trade", "baobab-control-plane"]),
            (("access_token_claims", "scope"), "trade:buy"),
            (("access_token_claims", "scope"), "trade:buy openid"),
        ]:
            with self.subTest(path=path, value=value):
                self.assertEqual([], errors(changed(path, value)))

    def test_request_carries_requests_only_never_asserted_identity(self):
        for key, value in [("tenant_id", "tn_zuribeans"), ("principal_id", "p"), ("buyer_membership_id", "m"),
                           ("roles", ["buyer-admin"])]:
            with self.subTest(key=key):
                self.assertNotEqual([], errors(changed(("request", key), value)))
        for path, value in [(("request", "correlation_id"), "trade-ctx/1"), (("request", "correlation_id"), None),
                            (("request", "requested_country_code"), "za"),
                            (("request", "requested_organisation_id"), "x")]:
            with self.subTest(path=path, value=value):
                self.assertNotEqual([], errors(changed(path, value)))
        self.assertEqual([], errors(changed(("request", "requested_organisation_id"), None)))

    def test_trade_buy_is_registered_human_only_and_grants_nothing(self):
        scopes = {s["name"]: s for s in yaml.safe_load((CONTRACTS / "authorization/v1/scope-registry.yaml").read_text())["scopes"]}
        self.assertEqual(scopes["trade:buy"]["audience"], ["baobab-trade"])
        self.assertEqual(scopes["trade:buy"]["allowed_actors"], ["human"])
        self.assertIs(scopes["trade:buy"]["grants_authority"], False)
        workloads = yaml.safe_load((CONTRACTS / "identity/v1/workload-registry.yaml").read_text())["workloads"]
        for name, entry in workloads.items():
            with self.subTest(workload=name):
                self.assertNotIn("trade:buy", entry["allowed_scopes"])

    def test_trade_b2b_security_scheme_is_provider_neutral(self):
        api = yaml.safe_load((CONTRACTS / "trade/v1/openapi.yaml").read_text())
        scheme = api["components"]["securitySchemes"]["humanOidc"]
        self.assertEqual(scheme["type"], "openIdConnect")
        self.assertTrue(scheme["openIdConnectUrl"].endswith("/.well-known/openid-configuration"))
        self.assertNotIn("realms/", json.dumps(scheme))
        self.assertEqual(api["security"], [{"humanOidc": ["trade:buy"]}])


def definition_errors(name, document):
    validator = Draft202012Validator({"$ref": f"{SCHEMA_ID}#/$defs/{name}"}, registry=REGISTRY,
                                     format_checker=FormatChecker())
    return list(validator.iter_errors(document))


BFF_CLAIMS = {"iss": "https://iam.example.test", "sub": "synthetic-estate-bff", "aud": "baobab-trade", "exp": 1792670460,
              "iat": 1792670400, "jti": "synthetic-jti", "scope": "trade:buyer-handoff", "actor_type": "workload",
              "client_id": "synthetic-estate-bff"}
# Shape only: three base64url segments, deliberately not a decodable JWT.
HANDOFF = {"subject_token": ".".join(["synthetic-header", "synthetic-payload", "synthetic-signature"]),
           "subject_token_type": "urn:ietf:params:oauth:token-type:access_token",
           "correlation_id": "0b6f2c1e-6d0a-4f43-9c1a-2f1d6b1e9a40"}


class BuyerIdentityHandoffV11(unittest.TestCase):
    """v1.1: the BFF authenticates as itself; the human token is subject evidence."""

    def test_bff_caller_token_is_a_trade_audience_workload_token_for_buyer_handoff(self):
        self.assertEqual([], definition_errors("BffCallerTokenClaims", BFF_CLAIMS))
        for key, value in [("actor_type", "human"), ("aud", "baobab-control-plane"), ("scope", "trade:buy"),
                           ("client_id", None), ("jti", None)]:
            document = dict(BFF_CLAIMS)
            if value is None:
                document.pop(key)
            else:
                document[key] = value
            with self.subTest(key=key):
                self.assertNotEqual([], definition_errors("BffCallerTokenClaims", document))

    def test_handoff_body_carries_subject_evidence_and_requests_only(self):
        self.assertEqual([], definition_errors("BuyerOperationHandoffRequest", HANDOFF))
        self.assertEqual([], definition_errors("BuyerOperationHandoffRequest",
                                               dict(HANDOFF, requested_digital_estate_id="estate_synthetic",
                                                    requested_organisation_id="2c8e4f6a-1b3d-4e5f-8a7c-9d0e1f2a3b4c")))
        for key, value in [("principal_id", "p"), ("tenant_id", "tn_x"), ("digital_estate_id", "estate_x"),
                           ("subject_token_type", "urn:ietf:params:oauth:token-type:id_token"),
                           ("subject_token", "opaque")]:
            with self.subTest(key=key):
                self.assertNotEqual([], definition_errors("BuyerOperationHandoffRequest", dict(HANDOFF, **{key: value})))
        for key in ["subject_token", "subject_token_type", "correlation_id"]:
            document = dict(HANDOFF)
            document.pop(key)
            with self.subTest(missing=key):
                self.assertNotEqual([], definition_errors("BuyerOperationHandoffRequest", document))


if __name__ == "__main__":
    unittest.main()
