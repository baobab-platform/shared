# ADR-SHARED-008 — Gate ZB-01 Capability Domain Registration and Canonical Event-Type Convention Confirmation

**Status:** Accepted — Normative Contract Amendment
**Date:** 2026-09-13
**Decision Owners:** BAOBAB-PLATFORM / Baobab Platform Architecture
**Primary Repository:** `baobab-platform/shared`
**Affected Repositories:** `baobab-platform/shared`, `baobab-platform/baobab-cp`, `baobab-platform/baobab-trade`
**Reference Tenant:** ZuriBeans
**Trigger:** ZuriBeans Go-Live Implementation Plan, **Gate ZB-01 — Contract Convergence** ("reconcile canonical IDs; reconcile event envelopes").

**Depends On / Amends:**

- ADR-SHARED-007 — Canonical Capability Contracts, Composition Registry and Cross-Engine Provider Model (§9 Capability Naming Convention, §11 Domain Namespace Governance, §42 Event Vocabulary)
- `contracts/events/v1/envelope.schema.json` (the shipped, enforced event-envelope contract)
- `contracts/capability/v1/namespace-registry.yaml` and `domain.schema.json` (amended by this ADR)
- `baobab-cp` ADR-BCP-011 — Market Participation, Trade Lanes and Cross-Market Trading Model
- `baobab-cp` ADR-BCP-012 — Intercompany and Inter-Branch Trading, Legal-Entity Relationship and Internal Settlement Model
- `baobab-cp` ADR-BCP-015 — Gate ZB-00 Capability Vocabulary Alignment, Quality-State Ownership and Roadmap Conflict Resolution (CR-006)
- `baobab-cp` Tenant Onboarding & Provisioning Technical Specification (CR-003)
- `baobab-trade` ADR-0018 (Accepted) and its Accepted Addendum
- `baobab-trade` ADR-0021 — Customs, Trade Compliance and Regulatory Provider Architecture

---

## 1. Purpose

