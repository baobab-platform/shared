# EA-02B — Candidate Capability Review

**Governing decision:** ADR-SHARED-017 §12–14 (Accepted)
**Input:** `docs/architecture/ea-02a-capability-census.md`
**Reviewed:** 2026-09-30 against Shared `a8cecd6`

The EA-02A census recorded implemented work that has no canonical
capability. This review decides, for each candidate, whether it becomes a
canonical key, at what granularity and under which domain, and what must
exist first. A key becomes canonical only when a Shared PR adds it to
`contracts/capability/v1/catalogue.yaml` (§12).

**Decision (2026-09-30):** the platform owner accepted the review as
proposed.
- Both **Accept now** keys are catalogued in the same change as this record.
- The eight **Accept, contract first** keys are **reserved**. Each is
  catalogued once its Shared request/response contract lands and its
  engine conforms to it. Until then an engine lists it only as a
  `proposed_key` candidate, and no other capability may take the name.

## How candidates were tested

§13 asks whether a candidate is consumable, contractable, grantable or
composable, replaceable, testable, auditable and provider-neutral. The
catalogue makes **contractable** concrete: each contract major of a
canonical definition must name a Shared `request_schema` and
`response_schema` (`capability.schema.json#/$defs/capabilityContractVersion`).
A candidate whose request/response shapes live only in an engine repository
fails that test today, however real its implementation.

**Consumable** means another engine, a digital estate or the Control Plane
calls it through capability resolution. It excludes an engine's own admin
UI and a vendor's generated API: Payload's REST routes, for example, are
Payload-shaped rather than Baobab contracts.

Verdicts:

| Verdict | Meaning |
|---|---|
| **Accept now** | Passes every test, and the Shared contract already exists. Catalogued with this record |
| **Accept, contract first** | A real capability, but its Shared request/response contract must be written, and the engine's implementation conformed to it, before it is catalogued |
| **Defer** | Granularity or authority is unsettled; revisit when the named condition is met |
| **Not a capability** | Implementation detail, platform plumbing, or owned elsewhere (§13) |

Keys use `<domain>.<resource>.<action>` in a registered domain. They name
no vendor, and the resource and action words follow the catalogue
(`.manage` for a lifecycle a consumer drives, a verb for a single act).

## Summary

| Candidate | Proposed key | Owner | Verdict |
|---|---|---|---|
| Cancel a payment intent | `payment.intent.cancel` | baobab-payments | **Accept now** |
| Account for a commerce order in ERP (order-to-cash) | `finance.order-consequence.process` | baobab-erp | **Accept now** |
| ERP physical inventory availability | `inventory.availability.query` | baobab-erp | Accept, contract first |
| B2B buyer application, KYB evidence and decision | `customer.buyer-application.manage` | baobab-trade | Accept, contract first |
| B2B buyer membership and invitations | `customer.buyer-membership.manage` | baobab-trade | Accept, contract first |
| Human authentication | `identity.authentication.perform` | baobab-iam | Accept, contract first |
| Workload authentication | `identity.workload-token.issue` | baobab-iam | Accept, contract first |
| Content resolution | `content.entry.resolve` | baobab-cms | Accept, contract first |
| Research missions | `intelligence.research-mission.manage` | baobab-pulse | Accept, contract first |
| Evidence search (semantic retrieval) | `intelligence.evidence.search` | baobab-pulse | Accept, contract first |
| Market assortment, product trade profiles | — | — | Defer |
| Tax registrations | — | — | Defer |
| Sessions, revocation, identity lifecycle | — | — | Defer |
| Content management, media | — | — | Defer |
| ERP master data bootstrap | — | — | Defer |
| Buyer context resolution; ERP context, mapping, provisioning; Haystack pipelines; `iam.*` roles; MFA policy | — | — | Not a capability |

## Accept now

### `payment.intent.cancel`

