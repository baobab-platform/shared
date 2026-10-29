"""LA-05G: staging-only legal responsibility assessor identities are inert."""
from pathlib import Path
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[2]
NAMES = {
    "baobab-trade-legal-actor-assessor-staging": "baobab-trade",
    "baobab-erp-legal-actor-assessor-staging": "baobab-erp",
    "baobab-payments-legal-actor-assessor-staging": "baobab-payments",
    "baobab-trade-docs-legal-actor-assessor-staging": "baobab-trade-docs",
}
# Accepted owner-specific resolution transports added after LA-05G. They
# remain non-authorising, workload-only and PROVISIONED; never live grants.
OWNER_RESOLUTION_SCOPES = {
    "baobab-trade-legal-actor-assessor-staging": {
        "trade-seller-binding:attest", "trade-seller-binding:resolve", "trade-order-authority:resolve",
    },
    "baobab-erp-legal-actor-assessor-staging": {"erp-posting-authority:resolve"},
    "baobab-payments-legal-actor-assessor-staging": {"payments-money-movement-authority:resolve"},
    "baobab-trade-docs-legal-actor-assessor-staging": set(),
}


class LegalActorAssessorWorkloadBoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workloads = yaml.safe_load(
            (ROOT / "contracts/identity/v1/workload-registry.yaml").read_text()
        )["workloads"]
        cls.scopes = {
            v["name"]: v
            for v in yaml.safe_load(
                (ROOT / "contracts/authorization/v1/scope-registry.yaml").read_text()
            )["scopes"]
        }

    def test_registered_transport_scope_is_workload_only_and_not_authority(self):
        scope = self.scopes["legal-actor:assess"]
        self.assertEqual(scope["audience"], ["baobab-control-plane"])
        self.assertEqual(scope["allowed_actors"], ["workload"])
        self.assertFalse(scope["grants_authority"])

    def test_documentary_scope_is_negative_only_and_private(self):
        scope = self.scopes["documentary:restriction-assess"]
        self.assertEqual(scope["audience"], ["baobab-control-plane"])
        self.assertEqual(scope["allowed_actors"], ["workload"])
        self.assertFalse(scope["grants_authority"])
        authorised = {
            "baobab-erp-legal-actor-assessor-staging",
            "baobab-payments-legal-actor-assessor-staging",
        }
        for name, workload in self.workloads.items():
            if name not in authorised:
                self.assertNotIn("documentary:restriction-assess",
                                 workload.get("allowed_scopes", []))

    def test_no_staging_assessor_has_live_credentials_or_permissions(self):
        self.assertEqual(len(NAMES), 4)
        for name, owner in NAMES.items():
            with self.subTest(workload=name):
                w = self.workloads[name]
                self.assertEqual(w["status"], "PROVISIONED")
                self.assertEqual(w["environment"], "staging")
                self.assertEqual(w["owner"], "baobab-platform/" + owner)
                self.assertEqual(w["repository"], "baobab-platform/" + owner)
                self.assertEqual(w["rotation_owner"], "baobab-platform/" + owner)
                self.assertEqual(w["credential_type"], "federated_workload_token")
                self.assertEqual(w["allowed_audiences"], ["baobab-control-plane"])
                expected = {"context:resolve", "legal-actor:assess"}
                expected.update(OWNER_RESOLUTION_SCOPES[name])
                if name in {
                    "baobab-erp-legal-actor-assessor-staging",
                    "baobab-payments-legal-actor-assessor-staging",
                }:
                    expected.add("documentary:restriction-assess")
                self.assertEqual(set(w["allowed_scopes"]), expected)
                self.assertEqual(w["context_purposes"], ["RUNTIME"])
                for field in ("tenant_id", "organisation_id", "legal_entity_id",
                              "merchant_id", "permissions", "granted_roles",
                              "private_key", "client_secret", "provider_entitlement"):
                    self.assertNotIn(field, w)

    def test_owner_resolution_transports_remain_non_authorising_and_owner_private(self):
        for owner, allowed in OWNER_RESOLUTION_SCOPES.items():
            for name in allowed:
                with self.subTest(scope=name):
                    scope = self.scopes[name]
                    self.assertEqual(["baobab-control-plane"], scope["audience"])
                    self.assertEqual(["workload"], scope["allowed_actors"])
                    self.assertIs(False, scope["grants_authority"])
                    holders = {key for key, w in self.workloads.items()
                               if name in w.get("allowed_scopes", [])}
                    self.assertEqual({owner}, holders)

    def test_existing_production_workloads_not_silently_granted_assessor(self):
        for name, w in self.workloads.items():
            if name in NAMES:
                continue
            with self.subTest(workload=name):
                self.assertNotIn("legal-actor:assess", w.get("allowed_scopes", []),
                                 "LA-05G must not enable other production or staging clients")

    def test_provisioned_scope_does_not_activate_workload(self):
        for name in NAMES:
            self.assertNotEqual(self.workloads[name]["status"], "ACTIVE")


if __name__ == "__main__":
    unittest.main()
