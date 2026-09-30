# EA-02A — Capability Census

**Governing decision:** ADR-SHARED-017 §12–13 and Phase 2 (Accepted)
**Companion:** `docs/architecture/ea-02-capability-catalogue.md` (implementation record)
**Started:** 2026-09-30

This census records, per engine, what each engine actually implements
against the Canonical Capability Catalogue, based on repository evidence.
It is the input to catalogue changes and engine provider declarations
(`.baobab/capability-provider.yaml`). It creates no canonical keys itself
(§12): a candidate becomes canonical only through an accepted Shared PR
that adds it to `contracts/capability/v1/catalogue.yaml`.

Each finding is classified as one of:

| Class | Meaning |
|---|---|
| **Implemented** | The canonical contract is implemented, with evidence |
| **Partial** | Part of the canonical contract is implemented |
| **Contracted, unimplemented** | Canonical in Shared, not implemented by this engine |
| **Candidate** | Implemented or intended, but no canonical capability exists. Needs architecture review |
| **Implementation detail** | Not a capability (§13) |
| **Owned elsewhere** | Belongs to another engine's or Shared's authority |

## Progress

| Engine | Census | Declaration | Canonical capabilities | Implemented | Candidates recorded |
|---|---|---|---:|---:|---|
| Payments | Surveyed | baobab-payments#12 | 4 | 4 (sandbox) | `payment.intent.cancel` |
| Subscriptions | Surveyed | baobab-subscriptions#18 | 2 | 2 (temporary-billing) | none |
| Trade | Surveyed | baobab-trade#109 (planned-only) | 3 | 0 | B2B onboarding family (review, below) |
| IAM | Not yet | — | 0 | — | — |
| CMS | Not yet | — | 0 | — | — |
| ERP | Not yet | — | 0 | — | — |
| Pulse | Not yet | — | 0 | — | — |
| Regulations | Not yet (namespace review first, §43) | — | 0 | — | — |

The survey order follows the EA-02 audit: engines with canonical
definitions first, then IAM, CMS, ERP and Pulse, and Regulations last.

## Payments (`baobab-payments`, audited at `03ff405`)

| Finding | Class | Evidence |
|---|---|---|
| `payment.intent.create` | Implemented | `src/http.rs`, `src/service.rs`, `tests/payments.rs` |
| `payment.payment.authorize` | Implemented | `src/service.rs` (confirm), `src/provider.rs`, `tests/payments.rs` |
| `payment.payment.capture` | Implemented | same |
| `payment.refund.create` | Implemented | same; ADR-PAY-0013 |
| Cancel a payment intent (`POST /v1/payment-intents/{id}/cancel`) | **Candidate** `payment.intent.cancel` | Implemented in `src/service.rs`. Shared `payments/v1` already defines `CancelPaymentRequest` and `PaymentCancelled`; ADR-PAY-0008 lifecycle |
| Read intent / payment by tenant | Implementation detail | Read routes that support the capabilities above; not separately grantable today |
| HyperSwitch provider | Not implemented | ADR-PAY-0001 is accepted, but `src/provider.rs` has only the sandbox. No provider is declared until the adapter exists |
| Payout, disputes, settlement (ADR-PAY-0014–0016) | Not surveyed as candidates | Architecture only; no implementation |

Only the sandbox provider is implemented (simulated, never production
permitted). Its declaration regenerates the transitional
`payments/v1/capabilities.json` bundle.

## Subscriptions (`baobab-subscriptions`, audited at `a7a3bf4`)

| Finding | Class | Evidence |
|---|---|---|
| `billing.subscription.manage` (ensure, read, suspend, resume, terminate a billing projection) | Implemented | `HttpApi.java`, `BillingService.java`, `TemporaryProvider.java`, `BillingScenarios.java`, `PostgresBillingTest.java` |
| `billing.usage.record` | Implemented | `HttpApi.java`, `BillingService.java`, `BillingScenarios.java`, `PinnedContractsTest.java` |
| Kill Bill provider | Not implemented | ADR-SUB-0001 is accepted, but only `TemporaryProvider` exists |
| Invoice projection, credits, payment obligation (ADR-SUB-0012–0013) | Not surveyed as candidates | Architecture only; no implementation |

Every HTTP route maps to one of the two canonical capabilities. The
declaration regenerates the transitional `subscriptions/v1/capabilities.json`
bundle exactly.

## Trade (`baobab-trade`, audited at `170c54e`)

| Finding | Class | Evidence |
|---|---|---|
| `commerce.cart.manage` | **Contracted, unimplemented** | There is no canonical quick-order route. Medusa's native cart, guarded by `src/workflows/thamani-cart-eligibility-guard.ts`, is not the canonical contract |
| `commercial.rfq.manage` | **Contracted, unimplemented** | No RFQ route |
| `commercial.quotation.manage` | **Contracted, unimplemented** | No quotation route |
| B2B buyer organisation onboarding: apply, KYB evidence, review and decision (`src/api/{store,admin}/b2b/applications/**`, `organisations/apply`) | **Candidate family, needs review** | Implemented (Gate ZB-04, `conformance/zb04-certification.json`); Shared has `buyer-organisation` and `supplier-onboarding` contracts, but no canonical capability |
| B2B organisation membership and invitations (`organisations/{id}/members/**`, `invitations/accept`) | **Candidate family, needs review** | Implemented; overlaps `organisation` and `customer` namespaces |
| Buyer context resolution (`store/b2b/context`) | Owned elsewhere / needs review | Shared `trade/v1/buyer-context.schema.json`; resolution authority is shared with the Control Plane |
| Market assortment and product trade profiles (`store/b2b/assortment`, `admin/b2b/product-trade-profiles/**`) | **Candidate family, needs review** | Implemented (ADR-0030, ZB-06); `catalogue` namespace |
| Tax registrations (`organisations/{id}/tax-registrations`) | **Candidate, needs review** | `tax` namespace (ADR-0018) |
| Capability snapshot (`store/b2b/capabilities`) | Implementation detail | A per-buyer feature snapshot, not a Baobab capability |
| ERP projection and inbound ERP events | Owned elsewhere / integration | ADR-0005 boundary; `integration` namespace if ever exposed |

The Trade declaration is therefore **planned-only**: all three canonical
capabilities are `CONTRACTED` for `baobab-trade.medusa`. The B2B families
above are real implemented platform value without canonical keys, which is
the architecture debt §58 names. They need an architecture review to
decide granularity (§13: consumable, contractable, grantable, replaceable,
testable, auditable, provider-neutral) before any key is proposed.
Declarations do not invent keys for them.

## Next

1. Review the recorded candidates (`payment.intent.cancel`, Trade's B2B
   families) and add accepted ones to the catalogue with canonical
   definitions.
2. Survey IAM, CMS, ERP and Pulse the same way, then Regulations after
   the `regulations` namespace review.
3. Until the active engines (Trade, ERP, CMS, Pulse, IAM) have
   declarations, Foundation enforcement (G-FCI-1) stays off.
