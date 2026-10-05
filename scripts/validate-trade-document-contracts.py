#!/usr/bin/env python3
"""Validate TradeDocument v2 contracts (ADR-SHARED-020 / RTD-04).

The v2 package reconciles the pre-activation v1 scaffold with TDOC-0001/0002.
This gate protects the authority and semantic separations that motivated v2.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = ROOT / "contracts"
V1 = CONTRACTS / "trade-document" / "v1"
V2 = CONTRACTS / "trade-document" / "v2"
BASE_URI = "https://contracts.baobab-platform.com/"

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

domain = load_json(V2 / "domain.schema.json")
events = load_json(V2 / "events.schema.json")
asyncapi = yaml.safe_load((V2 / "asyncapi.yaml").read_text())
v1_domain = load_json(V1 / "domain.schema.json")

expected_ids = {
    "domain.schema.json": BASE_URI + "trade-document/v2/domain.schema.json",
    "events.schema.json": BASE_URI + "trade-document/v2/events.schema.json",
}
for name, expected in expected_ids.items():
    doc = domain if name == "domain.schema.json" else events
    if doc.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        fail(f"{name} must use JSON Schema Draft 2020-12")
    if doc.get("$id") != expected:
        fail(f"{name} has incorrect immutable $id: {doc.get('$id')!r}")

defs = domain.get("$defs", {})

# Identity authority: Trade Docs, not Control Plane.
tdoc_id = defs.get("tradeDocumentId", {})
if "Control Plane" in tdoc_id.get("description", ""):
    fail("v2 tradeDocumentId still claims Control Plane minting")
if not tdoc_id.get("pattern", "").startswith("^tdoc_"):
    fail("v2 tradeDocumentId must keep opaque tdoc_ domain identity")

# Extensible type registry seam, not the old closed enum.
type_def = defs.get("documentTypeCode", {})
if "enum" in type_def:
    fail("documentTypeCode must be extensible; closed enum is prohibited in v2")
if not type_def.get("pattern"):
    fail("documentTypeCode must retain a governed code syntax")

# Lifecycle axes must stay separate.
lifecycle = set(defs.get("documentLifecycleState", {}).get("enum", []))
verification = set(defs.get("verificationState", {}).get("enum", []))
if {"VERIFIED", "REJECTED"} & lifecycle:
    fail("verification/workflow outcomes leaked back into document lifecycle")
if not {"DRAFT", "ISSUED", "SUPERSEDED", "VOIDED"}.issubset(lifecycle):
    fail("document lifecycle is missing required TDOC states")
if "VERIFIED" not in verification or "FAILED" not in verification:
    fail("verification axis is incomplete")

trade_document = defs.get("tradeDocument", {})
td_props = trade_document.get("properties", {})
for forbidden in ("status", "storage_reference", "related_shipment_id", "related_procurement_request_id"):
    if forbidden in td_props:
        fail(f"TradeDocument root must not contain legacy field {forbidden}")
for required in (
    "trade_document_id", "tenant_id", "document_type", "document_family",
    "issuer_claim", "lifecycle_state", "aggregate_version",
):
    if required not in trade_document.get("required", []):
        fail(f"TradeDocument must require {required}")

artifact = defs.get("contentArtifact", {})
if "storage_reference" not in artifact.get("required", []):
    fail("ContentArtifact must own storage_reference")
if "digest_value" not in artifact.get("required", []):
    fail("ContentArtifact must carry integrity metadata")

version = defs.get("documentVersion", {})
for required in (
    "document_version_id", "trade_document_id", "version_sequence",
    "lifecycle_snapshot", "content_artifacts", "provenance",
):
    if required not in version.get("required", []):
        fail(f"DocumentVersion must require {required}")
for forbidden in ("verification_state", "temporal_validity_state"):
    if forbidden in version.get("properties", {}):
        fail(f"DocumentVersion must remain immutable; mutable projection {forbidden} is embedded")

for projection_name, state_field in (
    ("documentVerificationProjection", "verification_state"),
    ("documentTemporalValidityProjection", "temporal_validity_state"),
):
    projection = defs.get(projection_name, {})
    if state_field not in projection.get("required", []):
        fail(f"{projection_name} must require {state_field}")

relations = defs.get("relationshipType", {}).get("enum", [])
if "FULFILS_REQUIREMENT" in relations:
    fail("RTD-04 must not pre-empt RTD-05/RTD-06 with a document-to-requirement relationship")

# Preserve v1 instead of silently mutating it (Thamani ADR-THA-0018).
if "tradeDocumentStatus" not in v1_domain.get("$defs", {}):
    fail("v1 compatibility scaffold was mutated/removed instead of preserved")
if "storage_reference" not in v1_domain.get("$defs", {}).get("tradeDocument", {}).get("properties", {}):
    fail("v1 compatibility shape changed; RTD-04 requires a new v2 package")

# Validate resource examples against the real cross-schema registry.
for file_name, def_name in (
    ("trade-document.json", "tradeDocument"),
    ("document-version.json", "documentVersion"),
    ("document-verification.json", "documentVerificationProjection"),
    ("document-temporal-validity.json", "documentTemporalValidityProjection"),
):
    instance = load_json(V2 / "examples" / file_name)
    schema = {"$ref": domain["$id"] + f"#/$defs/{def_name}"}
    errors = sorted(
        Draft202012Validator(schema, registry=registry, format_checker=FormatChecker()).iter_errors(instance),
        key=lambda e: list(map(str, e.absolute_path)),
    )
    for error in errors:
        fail(f"{file_name}: {'/'.join(map(str, error.absolute_path)) or '<root>'}: {error.message}")

# Negative proof: verification must never be accepted as lifecycle.
bad = dict(load_json(V2 / "examples" / "trade-document.json"))
bad["lifecycle_state"] = "VERIFIED"
schema = {"$ref": domain["$id"] + "#/$defs/tradeDocument"}
if not list(Draft202012Validator(schema, registry=registry).iter_errors(bad)):
    fail("TradeDocument incorrectly accepts VERIFIED as a lifecycle state")

# Proposed v2 event surface.
messages = (asyncapi.get("components") or {}).get("messages") or {}
actual_types = {message.get("name") for message in messages.values()}
expected_types = {
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
if actual_types != expected_types:
    fail(f"v2 AsyncAPI event set differs from RTD-04 target: {sorted(actual_types ^ expected_types)}")
if any(".trade-document.verified." in t or ".trade-document.rejected." in t for t in actual_types):
    fail("v2 reintroduced legacy lifecycle/verification conflation")

if failures:
    for message in failures:
        print(f"FAIL: {message}", file=sys.stderr)
    print(f"{len(failures)} TradeDocument v2 contract failure(s)", file=sys.stderr)
    sys.exit(1)

print("TradeDocument v2 contracts passed RTD-04 authority, lifecycle, versioning and artifact invariants")
