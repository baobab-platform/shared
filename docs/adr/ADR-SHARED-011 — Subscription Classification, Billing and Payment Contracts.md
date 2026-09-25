# ADR-SHARED-011 — Subscription Classification, Billing and Payment Contracts

| | |
|---|---|
| **Status** | Accepted |
| **Date** | 2026-09-25 |
| **Repository** | `baobab-platform/shared` |
| **Depends on** | ADR-SHARED-007; ADR-SHARED-008; baobab-cp ADR-BCP-005, ADR-BCP-017, ADR-BCP-018 (gate ORG-11); baobab-subscriptions ADR-SUB-0001; baobab-payments ADR-PAY-0001 |
| **Applies to** | `baobab-cp`, `baobab-subscriptions`, `baobab-payments` and their consumers |

## Context

ADR-BCP-018 gate ORG-11 requires that INTERNAL eligibility, established by the Control Plane from governed CorporateRelationship and PlatformRelationship evidence, reaches a ProductSubscription and its billing without changing CapabilityGrant semantics. Two things were missing:

- **Classification.** `contracts/product/v1` ProductSubscription carried no subscription classification, so nothing could say durably that a subscription is INTERNAL, or why.
- **Billing and payment contracts.** ADR-SUB-0001 and ADR-PAY-0001 adopt dedicated billing and payment engines. Neither had a canonical contract, and no capability domain existed for subscription billing.

## Decision

### 1. ProductSubscription classification (`contracts/product/v1`, additive)

- **`subscriptionType`** is the ADR-BCP-005 vocabulary: COMMERCIAL, INTERNAL, TRIAL, PARTNER, MANUAL and MIGRATION. It is identical to `admission/v1` `subscriptionType`, and a validator keeps the two equal. There is no INTERNAL_GROUP.
- **`classificationSource`**: ADMISSION_DECISION, RECLASSIFICATION, MIGRATION or MANUAL_GOVERNANCE.
- **ProductSubscription `classification`** holds the current classification: type, source, reference and time. For an ADMISSION_DECISION source, the reference is the `admission_decision_id`.
- **`SubscriptionClassificationRecord`** is one immutable, audited classification or reclassification.
  - An INTERNAL record always carries the server-evaluated `InternalEligibilityEvidence` (`admission/v1`): the qualifying platform relationships, which lead to the corporate relationships.
  - Records reference authoritative facts rather than copying the corporate graph.
  - Reclassification (INTERNAL → COMMERCIAL, COMMERCIAL → PARTNER, …) is a new record on the same ProductSubscription. It never replaces the tenant, organisation or subscription identity.
- **`ClassificationExplanation`** is the read model that answers "why is this subscription INTERNAL?". It gives the current record, the history, eligibility re-evaluated now (so drift is visible), and the billing policy.
- **`billing-policy.yaml`** is the billing policy per subscription type. INTERNAL is zero monetary charge and no billing, yet metering, entitlement control, audit, readiness and isolation all remain on, and payment execution is never invoked (ADR-BCP-017 §11).
- **`subscription.classified`** is a new event. It carries identifiers and state only.

### 1a. Drift and authorization

- **Drift rule.** `organisation/v1` gains the drift rule `INTERNAL_CLASSIFICATION_BASIS_NOT_IN_FORCE` (resource type `PRODUCT_SUBSCRIPTION`). It fires when an INTERNAL subscription's recorded eligibility basis is no longer in force, for example after a divestiture. The remediation is governed review or reclassification, never silent deletion of the tenant or subscription.
- **New scopes** in `authorization/v1/scope-registry.yaml`, both privileged:
  - `subscription:read` to read classifications and explanations;
  - `subscription:classify` to classify or reclassify.

### 2. Billing contracts (`contracts/subscriptions/v1`)

