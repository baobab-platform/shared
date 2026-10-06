#!/usr/bin/env python3
"""Validate ADR-SHARED-024 / RTD-08 Regulations namespace and event activation."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = ROOT / "contracts"
CAPABILITY = CONTRACTS / "capability" / "v1"
EVENTS = CONTRACTS / "events" / "v1"
EXCHANGE = CONTRACTS / "regulatory-document-exchange" / "v1"
ASSESSMENT = CONTRACTS / "regulatory-document-assessment" / "v1"
DOC_EVIDENCE = CONTRACTS / "regulatory-document-evidence" / "v1"

failures: list[str] = []


def fail(message: str) -> None:
    failures.append(message)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


namespace_doc = yaml.safe_load((CAPABILITY / "namespace-registry.yaml").read_text())
domain_schema = load_json(CAPABILITY / "domain.schema.json")
contexts_doc = yaml.safe_load((EVENTS / "context-registry.yaml").read_text())
event_registry_doc = yaml.safe_load((EVENTS / "event-registry.yaml").read_text())
surface_doc = yaml.safe_load((EXCHANGE / "event-surfaces.yaml").read_text())
assessment_async = yaml.safe_load((ASSESSMENT / "asyncapi.yaml").read_text())
document_async = yaml.safe_load((DOC_EVIDENCE / "asyncapi.yaml").read_text())

namespace_domains = [item["key"] for item in namespace_doc.get("domains", [])]
schema_domains = domain_schema.get("$defs", {}).get("capabilityDomain", {}).get("enum", [])

if "regulations" not in namespace_domains:
    fail("namespace-registry.yaml must register regulations")
if "regulations" not in schema_domains:
    fail("capabilityDomain enum must register regulations")
if sorted(namespace_domains) != sorted(schema_domains):
    fail("namespace registry and capabilityDomain enum must remain identical")

# RTD-08 explicitly does not migrate these namespaces.
for domain in ("tax", "customs"):
    if domain not in namespace_domains:
        fail(f"RTD-08 must preserve the existing {domain} capability domain")

contexts = {item["key"]: item for item in contexts_doc.get("contexts", [])}
reg_context = contexts.get("regulations")
if not reg_context:
    fail("regulations event context is missing")
else:
    if reg_context.get("status") != "ACTIVE":
        fail("regulations event context must be ACTIVE")
    if reg_context.get("stewards") != ["baobab-regulations"]:
        fail("regulations context must have exactly baobab-regulations as steward")
    if reg_context.get("capability_domains") != ["regulations"]:
        fail("regulations context must map only to the regulations capability domain")
    if "ADR-SHARED-024" not in (reg_context.get("authority") or []):
        fail("regulations context must cite ADR-SHARED-024 activation authority")

expected_types = {
    "com.baobab-platform.regulations.document-requirements.determined.v1",
    "com.baobab-platform.regulations.requirement-satisfaction.evaluated.v1",
}

messages = {
    msg["name"]
    for msg in (assessment_async.get("components", {}).get("messages", {}) or {}).values()
    if isinstance(msg, dict) and msg.get("name")
}
if messages != expected_types:
    fail(f"RTD-08 AsyncAPI message set mismatch: {sorted(messages ^ expected_types)}")

entries = {
    item["type"]: item
    for item in event_registry_doc.get("events", [])
    if isinstance(item, dict) and item.get("type")
}
for event_type in sorted(expected_types):
    entry = entries.get(event_type)
    if not entry:
        fail(f"{event_type}: missing from event registry")
        continue
    if entry.get("producer") != "baobab-regulations":
        fail(f"{event_type}: producer must be baobab-regulations")
    if entry.get("lifecycle") != "ACTIVE":
        fail(f"{event_type}: lifecycle must be ACTIVE")
    if entry.get("asyncapi") != "contracts/regulatory-document-assessment/v1/asyncapi.yaml":
        fail(f"{event_type}: incorrect AsyncAPI registry path")

surfaces = {item["type"]: item for item in surface_doc.get("events", [])}
for event_type in sorted(expected_types):
    surface = surfaces.get(event_type, {})
    if surface.get("context") != "regulations":
        fail(f"{event_type}: event surface context must be regulations")
    if surface.get("target_producer") != "baobab-regulations":
        fail(f"{event_type}: target producer must be baobab-regulations")
    if surface.get("activation_step") != "RTD-08":
        fail(f"{event_type}: activation step must remain RTD-08")
    if surface.get("status") != "ACTIVE":
        fail(f"{event_type}: surface must be ACTIVE")
    if surface.get("activation_authority") != "ADR-SHARED-024":
        fail(f"{event_type}: activation authority must be ADR-SHARED-024")
    if surface.get("asyncapi") != "../../regulatory-document-assessment/v1/asyncapi.yaml":
        fail(f"{event_type}: surface must point to the Regulations owner AsyncAPI")

# RTD-07 document-side producer authority must remain intact.
document_type = "com.baobab-platform.documents.regulatory-evidence.offered.v1"
document_entry = entries.get(document_type)
if not document_entry:
    fail(f"{document_type}: document-side RTD-07 event disappeared")
else:
    if document_entry.get("producer") != "baobab-trade-docs":
        fail(f"{document_type}: must remain produced by baobab-trade-docs")
    if document_entry.get("lifecycle") != "ACTIVE":
        fail(f"{document_type}: must remain ACTIVE")

document_messages = {
    msg["name"]
    for msg in (document_async.get("components", {}).get("messages", {}) or {}).values()
    if isinstance(msg, dict) and msg.get("name")
}
if document_messages != {document_type}:
    fail("RTD-07 document-side AsyncAPI changed unexpectedly during RTD-08")

# No speculative wider Regulations event family is activated by RTD-08.
registered_regulations_types = {
    event_type for event_type in entries if event_type.startswith("com.baobab-platform.regulations.")
}
if registered_regulations_types != expected_types:
    fail(
        "RTD-08 must activate only the two contracted Regulations types; "
        f"unexpected={sorted(registered_regulations_types ^ expected_types)}"
    )

# The old repository-local v0 event family is not a Shared platform event.
for event_type in entries:
    if "regulations.evaluation." in event_type or event_type.endswith(".v0"):
        fail(f"{event_type}: local Regulations v0 audit event must not be promoted")

# Validate active owner-specific examples against canonical envelope + RTD-06 data schemas.
registry = Registry()
for path in sorted(CONTRACTS.rglob("*.json")):
    try:
        doc = load_json(path)
    except json.JSONDecodeError:
        continue
    if isinstance(doc, dict) and isinstance(doc.get("$id"), str):
        registry = registry.with_resource(doc["$id"], Resource.from_contents(doc))

envelope = load_json(EVENTS / "envelope.schema.json")
exchange_payloads = load_json(EXCHANGE / "events.schema.json")
examples = {
    "document-requirements-determined.json": (
        "com.baobab-platform.regulations.document-requirements.determined.v1",
        "documentRequirementsDeterminedEventData",
        "regulatory-decision:",
    ),
    "requirement-satisfaction-evaluated.json": (
        "com.baobab-platform.regulations.requirement-satisfaction.evaluated.v1",
        "requirementSatisfactionEvaluatedEventData",
        "regulatory-evidence-assessment:",
    ),
}

def walk_refs(node):
    if isinstance(node, dict):
        if {"owner_engine_id", "object_type", "object_id", "scope"}.issubset(node.keys()):
            yield node
        for value in node.values():
            yield from walk_refs(value)
    elif isinstance(node, list):
        for value in node:
            yield from walk_refs(value)

for filename, (event_type, def_name, subject_prefix) in examples.items():
    example = load_json(ASSESSMENT / "examples" / filename)

    for error in Draft202012Validator(
        envelope, registry=registry, format_checker=FormatChecker()
    ).iter_errors(example):
        fail(f"{filename} envelope: {error.message}")

    payload_target = {
        "$ref": exchange_payloads["$id"] + f"#/$defs/{def_name}"
    }
    for error in Draft202012Validator(
        payload_target, registry=registry, format_checker=FormatChecker()
    ).iter_errors(example.get("data")):
        fail(f"{filename} data: {error.message}")

    if example.get("type") != event_type:
        fail(f"{filename}: event type mismatch")
    if example.get("source") != "urn:baobab-platform:service:baobab-regulations":
        fail(f"{filename}: source must identify logical baobab-regulations producer")
    if not str(example.get("subject", "")).startswith(subject_prefix):
        fail(f"{filename}: unexpected canonical subject")
    if example.get("tenantid") != (example.get("data") or {}).get("tenant_id"):
        fail(f"{filename}: envelope tenantid must equal payload tenant_id")

    for ref in walk_refs(example.get("data") or {}):
        if ref.get("scope") == "tenant" and ref.get("tenant_id") != example.get("tenantid"):
            fail(f"{filename}: nested tenant-scoped reference crosses event tenant")

# ACTIVE contract authority must not be presented as runtime deployment evidence.
description = str((assessment_async.get("info") or {}).get("description", ""))
if "baobab-regulations" not in description:
    fail("RTD-08 AsyncAPI must identify baobab-regulations producer authority")
readme_text = (ASSESSMENT / "README.md").read_text()
if "does not assert" not in readme_text.lower() or "outbox" not in readme_text.lower():
    fail("RTD-08 README must distinguish active contract authority from runtime deployment")

if failures:
    for message in failures:
        print(f"FAIL: {message}", file=sys.stderr)
    print(f"{len(failures)} RTD-08 activation failure(s)", file=sys.stderr)
    sys.exit(1)

print("RTD-08 Regulations namespace/event activation passed namespace, stewardship, producer and authority-separation invariants")
