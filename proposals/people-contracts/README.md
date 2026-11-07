# Baobab People — Shared contract obligation (proposal)

**Status: PROPOSED / NON-CANONICAL — 2026-11-07.** Sponsor: baobab-platform/baobab-erp, ADR-ERP-023. Review authority: Shared, with CP, IAM, Finance, Payments, Documents, Regulations and privacy/statutory specialists.

This is the required **contract obligation declaration**, not a published contract, capability catalogue entry, domain/namespace reservation, runtime entitlement or release approval. Proposed keys in `obligations.yaml` are discussion labels only. Until an accepted Shared ADR and versioned schemas land, all People support remains **unregistered and unavailable** to CP capability resolution. Never add a provider's proposed keys to `support`.

## Required review sequence

1. Agree the workforce/attendance/payroll capability granularity and namespace after reviewing existing `organisation`, `contract`, `tax`, `finance`, `payment`, `documents` and IAM semantics; avoid making all HR features one overpowered capability.
2. Accept a Shared People ADR and publish versioned, closed request/response/error contracts, immutable lifecycle and event schemas, compatible scope registry and capability definitions. Register only accepted names through `contracts/capability/v1/namespace-registry.yaml`, `domain.schema.json` and the sorted catalogue using their existing validation tools.
3. Include exact employer/tenant and employment-version authority, legal and effective dates, provenance, zero-leakage responses, state transitions, correction/reversal lineage, idempotency, rule pack identity and producer ownership.
4. Register only independently evidenced ERP/provider support in `baobab-erp/.baobab/capability-provider.yaml`; use CP grants, bindings and activation only after independent EA-09 and ZA qualification.
5. Maintain a qualified external payroll bureau as a possible implementation, not a second source of truth for the same pay-run/version.

### Non-goals

No live HR records, statutory rates, filings, employee-facing endpoints, OSGi bundle, bank disbursement or iDempiere runtime activation is authorised here. Neither Shared contract approval nor a synthetic unit test is statutory or legal approval.

This proposal follows [ADR-SHARED-017](../../docs/adr/ADR-SHARED-017%20%E2%80%94%20Canonical%20Capability%20Catalogue%2C%20Provider%20Declaration%2C%20Engine%20Registry%20and%20Runtime%20Capability%20Convergence.md) and [ADR-SHARED-041](../../docs/adr/ADR-SHARED-041%20%E2%80%94%20Baobab%20Platform%20Engineering%20Philosophy%20and%20African%20Enterprise%20Product%20Excellence.md).
