#!/usr/bin/env python3
"""EA-09 / P-CAP-08 certification and Pulse activation invariants."""

from __future__ import annotations

import json
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[2]
CONTRACTS = ROOT / "contracts"
BASE = "https://contracts.baobab-platform.com/"


def registry() -> Registry:
    result = Registry()
    for path in CONTRACTS.rglob("*.json"):
        doc = json.loads(path.read_text())
        if isinstance(doc, dict) and isinstance(doc.get("$id"), str):
            result = result.with_resource(doc["$id"], Resource.from_contents(doc))
    return result


cert_schema = json.loads(
    (CONTRACTS / "capability/v1/certification.schema.json").read_text()
)
validator = Draft202012Validator(
    {
        "$ref": (
            BASE
            + "capability/v1/certification.schema.json"
            + "#/$defs/ProviderCapabilityCertificationRecordRequest"
        )
    },
    registry=registry(),
    format_checker=FormatChecker(),
)

valid_request = {
    "provider_id": "provider_0199a1b2c3d47e8f9a0b1c2d3e4f5a6b",
    "capability_key": "intelligence.evidence.search",
    "contract_version": 1,
    "release_id": "release_0199a1b2c3d47e8f9a0b1c2d3e4f5a6b",
    "qualification_profile": "ea-09/pulse-intelligence-v1",
    "evidence": [
        {
            "type": "CONTRACT_TEST",
            "uri": "https://github.com/baobab-platform/baobab-pulse/actions/runs/1",
            "digest": "sha256:" + "a" * 64,
        }
    ],
    "reason": "Qualification suite passed.",
}
assert not list(validator.iter_errors(valid_request))

policy = yaml.safe_load((CONTRACTS / "topology/v1/release-policy.yaml").read_text())
assert policy["approval"]["certification_required"] == {
    "local": False,
    "development": False,
    "staging": False,
    "production": True,
}

scopes = yaml.safe_load(
    (CONTRACTS / "authorization/v1/scope-registry.yaml").read_text()
)["scopes"]
by_scope = {item["name"]: item for item in scopes}
assert by_scope["provider:certify"]["audience"] == ["baobab-control-plane"]
assert by_scope["provider:certify"]["allowed_actors"] == ["human"]
assert by_scope["provider:certify"]["privileged"] is True

index = yaml.safe_load(
    (CONTRACTS / "capability/v1/registration-bundles.yaml").read_text()
)
pulse = [
    item
    for item in index["bundles"]
    if item["provider_key"] == "baobab-pulse.core"
]
assert pulse == [
    {
        "path": "intelligence/v1/pulse-registration.json",
        "engine_id": "baobab-pulse",
        "provider_key": "baobab-pulse.core",
    }
]

bundle = json.loads(
    (CONTRACTS / "intelligence/v1/pulse-registration.json").read_text()
)
assert bundle["repository"] == "baobab-pulse"
assert bundle["provider"]["provider_key"] == "baobab-pulse.core"
assert bundle["provider"]["lifecycle"] == "DRAFT"
assert bundle["provider"]["simulated"] is False
assert bundle["provider"]["production_permitted"] is True
assert bundle["provider"]["invocation"] == {
    "service_reference": "service://baobab-pulse/capabilities",
    "protocol": "http",
}
assert {
    item["capability_key"] for item in bundle["support"]
} == {
    "intelligence.evidence.search",
    "intelligence.research-mission.manage",
}
assert {
    item["lifecycle"] for item in bundle["capabilities"]
} == {"ACTIVE"}
assert {
    item["maturity"] for item in bundle["capabilities"]
} == {"EXPERIMENTAL"}

print("EA-09 / P-CAP-08 certification and Pulse activation invariants passed")
