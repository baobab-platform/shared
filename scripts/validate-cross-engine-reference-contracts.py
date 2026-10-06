#!/usr/bin/env python3
"""Validate CrossEngineObjectReference v1 (ADR-SHARED-021 / RTD-05).

Protects the identity, authority, scope and historical-pinning boundaries that
separate engine-owned canonical objects from Control Plane CanonicalEntity and
ADR-SHARED-013 ExternalReference identities.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = ROOT / "contracts"
PACKAGE = CONTRACTS / "cross-engine-reference" / "v1"

failures: list[str] = []


def fail(message: str) -> None:
    failures.append(message)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


registry = Registry()
for path in sorted(CONTRACTS.rglob("*.json")):
    try:
        document = load_json(path)
    except json.JSONDecodeError:
        continue
    if isinstance(document, dict) and isinstance(document.get("$id"), str):
        registry = registry.with_resource(document["$id"], Resource.from_contents(document))

schema = load_json(PACKAGE / "domain.schema.json")
expected_id = "https://contracts.baobab-platform.com/cross-engine-reference/v1/domain.schema.json"
if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
    fail("domain.schema.json must use JSON Schema Draft 2020-12")
if schema.get("$id") != expected_id:
    fail(f"domain.schema.json has incorrect immutable $id: {schema.get('$id')!r}")

defs = schema.get("$defs", {})
base = defs.get("crossEngineObjectReference", {})
required = set(base.get("required", []))
for name in ("owner_engine_id", "object_type", "object_id", "reference_mode", "scope"):
    if name not in required:
        fail(f"crossEngineObjectReference must require {name}")

props = base.get("properties", {})
for forbidden in (
    "engine_instance_id",
    "system_namespace",
    "external_reference_id",
    "canonical_entity_id",
    "payload",
    "data",
    "metadata",
    "permissions",
):
    if forbidden in props:
        fail(f"crossEngineObjectReference must not contain {forbidden}")

owner_ref = props.get("owner_engine_id", {}).get("$ref")
if owner_ref != "../../control-plane/v1/domain.schema.json#/$defs/engineId":
    fail("owner_engine_id must reuse the canonical Shared engineId grammar")

if "enum" in defs.get("objectType", {}):
    fail("objectType must remain extensible; Shared must not own every engine's object taxonomy")
if not defs.get("objectType", {}).get("pattern"):
    fail("objectType must retain a stable syntax")

modes = set(defs.get("referenceMode", {}).get("enum", []))
if modes != {"CURRENT", "IDENTITY_PINNED", "VERSION_PINNED"}:
    fail(f"referenceMode set is incorrect: {sorted(modes)}")

scopes = set(defs.get("referenceScope", {}).get("enum", []))
if scopes != {"platform", "tenant"}:
    fail(f"referenceScope set is incorrect: {sorted(scopes)}")

# Examples are contract proofs, not documentation-only samples.
examples = {
    "document-version-pinned.json": "crossEngineObjectReference",
    "evidence-set-version-pinned.json": "crossEngineObjectReference",
    "capability-current-platform.json": "crossEngineObjectReference",
    "regulatory-decision-observation.json": "crossEngineReferenceObservation",
}
for filename, def_name in examples.items():
    instance = load_json(PACKAGE / "examples" / filename)
    target = {"$ref": schema["$id"] + f"#/$defs/{def_name}"}
    errors = sorted(
        Draft202012Validator(target, registry=registry, format_checker=FormatChecker()).iter_errors(instance),
        key=lambda e: list(map(str, e.absolute_path)),
    )
    for error in errors:
        fail(f"{filename}: {'/'.join(map(str, error.absolute_path)) or '<root>'}: {error.message}")

base_uri = schema["$id"] + "#/$defs/crossEngineObjectReference"
base_validator = Draft202012Validator({"$ref": base_uri}, registry=registry, format_checker=FormatChecker())

tenant_current = {
    "owner_engine_id": "baobab-regulations",
    "object_type": "REGULATORY_DECISION",
    "object_id": "regdec_01",
    "reference_mode": "CURRENT",
    "scope": "tenant",
    "tenant_id": "tn_01abcdef",
}
platform_current = {
    "owner_engine_id": "baobab-cp",
    "object_type": "CAPABILITY",
    "object_id": "documents.trade-document.manage",
    "reference_mode": "CURRENT",
    "scope": "platform",
}
version_pinned = {
    "owner_engine_id": "baobab-pulse",
    "object_type": "EVIDENCE_SET",
    "object_id": "evset_01",
    "reference_mode": "VERSION_PINNED",
    "object_version": {"kind": "VERSION", "value": "4"},
    "scope": "tenant",
    "tenant_id": "tn_01abcdef",
}
identity_pinned = {
    "owner_engine_id": "baobab-trade-docs",
    "object_type": "DOCUMENT_VERSION",
    "object_id": "tdocv_01",
    "reference_mode": "IDENTITY_PINNED",
    "scope": "tenant",
    "tenant_id": "tn_01abcdef",
}

positive = {
    "tenant CURRENT": tenant_current,
    "platform CURRENT": platform_current,
    "VERSION_PINNED": version_pinned,
    "IDENTITY_PINNED": identity_pinned,
}
for label, instance in positive.items():
    errors = list(base_validator.iter_errors(instance))
    if errors:
        fail(f"{label} should validate: {errors[0].message}")

negative = {
    "tenant scope without tenant_id": {k: v for k, v in tenant_current.items() if k != "tenant_id"},
    "platform scope with tenant_id": {**platform_current, "tenant_id": "tn_01abcdef"},
    "CURRENT with object_version": {
        **tenant_current,
        "object_version": {"kind": "VERSION", "value": "1"},
    },
    "IDENTITY_PINNED with object_version": {
        **identity_pinned,
        "object_version": {"kind": "VERSION", "value": "1"},
    },
    "VERSION_PINNED without object_version": {
        k: v for k, v in version_pinned.items() if k != "object_version"
    },
    "engine instance masquerading as owner": {
        **tenant_current,
        "owner_engine_id": "ei_01abcdef",
    },
    "copied payload": {
        **tenant_current,
        "payload": {"decision": "ALLOW"},
    },
    "external-system identity fields": {
        **tenant_current,
        "system_namespace": "medusa",
        "external_reference_id": "ref_01",
    },
}
for label, instance in negative.items():
    if not list(base_validator.iter_errors(instance)):
        fail(f"{label} must be rejected")

# Pinned helper must reject CURRENT but accept both pinned modes.
pinned_uri = schema["$id"] + "#/$defs/pinnedCrossEngineObjectReference"
pinned_validator = Draft202012Validator({"$ref": pinned_uri}, registry=registry)
if not list(pinned_validator.iter_errors(tenant_current)):
    fail("pinnedCrossEngineObjectReference must reject CURRENT")
for label, instance in (("identity", identity_pinned), ("version", version_pinned)):
    if list(pinned_validator.iter_errors(instance)):
        fail(f"pinnedCrossEngineObjectReference must accept {label}-pinned reference")

# Observation time belongs outside reference identity.
observation = defs.get("crossEngineReferenceObservation", {})
if "observed_at" not in observation.get("required", []):
    fail("crossEngineReferenceObservation must require observed_at")
if "observed_at" in props or "resolved_at" in props:
    fail("reference identity must not embed consumer observation/resolution timestamps")

if failures:
    for message in failures:
        print(f"FAIL: {message}", file=sys.stderr)
    print(f"{len(failures)} cross-engine reference contract failure(s)", file=sys.stderr)
    sys.exit(1)

print("CrossEngineObjectReference v1 passed RTD-05 authority, scope, pinning and separation invariants")
