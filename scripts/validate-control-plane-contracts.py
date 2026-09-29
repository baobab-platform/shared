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
     external-systems.yaml registers well-formed systems (ADR-SHARED-012);
  6. every provisioning blocking reason is a registered code
     (ADR-SHARED-015);
  7. the provider migration contract keeps cohorts deterministic, stateful
     cutovers single-writer and its lifecycle, blockers and warnings in
     step with provider-migration-lifecycle.yaml (ADR-BCP-006 sections
     44-58, 119-122);
  8. the changeset contract derives what the caller must not supply, has
     no dead-end state, names real operations for its commands, and keeps
     change kinds, plan steps and blocking codes in step with
     changeset-lifecycle.yaml (ADR-BCP-021 gate CCM-01).

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
    "platform-context.schema.json": {
        "organisationKind", "PlatformContextResolveRequest", "PlatformContext",
        "ComposedResolutionRequest", "ComposedResolution",
    },
    "provisioning-desired-state.schema.json": {
        "desiredStateProvenance", "ProvisioningDesiredState", "TenantProvisioningCreateRequest",
    },
    "change-plan.schema.json": {
        "riskClass", "planFinding", "planCheck", "planStep", "impactAnalysis", "ChangePlan",
    },
    "provisioning-plan.schema.json": {
        "provisioningOperation", "provisioningStepResources", "provisioningStep", "ProvisioningPlan",
    },
    "approval-decision.schema.json": {
        "approvalOutcome", "ApprovalDecisionRequest", "ApprovalDecision",
    },
    "execution-operation.schema.json": {
        "operationStatus", "operationType", "ExecutionOperation", "OperationCommandRequest",
    },
    "provider-migration.schema.json": {
        "migrationStage", "migrationMode", "dataStrategy", "rollbackStrategy", "migrationCapability",
        "cohortSelector", "migrationCohort", "cutoverWindow", "ProviderMigrationRequest", "migrationOperation",
        "migrationStepResources", "migrationStep", "migrationDiscovery", "ProviderMigrationPlan", "migrationTransition",
        "ProviderMigrationAdvanceRequest", "ProviderMigration",
    },
    "engine-migration-task.schema.json": {
        "engineMigrationTaskId", "taskOperation", "taskRole", "taskDirection", "taskStatus", "counterpart", "cohortContexts",
        "taskResult", "EngineMigrationTask", "EngineMigrationTaskPage", "EngineMigrationTaskReport",
    },
    "changeset.schema.json": {
        "changesetState", "changesetType", "changeSource", "TenantSuspension", "TenantReinstatement", "MarketActivation", "MappingActivation", "desiredChange",
        "ChangesetCreateRequest", "ChangesetCancelRequest", "planReference", "Changeset", "ChangesetPage",
        "changesetOperation", "changesetStepResources", "changesetStep", "ChangesetPlan", "affectedResource",
        "verificationResult", "ChangeOutcome",
    },
    "market.schema.json": {
        "marketId", "marketType", "market", "marketHierarchy", "marketValidationFinding",
        "MarketCreateRequest", "MarketUpdateRequest", "MarketActivationRequest",
    },
    "tenant-provisioning.schema.json": {
        "legacyProvisioningState", "blockingReason", "TenantProvisioning", "TenantProvisioningReplanRequest",
        "ProvisioningCommandRequest", "TenantProvisioningPage", "ProvisioningReadiness", "ProvisioningDrift",
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


def check_platform_context() -> None:
    schema = "platform-context.schema.json"
    example = json.loads((CP / "examples" / "platform-context.json").read_text())
    for key, definition in (("resolve_request", "PlatformContextResolveRequest"),
                            ("resolve_by_iam_request", "PlatformContextResolveRequest"),
                            ("context", "PlatformContext"),
                            ("composed_request", "ComposedResolutionRequest"),
                            ("composed", "ComposedResolution")):
        accepts(schema, definition, example[key], f"platform-context {key}")
    # An empty body is a valid request: the verified token supplies the rest.
    accepts(schema, "PlatformContextResolveRequest", {}, "empty platform-context request")

    request, by_iam = example["resolve_request"], example["resolve_by_iam_request"]
    rejects(schema, "PlatformContextResolveRequest", {**request, **by_iam}, "organisation_id and iam_organization together")
    rejects(schema, "PlatformContextResolveRequest", {**request, "expected_organisation_type": "PRODUCT"}, "non-organisation kind")
    rejects(schema, "PlatformContextResolveRequest", {**request, "tenant_id": "tenant-123"}, "non-canonical tenant id")
    rejects(schema, "PlatformContextResolveRequest", {**request, "principal_id": "prn_x"}, "caller-stated principal")

    context = example["context"]
    for field in ("context_id", "tenant_id", "resolved_at"):
        bad = copy.deepcopy(context)
        del bad[field]
        rejects(schema, "PlatformContext", bad, f"context without {field}")
    rejects(schema, "PlatformContext", {**context, "context_id": "ctx-1"}, "non-uuid context id")

    composed_request, composed = example["composed_request"], example["composed"]
    bad = copy.deepcopy(composed_request)
    del bad["canonical_entity_id"]
    rejects(schema, "ComposedResolutionRequest", bad, "composed request without canonical_entity_id")
    rejects(schema, "ComposedResolution", {**composed, "capability": {**composed["capability"], "binding_mode": "SECONDARY"}},
            "retired binding mode")
    rejects(schema, "ComposedResolution", {**composed, "topology": {**composed["topology"], "id": "instance-1"}},
            "non-canonical engine instance id")


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


def check_mapping_resolution() -> None:
    schema = "canonical-mapping.schema.json"
    example = json.loads((CP / "examples" / "mapping-resolution.json").read_text())
    accepts(schema, "resolutionRequest", example["resolution_request"], "mapping-resolution request")
    for key in ("resolution_response", "canonical_resolution_response"):
        accepts(schema, "resolutionResponse", example[key], f"mapping-resolution {key}")

    registry = yaml.safe_load((CP / "external-systems.yaml").read_text())
    registered = {(system["system_namespace"], engine) for system in registry["systems"] for engine in system["engine_ids"]}
    request = example["resolution_request"]
    if (request["target_system_namespace"], request["target_engine_id"]) not in registered:
        fail("mapping-resolution request names an unregistered system")

    # The context is redeemed, never supplied (ADR-SHARED-014).
    for field, value in (("context", {"tenant_id": "tn_0199a1b2c3d47e8f9a0b1c2d3e4f5a6b"}),
                         ("tenant_id", "tn_0199a1b2c3d47e8f9a0b1c2d3e4f5a6b"), ("market_id", "mkt_kenya"),
                         ("legal_entity_id", "le_0199a1b2c3d47e8f"), ("target_capability", "commerce.catalog")):
        rejects(schema, "resolutionRequest", {**request, field: value}, f"mapping resolution naming {field}")
    without_context = copy.deepcopy(request)
    del without_context["context_id"]
    rejects(schema, "resolutionRequest", without_context, "mapping resolution without a context")
    rejects(schema, "resolutionRequest", {**request, "target_engine_id": "baobab_trade"}, "snake_case target engine")

    response = example["resolution_response"]
    rejects(schema, "resolutionResponse", {**response, "target_canonical_entity_id": "0199a1b2-c3d4-7e8f-9a0b-1c2d3e4f5a6d"},
            "resolution naming both targets")
    neither = copy.deepcopy(response)
    del neither["external_reference_id"]
    rejects(schema, "resolutionResponse", neither, "resolution naming no target")
    for field in ("tenant_id", "context_id", "mapping_version"):
        missing = copy.deepcopy(response)
        del missing[field]
        rejects(schema, "resolutionResponse", missing, f"resolution without {field}")


def check_tenant_provisioning() -> None:
    example = json.loads((CP / "examples" / "tenant-provisioning.json").read_text())
    for key, schema, definition in (
            ("create_request", "provisioning-desired-state.schema.json", "TenantProvisioningCreateRequest"),
            ("desired_state", "provisioning-desired-state.schema.json", "ProvisioningDesiredState"),
            ("plan", "provisioning-plan.schema.json", "ProvisioningPlan"),
            ("approval_request", "approval-decision.schema.json", "ApprovalDecisionRequest"),
            ("approval", "approval-decision.schema.json", "ApprovalDecision"),
            ("provisioning", "tenant-provisioning.schema.json", "TenantProvisioning"),
            ("operation", "execution-operation.schema.json", "ExecutionOperation"),
            ("readiness", "tenant-provisioning.schema.json", "ProvisioningReadiness"),
            ("drift", "tenant-provisioning.schema.json", "ProvisioningDrift")):
        accepts(schema, definition, example[key], f"tenant-provisioning {key}")

    # Callers never supply how engines are wired (ADR-SHARED-015).
    create = example["create_request"]
    for field, value in (("manifest", {}), ("capability_grants", []), ("capability_bindings", []),
                         ("engine_instance", "ei_0199a1b2c3d47e8f"), ("tenant_id", "tn_0199a1b2c3d47e8f9a0b1c2d3e4f5a6b")):
        rejects("provisioning-desired-state.schema.json", "TenantProvisioningCreateRequest", {**create, field: value},
                f"provisioning create request naming {field}")
    desired = example["desired_state"]
    for field in ("capability_grants", "bindings", "engine_id", "engine_instance_id", "provider_key"):
        rejects("provisioning-desired-state.schema.json", "ProvisioningDesiredState", {**desired, field: "baobab-trade"},
                f"desired state naming {field}")
    without_provenance = copy.deepcopy(desired)
    del without_provenance["provenance"]
    rejects("provisioning-desired-state.schema.json", "ProvisioningDesiredState", without_provenance, "desired state without provenance")

    # The plan is canonical, digest-bound and names topology in ADR-SHARED-012 identifiers.
    plan = example["plan"]
    def with_step(**changes: object) -> dict:
        changed = copy.deepcopy(plan)
        step = changed["steps"][1]
        for key, value in changes.items():
            if key == "operation":
                step["operation"] = value
            else:
                step["resources"][key] = value
        return changed
    for label, changed in (("a UUID engine instance", with_step(engine_instance_id="0199a1b2-c3d4-7e8f-9a0b-1c2d3e4f5a6c")),
                           ("a snake_case engine", with_step(engine_id="baobab_trade")),
                           ("a provider-specific operation", with_step(operation="CALL_MEDUSA_API")),
                           ("a provider-specific resource", with_step(medusa_store_id="store_1"))):
        rejects("provisioning-plan.schema.json", "ProvisioningPlan", changed, f"plan step with {label}")
    for field in ("plan_digest", "base_revision", "impact_analysis", "risk_class"):
        missing = copy.deepcopy(plan)
        del missing[field]
        rejects("provisioning-plan.schema.json", "ProvisioningPlan", missing, f"plan without {field}")
    rejects("provisioning-plan.schema.json", "ProvisioningPlan", {**plan, "plan_digest": "abc123"}, "plan with an unqualified digest")
    rejects("provisioning-plan.schema.json", "ProvisioningPlan", {**plan, "approved": True}, "plan carrying its own approval")

    # Approval binds the exact plan; the approver is never a body field.
    request = example["approval_request"]
    without_digest = copy.deepcopy(request)
    del without_digest["plan_digest"]
    rejects("approval-decision.schema.json", "ApprovalDecisionRequest", without_digest, "approval without the plan digest")
    rejects("approval-decision.schema.json", "ApprovalDecisionRequest", {**request, "approved_by": "someone"}, "approval naming its approver")
    rejects("approval-decision.schema.json", "ApprovalDecisionRequest", {**request, "decision": "REJECTED"}, "rejection without a reason")
    approval = example["approval"]
    for outcome in ("REJECTED", "CHANGES_REQUESTED"):
        rejects("approval-decision.schema.json", "ApprovalDecision", {**approval, "decision": outcome}, f"recorded {outcome} without its reason")
        rejects("approval-decision.schema.json", "ApprovalDecision", {**approval, "decision": outcome, "reason": ""}, f"recorded {outcome} with an empty reason")
    accepts("approval-decision.schema.json", "ApprovalDecision", {**approval, "decision": "REJECTED", "reason": "Residency not met"}, "recorded rejection with its reason")

    # Three lifecycles stay distinct.
    operation = example["operation"]
    rejects("execution-operation.schema.json", "ExecutionOperation", {**operation, "status": "FAILED"}, "failed operation without a problem")
    rejects("execution-operation.schema.json", "ExecutionOperation", {**operation, "status": "ACTIVE"}, "operation in a tenant state")
    succeeded = {**operation, "status": "SUCCEEDED", "completed_at": "2026-09-27T09:20:00Z"}
    rejects("execution-operation.schema.json", "ExecutionOperation", succeeded, "succeeded operation without its result")
    result = {"resource_type": "TENANT_PROVISIONING", "resource_id": operation["subject"]["id"]}
    rejects("execution-operation.schema.json", "ExecutionOperation", {**succeeded, "result": result}, "succeeded operation without the resource's state")
    accepts("execution-operation.schema.json", "ExecutionOperation", {**succeeded, "result": {**result, "resource_state": "READY"}},
            "succeeded operation naming the resource's state")
    readiness = example["readiness"]
    rejects("tenant-provisioning.schema.json", "ProvisioningReadiness", {**readiness, "snapshots": []}, "evaluated readiness without snapshots")
    unknown = {key: value for key, value in readiness.items() if key != "evaluated_at"}
    accepts("tenant-provisioning.schema.json", "ProvisioningReadiness", {**unknown, "status": "UNKNOWN", "snapshots": []}, "unevaluated readiness")
    rejects("tenant-provisioning.schema.json", "TenantProvisioningReplanRequest", {"desired_state_version": 2}, "replan without a reason")
    rejects("tenant-provisioning.schema.json", "TenantProvisioningReplanRequest", {"reason": "stale", "manifest": {}}, "replan carrying a manifest")
    provisioning = example["provisioning"]
    rejects("tenant-provisioning.schema.json", "TenantProvisioning", {**provisioning, "state": "provisioning"}, "provisioning in the legacy coarse state")
    rejects("tenant-provisioning.schema.json", "TenantProvisioning", {**provisioning, "state": "RUNNING"}, "provisioning in an operation status")
    rejects("tenant-provisioning.schema.json", "TenantProvisioning", {**provisioning, "state": "BLOCKED", "blocking_reasons": []},
            "BLOCKED provisioning without reasons")

    lifecycle = yaml.safe_load((CP / "tenant-provisioning-lifecycle.yaml").read_text())
    states = set(json.loads((CP / "domain.schema.json").read_text())["$defs"]["tenantProvisioningState"]["enum"])
    if set(lifecycle["states"]) | set(lifecycle["terminal_states"]) != states:
        fail("tenant-provisioning-lifecycle.yaml states differ from tenantProvisioningState")
    for state, spec in lifecycle["states"].items():
        for command, target in (spec or {}).get("transitions", {}).items():
            if target not in states:
                fail(f"tenant-provisioning-lifecycle.yaml {state}.{command} targets unknown state {target}")
            if command == "apply" and state != "PLANNED":
                fail(f"tenant-provisioning-lifecycle.yaml applies from {state}; only a PLANNED provisioning is applied")
    # Every transition has a trigger, and every command is an operation (no dead-end state).
    openapi = yaml.safe_load((CP / "openapi.yaml").read_text())
    operation_ids = {op.get("operationId") for item in openapi["paths"].values() for op in item.values() if isinstance(op, dict)}
    commands, system = lifecycle["triggers"]["commands"], set(lifecycle["triggers"]["system"])
    if set(commands) & system:
        fail(f"tenant-provisioning-lifecycle.yaml transitions {sorted(set(commands) & system)} are both command and system")
    for transition, operation_id in commands.items():
        if operation_id not in operation_ids:
            fail(f"tenant-provisioning-lifecycle.yaml command {transition} names unknown operation {operation_id}")
    used = {command for spec in lifecycle["states"].values() for command in (spec or {}).get("transitions", {})}
    if used != set(commands) | system:
        fail(f"tenant-provisioning-lifecycle.yaml triggers differ from transitions: {sorted(used ^ (set(commands) | system))}")
    for terminal in lifecycle["terminal_states"]:
        if terminal in lifecycle["states"]:
            fail(f"tenant-provisioning-lifecycle.yaml terminal state {terminal} has transitions")
    legacy = set(json.loads((CP / "tenant-provisioning.schema.json").read_text())["$defs"]["legacyProvisioningState"]["enum"])
    if set(lifecycle["legacy_projection"]) != states or not set(lifecycle["legacy_projection"].values()) <= legacy:
        fail("tenant-provisioning-lifecycle.yaml legacy_projection must map every state to a legacy state")


def stateful_order_problems(plan: dict, sequence: list[str]) -> list[str]:
    """Why a STATEFUL_CUTOVER plan's cohorts could shift authority before
    their data moves: each sequence step must reach the one before it
    through depends_on, and the cohort's VALIDATE_COHORT must reach the last."""
    if plan["migration_mode"] != "STATEFUL_CUTOVER":
        return []
    steps = {step["step_id"]: step for step in plan["steps"]}

    def reaches(start: str, goal: str) -> bool:
        seen, frontier = set(), [start]
        while frontier:
            current = frontier.pop()
            for dependency in steps.get(current, {}).get("depends_on", []):
                if dependency == goal:
                    return True
                if dependency not in seen:
                    seen.add(dependency)
                    frontier.append(dependency)
        return False

    problems = []
    for cohort in plan["request"]["cohorts"]:
        key = cohort["cohort_key"]
        mine = [step for step in plan["steps"] if step["resources"].get("cohort_key") == key]
        chain = []
        for operation in sequence + ["VALIDATE_COHORT"]:
            found = [step["step_id"] for step in mine if step["operation"] == operation]
            if len(found) != 1:
                problems.append(f"cohort {key} has {len(found)} {operation} steps, not one")
                break
            chain.append(found[0])
        else:
            for before, after in zip(chain, chain[1:]):
                if not reaches(after, before):
                    problems.append(f"cohort {key}: {after} does not depend on {before}")
    return problems


def check_provider_migration() -> None:
    schema = "provider-migration.schema.json"
    example = json.loads((CP / "examples" / "provider-migration.json").read_text())
    for key, definition in (("request", "ProviderMigrationRequest"), ("preview", "ProviderMigrationPlan"),
                            ("plan", "ProviderMigrationPlan"), ("migration", "ProviderMigration")):
        accepts(schema, definition, example[key], f"provider-migration {key}")
    request = example["request"]

    # The mode decides the data strategy: stateless moves no data, stateful
    # moves it inside a cutover window, and dual write is never a strategy.
    stateless = {**request, "migration_mode": "STATELESS_REBIND", "data_strategy": "NONE"}
    stateless.pop("cutover_window")
    accepts(schema, "ProviderMigrationRequest", stateless, "stateless rebind without data or window")
    for label, changed in (
            ("stateless migration moving data", {**stateless, "data_strategy": "BULK_MIGRATE_THEN_CUTOVER"}),
            ("stateful migration moving no data", {**request, "data_strategy": "NONE"}),
            ("stateful migration without a cutover window", {k: v for k, v in request.items() if k != "cutover_window"}),
            ("a dual-write data strategy", {**request, "data_strategy": "DUAL_WRITE"}),
            ("a percentage cohort", {**request, "cohorts": [{"cohort_key": "tenth", "selector": {"percentage": 10}}]}),
            ("an empty cohort selector", {**request, "cohorts": [{"cohort_key": "none", "selector": {}}]}),
            ("no cohorts", {**request, "cohorts": []}),
            ("an owner email", {**request, "owners": ["ops@example.com"]}),
            # The Control Plane discovers what is affected; the caller never says.
            ("caller-supplied bindings", {**request, "binding_ids": ["cb_1"]}),
            ("a caller-supplied engine instance", {**request, "engine_instance_id": "ei_0199a1b2c3d47e8f"})):
        rejects(schema, "ProviderMigrationRequest", changed, f"migration request with {label}")

    plan = example["plan"]
    def with_step(**changes: object) -> dict:
        changed = copy.deepcopy(plan)
        step = changed["steps"][1]
        for key, value in changes.items():
            if key == "operation":
                step["operation"] = value
            else:
                step["resources"][key] = value
        return changed
    for label, changed in (("a provider-specific operation", with_step(operation="CALL_IDEMPIERE_API")),
                           ("a UUID engine instance", with_step(engine_instance_id="0199a1b2-c3d4-7e8f-9a0b-1c2d3e4f5a6c")),
                           ("a provider-specific resource", with_step(idempiere_client_id="11"))):
        rejects(schema, "ProviderMigrationPlan", changed, f"migration plan step with {label}")
    for field in ("plan_digest", "discovery", "impact_analysis", "risk_class"):
        missing = copy.deepcopy(plan)
        del missing[field]
        rejects(schema, "ProviderMigrationPlan", missing, f"migration plan without {field}")
    migration = example["migration"]
    rejects(schema, "ProviderMigration", {**migration, "provider_migration_id": "0199a1b2-c3d4-7e8f"}, "migration with a raw UUID id")
    rejects(schema, "ProviderMigration", {**migration, "stage": "CUTOVER"}, "migration with an unknown stage")

    # Semantic rules the schema cannot express.
    for key in ("preview", "plan"):
        document = example[key]
        if document["source_provider_key"] == document["target_provider_key"]:
            fail(f"provider-migration {key}: source and target provider are the same")
    if request["source_provider_key"] == request["target_provider_key"]:
        fail("provider-migration request: source and target provider are the same")
    open_cohorts = [i for i, cohort in enumerate(request["cohorts"]) if "selector" not in cohort]
    if open_cohorts and open_cohorts != [len(request["cohorts"]) - 1]:
        fail("provider-migration request: only the last cohort may omit its selector")
    keys = [cohort["cohort_key"] for cohort in request["cohorts"]]
    if len(keys) != len(set(keys)) or [c["cohort_key"] for c in plan["discovery"]["cohorts"]] != keys:
        fail("provider-migration plan: discovery must list the request's cohorts once each, in order")

    lifecycle = yaml.safe_load((CP / "provider-migration-lifecycle.yaml").read_text())
    stages = set(json.loads((CP / schema).read_text())["$defs"]["migrationStage"]["enum"])
    if set(lifecycle["states"]) | set(lifecycle["terminal_states"]) != stages:
        fail("provider-migration-lifecycle.yaml states differ from migrationStage")
    for stage, spec in lifecycle["states"].items():
        for command, target in (spec or {}).get("transitions", {}).items():
            if target not in stages:
                fail(f"provider-migration-lifecycle.yaml {stage}.{command} targets unknown stage {target}")
    if lifecycle["initial_state"] != "PLAN" or example["migration"]["stage"] != "PLAN":
        fail("a provider migration is created in PLAN")
    for terminal in lifecycle["terminal_states"]:
        if terminal in lifecycle["states"]:
            fail(f"provider-migration-lifecycle.yaml terminal stage {terminal} has transitions")
    reachable, frontier = {lifecycle["initial_state"]}, [lifecycle["initial_state"]]
    while frontier:
        for target in (lifecycle["states"].get(frontier.pop()) or {}).get("transitions", {}).values():
            if target not in reachable:
                reachable.add(target)
                frontier.append(target)
    if not set(lifecycle["terminal_states"]) <= reachable:
        fail(f"provider-migration-lifecycle.yaml cannot reach {sorted(set(lifecycle['terminal_states']) - reachable)}")

    # Exactly one authoritative writer: in every stateful cohort each step
    # of the sequence depends, directly or transitively, on the one before,
    # so no executor that follows depends_on can shift authority before the
    # cohort's data is frozen, migrated and reconciled.
    operations = set(json.loads((CP / schema).read_text())["$defs"]["migrationOperation"]["enum"])
    sequence = lifecycle["stateful_cohort_sequence"]
    if not set(sequence) <= operations:
        fail("provider-migration-lifecycle.yaml stateful_cohort_sequence names unknown operations")
    for problem in stateful_order_problems(plan, sequence):
        fail(f"provider-migration plan: {problem}")
    broken = copy.deepcopy(plan)
    shift = next(s for s in broken["steps"] if s["operation"] == "SHIFT_COHORT")
    freeze = next(s for s in broken["steps"] if s["operation"] == "FREEZE_COHORT_WRITES"
                  and s["resources"].get("cohort_key") == shift["resources"].get("cohort_key"))
    shift["depends_on"] = [freeze["step_id"]]
    if not stateful_order_problems(broken, sequence):
        fail("the stateful order check accepts a shift that depends only on the freeze")

    # The approved plan fixes every binding's target instance: each
    # CREATE_MIGRATION_BINDING step names its bindings and their one
    # instance, no binding is named twice, and an unblocked plan moves
    # every binding discovery found.
    for key in ("preview", "plan"):
        document = example[key]
        named: list[str] = []
        for step in document["steps"]:
            if step["operation"] != "CREATE_MIGRATION_BINDING":
                continue
            ids = step["resources"]["binding_ids"]
            if len(ids) != step["resources"]["binding_count"]:
                fail(f"provider-migration {key}: {step['step_id']} names {len(ids)} bindings but counts {step['resources']['binding_count']}")
            named.extend(ids)
        if len(named) != len(set(named)):
            fail(f"provider-migration {key}: a binding moves to more than one target instance")
        if not document["blockers"] and len(named) != document["discovery"]["binding_count"]:
            fail(f"provider-migration {key}: its steps move {len(named)} of {document['discovery']['binding_count']} discovered bindings")
    # Each fixture removes exactly one field from a fresh copy, so each
    # requirement is tested on its own.
    for field in ("binding_ids", "engine_instance_id", "binding_count", "capability_key"):
        missing = copy.deepcopy(plan)
        bind = next(s for s in missing["steps"] if s["operation"] == "CREATE_MIGRATION_BINDING")
        del bind["resources"][field]
        rejects(schema, "ProviderMigrationPlan", missing, f"a migration binding step without {field}")

    # A plan embeds the request it executes; the fields it repeats agree.
    for key in ("preview", "plan"):
        document = example[key]
        for field in ("source_provider_key", "target_provider_key", "migration_mode"):
            if document[field] != document["request"][field]:
                fail(f"provider-migration {key}: {field} differs from its request's")
    without_request = copy.deepcopy(plan)
    del without_request["request"]
    rejects(schema, "ProviderMigrationPlan", without_request, "migration plan without its request")
    rejects(schema, "ProviderMigration", {**migration, "stage": "DISCOVER"}, "a migration in DISCOVER, which is only the preview")

    registry = yaml.safe_load((CONTRACTS / "authorization" / "v1" / "reason-code-registry.yaml").read_text())
    registered = {entry["code"] for entry in registry["reason_codes"] if entry["category"] == "provider_migration_blocker"}
    if set(lifecycle["blocking_codes"]) != registered:
        fail(f"provider-migration-lifecycle.yaml blocking_codes differ from provider_migration_blocker codes: "
             f"{sorted(set(lifecycle['blocking_codes']) ^ registered)}")
    if set(lifecycle["warning_codes"]) & registered:
        fail("a provider migration warning code is registered as a blocker")
    for key in ("preview", "plan"):
        for finding in example[key]["blockers"]:
            if finding["code"] not in lifecycle["blocking_codes"]:
                fail(f"provider-migration {key}: blocker {finding['code']} is not a provider migration blocking code")
        for finding in example[key]["warnings"]:
            if finding["code"] not in lifecycle["warning_codes"]:
                fail(f"provider-migration {key}: warning {finding['code']} is not a provider migration warning code")


def check_migration_execution() -> None:
    """ADR-SHARED-016: approval, stage commands and engine migration tasks."""
    schema = "provider-migration.schema.json"
    tasks = "engine-migration-task.schema.json"
    example = json.loads((CP / "examples" / "provider-migration.json").read_text())
    accepts("approval-decision.schema.json", "ApprovalDecision", example["approval"], "provider-migration approval")
    accepts(schema, "ProviderMigration", example["advancing"], "provider-migration advancing")
    accepts("execution-operation.schema.json", "ExecutionOperation", example["operation"], "provider-migration operation")
    for key in ("advance_request", "rollback_request"):
        accepts(schema, "ProviderMigrationAdvanceRequest", example[key], f"provider-migration {key}")
    advance = example["advance_request"]
    for label, changed in (("named steps", {**advance, "steps": ["internal-canary-shift-cohort"]}),
                           ("an unknown transition", {**advance, "transition": "cutover"}),
                           ("replan, which is not an advance", {**advance, "transition": "replan"}),
                           ("a caller-supplied approval", {**advance, "approval_id": "apd_0199a1b2c3d47ec1"})):
        rejects(schema, "ProviderMigrationAdvanceRequest", changed, f"an advance with {label}")
    for transition in ("cancel", "roll_back"):
        rejects(schema, "ProviderMigrationAdvanceRequest", {"transition": transition}, f"a {transition} without a reason")
    approval, migration = example["approval"], example["migration"]
    if (approval["subject_id"], approval["plan_id"], approval["plan_version"], approval["plan_digest"]) != \
            (migration["provider_migration_id"], migration["plan_id"], migration["plan_version"], migration["plan_digest"]):
        fail("provider-migration approval does not bind the migration's current plan")
    if approval["decided_by"] == migration["created_by"]:
        fail("provider-migration approval is decided by the migration's creator")
    operation = example["operation"]
    if operation["operation_type"] != "PROVIDER_MIGRATION_ADVANCE" or operation["subject"]["type"] != "PROVIDER_MIGRATION" \
            or example["advancing"]["operation_id"] != operation["operation_id"]:
        fail("a provider migration advances by a PROVIDER_MIGRATION_ADVANCE operation on the migration")

    # The lifecycle's execution rules name real transitions, operations,
    # roles and strategies, and every advance runs the stateful sequence in
    # order.
    lifecycle = yaml.safe_load((CP / "provider-migration-lifecycle.yaml").read_text())
    defs = json.loads((CP / schema).read_text())["$defs"]
    task_defs = json.loads((CP / tasks).read_text())["$defs"]
    operations = set(defs["migrationOperation"]["enum"])
    transitions = {name for spec in lifecycle["states"].values() for name in (spec or {}).get("transitions", {})}
    advance_enum = set(defs["migrationTransition"]["enum"])
    if advance_enum != transitions - {"replan"}:
        fail(f"migrationTransition differs from the lifecycle's command transitions: {sorted(advance_enum ^ (transitions - {'replan'}))}")
    compensating = {"cancel", "roll_back"}
    if set(lifecycle["stage_steps"]) != advance_enum - compensating:
        fail(f"stage_steps differ from the forward transitions: {sorted(set(lifecycle['stage_steps']) ^ (advance_enum - compensating))}")
    for transition, spec in lifecycle["stage_steps"].items():
        if spec["scope"] not in {"MIGRATION", "FIRST_COHORT", "NEXT_COHORT", "CURRENT_COHORT"}:
            fail(f"stage_steps.{transition} has an unknown scope {spec['scope']}")
        if not set(spec["operations"]) <= operations - {"REMOVE_MIGRATION_BINDING"}:
            fail(f"stage_steps.{transition} names operations that are not plan operations")
    sequence = lifecycle["stateful_cohort_sequence"]
    for transition in ("canary", "shift"):
        ops = lifecycle["stage_steps"][transition]["operations"]
        if [op for op in ops if op in sequence] != sequence:
            fail(f"stage_steps.{transition} does not run the stateful cohort sequence in order")
    if set(lifecycle["engine_steps"]) != set(task_defs["taskOperation"]["enum"]):
        fail("engine_steps differ from the engine migration task operations")
    roles = set(task_defs["taskRole"]["enum"])
    for op, spec in lifecycle["engine_steps"].items():
        if set(spec) != {"forward", "reverse"} or not set(spec["forward"]) | set(spec["reverse"]) <= roles:
            fail(f"engine_steps.{op} must assign forward and reverse to known roles")
    # One writer at a time: the freeze and the unfreeze are on opposite sides.
    engine = lifecycle["engine_steps"]
    if engine["FREEZE_COHORT_WRITES"]["forward"] != ["SOURCE"] or engine["UNFREEZE_COHORT_WRITES"]["forward"] != ["TARGET"] \
            or engine["FREEZE_COHORT_WRITES"]["reverse"] != ["TARGET"] or engine["UNFREEZE_COHORT_WRITES"]["reverse"] != ["SOURCE"]:
        fail("engine_steps must freeze the side losing authority and unfreeze the side gaining it")
    if set(engine["RECONCILE_COHORT_DATA"]["forward"]) != roles or set(engine["RECONCILE_COHORT_DATA"]["reverse"]) != roles:
        fail("reconciliation must be reported by both sides")
    if set(lifecycle["rollback_steps"]) != set(defs["rollbackStrategy"]["enum"]):
        fail("rollback_steps differ from rollbackStrategy")
    for strategy, ops in lifecycle["rollback_steps"].items():
        if not set(ops) <= operations:
            fail(f"rollback_steps.{strategy} names unknown operations")
    if lifecycle["rollback_steps"]["FORWARD_FIX_ONLY"]:
        fail("FORWARD_FIX_ONLY moves no cohort back")
    # A frozen cohort is always released by the side it was frozen on.
    release = lifecycle["rollback_release"]
    if release != ["UNFREEZE_COHORT_WRITES"] or engine["UNFREEZE_COHORT_WRITES"]["reverse"] != ["SOURCE"]:
        fail("rollback_release must reverse the freeze on the source, which is still authoritative")
    if not set(lifecycle["compensation"]["cancel"]) <= operations:
        fail("compensation.cancel names unknown operations")
    for key in ("preview", "plan"):
        if any(step["operation"] == "REMOVE_MIGRATION_BINDING" for step in example[key]["steps"]):
            fail(f"provider-migration {key}: REMOVE_MIGRATION_BINDING is compensation only")
    if not (isinstance(lifecycle["task_lease_seconds"], int) and 0 < lifecycle["task_lease_seconds"] <= 3600):
        fail("task_lease_seconds must be between 1 and 3600")

    # Engine migration tasks.
    task_example = json.loads((CP / "examples" / "engine-migration-task.json").read_text())
    for key in ("pending", "claimed", "succeeded", "freeze_succeeded", "failed"):
        accepts(tasks, "EngineMigrationTask", task_example[key], f"engine migration task {key}")
        task = task_example[key]
        if task["role"] not in engine[task["operation"]][task["direction"].lower()]:
            fail(f"engine migration task {key}: {task['operation']} {task['direction']} is not assigned to {task['role']}")
        if task["provider_migration_id"] != migration["provider_migration_id"]:
            fail(f"engine migration task {key} belongs to another migration")
    accepts(tasks, "EngineMigrationTaskPage", task_example["page"], "engine migration task page")
    for key in ("report_succeeded", "report_failed"):
        accepts(tasks, "EngineMigrationTaskReport", task_example[key], f"engine migration task {key}")
    registry = yaml.safe_load((CONTRACTS / "authorization" / "v1" / "reason-code-registry.yaml").read_text())
    failures = {entry["code"] for entry in registry["reason_codes"] if entry["category"] == "provider_migration_task_failure"}
    for code in (task_example["failed"]["result"]["reason_code"], task_example["report_failed"]["reason_code"]):
        if code not in failures:
            fail(f"engine migration task failure {code} is not a provider_migration_task_failure code")
    for code in ("MIGRATION_RECONCILIATION_MISMATCH", "MIGRATION_TASK_TIMEOUT"):
        if code not in failures:
            fail(f"ADR-SHARED-016 needs the provider_migration_task_failure code {code}")
    claimed, succeeded, failed = task_example["claimed"], task_example["succeeded"], task_example["failed"]
    for label, changed in (
            ("a migrate task without its counterpart", {k: v for k, v in claimed.items() if k != "counterpart"}),
            ("a claimed task without its lease", {k: v for k, v in claimed.items() if k != "lease_expires_at"}),
            ("a claimed task without its claimant", {k: v for k, v in claimed.items() if k != "claimed_by"}),
            ("a failed task without a reason code", {**failed, "result": {"detail": "failed"}}),
            ("a reconciled task without its digest", {**succeeded, "result": {"record_count": 1}}),
            ("a reported task without a result", {k: v for k, v in succeeded.items() if k != "result"}),
            ("a task carrying an endpoint", {**claimed, "counterpart": {**claimed["counterpart"], "endpoint": "https://erp.internal"}}),
            ("a task carrying a credential", {**claimed, "credentials": {"token": "x"}}),
            ("a task carrying business data", {**succeeded, "result": {**succeeded["result"], "records": [{"invoice": 1}]}}),
            ("a provider-specific operation", {**claimed, "operation": "RUN_IDEMPIERE_EXPORT"}),
            ("a local operation as a task", {**claimed, "operation": "SHIFT_COHORT"}),
            ("a UUID engine instance", {**claimed, "engine_instance_id": "0199a1b2-c3d4-7e8f-9a0b-1c2d3e4f5a6c"}),
            ("an overlong detail", {**failed, "result": {**failed["result"], "detail": "x" * 501}}),
            ("a malformed digest", {**succeeded, "result": {**succeeded["result"], "content_digest": "md5:abc"}})):
        rejects(tasks, "EngineMigrationTask", changed, f"engine migration task with {label}")
    report = task_example["report_succeeded"]
    for label, changed in (("its task id", {**report, "task_id": claimed["task_id"]}),
                           ("its engine instance", {**report, "engine_instance_id": claimed["engine_instance_id"]}),
                           ("a status other than an outcome", {**report, "outcome": "CLAIMED"})):
        rejects(tasks, "EngineMigrationTaskReport", changed, f"a task report naming {label}")
    rejects(tasks, "EngineMigrationTaskReport", {"outcome": "FAILED"}, "a FAILED report without a reason code")


def check_changeset() -> None:
    schema = "changeset.schema.json"
    example = json.loads((CP / "examples" / "changeset.json").read_text())
    for key, file, definition in (
            ("create_request", schema, "ChangesetCreateRequest"), ("draft", schema, "Changeset"),
            ("blocked", schema, "Changeset"), ("awaiting_approval", schema, "Changeset"), ("plan", schema, "ChangesetPlan"),
            ("approval_request", "approval-decision.schema.json", "ApprovalDecisionRequest"),
            ("approval", "approval-decision.schema.json", "ApprovalDecision"),
            ("operation", "execution-operation.schema.json", "ExecutionOperation"),
            ("completed", schema, "Changeset"), ("outcome", schema, "ChangeOutcome")):
        accepts(file, definition, example[key], f"changeset {key}")

    # The caller states intent; type, scope, source and requester are derived.
    create = example["create_request"]
    for field, value in (("changeset_type", "SUSPEND"), ("source", "API"), ("requested_by", "prn_someone"),
                         ("target_scope", {"level": "PLATFORM"}), ("risk_class", "LOW"), ("state", "APPROVED")):
        rejects(schema, "ChangesetCreateRequest", {**create, field: value}, f"changeset create request naming {field}")
    for label, change in (("an unknown kind", {"kind": "TENANT_DELETION", "tenant_id": create["desired_change"]["tenant_id"]}),
                          ("a provider command", {**create["desired_change"], "medusa_store_id": "store_1"}),
                          ("no tenant", {"kind": "TENANT_SUSPENSION"})):
        rejects(schema, "ChangesetCreateRequest", {**create, "desired_change": change}, f"changeset desired change with {label}")

    # State requires its evidence.
    draft, awaiting, completed = example["draft"], example["awaiting_approval"], example["completed"]
    rejects(schema, "Changeset", {**draft, "state": "BLOCKED"}, "a BLOCKED changeset without blocking reasons")
    rejects(schema, "Changeset", {k: v for k, v in awaiting.items() if k != "current_plan"}, "a changeset awaiting approval without a plan")
    rejects(schema, "Changeset", {k: v for k, v in completed.items() if k != "operation_id"}, "a COMPLETED changeset without its operation")
    rejects(schema, "Changeset", {k: v for k, v in completed.items() if k != "approval_id"}, "a COMPLETED changeset without its approval")
    plan = example["plan"]
    changed = copy.deepcopy(plan)
    changed["steps"][0]["operation"] = "CALL_MEDUSA_API"
    rejects(schema, "ChangesetPlan", changed, "a changeset plan step with a provider-specific operation")
    rejects(schema, "ChangesetPlan", {k: v for k, v in plan.items() if k != "desired_change"}, "a changeset plan without its desired change")
    outcome = example["outcome"]
    rejects(schema, "ChangeOutcome", {k: v for k, v in outcome.items() if k != "applied_plan_digest"}, "a COMPLETED outcome without the applied plan")
    rejects(schema, "ChangeOutcome", {**outcome, "final_state": "APPLYING"}, "an outcome of a changeset that has not ended")

    # The lifecycle: states match the schema, no state is a dead end, and
    # every command is a real operation.
    lifecycle = yaml.safe_load((CP / "changeset-lifecycle.yaml").read_text())
    defs = json.loads((CP / schema).read_text())["$defs"]
    states = set(defs["changesetState"]["enum"])
    terminals = set(lifecycle["terminal_states"])
    if set(lifecycle["states"]) | terminals != states:
        fail(f"changeset-lifecycle.yaml states differ from changesetState: {sorted((set(lifecycle['states']) | terminals) ^ states)}")
    graph = {state: set((spec or {}).get("transitions", {}).values()) for state, spec in lifecycle["states"].items()}
    for state, targets in graph.items():
        if state in terminals:
            fail(f"changeset-lifecycle.yaml terminal state {state} has transitions")
        for target in targets - states:
            fail(f"changeset-lifecycle.yaml {state} targets unknown state {target}")

    def reach(start: str) -> set[str]:
        seen, frontier = {start}, [start]
        while frontier:
            for target in graph.get(frontier.pop(), set()):
                if target not in seen:
                    seen.add(target)
                    frontier.append(target)
        return seen
    if not terminals <= reach(lifecycle["initial_state"]) or not states <= reach(lifecycle["initial_state"]):
        fail(f"changeset-lifecycle.yaml leaves states unreachable: {sorted(states - reach(lifecycle['initial_state']))}")
    for state in graph:
        if not reach(state) & terminals:
            fail(f"changeset-lifecycle.yaml state {state} can never end")
    commands, system = lifecycle["triggers"]["commands"], set(lifecycle["triggers"]["system"])
    used = {name for spec in lifecycle["states"].values() for name in (spec or {}).get("transitions", {})}
    if set(commands) & system or used != set(commands) | system:
        fail(f"changeset-lifecycle.yaml triggers differ from transitions: {sorted(used ^ (set(commands) | system))}")
    openapi = yaml.safe_load((CP / "openapi.yaml").read_text())
    operation_ids = {op.get("operationId") for item in openapi["paths"].values() for op in item.values() if isinstance(op, dict)}
    for command, operation_id in commands.items():
        if operation_id not in operation_ids:
            fail(f"changeset-lifecycle.yaml command {command} names unknown operation {operation_id}")

    # Change kinds: one per desiredChange branch, a real type, real
    # operations and tenant statuses; the example plan runs its kind's steps.
    kinds = lifecycle["change_kinds"]
    branch_kinds = {defs[ref["$ref"].split("/")[-1]]["properties"]["kind"]["const"] for ref in defs["desiredChange"]["oneOf"]}
    if set(kinds) != branch_kinds:
        fail(f"changeset-lifecycle.yaml change_kinds differ from desiredChange: {sorted(set(kinds) ^ branch_kinds)}")
    # Each kind's statuses are in its own target's lifecycle vocabulary, and
    # an approval_scope is a registered scope.
    target_statuses = {
        "TENANT": set(json.loads((CP / "tenant.schema.json").read_text())["$defs"]["lifecycleStatus"]["enum"]),
        "MARKET": set(json.loads((CP / "market.schema.json").read_text())["$defs"]["market"]["properties"]["status"]["enum"]),
        "MAPPING": set(json.loads((CP / "domain.schema.json").read_text())["$defs"]["mappingStatus"]["enum"]),
    }
    registered_scopes = {entry["name"] for entry in yaml.safe_load(
        (CONTRACTS / "authorization" / "v1" / "scope-registry.yaml").read_text())["scopes"]}
    for kind, spec in kinds.items():
        if spec["changeset_type"] not in defs["changesetType"]["enum"]:
            fail(f"change kind {kind} derives unknown type {spec['changeset_type']}")
        if not set(spec["operations"]) <= set(defs["changesetOperation"]["enum"]):
            fail(f"change kind {kind} names unknown operations")
        statuses = target_statuses.get(spec.get("target"))
        if statuses is None:
            fail(f"change kind {kind} names unknown target {spec.get('target')!r}")
        elif not set(spec["from_status"]) | {spec["to_status"]} <= statuses:
            fail(f"change kind {kind} names statuses its {spec['target']} lifecycle lacks")
        if "approval_scope" in spec and spec["approval_scope"] not in registered_scopes:
            fail(f"change kind {kind} names unregistered approval_scope {spec['approval_scope']}")
    # The schema itself binds every plan to its kind's type and exact
    # operations, not only the example: a branch per kind, matching the
    # lifecycle, and a crossed plan is rejected.
    schema_branches = {}
    for branch in defs["ChangesetPlan"]["allOf"][1:]:
        kind_const = branch["if"]["properties"]["desired_change"]["properties"]["kind"]["const"]
        then = branch["then"]["properties"]
        schema_branches[kind_const] = (then["changeset_type"]["const"],
                                       [item["properties"]["operation"]["const"] for item in then["steps"]["prefixItems"]],
                                       then["steps"]["maxItems"])
    for kind_name, spec in kinds.items():
        if schema_branches.get(kind_name) != (spec["changeset_type"], spec["operations"], len(spec["operations"])):
            fail(f"ChangesetPlan does not bind {kind_name} to its type and operations: {schema_branches.get(kind_name)}")
    crossed = copy.deepcopy(plan)
    crossed["steps"][0]["operation"] = "REINSTATE_TENANT"
    rejects(schema, "ChangesetPlan", crossed, "a suspension plan that reinstates")
    extra = copy.deepcopy(plan)
    extra["steps"].append({**plan["steps"][0], "step_id": "suspend-again"})
    rejects(schema, "ChangesetPlan", extra, "a plan with a step its kind does not run")
    rejects(schema, "ChangesetPlan", {**plan, "changeset_type": "REINSTATE"}, "a suspension plan typed REINSTATE")
    rejects(schema, "Changeset", {**draft, "changeset_type": "REINSTATE"}, "a suspension changeset typed REINSTATE")
    compensated = {k: v for k, v in completed.items() if k != "operation_id"}
    rejects(schema, "Changeset", {**compensated, "state": "COMPENSATED"}, "a COMPENSATED changeset without its operation")

    kind = kinds[plan["desired_change"]["kind"]]
    if [step["operation"] for step in plan["steps"]] != kind["operations"] or plan["changeset_type"] != kind["changeset_type"] \
            or draft["changeset_type"] != kind["changeset_type"]:
        fail("the example changeset's plan does not run its change kind's operations and type")
    # Market and mapping activation: optional governed paths beside the
    # direct activate routes. Each plan runs its own kind and touches only
    # its own kind of resource, in that resource's status vocabulary.
    for key, target_key, foreign in (("market_activation_plan", "market_id", "mapping_id"),
                                     ("mapping_activation_plan", "mapping_id", "market_id")):
        activation = example[key]
        accepts(schema, "ChangesetPlan", activation, f"changeset {key}")
        spec = kinds[activation["desired_change"]["kind"]]
        if [step["operation"] for step in activation["steps"]] != spec["operations"] \
                or activation["changeset_type"] != spec["changeset_type"] or "approval_scope" not in spec:
            fail(f"changeset {key} does not run its change kind's operations and type, or its kind has no approval_scope")
        other = example["mapping_activation_plan" if key == "market_activation_plan" else "market_activation_plan"]
        rejects(schema, "ChangesetPlan", {**activation, "steps": other["steps"]}, f"a {key} running the other kind's steps")
        rejects(schema, "ChangesetPlan", {**activation, "changeset_type": "SUSPEND"}, f"a {key} typed SUSPEND")
        wrong = copy.deepcopy(activation)
        wrong["steps"][0]["resources"][foreign] = wrong["steps"][0]["resources"].pop(target_key)
        wrong["steps"][0]["resources"]["tenant_id"] = plan["desired_change"]["tenant_id"]
        rejects(schema, "ChangesetPlan", wrong, f"a {key} step naming two resources")
        lowered = copy.deepcopy(activation)
        lowered["steps"][0]["resources"]["to_status"] = "active"
        rejects(schema, "ChangesetPlan", lowered, f"a {key} step in the tenant status vocabulary")
        rejects(schema, "ChangesetCreateRequest",
                {**create, "desired_change": {**activation["desired_change"], "verified": True}},
                f"a {key} desired change with an extra property")
        # Every step acts on the desired change's own resource: the schema
        # requires the kind's resource, the example names the same id.
        for index in range(len(activation["steps"])):
            elsewhere = copy.deepcopy(activation)
            resources = elsewhere["steps"][index]["resources"]
            resources.pop(target_key)
            resources[foreign] = other["desired_change"][foreign]
            resources.pop("target_revision", None)
            resources["from_status"] = resources.get("from_status") and "VALIDATED"
            resources = {k: v for k, v in resources.items() if v is not None}
            elsewhere["steps"][index]["resources"] = resources
            rejects(schema, "ChangesetPlan", elsewhere, f"a {key} step {index} acting on another kind of resource")
            untargeted = copy.deepcopy(activation)
            untargeted["steps"][index]["resources"] = {"to_status": "ACTIVE"}
            rejects(schema, "ChangesetPlan", untargeted, f"a {key} step {index} naming no resource")
        for step in activation["steps"]:
            if step["resources"][target_key] != activation["desired_change"][target_key]:
                fail(f"changeset {key}: step {step['step_id']} acts on another {target_key} than its desired change")

    # Tenant step resources keep their v1 shape: no resource at all, or
    # statuses alone, stay valid tenant steps.
    for resources in ({}, {"to_status": "suspended"}, {"from_status": "active", "to_status": "suspended"}):
        compatible = copy.deepcopy(plan)
        compatible["steps"][1]["resources"] = resources
        accepts(schema, "ChangesetPlan", compatible, f"a v1 tenant step with resources {resources}")
    for step in plan["steps"][1:]:
        if not step["depends_on"]:
            fail(f"changeset plan step {step['step_id']} depends on nothing; a kind's operations run in order")

    registry = yaml.safe_load((CONTRACTS / "authorization" / "v1" / "reason-code-registry.yaml").read_text())
    registered = {entry["code"] for entry in registry["reason_codes"] if entry["category"] == "changeset_blocker"}
    if set(lifecycle["blocking_codes"]) != registered:
        fail(f"changeset-lifecycle.yaml blocking_codes differ from changeset_blocker codes: {sorted(set(lifecycle['blocking_codes']) ^ registered)}")
    for key in ("blocked", "plan"):
        for finding in example[key].get("blocking_reasons", []) + example[key].get("blockers", []):
            if finding["code"] not in registered:
                fail(f"changeset {key}: {finding['code']} is not a changeset_blocker code")
    if example["approval"]["subject_type"] != "CHANGESET" or example["operation"]["operation_type"] != "CHANGESET_APPLY":
        fail("a changeset's approval and operation name the CHANGESET subject and CHANGESET_APPLY")


def market_findings(market: dict, known_markets: set[str]) -> list[str]:
    """The market-lifecycle.yaml validation rules, evaluated as the Control Plane must.

    A list that is supplied constrains even when empty; absent (or null)
    does not. Times are compared as instants, never as strings."""
    def supplied(field: str) -> bool:
        return market.get(field) is not None

    def instant(value: str) -> datetime:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))

    codes = []
    countries = market.get("countries") or []
    if not market.get("default_country") and not countries:
        codes.append("MARKET_COUNTRY_REQUIRED")
    if market.get("default_country") and supplied("countries") and market["default_country"] not in countries:
        codes.append("MARKET_COUNTRY_NOT_LISTED")
    if not market.get("default_currency"):
        codes.append("MARKET_CURRENCY_REQUIRED")
    elif supplied("allowed_currencies") and market["default_currency"] not in market["allowed_currencies"]:
        codes.append("MARKET_CURRENCY_NOT_ALLOWED")
    if not market.get("default_locale"):
        codes.append("MARKET_LOCALE_REQUIRED")
    elif supplied("supported_locales") and market["default_locale"] not in market["supported_locales"]:
        codes.append("MARKET_LOCALE_NOT_SUPPORTED")
    if not market.get("timezone"):
        codes.append("MARKET_TIMEZONE_REQUIRED")
    if not market.get("effective_from"):
        codes.append("MARKET_EFFECTIVE_FROM_REQUIRED")
    elif market.get("effective_to") and instant(market["effective_to"]) <= instant(market["effective_from"]):
        codes.append("MARKET_EFFECTIVE_WINDOW_INVALID")
    parent = market.get("parent_market_id")
    if parent and (parent == market.get("market_id") or parent not in known_markets):
        codes.append("MARKET_PARENT_UNKNOWN")
    return codes