Gate ZB-01 (Contract Convergence) requires canonical IDs and event envelopes to be reconciled across repositories before further implementation. Auditing `baobab-cp` ADR-BCP-015 (Gate ZB-00's own conflict-resolution ADR) against Shared's actual shipped contracts — not just its own ADR text — surfaced two defects that block that reconciliation:

1. ADR-BCP-015's CR-006 resolved eight ADRs' capability vocabulary onto the masterplan's §10 taxonomy, but four of the resulting top-level capability domains (`market`, `internal-trade`, `customs`, `tax`) do not exist in Shared's governed namespace registry. Per ADR-SHARED-007 §11, a new top-level domain requires architectural review — a registry edit alone is insufficient.
2. ADR-BCP-015's CR-006 and its own parent Technical Specification's CR-003 both declared `baobab.<bounded-context>.<aggregate>.<event>.v<major>` as the canonical event-type format. This contradicts `contracts/events/v1/envelope.schema.json`, which already enforces (via JSON Schema pattern) and every shipped identity/ERP/supplier-onboarding event already uses `com.baobab-platform.<context>.<...>.v<N>`. Per this package's own README, an earlier `baobab.*` proposal was already considered and rejected during a prior Phase-0 audit — `baobab-cp`'s Technical Specification appears to have been written without checking Shared's shipped state.

This ADR resolves both.

---

## 2. Decision — Domain Registration

The following top-level capability domains are added to `contracts/capability/v1/namespace-registry.yaml` and `domain.schema.json`'s `capabilityDomain` enum, effective immediately:

| Domain | Description | Registers |
|---|---|---|
| `market` | Market participation capabilities (sourcing, procurement, selling, importing, exporting, warehousing, distribution, fulfilment) and cross-market trade-lane relationships. | ADR-BCP-011 |
| `internal-trade` | Inter-branch and intercompany movement between legal entities of the same tenant (transfer pricing, mirrored documents, in-transit ownership, elimination). | ADR-BCP-012 |
| `customs` | Customs declaration, duty/import-tax calculation and clearance capabilities. | `baobab-trade` ADR-0021 |
| `tax` | Multi-jurisdiction tax registration, calculation and reconciliation capabilities. | `baobab-trade` ADR-0018 + Addendum |

These are the only four new domains this ADR registers. Capability keys already resolvable under existing domains (e.g. `procurement.*` under `procurement`, `logistics.*`/`shipping.*` under `logistics`, `counterparty.*` under `counterparty`) are unaffected — ADR-BCP-015 CR-006's mapping of those onto existing domains stands without amendment here.

Both `namespace-registry.yaml` and `domain.schema.json` have been updated together and validated with `scripts/validate-capability-contracts.rb`, per this package's own consistency requirement.

---

## 3. Decision — Canonical Event-Type Convention

`com.baobab-platform.<context>.<...>.v<N>` — the pattern already enforced by `contracts/events/v1/envelope.schema.json` (`^com\.baobab-platform\.[a-z0-9]+(?:[.-][a-z0-9]+)*\.v[1-9][0-9]*$`) and already used by every shipped event in `contracts/identity-events/v1/`, `contracts/erp/v1/`, and `contracts/supplier-onboarding/v1/` — is confirmed as the **sole** canonical event-type convention for the entire Baobab platform.

Consequently:

- `baobab-cp`'s Tenant Onboarding & Provisioning Technical Specification, CR-003 ("Baobab SHALL standardise canonical event names as `baobab.<bounded-context>.<aggregate>.<event>.v<major>`") is **superseded**. Its stated examples (e.g. `baobab.tenant.tenant.created.v1`) are invalid; the equivalent canonical form is `com.baobab-platform.tenant.tenant.created.v1`.
- `baobab-cp` ADR-BCP-015 §2.2 item 5 and its event-renaming examples in §2.1 (which renamed several ADRs' ad hoc event names to the `baobab.*` form) target the wrong convention. The correct target is `com.baobab-platform.*`. Example corrections: `supplier.registered` → `com.baobab-platform.procurement.supplier.registered.v1` (not `baobab.procurement.supplier.registered.v1`); `commercial-price.resolved` → `com.baobab-platform.commercial.price.resolved.v1`; `shipment.created` → `com.baobab-platform.trade.shipment.created.v1`; `counterparty.merged` → `com.baobab-platform.counterparty.counterparty.merged.v1`.
- ADR-BCP-011 and ADR-BCP-013, which the Gate ZB-00 audit found to correctly follow the (wrongly specified) `baobab.*` convention, in fact need the same correction to `com.baobab-platform.*` to match what Shared actually ships.
- This ADR does not re-litigate ADR-SHARED-007 §42/§43, which already left the exact event-type string format to "the existing canonical event-envelope principles in Shared" without spelling it out; this ADR makes that reference concrete and closes the ambiguity CR-003 introduced by re-specifying it differently.

Neither `baobab-cp` nor `baobab-trade` document is rewritten by this ADR. Each carries a pointer at its next revision: *"Event-type strings in this document are superseded where they conflict with ADR-SHARED-008 §3."*

---

## 4. Why Shared Is Authoritative Here

Per ADR-SHARED-007 §11 and this package's own architectural role (contract authority, not runtime authority), no downstream repository — including `baobab-cp` — may unilaterally declare a competing canonical vocabulary or event-naming convention. `baobab-cp`'s Technical Specification is the tenant-onboarding *runtime* programme; it correctly identifies that a canonical convention is needed, but it is not itself the place that convention is set once Shared has already shipped one. Where the two conflict, Shared's shipped, enforced contract wins, and the downstream document is corrected by reference — the same pattern ADR-BCP-015 itself established for reconciling ADR-BCP-011 through ADR-0022.

---

## 5. Consequences

- No new capability keys under `market.*`, `internal-trade.*`, `customs.*`, or `tax.*` may be declared in any `CapabilityGrant`, `CapabilityBinding`, or `CapabilityProvider` record until `baobab-cp`'s runtime capability registry picks up this revision of `domain.schema.json`.
- No schema, migration, or event publisher SHALL be written against the `baobab.*` event-type format in any repository from this point forward; all new event types use `com.baobab-platform.*` and are validated against `contracts/events/v1/envelope.schema.json`'s pattern.
- `baobab-cp` carries an action item to add a short pointer to ADR-BCP-015 (§2.2) and to the Technical Specification (CR-003) noting supersession by this ADR, without re-deriving the resolution there.
- Gate ZB-01's "reconcile canonical IDs; reconcile event envelopes" task is satisfied for the vocabulary and event-format dimensions; the remaining Gate ZB-01 tasks (publishing buyer-organisation, RFQ, quotation, procurement, shipment, trade-lane, inventory-ownership, trade-document, and intercompany contracts as versioned Shared packages) are separate, larger contract-authoring efforts not addressed by this ADR.
