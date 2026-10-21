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

    def test_cms_is_registered_only_as_validator_of_its_resource_server_audience(self):
        cms = self.registry["workloads"]["baobab-cms-workload"]
        self.assertIn("context:validate", cms["allowed_scopes"])
        self.assertEqual(cms["validates_audiences"], ["baobab-cms"])
        self.assertNotIn("baobab-cms", cms["allowed_audiences"])

        scopes = yaml.safe_load(
            (self.root / "contracts/authorization/v1/scope-registry.yaml").read_text()
        )["scopes"]
        by_name = {scope["name"]: scope for scope in scopes}
        for name in ("content:entry:resolve", "content:entry:preview"):
            self.assertEqual(by_name[name]["audience"], ["baobab-cms"])
            self.assertIn("workload", by_name[name]["allowed_actors"])

    def test_nabhold_is_a_least_privilege_caller_not_a_validator(self):
        nabhold = self.registry["workloads"]["nabhold-backend"]
        self.assertEqual(nabhold["status"], "PROVISIONED")
        self.assertEqual(nabhold["repository"], "baobab-platform/nabhold")
        self.assertEqual(nabhold["credential_type"], "client_credentials")
        self.assertEqual(
            sorted(nabhold["allowed_audiences"]), ["baobab-cms", "baobab-control-plane"]
        )
        self.assertEqual(
            sorted(nabhold["allowed_scopes"]), ["content:entry:resolve", "context:resolve"]
        )
        self.assertNotIn("validates_audiences", nabhold)
        for withheld in ("context:validate", "content:entry:preview", "provider-migration:task"):
            self.assertNotIn(withheld, nabhold["allowed_scopes"])

    def test_int02_exception_rejects_changed_boundary(self):
        original = copy.deepcopy(self.registry["workloads"]["baobab-int02-pulse-consumer"])
        self.assertEqual(self.validate().returncode, 0)
        changes = {
            "owner": "baobab-platform/baobab-pulse",
            "repository": "baobab-platform/baobab-pulse",
            "runtime": "persistent runtime",
            "environment": "production",
            "allowed_audiences": ["baobab-control-plane"],
            "allowed_scopes": ["context:resolve"],
            "credential_type": "federated_workload_token",
            "rotation_owner": "baobab-platform/baobab-iam",
            "status": "PROVISIONED",
            "unreviewed_authority": True,
        }
        for field, value in changes.items():
            with self.subTest(field=field):
                changed = copy.deepcopy(original)
                changed[field] = value
                self.registry["workloads"]["baobab-int02-pulse-consumer"] = changed
                self.assertNotEqual(self.validate().returncode, 0)
        self.registry["workloads"].pop("baobab-int02-pulse-consumer")
        self.assertNotEqual(self.validate().returncode, 0)

    def test_int03_caller_and_validator_have_independent_least_privilege(self):
        caller = self.registry["workloads"]["baobab-int03-cms-consumer"]
        validator = self.registry["workloads"]["baobab-int03-cms-validator"]
        self.assertEqual(caller["status"], "ACTIVE")
        self.assertEqual(validator["status"], "ACTIVE")
        self.assertEqual(caller["environment"], "development")
        self.assertEqual(validator["environment"], "development")
        self.assertEqual(caller["allowed_audiences"], ["baobab-control-plane", "baobab-cms"])
        self.assertEqual(caller["allowed_scopes"], ["context:resolve", "content:entry:resolve"])
        self.assertNotIn("validates_audiences", caller)
        self.assertEqual(validator["allowed_audiences"], ["baobab-control-plane"])
        self.assertEqual(validator["allowed_scopes"], ["context:validate"])
        self.assertEqual(validator["validates_audiences"], ["baobab-cms"])
        self.assertNotEqual(caller["owner"], validator["owner"])
        self.assertEqual(self.registry["workloads"]["nabhold-backend"]["status"], "PROVISIONED")
        self.assertEqual(self.registry["workloads"]["baobab-cms-workload"]["environment"], "production")
        self.assertEqual(self.validate().returncode, 0)

    def test_int03_complete_rows_reject_boundary_changes_or_removal(self):
        for client_id in ("baobab-int03-cms-consumer", "baobab-int03-cms-validator"):
            original = copy.deepcopy(self.registry["workloads"][client_id])
            changes = {
                "owner": "baobab-platform/baobab-iam",
                "repository": "baobab-platform/baobab-iam",
                "runtime": "persistent product runtime",
                "environment": "production",
                "allowed_audiences": ["baobab-cms"],
                "allowed_scopes": ["content:entry:preview"],
                "credential_type": "federated_workload_token",
                "rotation_owner": "baobab-platform/baobab-iam",
                "status": "PROVISIONED",
                "context_purposes": ["RUNTIME"],
                "unreviewed_authority": True,
                "validates_audiences": ["baobab-pulse"],
            }
            for field, value in changes.items():
                with self.subTest(client=client_id, field=field):
                    changed = copy.deepcopy(original)
                    changed[field] = value
                    self.registry["workloads"][client_id] = changed
                    self.assertNotEqual(self.validate().returncode, 0)
            self.registry["workloads"].pop(client_id)
            self.assertNotEqual(self.validate().returncode, 0)
            self.registry["workloads"][client_id] = original

    def test_int03_does_not_promote_the_product_caller(self):
        product = self.registry["workloads"]["nabhold-backend"]
        for field, value in (("status", "ACTIVE"), ("environment", "development")):
            original = product[field]
            product[field] = value
            self.assertNotEqual(self.validate().returncode, 0)
            product[field] = original

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

