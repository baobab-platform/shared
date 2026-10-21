#!/usr/bin/env python3
"""Delegated human Principal resolution (identity/v1, ZB-G03 step 3).

These tests pin the static boundary only: the caller presents subject
evidence and can assert no identity, and a resolution carries no authority.
Token verification, introspection, issuer trust and buyer eligibility remain
Control Plane runtime obligations.
"""
import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource
import yaml

ROOT = Path(__file__).resolve().parents[2]
CONTRACTS = ROOT / "contracts"
SCHEMA_ID = "https://contracts.baobab-platform.com/identity/v1/principal-resolution.schema.json"
SCHEMA = json.loads((CONTRACTS / "identity/v1/principal-resolution.schema.json").read_text())
API = yaml.safe_load((CONTRACTS / "identity/v1/principal-resolution.openapi.yaml").read_text())
# Shape only: three base64url segments, deliberately not a decodable JWT.
TOKEN = ".".join(["synthetic-header", "synthetic-payload", "synthetic-signature"])
CORRELATION = "0b6f2c1e-6d0a-4f43-9c1a-2f1d6b1e9a40"


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


def request(**change):
    document = {"subject_token": TOKEN, "subject_token_type": "urn:ietf:params:oauth:token-type:access_token",
                "correlation_id": CORRELATION}
    document.update(change)
    return {k: v for k, v in document.items() if v is not None}


def resolution(**change):
    document = {"outcome": "RESOLVED", "principal_id": "019a0915-a8c0-7000-8000-000000000001", "actor_type": "human",
                "status": "ACTIVE", "external_identity_id": "019a0915-a8c0-7000-8000-000000000002",
                "evidence_expires_at": "2026-10-21T21:00:00Z"}
    document.update(change)
    return document


