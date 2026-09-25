# Subscription Billing Contracts (`subscriptions/v1`)

**Governing ADRs:** ADR-SHARED-011 (this repository); ADR-SUB-0001, ADR-SUB-0003, ADR-SUB-0006 and ADR-SUB-0016 (`baobab-platform/baobab-subscriptions`); ADR-BCP-005, ADR-BCP-017 and ADR-BCP-018 gate ORG-11 (`baobab-platform/baobab-cp`)
**Contract authority:** `baobab-platform/shared`
**Runtime authority:** `baobab-platform/baobab-subscriptions`

The Baobab Billing API. `baobab-subscriptions` bills a Control Plane ProductSubscription only through a **billing projection**. The projection references the subscription and its classification provenance, and never redefines them:

```text
CP ProductSubscription + classification ──► BillingProjection ──► baobab-subscriptions ──► BillingProvider (temporary; Kill Bill later)
```

## Files

| File | Contents |
|---|---|
| `domain.schema.json` | Identifiers (`bsub_`, `usage_`), the billing lifecycle, operational condition, readiness status and blocker codes, provider kinds, usage metric keys |
| `billing.schema.json` | `EnsureBillingProjectionRequest`, `BillingProjection`, `BillingProjectionCommand`, `RecordUsageRequest`, `UsageRecord` |
| `events.schema.json` and `asyncapi.yaml` | `billing-subscription.created`, `.suspended`, `.resumed` and `.terminated`; `usage.recorded` |
| `capabilities.json` | The engine's capability registration: `billing.subscription.manage` and `billing.usage.record`, provided by the simulated `baobab-subscriptions.temporary-billing` |

## Rules the schemas enforce

- **The Control Plane is the authority.**
  - Tenant, legal entity, PlatformAccount and classification come from the Control Plane over workload identity.
  - An ensure request cannot carry eligibility evidence. The engine records the classification; it never evaluates it.
- **The policy comes from Shared.** A projection applies the `product/v1/billing-policy.yaml` entry for its type. INTERNAL means zero charge, no billing, metering on, and payments never invoked.
- **Lifecycle (ADR-SUB-0003).**
  - `billing_state` is the business lifecycle: `PENDING_CONFIGURATION` → `PROVISIONING` → `ACTIVE` ⇄ `SUSPENDED` → `TERMINATING` → `TERMINATED`. `TERMINATED` is final.
  - Infrastructure trouble is `operational_condition` (`HEALTHY`, `DEGRADED`, `RECONCILIATION_REQUIRED`, `RETRYING` or `BLOCKED`). It is never a billing state.
  - Every request and command carries the Control Plane's `authoritative_revision`, so an older one never regresses a newer projection.
- **Readiness is honest (ADR-SUB-0006).**
  - Readiness is reported as separate facts (classification, projection, metering, billing configuration, provider, payment path) plus machine-readable blockers, never as one boolean.
  - INTERNAL is `READY` with no provider or payment dependency.
  - Money-requiring billing on a simulated provider is never `ACTIVE` and never `READY`. It is `BLOCKED`, carries `BILLING_PROVIDER_NOT_CONFIGURED`, and reports `provider_ready: false`.
  - Suspension and termination appear as blockers.
- **The temporary provider is always `simulated`.**
- **Usage is metered for every type**, and `billable` is false where the policy charges nothing.
- **Billing events are their own aggregate**, distinct from `product.subscription.*`. They carry identifiers and state only.

Every mutation takes an `Idempotency-Key`. `scripts/validate-commercial-contracts.py` validates this package.
