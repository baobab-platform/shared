"""BA-SEC-DEP-001 advisory watcher tests; offline and no live secrets/network."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "scripts/action_advisory_watch.py"
spec = importlib.util.spec_from_file_location("action_advisory_watch", SOURCE)
watch = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(watch)

SHA = "0123456789abcdef" * 2 + "12345678"
SECOND_SHA = "fedcba9876543210" * 2 + "87654321"


def action_advisory(name="owner/tool", ghsa="GHSA-aaaa-bbbb-cccc"):
    return {
        "ghsa_id": ghsa,
        "severity": "high",
        "html_url": "https://github.com/advisories/" + ghsa,
        "vulnerabilities": [{
            "package": {"ecosystem": "actions", "name": name},
            "vulnerable_version_range": "< 2.3.0",
            "first_patched_version": "2.3.0",
        }],
    }


class ActionAdvisoryWatchTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory(prefix="baobab-action-watch-")
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        (self.root / ".github/workflows").mkdir(parents=True)
        (self.root / ".github/actions/custom").mkdir(parents=True)
        self.workflow = self.root / ".github/workflows/ci.yml"
        self.workflow.write_text(
            "steps:\n"
            f"  - uses: Owner/Tool@{SHA} # v2.2.0\n"
            f"  - uses: org/reusable/.github/workflows/ci.yml@{SECOND_SHA} # v1.2.3\n"
            f"  - uses: ./local\n"
            f"  - uses: docker://repo/image@sha256:{'a' * 64}\n",
            encoding="utf-8",
        )
        (self.root / ".github/actions/custom/action.yml").write_text(
            f"runs:\n  steps:\n    - uses: owner/tool@{SECOND_SHA}\n", encoding="utf-8",
        )

    def test_inventory_detects_external_sha_actions_and_reusable_workflows(self):
        entries = watch.inventory(self.root)
        self.assertEqual(len(entries), 3)
        self.assertEqual([entry["package"] for entry in entries], [
            "org/reusable", "owner/tool", "owner/tool"
        ])
        self.assertEqual(entries[0]["version_hint"], "v1.2.3")
        self.assertIsNone(entries[1]["version_hint"])
        self.assertTrue(all(len(e["sha"]) == 40 for e in entries))

    def test_matching_public_package_is_triage_not_vulnerable_sha_claim(self):
        result = watch.review(self.root, [action_advisory()])
        self.assertEqual(result["status"], "TRIAGE_REQUIRED")
        self.assertEqual(len(result["matches"]), 2)
        for item in result["matches"]:
            self.assertEqual(item["affected_sha"], "UNKNOWN_REQUIRES_UPSTREAM_RELEASE_VERIFICATION")
            self.assertEqual(item["ghsa_id"], "GHSA-aaaa-bbbb-cccc")
        self.assertEqual(result["action_references"], 3)

    def test_missing_match_is_not_clearance(self):
        result = watch.review(self.root, [])
        self.assertEqual(result["status"], "NO_PACKAGE_MATCH_NOT_A_SECURITY_CLEARANCE")
        self.assertEqual(result["matches"], [])
        self.assertTrue(any("not prove" in note for note in result["limitations"]))

    def test_unreviewed_or_different_ecosystem_advisory_not_classified(self):
        row = action_advisory()
        row["vulnerabilities"][0]["package"]["ecosystem"] = "npm"
        result = watch.review(self.root, [row])
        self.assertEqual(result["matches"], [])

    def test_reusable_workflow_is_checked_by_package_owner_repo(self):
        result = watch.review(self.root, [action_advisory("org/reusable")])
        self.assertEqual(len(result["matches"]), 1)
        self.assertEqual(result["matches"][0]["package"], "org/reusable")

    def test_empty_and_malformed_advisory_rows_are_safe(self):
        result = watch.review(self.root, [{}, {"ghsa_id": "GHSA-test", "vulnerabilities": []}])
        self.assertEqual(result["matches"], [])

    def test_cli_offline_json_output_contains_status_and_no_credentials(self):
        data_path = self.root / "sample-advisories.json"
        data_path.write_text(json.dumps([action_advisory()]), encoding="utf-8")
        output = self.root / "report.json"
        proc = subprocess.run([
            sys.executable, str(SOURCE), "--root", str(self.root),
            "--advisories-file", str(data_path), "--output", str(output),
        ], capture_output=True, text=True, timeout=15)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        report = json.loads(output.read_text(encoding="utf-8"))
        self.assertEqual(report["status"], "TRIAGE_REQUIRED")
        self.assertNotIn("TOKEN", output.read_text(encoding="utf-8"))

    def test_cli_unavailable_source_is_unknown_not_clean(self):
        output = self.root / "report.json"
        proc = subprocess.run([
            sys.executable, str(SOURCE), "--root", str(self.root),
            "--advisories-file", str(self.root / "not-found.json"),
            "--output", str(output),
        ], capture_output=True, text=True, timeout=15)
        self.assertEqual(proc.returncode, 2)
        self.assertEqual(json.loads(output.read_text())["status"], "UNKNOWN_SOURCE_UNAVAILABLE")

    def test_pinning_enforcement_and_monitoring_separate(self):
        action_text = (ROOT / ".github/workflows/action-advisory-watch.yml").read_text()
        self.assertIn("permissions:\n  contents: read", action_text)
        self.assertNotIn("pull_request_target", action_text)
        self.assertIn("retention-days: 90", action_text)


if __name__ == "__main__":
    unittest.main()
