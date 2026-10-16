# ADR-SHARED-039 — Trade Order Authority and CP-Owned Seller Operating Bindings

**Status:** Accepted — Normative Shared Contract Architecture (platform owner decisions for EA-R03 Trade, 2026-10-16)  
**Date:** 2026-10-16  
**Repository:** `baobab-platform/shared`  
**Decision ID:** ADR-SHARED-039  
**Work item:** EA v2.2 EA-R03 / D-03 / LA-05, P0-04B Trade increment Trade-0  
**Depends On:** ADR-SHARED-034 (resolution pattern), ADR-SHARED-035 (money movement), ADR-BCP-026/027, Trade ADR-0010 §28, ADR-0014, ADR-0015  
**Semantic Owners:** Control Plane (seller operating authority and legal authority), `baobab-trade` (native commerce execution and attribution)  
**Canonical Contract:** `contracts/trade/v2/order-operations.yaml` (catalogue `version: 1`), `contracts/trade/v2/order-authority.schema.json`, `contracts/trade/v2/seller-operating-binding.schema.json`

---

## 1. Decision

The guiding rule is:

> Every consequential Trade operation must be classified and authorised at its actual execution point, regardless of which API, workflow, administrator, background job or database path initiates it.

The cart-completion fence (P0-04B-03) is not a general enforcement boundary. A seller binding that was never activated is never an escape route from authorisation:

> Absence of a seller binding is grounds for denial, never grounds for exemption from enforcement.

Trade enforcement is delivered in five bounded increments, in this order: Trade-0, then Trade-A, Trade-B, Trade-C, and finally Trade-D.

| Increment | Scope | Completion condition |
|---|---|---|
| **Trade-0** | This contract, the CP Seller Operating Binding registry and lifecycle, the CP Trade Order Authority resolver, and Trade's native-configuration attestation | The catalogue, binding and decision contracts are frozen, and CP is authoritative for binding state |
| **Trade-A** | Cart completion, direct order creation, admin and draft order creation and finalisation, and every route that creates or commits an order | No order is created or committed without valid authority, whatever the entry point |
| **Trade-B** | Order edits, cancellations, returns, exchanges and claims | Every consequential lifecycle transition has its own class. Unrecognised transitions are denied |
| **Trade-C** | Trade's requests for payment authorisation, capture, void and refund, and for fulfilment and shipment | Every outbound effect carries authorised commercial provenance. Receiving engines enforce their own authority |
| **Trade-D** | All remaining native write surfaces, order tables, background jobs, direct-write bypasses and cross-engine retries, plus real-runtime acceptance | No unclassified protected mutation commits, and real-runtime acceptance is demonstrated |

Trade-D is the comprehensive closure and certification pass. It never permits Trade-A to C to leave exposed the write paths they introduce. Every increment protects its own write paths at the HTTP boundary, at the workflow and service boundary, and in persistence.

Until each increment establishes its enforcement boundary, every affected consequential operation is **denied in protected environments** (§6).

## 2. Closed catalogue

`order-operations.yaml` is a closed catalogue in which each class names exactly one legal-actor role and one activity. CP derives both from the catalogue, and the caller never supplies them. A generic class such as `trade.order.manage` must never exist.

All classes use the role `SELLER_OF_RECORD`. Each class has its own activity, so a mandate scoped to one never covers another. No Trade activity coincides with an `erp/v2` or `payments/v2` activity.

