"""BA-SEC-DEP-001 conformance tests.

Extract and execute the *actual embedded workflow validator* in a disposable
repository. This avoids green tests against a second, divergent implementation.
Tests use synthetic manifests, not network registries or live credentials.
"""
from __future__ import annotations

import copy
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = ROOT / ".github/workflows/enforce-dependabot-config.yml"
ACTUAL = ROOT / ".github/dependabot.yml"
TEMPLATE = ROOT / "templates/dependabot.yml"


def validator_source() -> str:
    workflow = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
    steps = workflow["jobs"]["check"]["steps"]
    matches = [step for step in steps if step.get("name", "").startswith("Validate dependabot.yml")]
    if len(matches) != 1:
        raise AssertionError("expected exactly one real embedded conformance script")
    return matches[0]["run"]


def entry(ecosystem: str, directory: str = "/") -> dict:
    return {
        "package-ecosystem": ecosystem,
        "directory": directory,
        "schedule": {"interval": "weekly"},
        "open-pull-requests-limit": 5,
        "labels": ["dependencies"],
        "commit-message": {"prefix": "chore"},
        "groups": {
            "routine": {
                "applies-to": "version-updates",
                "patterns": ["*"],
                "update-types": ["minor", "patch"],
            }
        },
    }


class DependabotMaintenancePolicyTests(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        self.sandbox = tempfile.TemporaryDirectory(prefix="baobab-dependabot-policy-")
        self.addCleanup(self.sandbox.cleanup)
        self.root = Path(self.sandbox.name)
        (self.root / ".github/workflows").mkdir(parents=True)
        (self.root / ".github/workflows/ci.yml").write_text("name: Synthetic\n", encoding="utf-8")
        (self.root / "package.json").write_text('{"name":"synthetic","private":true}\n', encoding="utf-8")
        self.config = {"version": 2, "updates": [entry("github-actions"), entry("npm")]}

    def run_policy(self, *, mode="strict", required="github-actions", save=True):
        config_file = self.root / ".github/dependabot.yml"
        if save:
            config_file.write_text(yaml.safe_dump(self.config, sort_keys=False), encoding="utf-8")
        env = {
            **os.environ,
            "REQUIRED_ECOSYSTEMS": required,
            "POLICY_LEVEL": mode,
            "DEFAULT_BRANCH": "main",
        }
        return subprocess.run(
            [sys.executable, "-c", validator_source()],
            cwd=self.root, env=env, capture_output=True, text=True, timeout=12,
            check=False,
        )

    def assert_invalid(self, expected):
        result = self.run_policy()
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn(expected, result.stdout + result.stderr)

    def test_shared_configuration_and_template_are_parseable_and_default_branch_safe(self):
        for path in (ACTUAL, TEMPLATE):
            with self.subTest(path=path):
                parsed = yaml.safe_load(path.read_text(encoding="utf-8"))
                self.assertEqual(parsed["version"], 2)
                self.assertTrue(parsed["updates"])
                self.assertTrue(all("target-branch" not in e for e in parsed["updates"]))
                for update in parsed["updates"]:
                    for group in update.get("groups", {}).values():
                        self.assertEqual(group.get("applies-to"), "version-updates")

    def test_shared_has_root_pnpm_coverage(self):
        parsed = yaml.safe_load(ACTUAL.read_text(encoding="utf-8"))
        ecosystems = {e["package-ecosystem"] for e in parsed["updates"]}
        self.assertIn("npm", ecosystems)
        self.assertIn("github-actions", ecosystems)
        self.assertTrue((ROOT / "pnpm-lock.yaml").is_file())
        self.assertTrue((ROOT / "package.json").is_file())

    def test_strict_valid_actions_and_npm(self):
        result = self.run_policy(required="github-actions,npm")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("passes BA-SEC-DEP-001 (strict)", result.stdout)

    def test_baseline_supports_legacy_unscoped_group_without_weakening_strict(self):
        del self.config["updates"][0]["groups"]["routine"]["applies-to"]
        result = self.run_policy(mode="baseline")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assert_invalid("must explicitly set applies-to")

    def test_missing_config_fails(self):
        result = self.run_policy(save=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing .github/dependabot.yml", result.stdout)

    def test_wrong_schema_fails(self):
        self.config["version"] = 1
        self.assert_invalid("version must be exactly 2")

    def test_missing_required_ecosystem_fails(self):
        self.config["updates"] = [entry("npm")]
        self.assert_invalid("missing required ecosystem")

    def test_root_manifest_without_ecosystem_fails(self):
        self.config["updates"] = [entry("github-actions")]
        self.assert_invalid("root manifest exists but 'npm'")

    def test_nonexistent_manifest_path_fails(self):
        self.config["updates"][1]["directory"] = "/not-found"
        self.assert_invalid("has no supported real manifest")

    def test_directory_traversal_fails(self):
        self.config["updates"][1]["directory"] = "/../unsafe"
        self.assert_invalid("unsafe or non-root-relative directory")

    def test_duplicate_ecosystem_directory_fails(self):
        self.config["updates"].append(copy.deepcopy(self.config["updates"][1]))
        self.assert_invalid("duplicate ecosystem/directory")

    def test_mutually_exclusive_directories_fails(self):
        self.config["updates"][1]["directories"] = ["/"]
        self.assert_invalid("specify exactly one of directory or directories")

    def test_valid_glob_directories_for_nested_go_modules(self):
        (self.root / "modules/iam").mkdir(parents=True)
        (self.root / "modules/iam/go.mod").write_text("module synthetic\n", encoding="utf-8")
        go = entry("gomod")
        go.pop("directory")
        go["directories"] = ["/modules/*"]
        self.config["updates"].append(go)
        result = self.run_policy()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_unscoped_version_group_fails(self):
        del self.config["updates"][1]["groups"]["routine"]["applies-to"]
        self.assert_invalid("must explicitly set applies-to")

    def test_broad_security_group_fails(self):
        self.config["updates"][1]["groups"]["security-all"] = {
            "applies-to": "security-updates", "patterns": ["*"],
        }
        self.assert_invalid("broad security group")

    def test_unconditional_ignore_fails(self):
        self.config["updates"][1]["ignore"] = [{"dependency-name": "vulnerable-package"}]
        self.assert_invalid("unconditional ignore")

    def test_version_only_ignore_keeps_security_update_route(self):
        self.config["updates"][1]["ignore"] = [{
            "dependency-name": "@types/node",
            "update-types": ["version-update:semver-major"],
        }]
        result = self.run_policy()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_default_target_branch_fails(self):
        self.config["updates"][0]["target-branch"] = "main"
        self.assert_invalid("redundant target-branch")

    def test_invalid_registry_reference_fails(self):
        self.config["updates"][1]["registries"] = ["nonexistent"]
        self.assert_invalid("references undefined registry")

    def test_boolean_pr_limit_fails(self):
        self.config["updates"][1]["open-pull-requests-limit"] = True
        self.assert_invalid("positive integer")

    def test_zero_pr_limit_disables_maintenance_and_fails_strict(self):
        self.config["updates"][1]["open-pull-requests-limit"] = 0
        self.assert_invalid("positive integer")

    def test_unbounded_routine_catchall_fails(self):
        del self.config["updates"][1]["groups"]["routine"]["update-types"]
        self.assert_invalid("must separate major upgrades")

    def test_mixed_major_and_patch_group_fails(self):
        self.config["updates"][1]["groups"]["routine"]["update-types"] = ["major", "patch"]
        self.assert_invalid("must separate major upgrades")

    def test_invalid_schedule_fails(self):
        self.config["updates"][1]["schedule"]["interval"] = "never"
        self.assert_invalid("unsupported schedule.interval")

    def test_nonnumeric_manifest_or_invalid_groups_fails_safely(self):
        self.config["updates"][0]["groups"] = "invalid"
        self.assert_invalid("groups must be a mapping")

    def test_approved_policy_status_and_no_claim_of_rollout(self):
        policy = (ROOT / "docs/governance/baobab-dependency-security-maintenance-policy-v1.0.md").read_text(encoding="utf-8")
        self.assertIn("**APPROVED", policy)
        self.assertIn("no claim of 20-repository conformance", policy)


if __name__ == "__main__":
    unittest.main()
