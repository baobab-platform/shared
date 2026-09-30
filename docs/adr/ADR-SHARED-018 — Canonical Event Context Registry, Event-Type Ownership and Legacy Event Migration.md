# ADR-SHARED-018 — Canonical Event Context Registry, Event-Type Ownership and Legacy Event Migration

**Status:** Proposed
**Date:** 2026-09-30
**Repository:** `baobab-platform/shared`
**Decision Type:** Cross-Platform Event Architecture / Contract Governance
**Refines:** ADR-SHARED-008 §3 (canonical event-type convention). It does not replace it.
**Related:** ADR-SHARED-007 (capability domains), ADR-SHARED-017 (capability catalogue, engine registry), ADR-0004 (cross-engine event metadata), EA Implementation Plan v2.0 EA-01 and EA-06, G-REG-NS (Option B)
**Trade ADRs consulted for ownership:** ADR-0013 (inventory), ADR-0015 (payment), ADR-0016 (fulfilment), ADR-0017 (B2B customer), ADR-0018 and Addendum (tax), ADR-0021 (customs and compliance), ADR-0024 (product classification)
**Contract Authority:** `baobab-platform/shared`

---

## 1. Question

> How does Baobab govern canonical event contexts and event-type ownership, and how are Trade's legacy event types mapped into that model?

This is **not** a proposal to register `commerce` as a capability domain.
`commerce` is already registered in
`contracts/capability/v1/namespace-registry.yaml` and governed by
ADR-SHARED-007.

## 2. Context

ADR-SHARED-008 §3 fixed the event-type syntax:

```text
com.baobab-platform.<context>.<...>.v<N>
```

`contracts/events/v1/envelope.schema.json` enforces that syntax with a
pattern. `scripts/validate-event-registry.py` adds a platform check: every
message in any `contracts/<package>/v<N>/asyncapi.yaml` is canonical,
registered exactly once, composed with the envelope, and has a payload
schema that resolves.

Nothing governs the `<context>` segment itself. Today:

- **There is no context registry.** A package can mint any context, and
  the checks above only confirm that it is lower-case.
- **Contexts already diverge from capability domains.** Nineteen
  AsyncAPI packages use 20 contexts. Several are not capability domains:
  `control-plane`, `capability`, `credential`, `entitlement`, `session`,
  `workload`, `membership`, `supplier-onboarding`, `subscriptions`,
  `product`, `erp` and `payments`. The capability domains are `payment`,
  `finance` and `billing`, not `payments` or `erp`. The divergence is
  not an error. Capabilities and events are different abstractions, but
  the relationship between them is undocumented.
- **At least one context names an engine.** `erp` is the name of an
  engine role, not a bounded context. The capability-key rule in
  `namespace-registry.yaml` forbids vendor, engine, tenant and region
  names; no equivalent rule exists for events.
- **Producer authority is unrecorded.** AsyncAPI records channels and
  messages. It does not record which engine may produce a type. Payment
  events are one example: `payments.payment.*` is emitted by
  baobab-payments, while Trade emits `commerce.payment.*` about related
  facts.
- **Trade emits 38 legacy `com.nabhold.*` types.** They are listed in §9.
  Some encode organisation-prefix history only. Others encode a
  taxonomy that later ADRs changed, and some encode a tenant name
  (`thamani-*`) or a target engine (`erp-*`).

A capability identifies something that may be granted and resolved, for
example `commerce.cart.manage`. An event identifies a fact that occurred
in a bounded context, for example
`com.baobab-platform.commerce.cart.created.v1`. The two often correspond.
Forcing them to be the same abstraction would couple two lifecycles that
change for different reasons.

## 3. Decision

### 3.1 Two related registries

```text
Capability namespace governance
        └── contracts/capability/v1/namespace-registry.yaml   (existing, ADR-SHARED-007)

Event context governance
        └── contracts/events/v1/context-registry.yaml         (new)

Event-type registration
        └── contracts/events/v1/event-registry.yaml           (new; index over AsyncAPI)
```

The event context registry is related to the capability namespace
registry. It is not required to be identical.

### 3.2 Context registry

`contracts/events/v1/context-registry.yaml` governs the `<context>`
segment. Each entry carries at least:

