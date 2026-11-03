"""ADR-SHARED-043: N02, N04 and N07 are separate, inert clients."""
from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[2]

class ReconciledCeilings(unittest.TestCase):
    def test_closed_workload_scopes(self):
        rows = yaml.safe_load((ROOT / "contracts/identity/v1/workload-registry.yaml").read_text())["workloads"]
        exact = {
            "baobab-dev-iam-runtime-reader": ["identity-runtime:read"],
            "baobab-dev-zuribeans-cp-principal-validator": ["identity:principal:resolve"],
            "baobab-dev-tms-subject": ["context:resolve", "legal-actor:assess", "tms:booking:submit"],
            "baobab-dev-tms-validator": ["context:validate"],
        }
        for name, scopes in exact.items():
            self.assertEqual(rows[name]["allowed_scopes"], scopes)
            self.assertEqual(rows[name]["status"], "PROVISIONED")
            self.assertEqual(rows[name]["environment"], "development")
            self.assertNotIn("client_secret", rows[name])
            self.assertNotIn(name + "-staging", rows)
            self.assertNotIn(name + "-production", rows)
        self.assertEqual(rows["baobab-dev-tms-validator"]["validates_audiences"], ["baobab-tms"])
        self.assertEqual(rows["baobab-dev-zuribeans-cp-principal-validator"]["subject_principal_audiences"], ["baobab-trade"])
        self.assertEqual(
            {n for n, r in rows.items() if "identity-runtime:read" in r.get("allowed_scopes", [])},
            {"baobab-dev-iam-runtime-reader"},
        )
        self.assertEqual(
            {n for n, r in rows.items() if "tms:booking:submit" in r.get("allowed_scopes", [])},
            {"baobab-dev-tms-subject"},
        )

    def test_browser_is_separate_and_non_authorizing(self):
        rows = yaml.safe_load((ROOT / "contracts/identity/v1/workload-registry.yaml").read_text())["workloads"]
        clients = yaml.safe_load((ROOT / "contracts/identity/v1/native-browser-client-registry.yaml").read_text())["clients"]
        name = "baobab-dev-zuribeans-native-browser-bff"
        self.assertEqual(set(clients), {name})
        self.assertNotIn(name, rows)
        self.assertEqual(clients[name]["status"], "PROVISIONED")
        self.assertEqual(clients[name]["grant_types"], ["authorization_code"])
        self.assertEqual(clients[name]["pkce_method"], "S256")
        self.assertIs(clients[name]["grants_business_authority"], False)
        self.assertIs(clients[name]["creates_principal"], False)
        self.assertEqual(rows["baobab-dev-zuribeans-bff"]["allowed_scopes"], ["trade:buyer-handoff"])

if __name__ == "__main__":
    unittest.main()
