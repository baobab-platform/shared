from __future__ import annotations

import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
WORKFLOWS = ROOT / ".github/workflows"


def load(name: str) -> tuple[dict, str]:
    text = (WORKFLOWS / name).read_text()
    document = yaml.safe_load(text)
    assert isinstance(document, dict)
    return document, text


def workflow_call_inputs(document: dict) -> dict:
    """PyYAML may parse the key `on` as boolean True."""
    on_block = document.get(True, document.get("on"))
    assert isinstance(on_block, dict)
    call = on_block["workflow_call"]
    return call["inputs"]


entry, entry_text = load("foundation-repository-gates.yml")
expected_jobs = {
    "classify",
    "baseline",
    "reproducibility",
    "runtime",
    "environment",
    "security",
    "container",
    "result",
}
assert expected_jobs <= set(entry["jobs"])
assert set(entry["jobs"]["result"]["needs"]) == expected_jobs - {"result"}
assert entry["jobs"]["classify"]["with"]["foundation_ref"]
assert entry["jobs"]["environment"]["with"]["foundation_ref"]

# Phase 4: profile input and conditional gate families
profile_input = workflow_call_inputs(entry)["profile"]
assert profile_input["default"] == "full"
assert "contract" in profile_input["description"]
assert "security-pr" in profile_input["description"]
assert entry["jobs"]["baseline"].get("if")
assert entry["jobs"]["security"].get("if")
assert entry["jobs"]["container"].get("if")
assert "skipped" in entry_text

# Phase 5: exception evidence + release policy input
assert "release_require_zero_exceptions" in workflow_call_inputs(entry)
assert "foundation-exceptions.json" in entry_text
assert "foundation-exceptions" in entry_text
assert entry["jobs"]["security"]["with"].get("package_managers")
assert entry["jobs"]["security"]["with"].get("infrastructure") is not None

# Product entrypoints
for product, profile in (
    ("foundation-product-contract.yml", "contract"),
    ("foundation-product-container.yml", "container"),
):
    product_doc, product_text = load(product)
    assert "foundation-repository-gates.yml" in product_text
    assert f"profile: {profile}" in product_text

container_product, container_product_text = load("foundation-product-container.yml")
assert "release_require_zero_exceptions" in container_product_text

security_product, security_product_text = load("foundation-product-security.yml")
assert "foundation-repository-gates.yml" in security_product_text
assert "security-deep" in security_product_text
assert "security-pr" in security_product_text

self_consumer, self_consumer_text = load("foundation.yml")
assert "profile:" in self_consumer_text
assert "security-deep" in self_consumer_text

classifier, classifier_text = load("reusable-foundation-classify.yml")
on_block = classifier.get(True, classifier.get("on"))
outputs = on_block["workflow_call"]["outputs"]
for output in (
    "python",
    "node",
    "go",
    "java",
    "rust",
    "infrastructure",
    "container_artifact",
    "container_dockerfile",
    "container_context",
    "container_runtime",
    "environment_required",
    "environment_profile",
    "package_managers",
    "exceptions",
):
    assert output in outputs
assert "check-jsonschema==0.38.0" in classifier_text
assert ".foundation/.baobab/repository.schema.json" in classifier_text

runtime, runtime_text = load("reusable-foundation-runtime.yml")
runtime_jobs = {"python", "node", "go", "java", "rust", "terraform", "exception", "result"}
assert runtime_jobs <= set(runtime["jobs"])
assert "cargo clippy" in runtime_text
assert "terraform fmt -check" in runtime_text
assert "go vet ./..." in runtime_text

security, security_text = load("reusable-foundation-security.yml")
assert {"portable", "native-deps", "secrets", "dependency-review", "sast", "result"} <= set(
    security["jobs"]
)
assert "security-secrets-scan.yml" in security_text
assert "--scanners vuln" in security_text
assert "--scanners misconfig" in security_text
assert "reusable-foundation-dependency-adapters.yml" in security_text

