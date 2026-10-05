#!/usr/bin/env python3
"""Validate RTD-06 Regulations ↔ Trade Docs exchange contracts."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = ROOT / "contracts"
PACKAGE = CONTRACTS / "regulatory-document-exchange" / "v1"
EVENT_REGISTRY = CONTRACTS / "events" / "v1" / "event-registry.yaml"

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

domain = load_json(PACKAGE / "domain.schema.json")
events = load_json(PACKAGE / "events.schema.json")
surfaces = yaml.safe_load((PACKAGE / "event-surfaces.yaml").read_text())

expected_ids = {
    "domain.schema.json": "https://contracts.baobab-platform.com/regulatory-document-exchange/v1/domain.schema.json",
    "events.schema.json": "https://contracts.baobab-platform.com/regulatory-document-exchange/v1/events.schema.json",
}
for name, expected in expected_ids.items():
    doc = domain if name == "domain.schema.json" else events
    if doc.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        fail(f"{name} must use JSON Schema Draft 2020-12")
    if doc.get("$id") != expected:
        fail(f"{name} has incorrect immutable $id: {doc.get('$id')!r}")

defs = domain.get("$defs", {})

# RTD-05 must be the identity primitive, not ad-hoc owner/id fields.
specialised = {
    "regulatoryDecisionReference": ("baobab-regulations", "REGULATORY_DECISION"),
    "documentRequirementReference": ("baobab-regulations", "DOCUMENT_REQUIREMENT"),
    "permitRequirementReference": ("baobab-regulations", "PERMIT_REQUIREMENT"),
    "evidenceRequirementReference": ("baobab-regulations", "EVIDENCE_REQUIREMENT"),
    "regulatoryEvidenceAssessmentReference": ("baobab-regulations", "REGULATORY_EVIDENCE_ASSESSMENT"),
    "documentVersionReference": ("baobab-trade-docs", "DOCUMENT_VERSION"),
    "contentArtifactReference": ("baobab-trade-docs", "CONTENT_ARTIFACT"),
}
for def_name, (owner, obj_type) in specialised.items():
    item = defs.get(def_name, {})
    encoded = json.dumps(item, sort_keys=True)
    if "cross-engine-reference/v1/domain.schema.json" not in encoded:
        fail(f"{def_name} must compose RTD-05 CrossEngineObjectReference")
    if owner not in encoded or obj_type not in encoded:
        fail(f"{def_name} must constrain owner={owner} and object_type={obj_type}")

# DocumentVersion is immutable identity-pinned evidence.
document_version_ref = json.dumps(defs.get("documentVersionReference", {}), sort_keys=True)
if "IDENTITY_PINNED" not in document_version_ref:
    fail("documentVersionReference must be IDENTITY_PINNED")

# Command caller must not choose legal/knowledge time or satisfaction.
assessment_request_props = defs.get("documentEvidenceAssessmentRequest", {}).get("properties", {})
for forbidden in ("legal_time", "knowledge_time", "outcome", "satisfaction", "regulatory_result"):
    if forbidden in assessment_request_props:
        fail(f"assessment request must not allow caller-supplied {forbidden}")

# Trade Docs fact projection must not contain regulatory conclusions.
fact_props = defs.get("documentEvidenceFactBundle", {}).get("properties", {})
for forbidden in ("requirement_satisfied", "satisfaction", "regulatory_outcome", "regulatory_decision"):
    if forbidden in fact_props:
        fail(f"Trade Docs fact bundle must not contain {forbidden}")

# Regulations result must not perform operational enforcement.
result_props = defs.get("documentEvidenceAssessmentResult", {}).get("properties", {})
for forbidden in ("shipment_status", "order_status", "release_shipment", "hold_shipment", "accounting_entry"):
    if forbidden in result_props:
        fail(f"Regulations assessment result must not contain operational field {forbidden}")

# Validate resource examples against actual cross-schema registry.
examples = {
    "requirement-set.json": "regulatoryDocumentRequirementSet",
    "document-evidence-fact-bundle.json": "documentEvidenceFactBundle",
    "assessment-request.json": "documentEvidenceAssessmentRequest",
    "assessment-result.json": "documentEvidenceAssessmentResult",
    "requirement-resolve-request.json": "requirementResolveRequest",
    "document-evidence-resolve-request.json": "documentEvidenceResolveRequest",
    "document-evidence-resolve-response.json": "documentEvidenceResolveResponse",
}
validated_instances = {}
for filename, def_name in examples.items():
    instance = load_json(PACKAGE / "examples" / filename)
    validated_instances[filename] = instance
    target = {"$ref": domain["$id"] + f"#/$defs/{def_name}"}
    errors = sorted(
        Draft202012Validator(target, registry=registry, format_checker=FormatChecker()).iter_errors(instance),
        key=lambda e: list(map(str, e.absolute_path)),
    )
    for error in errors:
        fail(f"{filename}: {'/'.join(map(str, error.absolute_path)) or '<root>'}: {error.message}")

# Event payload examples.
event_examples = {
    "event-document-requirements-determined.json": "documentRequirementsDeterminedEventData",
    "event-document-regulatory-evidence-offered.json": "documentRegulatoryEvidenceOfferedEventData",
    "event-requirement-satisfaction-evaluated.json": "requirementSatisfactionEvaluatedEventData",
}
for filename, def_name in event_examples.items():
    instance = load_json(PACKAGE / "examples" / filename)
    target = {"$ref": events["$id"] + f"#/$defs/{def_name}"}
    errors = sorted(
        Draft202012Validator(target, registry=registry, format_checker=FormatChecker()).iter_errors(instance),
        key=lambda e: list(map(str, e.absolute_path)),
    )
    for error in errors:
        fail(f"{filename}: {'/'.join(map(str, error.absolute_path)) or '<root>'}: {error.message}")

# Tenant consistency proof for fixtures. Runtime must apply the same rule after
# redeeming PlatformContext.
def walk_refs(node):
    if isinstance(node, dict):
        if {"owner_engine_id", "object_type", "object_id", "scope"}.issubset(node.keys()):
            yield node
        for value in node.values():
            yield from walk_refs(value)
    elif isinstance(node, list):
        for value in node:
            yield from walk_refs(value)

for filename in list(examples) + list(event_examples):
    instance = load_json(PACKAGE / "examples" / filename)
    root_tenant = instance.get("tenant_id")
    if root_tenant is None:
        if filename in ("assessment-request.json", "requirement-resolve-request.json", "document-evidence-resolve-request.json", "document-evidence-resolve-response.json", "document-evidence-fact-bundle.json", "assessment-result.json", "requirement-set.json"):
            # no enclosing tenant field; still require every tenant-scoped ref in a
            # fixture to agree with each other
            tenants = {r.get("tenant_id") for r in walk_refs(instance) if r.get("scope") == "tenant"}
            tenants.discard(None)
            if len(tenants) > 1:
                fail(f"{filename}: tenant-scoped references disagree: {sorted(tenants)}")
        continue
    for ref in walk_refs(instance):
        if ref.get("scope") == "tenant" and ref.get("tenant_id") != root_tenant:
            fail(f"{filename}: nested reference tenant {ref.get('tenant_id')} differs from event tenant {root_tenant}")

# Assessment result and request must refer to same requirement/decision in the
# golden fixtures.
req = validated_instances.get("assessment-request.json", {})
res = validated_instances.get("assessment-result.json", {})
if req.get("requirement_reference") != res.get("requirement_reference"):
    fail("assessment request/result fixture requirement reference mismatch")
if req.get("regulatory_decision_reference") != res.get("regulatory_decision_reference"):
    fail("assessment request/result fixture decision reference mismatch")

# Planned events are deliberately NOT activated yet.
surface_items = surfaces.get("events", [])
expected_surfaces = {
    "com.baobab-platform.documents.regulatory-evidence.offered.v1": ("documents", "baobab-trade-docs", "RTD-07"),
    "com.baobab-platform.regulations.document-requirements.determined.v1": ("regulations", "baobab-regulations", "RTD-08"),
    "com.baobab-platform.regulations.requirement-satisfaction.evaluated.v1": ("regulations", "baobab-regulations", "RTD-08"),
}
actual = {item.get("type"): item for item in surface_items}
if set(actual) != set(expected_surfaces):
    fail(f"event surface set mismatch: {sorted(set(actual) ^ set(expected_surfaces))}")
for event_type, (context, producer, step) in expected_surfaces.items():
    item = actual.get(event_type, {})
    if item.get("context") != context:
        fail(f"{event_type}: expected context {context}")
    if item.get("target_producer") != producer:
        fail(f"{event_type}: expected target producer {producer}")
    if item.get("activation_step") != step:
        fail(f"{event_type}: expected activation step {step}")
    if item.get("status") != "DEFINED_NOT_ACTIVATED":
        fail(f"{event_type}: RTD-06 must leave event DEFINED_NOT_ACTIVATED")
    if not str(item.get("payload_ref", "")).startswith("./events.schema.json#/$defs/"):
        fail(f"{event_type}: payload_ref must target RTD-06 events.schema.json")

global_registry = yaml.safe_load(EVENT_REGISTRY.read_text())
registered_types = {
    item.get("type")
    for item in (global_registry.get("events") or [])
    if isinstance(item, dict)
}
for event_type in expected_surfaces:
    if event_type in registered_types:
        fail(f"{event_type} is prematurely registered; activation belongs to RTD-07/RTD-08")

if (PACKAGE / "asyncapi.yaml").exists():
    fail("RTD-06 must not add AsyncAPI before event activation governance")

# OpenAPI semantic checks.
for filename, expected_ops in {
    "regulations.openapi.yaml": {"resolveDocumentaryRequirement", "assessDocumentaryEvidence"},
    "trade-docs.openapi.yaml": {"resolveRegulatoryDocumentEvidence"},
}.items():
    doc = yaml.safe_load((PACKAGE / filename).read_text())
    if doc.get("openapi") != "3.1.0":
        fail(f"{filename} must use OpenAPI 3.1.0")
    operations = set()
    for path_item in (doc.get("paths") or {}).values():
        if not isinstance(path_item, dict):
            continue
        for operation in path_item.values():
            if isinstance(operation, dict) and operation.get("operationId"):
                operations.add(operation["operationId"])
    if operations != expected_ops:
        fail(f"{filename} operation set mismatch: expected {sorted(expected_ops)}, got {sorted(operations)}")

reg_api = yaml.safe_load((PACKAGE / "regulations.openapi.yaml").read_text())
assessment_op = reg_api["paths"]["/documentary-evidence/assessments"]["post"]
param_refs = {p.get("$ref") for p in assessment_op.get("parameters", []) if isinstance(p, dict)}
if "#/components/parameters/IdempotencyKey" not in param_refs:
    fail("assessDocumentaryEvidence must require Idempotency-Key")

if failures:
    for message in failures:
        print(f"FAIL: {message}", file=sys.stderr)
    print(f"{len(failures)} RTD-06 contract failure(s)", file=sys.stderr)
    sys.exit(1)

print("RTD-06 Regulations ↔ Trade Docs exchange contracts passed authority, pinning, tenancy and activation invariants")