```yaml
contexts:
  - key: commerce
    status: ACTIVE            # ACTIVE | RESERVED | DEPRECATED
    stewards: [baobab-trade]  # engines whose ADRs grant authority over facts in this context
    authority: [ADR-0014, ADR-0016]
    capability_domains: [commerce]   # related capability domains, possibly none
    description: >
      Cart, checkout, order-commitment and commerce-fulfilment-lifecycle facts.
```

Rules:

1. A context key follows the capability-key hygiene rules. It names no
   vendor, engine, tenant, Digital Estate, country or region.
2. Adding a context is an architecture review, like adding a capability
   domain (ADR-SHARED-007 §11).
3. A context MAY have several stewards when accepted ADRs divide authority
   within it. Each event type still has exactly one authorised producer
   (§3.3).
4. Existing contexts are registered as found, so no shipped event breaks.
   `erp` is registered `DEPRECATED` under §8.1, and `payments` is `ACTIVE`
   under §8.2.
5. A `DEPRECATED` context exists only for compatibility with events that
   have already been published. No new event type may be registered
   under it.
6. `regulations` is registered `RESERVED` until G-REG-NS step 3 registers
   the domain. Its event types become `ACTIVE` with the Regulations
   engine's first accepted contracts.

### 3.3 Event registry

`contracts/events/v1/event-registry.yaml` is the platform index of event
types. It indexes the AsyncAPI definitions and does not replace them,
the same way `catalogue.yaml` indexes capability definitions under
ADR-SHARED-017.

```yaml
events:
  - type: com.baobab-platform.commerce.order.placed.v1
    context: commerce
    aggregate: order
    fact: placed
    major: 1
    producer: baobab-trade
    asyncapi: contracts/trade/v1/asyncapi.yaml
    payload_schema: contracts/trade/v1/events/order-placed.schema.json
    lifecycle: ACTIVE          # PROPOSED | ACTIVE | DEPRECATED | RETIRED
    supersedes:                # legacy types this replaces, if any
      - com.nabhold.commerce.erp-order.projection-requested.v1
```

The event registry records one producer per type. A consumer may subscribe
to any registered type, and consumers are not recorded here.

### 3.4 Naming grammar

ADR-SHARED-008's syntax is kept. The segments after the context are made
explicit:

```text
com.baobab-platform.<context>.<aggregate>.<fact>.v<major>
```

- `<aggregate>`: the business entity the fact is about, in kebab-case
  (`order`, `stock-reservation`, `purchase-approval`).
- `<fact>`: a past-tense business fact (`created`, `placed`, `accepted`,
  `released`, `status-changed`). A compound fact is allowed when it is
  still past tense (`discrepancy-detected`).
- An event states what happened. It is never a command to another engine.
  `order.create` is not an event. A type whose meaning is "engine X please
  do Y" (`erp-order.projection-requested`) is a command and belongs on a
  governed API or capability. The consumer subscribes to the business
  fact instead.
- A request is a valid fact only when the request itself is a business
  event in the producer's domain. `purchase-approval.requested` qualifies:
  an approver has been asked.
- No vendor, engine, tenant, Digital Estate, country or region names
  appear in any segment.
- Deeper segments are allowed when the aggregate needs them. The grammar
  favours business facts, not a fixed depth.

### 3.5 Validation

Once the registries exist, Shared CI proves:

```text
message in an AsyncAPI package
        ↓ registered in event-registry.yaml, and vice versa
        ↓ context registered and not RETIRED
        ↓ payload schema exists and resolves
        ↓ producer is a registered engine (ADR-SHARED-017 engine registry)
        ↓ major in the type equals `major`
        ↓ name follows §3.4 (no engine, tenant or region tokens)
```

A later EA-06 Foundation check proves the producer side: a repository
emits only registered types for which it is the registered producer.

### 3.6 Historical and in-flight events

| Case | Rule |
|---|---|
| Already published event with a legacy type | A historical fact. It is never rewritten: deduplication, replay, evidence and audit depend on the original type. |
| Pending, unpublished outbox row with a legacy type | Migrated only under an explicit compatibility rule recorded in the producer's migration PR (map legacy to canonical, or drain before switching). |
| Newly produced event | MUST use the canonical type. |

Resetting a pre-production environment instead is an explicit
environment decision. It is not part of this contract.

