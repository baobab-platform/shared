"""Fail-closed IAM-N07/DEV-08 TMS development-only workload tests."""
from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[2]


class TmsDevelopmentCeilingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workloads = yaml.safe_load(
            (ROOT / "contracts/identity/v1/workload-registry.yaml").read_text()
        )["workloads"]
        cls.scopes = yaml.safe_load(
            (ROOT / "contracts/authorization/v1/scope-registry.yaml").read_text()
        )["scopes"]

    def test_exact_provisioned_tms_clients(self):
        expected = {
            "baobab-dev-tms-subject": {
                "repository": "baobab-platform/baobab-tms",
                "owner": "baobab-platform/baobab-tms",
                "runtime": "DEV-08 source-candidate TMS workload operation subject",
                "environment": "development",
                "allowed_audiences": ["baobab-control-plane", "baobab-tms"],
                "allowed_scopes": ["context:resolve", "legal-actor:assess", "tms:booking:submit"],
                "credential_type": "client_credentials",
                "rotation_owner": "baobab-platform/baobab-tms",
                "status": "PROVISIONED",
            },
            "baobab-dev-tms-validator": {
                "repository": "baobab-platform/baobab-tms",
                "owner": "baobab-platform/baobab-tms",
                "runtime": "DEV-08 independent TMS subject context validator",
                "environment": "development",
                "allowed_audiences": ["baobab-control-plane"],
                "allowed_scopes": ["context:validate"],
                "validates_audiences": ["baobab-tms"],
                "credential_type": "client_credentials",
                "rotation_owner": "baobab-platform/baobab-tms",
                "status": "PROVISIONED",
            },
        }
        self.assertEqual({k: self.workloads[k] for k in expected}, expected)
        self.assertEqual(
            {n for n, r in self.workloads.items()
             if "tms:booking:submit" in r.get("allowed_scopes", [])},
            {"baobab-dev-tms-subject"},
        )
        for k in expected:
            for suffix in ("-staging", "-production"):
                self.assertNotIn(k + suffix, self.workloads)

    def test_scope_grants_no_native_booking_authority(self):
        rows = [r for r in self.scopes if r["name"] == "tms:booking:submit"]
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["audience"], ["baobab-tms"])
        self.assertEqual(rows[0]["allowed_actors"], ["workload"])
        self.assertIs(rows[0]["grants_authority"], False)
        self.assertEqual(self.workloads["baobab-dev-tms-validator"]["allowed_scopes"], ["context:validate"])
        for n in ("baobab-dev-tms-subject", "baobab-dev-tms-validator"):
            row = self.workloads[n]
            self.assertEqual(row["status"], "PROVISIONED")
            self.assertFalse({"token", "client_secret", "principal_id", "provider_permission"}.intersection(row))
        self.assertNotIn("trade:buy", self.workloads["baobab-dev-tms-subject"]["allowed_scopes"])


if __name__ == "__main__":
    unittest.main()
