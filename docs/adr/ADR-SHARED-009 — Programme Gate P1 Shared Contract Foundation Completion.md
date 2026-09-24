# ADR-SHARED-009 — Programme Gate P1 Shared Contract Foundation Completion

**Status:** Accepted — Normative Contract Addition
**Date:** 2026-09-16
**Decision Owners:** BAOBAB-PLATFORM / Baobab Platform Architecture
**Primary Repository:** `baobab-platform/shared`
**Affected Repositories:** `baobab-platform/shared`, `baobab-platform/baobab-cp`
**Reference Tenant:** ZuriBeans
**Trigger:** `baobab-cp` Tenant Onboarding & Provisioning Technical Specification, **Programme Gate P1 — Shared Contract Foundation** (§88): "Implement in `baobab-platform/shared`: Capability, CapabilityScope, CapabilityGrant, CapabilityProvider, CapabilityBinding, Product, ProductVersion, Composition, Subscription, Context, Provisioning, Readiness, Drift, event vocabulary, reason codes. All schemas validate."

**Depends On:**

- ADR-SHARED-007 — Canonical Capability Contracts, Composition Registry and Cross-Engine Provider Model
- ADR-SHARED-008 — Gate ZB-01 Capability Domain Registration and Canonical Event-Type Convention Confirmation
- `baobab-cp` ADR-BCP-015 (CR-006: capability vocabulary), ADR-BCP-013 (inventory), ADR-BCP-011 (market participation)
- `baobab-cp` `docs/reconciliation/phase-0-architecture-inventory-and-lock.md` (Programme Gate P0, whose classification of `ProductSubscription` and the absence of `Readiness`/`Drift` this ADR directly answers)

---

## 1. Purpose

Programme Gate P0 (`baobab-cp`, Accepted) found `ProductSubscription` implemented only as a thin `tenant_id`/`product_id`/`status` table with no `ProductVersion`, composition, or entitlement-projection linkage, and found `ReadinessSnapshot` and `Drift` entirely absent from both the runtime schema and — this ADR's own audit confirms — from `baobab-platform/shared`'s contracts. Of Programme Gate P1's fourteen required items, an audit of `baobab-platform/shared`'s existing `contracts/` tree before this ADR found:

| Item | Status before this ADR |
|---|---|
| Capability | Present (`contracts/capability/v1/capability.schema.json`) |
| CapabilityScope | Present (`scope.schema.json`) |
| CapabilityGrant | Present (`grant.schema.json`) |
| CapabilityProvider | Present (`provider.schema.json`) |
| CapabilityBinding | Present (`binding.schema.json`) |
| Composition | Present (`composition.schema.json`) |
| Context | Present (`control-plane/v1/context-resolution.schema.json`) |
| event vocabulary | Present, corrected (ADR-SHARED-008) |
| reason codes | Present (`authorization/v1/reason-code-registry.yaml`), already includes `BINDING_NOT_FOUND` and the full `capability_resolution_denial` category |
| Provisioning | Present only as thin lifecycle event payloads (`provisioning-started`/`provisioning-state-changed.schema.json`) and a state machine (`provisioning-state-machine.yaml`) — no `TenantProvisioning` aggregate resource |
| **Product** | **Absent** — only a bare `productId` string pattern existed (`control-plane/v1/domain.schema.json`), no entity |
| **ProductVersion** | **Absent** |
| **Subscription** | **Absent** as a resource schema (only referenced by name from `capability/v1/domain.schema.json#/$defs/capabilityGrantSource`'s `PRODUCT_SUBSCRIPTION` value) |
| **Readiness** | **Absent** |
| **Drift** | **Absent** |

This ADR closes the five absent items and completes the one partial item (Provisioning), without touching the nine already-present items beyond what ADR-SHARED-008 already corrected.

---

## 2. Decision — New Contract Package: `contracts/product/v1/`

A new package, structured identically to `contracts/capability/v1/` (its own `domain.schema.json`, resource schemas, `events.schema.json`, `asyncapi.yaml`, `README.md`, `examples/`), defines:

- **`Product`** — a sellable platform offering, identified by the pre-existing `control-plane/v1/domain.schema.json#/$defs/productId` grammar (no new product identifier is introduced).
- **`ProductVersion`** — an immutable, semantically-versioned packaging of a Product as a `CapabilityComposition` (`product.schema.json`'s `composition_key` references `capability/v1/composition.schema.json` directly). New opaque ID: `prodver_`.
- **`ProductSubscription`** — which tenant subscribed to which ProductVersion, plus any additional profile/add-on compositions selected (`subscription_profiles[]`, e.g. `profile.b2b`, `profile.crossborder`). New opaque ID: `sub_`.
- **`EntitlementProjection`** — the read-model record that a subscription's composition graph has been expanded into a real `CapabilityGrant` (`capability/v1/grant.schema.json`, `source=PRODUCT_SUBSCRIPTION`). New opaque ID: `entproj_`.

The full chain these contracts describe:

```text
ProductSubscription
      |
      v
ProductVersion --composition_key--> CapabilityComposition
      |                                      |
      +--subscription_profiles[]-------------+--> (additional composition members)
                                             |
                                             v
                                     CapabilityGrant (source=PRODUCT_SUBSCRIPTION)
                                             |
                                             v
                                     EntitlementProjection
```

Composition expansion, grant materialisation, and all business logic remain `baobab-platform/baobab-cp`'s runtime responsibility, per the same "contract-authority package, not a runtime" boundary `capability/v1/README.md` already states.

---

## 3. Decision — Provisioning Completion

`contracts/control-plane/v1/provisioning-plan.schema.json` adds `TenantProvisioning`, the onboarding process aggregate the Technical Specification §21 requires. It does **not** replace or renumber the already-implemented, already-migrated coarse lifecycle state machine (`provisioning-state-machine.yaml`'s `requested`/`accepted`/`provisioning`/`reconciling`/`active`/`suspended`/`failed`/`decommissioning`/`cancelled`, consumed by `baobab-cp`'s `internal/store/postgres/migrations/000019_tenant_lifecycle.sql`). Instead, `TenantProvisioning.state` reuses that enum verbatim, and a new, additive `current_phase` field (`domain.schema.json#/$defs/tenantProvisioningPhase`) carries the Technical Specification §22's finer-grained orchestration phases (`DRAFT` through `READY`) that occur *within* the coarse states. This mirrors ADR-BCP-015's own precedent of correcting-by-addition rather than renaming an already-shipped enum out from under running code.

`blocking_reasons[]` cites `contracts/authorization/v1/reason-code-registry.yaml`'s existing `capability_resolution_denial` codes (e.g. `BINDING_NOT_FOUND`, matching the Technical Specification §51's own example verbatim) rather than introducing a fourth reason-code category — a provisioning blocker is, at root, always a capability resolution failure for some mandatory capability, so the existing vocabulary is reused, not duplicated.

---

## 4. Decision — Readiness and Drift

`contracts/control-plane/v1/readiness.schema.json` adds `ReadinessSnapshot`: a hierarchical readiness projection (`PROVIDER`/`CAPABILITY`/`PRODUCT`/`ESTATE`/`TENANT` levels, Technical Specification §44), each non-`READY` snapshot required to carry `blocking_reasons[]` from the same `capability_resolution_denial` vocabulary — satisfying §44's "never merely `ready: false` where structured reasons are available." `contributing_snapshots[]` lets a higher-level snapshot (e.g. `PRODUCT`) reference the lower-level snapshots (its mandatory capabilities' `CAPABILITY` snapshots) it aggregates, so a snapshot's status is always derivable rather than independently asserted.

