"""DEV-00 reporting regressions; these tests never claim runtime acceptance."""
import copy
from datetime import date, timedelta
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts/ea_dev_register.py"
spec = importlib.util.spec_from_file_location("ea_dev_register", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class RegisterTests(unittest.TestCase):
    def setUp(self):
        self.live = json.loads(module.REGISTER.read_text(encoding="utf-8"))
        # Mutation tests use a stable source-only fixture, not today's progress
        # or calendar state. Normal register maintenance must not break them.
        self.data = copy.deepcopy(self.live)
        self.data["observed_on"] = "2026-10-24"
        for package in self.data["packages"]:
            package.update(observed_on="2026-10-24", actual_completion_date=None,
                           progress="SOURCE_IN_PROGRESS", assessment="IMPLEMENTED_PENDING_REVIEW",
                           mandatory_ci="PENDING_THIS_PR", environment="NO_RUNTIME_OBSERVED",
                           evidence_class="SOURCE", protected_staging_accepted=False,
                           external_certification_accepted=False, production_accepted=False)
            package["blockers"] = [{"kind": "IMPLEMENTED_NOT_TESTED", "detail": "Test fixture only"}]
            package["runtime"].update(status="NOT_OBSERVED", evidence_urls=[], cleanup="NOT_OBSERVED")
            for case in package["runtime"]["cases"]:
                case.update(result="BLOCKED", evidence_urls=[], reason="TEST_FIXTURE_ONLY")

    def rejects(self, mutate):
        data = copy.deepcopy(self.data)
        mutate(data)
        with self.assertRaises((ValueError, TypeError)):
            module.validate(data)

    def test_inventory_and_generated_view_are_valid(self):
        module.validate(self.live)
        self.assertEqual(module.render(self.live), module.VIEW.read_text(encoding="utf-8"))

    def test_missing_and_duplicate_packages_are_rejected(self):
        self.rejects(lambda d: d["packages"].pop())
        self.rejects(lambda d: d["packages"].__setitem__(1, d["packages"][0]))

    def test_cycles_and_unknown_dependencies_are_rejected(self):
        self.rejects(lambda d: d["packages"][0]["dependencies"].append("DEV-01"))
        self.rejects(lambda d: d["packages"][0]["dependencies"].append("DEV-99"))

    def test_missing_duplicate_or_skipped_runtime_cases_are_rejected(self):
        self.rejects(lambda d: d["packages"][4]["runtime"]["cases"].pop())
        self.rejects(lambda d: d["packages"][5]["runtime"]["cases"].append(
            d["packages"][5]["runtime"]["cases"][0]))
        self.rejects(lambda d: d["packages"][5]["runtime"]["cases"][0].update(result="NOT_APPLICABLE"))

    def test_source_ci_cannot_promote_runtime_or_protected_acceptance(self):
        self.rejects(lambda d: d["packages"][4]["runtime"].update(status="PASS"))
        self.rejects(lambda d: d["packages"][4]["runtime"]["cases"][0].update(result="PASS"))
        self.rejects(lambda d: d["packages"][0].update(progress="REAL_COMPONENT_SYNTHETIC_DATA"))
        for name in ("protected_staging_accepted", "external_certification_accepted", "production_accepted"):
            self.rejects(lambda d: d["packages"][0].update({name: True}))

    def test_runtime_summary_requires_every_case_and_complete_cleanup(self):
        package = self.data["packages"][4]
        package.update(environment="ISOLATED_DEVELOPMENT", evidence_class="REAL_COMPONENT_SYNTHETIC_DATA")
        url = "https://github.com/baobab-platform/infrastructure/actions/runs/123"
        package["runtime"].update(status="PASS", evidence_urls=[url], cleanup="COMPLETE")
        for case in package["runtime"]["cases"]:
            case.update(result="PASS", evidence_urls=[url], reason="TEST_ONLY_REFERENCE_NOT_AN_ACTUAL_RECEIPT")
        # The validator checks reporting consistency, not the external receipt.
        # The owning reviewer must independently verify every linked assertion.
        module.validate(self.data)
        self.rejects(lambda d: d["packages"][4]["runtime"].update(cleanup="NOT_OBSERVED"))
        self.rejects(lambda d: d["packages"][4]["runtime"]["cases"][0].update(result="BLOCKED"))

    def test_source_and_ci_references_are_immutable_and_owner_scoped(self):
        self.rejects(lambda d: d["baselines"][0].update(sha="main"))
        self.rejects(lambda d: d["baselines"][0].update(ci_urls=[]))
        self.rejects(lambda d: d["baselines"][0].update(
            ci_urls=["https://github.com/baobab-platform/other/actions/runs/1"]))
        self.rejects(lambda d: d["packages"][0]["source_baselines"].append("imaginary-source"))
        self.rejects(lambda d: d["packages"][0].update(progress="SOURCE_MERGED"))
        self.rejects(lambda d: d["packages"][0].update(environment="production"))

    def test_duplicate_json_keys_are_rejected(self):
        with self.assertRaises(ValueError):
            json.loads('{"status":"BLOCKED","status":"PASS"}', object_pairs_hook=module.unique_object)

    def test_no_unknown_fields_or_changed_canonical_case_ids(self):
        self.rejects(lambda d: d.update(force_active=True))
        self.rejects(lambda d: d["packages"][0].update(skip_security=True))
        self.rejects(lambda d: d["packages"][5]["runtime"]["canonical_scenarios"].append("NAB-99"))

    def test_future_completion_and_incomplete_package_are_rejected(self):
        self.rejects(lambda d: d["packages"][0].update(actual_completion_date="2099-01-01"))
        self.rejects(lambda d: d["packages"][4].update(actual_completion_date="2026-10-24"))

    def test_staleness_is_visible_without_fabricating_freshness_or_freezing_ci(self):
        self.assertEqual(module.freshness(self.data, date(2026, 10, 31)), "WITHIN_OBSERVATION_WINDOW")
        self.assertEqual(module.freshness(self.data, date(2026, 11, 1)), "STALE")
        stale_on = date.fromisoformat(self.live["observed_on"]) + timedelta(days=self.live["freshness_days"] + 1)
        result = subprocess.run([sys.executable, str(SCRIPT), "--check", "--as-of", stale_on.isoformat()],
                                capture_output=True, text=True, check=True)
        self.assertIn("STALE", result.stdout)
        self.assertIn("validation grants no runtime qualification", result.stdout)
        self.assertEqual(self.data["observed_on"], "2026-10-24")
        self.data["packages"][2]["observed_on"] = "2026-10-01"
        self.assertEqual(module.freshness(self.data, date(2026, 10, 24)), "STALE")

    def test_register_does_not_require_an_optional_49_packet(self):
        # All required reporting inputs live in Shared. No packet, identities,
        # network, database or external service is an input to this CI check.
        result = subprocess.run([sys.executable, str(SCRIPT), "--check", "--as-of", self.live["observed_on"]],
                                capture_output=True, text=True, check=True)
        self.assertIn("VALID_REGISTER_SOURCE_ONLY", result.stdout)
        source = SCRIPT.read_text(encoding="utf-8")
        self.assertNotIn("int03c_approval_packet", source)

    def test_retained_dev01_originals_preserve_hashes_and_scope(self):
        # This dated historical receipt is intentionally immutable; it is not
        # the mutable register clock used by the maintenance tests above.
        folder = ROOT / "docs/architecture/evidence/dev01-2026-10-24"
        suite = json.loads((folder / "dev01-lifecycle-suite.json").read_text())
        self.assertEqual(len(suite["checks"]), 6)
        self.assertTrue(all(value is True for value in suite["checks"].values()))
        receipts = list(folder.glob("dev01-*/completed/receipt.json"))
        self.assertEqual(len(receipts), 2)
        passed = []
        for path in receipts:
            raw = path.read_bytes()
            digest = json.loads(path.with_name("receipt.sha256.json").read_text())
            self.assertEqual(hashlib.sha256(raw).hexdigest(), digest["sha256"])
            receipt = json.loads(raw)
            self.assertEqual(receipt["harness_sha"], suite["harness_sha"])
            self.assertIs(receipt["teardown_verified"], True)
            self.assertIs(receipt["protected_acceptance"], False)
            self.assertIs(receipt["production_authorized"], False)
            self.assertIs(receipt["int03c_qualified"], False)
            self.assertIs(receipt["nab03_qualified"], False)
            passed.append(receipt["lifecycle_passed"])
        self.assertEqual(sorted(passed), [False, True])

    def test_retained_dev02_fixture_inventory_is_non_authorising(self):
        folder = ROOT / "docs/architecture/evidence/dev02-2026-10-24"
        raw = (folder / "dev02-fixture-suite.json").read_bytes()
        digest = json.loads((folder / "dev02-fixture-suite.sha256.json").read_text())
        self.assertEqual(hashlib.sha256(raw).hexdigest(), digest["sha256"])
        suite = json.loads(raw)
        self.assertEqual(suite["schema"], "infrastructure.dev02.fixture-suite.v1")
        self.assertEqual(suite["source_pins"]["baobab-cp"], "6ed4c63f4e28b3370c4f83c097f22d2308f4d474")
        self.assertIs(suite["teardown_verified"], True)
        for key in ("protected_acceptance", "production_authorized", "int03c_qualified", "nab03_qualified"):
            self.assertIs(suite[key], False)
        report = suite["fixture_checks"]
        self.assertIs(report["synthetic_only"], True)
        for key in ("official_actor_verified", "provider_permissions_granted", "protected_acceptance"):
            self.assertIs(report[key], False)
        expected = {"valid_scoped": "ACTOR_NOT_VERIFIED", "missing": "NO_APPLICABLE_MANDATE",
                    "stale": "REVOKED_OR_EXPIRED", "revoked": "REVOKED_OR_EXPIRED",
                    "wrong_market": "NO_APPLICABLE_MANDATE", "pending": "NO_APPLICABLE_MANDATE"}
        expected.update({"boundary_wrong_" + field: "NO_APPLICABLE_MANDATE"
                         for field in ("role", "activity", "capability", "tenant", "organisation", "market")})
        rows = report["observations"]
        self.assertEqual(len(rows), 24)
        self.assertEqual({(row["enterprise"], row["case"]) for row in rows},
                         {(e, key) for e in ("zuribeans", "equator-estate") for key in expected})
        for row in rows:
            self.assertIs(row["passed"], True)
            self.assertEqual(row["policy_outcome"], expected[row["case"]])

    def test_legitimate_date_refresh_keeps_a_valid_register(self):
        refreshed = copy.deepcopy(self.data)
        refreshed["observed_on"] = "2027-01-02"
        for package in refreshed["packages"]:
            package["observed_on"] = refreshed["observed_on"]
        module.validate(refreshed)
        self.assertEqual(module.freshness(refreshed, date(2027, 1, 2)), "WITHIN_OBSERVATION_WINDOW")


if __name__ == "__main__":
    unittest.main()
