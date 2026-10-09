#!/usr/bin/env python3
"""LA-01 canonical contract conformance for ADR-BCP-026/027.

V1 APIs remain *wire-compatible*, pinned consumers do not automatically upgrade.
V2 schemas define governed future inputs/outputs; this script must never be
mistaken for proof of a running Control Plane implementation.
"""
from __future__ import annotations

import json
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = ROOT / "contracts"
BASE = "https://contracts.baobab-platform.com/"
ORG = "0199a1b2-c3d4-7e8f-9a0b-1c2d3e4f5a6b"
NABHOLD_ORG = "0199a1b2-c3d4-7e8f-9a0b-1c2d3e4f5a6c"
TENANT = "tn_01kaabbccddeeff"
MANDATE = "0199a1b2-c3d4-7e8f-9a0b-1c2d3e4f5a6d"
SPONSORSHIP = "0199a1b2-c3d4-7e8f-9a0b-1c2d3e4f5a6e"
DATE = "2026-10-09T09:00:00Z"
END = "2027-10-09T09:00:00Z"
FILES = {
    "organisation/v2/legal-actor-mandate.schema.json",
    "organisation/v2/pre-tenant-admission.schema.json",
    "organisation/v2/founding-admission.schema.json",
    "admission/v2/business-identity.schema.json",
    "control-plane/v2/tenant-registration.schema.json",
    "control-plane/v2/context-resolution.schema.json",
}
LOCKED = {
    ("organisation", "v2"): {
        "legal-actor-mandate.schema.json",
        "pre-tenant-admission.schema.json",
        "founding-admission.schema.json",
    },
    ("admission", "v2"): {"business-identity.schema.json"},
    ("control-plane", "v2"): {
        "tenant-registration.schema.json",
        "context-resolution.schema.json",
    },
}


def require(condition: bool, detail: str) -> None:
    if not condition:
        raise AssertionError(detail)


def read(relative: str) -> dict:
    return json.loads((CONTRACTS / relative).read_text())


def registry() -> Registry:
    result = Registry()
    for path in sorted(CONTRACTS.rglob("*.schema.json")):
        doc = json.loads(path.read_text())
        if isinstance(doc, dict) and doc.get("$id"):
            result = result.with_resource(doc["$id"], Resource.from_contents(doc))
    return result


REGISTRY = registry()
FORMATS = FormatChecker()


def errors(relative: str, fragment: str | None, value: dict) -> list[str]:
    uri = BASE + relative + ("#/$defs/" + fragment if fragment else "")
    validator = Draft202012Validator({"$ref": uri}, registry=REGISTRY, format_checker=FORMATS)
    return sorted(e.message for e in validator.iter_errors(value))


def accepts(relative: str, fragment: str | None, value: dict, scenario: str) -> None:
    violations = errors(relative, fragment, value)
    require(not violations, f"{scenario}: expected valid; got {violations}")


def rejects(relative: str, fragment: str | None, value: dict, scenario: str) -> None:
    require(bool(errors(relative, fragment, value)), f"{scenario}: expected rejection")


for relative in FILES:
    doc = read(relative)
    Draft202012Validator.check_schema(doc)
    require(doc.get("$id") == BASE + relative, f"Bad schema $id: {relative}")
    require(doc.get("$schema") == "https://json-schema.org/draft/2020-12/schema", relative)

lock = yaml.safe_load((ROOT / "contracts.lock.yaml").read_text())
for (domain, version), names in LOCKED.items():
    matching = [e for e in lock["contracts"] if e["domain"] == domain and e["version"] == version]
    require(len(matching) == 1, f"Contract lock lacks unique {domain}/{version}")
    require(set(matching[0]["schemas"]) == names, f"Contract lock mismatch {domain}/{version}")

tenancy = yaml.safe_load((CONTRACTS / "tenancy/tenancy.yaml").read_text())
policy = tenancy["tenant_definition"]
require(tenancy["schema"]["version"] == "2.0", "Tenancy not v2")
require(policy["organisation_is_primary_boundary"] is True, "Organisation not PRIMARY")
require(policy["requires_active_primary_organisation"] is True, "PRIMARY mapping not mandatory")
require(policy["requires_default_active_canonical_legal_entity"] is False, "Legacy legal actor still universal")
require(policy["requires_legal_actor_for_restricted_operations"] is True, "Legal actor enforcement lost")
require(tenancy["identifiers"]["organisation_id"]["required"] is True, "No canonical Organisation")
require(tenancy["identifiers"]["entity_id"]["required"] is False, "Legacy entity not optional")