def check_market() -> None:
    schema = "market.schema.json"
    example = json.loads((CP / "examples" / "market.json").read_text())
    for key, definition in (("create_request", "MarketCreateRequest"), ("draft", "market"), ("update_request", "MarketUpdateRequest"),
                            ("validated", "market"), ("activation_request", "MarketActivationRequest"), ("active", "market")):
        accepts(schema, definition, example[key], f"market {key}")

    # The lifecycle: DRAFT and VALIDATED follow validation; only activation is
    # a decision, and it is made by someone other than the maker.
    lifecycle = yaml.safe_load((CP / "market-lifecycle.yaml").read_text())
    statuses = set(json.loads((CP / schema).read_text())["$defs"]["market"]["properties"]["status"]["enum"])
    # Participation is by country, derived from the registry.
    participation = lifecycle["participation"]
    market_properties = json.loads((CP / schema).read_text())["$defs"]["market"]["properties"]
    if participation["key"] != "country" or participation["covered_by"] != ["default_country", "countries"] \
            or not set(participation["covered_by"]) <= set(market_properties) or participation["primary"] != participation["covered_by"]:
        fail("market-lifecycle.yaml participation must cover a country through default_country, then countries")
    if not participation["available_statuses"] or not set(participation["available_statuses"]) <= statuses \
            or "DRAFT" in participation["available_statuses"] or "VALIDATED" in participation["available_statuses"]:
        fail("market-lifecycle.yaml participation is available only from activated statuses")
    onboarding = json.loads((CONTRACTS / "admission" / "v1" / "onboarding.schema.json").read_text())["$defs"]
    if not onboarding["marketParticipation"]["properties"]["market"]["$ref"].endswith("#/$defs/countryCode"):
        fail("participation is keyed by country: marketParticipation.market must be a countryCode")
    for t in lifecycle["transitions"]:
        if t["from"] not in statuses or t["to"] not in statuses:
            fail(f"market-lifecycle.yaml: {t['command']} {t['from']} -> {t['to']} uses an unknown status")
        if t["from"] in lifecycle["terminal"]:
            fail(f"market-lifecycle.yaml: terminal {t['from']} has an exit")
    served = {(t["command"], t["from"], t["to"], t["actor"]) for t in lifecycle["transitions"] if t["served"]}
    if served != {("validate", "DRAFT", "VALIDATED", "PLATFORM"), ("invalidate", "VALIDATED", "DRAFT", "PLATFORM"),
                  ("activate", "VALIDATED", "ACTIVE", "APPROVER")}:
        fail(f"market-lifecycle.yaml: the served transitions must be validate, invalidate and activate, not {sorted(served)}")
    if set(lifecycle["editable"]) != {"DRAFT", "VALIDATED"} or lifecycle["initial"] != "DRAFT":
        fail("market-lifecycle.yaml: a market starts DRAFT and only DRAFT and VALIDATED markets are editable")
    rule_codes = [r["code"] for r in lifecycle["validation_rules"]]
    registry = yaml.safe_load((CONTRACTS / "authorization" / "v1" / "reason-code-registry.yaml").read_text())
    registered = {e["code"] for e in registry["reason_codes"] if e["category"] == "market_validation"}
    if set(rule_codes) != registered:
        fail(f"market_validation reason codes {sorted(registered)} differ from the lifecycle rules {sorted(rule_codes)}")

    # Findings are exactly what the rules compute, and status follows them.
    known = {example["draft"]["market_id"]}
    for key in ("draft", "validated", "active"):
        market = example[key]
        computed = market_findings(market, known)
        listed = [f["code"] for f in market.get("validation_findings", [])]
        if key == "draft" and (market["status"] != "DRAFT" or sorted(computed) != sorted(listed) or not computed):
            fail(f"market {key}: its findings {listed} are not the rules' findings {computed}")
        if key != "draft" and (computed or listed):
            fail(f"market {key} is {market['status']} but the rules find {computed}")
    merged = {**example["draft"], **example["update_request"]}
    if market_findings(merged, known):
        fail("market update_request does not make the draft valid")
    active = example["active"]
    if active["activated_by"] in (example["validated"]["created_by"], example["validated"].get("updated_by")):
        fail("market active: activated by its maker")

    # The caller never states status, identity or audit fields, nor the approver.
    create = example["create_request"]
    for field, value in (("status", "ACTIVE"), ("market_id", "mkt_chosen"), ("created_by", "prn_x"), ("revision", 7),
                         ("activated_by", "prn_x"), ("validation_findings", [])):
        rejects(schema, "MarketCreateRequest", {**create, field: value}, f"market create request naming {field}")
    for field, value in (("canonical_key", "za.retail"), ("owner_tenant_id", "tn_other1"), ("status", "VALIDATED")):
        rejects(schema, "MarketUpdateRequest", {field: value}, f"market update request changing {field}")
    rejects(schema, "MarketUpdateRequest", {}, "an empty market update")
    rejects(schema, "MarketActivationRequest", {"approved_by": "prn_thandi"}, "market activation naming its approver")
    rejects(schema, "market", {k: v for k, v in active.items() if k != "activated_by"}, "an ACTIVE market without its activator")
    rejects(schema, "market", {**example["validated"], "validation_findings": example["draft"]["validation_findings"]},
            "a VALIDATED market with validation findings")
    rejects(schema, "market", {**example["draft"], "validation_findings": []}, "a DRAFT market without findings")
    rejects(schema, "market", {k: v for k, v in example["draft"].items() if k != "validation_findings"},
            "a DRAFT market that omits its findings")

    # The rules themselves: supplied lists constrain even when empty, and
    # times are instants.
    valid = {**example["draft"], **example["update_request"]}
    for label, change, code in (
            ("an empty currency allow-list", {"allowed_currencies": []}, "MARKET_CURRENCY_NOT_ALLOWED"),
            ("an empty locale list", {"supported_locales": []}, "MARKET_LOCALE_NOT_SUPPORTED"),
            ("an empty country list beside a default country", {"countries": []}, "MARKET_COUNTRY_NOT_LISTED"),
            ("an end earlier as an instant but later as a string",
             {"effective_from": "2026-01-01T10:00:00-03:00", "effective_to": "2026-01-01T11:00:00+03:00"}, "MARKET_EFFECTIVE_WINDOW_INVALID"),
            ("an unknown parent", {"parent_market_id": "mkt_nosuchmarket"}, "MARKET_PARENT_UNKNOWN")):
        if market_findings({**valid, **change}, known) != [code]:
            fail(f"market rule check: {label} must yield only {code}, not {market_findings({**valid, **change}, known)}")
    if market_findings({**valid, "allowed_currencies": None, "supported_locales": None}, known):
        fail("market rule check: absent allow-lists do not constrain")

    # The four routes use the request schemas and require a revision to change or activate.
    openapi = yaml.safe_load((CP / "openapi.yaml").read_text())
    ops = {op.get("operationId"): (path, method, op) for path, item in openapi["paths"].items()
           for method, op in item.items() if isinstance(op, dict) and "operationId" in op}
    for operation_id, body, if_match in (("createMarket", "MarketCreateRequest", False),
                                         ("updateMarket", "MarketUpdateRequest", True),
                                         ("activateMarket", "MarketActivationRequest", True)):
        _, _, op = ops[operation_id]
        ref = op["requestBody"]["content"]["application/json"]["schema"]["$ref"]
        if ref != f"./market.schema.json#/$defs/{body}":
            fail(f"{operation_id} accepts {ref}, not {body}")
        has_if_match = {"$ref": "#/components/parameters/MarketIfMatch"} in op.get("parameters", [])
        if has_if_match != if_match:
            fail(f"{operation_id}: If-Match must {'' if if_match else 'not '}be required")
    if ops["activateMarket"][2]["security"] != [{"adminOidc": ["market:approve"]}]:
        fail("activateMarket must require adminOidc market:approve")
    # Whoever may update or activate a market can read the revision to name.
    readers = ops["getMarket"][2]["security"]
    for operation_id in ("updateMarket", "activateMarket"):
        for requirement in ops[operation_id][2]["security"]:
            if requirement not in readers:
                fail(f"getMarket must admit {requirement}, which {operation_id} requires")
    if "MARKET_PARENT_UNKNOWN (422)" in ops["createMarket"][2]["description"].replace("\n", " "):
        fail("createMarket: an unknown parent is a validation finding, not a 422")
    if [lifecycle_t.get("operation_id") for lifecycle_t in lifecycle["transitions"] if lifecycle_t.get("operation_id")] != ["activateMarket"]:
        fail("market-lifecycle.yaml: only activate names an operation")


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
                     ("capability-explanation.schema.json", "CapabilityExplanationRequest"),
                     ("platform-context.schema.json", "PlatformContextResolveRequest"),
                     ("platform-context.schema.json", "PlatformContext"),
                     ("platform-context.schema.json", "ComposedResolutionRequest"),
                     ("platform-context.schema.json", "ComposedResolution")):
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


