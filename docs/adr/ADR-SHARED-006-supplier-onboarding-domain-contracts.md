# ADR-0006: Supplier-Onboarding Domain Contracts

| | |
|---|---|
| **Status** | Accepted |
| **Date** | 2026-09-07 |
| **Owner** | Chief Software Engineer, Baobab-Platform Group Africa |
| **Repository** | `baobab-platform/shared` |
| **Depends on** | ADR-0001; ADR-0003; ADR-0005 |
| **Applies to** | `thamani`, `zuribeans` (reference only — not modified by this ADR), `baobab-cp`, `baobab-erp`, authorised digital estates |

## 1. Context

`baobab-platform/thamani` needs a supplier registration, vetting and cross-border
sourcing capability. Before designing one, this program repeated the
"who owns this, who is authoritative" discovery `baobab-platform/zuribeans`
already ran for its own supplier-side amendment
(`docs/adr/0006-supplier-registration-data-ownership.md` in that
repository) and reached the identical conclusion:

- `baobab-platform/baobab-cp`'s canonical model has no Organisation type yet, and
  its Mapping/MappingScope tables do not yet match their own accepted
  schema.
- `baobab-platform/baobab-erp` has no Business Partner adapter — no code exists to
  provision a supplier as an ERP vendor.
- No message broker exists anywhere in this ecosystem to publish
  `supplier.*` events to.
- `contracts/erp/v1/system-of-record.yaml` already declares `Supplier`
  (`canonical_owner: erp`) and `Organisation` (`canonical_owner:
  unassigned`, CI-enforced) — a new domain must reference both without
  redefining either.

`baobab-platform/zuribeans` had already built a real, tested vertical slice against
this exact gap: its own Postgres schema, a full lifecycle transition table,
declared-vs-verified capability and certification records, and a
`canonical_organisation_id` seam left null pending a canonical Organisation
owner. Rather than let a second estate re-derive and duplicate that shape
from scratch, this ADR extracts the *mechanism* it proved (not its specific
business states) into a shared package, and defines the equivalent
cross-engine event contracts other estates' ERP/reporting consumers can
eventually build against.

## 2. Decision

### 2.1 Package ownership

`packages/supplier-domain` (`@baobab-platform/supplier-domain`) is the canonical,
reusable supplier-onboarding domain mechanism: a generic lifecycle
state-machine factory, and Zod shapes for a supplier organisation, its
contacts, capabilities, certifications, and status-change audit trail. It
generalizes `baobab-platform/zuribeans` ADR-0006's proven shape but does not modify
that repository, which remains free to keep its own independent
implementation, adopt this package, or do neither — this ADR creates an
option, not an obligation.

The package defines shapes and transition rules only. It is not
persistence, not identity, and never mints a canonical Organisation
identifier (see §2.3 of ADR-0005 and the "Organisation" entry in
`contracts/erp/v1/system-of-record.yaml`, whose `canonical_owner:
unassigned` this ADR does not change).

### 2.2 Contract ownership

`contracts/supplier-onboarding/v1` is the canonical cross-engine
supplier-onboarding event package: `supplier-application-submitted`,
`supplier-application-decided`, `supplier-qualification-updated`, and
`supplier-capability-verified`, all built on
`contracts/events/v1/envelope.schema.json`. It carries its own
`system-of-record.yaml`, scoped to this domain's own concepts (`Supplier
Application`, `Supplier Capability`, `Supplier Certification`) — it does
not add rows to, or otherwise amend, `contracts/erp/v1/system-of-record.yaml`.

### 2.3 What remains explicitly deferred

Consistent with `baobab-platform/zuribeans` ADR-0006's own restraint, this ADR does
not:

- Mint a canonical Organisation identifier or assign that concept an
  owner — still `unassigned`, still CI-enforced in
  `contracts/erp/v1/system-of-record.yaml`.
- Stand up an ERP Business Partner adapter, a message broker, or document
  storage for supplier certifications — none exist anywhere in this
  ecosystem yet, and building one against nothing on the other end is the
  "heavyweight infrastructure not justified by current workload" this
  platform's engineering constraints already warn against.
- Define product-proposal or market-eligibility contracts. Those are
  larger, separate concepts left for a later ADR once a real
  product-submission workflow exists to validate the shape against.

## 3. Consequences

- `baobab-platform/thamani` can adopt `@baobab-platform/supplier-domain` and
  `contracts/supplier-onboarding/v1` once this package is released,
  instead of re-deriving ADR-0006's discovery and design from scratch.
- `baobab-platform/zuribeans` is unaffected; nothing in this ADR requires it to
  change.
- A future ADR must still resolve canonical Organisation ownership before
  any estate's `canonical_organisation_id` can be populated, and must still
  design ERP Business Partner provisioning before a supplier application
  can become an operational vendor record.
