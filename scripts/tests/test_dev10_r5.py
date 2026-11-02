"""Adversarial DEV10-R5 gate tests, including forged acceptance and missing owners."""
import copy
import json
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from dev10_r5_acceptance import validate  # noqa: E402


class R5SafetyTests(unittest.TestCase):
    def setUp(self):
        self.packet = json.loads((ROOT / ".baobab/dev10-r5-acceptance.json").read_text())
        self.matrix = json.loads((ROOT / ".baobab/dev10-toolchain-matrix.json").read_text())

    def check_denied(self, modify):
        packet = copy.deepcopy(self.packet)
        modify(packet)
        with self.assertRaises(ValueError):
            validate(packet, self.matrix)

    def test_source_only_packet_is_valid_not_accepted(self):
        self.assertIn("HELD_PACKET_VALID", validate(self.packet, self.matrix))
        with self.assertRaisesRegex(ValueError, "R5_NOT_ACCEPTED"):
            validate(self.packet, self.matrix, require_final=True)

    def test_any_missing_owner_denied(self):
        self.check_denied(lambda p: p["owners"].pop())

    def test_fabricated_runtime_approval_denied(self):
        self.check_denied(lambda p: p["decision"].update(engineering_acceptance="ACCEPTED"))

    def test_fabricated_image_digest_denied(self):
        self.check_denied(lambda p: p["candidate_provider"].update(published_candidate_digest="sha256:"+"a"*64))

    def test_missing_security_failure_denied(self):
        self.check_denied(lambda p: next(x for x in p["controls"] if x["id"] == "R4-UNWAIVED-SECURITY").update(state="SOURCE_VERIFIED"))

    def test_staging_and_production_forbidden(self):
        self.check_denied(lambda p: p["decision"].update(production_approved=True))

    def test_codespaces_actions_confusion_denied(self):
        self.check_denied(lambda p: p["evidence_policy"].update(git_checks_not_hosted_codespaces=False))

    def test_wrong_owner_source_denied(self):
        self.check_denied(lambda p: p["owners"][0].update(baseline_main_sha="0"*40))

    def test_unreviewed_toolchain_major_denied(self):
        self.check_denied(lambda p: p["preferred_technologies"].update(node="24"))

    def test_duplicate_control_denied(self):
        self.check_denied(lambda p: p["controls"].append(copy.deepcopy(p["controls"][-1])))

    def test_no_unverified_urls(self):
        self.check_denied(lambda p: p["controls"][0]["evidence_urls"].append("http://example.com/accepted"))


if __name__ == "__main__":
    unittest.main()
