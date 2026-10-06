#!/usr/bin/env python3
"""Validate R-CAP-08 canonical regulatory decision contracts."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = ROOT / "contracts"
PACKAGE = CONTRACTS / "regulatory-decision" / "v1"
CAPABILITY_DEFS = CONTRACTS / "regulations" / "v1" / "capabilities.yaml"
CATALOGUE = CONTRACTS / "capability" / "v1" / "catalogue.yaml"

failures: list[str] = []


def fail(message: str) -> None:
    failures.append(message)


def load_json(path: Path) -> dict:
    value = json.loads(path.read_text())
    if not isinstance(value, dict):
        raise TypeError(f"{path} must contain a JSON object")
    return value


registry = Registry()
for path in sorted(CONTRACTS.rglob("*.json")):
    try:
        document = load_json(path)
    except (json.JSONDecodeError, TypeError):
        continue
    if isinstance(document.get("$id"), str):
        registry = registry.with_resource(document["$id"], Resource.from_contents(document))

domain = load_json(PACKAGE / "domain.schema.json")
if domain.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
    fail("regulatory-decision domain schema must use JSON Schema Draft 2020-12")
if domain.get("$id") != "https://contracts.baobab-platform.com/regulatory-decision/v1/domain.schema.json":
    fail("regulatory-decision domain schema has incorrect immutable $id")

defs = domain.get("$defs", {})
for required_def in (
    "decisionEvaluateRequest",
    "decisionEvaluateResponse",
    "regulatoryDecisionReference",
    "regulatoryAssessmentReference",
    "ruleSetReference",
    "decisionReason",
    "decisionProvenance",
    "replayIdentity",
):
    if required_def not in defs:
        fail(f"domain schema is missing $defs/{required_def}")

# R-CAP-08 authority and pinning.
for name, obj_type in (
    ("regulatoryDecisionReference", "REGULATORY_DECISION"),
    ("regulatoryAssessmentReference", "REGULATORY_ASSESSMENT"),
    ("ruleSetReference", "REGULATORY_RULE_SET"),
    ("ruleVersionReference", "REGULATORY_RULE_VERSION"),
):
    encoded = json.dumps(defs.get(name, {}), sort_keys=True)
    if "pinnedCrossEngineObjectReference" not in encoded:
        fail(f"{name} must use the pinned ADR-SHARED-021 reference")
    if "baobab-regulations" not in encoded or obj_type not in encoded:
        fail(f"{name} must constrain owner=baobab-regulations object_type={obj_type}")

request = defs.get("decisionEvaluateRequest", {})
required = set(request.get("required", []))
for field in (
    "context_id",
    "question",
    "assessment_purpose",
    "subject_references",
    "regulated_activities",
    "facts",
    "evidence_references",
    "rule_set_reference",
    "legal_time",
    "knowledge_time",
    "evaluation_profile",
    "requested_assurance",
    "requested_enforcement_class_ceiling",
    "replay_key",
):
    if field not in required:
        fail(f"decisionEvaluateRequest must require {field}")

request_props = request.get("properties", {})
for forbidden in (
    "tenant_id",
    "opa_url",
    "rego_package",
    "rego_query",
    "bundle_revision",
    "compiler_version",
    "engine_instance_id",
):
    if forbidden in request_props:
        fail(f"decisionEvaluateRequest must not expose {forbidden}")

# Outcomes are regulatory semantics, never evaluator health/protocol states.
outcomes = set(defs.get("decisionOutcome", {}).get("enum", []))
expected_outcomes = {
    "SATISFIED",
    "SATISFIED_WITH_REQUIREMENTS",
    "UNSATISFIED",
    "PROHIBITED",
    "INDETERMINATE",
    "NOT_APPLICABLE",
}
if outcomes != expected_outcomes:
    fail(f"decisionOutcome mismatch: expected {sorted(expected_outcomes)}, got {sorted(outcomes)}")
for technical in (
    "ERROR",
    "EVALUATOR_UNDEFINED",
    "EVALUATOR_PROTOCOL_ERROR",
    "EVALUATOR_RUNTIME_ERROR",
    "EVALUATOR_NOT_READY",
):
    if technical in outcomes:
        fail(f"technical failure {technical} must not be a regulatory outcome")

response = defs.get("decisionEvaluateResponse", {})
response_required = set(response.get("required", []))
for field in (
    "decision_reference",
    "assessment_reference",
    "outcome",
    "enforcement_class",
    "reasons",
    "legal_basis_references",
    "evidence_references",
    "recommended_disposition",
    "rule_set_reference",
    "rule_set_fingerprint",
    "evaluated_at",
    "legal_time",
    "knowledge_time",
    "provenance",
    "replay_identity",
):
    if field not in response_required:
        fail(f"decisionEvaluateResponse must require {field}")

response_props = response.get("properties", {})
for forbidden in (
    "shipment_status",
    "order_status",
    "release_shipment",
    "hold_shipment",
    "opa_decision_id",
    "rego_result",
):
    if forbidden in response_props:
        fail(f"decisionEvaluateResponse must not contain {forbidden}")

# Validate examples through the complete offline registry.
for filename, def_name in (
    ("evaluate-request.json", "decisionEvaluateRequest"),
    ("evaluate-response.json", "decisionEvaluateResponse"),
):
    instance = load_json(PACKAGE / "examples" / filename)
    target = {"$ref": domain["$id"] + f"#/$defs/{def_name}"}
    errors = sorted(
        Draft202012Validator(
            target,
            registry=registry,
            format_checker=FormatChecker(),
        ).iter_errors(instance),
        key=lambda error: list(map(str, error.absolute_path)),
    )
    for error in errors:
        location = "/".join(map(str, error.absolute_path)) or "<root>"
        fail(f"{filename}: {location}: {error.message}")

# Request fixture must carry one trusted tenant only through nested tenant refs,
# never as a root authority selector.
request_example = load_json(PACKAGE / "examples" / "evaluate-request.json")
if "tenant_id" in request_example:
    fail("evaluate-request example must not contain root tenant_id")

def walk_refs(node):
    if isinstance(node, dict):
        if {"owner_engine_id", "object_type", "object_id", "scope"}.issubset(node):
            yield node
        for value in node.values():
            yield from walk_refs(value)
    elif isinstance(node, list):
        for value in node:
            yield from walk_refs(value)

tenants = {
    ref.get("tenant_id")
    for ref in walk_refs(request_example)
    if ref.get("scope") == "tenant"
}
tenants.discard(None)
if len(tenants) > 1:
    fail(f"evaluate-request tenant-scoped references disagree: {sorted(tenants)}")

# OpenAPI surface: exact operation, mandatory idempotency, and technical 503.
openapi = yaml.safe_load((PACKAGE / "regulations.openapi.yaml").read_text())
if openapi.get("openapi") != "3.1.0":
    fail("regulatory decision OpenAPI must use 3.1.0")
operation = (
    (openapi.get("paths") or {})
    .get("/decisions/evaluate", {})
    .get("post", {})
)
if operation.get("operationId") != "evaluateRegulatoryDecision":
    fail("POST /decisions/evaluate must use operationId evaluateRegulatoryDecision")
parameter_refs = {
    item.get("$ref")
    for item in operation.get("parameters", [])
    if isinstance(item, dict)
}
if "#/components/parameters/IdempotencyKey" not in parameter_refs:
    fail("evaluateRegulatoryDecision must require Idempotency-Key")
if "503" not in (operation.get("responses") or {}):
    fail("evaluateRegulatoryDecision must expose technical unavailability separately")

# Capability catalogue/definition must point exactly at this contract.
catalogue = yaml.safe_load(CATALOGUE.read_text())
catalogued = {
    item.get("capability_key"): item
    for item in (catalogue.get("capabilities") or [])
    if isinstance(item, dict)
}
entry = catalogued.get("regulations.decision.evaluate")
if not isinstance(entry, dict):
    fail("regulations.decision.evaluate must be catalogued")
else:
    if entry.get("owner") != "baobab-regulations":
        fail("regulations.decision.evaluate owner must be baobab-regulations")
    if entry.get("source") != "../../regulations/v1/capabilities.yaml":
        fail("regulations.decision.evaluate must source regulations/v1/capabilities.yaml")

definitions_doc = yaml.safe_load(CAPABILITY_DEFS.read_text())
definitions = {
    item.get("capability_key"): item
    for item in (definitions_doc.get("capabilities") or [])
    if isinstance(item, dict)
}
definition = definitions.get("regulations.decision.evaluate")
if not isinstance(definition, dict):
    fail("regulations.decision.evaluate capability definition is missing")
else:
    if definition.get("lifecycle") != "DRAFT":
        fail("regulations.decision.evaluate lifecycle must remain DRAFT")
    if definition.get("maturity") != "EXPERIMENTAL":
        fail("regulations.decision.evaluate maturity must remain EXPERIMENTAL")
    contracts = definition.get("contracts") or []
    if len(contracts) != 1 or contracts[0].get("major") != 1:
        fail("regulations.decision.evaluate must define exactly contract major 1")
    else:
        contract = contracts[0]
        if contract.get("request_schema") != (
            "../../regulatory-decision/v1/domain.schema.json#/$defs/decisionEvaluateRequest"
        ):
            fail("decision.evaluate request schema reference is incorrect")
        if contract.get("response_schema") != (
            "../../regulatory-decision/v1/domain.schema.json#/$defs/decisionEvaluateResponse"
        ):
            fail("decision.evaluate response schema reference is incorrect")
        if contract.get("error_schema") != "../../errors/v1/problem-details.schema.json":
            fail("decision.evaluate error schema must use Shared ProblemDetails")

if failures:
    for message in failures:
        print(f"FAIL: {message}", file=sys.stderr)
    print(f"{len(failures)} R-CAP-08 contract failure(s)", file=sys.stderr)
    sys.exit(1)

print(
    "R-CAP-08 decision evaluation contract passed provider-neutrality, temporal, "
    "pinning, replay, outcome/error and capability-catalogue invariants"
)
