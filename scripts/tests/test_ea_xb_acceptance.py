"""EA-XB acceptance inventory structural and fail-closed publication tests.

Tests do NOT execute a customs clearance, manufacturing, shipment or payment.
"""
from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "validate_ea_xb_acceptance.py"
SPEC = importlib.util.spec_from_file_location("validate_ea_xb_acceptance", SCRIPT)
assert SPEC and SPEC.loader
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)
MANIFEST = json.loads(module.MANIFEST.read_text(encoding="utf-8"))


class CrossBorderProgrammeTest(unittest.TestCase):
    def test_complete_design_validates_and_publication_is_linked(self):
        self.assertEqual(module.validate(), [])

    def test_all_cases_mandatory_and_no_execution_evidence(self):
        self.assertEqual([case["id"] for case in MANIFEST["cases"]], list(module.CASE_IDS))
        self.assertTrue(all(case["required"] is True for case in MANIFEST["cases"]))
        self.assertTrue(all(case["status"] == "NOT_RUN" and case["evidence"] is None
                            for case in MANIFEST["cases"]))
        self.assertEqual(MANIFEST["evidence_class"], "DESIGN_ONLY")
        self.assertEqual(MANIFEST["run_status"], "NOT_EXECUTED")

    def test_rejects_removing_or_reordering_mandatory_case(self):
        changed = deepcopy(MANIFEST)
        changed["cases"].pop(8)
        self.assertIn("exact, ordered, unique", " ".join(module.validate_manifest(changed)))
        changed = deepcopy(MANIFEST)
        changed["cases"][0], changed["cases"][1] = changed["cases"][1], changed["cases"][0]
        self.assertIn("exact, ordered, unique", " ".join(module.validate_manifest(changed)))

    def test_rejects_false_pass_or_synthetic_external_approval(self):
        changed = deepcopy(MANIFEST)
        changed["cases"][0]["status"] = "PASS"
        self.assertIn("design must not claim PASS", " ".join(module.validate_manifest(changed)))
        changed = deepcopy(MANIFEST)
        changed["scenario_topology"]["corridor"]["customs_approval"] = "GRANTED"
        self.assertIn("must not be fabricated", " ".join(module.validate_manifest(changed)))
        changed = deepcopy(MANIFEST)
        changed["evidence_class"] = "PRODUCTION_ACCEPTANCE"
        self.assertIn("design is not runtime evidence", " ".join(module.validate_manifest(changed)))

    def test_rejects_subscribed_only_buyer_and_hidden_digital_estate(self):
        changed = deepcopy(MANIFEST)
        changed["scenario_topology"]["importer"]["variant"] = ["INDEPENDENT_EXTERNAL_CLIENT_TENANT"]
        self.assertIn("both tenant and non-tenant buyer", " ".join(module.validate_manifest(changed)))
        changed = deepcopy(MANIFEST)
        changed["scenario_topology"]["exporter"]["digital_estate_required"] = True
        self.assertIn("must not require a DigitalEstate", " ".join(module.validate_manifest(changed)))

    def test_rejects_missing_negatives_and_unowned_cases(self):
        changed = deepcopy(MANIFEST)
        changed["cases"][4]["negative"] = ""
        self.assertIn("negative must be substantive", " ".join(module.validate_manifest(changed)))
        changed = deepcopy(MANIFEST)
        changed["cases"][9]["owners"] = []
        self.assertIn("responsible owners", " ".join(module.validate_manifest(changed)))

    def test_programme_does_not_mutate_existing_l4_registry(self):
        l4 = module.L4.read_text(encoding="utf-8")
        self.assertIn("INT-07", l4)
        self.assertIn("INT-08", l4)
        self.assertNotIn("XBE-01", l4)


if __name__ == "__main__":
    unittest.main()