| Class | Activity | Increment | Activatable |
|---|---|---|---|
| `trade.order.commit` | `CHECKOUT_ORDER_COMMITMENT` | Trade-A | yes |
| `trade.order.create` | `DIRECT_ORDER_COMMITMENT` | Trade-A | yes |
| `trade.draft-order.finalize` | `DRAFT_ORDER_FINALISATION` | Trade-A | yes |
| `trade.order.edit` | `ORDER_AMENDMENT` | Trade-B | no |
| `trade.order.cancel` | `ORDER_CANCELLATION` | Trade-B | no |
| `trade.return.accept` | `RETURN_ACCEPTANCE` | Trade-B | no |
| `trade.exchange.accept` | `EXCHANGE_ACCEPTANCE` | Trade-B | no |
| `trade.claim.accept` | `CLAIM_ACCEPTANCE` | Trade-B | no |
| `trade.payment-authorization.request` | `PAYMENT_AUTHORIZATION_INSTRUCTION` | Trade-C | no |
| `trade.payment-capture.request` | `PAYMENT_CAPTURE_INSTRUCTION` | Trade-C | no |
| `trade.payment-void.request` | `PAYMENT_VOID_INSTRUCTION` | Trade-C | no |
| `trade.payment-refund.request` | `PAYMENT_REFUND_INSTRUCTION` | Trade-C | no |
| `trade.fulfilment.create` | `FULFILMENT_INSTRUCTION` | Trade-C | no |
| `trade.shipment.create` | `SHIPMENT_INSTRUCTION` | Trade-C | no |

**Activatable classes.** CP resolves a class only when it is `activatable`. For every other class it answers `OPERATION_NOT_ACTIVATED` before any mandate lookup, and Trade refuses the route by name. Only a reserved class may receive that answer. A later increment activates its classes through a versioned catalogue revision.

**Catalogued is not supported.** Trade publishes support for a class only once its enforcement, bypass closure and acceptance evidence exist.

`capability_key` is null for every class until finance and commerce capability keys are registered. A null key matches only mandates that have no capability scope (ADR-SHARED-034 §5).

**Independent decisions.**
- Creation and material change are separate decisions. An authorised commitment never authorises a later change to seller, responsible legal entity, total, currency, payment beneficiary or fulfilment obligations.
- A derived native row may inherit its root operation's decision only where Trade proves same-operation causality and transactional provenance.

**Separate authorities.**
- A Trade decision is never money-movement authority (ADR-SHARED-035) and never ERP posting authority (ADR-SHARED-034).
- A Trade-C payment instruction is the commercial request only. Payments independently resolves its own `payments/v2` decision and checks provider readiness.
- Fulfilling an order never authorises ERP shipment completion or costing.

## 3. Seller Operating Bindings are CP-owned

> The Control Plane SHALL be the authoritative system of record for reusable Seller Operating Bindings, including their canonical scope, approval, activation, suspension, revocation and effective-dated lifecycle. Trade SHALL remain authoritative for native seller configuration, carts, orders and transactional seller attribution. Trade MAY retain a local projection of CP binding state but SHALL NOT independently confer or extend binding authority. Every consequential Trade operation SHALL require a current CP-issued authorization resolving an applicable ACTIVE Seller Operating Binding and an independently valid legal-actor mandate. Existing per-cart binding records SHALL remain historical evidence and SHALL NOT automatically be promoted into reusable Seller Operating Bindings.

| Information | Authoritative owner |
|---|---|
| Tenant, operating Organisation, legal entity, market | CP |
| Seller Operating Binding identity, version, scope, lifecycle and current status | CP |
| Human proposal, approval, activation, suspension and revocation | CP, with IAM-authenticated principals |
| Medusa seller configuration, sales channels and native identifiers | Trade |
| Cart and order seller attribution, and the immutable commitment snapshot | Trade |
| Operation-specific legal-actor decision | CP |
| Order creation, change and fulfilment execution | Trade |

**A binding is scoped to the seller's operating context, not to a cart.** That context is: tenant, operating Organisation, responsible legal entity, market, Trade engine instance, currency scope and Trade's attested native configuration. The native configuration covers sales channels and regions.

CP stores only an opaque `native_configuration_reference` and its SHA-256 `native_configuration_digest`. It never copies Medusa's seller, channel or region tables.

**Lifecycle** (`seller-operating-binding.schema.json`):