BLOCKING_CATEGORIES = ("capability_resolution_denial", "provisioning_blocker")


# Where a blocking reason is carried: TenantProvisioning and readiness
# blocking_reasons, and ProvisioningPlan blockers. Plan warnings are not
# blocking reasons.
BLOCKING_KEYS = ("blocking_reasons", "blockers")


def blocking_codes(document: object) -> list[str]:
    """The code of every blocking reason anywhere in document."""
    codes: list[str] = []
    if isinstance(document, dict):
        for key, value in document.items():
            if key in BLOCKING_KEYS and isinstance(value, list):
                codes.extend(reason["code"] for reason in value if isinstance(reason, dict) and "code" in reason)
            else:
                codes.extend(blocking_codes(value))
    elif isinstance(document, list):
        for item in document:
            codes.extend(blocking_codes(item))
    return codes


def check_blocking_reason_codes() -> None:
    registry = yaml.safe_load((CONTRACTS / "authorization" / "v1" / "reason-code-registry.yaml").read_text())
    registered = {entry["code"] for entry in registry["reason_codes"] if entry["category"] in BLOCKING_CATEGORIES}
    if not registered:
        fail("reason-code-registry.yaml registers no provisioning blocking codes")
    # The traversal finds plan blockers and blocking reasons, never warnings.
    probe = {"plan": {"blockers": [{"code": "A_BLOCKER", "message": "m"}], "warnings": [{"code": "A_WARNING", "message": "m"}]},
             "readiness": {"snapshots": [{"blocking_reasons": [{"code": "A_REASON"}]}]}}
    if sorted(blocking_codes(probe)) != ["A_BLOCKER", "A_REASON"]:
        fail(f"blocking_codes collects {sorted(blocking_codes(probe))} from a plan and readiness probe")
    for path in sorted((CP / "examples").glob("*.json")):
        if path.name in ("provider-migration.json", "changeset.json"):
            continue  # checked against their own categories by check_provider_migration and check_changeset
        for code in blocking_codes(json.loads(path.read_text())):
            if code not in registered:
                fail(f"examples/{path.name}: blocking reason {code!r} is not registered under {' or '.join(BLOCKING_CATEGORIES)}")


def main() -> int:
    check_schemas()
    check_canonical_entity()
    check_capability_explanation()
    check_platform_context()
    check_mapping_administration()
    check_mapping_resolution()
    check_tenant_provisioning()
    check_provider_migration()
    check_migration_execution()
    check_changeset()
    check_market()
    check_openapi_references()
    check_topology_identifiers()
    check_external_systems()
    check_blocking_reason_codes()
    if FAILURES:
        for message in FAILURES:
            print(f"FAIL: {message}", file=sys.stderr)
        return 1
    print("control-plane/v1 administrative contracts: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
