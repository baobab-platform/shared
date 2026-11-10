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
        self.assertIn("# Baobab Platform Enterprise Architecture Implementation Plan v2.2", old_plan)
        self.assertIn("**Status:** ACCEPTED", old_plan)
        self.assertIn("**Status:** Accepted programme acceptance companion", matrix)

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


    def test_shared_adr_catalogue_has_no_missing_decisions(self):
        import json
        import re

        manifest = json.loads((ROOT / "docs/assessments/adr-shared-source-traceability-2026-11-10.json").read_text())
        self.assertEqual(list(range(1, 46)), [row["number"] for row in manifest["decisions"]])
        documents = {
            match.group(1): path
            for path in (ROOT / "docs/adr").glob("ADR-*.md")
            if (match := re.match(r"^(ADR-(?:SHARED-)?\d{3,4})(?:\b|[- ])", path.name))
        }
        expected = {row["id"] for row in manifest["decisions"]}
        self.assertEqual(expected, set(documents), "ADR folder and source audit inventory diverged")
        index = (ROOT / "docs/adr/README.md").read_text()
        indexed = re.findall(r"^\|\s*\[(ADR-(?:SHARED-)?\d{3,4})\b", index, re.MULTILINE)
        self.assertEqual(len(indexed), len(set(indexed)), "Duplicate ADR register entries")
        self.assertEqual(expected, set(indexed), "Every ADR must have exactly one index entry")
        for n in range(1, 7):
            self.assertIn(f"historical ADR-{n:04}", index, "Retain accepted legacy ADR references")
        self.assertEqual("2026-11-10", manifest["audit_date"])
        self.assertTrue(all(row["runtime_qualification"] == "NOT_ASSESSED" for row in manifest["decisions"]))
        for row in manifest["decisions"]:
            with self.subTest(adr=row["id"]):
                self.assertTrue((ROOT / row["source"]).is_file())
                if row["related_check"] is not None:
                    self.assertTrue((ROOT / row["related_check"]).is_file())
                self.assertIn(row["id"], documents)
                self.assertTrue(row["owner_validation_required"])
                self.assertEqual("PROPOSED" if row["number"] == 33 else "ACCEPTED", row["decision_status"])

    def test_proposed_finance_and_accepted_product_read_are_indexed_honestly(self):
        index = (ROOT / "docs/adr/README.md").read_text()
        for number, state in ((33, "Proposed"), (44, "Accepted")):
            key = f"ADR-SHARED-{number:03}"
            row = next((line for line in index.splitlines() if line.startswith(f"| [{key} ")), None)
            self.assertIsNotNone(row, f"Missing {key}")
            self.assertIn(state, row)
        finance = next((ROOT / "docs/adr").glob("ADR-SHARED-033*.md")).read_text()
        self.assertIn("**Status:** Proposed", finance)
        read = next((ROOT / "docs/adr").glob("ADR-SHARED-044*.md")).read_text()
        self.assertIn("| Status | Accepted |", read)


if __name__ == "__main__":
    unittest.main()