1. **Attest.** The Trade workload submits an authenticated native-configuration attestation, covering configuration reference, digest, currency scope and engine instance, under its RUNTIME context. CP validates the canonical side: tenant, Organisation, market and the engine instance's binding to the tenant. CP then records the attestation. An attestation authorises nothing.
2. **Propose.** A human maker proposes a binding version from one attestation, naming the responsible legal entity and the effective period. CP persists it as `PENDING_APPROVAL`.
3. **Approve.** A different human checker approves that exact version, and its status becomes `APPROVED`.
4. **Activate.** A third human operator activates it, and the binding becomes `ACTIVE`. CP first revalidates the legal entity's verification, the engine-instance binding, the attestation and the effective dates. **Only CP's durable commit of `ACTIVE` activates a binding.** Neither a published event nor a Trade projection does.
5. **Suspend, reinstate or revoke.** An operator may suspend an ACTIVE binding. Reinstating it is a fresh activation under the same separation-of-duties checks. Revocation is terminal. A change of scope or native configuration is a new version, which supersedes the old one.

**Separation of duties.**
- Maker, checker and operator are three distinct canonical principals.
- Each command needs its own exact `organisation.seller-operating-binding.*` administrative grant (HIGH risk, ORGANISATION scope, not delegable). These grants are registered but assigned to no profile.
- Every transition is an immutable history row.
- CP publishes a versioned `trade.seller-operating-binding.changed` lifecycle event through its transactional outbox, but the event is information, not authority.

**Disagreement always fails closed.**

| Condition | Treatment |
|---|---|
| CP says ACTIVE, Trade's projection says otherwise | Trade refreshes its projection. The projection is never authority |
| Trade says ACTIVE, CP says SUSPENDED, REVOKED or missing | Deny |
| Trade's current native-configuration digest differs from the attested one | Deny until re-attested and a new version is activated |
| A legacy ACTIVE per-cart binding exists but no CP binding | Deny new consequential operations |
| CP is unreachable | Fail closed for new consequential operations |
| The binding is revoked after an order was committed | Preserve the historical order. Govern further actions separately (§5) |

**Migration of existing per-cart bindings.** Existing `native_seller_cart_binding` records stay in Trade as immutable historical evidence. They are never copied into CP or treated as reusable authority. New reusable bindings are proposed with references to that evidence, and then go through the governed approval and activation steps above. An approved migration process may batch proposals. It may never manufacture approval evidence.

## 4. CP Trade Order Authority resolver

`POST /internal/trade/v1/order-authority/resolve` uses scope `trade-order-authority:resolve`. It is workload-only and admits no human or client.

**Request.** The request names only:
- a workload-owned RUNTIME `context_id`;
- the `engine_instance_id`;
- an `operation_class`;
- a `seller_operating_binding_reference` (`binding_id`, `binding_version`);
- Trade's current `native_configuration_digest`;
- the operation's ISO 4217 `currency`, which CP requires to be in the binding's `currency_scope` and echoes back;
- an opaque `operation_reference`.

The caller can never select a tenant, Organisation, legal entity, mandate, role, activity, market or time.

**What CP checks, in order:**
1. It redeems the RUNTIME context.
2. It loads the binding from its own store by id and version.
3. It requires `ACTIVE` status, the effective period, and no supersession, suspension or revocation.
4. It requires that tenant, Organisation, market and Trade engine instance all match the binding's scope.
5. It requires that the digest equals the attested digest, and that the currency is in the binding's currency scope.
6. It derives the role and activity from the catalogue, answering `OPERATION_NOT_ACTIVATED` for reserved classes.
7. It resolves exactly one current, verified `SELLER_OF_RECORD` mandate of the binding's legal entity that covers that activity.

**Outcomes.**
- Positive and negative outcomes are both recorded immutably.
- `AUTHORIZED` lasts at most 30 seconds, is bound to one binding version, one operation class and one operation reference, and grants nothing (`provider_permissions_granted: false`).
- A missing binding, an unavailable store, an incomplete activation record or an ambiguous assignment answers a denial outcome or 503. It is never assumed to be ACTIVE.

