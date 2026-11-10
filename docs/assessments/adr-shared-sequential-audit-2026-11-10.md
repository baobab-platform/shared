# ADR-SHARED Conformance Audit — Sequential Register

**Audit started:** 10 November 2026  
**Source baseline:** `baobab-platform/shared` main at `2a2ac16a26e0c217875002f25d7f00e181cf8c5b`  
**Scope:** 45 ADR-SHARED documents (001–045); this register records completed review slices only.

## Evidence vocabulary

- **Source enforced:** Shared contract, schema or package exists and is exercised by a source-level CI check. This is *not* evidence of deployed consumer correctness.
- **Source defined:** Shared has accepted documentation and matching artifacts, but this audit does not prove all referenced runtime behaviours.
- **External qualification outstanding:** Requires a separately witnessed CP, IAM, engine, estate or Infrastructure run and version pin.
- **Governance reconciliation:** A historical statement overlaps or conflicts with a later accepted decision. Do not silently implement it or pretend that an unreviewed supersession was approved.
- **Not audited:** No conformance verdict has been reached.

## 001 — Digital Estate & Contract Architecture

**Finding:** Source implemented **in material part**; legacy architecture assumptions need explicit governance reconciliation; external consumer qualification remains outstanding. This is not a declaration of full ADR completion.

| Obligation | Source evidence | Verdict |
| --- | --- | --- |
| Independently owned digital estates and engine-neutral Shared boundary | `contracts/tenancy/tenancy.yaml`, `contracts/legal-entity/registry.yaml`, `README.md` | Source defined |
| Distinct legal identity, organisation, tenant and estate | `contracts/tenancy/tenancy.yaml`, `contracts/control-plane/v1/domain.schema.json`, `scripts/validate-governance-contracts.rb` | Source enforced |
| First-party registry does not grant runtime entitlements or legal mandates | `contracts/legal-entity/registry.yaml`, `contracts/organisation/v2/` | Source defined; this PR adds schema and type/provenance negative fixtures |
| Governance vs interface contracts | `contracts/`, `contracts/events/v1/`, `contracts/control-plane/v1/` | Source defined |
| Reusable versioned shared packages and consumer pinning | `packages/`, `contracts.lock.yaml`, `scripts/contract_lock.py` | Source implemented; downstream pin evidence outstanding |
| Original mandatory Django-monolith / Apollo Federation / gRPC deployment diagram, all-frontends-must-be-Turborepo assumptions | Later `ADR-SHARED-002`, `ADR-SHARED-003`, `ADR-SHARED-005`, accepted EA v2.3 and actual Go CP / independent engines | **Governance reconciliation**: historical diagram must not be used as an executable target without a reviewed amendment; no unapproved vendor mandate introduced |
| Cross-repository estate isolation, independently operated engine authority, full consumer acceptance | Each owning repository and connected-run evidence | **External qualification outstanding** |

**New implementation in the ADR-001 PR:** `contracts/legal-entity/registry.schema.json`; `scripts/validate-legal-entity-registry.py`; `scripts/tests/test_legal_entity_registry.py`; CI gate. The guard rejects strings masquerading as consent booleans, duplicate identities and products, invented tenant/CP authority, unsubstantiated incorporation claims, and separation-policy drift. It validates declared intent only, not CP authority, group relationship, legal incorporation or active subscriptions.

**Boundary:** `NABHOLD`, `ZURIBEANS`, `THAMANI-GLOBAL`, `EQUATOR-ESTATE` are first-party identities; external customer legal entities are CP-issued/registered and are not to be added to this static bootstrap registry. The old `BAOBAB-PLATFORM` example is not silently revived.

## 002 — Control Plane Polyrepo Boundaries

**Finding:** Shared responsibility is consistent with `contracts/`, `packages/`, reusable workflows, `scripts/`; `shared` does not run a management API or mint tenant identities. **Source defined**, cross-repository ownership / no direct environment-orchestrator calls **not yet independently tested**. Runtime wiring belongs in CP/Infrastructure/engines, not a second backend in Shared.

## 003 — Tenant, Legal Entity and Digital Estate Separation

**Finding:** `contracts/tenancy/tenancy.yaml`, `contracts/control-plane/v1` and `contracts/organisation/v2` express distinct identities, CP-owned mappings and no implied estate tenancy. Existing Ruby governance validator and this PR's new negative fixtures guard the local seam. **Source enforced; CP/runtime isolation not certified by this source audit.** The later primary-Organisation model (`ADR-BCP-026/027`) supersedes the historical unconditional legal-entity default; pinned v1 consumers remain governed by their own version.

## 004 — Canonical Cross-Engine Metadata

**Finding:** canonical `contracts/events/v1/envelope.schema.json`, `contracts/errors/v1/problem-details.schema.json`, `contracts/idempotency/v1/policy.yaml` and Ruby/event registry validation exist. **Source defined/enforced.** Durable multi-engine inbox/outbox replay, native effects and exported trace continuity require separate runtime proof; a schema passing does not prove these.

## 005 — ERP System-of-Record & Boundary Contracts

**Finding:** `contracts/erp/v1/system-of-record.yaml`, OpenAPI/AsyncAPI and ERP validators exist; vendor-private IDs are not the canonical source. **Source defined/enforced.** Native iDempiere, real Trade `order.placed` consequence, durable inbox and ERP financial replay are owned and qualified separately; no runtime acceptance asserted here.

## 006 — Supplier-Onboarding Domain Contracts

**Finding:** `packages/supplier-domain`, `contracts/supplier-onboarding/v1` and event/contract validation artifacts exist. **Source defined.** Consumer adoption and native ERP vendor provisioning remain distinct, unproven by this Shared-only pass; ADR-006 expressly does not implement the ERP adapter.

## Remaining decisions

**ADR-SHARED-007–045: not yet individually audited in this register.** Continue numerical review against the latest accepted amendments, source and owning-repository evidence. A document existing, a green schema test, or an open PR is not a production qualification.

## Audit protocol for every subsequent ADR

1. Read the exact ADR, status, amendment/supersession chain and acceptance conditions at a pinned commit.
2. Locate canonical schemas, examples, registries, packages, tests, CI invocation and consumer locks. Do not equate declaration with execution.
3. For a real gap, implement the smallest authoritative fix in the owning repository, add positive/negative tests and a bounded PR; record dependencies on other repositories separately.
4. Check CI at the final head, review failures, security/privacy/idempotency/tenancy/SoD negative paths, and record evidence SHA and limitations.
5. Advance the next ADR without auto-merging or treating staging/production as authorised.

**Current release assertion:** none. This document is an audit ledger, not a conformance certificate.
