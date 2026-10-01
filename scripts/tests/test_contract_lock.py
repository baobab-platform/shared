#!/usr/bin/env python3
"""Tests for scripts/contract_lock.py (EA Plan v2.0 EA-01A/C/D).

Each test builds a small Shared git history and a consumer repository in a
temporary directory.

  python3 -m pip install -r .github/foundation-tests/requirements.txt
  python3 scripts/tests/test_contract_lock.py
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import contract_lock as cl  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_A = '{"type": "object"}\n'
SCHEMA_B = '{"type": "object", "required": ["id"]}\n'


def git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True).stdout.strip()


class LockTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)
        self.shared_path = base / "shared"
        self.consumer = base / "consumer"
        self.consumer.mkdir()
        self.shared_path.mkdir()
        git(self.shared_path, "init", "-q", "-b", "main")
        git(self.shared_path, "config", "user.email", "test@example.invalid")
        git(self.shared_path, "config", "user.name", "test")
        self.pin = self.commit({"contracts/a/v1/a.schema.json": SCHEMA_A,
                                "contracts/b/v1/b.yaml": "kind: b\n",
                                "contracts/c/v1/c.schema.json": SCHEMA_A})
        self.shared = cl.Shared(self.shared_path)
        self.repository(lifecycle="active", capabilities=["engine", "rust"])

    def tearDown(self):
        self.tmp.cleanup()

    def commit(self, files: dict[str, str | None]) -> str:
        for path, text in files.items():
            target = self.shared_path / path
            if text is None:
                target.unlink()
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text)
        git(self.shared_path, "add", "-A")
        git(self.shared_path, "commit", "-q", "-m", "change")
        return git(self.shared_path, "rev-parse", "HEAD")

    def repository(self, lifecycle: str, capabilities: list[str]):
        path = self.consumer / ".baobab/repository.yaml"
        path.parent.mkdir(exist_ok=True)
        path.write_text(yaml.safe_dump({"repository": {"lifecycle": lifecycle}, "capabilities": capabilities}))

    def lock(self, commit: str | None = None, contracts: list[str] | None = None, **overrides):
        document = {
            "schema": "baobab-contract-consumer-lock",
            "version": "1.0",
            "source": {"repository": "baobab-platform/shared", "commit": commit or self.pin},
            "contracts": contracts or ["contracts/a/v1/a.schema.json", "contracts/b/v1/b.yaml"],
            "policy": {"updates": "explicit_pull_request", "compatibility": "validate_before_merge"},
        }
        document.update(overrides)
        (self.consumer / cl.LOCK_PATH).write_text(yaml.safe_dump(document, sort_keys=False))

    def check(self) -> list[str]:
        return cl.check(self.consumer, self.shared, "HEAD")

    def drift(self) -> dict:
        return cl.drift(self.consumer, self.shared, "HEAD")


class CheckTest(LockTest):
    def test_canonical_lock_passes(self):
        self.lock()
        self.assertEqual(self.check(), [])

    def test_active_engine_without_lock_fails(self):
        self.assertIn("is missing", self.check()[0])

    def test_active_control_plane_without_lock_fails(self):
        self.repository(lifecycle="active", capabilities=["go", "control-plane"])
        self.assertIn("is missing", self.check()[0])

    def test_experimental_engine_or_non_engine_may_omit_lock(self):
        self.repository(lifecycle="experimental", capabilities=["engine"])
        self.assertEqual(self.check(), [])
        self.repository(lifecycle="active", capabilities=["library"])
        self.assertEqual(self.check(), [])

    def test_repository_metadata_may_extend_the_lock(self):
        self.lock(contract_bundle={"name": "baobab-platform-resolution"})
        self.assertEqual(self.check(), [])

    def test_legacy_lock_shapes_fail(self):
        self.lock(schema="nabhold-contract-consumer-lock")
        self.assertTrue(any("schema" in f for f in self.check()))
        self.lock(source={"repository": "nabhold/shared", "commit": self.pin})
        self.assertTrue(any("source/repository" in f for f in self.check()))
        (self.consumer / cl.LOCK_PATH).write_text(yaml.safe_dump(
            {"version": 1, "contracts": [{"source": "baobab-platform/shared", "sha": self.pin}]}))
        self.assertTrue(self.check())

    def test_abbreviated_or_branch_pins_fail(self):
        self.lock(commit=self.pin[:12])
        self.assertTrue(any("source/commit" in f for f in self.check()))
        self.lock(commit="main")
        self.assertTrue(any("source/commit" in f for f in self.check()))

    def test_unsafe_contract_paths_fail(self):
        for path in ("contracts/../secrets.txt", "docs/adr/README.md", "/contracts/a/v1/a.schema.json"):
            self.lock(contracts=[path])
            self.assertTrue(self.check(), path)

    def test_unknown_commit_fails(self):
        self.lock(commit="0" * 40)
        self.assertIn("does not exist", self.check()[0])

    def test_commit_off_main_fails(self):
        git(self.shared_path, "checkout", "-q", "-b", "feature")
        off_main = self.commit({"contracts/a/v1/a.schema.json": SCHEMA_B})
        git(self.shared_path, "checkout", "-q", "main")
        self.lock(commit=off_main)
        self.assertIn("not on Shared main", self.check()[0])

    def test_missing_and_unparseable_contracts_fail(self):
        self.lock(contracts=["contracts/a/v1/missing.schema.json"])
        self.assertIn("does not exist at", self.check()[0])
        pin = self.commit({"contracts/a/v1/broken.schema.json": "{not json"})
        self.lock(commit=pin, contracts=["contracts/a/v1/broken.schema.json"])
        self.assertIn("does not parse", self.check()[0])

    def test_contract_removed_by_baseline_is_incompatible(self):
        self.lock()
        self.commit({"contracts/b/v1/b.yaml": None})
        self.assertIn("incompatible drift", self.check()[0])

    def test_warn_mode_passes_and_enforce_fails(self):
        self.assertEqual(cl.main(["check", "--repository-root", str(self.consumer),
                                  "--shared-repo", str(self.shared_path), "--mode", "warn"]), 0)
        self.assertEqual(cl.main(["check", "--repository-root", str(self.consumer),
                                  "--shared-repo", str(self.shared_path), "--mode", "enforce"]), 1)


class AutoModeTest(LockTest):
    def run_auto(self) -> int:
        return cl.main(["check", "--repository-root", str(self.consumer),
                        "--shared-repo", str(self.shared_path), "--mode", "auto"])

    def test_auto_enforces_for_engines(self):
        self.lock(schema="nabhold-contract-consumer-lock")
        self.assertEqual(self.run_auto(), 1)
        self.repository(lifecycle="experimental", capabilities=["engine"])
        self.assertEqual(self.run_auto(), 1)

    def test_auto_enforces_for_the_control_plane(self):
        self.repository(lifecycle="active", capabilities=["go", "control-plane"])
        self.lock(schema="nabhold-contract-consumer-lock")
        self.assertEqual(self.run_auto(), 1)

    def test_auto_warns_for_non_engines(self):
        self.repository(lifecycle="active", capabilities=["node", "digital-estate"])
        self.lock(schema="nabhold-contract-consumer-lock")
        self.assertEqual(self.run_auto(), 0)

    def test_auto_passes_a_canonical_engine_lock(self):
        self.lock()
        self.assertEqual(self.run_auto(), 0)


class DriftTest(LockTest):
    def test_current(self):
        self.lock()
        report = self.drift()
        self.assertEqual((report["classification"], report["behind"]), ("CURRENT", 0))

    def test_behind_with_unconsumed_changes_only(self):
        self.lock()
        self.commit({"contracts/c/v1/c.schema.json": SCHEMA_B})
        report = self.drift()
        self.assertEqual((report["classification"], report["behind"]), ("BEHIND_UNCHANGED", 1))

    def test_behind_with_consumed_change(self):
        self.lock()
        self.commit({"contracts/a/v1/a.schema.json": SCHEMA_B})
        self.commit({"contracts/c/v1/c.schema.json": SCHEMA_B})
        report = self.drift()
        self.assertEqual((report["classification"], report["behind"]), ("BEHIND_CHANGED", 2))
        self.assertEqual(report["contracts"][0], {"path": "contracts/a/v1/a.schema.json", "status": "changed"})
        self.assertIn("| `contracts/a/v1/a.schema.json` | changed |", cl.render_markdown(report))

    def test_removed_consumed_contract(self):
        self.lock()
        self.commit({"contracts/b/v1/b.yaml": None})
        self.assertEqual(self.drift()["classification"], "INCOMPATIBLE")

    def test_unusable_lock_is_unknown(self):
        self.assertEqual(self.drift()["reason"], "no lock")
        self.lock(schema="nabhold-contract-consumer-lock")
        self.assertEqual(self.drift()["classification"], "UNKNOWN")
        self.assertIn("Not assessed", cl.render_markdown(self.drift()))

    def test_drift_never_fails(self):
        self.lock()
        self.commit({"contracts/b/v1/b.yaml": None})
        self.assertEqual(cl.main(["drift", "--repository-root", str(self.consumer),
                                  "--shared-repo", str(self.shared_path), "--format", "json"]), 0)


class ReferenceLocksTest(unittest.TestCase):
    """The EA-01A reference shape (Payments, Subscriptions) matches the schema."""

    def test_plan_reference_shape(self):
        document = {
            "schema": "baobab-contract-consumer-lock",
            "version": "1.0",
            "source": {"repository": "baobab-platform/shared", "commit": "f20069d40361db34ea196218e6b28567e8dea11b"},
            "contracts": ["contracts/payments/v1/capabilities.json", "contracts/product/v1/billing-policy.yaml"],
            "policy": {"updates": "explicit_pull_request", "compatibility": "validate_before_merge"},
        }
        self.assertEqual(cl.schema_findings(document), [])


if __name__ == "__main__":
    unittest.main(verbosity=1)
