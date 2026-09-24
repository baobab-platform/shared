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
  5. contracts.lock.yaml registers exactly these schemas.

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
        "platformRelationshipId", "platformAccountId", "platformAccountMembershipId",
        "tenantOrganisationMappingId", "tenantLegalEntityMappingId", "platformId",
        "evidenceReference", "relationshipClassification",
    },
    "relationship.schema.json": {
        "CorporateRelationship", "CorporateGroup", "CorporateGroupMembership",
        "corporateRelationshipType", "relationshipStatus",
    },
    "platform.schema.json": {
        "PlatformRelationship", "PlatformAccount", "PlatformAccountMembership",
        "platformRelationshipType", "platformAccountRole",
    },
    "mapping.schema.json": {
        "TenantOrganisationMapping", "TenantLegalEntityMapping", "mappingStatus",
        "tenantOrganisationMappingRole", "tenantLegalEntityMappingRole",
    },
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
    "tenant_organisation_mappings": ("mapping.schema.json", "TenantOrganisationMapping"),
    "tenant_legal_entity_mappings": ("mapping.schema.json", "TenantLegalEntityMapping"),
}

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
if "root_organisation_id" in SCHEMAS["relationship.schema.json"]["$defs"]["CorporateGroup"]["required"]:
    fail("CorporateGroup.root_organisation_id must stay optional; a unique root may not exist")

# 3. Examples.
registry_doc = yaml.safe_load((CONTRACTS / "legal-entity" / "registry.yaml").read_text())
FIRST_PARTY = {entity["id"] for entity in registry_doc["entities"]}


def parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


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
    defaults: dict[str, int] = {}
    for m in doc.get("tenant_legal_entity_mappings", []):
        if m["legal_entity_id"] not in les:
            fail(f"{label}: {m['id']} maps unknown legal entity {m['legal_entity_id']!r}")
        if m["mapping_role"] == "DEFAULT" and m["status"] == "ACTIVE":
            defaults[m["tenant_id"]] = defaults.get(m["tenant_id"], 0) + 1
    for tenant, count in defaults.items():
        if count > 1:
            fail(f"{label}: tenant {tenant} has {count} active DEFAULT legal-entity mappings")


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


if nabhold is not None and acme is not None:
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

for label, schema_file, definition, record in NEGATIVE:
    if not errors_for(schema_file, definition, record):
        fail(f"negative fixture accepted: {label}")

# 5. Lock registration.
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
