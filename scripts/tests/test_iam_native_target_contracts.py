"""Negative-first IAM contract separation; only static Shared proposal checks."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import unittest
import yaml
from jsonschema import Draft202012Validator, FormatChecker

BASE = Path(__file__).resolve().parents[2] / "contracts"
IAM = BASE / "identity" / "v1"


class NativeTargetContracts(unittest.TestCase):
    def setUp(self):
        self.anchors = yaml.safe_load((IAM / "native-provider-targets.yaml").read_text())
        self.assurance = json.loads((IAM / "assurance-evaluation.schema.json").read_text())
        self.enterprise = json.loads((IAM / "enterprise-federation-start.schema.json").read_text())

    def validate(self, schema, section, instance):
        root = {"$schema": schema["$schema"], "$defs": schema["$defs"],
                "$ref": "#/$defs/" + section}
        return list(Draft202012Validator(root, format_checker=FormatChecker()).iter_errors(instance))

    def test_catalogue_and_target_allocation_are_distinct(self):
        catalogue = yaml.safe_load((BASE / "capability" / "v1" / "catalogue.yaml").read_text())
        keys = {item["capability_key"] for item in catalogue["capabilities"]}
        self.assertTrue({"identity.authentication.perform", "identity.workload-token.issue",
                         "identity.authentication.assurance", "identity.federation.enterprise"} <= keys)
        targets = self.anchors
        self.assertEqual(targets["status"], "TARGET_NOT_QUALIFIED")
        self.assertEqual(targets["token_issuance"], "SUBSUMED_IN_EXISTING_AUTHENTICATION_AND_WORKLOAD_CAPABILITIES")
        self.assertNotIn("identity.token.issuance", keys)
        self.assertEqual(len(targets["management_operations"]), len(set(targets["management_operations"])))
        self.assertFalse(set(targets["management_operations"]) & keys)
        facets = {p["provider_key"]: set(p["target_facets"]) for p in targets["providers"]}
        self.assertEqual(set(facets), {"baobab-iam.kratos", "baobab-iam.hydra", "baobab-iam.keycloak"})
        self.assertFalse({"HUMAN_AUTHENTICATION", "WORKLOAD_TOKEN_ISSUANCE"} & facets["baobab-iam.keycloak"])
        self.assertNotIn("ENTERPRISE_SSO", facets["baobab-iam.kratos"])
        self.assertNotIn("WORKLOAD_TOKEN_ISSUANCE", facets["baobab-iam.kratos"])

    def test_native_target_and_management_contract_schemas(self):
        from referencing import Registry, Resource
        target_schema = json.loads((IAM / "native-provider-targets.schema.json").read_text())
        management = json.loads((IAM / "iam-management-operation.schema.json").read_text())
        runtime = json.loads((IAM / "runtime-capability.schema.json").read_text())
        reg = Registry().with_resources([
            (management["$id"], Resource.from_contents(management)),
            (runtime["$id"], Resource.from_contents(runtime)),
        ])
        validator = Draft202012Validator(target_schema, registry=reg)
        self.assertEqual(list(validator.iter_errors(self.anchors)), [])
        for key, value in (("status", "DEVELOPMENT_QUALIFIED"), ("cp_binding", "ACTIVE"),
                           ("production_permitted", True), ("security_secret", "bad")):
            invalid = copy.deepcopy(self.anchors)
            invalid[key] = value
            self.assertTrue(list(validator.iter_errors(invalid)))
        request = {"schema": "baobab.identity.management-request.v1",
                   "operation": "identity.security.revoke",
                   "target_reference": "ref_targetsubject",
                   "change_request_reference": "ref_reviewrequested",
                   "expected_revision": 1,
                   "idempotency_key": "10000000-0000-4000-8000-000000000003"}
        self.assertFalse(self.validate(management, "IAMManagementRequest", request))
        for key in ("tenant_id", "approval_limit", "review_approved", "client_secret",
                    "provider_native_admin_token"):
            self.assertTrue(self.validate(management, "IAMManagementRequest",
                                          dict(request, **{key: "forbidden"})))
        verified = {"schema": "baobab.identity.management-outcome.v1",
                    "operation": "identity.security.revoke",
                    "status": "PROVIDER_VERIFIED",
                    "event_reference": "ref_eventcredential",
                    "provider_evidence_reference": "ref_originalevidence",
                    "observed_at": "2026-11-06T07:00:00Z"}
        self.assertFalse(self.validate(management, "IAMManagementOutcome", verified))
        for bad in ({k: v for k, v in verified.items()
                     if k != "provider_evidence_reference"},
                    dict(verified, active_binding=True),
                    dict(verified, status="PENDING")):
            self.assertTrue(self.validate(management, "IAMManagementOutcome", bad))

    def test_dev_qualification_is_not_cp_registration_or_a_self_attested_pass(self):
        from referencing import Registry, Resource
        proof_schema = json.loads((IAM / "native-development-qualification.schema.json").read_text())
        runtime = json.loads((IAM / "runtime-capability.schema.json").read_text())
        reference = Registry().with_resource(runtime["$id"], Resource.from_contents(runtime))
        validator = Draft202012Validator(proof_schema, registry=reference)
        example = json.loads((IAM / "examples/native-development-unqualified.json").read_text())
        self.assertFalse(list(validator.iter_errors(example)))
        qualified_without_witness = dict(example, qualification_state="DEVELOPMENT_QUALIFIED")
        self.assertTrue(list(validator.iter_errors(qualified_without_witness)))
        fake_witness = {
            "original_archive_digest": "sha256:" + "a" * 64,
            "github_run_id": 42170000000,
            "original_cases_digest": "sha256:" + "b" * 64,
            "independent_reviewer_reference": "ref_independentreview",
            "all_required_positive_observed": True,
            "all_required_negatives_observed": True,
            "teardown_verified": True,
            "runtime_origins_independently_attested": True,
        }
        candidate = dict(example, qualification_state="DEVELOPMENT_QUALIFIED",
                         independent_development_evidence=fake_witness)
        # Schema shape is not producer authenticity. This fixture MUST NOT be
        # published as qualified or used to activate a provider.
        self.assertFalse(list(validator.iter_errors(candidate)))
        for field, value in (("all_required_negatives_observed", False),
                             ("teardown_verified", False),
                             ("runtime_origins_independently_attested", False),
                             ("independent_reviewer_reference", "")):
            bad = copy.deepcopy(candidate)
            bad["independent_development_evidence"][field] = value
            self.assertTrue(list(validator.iter_errors(bad)))
        for key in ("provider_id", "engine_instance_id", "tenant_id",
                    "active_binding", "production_authorized", "consumer_grant"):
            self.assertTrue(list(validator.iter_errors(dict(example, **{key: True}))))
        with_original_evidence = dict(example, independent_development_evidence=fake_witness)
        self.assertTrue(list(validator.iter_errors(with_original_evidence)))

    def test_server_owned_assurance_and_denials(self):
        valid = {"schema": "baobab.identity.assurance-evaluation-request.v1",
                 "authentication_event_reference": "ref_authenticatedevent",
                 "session_reference": "ref_sessionproof", "operation_class": "BUYER_COMMIT"}
        self.assertFalse(self.validate(self.assurance, "AssuranceEvaluationRequest", valid))
        for key, value in (("minimum_assurance", "A1"), ("tenant_id", "tn_123"),
                           ("approval_limit", 100000), ("user_asserted_risk", "low"),
                           ("provider", "keycloak")):
            extra = dict(valid, **{key: value})
            self.assertTrue(self.validate(self.assurance, "AssuranceEvaluationRequest", extra))
        allowed = {"schema": "baobab.identity.assurance-evaluation-result.v1",
                   "outcome": "ASSURANCE_MET_NOT_AUTHORIZATION",
                   "required_level": "A2", "observed_level": "A2",
                   "authenticated_at": "2026-11-06T07:00:00Z",
                   "fresh_until": "2026-11-06T07:05:00Z",
                   "evidence_reference": "ref_approvedproof",
                   "evaluated_at": "2026-11-06T07:00:00Z",
                   "reason": "ASSURANCE_MET_NOT_AUTHORIZATION"}
        self.assertFalse(self.validate(self.assurance, "AssuranceEvaluationResult", allowed))
        for bad in (dict(allowed, outcome="GRANTED"),
                    dict(allowed, business_role="owner"),
                    {k: v for k, v in allowed.items() if k != "evidence_reference"}):
            self.assertTrue(self.validate(self.assurance, "AssuranceEvaluationResult", bad))

    def test_federation_does_not_select_issuer_or_grant_membership(self):
        valid = {"schema": "baobab.identity.enterprise-federation-start.v1",
                 "trust_reference": "ref_enterprisetrust",
                 "browser_session_reference": "ref_browserproof"}
        self.assertFalse(self.validate(self.enterprise, "EnterpriseFederationStartRequest", valid))
        for key in ("realm", "organisation_role", "domain_hint", "redirect_uri", "provider"):
            self.assertTrue(self.validate(self.enterprise, "EnterpriseFederationStartRequest",
                                          dict(valid, **{key: "forbidden"})))
        response = {"schema": "baobab.identity.enterprise-federation-challenge.v1",
                    "event_reference": "ref_federatedevent",
                    "authorization_url": "https://enterprise.example.test/authorize",
                    "expires_at": "2026-11-06T07:05:00Z"}
        self.assertFalse(self.validate(self.enterprise, "EnterpriseFederationChallenge", response))
        for bad in (dict(response, authorization_url="http://insecure.invalid"),
                    dict(response, principal_id="unverified"),
                    dict(response, role="administrator")):
            self.assertTrue(self.validate(self.enterprise, "EnterpriseFederationChallenge", bad))


if __name__ == "__main__":
    unittest.main()