**Trade's obligations.** Trade enforces each decision at the consequential execution point. It denies once `min(expires_at, its own receipt + 30 s)` has passed. It persists immutable commitment-time attribution on every order:
- binding id and version;
- Organisation;
- legal entity;
- market;
- engine instance;
- CP decision id;
- mandate;
- the authorisation time.

## 5. Binding resolution and remediation

**Exactly one binding, whatever the entry point.** Every consequential Trade order operation resolves exactly one applicable ACTIVE Seller Operating Binding, however the order originated:
- cart checkout;
- direct API;
- Admin API;
- draft finalisation;
- background process;
- import.

Zero matching bindings deny, and so do several. An administrator's choice of seller is only a request. Trade verifies that the principal may act for that Organisation, and CP decides the seller's authority. Native Medusa RBAC never substitutes for it.

**Binding discovery** (Trade-A TA-01, owner decision 2026-10-16).

> Trade SHALL discover an applicable Seller Operating Binding through an authenticated, scope-bound CP resolution operation using Trade's attested native configuration reference and digest.
>
> CP SHALL derive canonical tenant, operating Organisation and market from the authenticated runtime context and SHALL return exactly one currently applicable ACTIVE binding reference or deny resolution.
>
> Trade SHALL remain authoritative for mapping native carts, drafts, orders, sales channels and regions to the attested configuration. Native Medusa identifiers SHALL NOT be introduced into CP's canonical binding registry.
>
> Binding discovery SHALL NOT constitute commercial authority. Every consequential Trade operation SHALL independently obtain a current, operation-specific CP Order Authority decision for the resolved binding version.
>
> Event delivery and local projections MAY optimise discovery but SHALL NOT be required for correctness or substitute for current CP authorization.

`POST /internal/trade/v1/seller-operating-bindings/resolve` uses scope `trade-seller-binding:resolve`. It is workload-only, held by the same PROVISIONED staging workload, and grants no authority. Its request (`BindingResolveRequest`) names only:
- a workload-owned RUNTIME `context_id`;
- the `engine_instance_id`;
- Trade's opaque `native_configuration_reference`;
- Trade's current, independently recomputed `native_configuration_digest`;
- the ISO 4217 `currency` of the cart, draft or order.

CP evaluates its own registry at the time of the request. Candidates must match the context's tenant, operating Organisation and market, the engine instance, the reference, and have the currency in scope. Then, in order:

| Condition | Outcome |
|---|---|
| No candidate | `NO_APPLICABLE_BINDING` |
| No candidate is ACTIVE and in effect | `BINDING_NOT_ACTIVE` |
| ACTIVE, in-effect candidates exist, but none was attested under the request digest | `NATIVE_CONFIGURATION_MISMATCH` |
| More than one ACTIVE, in-effect candidate has the digest | `AMBIGUOUS_BINDING` |
| Exactly one | `RESOLVED`, with its `binding_reference` |

An unusable context answers `CONTEXT_NOT_USABLE`, and an unbound engine instance `ENGINE_INSTANCE_NOT_BOUND`. Every outcome except `RESOLVED` denies. CP records every resolution immutably before answering. `examples/binding-resolution-vectors.json` pins the precedence.

**No overlapping in-force scopes.** CP SHALL refuse to activate a binding version when another binding of the same tenant, operating Organisation, market and engine instance is in force (ACTIVE or SUSPENDED) for the same native configuration reference with an intersecting currency scope. `AMBIGUOUS_BINDING` remains a defence in depth; it is never a normal state.

**Trade's use of a resolution.** Trade may store the resolved binding version with the cart or draft as provisional attribution and reuse it as the candidate for later operations, only while its current native configuration still produces the same reference and digest. Otherwise it re-resolves. Trade never silently substitutes a different seller or binding, and a stored reference is never permission: each operation still obtains its own order-authority decision.