| Test | Finding |
|---|---|
| Consumable | Trade and the digital estates cancel an uncaptured payment when an order is abandoned or voided |
| Contractable | Request `payment.schema.json#/$defs/CancelPaymentRequest`, response `#/$defs/PaymentIntent`, event `events.schema.json#/$defs/PaymentCancelled`, errors `problem-details`. All exist in `payments/v1` |
| Grantable | Per tenant, alongside `payment.intent.create` |
| Replaceable | The same semantics hold for the sandbox and HyperSwitch (ADR-PAY-0001) |
| Testable, auditable | `tests/payments.rs` (`manual_capture_decline_and_cancel`, late-cancel 409); `PaymentCancelled` event |
| Provider-neutral | Yes |

Granularity: cancelling an intent also voids an authorised, uncaptured
payment (`src/service.rs`). That is one consumer act, so it is one
capability, not a separate `payment.payment.void`. It is named on the
intent, like `payment.intent.create`.

Consequence: `baobab-payments` moves `payment.intent.cancel` from
`planned_capabilities` (CANDIDATE) to sandbox `support` (IMPLEMENTED).

### `finance.order-consequence.process`

| Test | Finding |
|---|---|
| Consumable | Trade needs its orders' ERP consequences (sales order, shipment, invoice, payment accounting). The Control Plane binds a tenant to an ERP provider for this (the `baobab-erp` README architecture, via CapabilityBinding) |
| Contractable | Request `erp/v1/commerce-order-consequence.schema.json` (the `tradeToErp` channel), response `erp/v1/order-consequence-status.schema.json` (the `erpOutcomes` channel and `GET /order-consequences/{commerce_order_id}`), errors `problem-details`. The contract is already vendor-neutral |
| Grantable | Per tenant with ERP |
| Replaceable | The contract exposes no iDempiere or ERPNext identifier and chooses no vendor release (`erp/v1` README); ERP mints its own public IDs |
| Testable, auditable | Outcome events; the ERP conformance ledger (ADR-ERP-016) |
| Provider-neutral | Yes |

Granularity: one capability for the whole sell-side consequence of a
commerce order. The five ERP facts (`erp.sales-order.accepted.v1` and the
rest) are events of that one capability, not separate capabilities: no
consumer requests "post an invoice" on its own.

Consequence: `baobab-erp` can declare it as a `CONTRACTED` planned
capability for `baobab-erp.idempiere`. Its sell-side order-to-cash
(`modules/order_to_cash/service.py`) is real, but it does not consume
`commerce-order-consequence` or publish `order-consequence-status` yet,
so it is not claimed as support. This gives ERP, an active engine, a
declaration.

## Accept, contract first

Each item below is a real capability whose request and response shapes
live only in the engine. The work is:

1. Write the Shared request/response schemas.
2. Conform the engine's routes to them.
3. Catalogue the key.
4. Declare support.

These keys are reserved: engines may already list them as `proposed_key`
candidates.

### `inventory.availability.query` (ERP)

`erp/v1` already has the response
(`inventory-availability.schema.json`) and the operation
(`GET /inventory-availability`). Its query parameters have no request
schema, so the contract needs an `InventoryAvailabilityQuery` schema. ERP
has no route for it yet. This is the smallest contract gap in the review.

### `customer.buyer-application.manage` and `customer.buyer-membership.manage` (Trade)

`buyer-organisation/v1` makes Trade the authority for buyer applications,
commercial approval and buyer membership. It keeps this separate from CP
tenant admission (`admission/v1`, ADR-BCP-017) and from CP organisation
registration. The package defines the entities and events, and Trade
validates its events against them. The route request/response shapes
(apply, evidence, review and decision; invite, accept, revoke and resend)
are Trade-local.

Granularity: two capabilities, not one family and not one per route.

- **Application:** a bounded onboarding lifecycle (DRAFT to APPROVED or
  REJECTED), driven by the buyer and the reviewer.
- **Membership:** an ongoing roster with roles and purchasing authority,
  which starts only after approval.

They have different events, different actors and different lifetimes. The
evidence decision belongs inside the application capability.

Domain: `customer`. Buyer approval is a tenant's commercial acceptance of a
customer, not canonical organisation registration, which is `organisation`
and CP-owned (ADR-BCP-018).

