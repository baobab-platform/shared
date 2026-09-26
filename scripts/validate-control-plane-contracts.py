#!/usr/bin/env python3
"""Validate the Control Plane administrative read models (control-plane/v1).

Performs real JSON Schema Draft 2020-12 validation, with every cross-schema
$ref resolved against this repository, for the administrative definition
libraries that ADR-BCP-022 requires before an operation counts as complete:

  1. each schema is a valid Draft 2020-12 schema whose $id matches its file
     name and which defines exactly the $defs it is responsible for;
  2. every example validates against its definition;
  3. negative fixtures prove the load-bearing rules reject bad data;
  4. every openapi.yaml reference to these schemas names a real definition.

Setup (same dependencies as the Foundation fixture suite):
  python3 -m pip install -r .github/foundation-tests/requirements.txt
  python3 scripts/validate-control-plane-contracts.py
"""

from __future__ import annotations

import copy
import json
import re
import sys
from datetime import datetime
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = ROOT / "contracts"
CP = CONTRACTS / "control-plane" / "v1"
BASE_URI = "https://contracts.baobab-platform.com/control-plane/v1/"

RESPONSIBILITIES = {
    "canonical-entity.schema.json": {
        "canonicalKey", "entityType", "canonicalEntityStatus", "canonicalEntityClassification",
        "canonicalEntityAuthority", "CanonicalEntityCreateRequest", "CanonicalEntity",
    },
    "capability-explanation.schema.json": {
        "opaqueId", "CapabilityExplanationRequest", "CapabilityExplanation",
    },
}

FAILURES: list[str] = []


def fail(message: str) -> None:
    FAILURES.append(message)


FORMATS = FormatChecker()


@FORMATS.checks("date-time")
def _is_datetime(value: object) -> bool:
    if not isinstance(value, str):
        return True
    return re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})", value) is not None and \
        datetime.fromisoformat(value.replace("Z", "+00:00")) is not None


def build_registry() -> Registry:
    registry = Registry()
    for path in sorted(CONTRACTS.rglob("*.json")):
        try:
            document = json.loads(path.read_text())
        except json.JSONDecodeError:
            continue
        if isinstance(document, dict) and isinstance(document.get("$id"), str):
            registry = registry.with_resource(document["$id"], Resource.from_contents(document))
    return registry


REGISTRY = build_registry()


def validator_for(schema_file: str, definition: str) -> Draft202012Validator:
    return Draft202012Validator(
        {"$ref": f"{BASE_URI}{schema_file}#/$defs/{definition}"},
        registry=REGISTRY,
        format_checker=FORMATS,
    )


def accepts(schema_file: str, definition: str, instance: object, label: str) -> None:
    errors = sorted(validator_for(schema_file, definition).iter_errors(instance), key=str)
    for error in errors:
        fail(f"{label}: {definition} rejected a valid instance: {error.message} at {list(error.absolute_path)}")


def rejects(schema_file: str, definition: str, instance: object, label: str) -> None:
    if validator_for(schema_file, definition).is_valid(instance):
        fail(f"negative fixture accepted: {label}")


def check_schemas() -> None:
    for name, expected in RESPONSIBILITIES.items():
        document = json.loads((CP / name).read_text())
        Draft202012Validator.check_schema(document)
        if document.get("$id") != BASE_URI + name:
            fail(f"{name}: $id must be {BASE_URI + name}")
        defined = set(document.get("$defs", {}))
        if defined != expected:
            fail(f"{name}: $defs {sorted(defined)} differ from {sorted(expected)}")


