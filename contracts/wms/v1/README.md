# Baobab WMS / 3PL — canonical DRAFT capability tranche

**Authority:** Shared ADR-SHARED-017 and baobab-erp accepted ADR-ERP-024.
**Status:** DRAFT/EXPERIMENTAL vocabulary only; no WMS executor selected, no provider support, no CP grant/binding or regulated operating approval.

Two provider-neutral first-tranche capabilities are indexed in the canonical catalogue:

- `inventory.custody.read`: physical custody observations for a CP-authorised warehouse, inventory owner and operator; distinct from `inventory.availability.query`, Trade reservations and ERP valuation.
- `inventory.warehouse-operation.manage`: an idempotent operational observation record (receive/move/count/dispatch). A command is **not** a financial inventory posting, transport acceptance, change of title, or payment instruction.

**Authority rule:** Caller-provided `warehouse_ref`, `inventory_owner_ref` and other business identifiers are desired targets/filters only. The gateway/worker MUST resolve tenant, legal actor, service customer, warehouse operator, provider, current assignment, delegated warehouse scope and revocation using trusted IAM/CP context. Never infer that a depositor owns the operator or that group affiliation grants access. Different inventory owners and service customers may share an operator and site without sharing read access.

**Qualification:** Native versus BYOP selection, legal/service contract, effective-dated market packs, warehouse/provider binding, consent, receipt signatures, audit custody, no-overwrite/idempotent replay, post-commit loss readback, owner isolation, accounting reconciliation, health freshness and WMS-00…WMS-12 independent evidence are prerequisites for provider activation. Neither catalogue sync nor a DRAFT registration can activate a provider.
