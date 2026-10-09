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
                self.assertEqual(set(w["allowed_scopes"]),
                                 {"context:resolve", "legal-actor:assess"})
                self.assertEqual(w["context_purposes"], ["RUNTIME"])
                for field in ("tenant_id", "organisation_id", "legal_entity_id",
                              "merchant_id", "permissions", "granted_roles",
                              "private_key", "client_secret", "provider_entitlement"):
                    self.assertNotIn(field, w)

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
