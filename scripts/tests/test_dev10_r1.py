"""DEV10-R1 source-only contract regression. No hosted Codespaces or image proof."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
MATRIX = ROOT / ".baobab/dev10-toolchain-matrix.json"
TARGET = ROOT / ".baobab/dev10-target-toolchains.json"


class Dev10R1Tests(unittest.TestCase):
    def setUp(self):
        self.matrix = json.loads(MATRIX.read_text())
        self.target = json.loads(TARGET.read_text())

    def test_merged_source_matches_target_policy_and_no_implicit_adoption(self):
        self.assertEqual(self.matrix["provider"]["source_sha"], self.target["provider_source_sha"])
        self.assertEqual(self.target["state"], "PREFERRED_TARGET_NOT_ENGINEERING_QUALIFIED")
        self.assertEqual(self.target["current_effective_source"]["node"], "24")
        self.assertEqual(self.target["targets"]["node"]["series"], "26")
        self.assertEqual(self.target["current_effective_source"]["pnpm"], "11.24.0")
        self.assertEqual(self.target["targets"]["pnpm"]["series"], "12")
        self.assertEqual(self.target["targets"]["java"]["major"], 21)
        self.assertEqual(self.target["targets"]["postgresql"]["major"], 17)

    def test_all_consumer_snapshots_are_closed_and_immutable(self):
        rows = self.matrix["repositories"]
        self.assertEqual(len(rows), 13)
        self.assertEqual(len({row["repo"] for row in rows}), 13)
        self.assertIn("nabhold", {row["repo"] for row in rows})
        for row in rows:
            self.assertFalse(row["fresh_codespace_observed"])
            self.assertFalse(row["upgrade_branch_qualified"])
            self.assertEqual(row["evidence_urls"], [f'https://github.com/baobab-platform/{row["repo"]}/tree/{row["source_sha"]}'])

    def test_native_engine_specific_exceptions_are_not_fabricated(self):
        rows = {row["repo"]: row for row in self.matrix["repositories"]}
        self.assertEqual(rows["baobab-subscriptions"]["native_services"][0]["image"], "postgres:17-alpine")
        self.assertIn("ghcr.io/devcontainers/features/rust:1", rows["baobab-payments"]["features"])
        self.assertEqual(rows["baobab-payments"]["native_services"][0]["image"], "postgres:16-alpine")
        self.assertIsNone(rows["baobab-tms"]["environment_profile"])
        self.assertIn("PR29", rows["baobab-tms"]["gaps"][0])

    def test_protected_and_runtime_acceptance_remains_denied(self):
        for key in ("clean_codespace_qualified", "fleet_upgrade_qualified",
                    "postgres_physical_migration_qualified", "production_authorized"):
            self.assertIs(self.matrix[key], False)


if __name__ == "__main__":
    unittest.main()
