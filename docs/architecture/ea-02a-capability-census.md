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
| Payments | Surveyed | Merged (baobab-payments#12) | 5 | 5 (sandbox), once the declaration adds `payment.intent.cancel` | none; `payment.intent.cancel` accepted |
| Subscriptions | Surveyed | Merged (baobab-subscriptions#18) | 2 | 2 (temporary-billing) | none |
| Trade | Surveyed | Merged, planned-only (baobab-trade#109) | 3 | 0 | B2B families (review, below) |
| IAM | Surveyed | Waits for accepted candidates | 0 | — | Authentication families (review, below) |
| CMS | Surveyed | Waits for accepted candidates | 0 | — | Content families (review, below) |
| ERP | Surveyed | Can declare `finance.order-consequence.process` (CONTRACTED) | 1 | 0 | Finance and order-to-cash families (review, below) |
| Pulse | Surveyed | Waits for accepted candidates | 0 | — | Intelligence families (review, below) |
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

## Engines without canonical capabilities

IAM, CMS, ERP and Pulse have no canonical capability in the catalogue
today. A declaration must name at least one supported or planned
capability, so a declaration for any of them would have to propose new
keys. They therefore get **no declaration yet**: their findings below are
candidate families for architecture review, the same treatment as Trade's
B2B families. Once a review accepts a key into the catalogue, the engine
declares it, and until then nothing invents one. The namespaces named
below are the registered `capabilityDomain` values each family would fall
under; they are not keys.

## IAM (`baobab-iam`, audited at `6891527`)

IAM is Keycloak configured as code (ADR-0002); `providers/` holds no
custom SPI. So the implemented provider would be `baobab-iam.keycloak`
(`implementation_key: keycloak`), with `baobab-iam.ory` planned by
ADR-IAM-0019 to ADR-IAM-0022. The ADR's §44 example shows why the
capability must outlive either provider.

| Finding | Class | Evidence |
|---|---|---|
| Human authentication: workforce SSO (IAM-5), B2B organisation members (IAM-6 phase 1) | **Candidate family, needs review** (`identity`) | `config/realm/baobab-realm.json`, `config/clients/*-admin.json`, `tests/integration/run.sh`. ADR-SHARED-017 §14 uses `identity.authentication.perform` only as a conceptual example; it is not a key |
| Workload authentication (client credentials with `actor_type=workload`, IAM-4) | **Candidate family, needs review** (`identity`) | `config/clients/*-workload.json`; CP enforces the claim |
| Sessions, revocation and identity lifecycle (IAM-12 phase 1) | **Candidate family, needs review** (`identity`) | Realm admin events and the disable-and-revoke flow; Shared `identity-events/v1` |
| Credentials and MFA (IAM-11 phase 1) | Implementation detail today | Realm policy for privileged roles, not a separately consumable service |
| Customer (IAM-7) and supplier (IAM-8) identity | Not implemented | Scoped only; each has an open ownership decision |
| Canonical identity and external identity mapping | Owned elsewhere | `baobab-cp` (IAM-3) |
| `iam.*` role names (`iam.identity.suspend`, …) | Implementation detail | Administrative permissions, not capabilities |

## CMS (`baobab-cms`, audited at `1d74258`)

CMS is Payload (ADR-0011), so the provider would be `baobab-cms.payload`.
Its API surface is Payload's generated REST and GraphQL routes over the
collections, plus health and OIDC endpoints.

| Finding | Class | Evidence |
|---|---|---|
| Structured content management (pages, product content, digital estates, markets) | **Candidate family, needs review** (`content`) | `src/collections/*.ts`, tenant enforcement in `src/baobab/tenancy` |
| Content resolution (specificity, inheritance, locale fallback, fail-closed ambiguity) | **Candidate family, needs review** (`content`) | `src/baobab/content-resolution/resolver.ts`, `resolver.test.ts`; used by `src/collections/Pages.ts` |
| Media assets | **Candidate family, needs review** (`content`) | `src/collections/Media.ts`, `src/baobab/media/policy.ts` |
| Publication, localisation, navigation, SEO and taxonomy (§12 table) | Not implemented as distinct services | Collection fields only; revisit when routes exist |
| Outbox, webhooks, audit log, mapping projections | Implementation detail | Integration plumbing (ADR-0018) |

## ERP (`baobab-erp`, audited at `de39818`)

ERP is iDempiere (ADR-ERP-001), so the provider would be
`baobab-erp.idempiere`. Its conformance ledger
(`architecture/conformance.yaml`) is honest about maturity: 1 foundation,
most `partial`, several `planned`.

| Finding | Class | Evidence |
|---|---|---|
| Sell-side order-to-cash: sales order, shipment, customer invoice, payment and allocation (ADR-ERP-016) | **Candidate family, needs review** (`finance`, `fulfilment`) | `modules/order_to_cash/service.py`, tested over HTTP and Postgres against a fake iDempiere REST server. It is event-driven from Trade, not a caller-facing API |
| Projection of Trade commercial facts into native documents (ZB-05) | **Candidate family, needs review** (`finance`, `integration`) | `modules/integration/trade_projection_adapter.py` |
| Master data bootstrap: business partner, product (ADR-ERP-014) | **Candidate family, needs review** | Partial; ownership between CP, Trade and ERP needs deciding first |
| Warehouse provisioning (ADR-ERP-015) | Implementation detail today | Provisioning step, not a consumable service |
| General Ledger, AP, AR, costing, procurement accounting, reporting (§12 table) | Not implemented as Baobab services | iDempiere native only; ADR-ERP-008, -017 and -018 are partial or planned |
| `/context/resolve*`, `/mapping/resolve*`, `/events/inbound` | Implementation detail | Tenant and mapping plumbing (`modules/application/server.py`) |

## Pulse (`baobab-pulse`, audited at `004b748`)

Pulse is a self-declared scaffold, with Haystack behind an
anti-corruption layer (`src/baobab_pulse/infrastructure/haystack`). The
provider would be `baobab-pulse.haystack` or a provider-neutral reference
pipeline; that choice is part of the review.

| Finding | Class | Evidence |
|---|---|---|
| Research missions: create and read (`POST /research-missions`, `GET /research-missions/{id}`) | **Candidate family, needs review** (`intelligence`) | `src/baobab_pulse/api/routers/research_missions.py`, `application/services/research_mission_service.py`; deterministic reference pipeline |
| Evidence search, i.e. semantic retrieval (`POST /evidence/search`) | **Candidate family, needs review** (`intelligence`) | `api/routers/evidence.py`, `application/services/evidence_retrieval_service.py` |
| Signals, observations, risks, opportunities, forecasting | Not implemented as services | Domain model only (`src/baobab_pulse/domain/*`); no routes |
| Haystack pipelines, Qdrant projection | Implementation detail | §13's `haystack.pipeline-node.execute` is the named invalid example |

## Next

1. **Done:** the candidate review (`ea-02b-candidate-review.md`)
   accepted `payment.intent.cancel` and `finance.order-consequence.process`
   into the catalogue, and reserved eight keys pending their Shared
   contracts.
2. Survey Regulations after the `regulations` namespace review.
3. Until the active engines (Trade, ERP, CMS, Pulse, IAM) have
   declarations, Foundation enforcement (G-FCI-1) stays off.
