#!/usr/bin/env python3
"""Estate client binding (control-plane/v1, ADR-SHARED-042 CAA-04).

Static boundary only: the caller cannot name a tenant, binding or deployment,
an attestation is short-lived context, and the operation is a scoped,
unallocated Control Plane surface. Verifying the BFF evidence, matching the
deployment and refusing ambiguous bindings remain Control Plane runtime
obligations.
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
SCHEMA_ID = "https://contracts.baobab-platform.com/control-plane/v1/estate-client-binding.schema.json"
SCHEMA = json.loads((CONTRACTS / "control-plane/v1/estate-client-binding.schema.json").read_text())
API = yaml.safe_load((CONTRACTS / "control-plane/v1/estate-client-binding.openapi.yaml").read_text())
SCOPES = {s["name"]: s for s in yaml.safe_load((CONTRACTS / "authorization/v1/scope-registry.yaml").read_text())["scopes"]}
WORKLOADS = yaml.safe_load((CONTRACTS / "identity/v1/workload-registry.yaml").read_text())
ATTESTATION = json.loads((CONTRACTS / "control-plane/v1/examples/estate-client-binding-attestation.json").read_text())
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
    document = {"purpose": "BUYER_OPERATION", "client_evidence": TOKEN, "client_evidence_type": "urn:ietf:params:oauth:token-type:access_token",
                "subject_authorised_party": "synthetic-estate-bff", "engine_instance_id": "ei_synthetic01",
                "environment": "staging", "correlation_id": CORRELATION}
    document.update(change)
    return {k: v for k, v in document.items() if v is not None}


def binding(**change):
    document = {key: ATTESTATION[key] for key in ["binding_id", "issuer", "bff_client_id", "digital_estate_id",
                                                  "tenant_id", "engine_instance_id", "environment",
                                                  "deployment_reference", "revision", "evidence_reference"]}
    document.update(status="ACTIVE", effective_from="2026-10-01T00:00:00Z")
    document.update(change)
    return {k: v for k, v in document.items() if v is not None}


def parse(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


class EstateClientBinding(unittest.TestCase):
    def test_native_cp_topology_identifiers_are_carried_unchanged(self):
        engine = "019a0915-a8c0-7000-8000-000000000001"
        estate = "019a0915-a8c0-7000-8000-000000000002"
        self.assertEqual([], errors("EstateBindingResolveRequest", request(engine_instance_id=engine, requested_digital_estate_id=estate)))
        document = dict(ATTESTATION, engine_instance_id=engine, digital_estate_id=estate)
        self.assertEqual([], errors("EstateBindingAttestation", document))
        self.assertNotEqual([], errors("EstateBindingResolveRequest", request(engine_instance_id="not-a-canonical-engine")))

    def test_request_carries_evidence_and_no_authority(self):
        self.assertEqual([], errors("EstateBindingResolveRequest", request()))
        self.assertEqual([], errors("EstateBindingResolveRequest", request(requested_digital_estate_id="estate_synthetic")))
        for key, value in [("tenant_id", "tn_synthetic01"), ("binding_id", ATTESTATION["binding_id"]),
                           ("deployment_reference", "deployment.x"), ("revision", 3), ("digital_estate_id", "estate_x"),
                           ("host", "shop.example.test")]:
            with self.subTest(key=key):
                self.assertNotEqual([], errors("EstateBindingResolveRequest", request(**{key: value})))
        self.assertNotEqual([], errors("EstateBindingResolveRequest", request(purpose="ADMINISTRATION")))
        for key in ["purpose", "client_evidence", "client_evidence_type", "subject_authorised_party", "engine_instance_id",
                    "environment", "correlation_id"]:
            with self.subTest(missing=key):
                self.assertNotEqual([], errors("EstateBindingResolveRequest", request(**{key: None})))

    def test_client_evidence_is_an_access_token_shape(self):
        for change in [{"client_evidence": "not-a-jws"}, {"client_evidence_type": "urn:ietf:params:oauth:token-type:id_token"},
                       {"environment": "prod"}, {"engine_instance_id": "trade-1"}]:
            with self.subTest(change=change):
                self.assertNotEqual([], errors("EstateBindingResolveRequest", request(**change)))

    def test_attestation_is_valid_and_bounded(self):
        self.assertEqual([], errors("EstateBindingAttestation", ATTESTATION))
        attested, expires = parse(ATTESTATION["attested_at"]), parse(ATTESTATION["expires_at"])
        self.assertTrue(attested < expires <= attested + timedelta(seconds=60))
        for key in SCHEMA["$defs"]["EstateBindingAttestation"]["required"]:
            with self.subTest(missing=key):
                broken = copy.deepcopy(ATTESTATION)
                broken.pop(key)
                self.assertNotEqual([], errors("EstateBindingAttestation", broken))
        self.assertNotEqual([], errors("EstateBindingAttestation", dict(ATTESTATION, outcome="ACTIVE")))
        self.assertNotEqual([], errors("EstateBindingAttestation", dict(ATTESTATION, status="ACTIVE")))

    def test_binding_record_is_governed_and_versioned(self):
        self.assertEqual([], errors("EstateClientBinding", binding()))
        for change in [{"status": "PENDING"}, {"revision": 0}, {"environment": "qa"}, {"evidence_reference": None},
                       {"deployment_reference": None}, {"tenant_id": "tenant-1"}]:
            with self.subTest(change=change):
                self.assertNotEqual([], errors("EstateClientBinding", binding(**change)))

    def test_denials_are_closed(self):
        codes = SCHEMA["$defs"]["EstateBindingDenialCode"]["enum"]
        for code in ["BINDING_AMBIGUOUS", "BINDING_NOT_ACTIVE", "CLIENT_NOT_FOR_SUBJECT", "ENVIRONMENT_MISMATCH",
                     "ENGINE_INSTANCE_NOT_PERMITTED", "RESOLUTION_UNAVAILABLE"]:
            self.assertIn(code, codes)
        responses = API["paths"]["/internal/estate/v1/client-bindings/resolve"]["post"]["responses"]
        self.assertIn("BINDING_AMBIGUOUS", responses["409"]["description"])
        self.assertLessEqual({"200", "400", "401", "403", "404", "409", "503"}, set(responses))

    def test_operation_is_a_scoped_development_only_control_plane_surface(self):
        operation = API["paths"]["/internal/estate/v1/client-bindings/resolve"]["post"]
        self.assertEqual([{"EstateBindingWorkload": ["estate:client-binding:resolve"]}], operation["security"])
        scope = SCOPES["estate:client-binding:resolve"]
        self.assertEqual(["baobab-control-plane"], scope["audience"])
        self.assertEqual(["workload"], scope["allowed_actors"])
        self.assertFalse(scope["grants_authority"])
        handoff = SCOPES["trade:buyer-handoff"]
        self.assertEqual((["baobab-trade"], ["workload"], False),
                         (handoff["audience"], handoff["allowed_actors"], handoff["grants_authority"]))
        for client_id, entry in WORKLOADS["workloads"].items():
            with self.subTest(workload=client_id):
                if client_id == "baobab-dev-trade-buyer-validator":
                    self.assertEqual(entry["environment"], "development")
                    self.assertEqual(entry["subject_principal_audiences"], ["baobab-trade"])
                else:
                    self.assertNotIn("estate:client-binding:resolve", entry.get("allowed_scopes", []))
                if client_id == "baobab-dev-zuribeans-bff":
                    self.assertEqual(entry["environment"], "development")
                    self.assertEqual(entry["allowed_scopes"], ["trade:buyer-handoff"])
                else:
                    self.assertNotIn("trade:buyer-handoff", entry.get("allowed_scopes", []))


if __name__ == "__main__":
    unittest.main()