def check_canonical_entity() -> None:
    schema = "canonical-entity.schema.json"
    example = json.loads((CP / "examples" / "canonical-entity.json").read_text())
    accepts(schema, "CanonicalEntityCreateRequest", example["create_request"], "canonical-entity create_request")
    accepts(schema, "CanonicalEntity", example["created"], "canonical-entity created")
    accepts(schema, "CanonicalEntity", example["admitted_organisation"], "canonical-entity admitted_organisation")
    if example["created"]["status"] != "DRAFT" or example["created"]["version"] != 1:
        fail("canonical-entity created example must start DRAFT at version 1")

    request = example["create_request"]
    for field, value in (("id", "0199a1b2-c3d4-7e8f-9a0b-1c2d3e4f5a6b"), ("status", "ACTIVE"), ("version", 1),
                         ("created_at", "2026-09-26T09:00:00Z"), ("metadata", {})):
        rejects(schema, "CanonicalEntityCreateRequest", {**request, field: value},
                f"create request naming server-owned or arbitrary field {field}")
    for field in ("canonical_key", "entity_type", "display_name", "authority", "classification"):
        bad = copy.deepcopy(request)
        del bad[field]
        rejects(schema, "CanonicalEntityCreateRequest", bad, f"create request without {field}")
    rejects(schema, "CanonicalEntityCreateRequest", {**request, "canonical_key": "NoNamespace"}, "canonical key without namespace")
    rejects(schema, "CanonicalEntityCreateRequest", {**request, "entity_type": "supplier"}, "lower-case entity type")
    rejects(schema, "CanonicalEntityCreateRequest", {**request, "classification": "SECRET"}, "unknown classification")
    rejects(schema, "CanonicalEntityCreateRequest", {**request, "owner_tenant_id": "tenant-123"}, "non-canonical tenant id")

    entity = example["created"]
    rejects(schema, "CanonicalEntity", {**entity, "status": "active"}, "lower-case status")
    rejects(schema, "CanonicalEntity", {**entity, "version": 0}, "version 0")
    rejects(schema, "CanonicalEntity", {**entity, "metadata": {"k": "v"}}, "entity with arbitrary metadata")
    bad = copy.deepcopy(entity)
    del bad["version"]
    rejects(schema, "CanonicalEntity", bad, "entity without version")


def check_capability_explanation() -> None:
    schema = "capability-explanation.schema.json"
    example = json.loads((CP / "examples" / "capability-explanation.json").read_text())
    accepts(schema, "CapabilityExplanationRequest", example["request"], "capability-explanation request")
    accepts(schema, "CapabilityExplanation", example["routed"], "capability-explanation routed")
    accepts(schema, "CapabilityExplanation", example["failed"], "capability-explanation failed")

    request = example["request"]
    rejects(schema, "CapabilityExplanationRequest", {**request, "capability_key": "erp.receivables"}, "two-part capability key")
    rejects(schema, "CapabilityExplanationRequest", {**request, "tenant_id": "tn_x"}, "inline tenant in explain request")
    bad = copy.deepcopy(request)
    del bad["context_id"]
    rejects(schema, "CapabilityExplanationRequest", bad, "explain request without context_id")

    routed, failed = example["routed"], example["failed"]
    bad = copy.deepcopy(routed)
    del bad["topology"]
    rejects(schema, "CapabilityExplanation", bad, "ROUTED explanation without topology")
    rejects(schema, "CapabilityExplanation", {**failed, "policy": routed["policy"]}, "FAILED explanation with policy")
    rejects(schema, "CapabilityExplanation", {**failed, "outcome": "DENIED"}, "unknown outcome")
    rejects(schema, "CapabilityExplanation", {**failed, "grant_id": ""}, "empty stage identifier")


def check_openapi_references() -> None:
    openapi = yaml.safe_load((CP / "openapi.yaml").read_text())
    pattern = re.compile(r"^\./(" + "|".join(re.escape(n) for n in RESPONSIBILITIES) + r")#/\$defs/(\w+)$")
    seen: set[tuple[str, str]] = set()

    def walk(node: object) -> None:
        if isinstance(node, dict):
            ref = node.get("$ref")
            if isinstance(ref, str):
                match = pattern.match(ref)
                if match:
                    seen.add((match.group(1), match.group(2)))
                    if match.group(2) not in RESPONSIBILITIES[match.group(1)]:
                        fail(f"openapi.yaml references undefined {ref}")
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)

    walk(openapi)
    for required in (("canonical-entity.schema.json", "CanonicalEntity"),
                     ("canonical-entity.schema.json", "CanonicalEntityCreateRequest"),
                     ("capability-explanation.schema.json", "CapabilityExplanation"),
                     ("capability-explanation.schema.json", "CapabilityExplanationRequest")):
        if required not in seen:
            fail(f"openapi.yaml does not use {required[0]}#/$defs/{required[1]}")


def main() -> int:
    check_schemas()
    check_canonical_entity()
    check_capability_explanation()
    check_openapi_references()
    if FAILURES:
        for message in FAILURES:
            print(f"FAIL: {message}", file=sys.stderr)
        return 1
    print("control-plane/v1 administrative contracts: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