adapters, adapters_text = load("reusable-foundation-dependency-adapters.yml")
assert "pnpm audit" in adapters_text
assert "pip-audit" in adapters_text
assert "govulncheck" in adapters_text
assert "cargo-audit" in adapters_text
assert "foundation-dependency-adapters" in adapters_text
# Python audits the lockfile, never the runner environment; Rust is checksum-verified.
assert "pip-audit -l" not in adapters_text and "|| pip-audit" not in adapters_text
assert "--no-deps --disable-pip" in adapters_text
assert "tomllib" in adapters_text
assert "sha256sum --check --strict" in adapters_text
# govulncheck v1.1.4 panics on Go 1.27 sources (x/tools v0.29.0 SSA builder).
assert "govulncheck@v1.8.0" in adapters_text

sast, sast_text = load("reusable-foundation-sast.yml")
assert {"plan", "analyze", "status"} <= set(sast["jobs"])
assert "github.event.repository.visibility" in sast_text
assert "\"fallback\" => \"Fallback\"" in sast_text
assert "SAST /" in sast_text
assert "foundation-sast-decision" in sast_text
assert sast["jobs"]["analyze"].get("if") == "needs.plan.outputs.mode == 'codeql'"
assert "mode != 'codeql'" in str(sast["jobs"]["status"].get("if", ""))

dep_review, dep_review_text = load("reusable-foundation-dependency-review.yml")
assert "github.event.repository.visibility" in dep_review_text
assert "available" in dep_review_text

container, container_text = load("reusable-foundation-container.yml")
for requirement in ("container-policy", "container-scan", "sbom", "Healthcheck", "Config"):
    assert requirement in container_text
assert "trivy image" in container_text
# ignore_unfixed is an explicit opt-in that defaults to the strict scan and is
# plumbed through the entrypoint and the container product wrapper.
assert workflow_call_inputs(container)["ignore_unfixed"]["default"] is False
assert "--ignore-unfixed" in container_text and "IGNORE_UNFIXED" in container_text
gates, gates_text = load("foundation-repository-gates.yml")
assert workflow_call_inputs(gates)["container_ignore_unfixed"]["default"] is False
assert gates["jobs"]["container"]["with"]["ignore_unfixed"] == "${{ inputs.container_ignore_unfixed }}"
product, _ = load("foundation-product-container.yml")
assert workflow_call_inputs(product)["container_ignore_unfixed"]["default"] is False
assert product["jobs"]["foundation"]["with"]["container_ignore_unfixed"] == "${{ inputs.container_ignore_unfixed }}"

environment, environment_text = load("reusable-foundation-environment.yml")
assert ".foundation/.baobab/environment-profiles.json" in environment_text
assert "1.2.6" not in environment_text
assert "1.4.0-rc.0" not in environment_text

# Approved GitHub-hosted runner label for every workflow in this repository.
RUNNER_LABEL = "ubuntu-26.04"

for path in WORKFLOWS.glob("*.y*ml"):
    text = path.read_text()
    for label in re.findall(r"^\s*runs-on:\s*(\S+)", text, re.MULTILINE):
        assert label == RUNNER_LABEL, f"{path} uses runner {label}; expected {RUNNER_LABEL}"
    assert "contains(fromJSON(inputs.exceptions)" not in text, f"unsafe exception lookup in {path}"
    for reference in re.findall(r"^\s*uses:\s*([^\s#]+)", text, re.MULTILINE):
        if reference.startswith("./"):
            continue
        assert re.search(r"@[0-9a-f]{40}$", reference), f"unpinned reference {reference} in {path}"

# Security scope (M2): PR, branch and deep scans differ and emit distinct results.
security_inputs = workflow_call_inputs(security)
assert security_inputs["scope"]["default"] == "branch"
scope_expression = entry["jobs"]["security"]["with"]["scope"]
assert "security-deep" in scope_expression and "'deep'" in scope_expression
assert "pull_request" in scope_expression and "'pr'" in scope_expression and "'branch'" in scope_expression
secrets_opts = security["jobs"]["secrets"]["with"]["log-opts"]
assert "pull_request.base.sha" in secrets_opts and "'--all'" in secrets_opts and "'HEAD'" in secrets_opts
assert "inputs.scope == 'pr'" in security["jobs"]["dependency-review"]["with"]["enabled"]
assert all(name in security["jobs"]["result"]["name"] for name in ("'PR'", "'Deep'", "'Branch'"))
secrets_scan, secrets_scan_text = load("security-secrets-scan.yml")
assert workflow_call_inputs(secrets_scan)["log-opts"]["default"] == "HEAD"
assert '[0-9a-f]{40}' in secrets_scan_text and "LOG_OPTS" in secrets_scan_text

