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
        "organisationKind", "countryCode", "PlatformContextResolveRequest", "PlatformContext",
        "ContextAuthorityPurpose", "ProvisioningContextAuthority",
        "PlatformContextValidateRequest", "PlatformContextValidation",
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
        "changesetState", "changesetType", "changeSource", "TenantSuspension", "TenantReinstatement", "MarketActivation", "MappingActivation", "ProviderActivation", "EngineReleaseApproval", "DesiredReleaseChange", "AdministrativeGrantIssuance", "AdministrativeGrantDelegation", "administrativePrincipalStatus", "desiredChange",
        "ChangesetCreateRequest", "ChangesetCancelRequest", "planReference", "Changeset", "ChangesetPage",
        "changesetOperation", "changesetStepResources", "changesetStep", "ChangesetPlan", "affectedResource",
        "verificationResult", "ChangeOutcome",
    },
    "market.schema.json": {
        "marketId", "marketType", "market", "marketHierarchy", "marketValidationFinding",
        "MarketCreateRequest", "MarketUpdateRequest", "MarketActivationRequest",
    },
    "erp-assignment.schema.json": {
        "erpAssignmentMarket", "erpAssignmentLegalEntity", "ErpAssignment",
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
    rejects(schema, "PlatformContextResolveRequest", {**request, "country_code": "ug"}, "lower-case country selection")
    bad = copy.deepcopy(context)
    del bad["market_id"]
    rejects(schema, "PlatformContext", bad, "country without its primary market")
    bad = {k: v for k, v in context.items() if k not in ("country_code", "currency_code")}
    rejects(schema, "PlatformContext", bad, "market without its country")
    accepts(schema, "PlatformContext", {k: v for k, v in context.items() if k not in ("country_code", "market_id", "currency_code")},
            "context of a tenant that participates nowhere")

    composed_request, composed = example["composed_request"], example["composed"]
    bad = copy.deepcopy(composed_request)
    del bad["canonical_entity_id"]
    rejects(schema, "ComposedResolutionRequest", bad, "composed request without canonical_entity_id")
    rejects(schema, "ComposedResolution", {**composed, "capability": {**composed["capability"], "binding_mode": "SECONDARY"}},
            "retired binding mode")
    rejects(schema, "ComposedResolution", {**composed, "topology": {**composed["topology"], "id": "instance-1"}},
            "non-canonical engine instance id")


def check_platform_context_validation() -> None:
    """context:validate and POST /platform-context/validate (docs/architecture/context-authority-for-workloads.md).

    A resource server asks whether a stored context belongs to the actual caller it authenticated. The request carries the
    context and the caller's own token as cryptographic evidence and nothing the caller could assert; the response carries
    only the trusted facts, with a mandatory bound and no legal entity; the scope is defined and granted only to the ERP validator."""
    schema = "platform-context.schema.json"
    example = json.loads((CP / "examples" / "platform-context.json").read_text())
    request, validation = example["validate_request"], example["validation"]
    accepts(schema, "PlatformContextValidateRequest", request, "platform-context validate request")
    accepts(schema, "PlatformContextValidation", validation, "platform-context validation")

    for field in ("context_id", "subject_token"):
        missing = copy.deepcopy(request)
        del missing[field]
        rejects(schema, "PlatformContextValidateRequest", missing, f"validate request without {field}")
    # The caller can never state who is being validated, which audience to accept, or the tenant.
    for field in ("principal_id", "subject", "sub", "client_id", "azp", "actor_type", "expected_audience", "audience",
                  "aud", "validates_audience", "tenant_id", "issuer"):
        rejects(schema, "PlatformContextValidateRequest", {**request, field: "x"}, f"validate request carrying caller-controlled {field}")
    rejects(schema, "PlatformContextValidateRequest", {**request, "context_id": "ctx-1"}, "validate request with a non-uuid context")
    for token in ("", "a.b", "x" * 15, "x" * 8193):
        rejects(schema, "PlatformContextValidateRequest", {**request, "subject_token": token}, f"validate request with subject_token {token!r}")
    token_schema = json.loads((CP / schema).read_text())["$defs"]["PlatformContextValidateRequest"]["properties"]["subject_token"]
    # Serialization is not authority: opaque access tokens reach runtime verification.
    for token in ("opaque_access_token_0123456789", "a" * 16, "a" * 8192,
                  "token+with/slash=0123456789"):
        accepts(schema, "PlatformContextValidateRequest", {**request, "subject_token": token},
                "format-neutral access token")
    if "pattern" in token_schema or "compact JWT" in token_schema.get("description", ""):
        fail("subject_token must not constrain access-token serialization to JWT")
    if token_schema.get("minLength") != 16 or token_schema.get("maxLength") != 8192:
        fail("subject_token must retain the 16..8192 character bounds")
    if token_schema.get("writeOnly") is not True:
        fail("subject_token must be writeOnly: it is sent to the Control Plane and never returned")
    token_text = " ".join(token_schema.get("description", "").split())
    for phrase in ("only in this POST body", "independently", "never persisted", "never logged",
                   "never placed in a trace, an error or an audit payload"):
        if phrase not in token_text:
            fail(f"subject_token must document {phrase!r}")

    for field in ("context_id", "tenant_id", "resolved_at", "expires_at", "authority_purpose"):
        missing = copy.deepcopy(validation)
        del missing[field]
        rejects(schema, "PlatformContextValidation", missing, f"validation without {field}")
    # Valid-looking values, so a field is refused because the response is closed, not because "x" is malformed.
    probes = {"legal_entity_id": "ZURIBEANS", "principal_id": "prn_0199a1b2c3d47e8f", "country_code": "UG",
              "currency_code": "UGX", "organisation_type": "BUYER_ORGANISATION", "subject_token": "a.b.c"}
    for field, value in probes.items():
        rejects(schema, "PlatformContextValidation", {**validation, field: value}, f"validation carrying {field}")
    validation_properties = json.loads((CP / schema).read_text())["$defs"]["PlatformContextValidation"]["properties"]
    if set(validation_properties) != {"context_id", "tenant_id", "resolved_at", "expires_at", "market_id", "organisation_id",
                                      "authority_purpose", "provisioning_authority"}:
        fail("PlatformContextValidation must carry exactly context_id, tenant_id, resolved_at, expires_at, market_id, "
             f"organisation_id, authority_purpose and provisioning_authority (no legal_entity_id); found {sorted(validation_properties)}")

    # Pre-activation provisioning authority (docs/architecture/context-authority-for-workloads.md section 13): an explicit purpose
    # that is always stated, with the approved-plan tuple exactly when it is TENANT_PROVISIONING and never otherwise.
    defs = json.loads((CP / schema).read_text())["$defs"]
    if defs["ContextAuthorityPurpose"].get("enum") != ["RUNTIME", "TENANT_PROVISIONING"]:
        fail("ContextAuthorityPurpose must be exactly RUNTIME and TENANT_PROVISIONING")
    provisioning = example["provisioning_validation"]
    accepts(schema, "PlatformContextValidation", provisioning, "provisioning context validation")
    accepts(schema, "ProvisioningContextAuthority", provisioning["provisioning_authority"], "provisioning authority")
    rejects(schema, "PlatformContextValidation", {k: v for k, v in provisioning.items() if k != "provisioning_authority"},
            "a TENANT_PROVISIONING validation without its plan tuple")
    rejects(schema, "PlatformContextValidation", {**validation, "provisioning_authority": provisioning["provisioning_authority"]},
            "a RUNTIME validation carrying a plan tuple")
    rejects(schema, "PlatformContextValidation", {**validation, "authority_purpose": "PENDING_TENANT"}, "an unknown authority purpose")
    rejects(schema, "PlatformContextValidation", {k: v for k, v in validation.items() if k != "authority_purpose"},
            "a validation that leaves its purpose implied")
    for member in ("tenant_provisioning_id", "plan_id", "plan_version", "plan_digest"):
        incomplete = {k: v for k, v in provisioning["provisioning_authority"].items() if k != member}
        rejects(schema, "ProvisioningContextAuthority", incomplete, f"provisioning authority without {member}")
    rejects(schema, "ProvisioningContextAuthority", {**provisioning["provisioning_authority"], "approval_id": "apd_x1y2z3"},
            "provisioning authority carrying an approval id (approval records are Control Plane's)")
    purpose_text = " ".join(defs["ContextAuthorityPurpose"]["description"].split())
    for phrase in ("created only by the Control Plane's own provisioning execution, never through any HTTP operation",
                   "not redeemable as RUNTIME authority", "CONTEXT_NOT_FOUND (404)"):
        if phrase not in purpose_text:
            fail(f"ContextAuthorityPurpose must document {phrase!r}")
    request_properties = json.loads((CP / schema).read_text())["$defs"]["PlatformContextValidateRequest"]["properties"]
    if set(request_properties) != {"context_id", "subject_token"}:
        fail(f"PlatformContextValidateRequest must carry exactly context_id and subject_token; found {sorted(request_properties)}")

    openapi = yaml.safe_load((CP / "openapi.yaml").read_text())
    operation = openapi["paths"].get("/platform-context/validate", {}).get("post")
    if not operation:
        fail("openapi.yaml must declare POST /platform-context/validate")
        return
    if operation.get("security") != [{"workloadOidc": ["context:validate"]}]:
        fail("POST /platform-context/validate must be workloadOidc [context:validate] only")
    refs = (operation["requestBody"]["content"]["application/json"]["schema"]["$ref"],
            operation["responses"]["200"]["content"]["application/json"]["schema"]["$ref"])
    if refs != ("./platform-context.schema.json#/$defs/PlatformContextValidateRequest",
                "./platform-context.schema.json#/$defs/PlatformContextValidation"):
        fail("POST /platform-context/validate must use PlatformContextValidateRequest and PlatformContextValidation")
    if set(operation["responses"]) != {"200", "400", "401", "403", "404", "503"}:
        fail("POST /platform-context/validate must declare exactly 200, 400, 401, 403, 404 and 503")
    prose = " ".join(operation.get("description", "").split())
    for phrase in ("independently of the validator", "validates_audiences", "the request cannot choose the audience",
                   "canonical principal and requires it to equal Context.PrincipalID", "The caller never states a principal",
                   "an unbounded context is never cross-service authority", "indistinguishable", "TENANT_CONTEXT_MISMATCH",
                   "TENANT_NOT_ACTIVE", "This is not token exchange: no token is issued", "never persisted", "never logged",
                   "never placed in a trace, an error or an audit payload", "the validator principal, the resolved subject principal"):
        if phrase not in prose:
            fail(f"POST /platform-context/validate must document {phrase!r}")

    for phrase in ("authority_purpose", "TENANT_PROVISIONING", "context_purposes", "never through any HTTP operation",
                   "at most 15 minutes", "PROVISIONING_PROVIDERS, VERIFYING_READINESS or REMEDIATING",
                   "PROVISIONING_AUTHORITY_NOT_CURRENT", "The tenant ACTIVE rule is never relaxed for a RUNTIME context",
                   "a TENANT_PROVISIONING context is never accepted as RUNTIME authority"):
        if phrase not in prose:
            fail(f"POST /platform-context/validate must document {phrase!r}")
    if openapi["info"]["version"] != "1.37.0":
        fail("control-plane OpenAPI must be 1.37.0 (staff-assisted admission adds an operation)")
    resolve_text = " ".join(openapi["paths"]["/platform-context/resolve"]["post"]["description"].split())
    if "always authority_purpose RUNTIME" not in resolve_text:
        fail("POST /platform-context/resolve must state that its context is always RUNTIME")

    # Independent validation applies to both token profiles; a local signature is
    # meaningful only for a self-contained signed token (ADR-IAM-0020/0021).
    for phrase in ("For self-contained signed tokens", "issuer, signature and expiry",
                   "for opaque tokens", "trusted introspection result",
                   "configured issuer/provider authority", "active and unexpired",
                   "Both profiles require workload actor"):
        if phrase not in prose:
            fail(f"POST /platform-context/validate must document {phrase!r}")
    if "independently of the validator (issuer, signature, expiry" in prose:
        fail("POST /platform-context/validate must not require local signatures for opaque tokens")

    # Every consumer of a stored context judges the actual caller; none lets a context be a bearer credential.
    for path in ("/capabilities/resolve", "/capabilities/resolve-batch", "/resolution/mappings"):
        text = " ".join(openapi["paths"][path]["post"]["description"].split())
        for phrase in ("bound to the principal that resolved it", "canonical principal must equal the context's",
                       "indistinguishable from an unknown or expired one", "CONTEXT_NOT_FOUND, 404", "TENANT_CONTEXT_MISMATCH (403)",
                       "a TENANT_PROVISIONING context, which is never RUNTIME authority"):
            if phrase not in text:
                fail(f"POST {path} must document {phrase!r} (every consumer of a stored context enforces ownership)")
        if "another tenant's context" in text:
            fail(f"POST {path} must not describe a tenant-only context binding")
    context_text = json.loads((CP / schema).read_text())["$defs"]["PlatformContext"]["properties"]["context_id"]["description"]
    if "not a bearer credential" not in context_text:
        fail("PlatformContext.context_id must state that it is not a bearer credential")
    # capabilities/explain is unchanged: platform-level diagnostics for a human platform administrator, no ownership rule.
    explain = openapi["paths"]["/capabilities/explain"]["post"]
    if explain.get("security") != [{"adminOidc": ["capabilities:explain"]}]:
        fail("POST /capabilities/explain must stay adminOidc [capabilities:explain]")
    explain_text = " ".join(explain.get("description", "").split())
    if "platform-administrator authority" not in explain_text or "Not restricted to the caller's own tenant" not in explain_text:
        fail("POST /capabilities/explain must stay platform-level diagnostics requiring platform-administrator authority")

    scopes = {entry["name"]: entry for entry in yaml.safe_load(
        (CONTRACTS / "authorization" / "v1" / "scope-registry.yaml").read_text())["scopes"]}
    scope = scopes.get("context:validate")
    if not scope or scope.get("allowed_actors") != ["workload"] or scope.get("audience") != ["baobab-control-plane"] \
            or scope.get("grants_authority") is not False or scope.get("privileged"):
        fail("context:validate must be a non-privileged, workload-only scope for baobab-control-plane that grants no authority")
    for name in ("context:resolve", "context:validate"):
        if name not in scopes:
            fail(f"{name} must be registered")
    registry = yaml.safe_load((CONTRACTS / "identity" / "v1" / "workload-registry.yaml").read_text())
    # Audited allocation (owner decisions): each resource-server validator is
    # explicit and may validate only its own registered subject audience.
    holders = sorted(
        client
        for client, entry in registry["workloads"].items()
        if "context:validate" in entry["allowed_scopes"]
    )
    expected_holders = ["baobab-cms-workload", "baobab-dev-payments-validator", "baobab-dev-pulse-validator", "baobab-erp-workload", "baobab-int03-cms-validator", "baobab-pulse-workload"]
    if holders != expected_holders:
        fail(
            "context:validate may be allowed only to the registered CMS, ERP, Pulse and Payments "
            f"resource-server validators; found {holders}"
        )
    declared = {
        client: entry["validates_audiences"]
        for client, entry in registry["workloads"].items()
        if "validates_audiences" in entry
    }
    expected_validators = {
        "baobab-cms-workload": ["baobab-cms"],
        "baobab-erp-workload": ["baobab-erp"],
        "baobab-pulse-workload": ["baobab-pulse"],
        "baobab-int03-cms-validator": ["baobab-cms"],
        "baobab-dev-pulse-validator": ["baobab-pulse"],
        "baobab-dev-payments-validator": ["baobab-payments"],
    }
    if declared != expected_validators:
        fail(
            "validates_audiences must exactly bind each registered validator to "
            f"its resource-server audience; found {declared}"
        )


def check_capability_resolution() -> None:
    """resolveCapability names a registered capability_resolution_denial code
    for every non-RESOLVED decision it answers, and each code under exactly
    one decision (capability/v1 resolution.schema.json)."""
    openapi = yaml.safe_load((CP / "openapi.yaml").read_text())
    registry = yaml.safe_load((ROOT / "contracts/authorization/v1/reason-code-registry.yaml").read_text())["reason_codes"]
    registered = {r["code"] for r in registry if r["category"]…16941 tokens truncated…er_plan["desired_change"], "lifecycle": "ACTIVE"}},
            "a provider activation desired change with an extra property")

    # Engine release approval (ADR-BCP-025 section 2.4): the only path from
    # a recorded CANDIDATE release to APPROVED, approved under
    # engine-release:approve. Its plan reports every check, and its steps act
    # on the release alone, in releaseStatus.
    release_kind = kinds["ENGINE_RELEASE_APPROVAL"]
    if release_kind.get("approval_scope") != "engine-release:approve" or release_kind["from_status"] != ["CANDIDATE"] \
            or release_kind["to_status"] != "APPROVED":
        fail("ENGINE_RELEASE_APPROVAL must move CANDIDATE to APPROVED and require engine-release:approve")
    release_checks = release_kind.get("plan_checks", [])
    if {c["check"] for c in release_checks} != {"SUPPORT_CATALOGUED", "PROVENANCE", "CERTIFICATION"}:
        fail("ENGINE_RELEASE_APPROVAL plan_checks must be SUPPORT_CATALOGUED, PROVENANCE and CERTIFICATION")
    policy = yaml.safe_load((CONTRACTS / "topology" / "v1" / "release-policy.yaml").read_text())
    approve = [t for t in policy["status_transitions"]["transitions"] if t["command"] == "approve"]
    if len(approve) != 1 or approve[0]["from"] != release_kind["from_status"] or approve[0]["to"] != release_kind["to_status"]:
        fail("ENGINE_RELEASE_APPROVAL must be release-policy.yaml's approve transition")
    release_plan = example["engine_release_approval_plan"]
    accepts(schema, "ChangesetPlan", release_plan, "changeset engine_release_approval_plan")
    if [step["operation"] for step in release_plan["steps"]] != release_kind["operations"] \
            or release_plan["changeset_type"] != release_kind["changeset_type"]:
        fail("changeset engine_release_approval_plan does not run its change kind's operations and type")
    if [c["check"] for c in release_plan["readiness_requirements"]] != [c["check"] for c in release_checks]:
        fail("changeset engine_release_approval_plan must report every ENGINE_RELEASE_APPROVAL plan check, in order")
    for step in release_plan["steps"]:
        if step["resources"].get("release_id") != release_plan["desired_change"]["release_id"]:
            fail(f"changeset engine_release_approval_plan: step {step['step_id']} acts on another release")
    mixed = copy.deepcopy(release_plan)
    mixed["steps"][0]["resources"]["provider_id"] = provider_plan["desired_change"]["provider_id"]
    rejects(schema, "ChangesetPlan", mixed, "a release step naming a provider too")
    lowered = copy.deepcopy(release_plan)
    lowered["steps"][0]["resources"]["to_status"] = "ACTIVE"
    rejects(schema, "ChangesetPlan", lowered, "a release step in the provider lifecycle vocabulary")
    crossed = copy.deepcopy(release_plan)
    crossed["steps"] = provider_plan["steps"]
    rejects(schema, "ChangesetPlan", crossed, "a release approval plan running provider steps")
    rejects(schema, "ChangesetCreateRequest",
            {**create, "desired_change": {**release_plan["desired_change"], "status": "APPROVED"}},
            "a release approval desired change with an extra property")
    status_change = json.loads((CONTRACTS / "topology" / "v1" / "release.schema.json").read_text())["$defs"]["EngineReleaseStatusChangeRequest"]
    if "APPROVED" in status_change["properties"]["target_status"]["enum"]:
        fail("EngineReleaseStatusChangeRequest must not approve: approval is the ENGINE_RELEASE_APPROVAL changeset")

    # Desired release (ADR-BCP-025 section 2.5, gate ER-03): changes an
    # engine instance's desired release, never its status, under
    # desired-release:approve; its plan reports every check, and its steps
    # act on the instance alone, naming the release they desire.
    desired_kind = kinds["ENGINE_INSTANCE_DESIRED_RELEASE"]
    if desired_kind.get("approval_scope") != "desired-release:approve" or desired_kind.get("changes") != "desired_release" \
            or "to_status" in desired_kind or "RETIRED" in desired_kind["from_status"]:
        fail("ENGINE_INSTANCE_DESIRED_RELEASE must change desired_release of an instance that is not RETIRED, under desired-release:approve")
    desired_checks = [c["check"] for c in desired_kind.get("plan_checks", [])]
    if desired_checks != ["DESIRED_RELEASE_CHANGES", "RELEASE_APPROVED", "RELEASE_ENGINE", "PROVENANCE", "CERTIFICATION"]:
        fail(f"ENGINE_INSTANCE_DESIRED_RELEASE plan_checks are not the gate ER-03 checks: {desired_checks}")
    desired_plan = example["desired_release_plan"]
    accepts(schema, "ChangesetPlan", desired_plan, "changeset desired_release_plan")
    if [step["operation"] for step in desired_plan["steps"]] != desired_kind["operations"] \
            or [c["check"] for c in desired_plan["readiness_requirements"]] != desired_checks:
        fail("changeset desired_release_plan does not run its change kind's operations and report every check")
    for step in desired_plan["steps"]:
        if step["resources"].get("engine_instance_id") != desired_plan["desired_change"]["engine_instance_id"] \
                or step["resources"].get("desired_release_id") != desired_plan["desired_change"]["release_id"]:
            fail(f"changeset desired_release_plan: step {step['step_id']} acts on another instance or release")
    clearing = copy.deepcopy(desired_plan)
    clearing["desired_change"]["release_id"] = None
    for step in clearing["steps"]:
        step["resources"]["desired_release_id"] = None
    accepts(schema, "ChangesetPlan", clearing, "a desired release plan that clears it")
    mixed = copy.deepcopy(desired_plan)
    mixed["steps"][0]["resources"]["release_id"] = desired_plan["desired_change"]["release_id"]
    rejects(schema, "ChangesetPlan", mixed, "an engine instance step naming a release step's release_id too")
    lowered = copy.deepcopy(desired_plan)
    lowered["steps"][0]["resources"]["from_status"] = "active"
    rejects(schema, "ChangesetPlan", lowered, "an engine instance step outside engineInstanceStatus")
    stray = copy.deepcopy(release_plan)
    stray["steps"][0]["resources"]["desired_release_id"] = desired_plan["desired_change"]["release_id"]
    rejects(schema, "ChangesetPlan", stray, "a desired_release_id outside an engine instance step")
    rejects(schema, "ChangesetCreateRequest",
            {**create, "desired_change": {"kind": "ENGINE_INSTANCE_DESIRED_RELEASE", "engine_instance_id": desired_plan["desired_change"]["engine_instance_id"]}},
            "a desired release change that names no release_id, not even null")

    # Administrative grant changes (ADR-BCP-020 gate ADA-06): maker-checker
    # for HIGH and CRITICAL authority. Both kinds change administrative
    # authority, never a status, under administrator:approve; their steps act
    # on the grantee principal or the source grant alone.
    for kind_name, plan_key, target, operations in (
            ("ADMINISTRATIVE_GRANT_ISSUANCE", "administrative_grant_issuance_plan", "grantee_principal_id", ["ISSUE_ADMINISTRATIVE_GRANT", "VERIFY_ADMINISTRATIVE_GRANT"]),
            ("ADMINISTRATIVE_GRANT_DELEGATION", "administrative_grant_delegation_plan", "source_grant_id", ["DELEGATE_ADMINISTRATIVE_GRANT", "VERIFY_ADMINISTRATIVE_GRANT"])):
        grant_kind = kinds[kind_name]
        if grant_kind.get("approval_scope") != "administrator:approve" or grant_kind.get("changes") != "administrative_authority" \
                or "to_status" in grant_kind or grant_kind["from_status"] != ["ACTIVE"] or grant_kind["operations"] != operations:
            fail(f"{kind_name} must change administrative_authority of an ACTIVE target under administrator:approve")
        grant_plan = example[plan_key]
        accepts(schema, "ChangesetPlan", grant_plan, f"changeset {plan_key}")
        if [c["check"] for c in grant_plan["readiness_requirements"]] != [c["check"] for c in grant_kind["plan_checks"]]:
            fail(f"changeset {plan_key} does not report every plan check of {kind_name}")
        for step in grant_plan["steps"]:
            if set(step["resources"]) - {target, "from_status", "target_revision"}:
                fail(f"changeset {plan_key}: step {step['step_id']} names resources beyond {target}")
        crossed_grant = copy.deepcopy(grant_plan)
        other = "source_grant_id" if target == "grantee_principal_id" else "grantee_principal_id"
        crossed_grant["steps"][0]["resources"][other] = "agr_01k9src0001" if other == "source_grant_id" else "2f1c5c3e-8f0e-4a55-9a3b-5d7f9a1b2c3d"
        rejects(schema, "ChangesetPlan", crossed_grant, f"a {plan_key} step naming both grant resources")
        tenant_step = copy.deepcopy(grant_plan)
        tenant_step["steps"][0]["resources"]["tenant_id"] = plan["desired_change"]["tenant_id"]
        rejects(schema, "ChangesetPlan", tenant_step, f"a {plan_key} step also naming a tenant")
        wrong_type = copy.deepcopy(grant_plan)
        wrong_type["changeset_type"] = "SUSPEND"
        rejects(schema, "ChangesetPlan", wrong_type, f"a {plan_key} typed SUSPEND")
        statused = copy.deepcopy(grant_plan)
        statused["steps"][0]["resources"]["from_status"] = "active"
        rejects(schema, "ChangesetPlan", statused, f"a {plan_key} step outside its target's status vocabulary")
    standing_with_end = {"kind": "ADMINISTRATIVE_GRANT_ISSUANCE", **{k: v for k, v in example["administrative_grant_issuance_plan"]["desired_change"].items() if k != "kind"}, "grant_type": "STANDING"}
    rejects(schema, "ChangesetCreateRequest", {**create, "desired_change": standing_with_end}, "a STANDING grant issuance with valid_until")
    timed_without_end = {k: v for k, v in example["administrative_grant_issuance_plan"]["desired_change"].items() if k != "valid_until"}
    rejects(schema, "ChangesetCreateRequest", {**create, "desired_change": timed_without_end}, "a TIME_BOUND grant issuance without valid_until")
    accepts(schema, "ChangesetCreateRequest", {**create, "desired_change": example["administrative_grant_issuance_plan"]["desired_change"]}, "a grant issuance request")
    accepts(schema, "ChangesetCreateRequest", {**create, "desired_change": example["administrative_grant_delegation_plan"]["desired_change"]}, "a grant delegation request")

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