### 3.7 Producer migration mechanics

- **Database migrations are immutable.** Trigger functions that emit
  legacy types are changed by a new forward migration
  (`CREATE OR REPLACE FUNCTION …`). Migrations that have already run are
  not edited.
- **Consumers first.** A consumer accepts both the legacy and the
  canonical type before the producer switches. The producer then emits
  canonical types only; there is no dual publishing. The legacy
  acceptance is removed in a later PR.
- **Source.** The producer `source` becomes
  `urn:baobab-platform:service:<engine>`. The envelope forbids deployment
  hostnames, and `https://engines.nabhold.com/...` is one.

## 4. Relationship to ADR-SHARED-007 and ADR-SHARED-008

- **ADR-SHARED-008** decided the syntax. This ADR answers what it left
  implicit: which contexts are valid, who stewards them, and how
  individual event types are registered and owned.
- **ADR-SHARED-007** governs capability domains. Registering `commerce` as
  an event context does not reopen whether the commerce domain exists.

## 5. Consequences

- The envelope's regex remains the syntax gate. The registries become the
  semantic gate that EA-06 builds on.
- Existing Shared event types are registered without renaming. `erp.*`
  types are re-homed under §8.1.
- Trade's re-pin to current Shared (EA-01) waits for its event migration
  (§7). The old pin moves only after the semantic changes are absorbed.
- Digital Estate projections are served by canonical business facts
  filtered by envelope context, not by estate-named types.

## 6. Alternatives considered

1. **Prefix-only rename** (`com.nabhold.commerce.*` →
   `com.baobab-platform.commerce.*`). Rejected: it carries the old
   taxonomy forward, including tenant-named and engine-command types,
   under a new prefix.
2. **Make event contexts identical to capability domains.** Rejected: it
   would force renaming shipped contexts (`payments`, `control-plane`,
   `session`, …) and couple event and capability lifecycles.
3. **Keep AsyncAPI as the only registry.** Rejected: AsyncAPI does not
   record producer authority, context stewardship or event lifecycle.

## 7. Implementation sequence (Trade compatibility stack)

| Step | Change | Repository |
|---|---|---|
| T-COMPAT-01 | This ADR, reviewed and accepted | Shared |
| T-COMPAT-02 | `context-registry.yaml`, `event-registry.yaml`, validator extension (§3.5), and registration of existing events | Shared |
| T-COMPAT-03 | Trade producer migration: event constants, `source`, forward DB migration for the trigger functions, and consumer-first coordination with ERP | Trade (+ ERP consumer) |
| T-COMPAT-04 | Canonical mapping, market and tenancy adaptation to current Shared | Trade |
| T-COMPAT-05 | Control Plane API adaptation | Trade |
| T-COMPAT-06 | Shared pin bump | Trade |
| T-COMPAT-07 | Full compatibility and conformance proof | Trade |

Trade#110 (lock shape only, pin unchanged) is independent of this stack.

## 8. Decisions (closed 2026-09-30, platform architecture owner)

### 8.1 The `erp` context: DEPRECATED, mandatory time-bounded re-homing

`erp` names an engine role, not a durable business context, so it is not
part of the target taxonomy. It is registered `DEPRECATED`:

> `erp` exists only to preserve compatibility with already-published
> canonical events. No new event type may be registered under it.

Each existing `erp.*` type is re-homed by business authority:

```text
existing erp.* event
        ├─ financial or accounting fact   → finance.*
        ├─ inventory fact                 → inventory.*
        ├─ fulfilment or logistics fact   → fulfilment.* / logistics.*
        └─ other domain fact              → the owning business context
```

The context is retired once no consumer, replay window or retained outbox
data still needs the legacy types. The re-homing is a separate ERP change
stack. It is mandatory and must not be deferred indefinitely.

### 8.2 `payments` versus `payment`: keep `payments`

`payments` stays the canonical event context (`ACTIVE`, related capability
domain `payment`). Event contexts and capability domains intentionally
differ here (§3.1). Renaming the shipped `payments.payment.*` types to
`payment.*` would create compatibility work without improving their
meaning.

Only baobab-payments produces `payments.*`. Trade never emits
payment-provider facts under `payments.*`. Its order-side facts stay
distinct (`commerce.order-payment.*`, P-1 to P-4), so no business fact has
two producers.