# SAST provider (H2): the contract decides, the classifier resolves, and the
# security family consumes the decision instead of a caller boolean.
assert {"sast_provider", "ghas_approved"} <= set(outputs)
assert "sast_policy.rb" in classifier_text and "github.event.repository.visibility" in classifier_text
assert entry["jobs"]["classify"]["with"]["advanced_security_enabled"] == "${{ inputs.advanced_security_enabled }}"
assert entry["jobs"]["security"]["with"]["sast_provider"] == "${{ needs.classify.outputs.sast_provider }}"
assert "advanced_security_enabled" not in security_inputs
assert workflow_call_inputs(sast)["provider"]["default"] == "fallback"
assert "enabled" not in workflow_call_inputs(sast)
assert "ghas_approved" in workflow_call_inputs(dep_review)
assert "Deprecated" in workflow_call_inputs(entry)["advanced_security_enabled"]["description"]

# The .nabhold metadata bridge is gone from every Foundation workflow.
for path in WORKFLOWS.glob("*foundation*.y*ml"):
    text = path.read_text()
    assert "legacy_metadata_enabled" not in text, f"{path.name} still references legacy_metadata_enabled"
    assert ".nabhold/" not in text, f"{path.name} still reads .nabhold metadata"

# Drift guard (Phase 7): scheduled, read-only, driven by the shipped config.
drift, drift_text = load("foundation-org-conformance.yml")
drift_on = drift.get(True, drift.get("on"))
assert "schedule" in drift_on and "workflow_dispatch" in drift_on
assert "pull_request" not in drift_on, "org drift must not block unrelated pull requests"
assert drift["permissions"] == {"contents": "read"}
assert "scripts/foundation/org_conformance.py" in drift_text and ".baobab/org-conformance.yaml" in drift_text
assert "ORG_CONFORMANCE_TOKEN" in drift_text and "org-conformance-report" in drift_text

# Reusable-workflow nesting. GitHub allows at most 10 levels of connected
# workflows (the consumer's top-level caller counts as one) and at most 50
# workflows in one run. Each product wrapper adds a level on top of the
# orchestrator, so measure the deepest chain a consumer can start.
MAX_LEVELS = 10
MAX_WORKFLOWS = 50


def local_calls(name: str) -> list[str]:
    document, _ = load(name)
    calls = []
    for job in document.get("jobs", {}).values():
        uses = job.get("uses", "")
        if uses.startswith("./.github/workflows/"):
            calls.append(uses.removeprefix("./.github/workflows/"))
    return calls


def depth(name: str, seen: tuple[str, ...] = ()) -> int:
    assert name not in seen, f"reusable workflow cycle: {' -> '.join(seen + (name,))}"
    return 1 + max((depth(child, seen + (name,)) for child in local_calls(name)), default=0)


def workflow_count(name: str) -> int:
    return 1 + sum(workflow_count(child) for child in local_calls(name))


for entrypoint in (
    "foundation-repository-gates.yml",
    "foundation-product-contract.yml",
    "foundation-product-security.yml",
    "foundation-product-container.yml",
):
    levels = 1 + depth(entrypoint)  # + the consumer's own caller workflow
    assert levels <= MAX_LEVELS, f"{entrypoint} reaches {levels} workflow levels; GitHub allows {MAX_LEVELS}"
    total = 1 + workflow_count(entrypoint)
    assert total <= MAX_WORKFLOWS, f"{entrypoint} starts {total} workflows; GitHub allows {MAX_WORKFLOWS}"

# Every SHA-pinned action names the release it corresponds to, so the pin
# stays auditable (for example "# v7.0.1" or "# v7.0.0+6 (main, 2026-09-09)").
for path in WORKFLOWS.glob("*.y*ml"):
    for line in path.read_text().splitlines():
        match = re.match(r"^\s*(?:- )?uses:\s*([^\s#]+@[0-9a-f]{40})(.*)$", line)
        if match and not match.group(1).startswith("./"):
            assert re.search(r"#\s*v\d", match.group(2)), f"{path.name}: pin without a version comment: {match.group(1)}"

print("Foundation workflow wiring fixtures passed")