def check_event_ingress() -> None:
    """Signed delivery of engine events to the Control Plane (docs/architecture/signed-event-delivery.md).

    The event stays the transport-neutral contract; this pins the HTTPS binding: closed headers, the replay window and
    retention the schema, the allow-list and the doc agree on, one operation authenticated by the signature and by nothing
    else, and an accepted list that is a subset of what the event registry says the producer publishes.
    """
    events_dir = CONTRACTS / "events" / "v1"
    delivery_schema = json.loads((events_dir / "signed-delivery.schema.json").read_text())
    registry = Registry().with_resource(delivery_schema["$id"], Resource.from_contents(delivery_schema))

    def delivery(definition: str) -> Draft202012Validator:
        return Draft202012Validator({"$ref": f"{delivery_schema['$id']}#/$defs/{definition}"}, registry=registry,
                                    format_checker=FORMATS)

    digest = "hmac-sha256=" + "0" * 64
    good = {"Baobab-Key-Id": "erp-delivery-2026-10", "Baobab-Timestamp": "2026-10-07T17:30:00Z", "Baobab-Signature": digest}
    if not delivery("DeliveryHeaders").is_valid(good):
        fail("signed-delivery DeliveryHeaders rejected a valid header set")
    for label, change in (
        ("a missing key id", {"Baobab-Key-Id": None}),
        ("a missing timestamp", {"Baobab-Timestamp": None}),
        ("a missing signature", {"Baobab-Signature": None}),
        ("an uppercase key id", {"Baobab-Key-Id": "ERP-KEY"}),
        ("a key id with a path character", {"Baobab-Key-Id": "erp/key"}),
        ("a non-UTC timestamp", {"Baobab-Timestamp": "2026-10-07T17:30:00+02:00"}),
        ("a timestamp with fractions", {"Baobab-Timestamp": "2026-10-07T17:30:00.5Z"}),
        ("a bare hex signature", {"Baobab-Signature": "0" * 64}),
        ("an unknown algorithm", {"Baobab-Signature": "none=" + "0" * 64}),
        ("an uppercase hex signature", {"Baobab-Signature": "hmac-sha256=" + "A" * 64}),
        ("a truncated signature", {"Baobab-Signature": "hmac-sha256=" + "0" * 63}),
        ("an extra header member", {"Baobab-Extra": "x"}),
    ):
        bad = dict(good)
        for key, value in change.items():
            if value is None:
                bad.pop(key)
            else:
                bad[key] = value
        if delivery("DeliveryHeaders").is_valid(bad):
            fail(f"negative fixture accepted: DeliveryHeaders with {label}")

    receipt = {"event_id": "78844bfb-4ad7-446a-b8bf-4dad336e6beb", "status": "ACCEPTED", "received_at": "2026-10-07T17:30:00Z"}
    if not delivery("DeliveryReceipt").is_valid(receipt) or not delivery("DeliveryReceipt").is_valid({**receipt, "status": "DUPLICATE"}):
        fail("signed-delivery DeliveryReceipt rejected a valid receipt")
    for label, bad in (("an unknown status", {**receipt, "status": "APPLIED"}), ("a missing event id", {k: v for k, v in receipt.items() if k != "event_id"}),
                       ("an extra member", {**receipt, "applied": True})):
        if delivery("DeliveryReceipt").is_valid(bad):
            fail(f"negative fixture accepted: DeliveryReceipt with {label}")

    for definition, good_status, bad_status in (("DeliveryReceiptAccepted", "ACCEPTED", "DUPLICATE"), ("DeliveryReceiptDuplicate", "DUPLICATE", "ACCEPTED")):
        if not delivery(definition).is_valid({**receipt, "status": good_status}):
            fail(f"{definition} rejected a valid receipt")
        if delivery(definition).is_valid({**receipt, "status": bad_status}):
            fail(f"negative fixture accepted: {definition} with status {bad_status}")
    responses = yaml.safe_load((CP / "openapi.yaml").read_text())["paths"]["/integration/events"]["post"]["responses"]
    for code, definition in (("200", "DeliveryReceiptDuplicate"), ("202", "DeliveryReceiptAccepted")):
        ref = responses[code]["content"]["application/json"]["schema"].get("$ref", "")
        if not ref.endswith(f"signed-delivery.schema.json#/$defs/{definition}"):
            fail(f"receiveEngineEvent {code} must use {definition} so status cannot contradict the HTTP status")

    policy = delivery_schema["$defs"]["SenderPolicy"]["properties"]
    ingress = yaml.safe_load((CP / "event-ingress.yaml").read_text())
    if ingress.get("recipient") != "baobab-control-plane":
        fail("event-ingress.yaml recipient must be baobab-control-plane (the signature is bound to it)")
    if ingress.get("replay_window_seconds") != policy["replay_window_seconds"]["const"] or \
            ingress.get("receipt_retention_days") != policy["receipt_retention_days"]["const"]:
        fail("event-ingress.yaml replay window and receipt retention must equal signed-delivery.schema.json SenderPolicy")
    horizon = policy["max_retry_horizon_hours"]["const"]
    if ingress.get("max_retry_horizon_hours") != horizon or horizon >= ingress["receipt_retention_days"] * 24:
        fail("the sender retry horizon must equal SenderPolicy and stay below receipt retention")
    if ingress.get("identity") != ["source", "id"]:
        fail("receipts and conflicts are keyed by the envelope's (source, id), the delivery identity envelope.schema.json defines")
    if ingress.get("signing_algorithms") != ["hmac-sha256"]:
        fail("only hmac-sha256 is a defined delivery signature algorithm")

    # Observability: a closed metric catalogue whose labels are bounded vocabularies and never identify anything.
    ingress_defs = delivery_schema["$defs"]
    if ingress_defs["eventIngressMetric"]["enum"] != [
            "event_ingress_receipts_total", "event_ingress_rejections_total", "event_processing_total",
            "event_pending_age_seconds", "event_delivery_key_reload_failures_total"]:
        fail("signed-delivery.schema.json eventIngressMetric must be exactly the signed delivery metric catalogue")
    if ingress_defs["eventIngressMetricLabel"]["enum"] != ["result", "reason_code", "outcome", "event_type"]:
        fail("signed-delivery.schema.json eventIngressMetricLabel must be exactly result, reason_code, outcome, event_type")
    unbounded = {"event_id", "id", "source", "tenant_id", "key_id", "signature", "digest", "operation_id", "secret", "subject"}
    if unbounded & set(ingress_defs["eventIngressMetricLabel"]["enum"]):
        fail("signed delivery metric labels must stay bounded and anonymous")
    for vocabulary, expected in (("eventIngressResult", ["accepted", "duplicate", "conflict"]),
                                 ("eventProcessingOutcome", ["applied", "retried", "dead_lettered"]),
                                 ("eventIngressReasonCode", ["malformed", "unauthenticated", "too_large", "not_accepted", "payload_invalid", "unavailable"])):
        if ingress_defs[vocabulary]["enum"] != expected:
            fail(f"signed-delivery.schema.json {vocabulary} must be {expected}")

    registered = {entry["type"]: entry for entry in yaml.safe_load((events_dir / "event-registry.yaml").read_text())["events"]}
    accepted = ingress.get("accepted") or []
    if ingress_defs["eventIngressEventType"]["enum"] != [entry.get("type") for entry in accepted]:
        fail("signed-delivery.schema.json eventIngressEventType must be exactly the event types event-ingress.yaml accepts, so the event_type label stays bounded")
    if [entry.get("type") for entry in accepted] != ["com.baobab-platform.erp.provisioning.changed.v1"]:
        fail("the Control Plane accepts exactly ERP provisioning.changed over signed delivery; any other type is a reviewed contract change")
    for entry in accepted:
        known = registered.get(entry["type"])
        if known is None:
            fail(f"event-ingress.yaml accepts unregistered type {entry['type']}")
            continue
        if known.get("lifecycle") != "ACTIVE" or known.get("producer") != entry.get("producer"):
            fail(f"{entry['type']} must be an ACTIVE registry type produced by {entry.get('producer')}")
        if entry.get("source") != f"urn:baobab-platform:service:{entry.get('producer')}":
            fail(f"{entry['type']} source must be the producer's service URN")
        if entry.get("scope") != "tenant" or not entry.get("pending_max_age_hours"):
            fail(f"{entry['type']} must be tenant-scoped and bound how long an unmatched event stays pending")

    openapi = yaml.safe_load((CP / "openapi.yaml").read_text())
    operations = [(path, method, op) for path, item in openapi["paths"].items() for method, op in item.items()
                  if isinstance(op, dict) and "operationId" in op]
    signed = [(p, m, o["operationId"]) for p, m, o in operations
              if any("signedEventDelivery" in requirement for requirement in o.get("security", []))]
    if signed != [("/integration/events", "post", "receiveEngineEvent")]:
        fail(f"exactly POST /integration/events (receiveEngineEvent) may authenticate with signedEventDelivery, got {signed}")
    operation = openapi["paths"]["/integration/events"]["post"]
    if operation.get("security") != [{"signedEventDelivery": []}]:
        fail("receiveEngineEvent must be authenticated by the delivery signature alone (no bearer token, no scope)")
    if set(operation["responses"]) != {"200", "202", "400", "401", "409", "413", "422", "503"}:
        fail("receiveEngineEvent must answer exactly 200, 202, 400, 401, 409, 413, 422 and 503")
    if list(operation["requestBody"]["content"]) != ["application/cloudevents+json"]:
        fail("receiveEngineEvent accepts only application/cloudevents+json")
    if openapi["components"]["securitySchemes"]["signedEventDelivery"].get("name") != "Baobab-Signature":
        fail("the signedEventDelivery scheme must be the Baobab-Signature header")
    text = " ".join(operation["description"].split())
    for phrase in ("within 300 seconds", "at-least-once", "EVENT_ID_CONFLICT", "(source, id)", "within 72 hours", "durably recorded, never that it has been acted on",
                   "A bearer token is neither required nor accepted", "No failure answer, audit record or log carries the signature",
                   "The event is a trigger to inspect authoritative state"):
        if phrase not in text:
            fail(f"receiveEngineEvent must document {phrase!r}")
    for param in operation["parameters"]:
        if param.get("name", "").startswith("Baobab-") and not param.get("required"):
            fail(f"delivery header {param['name']} must be required")


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


BLOCKING_CATEGORIES = ("capability_resolution_denial", "provisioning_blocker", "release_drift")


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
    # A release_drift code is a blocking reason only where Shared policy gives
    # that drift a BLOCKED readiness effect; a DEGRADED one is never a blocker.
    drift_policy = yaml.safe_load((CONTRACTS / "topology" / "v1" / "release-policy.yaml").read_text())["drift"]["reasons"]
    drift_codes = {entry["code"] for entry in registry["reason_codes"] if entry["category"] == "release_drift"}
    for code in drift_codes:
        if drift_policy.get(code, {}).get("readiness_effect") not in ("BLOCKED", "DEGRADED"):
            fail(f"release-policy.yaml: drift reason {code} needs a readiness_effect of BLOCKED or DEGRADED")
    blockable = {code for code in drift_codes if drift_policy.get(code, {}).get("readiness_effect") == "BLOCKED"}
    registered = (registered - drift_codes) | blockable
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
    check_platform_context_validation()
    check_capability_resolution()
    check_mapping_administration()
    check_mapping_resolution()
    check_tenant_provisioning()
    check_erp_assignment()
    check_provider_migration()
    check_migration_execution()
    check_changeset()
    check_market()
    check_event_ingress()
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