### 8.3 `fulfilment`, `logistics` and `trade.shipment`: three distinct contexts

ADR-0016 fixes the boundary. This ADR records it so later work does not
collapse the three contexts:

| Context | Meaning | Authority |
|---|---|---|
| `fulfilment.*` | The customer and commerce fulfilment lifecycle and promise | Trade (ADR-0016) |
| `logistics.*` | Physical execution | ERP, WMS, 3PL or the bound logistics provider |
| `trade.shipment.*` | The cross-border trade-shipment lifecycle | Trade, only where the shipment is a trade-execution aggregate and not another name for the logistics record |

These are different facts, not duplicates. For example:

```text
logistics.shipment.dispatched          physical execution happened
        │ evidence causes
        ▼
fulfilment.fulfilment-order.dispatched   the commerce fulfilment obligation moved to dispatched
```

F-3 and F-4 therefore become `fulfilment.fulfilment-order.dispatched.v1`
and `fulfilment.fulfilment-order.delivered.v1`.

### 8.4 Compliance after G-REG-NS Option B: decision and enforcement are split

Regulations owns regulatory meaning and evaluation. Trade owns operational
enforcement.

- **R-1:** product classification is regulatory meaning. It becomes
  `regulations.product-classification.assigned.v1`, produced by
  baobab-regulations or by a provider acting through the Regulations
  engine boundary. Customs consumes the classification. Customs-specific
  facts stay under `customs.*`, for example
  `customs.declaration.submitted`, `customs.duty-assessment.completed`
  and `customs.clearance.granted`.
- **R-2:** split into two facts. Regulations emits the decision,
  `regulations.compliance-assessment.decided.v1`. Trade emits the
  operational consequence, `trade.shipment-compliance.enforced.v1`, which
  references the assessment or decision id and does not copy the
  regulatory authority.

```text
Regulations  "this transaction is prohibited"  → regulations.compliance-assessment.decided
Trade        blocks the shipment or order      → trade.shipment-compliance.enforced
```

This is a decision/enforcement split (PDP and PEP). ADR-0021 and ADR-0024
are amended by reference as part of the G-REG-NS reconciliation (step 2).
Interim rule: if Regulations does not yet produce these facts when
T-COMPAT-03 lands, Trade does not mint them under a Trade- or
customs-owned name, and it cannot keep the legacy names, which the
current envelope rejects. Trade keeps its classification and compliance
decisions as internal (LOCAL) facts until Regulations produces the
canonical types, and it still emits `trade.shipment-compliance.enforced.v1`
for the enforcement it performs.

### 8.5 Digital Estate projections (`thamani-*`): retire now, in T-COMPAT-03

The estates being frozen makes this the safest time. The `thamani-*` types
name a Digital Estate, encode their target consumer, behave as commands,
and make the producer aware of who consumes its events. D-1 to D-9 are
retired in T-COMPAT-03:

- **D-1 to D-8 (trigger-emitted).** A new forward migration re-creates
  the trigger functions without the `thamani-*` commands. Migration
  history is untouched, and nothing is dual-published.
- **Pending unpublished legacy rows.** The T-COMPAT-03 PR states
  explicitly whether it drains them before cutover or maps them once in
  migration logic.
- **Already-published events.** They stay historical and immutable
  (§3.6).

When Thamani development resumes, it consumes canonical business facts,
for example `product.*`, `supplier.*`, `inventory.*`, `trade.order.*`,
`trade.shipment.*`, `payments.*` and `commerce.order-payment.*`, subject
to its subscriptions, context and authorisation.

## 9. Normative migration table (Trade)

Every legacy type Trade emits, from `src/baobab/events/event-contracts.ts`,
`src/baobab/thamani/events/index.ts` and the outbox trigger migrations
`Migration20260909110000` and `Migration20260909190000`. Every row becomes
normative when this ADR is accepted. No row is open (§8).

Disposition values:

- **RENAME:** the same fact under a canonical name.
- **REPLACE:** the producer emits an existing canonical type instead.
- **RETIRE:** the type is removed and consumers use the named canonical
  fact.
- **LOCAL:** the type is an internal fact and is not published
  cross-engine.
