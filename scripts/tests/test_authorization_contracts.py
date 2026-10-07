"""Exercise workload audience registration through the real Ruby validator."""
import copy
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[2]


class ValidatorAudienceRegistrationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        shutil.copytree(ROOT / "contracts", self.root / "contracts")
        (self.root / "scripts").mkdir()
        shutil.copy2(ROOT / "scripts/validate-authorization-contracts.rb", self.root / "scripts")
        self.path = self.root / "contracts/identity/v1/workload-registry.yaml"
        self.registry = yaml.safe_load(self.path.read_text())
        base = copy.deepcopy(self.registry["workloads"]["baobab-erp-workload"])
        base["allowed_audiences"] = ["baobab-control-plane"]
        base["allowed_scopes"] = ["context:validate"]
        base["validates_audiences"] = ["baobab-erp"]
        self.registry["workloads"]["erp-api-validator"] = copy.deepcopy(base)
        self.registry["workloads"]["erp-worker-validator"] = copy.deepcopy(base)

    def validate(self):
        self.path.write_text(yaml.safe_dump(self.registry))
        return subprocess.run(
            ["ruby", str(self.root / "scripts/validate-authorization-contracts.rb")],
            capture_output=True, text=True, check=False,
        )

    def test_pulse_is_registered_only_for_its_resource_server_audience(self):
        pulse = self.registry["workloads"]["baobab-pulse-workload"]
        self.assertEqual(pulse["status"], "ACTIVE")
        self.assertIn("context:validate", pulse["allowed_scopes"])
        self.assertEqual(pulse["validates_audiences"], ["baobab-pulse"])
        self.assertNotIn("baobab-pulse", pulse["allowed_audiences"])

        scopes = yaml.safe_load(
            (self.root / "contracts/authorization/v1/scope-registry.yaml").read_text()
        )["scopes"]
        by_name = {scope["name"]: scope for scope in scopes}
        for name in (
            "intelligence:evidence:search",
            "intelligence:research-mission:manage",
            "intelligence:restricted",
        ):
            self.assertEqual(by_name[name]["audience"], ["baobab-pulse"])
            self.assertIn("workload", by_name[name]["allowed_actors"])

    def test_two_validators_for_one_audience(self):
        result = self.validate()
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_relationship_remains_explicit_and_least_privilege(self):
        cases = {
            "missing": None,
            "empty": [],
            "duplicate": ["baobab-erp", "baobab-erp"],
            "control-plane": ["baobab-control-plane"],
            "unregistered": ["unregistered-api"],
            "blank": [" "],
        }
        for name, audiences in cases.items():
            with self.subTest(name=name):
                entry = self.registry["workloads"]["erp-api-validator"]
                if audiences is None:
                    entry.pop("validates_audiences", None)
                else:
                    entry["validates_audiences"] = audiences
                result = self.validate()
                self.assertNotEqual(result.returncode, 0, result.stdout)

    def test_audience_registration_requires_scope(self):
        entry = self.registry["workloads"]["erp-api-validator"]
        entry["allowed_scopes"] = ["context:resolve"]
        result = self.validate()
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("does not allow context:validate", result.stderr)


if __name__ == "__main__":
    unittest.main()

