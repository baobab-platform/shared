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
     44-58, 119-122).

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
        "migrationStepResources", "migrationStep", "migrationDiscovery", "ProviderMigrationPlan", "ProviderMigration",
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
        if path.name == "provider-migration.json":
            continue  # checked against its own category by check_provider_migration
        for code in blocking_codes(json.loads(path.read_text())):
            if code not in registered:
                fail(f"examples/{path.name}: blocking reason {code!r} is not registered under {' or '.join(BLOCKING_CATEGORIES)}")


def main() -> int:
    check_schemas()
    check_canonical_entity()
    check_capability_explanation()
    check_mapping_administration()
    check_mapping_resolution()
    check_tenant_provisioning()
    check_provider_migration()
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
