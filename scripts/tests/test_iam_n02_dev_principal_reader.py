"""N02 proposed development CP Principal reader: no credential or entitlement."""
from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[2]


class N02ZuriBeansCPReaderCeiling(unittest.TestCase):
    def test_separate_development_cp_caller_is_unactivated(self):
        rows = yaml.safe_load(
            (ROOT / "contracts/identity/v1/workload-registry.yaml").read_text()
        )["workloads"]
        name = "baobab-dev-zuribeans-cp-principal-validator"
        self.assertEqual(rows[name], {
            "repository": "baobab-platform/zuribeans",
            "owner": "baobab-platform/zuribeans",
            "runtime": "IAM-N02 disposable ZuriBeans BFF CP Principal validator",
            "environment": "development",
            "allowed_audiences": ["baobab-control-plane"],
            "allowed_scopes": ["identity:principal:resolve"],
            "subject_principal_audiences": ["baobab-trade"],
            "credential_type": "client_credentials",
            "rotation_owner": "baobab-platform/zuribeans",
            "status": "PROVISIONED",
        })
        bff = rows["baobab-dev-zuribeans-bff"]
        self.assertEqual(bff["allowed_audiences"], ["baobab-trade"])
        self.assertEqual(bff["allowed_scopes"], ["trade:buyer-handoff"])
        self.assertEqual(bff["human_token_profile"], {
            "purpose": "ESTATE_BFF_BUYER",
            "audiences": ["baobab-trade"],
            "scopes": ["trade:buy"],
        })
        self.assertNotIn("identity:principal:resolve", bff["allowed_scopes"])
        self.assertNotIn("trade:buy", rows[name]["allowed_scopes"])
        self.assertNotIn("trade:buyer-handoff", rows[name]["allowed_scopes"])
        self.assertNotIn("context:validate", rows[name]["allowed_scopes"])
        self.assertNotIn("identity:principal:register-buyer",
                         rows[name]["allowed_scopes"])
        for key, row in rows.items():
            if key == name:
                continue
            self.assertNotEqual(key, name + "-staging")
            self.assertNotEqual(key, name + "-production")
        scopes = yaml.safe_load(
            (ROOT / "contracts/authorization/v1/scope-registry.yaml").read_text()
        )["scopes"]
        principal = [x for x in scopes if x["name"] == "identity:principal:resolve"]
        self.assertEqual(len(principal), 1)
        self.assertEqual(principal[0]["audience"], ["baobab-control-plane"])
        self.assertEqual(principal[0]["allowed_actors"], ["workload"])
        self.assertFalse(principal[0]["grants_authority"])


if __name__ == "__main__":
    unittest.main()
