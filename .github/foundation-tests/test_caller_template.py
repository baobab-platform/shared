"""Validate that the official Foundation caller template is executable.

The template must:
- supply every required input of foundation-repository-gates.yml
- declare permissions that cover the reusable workflow's needs
- document placeholders for security and migration inputs

Run from repository root:
  python3 .github/foundation-tests/test_caller_template.py
"""
from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = ROOT / "templates" / "caller-foundation-repository-gates.yml"
ENTRYPOINT = ROOT / ".github" / "workflows" / "foundation-repository-gates.yml"

REQUIRED_PERMISSIONS = {
    "contents": "read",
    "packages": "read",
    "actions": "read",
    "security-events": "write",
}

REQUIRED_INPUTS = {
    "foundation_ref",
}

DOCUMENTED_OPTIONAL_INPUTS = {
    "dockerfile",
    "build_context",
    "dependency_review_enabled",
    "advanced_security_enabled",
    "legacy_metadata_enabled",
}


def load_yaml(path: Path) -> dict:
    text = path.read_text()
    document = yaml.safe_load(text)
    assert isinstance(document, dict), f"{path} did not parse as a mapping"
    return document


def main() -> None:
    template = load_yaml(TEMPLATE)
    entrypoint = load_yaml(ENTRYPOINT)

    # Entrypoint must declare foundation_ref as required.
    entry_inputs = entrypoint[True]["workflow_call"]["inputs"]
    assert "foundation_ref" in entry_inputs
    assert entry_inputs["foundation_ref"].get("required") is True

    # Template top-level permissions must cover the reusable workflow.
    perms = template.get("permissions") or {}
    for key, value in REQUIRED_PERMISSIONS.items():
        assert perms.get(key) == value, (
            f"template permissions missing or wrong for {key}: expected {value!r}, got {perms.get(key)!r}"
        )

    # Single foundation job that calls the shared entrypoint.
    jobs = template.get("jobs") or {}
    assert "foundation" in jobs, "template must define a foundation job"
    job = jobs["foundation"]
    uses = job.get("uses") or ""
    assert "foundation-repository-gates.yml" in uses, (
        f"foundation job must call foundation-repository-gates.yml, got {uses!r}"
    )

    with_block = job.get("with") or {}
    for name in REQUIRED_INPUTS:
        assert name in with_block, f"template must pass required input {name!r}"
        value = with_block[name]
        assert value is not None and str(value).strip() != "", (
            f"required input {name!r} must be non-empty"
        )

    for name in DOCUMENTED_OPTIONAL_INPUTS:
        assert name in with_block, (
            f"template should pass optional input {name!r} explicitly for documentation"
        )

    # Placeholder SHA must appear so consumers replace it; do not ship a real SHA
    # that becomes stale. Prefer a clear REPLACE_ token.
    template_text = TEMPLATE.read_text()
    assert "REPLACE_WITH_FULL_SHARED_COMMIT_SHA" in template_text, (
        "template must use REPLACE_WITH_FULL_SHARED_COMMIT_SHA placeholder for the pin"
    )
    assert "advanced_security_enabled" in template_text
    assert "legacy_metadata_enabled" in template_text
    assert "security-events" in template_text

    print("Caller template validation passed")


if __name__ == "__main__":
    main()
