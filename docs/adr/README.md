# Architecture Decision Records

The register of `baobab-platform/shared`'s architecture decisions and platform specifications, with the status each one declares. It covers `docs/adr` and `docs/architecture/decisions`. `baobab-platform/baobab-cp` keeps its own register in `docs/adr/index.md`.

Each document is classed *Accepted*, *Proposed*, *Superseded* (in whole or in part), *Rejected* or *Historical* (EA Plan v2.0 §28). Accepted documents govern implementation. Proposed ones inform design but do not override an accepted decision. A historical document is the record of its time and governs nothing.

An ADR marked *amended* or *refined* stays authoritative except where the document named in its `Amended By` or `Refined By` header, or its status, decides otherwise.

| Document | Status |
|---|---|
| [ADR-0001: Baobab-Platform Digital Estate & Contract Architecture](ADR-0001-baobab-platform-digital-estate-architecture.md) | Accepted — tenancy portions superseded by ADR-0003 on 2026-09-01 |
| [ADR-0002: Control-plane polyrepo boundaries](ADR-0002-control-plane-polyrepo-boundaries.md) | Accepted |
| [ADR-0003: Separate Tenant, Legal Entity, and Digital Estate Identity](ADR-0003-tenant-legal-entity-and-digital-estate-separation.md) | Accepted |
| [ADR-0004: Canonical Cross-Engine Event, Error, and Idempotency Metadata](ADR-0004-canonical-cross-engine-metadata.md) | Accepted |
| [ADR-0005: ERP System of Record and Boundary Contracts](ADR-0005-erp-system-of-record-and-boundary-contracts.md) | Accepted |
| [ADR-0006: Supplier-Onboarding Domain Contracts](ADR-0006-supplier-onboarding-domain-contracts.md) | Accepted |
| [ADR-SHARED-007 — Canonical Capability Contracts, Composition Registry and Cross-Engine Provider Model](ADR-SHARED-007%20%E2%80%94%20Canonical%20Capability%20Contracts%2C%20Composition%20Registry%20and%20Cross-Engine%20Provider%20Model.md) | Accepted — Normative Platform Contract, amended in part and refined |
| [ADR-SHARED-008 — Gate ZB-01 Capability Domain Registration and Canonical Event-Type Convention Confirmation](ADR-SHARED-008%20%E2%80%94%20Gate%20ZB-01%20Capability%20Domain%20Registration%20and%20Canonical%20Event-Type%20Convention%20Confirmation.md) | Accepted — Normative Contract Amendment |
| [ADR-SHARED-009 — Programme Gate P1 Shared Contract Foundation Completion](ADR-SHARED-009%20%E2%80%94%20Programme%20Gate%20P1%20Shared%20Contract%20Foundation%20Completion.md) | Accepted — Normative Contract Addition (reason codes for provisioning blockers amended by ADR-SHARED-015 §8) |
| [ADR-SHARED-010 — Supplier KYB Evidence and Decision Contracts](ADR-SHARED-010%20%E2%80%94%20Supplier%20KYB%20Evidence%20and%20Decision%20Contracts.md) | Accepted |
| [ADR-SHARED-011 — Subscription Classification, Billing and Payment Contracts](ADR-SHARED-011%20%E2%80%94%20Subscription%20Classification%2C%20Billing%20and%20Payment%20Contracts.md) | Accepted |
| [ADR-SHARED-012 — Topology Identifiers and External System Registry](ADR-SHARED-012%20%E2%80%94%20Topology%20Identifiers%20and%20External%20System%20Registry.md) | Accepted |
| [ADR-SHARED-013 — External References and Canonical Mapping Administration](ADR-SHARED-013%20%E2%80%94%20External%20References%20and%20Canonical%20Mapping%20Administration.md) | Accepted |
| [ADR-SHARED-014 — Mapping Resolution in a Trusted Context](ADR-SHARED-014%20%E2%80%94%20Mapping%20Resolution%20in%20a%20Trusted%20Context.md) | Accepted |
| [ADR-SHARED-015 — Provisioning as Desired-State Convergence](ADR-SHARED-015%20%E2%80%94%20Provisioning%20as%20Desired-State%20Convergence.md) | Accepted |
| [ADR-SHARED-016 — Provider Migration Execution and Engine Migration Tasks](ADR-SHARED-016%20%E2%80%94%20Provider%20Migration%20Execution%20and%20Engine%20Migration%20Tasks.md) | Accepted |
| [ADR-SHARED-017 — Canonical Capability Catalogue, Provider Declaration, Engine Registry and Runtime Capability Convergence](ADR-SHARED-017%20%E2%80%94%20Canonical%20Capability%20Catalogue%2C%20Provider%20Declaration%2C%20Engine%20Registry%20and%20Runtime%20Capability%20Convergence.md) | Accepted — Normative Target Architecture (governing EA-02 decision; Phase 1 implemented, see [EA-02 implementation record](../architecture/ea-02-capability-catalogue.md)) |
| [ADR-SHARED-018 — Canonical Event Context Registry, Event-Type Ownership and Legacy Event Migration](ADR-SHARED-018%20%E2%80%94%20Canonical%20Event%20Context%20Registry%2C%20Event-Type%20Ownership%20and%20Legacy%20Event%20Migration.md) | Accepted — Normative Platform Contract (refines ADR-SHARED-008 §3) |
| [ADR-SHARED-019 — Regulatory Intelligence, Trade Documents and Evidence Cross-Engine Boundary](ADR-SHARED-019%20%E2%80%94%20Regulatory%20Intelligence%2C%20Trade%20Documents%20and%20Evidence%20Cross-Engine%20Boundary.md) | Accepted — Normative Cross-Engine Boundary Architecture |
| [ADR-SHARED-020 — TradeDocument v2 Contract Reconciliation and Pre-Activation Compatibility Boundary](ADR-SHARED-020%20%E2%80%94%20TradeDocument%20v2%20Contract%20Reconciliation%20and%20Pre-Activation%20Compatibility%20Boundary.md) | Accepted — Normative Shared Contract Reconciliation |
| [ADR-SHARED-021 — Canonical Cross-Engine Object Reference, Authority, Scope and Historical Pinning Contract](ADR-SHARED-021%20%E2%80%94%20Canonical%20Cross-Engine%20Object%20Reference%2C%20Authority%2C%20Scope%20and%20Historical%20Pinning%20Contract.md) | Accepted — Normative Shared Contract Architecture |
| [ADR-SHARED-022 — Regulations ↔ Trade Docs Documentary Requirement, Evidence and Reassessment Exchange](ADR-SHARED-022%20%E2%80%94%20Regulations%20%E2%86%94%20Trade%20Docs%20Documentary%20Requirement%2C%20Evidence%20and%20Reassessment%20Exchange.md) | Accepted — Normative Cross-Engine Contract Architecture |
| [ADR-SHARED-023 — Documents Event Context Stewardship and Trade Docs Producer Activation](ADR-SHARED-023%20%E2%80%94%20Documents%20Event%20Context%20Stewardship%20and%20Trade%20Docs%20Producer%20Activation.md) | Accepted — Normative Event Governance |
| [ADR-SHARED-024 — Regulations Capability Namespace, Event Context Stewardship and Producer Activation](ADR-SHARED-024%20%E2%80%94%20Regulations%20Capability%20Namespace%2C%20Event%20Context%20Stewardship%20and%20Producer%20Activation.md) | Accepted — Normative Namespace and Event Governance |
| [ADR-SHARED-025 — Intelligence Capability Namespace Scope and Pulse Consumer Boundary](ADR-SHARED-025%20%E2%80%94%20Intelligence%20Capability%20Namespace%20Scope%20and%20Pulse%20Consumer%20Boundary.md) | Accepted — Normative Namespace and Consumer-Boundary Governance |
| [ADR-SHARED-026 — Cross-Repository Regulations, Trade Docs and Pulse Conformance Architecture](ADR-SHARED-026%20%E2%80%94%20Cross-Repository%20Regulations%2C%20Trade%20Docs%20and%20Pulse%20Conformance%20Architecture.md) | Accepted — Normative Cross-Repository Conformance Architecture |
| [ADR-SHARED-027 — Regulations Capability Census and First Canonical Capability Tranche](ADR-SHARED-027%20%E2%80%94%20Regulations%20Capability%20Census%20and%20First%20Canonical%20Capability%20Tranche.md) | Accepted — Normative Capability Census Decision |
| [Baobab Canonical Mapping Model](Baobab%20Canonical%20Mapping%20Model.md) | Accepted — Canonical Architecture, refined |
| [ADR-0020: Capability-driven Foundation CI](../architecture/decisions/ADR-0020-capability-driven-foundation-ci.md) | Accepted |
| [Baobab Platform Enterprise Architecture Implementation Plan — Revision v2.0](Baobab%20Platform%20Enterprise%20Architecture%20Implementation%20Plan%20%E2%80%94%20Revised%202026-09-30.md) | Accepted — governing EA programme plan (2026-09-30); live status in the [EA dashboard](../architecture/ea-dashboard.md) |
| [Baobab Platform — Enterprise Architecture Production-Readiness Assessment v1](Baobab%20Platform%20%E2%80%94%20Version%201-Enterprise%20Architecture%20Production-Readiness%20Assessment.md) | Historical — findings retained; execution ordering superseded by EA Plan v2.0 |
