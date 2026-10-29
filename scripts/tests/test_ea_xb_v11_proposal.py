"""EA-XB v1.1 proposal structural safety and backwards-compatibility checks.

This test intentionally does NOT execute regulatory, finance, ERP, external
provider or cross-border operations; CI green is not architecture approval.
"""
import copy
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "validate_ea_xb_v11_proposal.py"
SPEC = importlib.util.spec_from_file_location("validate_ea_xb_v11_proposal", SCRIPT)
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)

PROPOSAL = json.loads(validator.PROPOSAL_PATH.read_text(encoding="utf-8"))
BASELINE = json.loads(validator.HISTORICAL_PATH.read_text(encoding="utf-8"))


class CorrectiveArchitectureProposalTest(unittest.TestCase):
    def test_full_source_publication_and_source_matrix(self):
        self.assertEqual(validator.validate(), [])

    def test_profile_sets_and_historical_xbe_unmodified(self):
        self.assertEqual(set(PROPOSAL["profiles"]), set(validator.EXPECTED))
        self.assertEqual([x["id"] for x in BASELINE["cases"]], list(validator.LEGACY_IDS))
        self.assertEqual([x["original_case_id"] for x in PROPOSAL["legacy_xbe_crosswalk"]],
                         list(validator.LEGACY_IDS))
        self.assertEqual(PROPOSAL["execution_status"], "NOT_EXECUTED")
        self.assertEqual(PROPOSAL["status"], "PROPOSED_FOR_REVIEW")

    def test_rejects_unscoped_manufacturing_as_universal_requirement(self):
        altered = copy.deepcopy(PROPOSAL)
        altered["profiles"]["XB-MFG"]["mandatory_for_cross_border"] = True
        self.assertIn("incorrect universal applicability",
                      " ".join(validator.check_manifest(altered, BASELINE)))

    def test_rejects_required_buyer_tenant_for_external_exchange(self):
        altered = copy.deepcopy(PROPOSAL)
        target = next(x for x in altered["reference_scenarios"]
                      if x["id"] == "MFG-PUMPS-ZA-UG-EXTERNAL")
        target["buyer_variant"] = "DUAL_QUALIFIED_TENANT"
        self.assertIn("buyer evidence variant changed",
                      " ".join(validator.check_manifest(altered, BASELINE)))

    def test_rejects_false_approval_and_execution_status(self):
        altered = copy.deepcopy(PROPOSAL)
        altered["status"] = "ACCEPTED"
        altered["cases"][0]["status"] = "PASS"
        errors = " ".join(validator.check_manifest(altered, BASELINE))
        self.assertIn("cannot claim acceptance", errors)
        self.assertIn("fabricated execution evidence", errors)

    def test_rejects_loss_of_legacy_case_mapping(self):
        altered = copy.deepcopy(PROPOSAL)
        altered["legacy_xbe_crosswalk"].pop(8)
        self.assertIn("must map once", " ".join(validator.check_manifest(altered, BASELINE)))

    def test_rejects_buyer_ap_inferred_from_seller_invoice(self):
        altered = copy.deepcopy(PROPOSAL)
        altered["governance"]["non_tenant_foreign_ledger_unobservable"] = False
        altered["legacy_xbe_crosswalk"][14]["proposed_case_ids"] = ["XBN-04"]
        errors = " ".join(validator.check_manifest(altered, BASELINE))
        self.assertIn("governance obligation disabled", errors)
        self.assertIn("XBE-15 must split", errors)

    def test_no_unreviewed_new_canonical_keys(self):
        doc = validator.DOCUMENT_PATH.read_text(encoding="utf-8")
        self.assertIn("NOT REGISTERED", doc)
        self.assertIn("No provider monopoly", doc)
        self.assertIn("explicit Platform Owner acceptance", doc)


if __name__ == "__main__":
    unittest.main()
