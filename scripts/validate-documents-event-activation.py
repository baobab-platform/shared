#!/usr/bin/env python3
"""Validate ADR-SHARED-023 / RTD-07 documents event producer activation."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = ROOT / "contracts"
EVENTS = CONTRACTS / "events" / "v1"
TDOC_V1 = CONTRACTS / "trade-document" / "v1"
TDOC_V2 = CONTRACTS / "trade-document" / "v2"
EXCHANGE = CONTRACTS / "regulatory-document-exchange" / "v1"
DOC_EVIDENCE = CONTRACTS / "regulatory-document-evidence" / "v1"

failures: list[str] = []


def fail(message: str) -> None:
    failures.append(message)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


contexts_doc = yaml.safe_load((EVENTS / "context-registry.yaml").read_text())
registry_doc = yaml.safe_load((EVENTS / "event-registry.yaml").read_text())
v1_async = yaml.safe_load((TDOC_V1 / "asyncapi.yaml").read_text())
v2_async = yaml.safe_load((TDOC_V2 / "asyncapi.yaml").read_text())
exchange_surfaces = yaml.safe_load((EXCHANGE / "event-surfaces.yaml").read_text())
evidence_async = yaml.safe_load((DOC_EVIDENCE / "asyncapi.yaml").read_text())

contexts = {item["key"]: item for item in contexts_doc.get("contexts", [])}
documents = contexts.get("documents")
if not documents:
    fail("documents event context is missing")
else:
    if documents.get("status") != "ACTIVE":
        fail("documents context must be ACTIVE")
    if "baobab-trade-docs" not in (documents.get("stewards") or []):
        fail("documents context must be stewarded by baobab-trade-docs")
    if "ADR-SHARED-023" not in (documents.get("authority") or []):
        fail("documents context must cite ADR-SHARED-023 activation authority")

entries = {item["type"]: item for item in registry_doc.get("events", [])}

v2_messages = {
    msg["name"]
    for msg in (v2_async.get("components", {}).get("messages", {}) or {}).values()
    if isinstance(msg, dict) and msg.get("name")
}
expected_v2 = {
    "com.baobab-platform.documents.content-artifact.registered.v2",
    "com.baobab-platform.documents.document-relationship.created.v2",
    "com.baobab-platform.documents.document-version.created.v2",
    "com.baobab-platform.documents.document-version.issued.v2",
    "com.baobab-platform.documents.document-version.validity-changed.v2",
    "com.baobab-platform.documents.document-version.verification-changed.v2",
    "com.baobab-platform.documents.trade-document.created.v2",
    "com.baobab-platform.documents.trade-document.issued.v2",
    "com.baobab-platform.documents.trade-document.superseded.v2",
    "com.baobab-platform.documents.trade-document.voided.v2",
}
if v2_messages != expected_v2:
    fail(f"TradeDocument v2 message set changed unexpectedly: {sorted(v2_messages ^ expected_v2)}")

for event_type in sorted(expected_v2):
    entry = entries.get(event_type)
    if not entry:
        fail(f"{event_type}: missing from event registry")
        continue
    if entry.get("producer") != "baobab-trade-docs":
        fail(f"{event_type}: producer must be baobab-trade-docs")
    if entry.get("lifecycle") != "ACTIVE":
        fail(f"{event_type}: lifecycle must be ACTIVE")
    if entry.get("asyncapi") != "contracts/trade-document/v2/asyncapi.yaml":
        fail(f"{event_type}: registry must point to TradeDocument v2 AsyncAPI")

v1_messages = {
    msg["name"]
    for msg in (v1_async.get("components", {}).get("messages", {}) or {}).values()
    if isinstance(msg, dict) and msg.get("name")
}
expected_legacy = {
    "com.baobab-platform.documents.trade-document.issued.v1",
    "com.baobab-platform.documents.trade-document.verified.v1",
    "com.baobab-platform.documents.trade-document.rejected.v1",
}
if v1_messages != expected_legacy:
    fail(f"legacy v1 message set changed unexpectedly: {sorted(v1_messages ^ expected_legacy)}")
for event_type in sorted(expected_legacy):
    entry = entries.get(event_type)
    if not entry:
        fail(f"{event_type}: legacy event must remain registered as compatibility history")
        continue
    if entry.get("lifecycle") != "PROPOSED":
        fail(f"{event_type}: legacy v1 event must remain PROPOSED")
    if entry.get("producer"):
        fail(f"{event_type}: legacy v1 event must remain producerless")

evidence_messages = {
    msg["name"]
    for msg in (evidence_async.get("components", {}).get("messages", {}) or {}).values()
    if isinstance(msg, dict) and msg.get("name")
}
evidence_type = "com.baobab-platform.documents.regulatory-evidence.offered.v1"
if evidence_messages != {evidence_type}:
    fail(f"regulatory-document-evidence AsyncAPI must define only {evidence_type}")
entry = entries.get(evidence_type)
if not entry:
    fail(f"{evidence_type}: missing from event registry")
else:
    if entry.get("producer") != "baobab-trade-docs":
        fail(f"{evidence_type}: producer must be baobab-trade-docs")
    if entry.get("lifecycle") != "ACTIVE":
        fail(f"{evidence_type}: lifecycle must be ACTIVE")
    if entry.get("asyncapi") != "contracts/regulatory-document-evidence/v1/asyncapi.yaml":
        fail(f"{evidence_type}: incorrect AsyncAPI registry path")

surface_items = {item["type"]: item for item in exchange_surfaces.get("events", [])}
surface = surface_items.get(evidence_type, {})
if surface.get("status") != "ACTIVE":
    fail(f"{evidence_type}: RTD-06 event surface must now be ACTIVE")
if surface.get("activation_authority") != "ADR-SHARED-023":
    fail(f"{evidence_type}: activation authority must be ADR-SHARED-023")
if surface.get("target_producer") != "baobab-trade-docs":
    fail(f"{evidence_type}: target producer must remain baobab-trade-docs")
if surface.get("activation_step") != "RTD-07":
    fail(f"{evidence_type}: activation step must remain RTD-07")

# RTD-08 may activate Regulations events, but RTD-07's document authority
# invariants still require the Regulations producer/context to remain distinct.
for reg_type in (
    "com.baobab-platform.regulations.document-requirements.determined.v1",
    "com.baobab-platform.regulations.requirement-satisfaction.evaluated.v1",
):
    entry = entries.get(reg_type)
    if not entry:
        fail(f"{reg_type}: RTD-08 activation is now required")
        continue
    if entry.get("producer") != "baobab-regulations":
        fail(f"{reg_type}: must be produced by baobab-regulations, never baobab-trade-docs")
    if entry.get("lifecycle") != "ACTIVE":
        fail(f"{reg_type}: must be ACTIVE after RTD-08")
    reg_surface = surface_items.get(reg_type, {})
    if reg_surface.get("status") != "ACTIVE":
        fail(f"{reg_type}: event surface must be ACTIVE after RTD-08")
    if reg_surface.get("activation_step") != "RTD-08":
        fail(f"{reg_type}: activation step must remain RTD-08")

# Validate the active document-side exchange example against both canonical
# envelope and RTD-06 data payload schema.
registry = Registry()
for path in sorted(CONTRACTS.rglob("*.json")):
    try:
        doc = load_json(path)
    except json.JSONDecodeError:
        continue
    if isinstance(doc, dict) and isinstance(doc.get("$id"), str):
        registry = registry.with_resource(doc["$id"], Resource.from_contents(doc))

example = load_json(DOC_EVIDENCE / "examples" / "regulatory-evidence-offered.json")
envelope = load_json(EVENTS / "envelope.schema.json")
payloads = load_json(EXCHANGE / "events.schema.json")

for error in Draft202012Validator(
    envelope, registry=registry, format_checker=FormatChecker()
).iter_errors(example):
    fail(f"regulatory-evidence-offered envelope: {error.message}")

payload_target = {
    "$ref": payloads["$id"] + "#/$defs/documentRegulatoryEvidenceOfferedEventData"
}
for error in Draft202012Validator(
    payload_target, registry=registry, format_checker=FormatChecker()
).iter_errors(example.get("data")):
    fail(f"regulatory-evidence-offered data: {error.message}")

if example.get("type") != evidence_type:
    fail("regulatory-evidence-offered example type mismatch")
if example.get("source") != "urn:baobab-platform:service:baobab-trade-docs":
    fail("active document event source must identify logical baobab-trade-docs producer")
if example.get("tenantid") != (example.get("data") or {}).get("tenant_id"):
    fail("event envelope tenantid must equal payload tenant_id")

# Every tenant-scoped nested RTD-05 reference must remain in the event tenant.
def walk_refs(node):
    if isinstance(node, dict):
        if {"owner_engine_id", "object_type", "object_id", "scope"}.issubset(node.keys()):
            yield node
        for value in node.values():
            yield from walk_refs(value)
    elif isinstance(node, list):
        for value in node:
            yield from walk_refs(value)

for ref in walk_refs(example.get("data") or {}):
    if ref.get("scope") == "tenant" and ref.get("tenant_id") != example.get("tenantid"):
        fail("regulatory-evidence-offered contains a foreign-tenant nested reference")

# ACTIVE does not mean runtime implementation exists. Keep architecture prose
# explicit so contract activation is not misread as deployment evidence.
v2_description = str((v2_async.get("info") or {}).get("description", ""))
if "baobab-trade-docs" not in v2_description or "does not claim" not in v2_description.lower():
    fail("TradeDocument v2 AsyncAPI must state producer authority without claiming runtime deployment")

if failures:
    for message in failures:
        print(f"FAIL: {message}", file=sys.stderr)
    print(f"{len(failures)} RTD-07 activation failure(s)", file=sys.stderr)
    sys.exit(1)

print("RTD-07 documents event activation passed stewardship, producer, legacy-v1 and post-RTD-08 authority-separation invariants")
