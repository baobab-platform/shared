from __future__ import annotations

import copy
import json
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[2]
SCHEMA = json.loads((ROOT / ".baobab/repository.schema.json").read_text())
VALIDATOR = Draft202012Validator(SCHEMA, format_checker=FormatChecker())

BASE = {
    "schema_version": 1,
    "repository": {"lifecycle": "active"},
    "capabilities": ["node", "container"],
    "environment": {"baobab_dev": {"required": True, "profile": "frontend"}},
    "package_managers": {"node": "pnpm"},
    "artifacts": {
        "container": {
            "enabled": True,
            "dockerfile": "Dockerfile",
            "context": ".",
            "runtime": True,
        }
    },
}


def errors(document: dict) -> list[str]:
    return [error.message for error in VALIDATOR.iter_errors(document)]


def expect_valid(name: str, document: dict) -> None:
    found = errors(document)
    assert not found, f"{name} should be valid: {found}"


def expect_invalid(name: str, document: dict) -> None:
    found = errors(document)
    assert found, f"{name} should be invalid"


expect_valid("base contract", BASE)

for capability in (
    "python",
    "node",
    "go",
    "java",
    "rust",
    "container",
    "infrastructure",
    "documentation",
    "contracts",
    "github-actions",
    "digital-estate",
    "engine",
    "library",
    "development-environment",
):
    contract = copy.deepcopy(BASE)
    contract["capabilities"] = [capability]
    contract["package_managers"] = {}
    contract["artifacts"]["container"] = False
    expect_valid(f"{capability} capability", contract)

for runtime, manager in {
    "node": "pnpm",
    "python": "uv",
    "java": "maven",
    "rust": "cargo",
}.items():
    contract = copy.deepcopy(BASE)
    contract["capabilities"] = [runtime]
    contract["package_managers"] = {runtime: manager}
    contract["artifacts"]["container"] = False
    expect_valid(f"{runtime}/{manager}", contract)

invalid_cases: dict[str, dict] = {}

case = copy.deepcopy(BASE)
case["unexpected"] = True
invalid_cases["unknown top-level field"] = case

case = copy.deepcopy(BASE)
case["capabilities"].append("node")
invalid_cases["duplicate capability"] = case

case = copy.deepcopy(BASE)
case["capabilities"] = ["cobol"]
invalid_cases["unknown capability"] = case

case = copy.deepcopy(BASE)
del case["environment"]["baobab_dev"]["profile"]
invalid_cases["required environment without profile"] = case

case = copy.deepcopy(BASE)
case["package_managers"]["node"] = "bower"
invalid_cases["unknown package manager"] = case

case = copy.deepcopy(BASE)
del case["artifacts"]["container"]["runtime"]
invalid_cases["container without runtime semantics"] = case

case = copy.deepcopy(BASE)
case["exceptions"] = {
    "runtime": {
        "reason": "short",
        "expires": "not-a-date",
        "approved_by": "nobody",
    }
}
invalid_cases["malformed exception"] = case

case = copy.deepcopy(BASE)
case["exceptions"] = {
    "unknown-control": {
        "reason": "A sufficiently long reason",
        "expires": "2099-12-31",
        "approved_by": "@platform",
    }
}
invalid_cases["unknown exception control"] = case

case = copy.deepcopy(BASE)
case["security"] = {"sast_provider": "semgrep"}
invalid_cases["unknown SAST provider"] = case

case = copy.deepcopy(BASE)
case["security"] = {"sast_provider": "codeql", "ghas": {"approved_by": "@platform"}}
invalid_cases["incomplete GHAS approval"] = case

case = copy.deepcopy(BASE)
case["security"] = {"provider": "codeql"}
invalid_cases["unknown security field"] = case

for name, document in invalid_cases.items():
    expect_invalid(name, document)

for provider in ("codeql", "fallback", "disabled"):
    declared = copy.deepcopy(BASE)
    declared["security"] = {"sast_provider": provider}
    expect_valid(f"security.sast_provider {provider}", declared)
approved = copy.deepcopy(BASE)
approved["security"] = {
    "sast_provider": "codeql",
    "ghas": {"approved_by": "@platform", "reason": "GHAS is licensed for this repository", "expires": "2099-12-31"},
}
expect_valid("codeql with GHAS approval", approved)

exception = copy.deepcopy(BASE)
exception["exceptions"] = {
    control: {
        "reason": "Temporary reviewed production waiver",
        "expires": "2099-12-31",
        "approved_by": "@platform",
    }
    for control in (
        "baseline",
        "reproducibility",
        "runtime",
        "environment",
        "dependency-review",
        "sast",
        "dependency-audit",
        "secret-scan",
        "container-policy",
        "container-scan",
        "sbom",
    )
}
expect_valid("all controlled exceptions", exception)

catalogue = json.loads((ROOT / ".baobab/environment-profiles.json").read_text())
assert catalogue["schema_version"] == 1
assert catalogue["provider"] == "baobab-dev"
assert set(catalogue["profiles"]) == {"full", "frontend", "frontend-e2e", "infra"}
for name, profile in catalogue["profiles"].items():
    assert profile["minimum_version"], f"{name} has no version floor"
    assert "tag_suffix" in profile, f"{name} has no tag suffix declaration"

own = yaml.safe_load((ROOT / ".baobab/environment.yaml").read_text())["environment"]
own_policy = catalogue["profiles"][own["profile"]]
own_version = own["minimum_version"].removesuffix(own_policy["tag_suffix"])
floor = tuple(int(part) for part in own_policy["minimum_version"].split("."))
assert tuple(int(part) for part in own_version.split(".")) >= floor, (
    f"shared declares baobab-dev {own_version}, below the {own['profile']} floor {own_policy['minimum_version']}"
)

loaded = yaml.safe_load((ROOT / ".baobab/repository.yaml").read_text())
expect_valid("shared repository contract", loaded)

print("Repository contract and environment catalogue fixtures passed")