# V1 remains intact for consumers with pinned Shared hashes.
old_reg = read("control-plane/v1/tenant-registration.schema.json")
old_context = read("control-plane/v1/context-resolution.schema.json")
require("legal_entity_id" in old_reg["required"], "v1 register inadvertently loosened")
require("organisation_id" not in old_reg["required"], "v1 register unexpectedly changed")
require("entity_id" in old_context["$defs"]["response"]["required"], "v1 context drift")
reg = "control-plane/v2/tenant-registration.schema.json"
ctx = "control-plane/v2/context-resolution.schema.json"
business = "admission/v2/business-identity.schema.json"
pre = "organisation/v2/pre-tenant-admission.schema.json"
actor = "organisation/v2/legal-actor-mandate.schema.json"
founding = "organisation/v2/founding-admission.schema.json"

registration = {
    "tenant_onboarding_request_id": "tor_01kaabc",
    "organisation_id": ORG,
    "display_name": "ZuriBeans",
    "isolation_strategy": "schema_per_tenant",
    "residency_region": "af-south-1",
}
accepts(reg, None, registration, "Organisation-only v2 tenant")
accepts(reg, None, {**registration, "legal_entity_id": "NABHOLD"}, "optional real LEGAL actor")
rejects(reg, None, {k: v for k, v in registration.items() if k != "organisation_id"}, "no PRIMARY")
rejects(reg, None, {**registration, "tenant_id": TENANT}, "caller-chosen tenant id")
rejects(reg, None, {**registration, "organisation_id": "ZURIBEANS"}, "using legal id as Organisation UUID")
rejects(reg, None, {**registration, "legal_entity_id": "zuribeans_za"}, "alias not canonical v2")
rejects(reg, None, {k: v for k, v in registration.items() if k != "tenant_onboarding_request_id"}, "no authorised request")
rejects("control-plane/v1/tenant-registration.schema.json", None, registration, "legacy v1 must not silently accept v2")

identity = {
    "operating_name": "ZuriBeans",
    "organisation_form": "UNINCORPORATED_ORGANISATION",
    "operating_country": "ZA",
    "incorporation_claim": "NOT_INCORPORATED",
    "authorised_representative": {"full_name": "Approved Representative", "role": "Manager"},
    "proposed_responsible_organisation_id": NABHOLD_ORG,
}
accepts(business, "BusinessIdentity", identity, "pre-incorporation without CIPC number")
accepts(business, "BusinessIdentity", {**identity, "operating_name": "Equator & Estate Co."}, "Equator")
accepts(business, "BusinessIdentity", {
    **identity, "operating_name": "Thamani Global", "organisation_form": "COMPANY",
    "incorporation_claim": "INCORPORATED_CLAIMED", "legal_name": "Thamani Global",
    "jurisdiction_of_incorporation": "ZA",
    "registration_identifiers": [{"type": "COMPANY_REGISTRATION", "value": "CLAIMED-ONLY"}],
}, "Thamani incorporation claim is not verification")
rejects(business, "BusinessIdentity", {**identity, "incorporation_claim": "INCORPORATED_CLAIMED"}, "company with no identifiers")
rejects(business, "BusinessIdentity", {**identity, "jurisdiction_of_incorporation": "ZA"}, "false non-incorporation jurisdiction")
rejects(business, "BusinessIdentity", {**identity, "verified": True}, "client cannot claim verification")
rejects(business, "BusinessIdentity", {**identity, "legal_entity_id": "ZURIBEANS"}, "client cannot create legal profile")
accepts(pre, "PreTenantOrganisationResolution", {
    "admission_decision_id": "adm_01kaab", "identity": identity,
    "resolution_outcome": "NEW_ORGANISATION", "organisation_id": ORG,
    "evaluated_at": DATE, "source_authority": "control-plane-reviewed",
}, "Organisation exists before Tenant")
rejects(pre, "PreTenantOrganisationResolution", {
    "admission_decision_id": "adm_01kaab", "identity": identity,
    "resolution_outcome": "NEW_ORGANISATION", "organisation_id": ORG,
    "evaluated_at": DATE, "source_authority": "control-plane-reviewed",
    "tenant_id": TENANT,
}, "pretenant must not mint a Tenant")

primary = {
    "tenant_id": TENANT, "primary_organisation_id": ORG,
    "primary_mapping_id": "tom_01kaabc",
    "mapping_status": "ACTIVE", "effective_from": DATE,
}
accepts(pre, "TenantPrimaryOrganisation", primary, "PRIMARY with no default LegalEntity")
accepts(pre, "TenantPrimaryOrganisation", {
    **primary, "default_legal_entity_id": "NABHOLD",
    "default_legal_entity_mapping_id": "tlem_01kaabc",
}, "Nabhold legal actor but ZuriBeans PRIMARY")
rejects(pre, "TenantPrimaryOrganisation", {
    **primary, "default_legal_entity_id": "NABHOLD",
}, "projection without explicit mapping")