- **The billing projection.** Billing sees a ProductSubscription only through a projection. The projection references the product subscription and its classification provenance, and never redefines them.
- **Tenant context comes from the Control Plane.** Tenant, legal entity and PlatformAccount are asserted by the Control Plane over workload identity.
- **Lifecycle (aligned with ADR-SUB-0003, 2026-09-25).**
  - `billing_state` follows ADR-SUB-0003 §5: `PENDING_CONFIGURATION`, `PROVISIONING`, `ACTIVE`, `SUSPENDED`, `TERMINATING` and `TERMINATED`.
  - Operational trouble is a separate `operational_condition`.
  - Requests, commands, projections and lifecycle events carry the Control Plane's `authoritative_revision`, so an out-of-order older revision never regresses state.
- **Readiness is honest (ADR-SUB-0006 §57-58).**
  - Readiness is separate facts plus machine-readable blockers.
  - INTERNAL is `READY` without any provider or payment dependency.
  - A billing-required projection served by a simulated provider is always `BLOCKED`, carries `BILLING_PROVIDER_NOT_CONFIGURED`, reports `provider_ready: false`, and is never `ACTIVE`.
- **Usage records** are metered for every type. INTERNAL usage is metered but not billable.
- **Events:**
  - `billing-subscription.created`, `.suspended`, `.resumed` and `.terminated`. `.terminated` replaces the original `.cancelled`, following ADR-SUB-0003 §10. The package had no consumers when it changed;
  - `usage.recorded`.

  They are distinct from the Control Plane's `product.subscription.*` aggregate.

### 3. Payment contracts (`contracts/payments/v1`)

- **Objects:** PaymentIntent, Payment, Refund and the payment context (tenant, legal entity, market, currency, source engine and reference, correlation).
- **Provider references** are opaque, and HyperSwitch objects are never the contract.
- **Sandbox results are marked.** Every result from a sandbox provider is `simulated: true`, and every payment event carries `simulated`, so a sandbox payment is always distinguishable from real settlement.

### 4. Capability domain `billing` (architecture review)

The capability namespace gains a top-level domain, `billing`: subscription billing, usage metering and credits. This follows ADR-SHARED-008's registration precedent.

It is deliberately distinct from:

- `finance`: invoicing, receivables and the ledger, owned by ERP;
- `payment`: payment execution.

Each engine package publishes its capability and provider descriptors (`capabilities.json`) as ordinary `capability/v1` records:

- `baobab-subscriptions` registers `billing.subscription.manage` and `billing.usage.record`;
- `baobab-payments` registers `payment.intent.create`, `payment.payment.authorize`, `payment.payment.capture` and `payment.refund.create`.

The Control Plane registers and binds these through its normal capability and provider mechanisms. Nothing is special-cased by engine name.

### 5. Engine workload scopes

Callers reach the engines with workload tokens whose audience is the engine itself (`baobab-subscriptions` or `baobab-payments`). A token issued for one engine, or for the Control Plane, is refused everywhere else. `authorization/v1/scope-registry.yaml` registers the scopes, all workload-only:

| Engine | Scope | Grants |
|---|---|---|
| `baobab-subscriptions` | `billing:manage` | Ensure, suspend and cancel billing projections |
| `baobab-subscriptions` | `billing:read` | Read billing projections |
| `baobab-subscriptions` | `usage:record` | Meter usage |
| `baobab-payments` | `payment:execute` | Create, confirm, capture and cancel payment intents |
| `baobab-payments` | `payment:refund` | Refund a payment |
| `baobab-payments` | `payment:read` | Read payment intents, payments and refunds |

Static bearer secrets are not a supported production mechanism.

## Consequences

- **Explainable INTERNAL.** The Control Plane can answer why a subscription is INTERNAL from Shared-defined records, without asking the billing engine.
- **Unchanged authority.** Billing and payment engines consume classification; they never originate it. CapabilityGrant semantics are unchanged: INTERNAL still grants through ProductSubscription → ProductVersion → CapabilityComposition → CapabilityGrant.
- **Additive only.** Every change here is additive to existing packages. `scripts/validate-commercial-contracts.py` enforces the rules above.