- **REHOME:** the fact belongs to another engine's authority. That engine
  produces the canonical type, and Trade stops producing it.

Producer column: **S** means the event is emitted from service code;
**T** means a database trigger function emits it.

### B2B organisation and approval (ADR-0017)

| # | Legacy type | Disposition | Canonical type | Producer | Rationale |
|---|---|---|---|---|---|
| B-1 | `commerce.b2b-organisation.created` | RETIRE | `customer.buyer-organisation.registered.v1` (existing) | S | ADR-0017: Trade consumes organisational identity and is not its authority. The canonical fact is the Control Plane's. |
| B-2 | `commerce.b2b-buyer.added` | RETIRE | `customer.buyer-membership.changed.v1` (existing) | S | Same authority reasoning. |
| B-3 | `commerce.b2b-approval.requested` | RENAME | `commerce.purchase-approval.requested.v1` | S | Order-approval workflow inside commerce. The request is itself a business fact. |
| B-4 | `commerce.b2b-approval.decided` | RENAME | `commerce.purchase-approval.decided.v1` | S | As B-3. |

### Inventory (ADR-0013, federated authority)

| # | Legacy type | Disposition | Canonical type | Producer | Rationale |
|---|---|---|---|---|---|
| I-1 | `commerce.inventory.reserved` | RENAME | `commerce.stock-reservation.placed.v1` | S | ADR-0013: Medusa is authoritative for commerce reservations. The fact is commerce's, not enterprise inventory's. |
| I-2 | `commerce.inventory.released` | RENAME | `commerce.stock-reservation.released.v1` | S | As I-1. |
| I-3 | `commerce.inventory.projected` | LOCAL | none; consumers use `erp.inventory.availability-changed.v1` | S | Trade's projection of ERP availability is a derived local fact. The authoritative fact is ERP's. |
| I-4 | `commerce.inventory.reconciled` | RENAME | `commerce.availability.reconciled.v1` | S | A commerce-side reconciliation outcome. It stays cross-engine only if a consumer needs it; otherwise LOCAL. |

### Payment (ADR-0015)

| # | Legacy type | Disposition | Canonical type | Producer | Rationale |
|---|---|---|---|---|---|
| P-1 | `commerce.payment.initiated` | RENAME | `commerce.order-payment.initiated.v1` | S | Trade orchestrates order payment. Provider execution facts are `payments.payment.*`, owned by baobab-payments. The distinct aggregate avoids two producers for one type. |
| P-2 | `commerce.payment.status-changed` | RENAME | `commerce.order-payment.status-changed.v1` | S | As P-1. |
| P-3 | `commerce.payment.reconciliation-required` | RENAME | `commerce.order-payment.discrepancy-detected.v1` | S | Past-tense fact rather than an instruction. |
| P-4 | `commerce.payment.reconciled` | RENAME | `commerce.order-payment.reconciled.v1` | S | As P-1. |

### Fulfilment (ADR-0016)

| # | Legacy type | Disposition | Canonical type | Producer | Rationale |
|---|---|---|---|---|---|
| F-1 | `commerce.fulfilment.requested` | RENAME | `fulfilment.fulfilment-order.requested.v1` | S | ADR-0016: Trade owns the commerce fulfilment lifecycle. `fulfilment` is a registered capability domain. |
| F-2 | `commerce.fulfilment.accepted` | RENAME | `fulfilment.fulfilment-order.accepted.v1` | S | As F-1. |
| F-3 | `commerce.fulfilment.dispatched` | RENAME | `fulfilment.fulfilment-order.dispatched.v1` | S | §8.3: the commerce lifecycle fact. Physical dispatch is `logistics.*`. |
| F-4 | `commerce.fulfilment.delivered` | RENAME | `fulfilment.fulfilment-order.delivered.v1` | S | §8.3, as F-3. |
| F-5 | `commerce.fulfilment.exception` | RENAME | `fulfilment.fulfilment-order.exception-raised.v1` | S | The legacy name is not past tense. |
| F-6 | `commerce.fulfilment.reconciled` | RENAME | `fulfilment.fulfilment-order.reconciled.v1` | S | As F-1. |

### Tax (ADR-0018 and Addendum)

