"""IAM-N04 runtime binding read is a narrow *development-only* ceiling.

It does not allocate the distinct CP AdministrativeGrant, issue a credential,
register a provider, or assert any actual CP/issuer acceptance.
"""
from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[2]


class N04RuntimeReaderCeiling(unittest.TestCase):
    def test_exact_development_only_runtime_reader_and_scope(self):
        registry = yaml.safe_load(
            (ROOT / "contracts/identity/v1/workload-registry.yaml").read_text())
        workloads = registry["workloads"]
        client = "baobab-dev-iam-runtime-reader"
        row = workloads[client]
        self.assertEqual(row, {
            "repository": "baobab-platform/baobab-iam",
            "owner": "baobab-platform/baobab-iam",
            "runtime": "IAM-N04 disposable developer CP runtime binding source reader",
            "environment": "development",
            "allowed_audiences": ["baobab-control-plane"],
            "allowed_scopes": ["identity-runtime:read"],
            "credential_type": "client_credentials",
            "rotation_owner": "baobab-platform/baobab-iam",
            "status": "ACTIVE",
        })
        owners = {
            name for name, entry in workloads.items()
            if "identity-runtime:read" in entry.get("allowed_scopes", [])
        }
        self.assertEqual(owners, {client})
        self.assertNotIn("validates_audiences", row)
        for prohibited in (
            "context:resolve", "context:validate", "federation-authority:read",
            "identity-runtime:observe", "provider-migration:task", "admin",
        ):
            self.assertNotIn(prohibited, row["allowed_scopes"])
        scopes = yaml.safe_load(
            (ROOT / "contracts/authorization/v1/scope-registry.yaml").read_text())
        matches = [scope for scope in scopes["scopes"]
                   if scope["name"] == "identity-runtime:read"]
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]["audience"], ["baobab-control-plane"])
        self.assertFalse(matches[0].get("grants_authority", True))
        self.assertEqual(matches[0]["allowed_actors"], ["workload"])


if __name__ == "__main__":
    unittest.main()