### `identity.authentication.perform` and `identity.workload-token.issue` (IAM)

ADR-SHARED-017 §44 makes identity authentication the model capability that
must survive Keycloak → Ory, and the review follows it.

Granularity: human and workload authentication are two capabilities.

- **Human:** interactive and session-based, with assurance and step-up
  (ADR-IAM-0024).
- **Workload:** client credentials, no session, `actor_type=workload`
  (ADR-0007).

They have different consumers, different credentials and different
failure modes. Workforce, B2B, customer and supplier are **populations**,
not capabilities: `actor_type` and realm policy distinguish them.

Contract: `identity/v1` has the principal, session, assurance and
workload-identity shapes, but no authentication request/response profile.
The ADR-0006 token profile (what a relying party sends, and the claims it
receives) must be expressed as Shared schemas first. OIDC stays the wire
protocol, and the Baobab contract is the profile over it.

### `content.entry.resolve` (CMS)

Content resolution is the CMS capability other parties consume. Digital
estates ask for the right content for a market, locale and context, and
get deterministic inheritance, fallback and fail-closed ambiguity
(`src/baobab/content-resolution`, tested against ADR numbering). It is
replaceable: the resolution semantics are Baobab's, not Payload's.

There is no `content/v1` package in Shared. It needs a request (context,
market, locale, entry reference) and a response (resolved entry with
provenance).

### `intelligence.research-mission.manage` and `intelligence.evidence.search` (Pulse)

Both are exposed (`POST /research-missions`, `GET /research-missions/{id}`,
`POST /evidence/search`), consumable and provider-neutral. Haystack sits
behind an anti-corruption layer. Their contracts live in
`src/baobab_pulse/contracts/api` and need a Shared `intelligence/v1`
package.

Pulse is a self-declared scaffold, so it should do this after its
first production intelligence domain, not before. Until then these stay
candidates.

## Defer

| Candidate | Condition to revisit |
|---|---|
| Market assortment, product trade profiles (Trade, ADR-0030) | Catalogue authority between Trade and CMS product content (CMS ADR-0015) is settled, and a Shared catalogue contract exists |
| Tax registrations (Trade, ADR-0018) | Whether registration management is Trade's or a Regulations/tax concern is decided (G-REG-NS) |
| Sessions, revocation, identity lifecycle (IAM-12) | The deprovisioning saga (ADR-0016) exists. Today this is admin action plus `identity-events/v1`, with no consumer-invoked contract |
| Content management, media (CMS) | A non-editorial consumer needs them. Today they are Payload's editorial API, which is vendor-shaped |
| ERP master data bootstrap (ADR-ERP-014) | The canonical organisation owner that `erp/v1` leaves unassigned is decided |

## Not a capability

- **Buyer context resolution:** the Control Plane's authority
  (`trade/v1/buyer-context.schema.json`).
- **ERP `/context/resolve*`, `/mapping/resolve*`, `/events/inbound` and
  provisioning operations:** tenant, mapping and provisioning plumbing.
  Provisioning is a platform operation on the engine, not a tenant
  capability.
- **Haystack pipelines and the Qdrant projection:** §13's own invalid
  example.
- **`iam.*` role names:** administrative permissions.
- **MFA and passkey policy:** policy within `identity.authentication.perform`,
  expressed as assurance, not a separate capability.

## Consequences

- **Declarations:**
  - ERP can declare now (`finance.order-consequence.process`, CONTRACTED).
  - IAM, CMS and Pulse can declare once their first contract lands; until
    then they may list the reserved keys as `proposed_key` candidates.
  - Trade adds its two customer keys when `buyer-organisation/v1` gains
    request/response schemas.
- **G-FCI-1:** stays off until IAM, CMS and Pulse declare. The earliest
  path is the identity token profile, `content/v1` resolution, and Pulse's
  `intelligence/v1`.
- **Proposed contract work, smallest first:**
  1. `erp/v1` InventoryAvailabilityQuery.
  2. `buyer-organisation/v1` commands.
  3. The `identity/v1` authentication profile.
  4. `content/v1` resolution.
  5. `intelligence/v1`.
