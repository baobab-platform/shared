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

classifier, classifier_text = load("reusable-foundation-classify.yml")
outputs = classifier[True]["workflow_call"]["outputs"]
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
assert {"portable", "secrets", "dependency-review", "sast", "result"} <= set(security["jobs"])
assert "security-secrets-scan.yml" in security_text
assert "--scanners vuln" in security_text
assert "--scanners misconfig" in security_text

sast, sast_text = load("reusable-foundation-sast.yml")
assert {"plan", "analyze", "status"} <= set(sast["jobs"])
assert "github.event.repository.visibility" in sast_text
assert "not_available" in sast_text
assert "SAST /" in sast_text
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