mandate = {
    "mandate_id": MANDATE, "tenant_id": TENANT,
    "operating_organisation_id": ORG,
    "responsible_legal_entity_id": "NABHOLD",
    "roles": ["SELLER_OF_RECORD"], "activity_scope": ["b2b-trade"],
    "market_scope": ["ZA"], "status": "ACTIVE",
    "authority_basis_reference": "approval/mandate-001",
    "evidence_references": ["evidence/review-001"],
    "legal_actor_verification_reference": "evidence/nabhold-registration",
    "effective_from": DATE, "effective_to": END,
    "approved_by": "principal-independent-reviewer",
    "approved_at": DATE, "created_at": DATE,
}
accepts(actor, "OperatingLegalActorMandate", mandate, "scoped Nabhold seller mandate")
rejects(actor, "OperatingLegalActorMandate", {k:v for k,v in mandate.items() if k != "approved_by"}, "active unapproved mandate")
rejects(actor, "OperatingLegalActorMandate", {**mandate, "market_scope": []}, "mandate without market")
rejects(actor, "OperatingLegalActorMandate", {**mandate, "roles": []}, "mandate without a role")
rejects(actor, "OperatingLegalActorMandate", {**mandate, "tenant_id": ""}, "mandate without tenant scope")
req = {"tenant_id": TENANT, "operating_organisation_id": ORG, "role": "SELLER_OF_RECORD", "activity": "b2b-trade", "market": "ZA", "effective_at": DATE}
accepts(actor, "LegalActorResolutionRequest", req, "trusted role lookup")
rejects(actor, "LegalActorResolutionRequest", {**req, "legal_entity_id": "NABHOLD"}, "caller-chosen actor")
accepts(actor, "LegalActorResolution", {
    "outcome": "AUTHORIZED", "evaluated_at": DATE,
    "policy_reference": "policy/legal-actor-1",
    "mandate_id": MANDATE, "responsible_legal_entity_id": "NABHOLD",
    "evidence_references": ["evidence/review-001"], "valid_until": END,
}, "scoped actor resolution")
rejects(actor, "LegalActorResolution", {
    "outcome": "AUTHORIZED", "evaluated_at": DATE,
    "policy_reference": "policy/legal-actor-1",
}, "authorised without mandate")
rejects(actor, "LegalActorResolution", {
    "outcome": "AMBIGUOUS", "evaluated_at": DATE,
    "policy_reference": "policy/legal-actor-1",
    "responsible_legal_entity_id": "NABHOLD",
}, "ambiguous result leaks actor")

accepts(ctx, "response", {
    "tenant_id": TENANT, "organisation_id": ORG, "lifecycle_status": "active",
    "product_id": "baobab-trade", "entitled": True, "cache_ttl_seconds": 30,
    "resolved_at": DATE, "correlation_id": MANDATE,
}, "v2 entitlement without legal entity")
rejects(ctx, "response", {
    "tenant_id": TENANT, "lifecycle_status": "active",
    "product_id": "baobab-trade", "entitled": True, "cache_ttl_seconds": 30,
    "resolved_at": DATE, "correlation_id": MANDATE,
}, "missing primary Organisation context")
rejects(ctx, "request", {"product_id": "baobab-trade", "legal_entity_id": "NABHOLD"}, "client override in context")

sponsor = {
    "id": SPONSORSHIP, "sponsor_organisation_id": NABHOLD_ORG,
    "operating_organisation_id": ORG, "platform_id": "baobab-platform",
    "status": "ACTIVE", "scope": "INTERNAL_GROUP_ADMISSION",
    "authority_basis_reference": "governance/founding-sponsorship-001",
    "approved_by": "principal-independent-reviewer", "approved_at": DATE,
    "effective_from": DATE, "effective_to": END,
    "provenance": "group-governance/2026-10-09",
}
accepts(founding, "FoundingGroupSponsorship", sponsor, "founding admission")
rejects(founding, "FoundingGroupSponsorship", {**sponsor, "scope": "UNRESTRICTED_ACCESS"}, "no IAM privilege from sponsorship")
defer = {
    "id": MANDATE, "organisation_id": ORG, "sponsorship_id": SPONSORSHIP,
    "requirement_ids": ["platform-documentary-requirement-1"],
    "policy_reference": "policy/founding-grace-v1",
    "approved_by": "principal-independent-reviewer", "approved_at": DATE,
    "effective_from": DATE, "expires_at": END,
    "maximum_duration_months": 12, "status": "ACTIVE",
}
accepts(founding, "FoundingDocumentaryDeferral", defer, "bounded named documentary grace")
rejects(founding, "FoundingDocumentaryDeferral", {**defer, "maximum_duration_months": 24}, "no 24-month grace")
rejects(founding, "FoundingDocumentaryDeferral", {**defer, "requirement_ids": []}, "no global blanket exemption")

print("LA-01 Organisation-first v2, founding sponsorship, actor and compatibility contracts passed")
