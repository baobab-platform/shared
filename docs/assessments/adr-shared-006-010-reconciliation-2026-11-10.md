# ADR-SHARED-006/010 — Authority and event documentation reconciliation

**Baseline:** shared main at 2a2ac16a26e0c217875002f25d7f00e181cf8c5b; 10 November 2026.

## Confirmed drift

1. Three supplier documents claimed canonical Organisation ownership was unassigned, whereas contracts/erp/v1/system-of-record.yaml now assigns it to control-plane under ADR-BCP-018.
2. Supplier README, AsyncAPI and package documentation claimed no message broker existed anywhere in Baobab. RabbitMQ/outbox engineering exists elsewhere, but supplier routing and replay remain unproven.
3. The supplier README enumerated four events while AsyncAPI declares six, including KYB evidence and decision events under ADR-SHARED-010.
4. The published supplierApplicationLifecycle table permits qualification → approved without checking KYB; it is a transition-shape utility, not authorisation or KYB policy. Removing its public API would require separate consumer review.

## Corrections and evidence

- Align descriptions with CP-owned canonical Organisation and keep estate supplier applications distinct from ERP Supplier records.
- Keep v1 canonical_organisation_id nullable for compatibility; when supplied it must be CP-attested.
- Correct the event inventory, qualify broker statements and enforce negative documentation/contract checks.
- Preserve the original September ADR decision with an implementation-era clarification rather than rewriting history.
- Local conformance script: scripts/tests/test_supplier_authority_drift.py; CI runs it alongside other canonical contract gates.

## Unqualified obligations

Runtime KYB approval cannot be certified from a schema or TypeScript lifecycle helper. The hosting estate must independently check current KYB, reviewer and legal-actor authority and preserve replay-safe, revocable approval. No live supplier producer/consumer route, ERP Business Partner projection, legal status, protected deployment or consumer compatibility is asserted by this source PR.
