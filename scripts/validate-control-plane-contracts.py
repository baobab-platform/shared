#!/usr/bin/env python3
"""Validate the Control Plane administrative read models (control-plane/v1).

Performs real JSON Schema Draft 2020-12 validation, with every cross-schema
$ref resolved against this repository, for the administrative definition
libraries that ADR-BCP-022 requires before an operation counts as complete:

  1. each schema is a valid Draft 2020-12 schema whose $id matches its file
     name and which defines exactly the $defs it is responsible for;
  2. every example validates against its definition;
  3. negative fixtures prove the load-bearing rules reject bad data;
  4. every openapi.yaml reference to these schemas names a real definition;
  5. the topology identifiers have one grammar everywhere and
     external-systems.yaml registers well-formed systems (ADR-SHARED-012).

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
    "canonical-mapping.schema.json": {
        "mapping", "mappingScope", "externalReference", "resolutionRequest", "resolutionResponse",
        "externalReferenceCreateRequest", "externalReferenceList", "mappingCreateRequest", "mappingUpdateRequest",
        "mappingRetireRequest", "externalReferenceResolutionRequest", "externalReferenceResolutionResponse",
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


def check_mapping_administration() -> None:
    schema = "canonical-mapping.schema.json"
    example = json.loads((CP / "examples" / "mapping-administration.json").read_text())
    for key, definition in (("external_reference_create_request", "externalReferenceCreateRequest"),
                            ("external_reference", "externalReference"),
                            ("mapping_create_request", "mappingCreateRequest"),
                            ("mapping", "mapping"),
                            ("migrated_canonical_mapping", "mapping"),
                            ("resolution_request", "externalReferenceResolutionRequest"),
                            ("resolution_response", "externalReferenceResolutionResponse")):
        accepts(schema, definition, example[key], f"mapping-administration {key}")

    registry = yaml.safe_load((CP / "external-systems.yaml").read_text())
    registered = {(system["system_namespace"], engine) for system in registry["systems"] for engine in system["engine_ids"]}
    for key in ("external_reference_create_request", "external_reference", "resolution_request"):
        pair = (example[key]["system_namespace"], example[key]["engine_id"])
        if pair not in registered:
            fail(f"mapping-administration {key} names unregistered system {pair}")

    create = example["external_reference_create_request"]
    for field, value in (("external_reference_id", "ref_0199a1b2c3d47e8f"), ("status", "active"),
                         ("source_authority", "engine"), ("created_at", "2026-09-26T09:00:00Z"), ("metadata", {})):
        rejects(schema, "externalReferenceCreateRequest", {**create, field: value}, f"external reference create naming {field}")
    rejects(schema, "externalReferenceCreateRequest", {**create, "engine_id": "baobab_trade"}, "snake_case engine id")

    proposal = example["mapping_create_request"]
    for field, value in (("mapping_id", "map_0199a1b2c3d47e8f"), ("status", "ACTIVE"), ("revision", 1),
                         ("created_by", "someone"), ("approved_by", "someone"), ("approved_at", "2026-09-26T09:00:00Z")):
        rejects(schema, "mappingCreateRequest", {**proposal, field: value}, f"mapping proposal naming {field}")
    rejects(schema, "mappingCreateRequest", {**proposal, "target_canonical_entity_id": "0199a1b2-c3d4-7e8f-9a0b-1c2d3e4f5a6d"},
            "mapping proposal with both targets")
    neither = copy.deepcopy(proposal)
    del neither["external_reference_id"]
    rejects(schema, "mappingCreateRequest", neither, "mapping proposal with no target")

    mapping = example["migrated_canonical_mapping"]
    without_subject = copy.deepcopy(mapping)
    del without_subject["canonical_entity_id"]
    rejects(schema, "mapping", without_subject, "mapping without its canonical entity")
    rejects(schema, "mapping", {**mapping, "external_reference_id": "ref_0199a1b2c3d47e8f"}, "mapping with both targets")
    rejects(schema, "mapping", {**mapping, "authority": "baobab"}, "mapping authority outside the enum")

    rejects(schema, "mappingUpdateRequest", {}, "empty mapping change")
    rejects(schema, "mappingUpdateRequest", {"tenant_id": proposal["tenant_id"]}, "mapping change moving its tenant")
    rejects(schema, "mappingUpdateRequest", {"external_reference_id": "ref_0199a1b2c3d47e8f"}, "mapping change moving its target")
    rejects(schema, "mappingRetireRequest", {"reason": "superseded", "retired_by": "someone"}, "retirement naming its actor")
    rejects(schema, "mappingRetireRequest", {}, "retirement without a reason")
    rejects(schema, "externalReferenceList", {"items": [example["external_reference"], example["external_reference"]]},
            "two references for one native identity")


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


def check_topology_identifiers() -> None:
    domain = json.loads((CP / "domain.schema.json").read_text())["$defs"]
    expected = {"engineId": "^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$", "engineInstanceId": "^ei_[a-z0-9]+$"}
    for name, pattern in expected.items():
        if domain.get(name, {}).get("pattern") != pattern:
            fail(f"domain.schema.json#/$defs/{name} must have pattern {pattern}")

    def ref_of(node: dict) -> str:
        if "$ref" in node:
            return node["$ref"]
        return next((option["$ref"] for option in node.get("anyOf", []) if "$ref" in option), "")

    mapping = json.loads((CP / "canonical-mapping.schema.json").read_text())["$defs"]
    for definition in ("externalReference", "mappingScope"):
        properties = mapping[definition]["properties"]
        for field, target in (("engine_id", "engineId"), ("engine_instance_id", "engineInstanceId")):
            if not ref_of(properties[field]).endswith(f"domain.schema.json#/$defs/{target}"):
                fail(f"canonical-mapping {definition}.{field} must reference domain.schema.json#/$defs/{target}")
    capability = CONTRACTS / "capability" / "v1"
    binding = json.loads((capability / "binding.schema.json").read_text())["$defs"]
    resolution = json.loads((capability / "resolution.schema.json").read_text())["$defs"]
    for label, node in (("capability/v1 binding", next(iter(binding.values()))["properties"]["engine_instance_id"]),
                        ("capability/v1 resolution invocationDescriptor", resolution["invocationDescriptor"]["properties"]["engine_instance_id"])):
        if not ref_of(node).endswith("control-plane/v1/domain.schema.json#/$defs/engineInstanceId"):
            fail(f"{label}.engine_instance_id must reference control-plane/v1 engineInstanceId")
    # These packages use another $id base, so they repeat the grammar.
    for path in ("authorization/v1/context.schema.json", "identity/v1/external-reference.schema.json"):
        node = json.loads((CONTRACTS / path).read_text())["properties"]["engine_instance_id"]
        if node.get("pattern") != expected["engineInstanceId"]:
            fail(f"{path} engine_instance_id must repeat the engineInstanceId pattern")

    reference = {
        "external_reference_id": "ref_0199a1b2c3d47e8f",
        "system_namespace": "medusa",
        "engine_id": "baobab-trade",
        "engine_instance_id": "ei_0199a1b2c3d47e8f",
        "native_entity_type": "customer",
        "native_id": "cus_01k4",
    }
    accepts("canonical-mapping.schema.json", "externalReference", reference, "external reference with canonical engine identifiers")
    rejects("canonical-mapping.schema.json", "externalReference", {**reference, "engine_instance_id": "0199a1b2-c3d4-7e8f-9a0b-1c2d3e4f5a6b"}, "UUID engine instance id")
    rejects("canonical-mapping.schema.json", "externalReference", {**reference, "engine_instance_id": "trade_eu_1"}, "slug engine instance id")
    rejects("canonical-mapping.schema.json", "externalReference", {**reference, "engine_id": "baobab_trade"}, "snake_case engine id")


def check_external_systems() -> None:
    registry = yaml.safe_load((CP / "external-systems.yaml").read_text())
    if registry.get("schema") != "baobab-external-system-registry" or registry.get("version") != "1.0":
        fail("external-systems.yaml must declare schema baobab-external-system-registry, version 1.0")
    mapping = json.loads((CP / "canonical-mapping.schema.json").read_text())["$defs"]["externalReference"]["properties"]
    namespace_pattern = re.compile(mapping["system_namespace"]["pattern"])
    engine_pattern = re.compile(json.loads((CP / "domain.schema.json").read_text())["$defs"]["engineId"]["pattern"])
    systems = registry.get("systems") or []
    if not systems:
        fail("external-systems.yaml registers no systems")
    seen: set[str] = set()
    for system in systems:
        namespace = system.get("system_namespace", "")
        if not namespace_pattern.fullmatch(namespace):
            fail(f"external-systems.yaml: {namespace!r} does not match externalReference system_namespace")
        if namespace in seen:
            fail(f"external-systems.yaml registers {namespace} twice")
        seen.add(namespace)
        engines = system.get("engine_ids") or []
        if not engines or len(set(engines)) != len(engines):
            fail(f"external-systems.yaml: {namespace} needs distinct engine_ids")
        for engine in engines:
            if not engine_pattern.fullmatch(engine):
                fail(f"external-systems.yaml: {namespace} engine {engine!r} does not match engineId")
        if not str(system.get("description", "")).strip():
            fail(f"external-systems.yaml: {namespace} needs a description")


def main() -> int:
    check_schemas()
    check_canonical_entity()
    check_capability_explanation()
    check_mapping_administration()
    check_openapi_references()
    check_topology_identifiers()
    check_external_systems()
    if FAILURES:
        for message in FAILURES:
            print(f"FAIL: {message}", file=sys.stderr)
        return 1
    print("control-plane/v1 administrative contracts: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