| # | Legacy type | Disposition | Canonical type | Producer | Rationale |
|---|---|---|---|---|---|
| X-1 | `commerce.tax.determined` | RENAME | `tax.transaction-tax.determined.v1` | S | ADR-0018: Trade owns the transaction tax commitment. `tax` is a registered domain. |
| X-2 | `commerce.tax.reconciliation-required` | RENAME | `tax.transaction-tax.discrepancy-detected.v1` | S | Past-tense fact. |
| X-3 | `commerce.tax.reconciled` | RENAME | `tax.transaction-tax.reconciled.v1` | S | As X-1. |
| X-4 | `commerce.tax-profile.verified` | RENAME | `tax.tax-registration.verified.v1` | S | Buyer tax-registration verification. |

### Trade readiness and compliance (ADR-0021, ADR-0024; G-REG-NS Option B)

| # | Legacy type | Disposition | Canonical type | Producer | Rationale |
|---|---|---|---|---|---|
| R-1 | `trade.classification.assigned` | REHOME | `regulations.product-classification.assigned.v1` (producer: baobab-regulations) | S | §8.4: regulatory meaning belongs to Regulations. Customs consumes it. |
| R-2 | `trade.compliance.decided` | REHOME + split | `regulations.compliance-assessment.decided.v1` (Regulations), then `trade.shipment-compliance.enforced.v1` (Trade; references the assessment id) | S | §8.4: decision and enforcement split. |
| R-3 | `trade.cross-border-order.created` | RENAME | `trade.cross-border-order.created.v1` | S | Prefix change only. Relationship to `trade.order.placed.v1` to confirm in T-COMPAT-02. |

### ERP integration (commands expressed as events)

| # | Legacy type | Disposition | Canonical type | Producer | Rationale |
|---|---|---|---|---|---|
| E-1 | `commerce.erp-order.projection-requested` | REPLACE | `trade.order.placed.v1` (existing; ERP already declares it as received) | S | A command to a named engine. ERP subscribes to the business fact Shared already defines. |
| E-2 | `commerce.erp-fulfilment.projection-requested` | RETIRE | the F-series facts | S | Command to a named engine. |
| E-3 | `commerce.erp-financial-status.projected` | LOCAL | none; the authoritative fact is `erp.order.consequence-changed.v1` | S | Trade's local projection of an ERP fact. |
| E-4 | `commerce.erp-integration.reconciliation-required` | RENAME | `integration.sync.discrepancy-detected.v1` | S | `integration` is a registered capability domain; the event names no engine. |

### Digital Estate projections (`thamani-*`; retired in T-COMPAT-03, §8.5)

| # | Legacy type | Disposition | Canonical facts consumed instead | Producer |
|---|---|---|---|---|
| D-1 | `commerce.thamani-product.projection-requested` | RETIRE | product facts | T |
| D-2 | `commerce.thamani-supplier.projection-requested` | RETIRE | supplier facts | T |
| D-3 | `commerce.thamani-warehouse.projection-requested` | RETIRE | `erp.warehouse.changed.v1` | T |
| D-4 | `commerce.thamani-order.projection-requested` | RETIRE | `trade.order.placed.v1` | T |
| D-5 | `commerce.thamani-shipment.projection-requested` | RETIRE | `trade.shipment.*` | T |
| D-6 | `commerce.thamani-payment.projection-requested` | RETIRE | P-series / `payments.payment.*` | T |
| D-7 | `commerce.thamani-return-refund.projection-requested` | RETIRE | a return/refund fact, to be registered | T |
| D-8 | `commerce.thamani-credit-line.projection-requested` | RETIRE | a credit-line fact, to be registered (ADR-0027) | T |
| D-9 | `commerce.thamani.reconciliation-required` | RETIRE | E-4 | S |

The rationale is the same for every D row: the types name a tenant and
Digital Estate and are commands to a consumer. Estates consume canonical
facts filtered by the envelope's tenant and estate attributes.

**Summary:** 38 legacy types.

| Disposition | Count |
|---|---:|
| RENAME | 21 |
| REPLACE | 1 |
| RETIRE | 12 |
| LOCAL | 2 |
| REHOME | 2 |
| Open | 0 |

Eight types are emitted by database triggers and need the §3.7 forward
migration: D-1 to D-8.
