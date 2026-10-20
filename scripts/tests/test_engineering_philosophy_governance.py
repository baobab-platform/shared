"""Guard the normative Baobab engineering philosophy's central publication.

This is intentionally a documentation-integrity check, *not* an assertion that
every first-party repository has completed local adoption or production signoff.
Cross-repository adoption requires independently evidenced rollouts (ADR-SHARED-041).
"""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
ADR_PATH = ROOT / "docs/adr/ADR-SHARED-041 — Baobab Platform Engineering Philosophy and African Enterprise Product Excellence.md"
INDEX_PATH = ROOT / "docs/adr/README.md"
ROOT_README = ROOT / "README.md"
CHECKLIST_PATH = ROOT / "docs/governance/engineering-philosophy-review.md"

PHILOSOPHY = (
    "Learn from established products. Reuse what is proven. "
    "Question what is inadequate. Re-engineer what must improve. "
    "Build what Africa needs."
)


class EngineeringPhilosophyGovernanceTests(unittest.TestCase):
    def test_normative_adr_and_index_are_consistent(self):
        adr = ADR_PATH.read_text(encoding="utf-8")
        index = INDEX_PATH.read_text(encoding="utf-8")
        self.assertIn("**Status:** Accepted", adr)
        self.assertIn("Normative Organisation-Wide Engineering Governance", adr)
        self.assertIn(PHILOSOPHY, adr)
        self.assertIn("all current and future `baobab-*` repositories", adr)
        self.assertIn("ADR-SHARED-041", index)
        self.assertIn("Accepted 2026-10-20", index)

    def test_philosophy_is_visible_and_reviewable(self):
        readme = ROOT_README.read_text(encoding="utf-8")
        checklist = CHECKLIST_PATH.read_text(encoding="utf-8")
        self.assertIn(PHILOSOPHY, readme)
        self.assertIn(PHILOSOPHY, checklist)
        self.assertIn("engineering-philosophy-review.md", readme)
        self.assertIn("ADR-SHARED-041", checklist)

    def test_governance_does_not_claim_unproven_rollout(self):
        adr = ADR_PATH.read_text(encoding="utf-8")
        self.assertIn("individual repository adoption", adr)
        self.assertIn("Existing code is not retroactively claimed noncompliant", adr)
        self.assertIn("not a current certification, ranking or marketing claim", adr)
        self.assertIn("protected production", adr.lower())


if __name__ == "__main__":
    unittest.main()
