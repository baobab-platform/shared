# Organisation, Corporate Group, Platform Account and Tenant Relationship Contracts

**Target path:** `baobab-platform/shared/contracts/organisation/v1/`

**Governing ADR:** ADR-BCP-018 — Canonical Organisation, Corporate Group, Platform Account and Tenant Relationship Model

**Contract authority:** `baobab-platform/shared`  
**Runtime authority:** `baobab-platform/baobab-cp`  
**First-party governance source:** Nabhold Group Africa records published through this repository

## Purpose

These contracts make Shared the schema/governance authority for the generic organisation and relationship model while leaving runtime ownership of instances with the Control Plane.

They support both:

```text
Nabhold Group Africa
├── ZuriBeans
├── Thamani Global
└── Equator & Estate
```

and arbitrary external enterprise groups such as:

```text
Acme Holdings
├── Acme Foods
├── Acme Logistics
└── Acme Retail
```

using the same generic architecture with no Nabhold-specific runtime branching.

## Files

| File | Contents |
|------|----------|
| `domain.schema.json` | Organisation, LegalEntityProfile, shared enums (form, verification state) |
| `relationship.schema.json` | CorporateRelationship, CorporateGroup, CorporateGroupMembership |
| `platform.schema.json` | PlatformRelationship, PlatformAccount, PlatformAccountMembership |
| `mapping.schema.json` | TenantOrganisationMapping, TenantLegalEntityMapping |
| `examples/` | Illustrative instances for Nabhold Group and an external group |

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

All consequential relationship resolution MUST fail closed when authoritative evidence is missing or conflicted.

## Compatibility

- Existing `BUYER_ORGANISATION` and `SUPPLIER_ORGANISATION` CanonicalEntity records (ADR-BCP-016 / ADR-0006) migrate forward without destructive rewrite.
- The singular `Tenant.LegalEntityID` field remains a compatibility projection of the default `TenantLegalEntityMapping` (`is_default: true`) until consumers migrate.
- First-party identities `NABHOLD`, `ZURIBEANS`, `THAMANI-GLOBAL`, `EQUATOR-ESTATE` continue to be governed by `contracts/legal-entity/registry.yaml`.
- External customers no longer require an entry in that registry (see amended `contracts/tenancy/tenancy.yaml` v1.1).

## Related contracts

- `contracts/tenancy/tenancy.yaml` (v1.1+)
- `contracts/legal-entity/registry.yaml` (first-party only)
- `contracts/erp/v1/system-of-record.yaml` (Organisation owner = control-plane)
- `contracts/control-plane/v1/canonical-mapping.schema.json`
- `contracts/buyer-organisation/v1/` (specialised buyer shape; remains valid)

## Implementation notes for Control Plane

1. Reuse `CanonicalEntity`, `CanonicalRelationship`, `Mapping`, `ExternalReference` and `MappingScope`.
2. Do not create a parallel identity system.
3. Introduce forward-only migrations for the new tables.
4. Derive INTERNAL subscription eligibility (ADR-BCP-017) only from verified CorporateRelationship / PlatformRelationship evidence.
5. Prove the five security statements with automated tests before merge.