`contracts/control-plane/v1/drift.schema.json` adds `Drift`: a per-object desired-vs-observed mismatch record (Technical Specification §42-43), deliberately per-object rather than per-tenant — Programme Gate P0 found only a primitive tenant-level `desired_state`/`observed_state` pair implemented and flagged that real Drift must operate at finer grain. `object_type` is a closed enum drawn from the objects Programme Gate P0's own classification identified as carrying desired/observed state (`TENANT`, `LEGAL_ENTITY`, `DIGITAL_ESTATE`, `MARKET_PARTICIPATION`, `PRODUCT_SUBSCRIPTION`, `CAPABILITY_GRANT`, `CAPABILITY_BINDING`, `PROVIDER_CONFIGURATION`), not an open-ended free-text field. `safe_to_reconcile` carries the Technical Specification §43's "Safe to fix?" branch point directly.

---

## 5. Validation

Every new and modified schema in this ADR was checked with `Draft202012Validator.check_schema` (structural validity) and, further, exercised against constructed instances of every new `$def` — `Product`, `ProductVersion`, `ProductSubscription` (both `ONBOARDING` and non-`ONBOARDING` source branches), `EntitlementProjection`, `TenantProvisioning` (both a mid-flight and a `BLOCKED` instance, confirming the `blocking_reasons` conditional), `ReadinessSnapshot`, and `DriftRecord` — with full cross-file `$ref` resolution against the real `contracts/` tree, not just isolated schema files. The two new example events (`subscription-created.json`, `entitlement-projection-materialized.json`) were validated against both `contracts/events/v1/envelope.schema.json` and their own `data` payload schemas. `scripts/validate-capability-contracts.rb` (the existing capability-domain/enum consistency check) continues to pass unmodified — this ADR's domain additions in ADR-SHARED-008 are unaffected by the product/provisioning/readiness/drift work.

---

## 6. Consequences

- Programme Gate P1's fourteen-item checklist is satisfied: nine items were already present (three corrected by ADR-SHARED-008), and this ADR adds the remaining five (`Product`, `ProductVersion`, `Subscription`, `Readiness`, `Drift`) and completes the sixth (`Provisioning`).
- `baobab-cp`'s `ProductSubscription` REMODEL, flagged by Programme Gate P0 as the largest single gap in its classification, now has a target contract to remodel against (`contracts/product/v1/subscription.schema.json`) rather than an ad hoc internal redesign.
- No existing contract file's `$id`, required fields, or enums were changed by this ADR outside of `control-plane/v1/domain.schema.json`'s purely additive new `$defs` (`tenantProvisioningId`, `tenantProvisioningPhase`, `readinessSnapshotId`, `readinessStatus`, `driftRecordId`, `driftObjectType`, `driftResolution`) — no consumer of the pre-existing contracts is broken by this change.
- `baobab-platform/baobab-cp` carries the action item to implement `TenantProvisioning`, `ReadinessSnapshot`, and `Drift` as real migrated tables (Programme Gates P7 and P10) and to remodel `product_subscriptions` against `contracts/product/v1/subscription.schema.json` (tracked next, per this session's own follow-on work).
