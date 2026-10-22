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


class ValidatorHumanTokenProfileTests(unittest.TestCase):
    """ADR-SHARED-042 section 14: an estate BFF's human token profile and its own handoff credential."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        shutil.copytree(ROOT / "contracts", self.root / "contracts")
        (self.root / "scripts").mkdir()
        shutil.copy2(ROOT / "scripts/validate-authorization-contracts.rb", self.root / "scripts")
        self.path = self.root / "contracts/identity/v1/workload-registry.yaml"
        self.registry = yaml.safe_load(self.path.read_text())
        bff = copy.deepcopy(self.registry["workloads"]["zuribeans-backend"])
        bff.update(status="PROVISIONED", allowed_audiences=["baobab-trade"], allowed_scopes=["trade:buyer-handoff"],
                   human_token_profile={"purpose": "ESTATE_BFF_BUYER", "audiences": ["baobab-trade"], "scopes": ["trade:buy"]})
        self.registry["workloads"]["synthetic-estate-bff"] = bff

    def validate(self):
        self.path.write_text(yaml.safe_dump(self.registry))
        return subprocess.run(
            ["ruby", str(self.root / "scripts/validate-authorization-contracts.rb")],
            capture_output=True, text=True, check=False,
        )

    def bff(self):
        return self.registry["workloads"]["synthetic-estate-bff"]

    def refused(self, reason):
        result = self.validate()
        self.assertNotEqual(0, result.returncode)
        self.assertIn(reason, result.stdout + result.stderr)

    def test_no_canonical_workload_holds_a_profile_or_the_handoff_scope(self):
        canonical = yaml.safe_load((ROOT / "contracts/identity/v1/workload-registry.yaml").read_text())["workloads"]
        for client_id, entry in canonical.items():
            with self.subTest(workload=client_id):
                self.assertNotIn("human_token_profile", entry)
                self.assertNotIn("trade:buyer-handoff", entry.get("allowed_scopes", []))

    def test_a_confidential_bff_with_both_validates(self):
        result = self.validate()
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_the_handoff_scope_and_profile_are_never_held_alone(self):
        self.bff().pop("human_token_profile")
        self.refused("registers no human_token_profile")
        self.setUp()
        self.bff()["allowed_scopes"] = ["context:resolve"]
        self.bff()["allowed_audiences"] = ["baobab-control-plane"]
        self.refused("human_token_profile requires trade:buyer-handoff")

    def test_profile_is_closed_human_only_and_never_control_plane(self):
        for change, reason in [
            ({"purpose": "ANYTHING"}, "purpose must be ESTATE_BFF_BUYER"),
            ({"scopes": ["context:resolve"]}, "is not a human-only scope"),
            ({"scopes": ["trade:buyer-handoff"]}, "is not a human-only scope"),
            ({"scopes": []}, "distinct, non-empty lists"),
            ({"audiences": ["baobab-control-plane"]}, "must not include baobab-control-plane"),
            ({"audiences": ["baobab-trade", "baobab-erp"]}, "audience baobab-erp has no human scope"),
            ({"extra": True}, "must name exactly purpose, audiences and scopes"),
        ]:
            self.setUp()
            self.bff()["human_token_profile"].update(change)
            with self.subTest(change=change):
                self.refused(reason)

    def test_only_a_confidential_client_qualifies(self):
        self.bff()["credential_type"] = "federated_workload_token"
        self.refused("requires a client_credentials (confidential) client")


if __name__ == "__main__":
    unittest.main()

