> **Accepted subset (8 November 2026):** ADR-SHARED-045 and `contracts/people/v1` now govern four separately catalogued People capability signatures and CP-issued provider selection. All other proposed names and obligations here remain **NON-CANONICAL** pending follow-up review. Acceptance does not activate providers, payroll or payments.

# Baobab People — Shared contract obligation (proposal)

**Status: PROPOSED / NON-CANONICAL — 2026-11-07.** Sponsor: baobab-platform/baobab-erp, ADR-ERP-023. Review authority: Shared, with CP, IAM, Finance, Payments, Documents, Regulations and privacy/statutory specialists.

This is the required **contract obligation declaration**, not a published contract, capability catalogue entry, domain/namespace reservation, runtime entitlement or release approval. Proposed keys in `obligations.yaml` are discussion labels only. Until an accepted Shared ADR and versioned schemas land, all People support remains **unregistered and unavailable** to CP capability resolution. Never add a provider's proposed keys to `support`.

## Required review sequence

1. Agree the workforce/attendance/payroll capability granularity and namespace after reviewing existing `organisation`, `contract`, `tax`, `finance`, `payment`, `documents` and IAM semantics; avoid making all HR features one overpowered capability.
2. Accept a Shared People ADR and publish versioned, closed request/response/error contracts, immutable lifecycle and event schemas, compatible scope registry and capability definitions. Register only accepted names through `contracts/capability/v1/namespace-registry.yaml`, `domain.schema.json` and the sorted catalogue using their existing validation tools.
3. Include exact employer/tenant and employment-version authority, legal and effective dates, provenance, zero-leakage responses, state transitions, correction/reversal lineage, idempotency, rule pack identity and producer ownership.
4. Register only independently evidenced ERP/provider support in `baobab-erp/.baobab/capability-provider.yaml`; use CP grants, bindings and activation only after independent EA-09 and ZA qualification.
5. Treat **tenant choice of existing or new workforce, attendance, leave, payroll, filing and document providers as first-class**, not a temporary payroll-bureau contingency. A tenant must not be required to license, migrate to, or activate native Baobab People to consume independent Baobab capabilities. Each chosen provider is independently qualified for its requested operation; no claimed compatibility from a proposal.
6. Require CP-governed, explicit provider selection and binding **per tenant, legal employer, capability, jurisdiction and effective window**, with current IAM/mandate checks. No global default, automatic replacement, covert failover, sibling-tenant inheritance or two authoritative writers for the same payroll run/version.
7. Design provider adapters and reversible portability before provider activation: source-of-record matrix, provenance, exact external references, consent/lawful purpose, restricted exports/imports, effective-dated cutovers, reconciliation and immutable correction/replay. Missing/invalid provider qualification must fail closed for the requested operation, not suspend unrelated tenant capabilities.

## Tenant freedom and interoperability (proposed review obligation)

**Bring Your Own Provider (BYOP) is a permanent supported choice**, including tenant-operated systems and contracted third-party HR/payroll providers. Tenants may use native People for some functions, other providers for others, or remain entirely external for workforce/payroll. Provider selection must never imply platform-account creation or privileged employee-data access. The adapter boundary, not a vendor-native API, exposes Shared-approved semantics where the tenant chooses integration.

A selected external provider can remain the authoritative source of HR or payroll facts; Baobab may store only lawful, minimum necessary projections, signed receipts or reconciled journal-intent references. For tenant-managed, offline or legacy providers without APIs, controlled encrypted file exchange or manual attested evidence may be designed and qualified; an adapter cannot invent source-system success. External provider approval and disbursement do not automatically become Baobab approvals or Payments executions. Conversely, a journal entering native iDempiere is still subject to its own ERP posting veto.

Qualification tests must cover native-only, external-only, mixed per-capability, migration-out and parallel-run scenarios; wrong employer/market, revoked grant, duplicate/replayed webhook, stale provider binding, out-of-scope source record, missing consent/purpose, failed cutover, conflicting results and provider outage must not produce cross-tenant disclosure or duplicate effects. Provider changes and historical payroll records require explicit retained ownership and reversible exit evidence.

### Non-goals

No live HR records, statutory rates, filings, employee-facing endpoints, OSGi bundle, bank disbursement or iDempiere runtime activation is authorised here. Neither Shared contract approval nor a synthetic unit test is statutory or legal approval.

This proposal follows [ADR-SHARED-017](../../docs/adr/ADR-SHARED-017%20%E2%80%94%20Canonical%20Capability%20Catalogue%2C%20Provider%20Declaration%2C%20Engine%20Registry%20and%20Runtime%20Capability%20Convergence.md) and [ADR-SHARED-041](../../docs/adr/ADR-SHARED-041%20%E2%80%94%20Baobab%20Platform%20Engineering%20Philosophy%20and%20African%20Enterprise%20Product%20Excellence.md).
