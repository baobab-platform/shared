# Organisation, Corporate Group, Platform Account and Tenant Relationship Contracts

**Governing ADR:** ADR-BCP-018 — Canonical Organisation, Corporate Group, Platform Account and Tenant Relationship Model (`baobab-platform/baobab-cp`)

**Contract authority:** `baobab-platform/shared`
**Runtime authority:** `baobab-platform/baobab-cp`
**First-party governance source:** `contracts/legal-entity/registry.yaml` (Nabhold Group Africa identities only)

## Purpose

These contracts make Shared the schema authority for the generic organisation and relationship model. The Control Plane owns the runtime instances. The same model serves the first-party Nabhold Group Africa structure and any external enterprise group. Runtime logic has no Nabhold-specific branches.

## Files

Every file is a definition library. Validate a resource against its fragment URI (for example `relationship.schema.json#/$defs/CorporateRelationship`), not against the document root.

| File | `$defs` it owns |
|------|-----------------|
| `domain.schema.json` | `Organisation`, `LegalEntityProfile`, shared enums (form, verification state, legal status, classification) and the opaque resource-ID grammars used by every file below |
| `relationship.schema.json` | `CorporateRelationship`, `CorporateGroup`, `CorporateGroupMembership` |
| `platform.schema.json` | `PlatformRelationship`, `PlatformAccount`, `PlatformAccountMembership` |
| `mapping.schema.json` | `TenantOrganisationMapping`, `TenantLegalEntityMapping` |
| `examples/` | Illustrative instances for Nabhold Group Africa and an external group |

`scripts/validate-organisation-contracts.py` checks that each file's `$id` and `$defs` match the table above.

## Resource identifiers

The Control Plane mints each resource ID. IDs are opaque and never contain names, countries, markets or brands:

| Resource | Grammar |
|----------|---------|
| CorporateRelationship | `crel_[a-z0-9]+` |
| CorporateGroup | `cgrp_[a-z0-9]+` |
| CorporateGroupMembership | `cgm_[a-z0-9]+` |
| PlatformRelationship | `prel_[a-z0-9]+` |
| PlatformAccount | `pacct_[a-z0-9]+` |
| PlatformAccountMembership | `pam_[a-z0-9]+` |
| TenantOrganisationMapping | `tom_[a-z0-9]+` |
| TenantLegalEntityMapping | `tlem_[a-z0-9]+` |

These IDs replace the earlier reuse of `control-plane/v1#/$defs/mappingId` (`map_*`). That grammar still belongs to the canonical-mapping contract.

Organisation IDs reuse `control-plane/v1#/$defs/canonicalEntityId`, because CanonicalEntity remains the identity spine. Legal-entity IDs reuse `canonicalLegalEntityId`. First-party IDs (`NABHOLD`, `ZURIBEANS`, `THAMANI-GLOBAL`, `EQUATOR-ESTATE`) stay unchanged. For newly admitted external legal entities, the Control Plane SHOULD mint opaque `LE-<token>` IDs (ADR-BCP-018 §12). Names, brands and registration numbers go in `legal_name`, `registration_identifiers` and external references.

## Trust rules the schema enforces

- **VERIFIED needs evidence.** A `CorporateRelationship`, `PlatformRelationship` or `LegalEntityProfile` with `verification_state: VERIFIED` must include a non-empty `evidence_references` list and a `verified_at` timestamp. The two relationship types also need `verified_by`. An applicant's claim is evidence to review; it is never a verified fact (ADR-BCP-018 §69, ADR-BCP-023). `verified_by` comes from the authenticated principal on the server and is never taken from a client payload.
- **Relationships are directed.** A `CorporateRelationship` states `source_organisation_id RELATIONSHIP_TYPE target_organisation_id` (for example `A OWNS B`). Inverse facts such as owned-by, parent-of, subsidiary-of and sister-of are derived from these records and are never stored. The vocabulary is `OWNS`, `CONTROLS`, `BRANCH_OF`, `AFFILIATE_OF`, `JOINT_VENTURE_WITH` and `SUCCESSOR_OF`.
- **Derived facts keep their lineage.** A record marked `direct_or_derived: DERIVED` must include `basis_relationship_ids`, `derived_at` and `derivation_version`. The same applies to `CorporateGroupMembership`, unless the membership has a governed `manual_basis_reference`.
- **Group affiliation needs a basis.** A `PLATFORM_GROUP_AFFILIATE` must point to the `CorporateRelationship` that justifies it (`basis_relationship_id`).
- **Ownership is not control.** `ownership_percentage` records a fact. Policy decides what follows from it (§21). When sources conflict, the relationship moves to `CONFLICTED`; the schema never picks one value.
- **Mappings are explicit.** Tenant mappings require `mapping_role` and `provenance`. The active `TenantLegalEntityMapping` whose `mapping_role` is `DEFAULT` is the compatibility projection of `Tenant.LegalEntityID`.

