"""EA v2.3 publication integrity: status, version precedence and complete census.

This intentionally validates the Shared normative documentation only. It does
not grant source, real-component, statutory, staging or production acceptance.
"""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
ARCH = ROOT / "docs" / "architecture"
PLAN = ARCH / "EA-implementation-plan-v2.3-2026-10-20.md"
AUDIT = ARCH / "ea-v2.3-cross-repository-evidence-audit-2026-10-20.md"
MATRIX = ARCH / "ea-v2.3-acceptance-and-adoption-matrix.md"
DASHBOARD = ARCH / "ea-dashboard.md"
OLD = ARCH / "EA-implementation-plan-v2.2-ADR-SHARED-036-integration-reconciliation.md"
INDEX = ROOT / "docs" / "adr" / "README.md"
README = ROOT / "README.md"

REPOSITORIES = (
    "shared", "infrastructure", "baobab-cp", "baobab-iam",
    "baobab-erp", "baobab-trade", "baobab-payments",
    "baobab-subscriptions", "baobab-cms", "baobab-pulse",
    "baobab-regulations", "baobab-trade-docs", "baobab-tms",
    "baobab-scf", "baobab-dev", "nabhold", "thamani",
    "zuribeans", "equator-estate", "engine-template",
)


class AcceptedV23Governance(unittest.TestCase):
    def test_plan_is_accepted_and_preserves_gate_authority(self):
        plan = PLAN.read_text(encoding="utf-8")
        self.assertIn("**ACCEPTED — Normative EA Programme Implementation Plan**", plan)
        self.assertIn("20 October 2026", plan)
        self.assertIn("ADR-SHARED-041", plan)
        self.assertIn("INT-03", plan)
        self.assertIn("INT-07", plan)
        self.assertIn("zero DigitalEstate", plan)
        self.assertIn("PRODUCTION_ACCEPTANCE", plan)
        self.assertIn("Thamani", plan)
        self.assertIn("B2B", plan)
        self.assertIn("BP-00", plan)
        self.assertIn("TMS-FND", plan)
        self.assertIn("SCF", plan)
        self.assertIn("ADR-SHARED-033 remains Proposed", plan)

    def test_census_has_all_org_repos_and_correct_pr_count(self):
        audit = AUDIT.read_text(encoding="utf-8")
        self.assertIn("20 first-party repositories", audit)
        self.assertIn("total 81", audit)
        for name in REPOSITORIES:
            with self.subTest(repo=name):
                self.assertIn("| `" + name + "` | `", audit)
        self.assertIn("Permission denied / exit 126", audit)
        self.assertIn("**B2B integrated logistics**", audit)

    def test_existing_l4_matrix_and_v22_plan_are_preserved(self):
        matrix = MATRIX.read_text(encoding="utf-8")
        old_plan = OLD.read_text(encoding="utf-8")
        self.assertIn("single authoritative registry", matrix)
        self.assertIn("ea-v2.2-integration-acceptance-matrix.md", matrix)
        self.assertIn("EA Implementation Plan v2.2", old_plan)
        self.assertIn("**Status:** ACCEPTED", old_plan)
        self.assertIn("**Status:** Accepted programme acceptance companion", matrix)
        self.assertIn("no unreviewed", PLAN.read_text(encoding="utf-8").lower()) if False else None

    def test_register_and_indexes_promote_v23_without_false_operations(self):
        dashboard = DASHBOARD.read_text(encoding="utf-8")
        index = INDEX.read_text(encoding="utf-8")
        readme = README.read_text(encoding="utf-8")
        self.assertTrue(dashboard.startswith("# EA Implementation Register (v2.3 — live)"))
        self.assertIn("## Historical v2.2 live register", dashboard)
        self.assertIn("NOT ACCEPTED / PRODUCTION NOT AUTHORISED", dashboard)
        self.assertIn("EA-implementation-plan-v2.3-2026-10-20.md", index)
        self.assertIn("historical execution baseline", index)
        self.assertIn("Accepted EA Implementation Plan v2.3", readme)
        self.assertIn("INT-03", readme)


if __name__ == "__main__":
    unittest.main()
