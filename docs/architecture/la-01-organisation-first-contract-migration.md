# LA-01 — Organisation-first canonical contract migration

**Decision authority:** Accepted ADR-BCP-026 and ADR-BCP-027 (9 October 2026).
**Contract owner:** baobab-platform/shared. **Runtime owner:** baobab-platform/baobab-cp.
**State:** Canonical versioned schemas published as future interfaces; no runtime conversion, live tenancy, legal mandate or provider readiness is claimed.

## Compatibility and deployment boundary

The old control-plane/v1 tenant registration requires legal_entity_id, the v1 context response requires entity_id, and v1 admission requires corporate registration-oriented application data. Their consumers, generated clients and contracts.lock pins MUST NOT break due to an in-place rewrite. Existing v1 schemas, OpenAPI and examples are preserved unchanged.

The normative governance contract tenancy/tenancy.yaml advances to v2.0; brand-new versioned wire schemas live in organisation/v2, admission/v2 and control-plane/v2. CP SHALL adopt these through separate, tested, explicitly pinned migration PRs. Shared passing CI is not proof that CP supports the v2 wire API.

| New contract | Responsibility |
|---|---|
| organisation/v2/pre-tenant-admission.schema.json | Resolve the primary Organisation before Tenant registration; an Organisation can exist without tenancy, LegalEntity or entitlements |
| admission/v2/business-identity.schema.json | Minimum identity declarations for incorporated and unincorporated applicants |
| control-plane/v2/tenant-registration.schema.json | AUTHORISED onboarding request and required primary Organisation; optional DEFAULT LegalEntity projection |
| control-plane/v2/context-resolution.schema.json | Tenant and PRIMARY Organisation required; no universal legal entity in context |
| organisation/v2/legal-actor-mandate.schema.json | Legal actor authority scoped by Tenant, Organisation, role, activity, market, validity and evidence |
| organisation/v2/founding-admission.schema.json | Founding sponsorship and named, bounded 12-month documentary deferral, separate from statutory duties |

All seven v2 schemas are registered in contracts.lock.yaml and validated with repository-local offline JSON Schema Draft 2020-12 references, accepted/rejected fixtures and compatibility checks.

## Non-negotiable rules

1. Tenant, Organisation, LegalEntity, BusinessUnit, TradingStyle and IAM identities remain separate. Exactly one active PRIMARY Organisation must exist for every operational Tenant.
2. A DEFAULT TenantLegalEntityMapping is optional for eligible v2 tenants. If present it is an explicitly governed, nullable compatibility projection; it cannot choose the primary Organisation or authorise all transactions.
3. A real LegalEntity may be legally responsible for multiple tenants, but provides NO cross-tenant IAM or data rights. Its operations require specific valid mandates when the activity calls for a responsible actor.
4. Mandates need approved authority, evidence, precise role, market and activity, effective window, and fail-closed resolution on absent, expired or conflicting authority. The schema does not itself prove a provider's legal/operational permission.
5. Historic contracts, invoices, shipments and financial records must retain their correct legal actor as of execution. Incorporation changes future authority by a governed effective-dated transition, not by rewriting historic attribution.
6. A first-party registry entry, founding sponsorship, INTERNAL eligibility, incorporation verification, group ownership and authority to trade are independent facts. Admission does not grant access, subscription or operational readiness.
7. Founding documentary grace covers explicitly named internal documents for a bounded period; it is not a waiver of statutory or third-party conditions.

## Declared founding group stage (2026-10-09)

| Stable first-party ID | Declared business/legal status | Legal actor expectation |
|---|---|---|
| NABHOLD | Registered LegalPerson with referenced CIPC documentation; CP must verify actual evidence | Own operations plus authorised scoped operating businesses |
| THAMANI-GLOBAL | CIPC registration declared; separately incorporated Nabhold subsidiary; verify registration and control independently | Normally Thamani is its own legal actor |
| ZURIBEANS | Independently operating trade business, not yet separately incorporated | Nabhold as proposed legal actor for only approved scopes |
| EQUATOR-ESTATE | Independently operating property and services business, not yet separately incorporated | Nabhold as proposed legal actor for only approved scopes |

Existing first-party identifiers and legacy role labels are preserved to avoid silent consumer breaks. New identity_class and incorporation_claim declarations in contracts/legal-entity/registry.yaml disambiguate operating businesses from company-registration evidence. These are business statements, not VERIFIED legal status or unlimited mandates.

## Work remaining after LA-01

LA-02: CP additive PostgreSQL changes, nullable legacy projection, primary Organisation integrity and data-provenance review.
LA-03: CP pre-tenant Organisation creation, corrected first-party reconciliation, admission, atomic tenant registration, migration-safe context handling.
LA-04: Governed operating legal-actor mandate APIs, decision policy, auditable evidence/approval/expiry.
LA-05: Explicit consumer pin migration, IAM/Trade/ERP/document/finance integration, legal attribution and tenant isolation.
LA-06/07: Founding-group tenant provisioning and accepted per-capability readiness, not a paper certification.

## Verification commands

- ruby scripts/validate-governance-contracts.rb
- python scripts/validate-operating-business-contracts.py
- python scripts/validate-organisation-contracts.py
- python scripts/validate-admission-contracts.py

No universal live trading authority, company incorporation, cross-border permit, property title, revenue subscription or production onboarding is granted by these contracts.