The validator also checks the examples for rules that JSON Schema can't express:

- every referenced ID must exist;
- a relationship's source and target must differ;
- effective dates must not run backwards;
- a tenant has at most one active DEFAULT mapping;
- an ACTIVE group membership may only be derived from VERIFIED relationships;
- a VERIFIED affiliate must rest on a VERIFIED basis.

The Control Plane must enforce the same rules in its persistence layer (ADR-BCP-018 §117–119).

## Architectural invariants (normative)

```text
Organisation != LegalEntity
Organisation != Tenant
Organisation != IAM Organisation
CorporateRelationship != CounterpartyRelationship          (ADR-BCP-014)
CorporateRelationship != ADR-BCP-012 LegalEntityRelationship
CorporateRelationship != PlatformRelationship
PlatformRelationship != ProductSubscription
PlatformAccount != Tenant
CorporateGroup != authorization boundary
Corporate ownership != authorization
same corporate group != cross-tenant access
same PlatformAccount != shared authorization
PLATFORM_GROUP_AFFILIATE != runtime permission
IAM organisation claim != canonical corporate truth
```

Any consequential decision that depends on a relationship MUST fail closed when authoritative evidence is missing or conflicted.

## Examples

- `examples/nabhold-group-organisation.json`: models the first-party structure from ADR-BCP-018 §58. The Shared registry is the authoritative source for Organisation and LegalEntity identity, so those records are VERIFIED with a registry evidence reference. The registry marks jurisdiction, registration and ownership details as TBD, so the example omits them or sets them to `UNKNOWN`. The `OWNS` and `PLATFORM_*` relationships stay `PENDING_REVIEW` until the "Verify CorporateRelationship" step of ADR-BCP-018 §109 is complete. Until then, ADR-BCP-017 INTERNAL eligibility fails closed.
- `examples/acme-holdings-external.json`: models an external group with opaque IDs throughout. Its VERIFIED facts are backed by evidence. It also includes an unreviewed applicant claim, a `CONFLICTED` ownership fact, a derived corporate group, a PlatformAccount and the tenant mappings.

## Compatibility

- Existing `BUYER_ORGANISATION` and `SUPPLIER_ORGANISATION` CanonicalEntity records (ADR-BCP-016 / ADR-0006) stay valid and migrate forward without any destructive rewrite.
- The singular `Tenant.LegalEntityID` field remains a compatibility projection of the default `TenantLegalEntityMapping` until consumers migrate.
- `TenantLegalEntityMapping.is_default` and `TenantOrganisationMapping.is_default` have been removed. They duplicated `mapping_role` and could contradict it. `mapping_role: DEFAULT` is now the only default marker.
- `PlatformAccountMembership` now links Organisations only, using the ADR §43 account roles. Tenant-to-account binding (§45, §119) is a separate explicit concept and does not yet have a contract.
- External customers no longer need an entry in the legal-entity registry (see `contracts/tenancy/tenancy.yaml` v1.1). A tenant must still resolve to an active canonical LegalEntity in the Control Plane.

## Related contracts

- `contracts/tenancy/tenancy.yaml` (v1.1+)
- `contracts/legal-entity/registry.yaml` (first-party only)
- `contracts/erp/v1/system-of-record.yaml` (Organisation and Legal Entity runtime owner = control-plane)
- `contracts/control-plane/v1/domain.schema.json` (identity spine: `canonicalEntityId`, `canonicalLegalEntityId`, `tenantId`)
- `contracts/buyer-organisation/v1/`, `contracts/supplier-onboarding/v1/` (specialised shapes that link through `canonical_organisation_id`)

## Implementation notes for Control Plane

1. Reuse `CanonicalEntity`, `CanonicalRelationship`, `Mapping`, `ExternalReference` and `MappingScope`. Do not create a parallel identity system.
2. Mint the resource IDs above. Resolve retries against natural keys, such as (tenant, organisation, role) or (organisation, platform, relationship type), instead of minting a fresh ID for each attempt.
3. Registration creates `UNVERIFIED` or `PENDING_REVIEW` facts. Only an explicit, governed verification step (ADR-BCP-023) moves them to `VERIFIED`.
4. Derive INTERNAL subscription eligibility (ADR-BCP-017) only from VERIFIED, directed `OWNS`/`CONTROLS` paths.
5. Prove the five security statements through the real authorization path before merge.