class PrincipalResolution(unittest.TestCase):
    def test_requests_carry_only_subject_evidence(self):
        for definition, extra in (("PrincipalResolveRequest", {}), ("BuyerPrincipalRegistrationRequest", {"purpose": "BUYER_ONBOARDING"})):
            with self.subTest(definition=definition):
                self.assertEqual([], errors(definition, request(**extra)))
                # The caller can assert no identity of its own.
                for key, value in [("issuer", "https://iam.example.test/"), ("subject", "s"),
                                   ("principal_id", "p"), ("email", "buyer@example.test"),
                                   ("customer_id", "cus_1"), ("organisation_id", "o"), ("tenant_id", "t")]:
                    self.assertNotEqual([], errors(definition, request(**extra, **{key: value})), key)

    def test_registration_declares_its_approved_purpose(self):
        self.assertNotEqual([], errors("BuyerPrincipalRegistrationRequest", request()))
        for purpose in ["SUPPLIER_ONBOARDING", "buyer_onboarding", "ADMIN"]:
            with self.subTest(purpose=purpose):
                self.assertNotEqual([], errors("BuyerPrincipalRegistrationRequest", request(purpose=purpose)))
        # Resolution is read-only and declares no purpose.
        self.assertNotEqual([], errors("PrincipalResolveRequest", request(purpose="BUYER_ONBOARDING")))

    def test_only_a_compact_access_token_is_evidence(self):
        for change in [{"subject_token_type": "urn:ietf:params:oauth:token-type:id_token"},
                       {"subject_token_type": None}, {"subject_token": None},
                       {"subject_token": "not-a-jwt"}, {"subject_token": TOKEN + ".extra"},
                       {"subject_token": "a" * 8200 + ".b.c"},
                       {"correlation_id": "trade-ctx/1"}, {"correlation_id": None}]:
            with self.subTest(change=change):
                self.assertNotEqual([], errors("PrincipalResolveRequest", request(**change)))

    def test_resolution_is_an_active_human_and_carries_no_authority(self):
        self.assertEqual([], errors("PrincipalResolution", resolution()))
        self.assertEqual([], errors("PrincipalResolution", resolution(outcome="REGISTERED")))
        for change in [{"actor_type": "workload"}, {"status": "SUSPENDED"}, {"outcome": "PROVISIONED"},
                       {"tenant_id": "t"}, {"organisation_id": "o"}, {"roles": ["BUYER"]},
                       {"membership_id": "m"}, {"issuer": "https://iam.example.test/"}, {"subject": "s"}]:
            with self.subTest(change=change):
                self.assertNotEqual([], errors("PrincipalResolution", resolution(**change)))

    def test_operations_are_private_workload_only_and_separately_scoped(self):
        paths = API["paths"]
        self.assertEqual(set(paths), {"/internal/identity/v1/principals/resolve",
                                      "/internal/identity/v1/principals/register-buyer"})
        expected = {"/internal/identity/v1/principals/resolve": "identity:principal:resolve",
                    "/internal/identity/v1/principals/register-buyer": "identity:principal:register-buyer"}
        for path, scope in expected.items():
            with self.subTest(path=path):
                operation = paths[path]["post"]
                self.assertEqual(operation["security"], [{"PrincipalResolutionWorkload": [scope]}])
                self.assertEqual(API["components"]["securitySchemes"]["PrincipalResolutionWorkload"]["flows"].keys(),
                                 {"clientCredentials"})
        self.assertNotIn("201", paths["/internal/identity/v1/principals/resolve"]["post"]["responses"])
        self.assertIn("404", paths["/internal/identity/v1/principals/resolve"]["post"]["responses"])
        register = paths["/internal/identity/v1/principals/register-buyer"]["post"]["responses"]
        self.assertTrue({"200", "201", "409", "429", "503"} <= set(register))
        # Operations, not catalogued capabilities (ADR-SHARED-042: no unregistered capability key).
        self.assertNotIn("identity.principal.", (CONTRACTS / "identity/v1/principal-resolution.openapi.yaml").read_text())

    def test_subject_audience_is_a_registered_validator_relationship(self):
        workloads = yaml.safe_load((CONTRACTS / "identity/v1/workload-registry.yaml").read_text())["workloads"]
        scopes = {"identity:principal:resolve", "identity:principal:register-buyer"}
        for name, entry in workloads.items():
            with self.subTest(workload=name):
                holds = bool(scopes & set(entry["allowed_scopes"]))
                self.assertEqual(holds, "subject_principal_audiences" in entry)

    def test_scopes_are_workload_only_grant_nothing_and_are_allocated_to_no_workload(self):
        scopes = {s["name"]: s for s in yaml.safe_load(
            (CONTRACTS / "authorization/v1/scope-registry.yaml").read_text())["scopes"]}
        workloads = yaml.safe_load((CONTRACTS / "identity/v1/workload-registry.yaml").read_text())["workloads"]
        for name in ("identity:principal:resolve", "identity:principal:register-buyer"):
            with self.subTest(scope=name):
                self.assertEqual(scopes[name]["audience"], ["baobab-control-plane"])
                self.assertEqual(scopes[name]["allowed_actors"], ["workload"])
                self.assertIs(scopes[name]["grants_authority"], False)
                for workload, entry in workloads.items():
                    self.assertNotIn(name, entry["allowed_scopes"], workload)

    def test_denial_codes_are_closed(self):
        self.assertEqual(set(SCHEMA["$defs"]["PrincipalResolutionDenialCode"]["enum"]), {
            "CALLER_NOT_PERMITTED", "SUBJECT_TOKEN_INVALID", "SUBJECT_TOKEN_NOT_CURRENT",
            "SUBJECT_TOKEN_NOT_FOR_CALLER", "IDENTITY_NOT_RESOLVED", "PRINCIPAL_NOT_ACTIVE",
            "REGISTRATION_NOT_ELIGIBLE", "IDENTITY_LINK_CONFLICT", "REGISTRATION_RATE_LIMITED", "RESOLUTION_UNAVAILABLE"})


if __name__ == "__main__":
    unittest.main()
