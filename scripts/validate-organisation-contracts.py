#!/usr/bin/env python3
"""Validate the ADR-BCP-018 organisation/v1 contracts.

Unlike the structural Ruby validators, this performs real JSON Schema
Draft 2020-12 validation with every cross-schema $ref resolved against the
contracts in this repository:

  1. each schema is a valid Draft 2020-12 schema, its $id matches its file
     name, and it defines exactly the $defs that file is responsible for;
  2. every $ref in organisation/v1 resolves;
  3. every example record validates against its $def, and the example
     documents are referentially and semantically coherent;
  4. negative fixtures prove the load-bearing rules actually reject bad data;
  5. asyncapi.yaml registers every ADR-BCP-018 section 124 event under the
     ADR-SHARED-008 naming convention, composed with the canonical envelope,
     and event payloads never publish names or evidence (section 125);
  6. contracts.lock.yaml registers exactly these schemas.

Setup (same dependencies as the Foundation fixture suite):
  python3 -m pip install -r .github/foundation-tests/requirements.txt
  python3 scripts/validate-organisation-contracts.py
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
ORG = CONTRACTS / "organisation" / "v1"
BASE_URI = "https://contracts.baobab-platform.com/organisation/v1/"

# File -> the $defs it is responsible for. Guards against the filename/$id/
# content permutation that previously shipped on this contract.
RESPONSIBILITIES = {
    "domain.schema.json": {
        "Organisation", "LegalEntityProfile", "organisationForm", "verificationState",
        "lifecycleStatus", "legalStatus", "organisationIdentifier", "organisationAddress",
        "corporateRelationshipId", "corporateGroupId", "corporateGroupMembershipId",
        "platformRelationshipId", "platformAccountId", "platformAccountMembershipId", "tenantPlatformAccountBindingId",
        "tenantOrganisationMappingId", "tenantLegalEntityMappingId", "platformId",
        "evidenceReference", "relationshipClassification", "iamOrganisationReferenceId",
    },
    "relationship.schema.json": {
        "CorporateRelationship", "CorporateGroup", "CorporateGroupMembership",
        "corporateRelationshipType", "relationshipStatus",
    },
    "platform.schema.json": {
        "PlatformRelationship", "PlatformAccount", "PlatformAccountMembership",
        "platformRelationshipType", "platformAccountRole", "platformAccountStatus", "platformAccountTransitions",
        "PlatformAccountStatusChangeRequest", "TenantPlatformAccountBinding", "tenantPlatformAccountBindingStatus",
        "TenantPlatformAccountBindingRequest", "TenantPlatformAccountBindingEndRequest",
    },
    "mapping.schema.json": {
        "TenantOrganisationMapping", "TenantLegalEntityMapping", "mappingStatus",
        "tenantOrganisationMappingRole", "tenantLegalEntityMappingRole",
    },
    "iam.schema.json": {
        "IamOrganisationReference", "IamOrganisationEvidence", "keycloakOrganizationClaim",
        "iamProvider", "iamIssuer", "providerOrganisationId", "iamReferenceStatus",
        "IamOrganisationLinkRequest", "IamOrganisationRetireRequest", "IamOrganisationResolution",
    },
    "admission.schema.json": {
        "OrganisationAdmissionRequest", "OrganisationAdmissionOutcome", "admissionDecisionId",
        "identityResolutionOutcome", "identityResolution", "applicantOrganisation", "legalVerification",
        "corporateRelationshipClaim", "platformAccountAssignment",
    },
    "counterparty.schema.json": {
        "CounterpartyRole", "OrganisationResolutionCandidate", "ResolutionCandidateDecision",
        "counterpartyRoleId", "resolutionCandidateId", "counterpartyRoleType", "counterpartyRoleStatus",
        "legacyOrganisationKind", "resolutionCandidateStatus", "matchedIdentifier",
        "CounterpartyRoleAssignRequest", "CounterpartyRoleEndRequest", "CounterpartyReconciliationReport",
    },
    "observability.schema.json": {
        "RelationshipDriftFinding", "RelationshipDriftReport", "OrganisationAuditEntry", "driftRule",
        "driftType", "driftSeverity", "driftResourceType", "organisationMetric", "organisationMetricLabel",
    },
    "events.schema.json": {
        "OrganisationCreated", "OrganisationVerified", "OrganisationSuspended", "LegalEntityVerified",
        "CorporateRelationshipActivated", "CorporateRelationshipEnded", "CorporateRelationshipConflicted",
        "PlatformRelationshipActivated", "PlatformRelationshipEnded", "PlatformAccountCreated",
        "PlatformAccountMembershipChanged", "TenantOrganisationMappingActivated", "TenantLegalEntityMappingActivated",
        "PlatformAccountStatusChanged", "TenantPlatformAccountBound", "TenantPlatformAccountBindingEnded",
    },
}

# ADR-BCP-018 section 124 event -> payload $def. Event types follow
# ADR-SHARED-008 (com.baobab-platform.<context>.<...>.vN).
EVENT_TYPES = {
    "com.baobab-platform.control-plane.organisation.created.v1": "OrganisationCreated",
    "com.baobab-platform.control-plane.organisation.verified.v1": "OrganisationVerified",
    "com.baobab-platform.control-plane.organisation.suspended.v1": "OrganisationSuspended",
    "com.baobab-platform.control-plane.legal-entity.verified.v1": "LegalEntityVerified",
    "com.baobab-platform.control-plane.corporate-relationship.activated.v1": "CorporateRelationshipActivated",
    "com.baobab-platform.control-plane.corporate-relationship.ended.v1": "CorporateRelationshipEnded",
    "com.baobab-platform.control-plane.corporate-relationship.conflicted.v1": "CorporateRelationshipConflicted",
    "com.baobab-platform.control-plane.platform-relationship.activated.v1": "PlatformRelationshipActivated",
    "com.baobab-platform.control-plane.platform-relationship.ended.v1": "PlatformRelationshipEnded",
    "com.baobab-platform.control-plane.platform-account.created.v1": "PlatformAccountCreated",
    "com.baobab-platform.control-plane.platform-account-membership.changed.v1": "PlatformAccountMembershipChanged",
    "com.baobab-platform.control-plane.tenant-organisation-mapping.activated.v1": "TenantOrganisationMappingActivated",
    "com.baobab-platform.control-plane.tenant-legal-entity-mapping.activated.v1": "TenantLegalEntityMappingActivated",
    "com.baobab-platform.control-plane.platform-account.status-changed.v1": "PlatformAccountStatusChanged",
    "com.baobab-platform.control-plane.tenant-platform-account-binding.bound.v1": "TenantPlatformAccountBound",
    "com.baobab-platform.control-plane.tenant-platform-account-binding.ended.v1": "TenantPlatformAccountBindingEnded",
}
ENVELOPE_REF = "../../events/v1/envelope.schema.json"
# Section 125: payloads carry identifiers and state, never these.
FORBIDDEN_EVENT_FIELDS = {
    "display_name", "official_name", "legal_name", "trading_names", "identifiers", "addresses",
    "registration_identifiers", "evidence_references", "evidence_reference", "metadata", "verified_by",
    "billing_profile_reference", "contract_references", "control_basis",
}

# Example document key -> (schema file, $def).
EXAMPLE_KEYS = {
    "organisations": ("domain.schema.json", "Organisation"),
    "legal_entity_profiles": ("domain.schema.json", "LegalEntityProfile"),
    "corporate_relationships": ("relationship.schema.json", "CorporateRelationship"),
    "corporate_groups": ("relationship.schema.json", "CorporateGroup"),
    "corporate_group_memberships": ("relationship.schema.json", "CorporateGroupMembership"),
    "platform_relationships": ("platform.schema.json", "PlatformRelationship"),
    "platform_accounts": ("platform.schema.json", "PlatformAccount"),
    "platform_account_memberships": ("platform.schema.json", "PlatformAccountMembership"),
    "tenant_platform_account_bindings": ("platform.schema.json", "TenantPlatformAccountBinding"),
    "tenant_organisation_mappings": ("mapping.schema.json", "TenantOrganisationMapping"),
    "tenant_legal_entity_mappings": ("mapping.schema.json", "TenantLegalEntityMapping"),
    "iam_organisation_references": ("iam.schema.json", "IamOrganisationReference"),
    "organisation_admission_requests": ("admission.schema.json", "OrganisationAdmissionRequest"),
    "organisation_admission_outcomes": ("admission.schema.json", "OrganisationAdmissionOutcome"),
    "counterparty_roles": ("counterparty.schema.json", "CounterpartyRole"),
    "organisation_resolution_candidates": ("counterparty.schema.json", "OrganisationResolutionCandidate"),
    "relationship_drift_findings": ("observability.schema.json", "RelationshipDriftFinding"),
    "organisation_audit_entries": ("observability.schema.json", "OrganisationAuditEntry"),
}

# ORG-15: ADR-BCP-018 section 130's metric catalogue, and label names that
# would make metrics high-cardinality or leak identity (ADR-BCP-008 s44).
SECTION_130_METRICS = {
    "organisation_total", "organisation_verification_total", "organisation_duplicate_candidate_total",
    "corporate_relationship_total", "corporate_relationship_conflict_total", "corporate_relationship_expiry_total",
    "platform_relationship_total", "platform_relationship_reclassification_total", "platform_account_total",
    "platform_account_membership_total", "tenant_organisation_mapping_total", "tenant_legal_entity_mapping_total",
    "internal_eligibility_review_total", "relationship_drift_total", "relationship_resolution_failure_total",
    "cross_tenant_group_access_denied_total", "corporate_group_derivation_total",
}
FORBIDDEN_METRIC_LABELS = {"tenant_id", "organisation_id", "legal_entity_id", "name", "display_name",
                           "registration_number", "identifier", "user_id", "principal_id"}

# ORG-13: identity is matched on these governed identifier types only
# (ADR-BCP-018 section 99), normalised as the Control Plane compares them.
GOVERNED_IDENTIFIER_TYPES = {"COMPANY_REGISTRATION", "TAX_IDENTIFIER", "VAT_IDENTIFIER", "LEI"}
LIVE_ROLE_STATUSES = {"PENDING", "ACTIVE", "SUSPENDED"}


def normalise_identifier(value: str) -> str:
    return re.sub(r"[\s./-]", "", value).upper()

REQUIRED_CORPORATE_VOCABULARY = {"OWNS", "CONTROLS", "BRANCH_OF", "AFFILIATE_OF", "JOINT_VENTURE_WITH", "SUCCESSOR_OF"}
FORBIDDEN_CORPORATE_VOCABULARY = {"PARENT_OF", "SUBSIDIARY_OF", "SISTER_OF", "RELATED_TO", "JOINT_VENTURE", "SUPPLIER_OF", "CUSTOMER_OF"}
REQUIRED_PLATFORM_VOCABULARY = {"PLATFORM_OWNER", "PLATFORM_OPERATOR", "PLATFORM_GROUP_AFFILIATE", "EXTERNAL_CLIENT", "PLATFORM_PARTNER", "MANAGED_ENTITY"}
OPAQUE_EXTERNAL_LEGAL_ENTITY = re.compile(r"^LE-[0-9A-Z]{8,}$")
RFC3339 = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$")

failures: list[str] = []


def fail(message: str) -> None:
    failures.append(message)


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


# jsonschema only checks "date-time" when an optional dependency is present;
# enforce RFC 3339 explicitly so the check cannot silently disappear.
FORMATS = FormatChecker()


@FORMATS.checks("date-time")
def _is_datetime(value: object) -> bool:
    if not isinstance(value, str):
        return True
    if not RFC3339.match(value):
        return False
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return True


def build_registry() -> Registry:
    registry = Registry()
    for path in sorted(CONTRACTS.rglob("*.json")):
        try:
            document = json.loads(path.read_text())
        except json.JSONDecodeError:
            continue  # other validators own non-organisation JSON well-formedness
        if isinstance(document, dict) and isinstance(document.get("$id"), str):
            registry = registry.with_resource(document["$id"], Resource.from_contents(document))
    return registry


REGISTRY = build_registry()
SCHEMAS: dict[str, dict] = {}


def validator_for(schema_file: str, definition: str) -> Draft202012Validator:
    return Draft202012Validator(
        {"$ref": f"{BASE_URI}{schema_file}#/$defs/{definition}"},
        registry=REGISTRY,
        format_checker=FORMATS,
    )


def errors_for(schema_file: str, definition: str, instance: object) -> list[str]:
    found = validator_for(schema_file, definition).iter_errors(instance)
    return [f"{'/'.join(str(p) for p in e.absolute_path) or '<root>'}: {e.message}" for e in found]


def walk_refs(node: object):
    if isinstance(node, dict):
        if isinstance(node.get("$ref"), str):
            yield node["$ref"]
        for value in node.values():
            yield from walk_refs(value)
    elif isinstance(node, list):
        for value in node:
            yield from walk_refs(value)


# 1-2. Schema packaging, meta-schema validity and $ref resolution.
for name, responsibilities in RESPONSIBILITIES.items():
    path = ORG / name
    if not path.is_file():
        fail(f"missing {rel(path)}")
        continue
    schema = json.loads(path.read_text())
    SCHEMAS[name] = schema
    try:
        Draft202012Validator.check_schema(schema)
    except Exception as error:  # noqa: BLE001 - report any meta-schema failure
        fail(f"{rel(path)} is not a valid Draft 2020-12 schema: {error}")
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        fail(f"{rel(path)} must declare Draft 2020-12")
    if schema.get("$id") != f"{BASE_URI}{name}":
        fail(f"{rel(path)} $id is {schema.get('$id')!r}; expected {BASE_URI}{name}")
    defined = set((schema.get("$defs") or {}).keys())
    if defined != responsibilities:
        missing = sorted(responsibilities - defined)
        extra = sorted(defined - responsibilities)
        fail(f"{rel(path)} $defs mismatch; missing={missing} unexpected={extra}")
    resolver = REGISTRY.resolver(base_uri=schema.get("$id", ""))
    for ref in walk_refs(schema):
        if ref.startswith(("http://", "https://")):
            fail(f"{rel(path)}: use repository-relative $ref, not absolute {ref!r}")
        try:
            resolver.lookup(ref)
        except Exception:  # noqa: BLE001
            fail(f"{rel(path)}: $ref {ref!r} does not resolve")

if failures:
    for message in failures:
        print(f"FAIL: {message}", file=sys.stderr)
    sys.exit(1)

# ADR vocabulary gates.
corporate_vocab = set(SCHEMAS["relationship.schema.json"]["$defs"]["corporateRelationshipType"]["enum"])
if not REQUIRED_CORPORATE_VOCABULARY <= corporate_vocab:
    fail(f"corporateRelationshipType missing {sorted(REQUIRED_CORPORATE_VOCABULARY - corporate_vocab)}")
if corporate_vocab & FORBIDDEN_CORPORATE_VOCABULARY:
    fail(f"corporateRelationshipType must not store inverse, vague or commercial facts: {sorted(corporate_vocab & FORBIDDEN_CORPORATE_VOCABULARY)}")
platform_vocab = set(SCHEMAS["platform.schema.json"]["$defs"]["platformRelationshipType"]["enum"])
if not REQUIRED_PLATFORM_VOCABULARY <= platform_vocab:
    fail(f"platformRelationshipType missing {sorted(REQUIRED_PLATFORM_VOCABULARY - platform_vocab)}")
if "tenant_id" in SCHEMAS["relationship.schema.json"]["$defs"]["CorporateRelationship"]["properties"]:
    fail("CorporateRelationship must not carry tenant_id (ADR-BCP-018 section 17)")
observability = SCHEMAS["observability.schema.json"]["$defs"]
if set(observability["organisationMetric"]["enum"]) != SECTION_130_METRICS:
    fail(f"organisationMetric must be exactly ADR-BCP-018 section 130's catalogue; "
         f"missing={sorted(SECTION_130_METRICS - set(observability['organisationMetric']['enum']))} "
         f"unexpected={sorted(set(observability['organisationMetric']['enum']) - SECTION_130_METRICS)}")
if set(observability["organisationMetricLabel"]["enum"]) & FORBIDDEN_METRIC_LABELS:
    fail(f"organisation metric labels must stay low-cardinality and anonymous: {sorted(set(observability['organisationMetricLabel']['enum']) & FORBIDDEN_METRIC_LABELS)}")
if set(observability["RelationshipDriftFinding"]["properties"]) & FORBIDDEN_EVENT_FIELDS:
    fail("RelationshipDriftFinding must not carry names or evidence (ADR-BCP-018 section 125)")
if "root_organisation_id" in SCHEMAS["relationship.schema.json"]["$defs"]["CorporateGroup"]["required"]:
    fail("CorporateGroup.root_organisation_id must stay optional; a unique root may not exist")

# 3. Examples.
registry_doc = yaml.safe_load((CONTRACTS / "legal-entity" / "registry.yaml").read_text())
FIRST_PARTY = {entity["id"] for entity in registry_doc["entities"]}


def parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def binding_problems(doc: dict) -> list[str]:
    """ORG-07 (ADR-BCP-018 sections 45, 119, 152): a tenant has at most one
    ACTIVE PlatformAccount binding; an ACTIVE binding names a live account
    and the tenant's ACTIVE primary organisation, which holds a live
    membership in that account. Nothing here is inferred from membership:
    the binding must exist explicitly."""
    problems = []
    accounts = {a["id"]: a for a in doc.get("platform_accounts", [])}
    primary = {m["tenant_id"]: m["organisation_id"] for m in doc.get("tenant_organisation_mappings", [])
               if m["mapping_role"] == "PRIMARY_ORGANISATION" and m["status"] == "ACTIVE"}
    members = {(m["platform_account_id"], m["organisation_id"]) for m in doc.get("platform_account_memberships", [])
               if m["status"] in LIVE_ROLE_STATUSES}
    active: dict[str, str] = {}
    for b in doc.get("tenant_platform_account_bindings", []):
        account = accounts.get(b["platform_account_id"])
        if account is None:
            problems.append(f"{b['id']} binds unknown account {b['platform_account_id']}")
            continue
        if b["status"] != "ACTIVE":
            continue
        if b["tenant_id"] in active:
            problems.append(f"{b['id']} and {active[b['tenant_id']]} are both ACTIVE for {b['tenant_id']}")
        active[b["tenant_id"]] = b["id"]
        if account["status"] == "CLOSED":
            problems.append(f"{b['id']} is ACTIVE on CLOSED account {account['id']}")
        org = primary.get(b["tenant_id"])
        if org is None:
            problems.append(f"{b['id']} binds {b['tenant_id']}, which has no ACTIVE primary organisation")
        elif b.get("organisation_id", org) != org:
            problems.append(f"{b['id']} records {b['organisation_id']}, not the tenant's primary organisation {org}")
        elif (b["platform_account_id"], org) not in members:
            problems.append(f"{b['id']}: the tenant's primary organisation {org} holds no live membership in {b['platform_account_id']}")
    return problems


def check_example_semantics(label: str, doc: dict) -> None:
    orgs = {o["canonical_entity_id"]: o for o in doc.get("organisations", [])}
    crs = {c["id"]: c for c in doc.get("corporate_relationships", [])}
    groups = {g["id"] for g in doc.get("corporate_groups", [])}
    accounts = {a["id"] for a in doc.get("platform_accounts", [])}
    les = {p["legal_entity_id"] for p in doc.get("legal_entity_profiles", [])}

    def need_org(where: str, ce: str | None) -> None:
        if ce is not None and ce not in orgs:
            fail(f"{label}: {where} references unknown organisation {ce!r}")

    seen_ids: set[str] = set()
    for key in EXAMPLE_KEYS:
        for record in doc.get(key, []):
            rid = record.get("id")
            if rid is not None:
                if rid in seen_ids:
                    fail(f"{label}: duplicate id {rid!r}")
                seen_ids.add(rid)
            if "effective_to" in record and parse_time(record["effective_to"]) < parse_time(record["effective_from"]):
                fail(f"{label}: {key} {rid or ''} ends before it starts")

    for p in doc.get("legal_entity_profiles", []):
        need_org(f"legal entity {p['legal_entity_id']}", p["organisation_id"])
        if p["legal_entity_id"] == p["organisation_id"]:
            fail(f"{label}: legal_entity_id must differ from organisation_id")
    for c in crs.values():
        need_org(f"{c['id']} source", c["source_organisation_id"])
        need_org(f"{c['id']} target", c["target_organisation_id"])
        if c["source_organisation_id"] == c["target_organisation_id"]:
            fail(f"{label}: {c['id']} relates an organisation to itself")
        for basis in c.get("basis_relationship_ids", []):
            if basis not in crs:
                fail(f"{label}: {c['id']} derives from unknown relationship {basis!r}")
    for g in doc.get("corporate_groups", []):
        need_org(f"{g['id']} root", g.get("root_organisation_id"))
    for m in doc.get("corporate_group_memberships", []):
        need_org(m["id"], m["organisation_id"])
        if m["corporate_group_id"] not in groups:
            fail(f"{label}: {m['id']} references unknown group")
        for basis in m["basis_relationship_ids"]:
            if basis not in crs:
                fail(f"{label}: {m['id']} basis {basis!r} is unknown")
            elif m["status"] == "ACTIVE" and crs[basis]["verification_state"] != "VERIFIED":
                fail(f"{label}: ACTIVE {m['id']} is derived from unverified {basis}")
            elif m["organisation_id"] not in (crs[basis]["source_organisation_id"], crs[basis]["target_organisation_id"]):
                fail(f"{label}: {m['id']} basis {basis} does not involve its organisation")
    for pr in doc.get("platform_relationships", []):
        need_org(pr["id"], pr["organisation_id"])
        if pr["relationship_type"] == "PLATFORM_GROUP_AFFILIATE":
            basis = crs.get(pr["basis_relationship_id"])
            if basis is None:
                fail(f"{label}: {pr['id']} basis is not in the example")
                continue
            if basis["target_organisation_id"] != pr["organisation_id"] or basis["relationship_type"] not in ("OWNS", "CONTROLS"):
                fail(f"{label}: {pr['id']} basis must be an OWNS/CONTROLS fact targeting the affiliate")
            if pr["verification_state"] == "VERIFIED" and basis["verification_state"] != "VERIFIED":
                fail(f"{label}: {pr['id']} is VERIFIED on an unverified corporate basis")
    for a in doc.get("platform_accounts", []):
        need_org(a["id"], a.get("primary_organisation_id"))
    for m in doc.get("platform_account_memberships", []):
        need_org(m["id"], m["organisation_id"])
        if m["platform_account_id"] not in accounts:
            fail(f"{label}: {m['id']} references unknown account")
    for m in doc.get("tenant_organisation_mappings", []):
        need_org(m["id"], m["organisation_id"])
    for problem in binding_problems(doc):
        fail(f"{label}: {problem}")
    defaults: dict[str, int] = {}
    for m in doc.get("tenant_legal_entity_mappings", []):
        if m["legal_entity_id"] not in les:
            fail(f"{label}: {m['id']} maps unknown legal entity {m['legal_entity_id']!r}")
        if m["mapping_role"] == "DEFAULT" and m["status"] == "ACTIVE":
            defaults[m["tenant_id"]] = defaults.get(m["tenant_id"], 0) + 1
    for tenant, count in defaults.items():
        if count > 1:
            fail(f"{label}: tenant {tenant} has {count} active DEFAULT legal-entity mappings")
    # ORG-09: a claim names a known counterparty; a quarantined admission
    # names its candidates and produced nothing else (sections 99-100).
    for req in doc.get("organisation_admission_requests", []):
        for claim in req.get("corporate_relationship_claims", []):
            need_org(f"{req['admission_decision_id']} claim counterparty", claim.get("counterparty_organisation_id"))
    for out in doc.get("organisation_admission_outcomes", []):
        produced = set(out) - {"admission_decision_id", "tenant_id", "identity_resolution", "candidate_organisation_ids"}
        if out["identity_resolution"] == "QUARANTINED":
            if not out.get("candidate_organisation_ids") or produced:
                fail(f"{label}: quarantined admission {out['admission_decision_id']} must list candidates and nothing else (has {sorted(produced)})")
        elif "organisation_id" not in out:
            fail(f"{label}: admission {out['admission_decision_id']} resolved an identity but names no organisation")
        for ce in out.get("candidate_organisation_ids", []):
            need_org(f"{out['admission_decision_id']} candidate", ce)
    # Section 65: one IAM organisation within one issuer is exactly one
    # canonical Organisation; one Organisation may have several.
    live_iam: dict[tuple[str, str, str], str] = {}
    for ref in doc.get("iam_organisation_references", []):
        need_org(ref["id"], ref["organisation_id"])
        if ref["status"] != "ACTIVE":
            continue
        key = (ref["provider"], ref["issuer"], ref["provider_organisation_id"])
        if key in live_iam:
            fail(f"{label}: {ref['id']} and {live_iam[key]} both actively link {key}")
        live_iam[key] = ref["id"]
    # ORG-13: roles are tenant-scoped and unique while live; candidates pair
    # two known organisations that really share every matched governed
    # identifier (names never match), and a decision keeps a candidate's own
    # organisation.
    live_roles: dict[tuple[str, str, str], str] = {}
    for role in doc.get("counterparty_roles", []):
        need_org(role["id"], role["organisation_id"])
        if role["status"] in LIVE_ROLE_STATUSES:
            key = (role["organisation_id"], role["tenant_id"], role["role"])
            if key in live_roles:
                fail(f"{label}: {role['id']} and {live_roles[key]} are both live for {key}")
            live_roles[key] = role["id"]
    governed: dict[str, set[tuple[str, str, str]]] = {}
    for ce, org in orgs.items():
        governed[ce] = {(i["type"], normalise_identifier(i["value"]), i.get("issuing_jurisdiction", "").upper())
                        for i in org.get("identifiers", []) if i["type"] in GOVERNED_IDENTIFIER_TYPES}
    for p in doc.get("legal_entity_profiles", []):
        governed.setdefault(p["organisation_id"], set()).update(
            (i["type"], normalise_identifier(i["value"]), i.get("issuing_jurisdiction", "").upper())
            for i in p.get("registration_identifiers", []) if i["type"] in GOVERNED_IDENTIFIER_TYPES)

    def carries(ce: str, match: dict) -> bool:
        jurisdiction = match.get("issuing_jurisdiction", "")
        return any(t == match["type"] and v == match["normalised_value"] and (not jurisdiction or j in ("", jurisdiction))
                   for t, v, j in governed.get(ce, set()))

    # ORG-15: findings name known organisations; audit entries are unique.
    for finding in doc.get("relationship_drift_findings", []):
        for ce in finding.get("organisation_ids", []):
            need_org(f"drift {finding['resource_id']}", ce)
    audit_ids = [a["audit_id"] for a in doc.get("organisation_audit_entries", [])]
    if len(audit_ids) != len(set(audit_ids)):
        fail(f"{label}: duplicate audit_id")
    pairs: dict[frozenset, str] = {}
    for cand in doc.get("organisation_resolution_candidates", []):
        pair = frozenset(cand["organisation_ids"])
        for ce in pair:
            need_org(cand["id"], ce)
        if pair in pairs:
            fail(f"{label}: {cand['id']} and {pairs[pair]} quarantine the same pair")
        pairs[pair] = cand["id"]
        for match in cand["matched_identifiers"]:
            if not all(carries(ce, match) for ce in pair):
                fail(f"{label}: {cand['id']} matched identifier {match} is not carried by both organisations")
        surviving = (cand.get("decision") or {}).get("surviving_organisation_id")
        if surviving is not None and surviving not in pair:
            fail(f"{label}: {cand['id']} surviving organisation {surviving!r} is not one of its organisations")


examples: dict[str, dict] = {}
for path in sorted((ORG / "examples").glob("*.json")):
    doc = json.loads(path.read_text())
    examples[path.name] = doc
    for key, records in doc.items():
        if key == "_comment":
            continue
        if key not in EXAMPLE_KEYS:
            fail(f"{rel(path)}: unknown example section {key!r}")
            continue
        schema_file, definition = EXAMPLE_KEYS[key]
        for index, record in enumerate(records):
            for error in errors_for(schema_file, definition, record):
                fail(f"{rel(path)} {key}[{index}] vs {definition}: {error}")
    check_example_semantics(rel(path), doc)

nabhold = examples.get("nabhold-group-organisation.json")
acme = examples.get("acme-holdings-external.json")
if nabhold is None or acme is None:
    fail("examples must include nabhold-group-organisation.json and acme-holdings-external.json")
if "organisation-drift-and-audit.json" not in examples:
    fail("examples must include organisation-drift-and-audit.json (ADR-BCP-018 gate ORG-15)")
if "legacy-buyer-supplier-migration.json" not in examples:
    fail("examples must include legacy-buyer-supplier-migration.json (ADR-BCP-018 gate ORG-13)")
else:
    nabhold_les = {p["legal_entity_id"] for p in nabhold["legal_entity_profiles"]}
    if nabhold_les != FIRST_PARTY:
        fail(f"first-party example legal entities {sorted(nabhold_les)} must match the Shared registry {sorted(FIRST_PARTY)}")
    for p in acme["legal_entity_profiles"]:
        if p["legal_entity_id"] in FIRST_PARTY:
            fail(f"external example reuses first-party registry id {p['legal_entity_id']}")
        if not OPAQUE_EXTERNAL_LEGAL_ENTITY.match(p["legal_entity_id"]):
            fail(f"external example legal_entity_id {p['legal_entity_id']!r} should be opaque LE-<token> (ADR-BCP-018 section 12)")
    if any(pr["relationship_type"] != "EXTERNAL_CLIENT" for pr in acme["platform_relationships"]):
        fail("external example organisations must be EXTERNAL_CLIENT; corporate structure does not make them first-party")
    if not any(o["verification_state"] != "VERIFIED" and o["source_authority"] == "applicant-submission" for o in acme["organisations"]):
        fail("external example must show an unreviewed applicant claim remaining unverified")

# 4. Negative fixtures: each mutation MUST be rejected by the schema.
def first(doc_name: str, key: str) -> dict:
    return copy.deepcopy(examples[doc_name][key][0])


def by(doc_name: str, key: str, **match) -> dict:
    for record in examples[doc_name][key]:
        if all(record.get(k) == v for k, v in match.items()):
            return copy.deepcopy(record)
    raise KeyError(f"{doc_name}:{key} has no record matching {match}")


NEGATIVE: list[tuple[str, str, str, dict]] = []


def negative(label: str, schema_file: str, definition: str, record: dict) -> None:
    NEGATIVE.append((label, schema_file, definition, record))


if nabhold is not None and acme is not None and "legacy-buyer-supplier-migration.json" in examples:
    A, N = "acme-holdings-external.json", "nabhold-group-organisation.json"

    r = by(A, "corporate_relationships", verification_state="VERIFIED"); del r["evidence_references"]
    negative("VERIFIED CorporateRelationship without evidence", "relationship.schema.json", "CorporateRelationship", r)
    r = by(A, "corporate_relationships", verification_state="VERIFIED"); del r["verified_by"]
    negative("VERIFIED CorporateRelationship without verifier", "relationship.schema.json", "CorporateRelationship", r)
    r = by(A, "corporate_relationships", verification_state="VERIFIED"); r["evidence_references"] = []
    negative("VERIFIED CorporateRelationship with empty evidence", "relationship.schema.json", "CorporateRelationship", r)
    r = first(A, "corporate_relationships"); r["relationship_type"] = "PARENT_OF"
    negative("stored inverse relationship type", "relationship.schema.json", "CorporateRelationship", r)
    r = first(A, "corporate_relationships"); r["relationship_type"] = "SUPPLIER_OF"
    negative("commercial role as corporate fact", "relationship.schema.json", "CorporateRelationship", r)
    r = first(A, "corporate_relationships"); r["tenant_id"] = "tn_01k8z3v1food"
    negative("tenant-scoped CorporateRelationship", "relationship.schema.json", "CorporateRelationship", r)
    r = first(A, "corporate_relationships"); r["id"] = "map_01k8z3p0food"
    negative("generic mapping id on CorporateRelationship", "relationship.schema.json", "CorporateRelationship", r)
    r = first(A, "corporate_relationships"); r["ownership_percentage"] = 140
    negative("ownership above 100%", "relationship.schema.json", "CorporateRelationship", r)
    r = first(A, "corporate_relationships"); r["direct_or_derived"] = "DERIVED"
    negative("DERIVED fact without lineage", "relationship.schema.json", "CorporateRelationship", r)
    r = first(A, "corporate_relationships"); r["effective_from"] = "15/03/2026"
    negative("non-RFC 3339 effective_from", "relationship.schema.json", "CorporateRelationship", r)
    r = first(A, "corporate_group_memberships"); r["basis_relationship_ids"] = []
    negative("group membership with no basis", "relationship.schema.json", "CorporateGroupMembership", r)
    r = first(A, "corporate_group_memberships"); del r["derivation_version"]
    negative("group membership without derivation version", "relationship.schema.json", "CorporateGroupMembership", r)

    r = first(A, "platform_relationships"); del r["platform_id"]
    negative("PlatformRelationship without platform_id", "platform.schema.json", "PlatformRelationship", r)
    r = by(N, "platform_relationships", relationship_type="PLATFORM_GROUP_AFFILIATE"); del r["basis_relationship_id"]
    negative("PLATFORM_GROUP_AFFILIATE without corporate basis", "platform.schema.json", "PlatformRelationship", r)
    r = first(A, "platform_relationships"); del r["evidence_references"]
    negative("VERIFIED PlatformRelationship without evidence", "platform.schema.json", "PlatformRelationship", r)
    r = first(A, "platform_relationships"); r["relationship_type"] = "INTERNAL"
    negative("subscription type as platform relationship", "platform.schema.json", "PlatformRelationship", r)
    r = first(A, "platform_account_memberships"); r["account_role"] = "ADMIN"
    negative("permission-like PlatformAccount role", "platform.schema.json", "PlatformAccountMembership", r)
    r = first(A, "platform_accounts"); r["tenant_id"] = "tn_01k8z3v1food"
    negative("PlatformAccount carrying a tenant identity", "platform.schema.json", "PlatformAccount", r)
    r = by(A, "tenant_platform_account_bindings", status="ACTIVE"); r["effective_to"] = "2026-05-01T00:00:00Z"
    negative("ACTIVE tenant binding with an end", "platform.schema.json", "TenantPlatformAccountBinding", r)
    r = by(A, "tenant_platform_account_bindings", status="ENDED"); del r["end_reason"]
    negative("ENDED tenant binding without an end reason", "platform.schema.json", "TenantPlatformAccountBinding", r)
    r = by(A, "tenant_platform_account_bindings", status="ACTIVE"); del r["bound_by"]
    negative("tenant binding without its principal", "platform.schema.json", "TenantPlatformAccountBinding", r)
    r = by(A, "tenant_platform_account_bindings", status="ACTIVE"); r["scopes"] = ["trade:read"]
    negative("tenant binding granting access", "platform.schema.json", "TenantPlatformAccountBinding", r)
    r = by(A, "tenant_platform_account_bindings", status="ACTIVE"); r["id"] = "tpab_Acme-Foods"
    negative("human-readable tenant binding id", "platform.schema.json", "TenantPlatformAccountBinding", r)
    r = by(A, "tenant_platform_account_bindings", status="ACTIVE"); r["status"] = "SUSPENDED"
    negative("suspended tenant binding", "platform.schema.json", "TenantPlatformAccountBinding", r)
    negative("account moved back to PENDING", "platform.schema.json", "PlatformAccountStatusChangeRequest",
             {"status": "PENDING", "reason": "reopen"})
    negative("account status change without a reason", "platform.schema.json", "PlatformAccountStatusChangeRequest",
             {"status": "SUSPENDED"})
    negative("binding request naming its tenant's organisation", "platform.schema.json", "TenantPlatformAccountBindingRequest",
             {"platform_account_id": "pacct_01k8z3t0acme", "reason": "x", "organisation_id": "ce_01k8z3m5r2fd"})

    # Semantic negatives: rules a schema cannot express.
    for label, mutate in (
        ("two ACTIVE bindings for one tenant", lambda d: d["tenant_platform_account_bindings"].append(
            dict(by(A, "tenant_platform_account_bindings", status="ACTIVE"), id="tpab_01k8z3w9dupe"))),
        ("ACTIVE binding on a CLOSED account", lambda d: d["platform_accounts"][0].update(status="CLOSED")),
        ("binding inferred without account membership", lambda d: d.update(platform_account_memberships=[
            m for m in d["platform_account_memberships"] if m["organisation_id"] != "ce_01k8z3m5r2fd"])),
        ("binding a tenant without a primary organisation", lambda d: d.update(tenant_organisation_mappings=[])),
    ):
        doc = copy.deepcopy(examples[A])
        mutate(doc)
        if not binding_problems(doc):
            fail(f"semantic negative accepted: {label}")
        NEGATIVE.append((label, "", "", {}))

    r = first(A, "tenant_legal_entity_mappings"); del r["provenance"]
    negative("TenantLegalEntityMapping without provenance", "mapping.schema.json", "TenantLegalEntityMapping", r)
    r = first(A, "tenant_legal_entity_mappings"); del r["mapping_role"]
    negative("TenantLegalEntityMapping without mapping_role", "mapping.schema.json", "TenantLegalEntityMapping", r)
    r = first(A, "tenant_organisation_mappings"); r["id"] = "tom_Acme-Foods"
    negative("human-readable mapping id", "mapping.schema.json", "TenantOrganisationMapping", r)
    r = first(A, "tenant_organisation_mappings"); r["tenant_id"] = "acme-foods"
    negative("non-opaque tenant id", "mapping.schema.json", "TenantOrganisationMapping", r)

    r = by(A, "legal_entity_profiles", legal_entity_id="LE-01K8Z3M5R2FD"); del r["evidence_references"]
    negative("VERIFIED LegalEntityProfile without evidence", "domain.schema.json", "LegalEntityProfile", r)
    r = first(A, "organisations"); r["organisation_form"] = "SUPPLIER"
    negative("commercial role as organisation form", "domain.schema.json", "Organisation", r)
    r = first(A, "organisations"); r["jurisdiction"] = "Kenya"
    negative("non-ISO jurisdiction", "domain.schema.json", "Organisation", r)

    r = by(A, "iam_organisation_references", status="ACTIVE"); del r["issuer"]
    negative("IamOrganisationReference without issuer", "iam.schema.json", "IamOrganisationReference", r)
    r = by(A, "iam_organisation_references", status="ACTIVE"); r["issuer"] = "http://id.baobab-platform.com/realms/baobab"
    negative("non-HTTPS IAM issuer", "iam.schema.json", "IamOrganisationReference", r)
    r = by(A, "iam_organisation_references", status="ACTIVE"); r["id"] = "iamorg_Acme-Foods"
    negative("human-readable IamOrganisationReference id", "iam.schema.json", "IamOrganisationReference", r)
    r = by(A, "iam_organisation_references", status="ACTIVE"); r["status"] = "DELETED"
    negative("IamOrganisationReference deleted instead of retired", "iam.schema.json", "IamOrganisationReference", r)
    r = by(A, "iam_organisation_references", status="ACTIVE"); r["provider"] = "okta"
    negative("unregistered IAM provider", "iam.schema.json", "IamOrganisationReference", r)
    negative("IAM evidence smuggling a canonical organisation_id", "iam.schema.json", "IamOrganisationEvidence",
             {"provider": "keycloak", "issuer": "https://id.baobab-platform.com/realms/baobab",
              "provider_organisation_id": "7f1c2a9e-3b4d-4e8f-9a1b-2c3d4e5f6a7b", "organisation_id": "ce_01k8z3m5r2fd"})
    negative("IAM evidence without a provider organisation id", "iam.schema.json", "IamOrganisationEvidence",
             {"provider": "keycloak", "issuer": "https://id.baobab-platform.com/realms/baobab"})
    # Admin API requests (ORG-10): the Organisation comes from the path and
    # the source authority from the Control Plane, never the body.
    link = {"provider": "keycloak", "issuer": "https://id.baobab-platform.com/realms/baobab",
            "provider_organisation_id": "7f1c2a9e-3b4d-4e8f-9a1b-2c3d4e5f6a7b"}
    for error in errors_for("iam.schema.json", "IamOrganisationLinkRequest", link):
        fail(f"a valid IAM organisation link request is rejected: {error}")
    negative("IAM link request naming its organisation", "iam.schema.json", "IamOrganisationLinkRequest",
             {**link, "organisation_id": "ce_01k8z3m5r2fd"})
    negative("IAM link request naming its source authority", "iam.schema.json", "IamOrganisationLinkRequest",
             {**link, "source_authority": "applicant"})
    negative("IAM link retirement without a reason", "iam.schema.json", "IamOrganisationRetireRequest", {"reason": "  "})
    negative("alias-only organization claim", "iam.schema.json", "keycloakOrganizationClaim", ["acme-foods"])
    negative("organization claim entry without id", "iam.schema.json", "keycloakOrganizationClaim", {"acme-foods": {}})
    negative("empty organization claim", "iam.schema.json", "keycloakOrganizationClaim", {})

    # Admission (ORG-09): nothing an applicant could use to self-classify or
    # to smuggle verified facts is accepted.
    r = first(A, "organisation_admission_requests"); r["platform_relationship_type"] = "PLATFORM_GROUP_AFFILIATE"
    negative("admission request self-classifying its platform relationship", "admission.schema.json", "OrganisationAdmissionRequest", r)
    r = first(A, "organisation_admission_requests"); r["applicant_organisation"]["verification_state"] = "VERIFIED"
    negative("applicant organisation claiming to be verified", "admission.schema.json", "OrganisationAdmissionRequest", r)
    r = first(A, "organisation_admission_requests"); r["corporate_relationship_claims"][0]["verification_state"] = "VERIFIED"
    negative("corporate relationship claim asserting verification", "admission.schema.json", "OrganisationAdmissionRequest", r)
    r = first(A, "organisation_admission_requests"); r["applicant_organisation"]["registration_identifiers"] = []
    negative("applicant without governed identifiers", "admission.schema.json", "OrganisationAdmissionRequest", r)
    r = first(A, "organisation_admission_requests"); r["identity_resolution"] = {"decision": "USE_EXISTING_ORGANISATION", "reason": "same company"}
    negative("existing-organisation resolution without an organisation", "admission.schema.json", "OrganisationAdmissionRequest", r)
    r = first(A, "organisation_admission_requests"); r["corporate_relationship_claims"][0]["counterparty_identifiers"] = [{"type": "LEI", "value": "5493001KJTIIGC8Y1R12"}]
    negative("corporate relationship claim naming two counterparties", "admission.schema.json", "OrganisationAdmissionRequest", r)
    r = first(A, "organisation_admission_requests"); r["platform_account"] = {"mode": "NEW_ACCOUNT"}
    negative("new PlatformAccount without a name", "admission.schema.json", "OrganisationAdmissionRequest", r)
    r = first(A, "organisation_admission_requests"); r["platform_account"] = {"mode": "EXISTING_ACCOUNT"}
    negative("existing PlatformAccount without an id", "admission.schema.json", "OrganisationAdmissionRequest", r)
    r = first(A, "organisation_admission_requests"); r["platform_account"]["account_role"] = "ADMIN"
    negative("permission-like PlatformAccount role at admission", "admission.schema.json", "OrganisationAdmissionRequest", r)
    r = first(A, "organisation_admission_requests"); del r["admission_decision_id"]
    negative("admission onboarding without a decision", "admission.schema.json", "OrganisationAdmissionRequest", r)

    # Counterparty roles and resolution candidates (ORG-13).
    L = "legacy-buyer-supplier-migration.json"
    r = first(L, "counterparty_roles"); r["role"] = "BUYER_ORGANISATION"
    negative("legacy entity kind as counterparty role", "counterparty.schema.json", "CounterpartyRole", r)
    r = first(L, "counterparty_roles"); del r["tenant_id"]
    negative("platform-wide counterparty role", "counterparty.schema.json", "CounterpartyRole", r)
    r = first(L, "counterparty_roles"); r["portal_access"] = True
    negative("counterparty role granting access", "counterparty.schema.json", "CounterpartyRole", r)
    r = by(L, "counterparty_roles", status="ENDED"); del r["effective_to"]
    negative("ENDED counterparty role without effective_to", "counterparty.schema.json", "CounterpartyRole", r)
    r = first(L, "counterparty_roles"); r["id"] = "crole_ZuriBeans-Buyer"
    negative("human-readable counterparty role id", "counterparty.schema.json", "CounterpartyRole", r)
    r = by(L, "organisation_resolution_candidates", status="OPEN"); r["matched_identifiers"] = [{"type": "LEGAL_NAME", "normalised_value": "ACMEFOODS"}]
    negative("resolution candidate matched on a name", "counterparty.schema.json", "OrganisationResolutionCandidate", r)
    r = by(L, "organisation_resolution_candidates", status="OPEN"); r["matched_identifiers"] = []
    negative("resolution candidate without a matched identifier", "counterparty.schema.json", "OrganisationResolutionCandidate", r)
    r = by(L, "organisation_resolution_candidates", status="OPEN"); r["organisation_ids"] = r["organisation_ids"][:1]
    negative("resolution candidate with one organisation", "counterparty.schema.json", "OrganisationResolutionCandidate", r)
    r = by(L, "organisation_resolution_candidates", status="OPEN"); r["organisation_ids"] = [r["organisation_ids"][0]] * 2
    negative("resolution candidate pairing an organisation with itself", "counterparty.schema.json", "OrganisationResolutionCandidate", r)
    r = by(L, "organisation_resolution_candidates", status="OPEN"); r["matched_identifiers"][0]["normalised_value"] = "pvt-2019/0443"
    negative("un-normalised matched identifier", "counterparty.schema.json", "OrganisationResolutionCandidate", r)
    r = by(L, "organisation_resolution_candidates", status="DISTINCT"); r["status"] = "OPEN"
    negative("OPEN resolution candidate carrying a decision", "counterparty.schema.json", "OrganisationResolutionCandidate", r)
    r = by(L, "organisation_resolution_candidates", status="DISTINCT"); del r["decided_by"]
    negative("decided resolution candidate without a reviewer", "counterparty.schema.json", "OrganisationResolutionCandidate", r)
    r = by(L, "organisation_resolution_candidates", status="DISTINCT"); r["status"] = "DUPLICATE_CONFIRMED"
    negative("candidate status disagreeing with its decision", "counterparty.schema.json", "OrganisationResolutionCandidate", r)
    r = by(L, "organisation_resolution_candidates", status="DISTINCT"); r["status"] = "MERGED"
    negative("resolution candidate claiming a merge", "counterparty.schema.json", "OrganisationResolutionCandidate", r)
    negative("duplicate confirmation without a surviving organisation", "counterparty.schema.json", "ResolutionCandidateDecision",
             {"decision": "DUPLICATE_CONFIRMED", "reason": "same registry entry"})
    negative("DISTINCT decision naming a surviving organisation", "counterparty.schema.json", "ResolutionCandidateDecision",
             {"decision": "DISTINCT", "reason": "different companies", "surviving_organisation_id": "ce_01k8z4b1hq2m"})
    negative("decision naming its own reviewer", "counterparty.schema.json", "ResolutionCandidateDecision",
             {"decision": "DISTINCT", "reason": "different companies", "decided_by": "prn_01k8z4f1rvwr"})
    negative("decision without a reason", "counterparty.schema.json", "ResolutionCandidateDecision", {"decision": "DISTINCT"})
    # Admin API requests (ORG-13): the tenant comes from the path and the
    # source authority from the Control Plane; a new role is never ENDED.
    assign = {"organisation_id": "ce_01k8z3m5r2fd", "role": "BUYER"}
    for error in errors_for("counterparty.schema.json", "CounterpartyRoleAssignRequest", assign):
        fail(f"a valid counterparty role assignment is rejected: {error}")
    negative("counterparty role created ENDED", "counterparty.schema.json", "CounterpartyRoleAssignRequest",
             {**assign, "status": "ENDED"})
    negative("counterparty role assignment naming its tenant", "counterparty.schema.json", "CounterpartyRoleAssignRequest",
             {**assign, "tenant_id": "tn_01k8z3m5r2fd"})
    negative("counterparty role assignment naming its source authority", "counterparty.schema.json",
             "CounterpartyRoleAssignRequest", {**assign, "source_authority": "applicant"})
    negative("counterparty role ended without a reason", "counterparty.schema.json", "CounterpartyRoleEndRequest", {})

    # Drift and audit lineage (ORG-15).
    D = "organisation-drift-and-audit.json"
    if D in examples:
        r = first(D, "relationship_drift_findings"); r["auto_repairable"] = True
        negative("auto-repairable relationship drift", "observability.schema.json", "RelationshipDriftFinding", r)
        r = first(D, "relationship_drift_findings"); r["remediation"] = "CASCADE"
        negative("drift remediated by cascade", "observability.schema.json", "RelationshipDriftFinding", r)
        r = first(D, "relationship_drift_findings"); r["display_name"] = "Illustrative Subsidiary"
        negative("drift finding carrying an organisation name", "observability.schema.json", "RelationshipDriftFinding", r)
        r = first(D, "relationship_drift_findings"); r["severity"] = "HIGH"
        negative("drift severity outside ADR-BCP-008", "observability.schema.json", "RelationshipDriftFinding", r)
        r = first(D, "relationship_drift_findings"); r["rule"] = "SOMETHING_ODD"
        negative("unregistered drift rule", "observability.schema.json", "RelationshipDriftFinding", r)
        r = first(D, "organisation_audit_entries"); del r["actor"]
        negative("audit entry without an actor", "observability.schema.json", "OrganisationAuditEntry", r)
        r = first(D, "organisation_audit_entries"); r["action"] = "Verified Ownership"
        negative("free-text audit action", "observability.schema.json", "OrganisationAuditEntry", r)
        negative("metric outside the section 130 catalogue", "observability.schema.json", "organisationMetric", "organisation_names_total")
        negative("organisation id as a metric label", "observability.schema.json", "organisationMetricLabel", "organisation_id")

    # Positive: the claim form and the evidence derived from it.
    claim = {"acme-foods": {"id": "7f1c2a9e-3b4d-4e8f-9a1b-2c3d4e5f6a7b"}}
    for error in errors_for("iam.schema.json", "keycloakOrganizationClaim", claim):
        fail(f"sample Keycloak organization claim rejected: {error}")
    evidence = {"provider": "keycloak", "issuer": "https://id.baobab-platform.com/realms/baobab",
                "provider_organisation_id": claim["acme-foods"]["id"]}
    for error in errors_for("iam.schema.json", "IamOrganisationEvidence", evidence):
        fail(f"sample IAM organisation evidence rejected: {error}")

for label, schema_file, definition, record in NEGATIVE:
    if schema_file and not errors_for(schema_file, definition, record):
        fail(f"negative fixture accepted: {label}")

# 5. Events: asyncapi registration, envelope composition and payload privacy.
asyncapi = yaml.safe_load((ORG / "asyncapi.yaml").read_text())
messages = (asyncapi.get("components") or {}).get("messages") or {}
channel_refs = {m.get("$ref", "").rsplit("/", 1)[-1]
                for ch in (asyncapi.get("channels") or {}).values()
                for m in (ch.get("messages") or {}).values()}
registered: dict[str, str] = {}
for key, message in messages.items():
    name = message.get("name", "")
    layers = ((message.get("payload") or {}).get("allOf")) or []
    envelope = [layer for layer in layers if isinstance(layer, dict) and layer.get("$ref") == ENVELOPE_REF]
    data_refs = [layer.get("properties", {}).get("data", {}).get("$ref", "") for layer in layers if isinstance(layer, dict)]
    data_refs = [ref for ref in data_refs if ref]
    if not envelope:
        fail(f"asyncapi message {key} is not composed with {ENVELOPE_REF}")
    if len(data_refs) != 1 or not data_refs[0].startswith("./events.schema.json#/$defs/"):
        fail(f"asyncapi message {key} must take its data from ./events.schema.json#/$defs/<Event>")
        continue
    definition = data_refs[0].rsplit("/", 1)[-1]
    if definition not in RESPONSIBILITIES["events.schema.json"]:
        fail(f"asyncapi message {key} data $def {definition!r} does not exist")
    if key not in channel_refs:
        fail(f"asyncapi message {key} is not published on any channel")
    registered[name] = definition
if registered != EVENT_TYPES:
    missing = sorted(set(EVENT_TYPES) - set(registered))
    unexpected = sorted(set(registered) - set(EVENT_TYPES))
    wrong = sorted(n for n in set(registered) & set(EVENT_TYPES) if registered[n] != EVENT_TYPES[n])
    fail(f"asyncapi events differ from ADR-BCP-018 section 124; missing={missing} unexpected={unexpected} wrong_payload={wrong}")
envelope_schema = json.loads((CONTRACTS / "events" / "v1" / "envelope.schema.json").read_text())
type_pattern = re.compile(envelope_schema["properties"]["type"]["pattern"])
for name in registered:
    if not type_pattern.match(name):
        fail(f"event type {name!r} violates the canonical envelope pattern (ADR-SHARED-008)")
for definition, schema in SCHEMAS["events.schema.json"]["$defs"].items():
    leaked = FORBIDDEN_EVENT_FIELDS & set(schema.get("properties", {}))
    if leaked:
        fail(f"event payload {definition} publishes {sorted(leaked)} (ADR-BCP-018 section 125)")
    if schema.get("additionalProperties") is not False:
        fail(f"event payload {definition} must set additionalProperties: false")


def event_errors(envelope: dict) -> list[str]:
    definition = EVENT_TYPES.get(envelope.get("type", ""))
    if definition is None:
        return [f"type {envelope.get('type')!r} is not a registered organisation event"]
    composed = {"allOf": [
        {"$ref": "https://contracts.baobab-platform.com/events/v1/envelope.schema.json"},
        {"type": "object", "properties": {"data": {"$ref": f"{BASE_URI}events.schema.json#/$defs/{definition}"}}},
    ]}
    validator = Draft202012Validator(composed, registry=REGISTRY, format_checker=FORMATS)
    return [f"{'/'.join(str(p) for p in e.absolute_path) or '<root>'}: {e.message}" for e in validator.iter_errors(envelope)]


event_examples = sorted((ORG / "examples" / "events").glob("*.json"))
if not event_examples:
    fail("examples/events must contain at least one event envelope")
seen_types: set[str] = set()
for path in event_examples:
    envelope = json.loads(path.read_text())
    seen_types.add(envelope.get("type", ""))
    for error in event_errors(envelope):
        fail(f"{rel(path)}: {error}")

if event_examples:
    sample = json.loads(event_examples[0].read_text())
    event_negatives = []
    leaked = copy.deepcopy(sample); leaked["data"]["evidence_references"] = ["evd_x"]
    event_negatives.append(("event payload leaking evidence references", leaked))
    legacy = copy.deepcopy(sample); legacy["type"] = legacy["type"].replace("com.baobab-platform.", "com.nabhold.")
    event_negatives.append(("legacy com.nabhold event type", legacy))
    missing_id = copy.deepcopy(sample); missing_id["data"] = {}
    event_negatives.append(("event payload without identifiers", missing_id))
    for label, envelope in event_negatives:
        NEGATIVE.append((label, "", "", {}))
        if not event_errors(envelope):
            fail(f"negative fixture accepted: {label}")

# 6. Lock registration.
lock = yaml.safe_load((ROOT / "contracts.lock.yaml").read_text())
entries = [c for c in lock.get("contracts", []) if c.get("domain") == "organisation" and c.get("version") == "v1"]
if len(entries) != 1:
    fail("contracts.lock.yaml must register organisation v1 exactly once")
elif set(entries[0].get("schemas", [])) != set(RESPONSIBILITIES):
    fail(f"contracts.lock.yaml organisation v1 schemas {entries[0].get('schemas')} must be {sorted(RESPONSIBILITIES)}")

if failures:
    for message in failures:
        print(f"FAIL: {message}", file=sys.stderr)
    print(f"{len(failures)} organisation contract failure(s)", file=sys.stderr)
    sys.exit(1)

print(f"organisation/v1 contracts passed ({len(NEGATIVE)} negative fixtures rejected)")
