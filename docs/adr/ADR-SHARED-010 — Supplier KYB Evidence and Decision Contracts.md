# ADR-SHARED-010 — Supplier KYB Evidence and Decision Contracts

| | |
|---|---|
| **Status** | Accepted |
| **Date** | 2026-09-21 |
| **Repository** | `baobab-platform/shared` |
| **Depends on** | ADR-0003; ADR-0005; ADR-0006 |
| **Applies to** | authorised supplier-hosting digital estates, ERP and reporting consumers |

## Context

Gate ZB-05 requires KYB before supplier approval. The v1 supplier-onboarding package
defines applications and qualification but has no portable representation of evidence or
its verification decision. Treating registration numbers as verified KYB would collapse
declaration and verification and permit accidental approval.

## Decision

The hosting estate remains authoritative for pre-approval KYB evidence metadata and
decisions. Add additive v1 events for evidence recording and decision recording.

- Events carry references and hashes, never document bytes, bank account data, secrets,
  sanctions-provider raw responses or internal reviewer notes.
- `declared` is never equivalent to `verified`.
- A failed or incomplete KYB decision cannot produce supplier approval.
- ERP remains authoritative for the operational Supplier/Business Partner after projection.
- Re-delivery is handled through envelope event identifiers and monotonically increasing
  aggregate revisions.

## Consequences

Estates can implement auditable KYB without inventing local event vocabularies. Document
custody, provider selection, retention and deletion remain separate governed decisions.
