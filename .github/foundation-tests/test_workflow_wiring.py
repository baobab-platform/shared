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
assert "not_available" in sast_text
assert "SAST /" in sast_text
assert "foundation-sast-decision" in sast_text
assert sast["jobs"]["analyze"].get("if") == "needs.plan.outputs.mode == 'codeql'"
assert "mode != 'codeql'" in str(sast["jobs"]["status"].get("if", ""))

dep_review, dep_review_text = load("reusable-foundation-dependency-review.yml")
assert "github.event.repository.visibility" in dep_review_text
assert "advanced_security_enabled" in dep_review_text
assert "available" in dep_review_text

container, container_text = load("reusable-foundation-container.yml")
for requirement in ("container-policy", "container-scan", "sbom", "Healthcheck", "Config"):
    assert requirement in container_text
assert "trivy image" in container_text

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

print("Foundation workflow wiring fixtures passed")