**Drafts.** Carts and drafts may hold provisional attribution while they remain non-consequential. They cannot become authoritative orders, reserve consequential resources, or start payment or fulfilment without a current binding and a fresh decision. If the seller changes, the provisional attribution is re-evaluated.

**Multiple sellers.** A commitment that involves more than one independent legal seller is denied until a separately governed multi-seller order model exists.

**Remediation.** A historical order stays readable under its preserved attribution, whether or not the seller is still ACTIVE. Remedial actions on the order of an inactive seller are refunds and cancellations. They need a separately governed wind-down and remediation authority, and are denied until that authority is catalogued. An inactive binding is never treated as ACTIVE.

## 6. Deny by name in protected runtimes

> In protected Trade runtimes, every consequential native Medusa route, custom route, workflow, service invocation and persisted effect SHALL resolve to exactly one supported canonical operation class, or be DENIED. Native Medusa RBAC SHALL NOT substitute for CP seller binding, legal-actor authorization or operation-specific authority. Uncatalogued financial operations SHALL NOT invoke a payment provider. Native Medusa capture and refund SHALL delegate through Baobab Payments' governed execution boundary. Historical reads and demonstrably non-consequential draft operations MAY remain available under independent IAM and tenant-isolation controls. Each operation class SHALL remain unavailable until its enforcement, bypass closure and acceptance evidence are demonstrated.

**What is denied.** Until each is catalogued, activated and enforced, these are denied in protected runtimes:
- admin order creation and draft finalisation;
- order edits, cancellations and status changes;
- returns, exchanges and claims;
- payment authorisation, capture and refund;
- fulfilment, shipment and delivery completion;
- commercially consequential inventory reservation or release;
- administrative pricing, seller, market or merchant reassignment.

**Effects, not names.** The denial applies to effects, not URL names. A route described as a draft update is denied if it creates an order, triggers a payment or changes a legally consequential obligation. Webhook-triggered cart completion uses the same gate.

**Three layers.** Each increment enforces at three layers:
- the HTTP boundary, with an explicit allowlist that authenticated administrators cannot bypass;
- the workflow and service boundary, covering non-HTTP invocation;
- the persistence and provider boundary.

The acceptance test for each increment drives a native Admin request, a direct workflow invocation and the persistence or provider side effect. All three must reach the same outcome.

**HTTP responses** use RFC 9457 problem documents and `Cache-Control: no-store`. A route never falls back to Medusa's ordinary handler after a denial.

| Condition | Status |
|---|---|
| No or invalid authentication | `401` |
| Insufficient permissions, or a missing, inactive or mismatched binding | `403` |
| Uncatalogued, reserved or prohibited mutation | `403`, code `TRADE_OPERATION_NOT_AUTHORISED` |
| CP authority temporarily unavailable | `503` |
| Catalogued, but provider capability not certified | `503`, readiness-specific code |
| Valid operation in an invalid lifecycle state | `409` |

## 7. Evidence and classification

- **Contract checks.** `validate-trade-order-authority-contract.py` checks:
  - the closed catalogue, with one role and one unique activity per class, no generic class, and no reuse of an ERP or Payments activity;
  - that the Trade-A classes alone are activatable;
  - the request, which must not let the caller select authority and must not carry native identifiers;
  - the decision's 30-second lease, role and activity binding, and `provider_permissions_granted: false`;
  - the binding lifecycle shapes, including three distinct principals.
- **Classification.** Engine-local real-component evidence on synthetic data is **not EA Gate D and not L4** (EA v2.2 §§3, 7). Protected and production commerce stay denied. Activation is never a flag.

## 8. Not decided here

- Real mandates, bindings and workload admission.
- Commerce capability keys.
- The remediation and wind-down authority class.
- The multi-seller order model.
- Payment-provider approval and certification (ADR-SHARED-035 D2).
- The Trade-B and Trade-C catalogue revisions that activate their classes.
