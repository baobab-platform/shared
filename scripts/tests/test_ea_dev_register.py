"""DEV-00 reporting regressions; these tests never claim runtime acceptance."""
import copy
from datetime import date
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
        self.data = json.loads(module.REGISTER.read_text(encoding="utf-8"))

    def rejects(self, mutate):
        data = copy.deepcopy(self.data)
        mutate(data)
        with self.assertRaises((ValueError, TypeError)):
            module.validate(data)

    def test_inventory_and_generated_view_are_valid(self):
        module.validate(self.data)
        self.assertEqual(module.render(self.data), module.VIEW.read_text(encoding="utf-8"))

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
        result = subprocess.run([sys.executable, str(SCRIPT), "--check", "--as-of", "2026-11-01"],
                                capture_output=True, text=True, check=True)
        self.assertIn("STALE", result.stdout)
        self.assertIn("runtime not qualified", result.stdout)
        self.assertEqual(self.data["observed_on"], "2026-10-24")
        self.data["packages"][2]["observed_on"] = "2026-10-01"
        self.assertEqual(module.freshness(self.data, date(2026, 10, 24)), "STALE")

    def test_register_does_not_require_an_optional_49_packet(self):
        # All required reporting inputs live in Shared. No packet, identities,
        # network, database or external service is an input to this CI check.
        result = subprocess.run([sys.executable, str(SCRIPT), "--check", "--as-of", "2026-10-24"],
                                capture_output=True, text=True, check=True)
        self.assertIn("VALID_REGISTER_SOURCE_ONLY", result.stdout)
        source = SCRIPT.read_text(encoding="utf-8")
        self.assertNotIn("int03c_approval_packet", source)


if __name__ == "__main__":
    unittest.main()
