# @baobab-platform/supplier-domain

Reusable supplier-onboarding domain mechanism: a lifecycle state machine
factory, and Zod shapes for a supplier organisation, its contacts,
capabilities, certifications, and status-change audit trail.

## Provenance

This package generalizes the concrete supplier-registration vertical slice
`baobab-platform/zuribeans` built and proved out in
[`docs/adr/0006-supplier-registration-data-ownership.md`](https://github.com/baobab-platform/zuribeans/blob/main/docs/adr/0006-supplier-registration-data-ownership.md)
(own Postgres schema, `supplier_organisations` / `supplier_contacts` /
`supplier_capabilities` / `supplier_certifications` / `supplier_status_events`
tables, an explicit lifecycle transition table instead of a boolean, and a
category registry instead of category-specific columns). That ADR's own
"who owns this, who is authoritative" discovery found nothing to defer to —
the same discovery, repeated independently for `baobab-platform/thamani`, reached
the identical conclusion. Rather than let a second estate duplicate that
logic from scratch, the *mechanism* (not Zuribeans' specific business
states) is extracted here so every digital estate that needs supplier
intake can start from a proven shape.

`baobab-platform/zuribeans` has not been changed to consume this package — it has
no obligation to, and this package's existence does not retroactively
require it. It remains the reference implementation this package
generalizes from.

## What this package is not

- **Not persistence.** No database, no ORM, no migrations. Each consuming
  estate owns its own schema and storage, exactly as Zuribeans' ADR-0006
  decided ("a Postgres database owned entirely by this estate... not
  shared with, and never a copy of, any Baobab engine's database").
- **Not identity.** `applicantIdentityRef` is an opaque string join point.
  This package does not decide what authenticates a supplier applicant —
  that is Zuribeans' Medusa customer today, and will be whatever Thamani's
  own account system provides once it exists.
- **Not a canonical Organisation.** `canonicalOrganisationId` is reserved
  and nullable everywhere in this package, and no code here ever populates
  it. `baobab-platform/baobab-cp` does not yet have a canonical Organisation type,
  and `baobab-platform/shared`'s own `contracts/erp/v1/system-of-record.yaml` keeps
  the "Organisation" concept's `canonical_owner` explicitly `unassigned`
  until a real contract is approved — a CI check in that repository fails
  if that invariant is ever silently changed. This package must never
  imply an owner exists ahead of that decision.
- **Not the ERP-owned "Supplier".** `contracts/erp/v1/system-of-record.yaml`
  already declares a `Supplier` concept: `canonical_owner: erp`, "Business
  Partner vendor role" in iDempiere terms, minted only once a real ERP
  adapter exists. The `SupplierOrganisation` in this package is a
  pre-approval, estate-owned applicant — not that entity. An application
  becoming an ERP Supplier is a future provisioning step this package does
  not perform.
- **Not an event bus.** `contracts/supplier-onboarding/v1/` (in this same
  repository) defines the canonical event contracts a supplier-onboarding
  case can eventually publish, but — same as ERP's own event contracts
  today — no message broker exists yet anywhere in this ecosystem to carry
  them. Publishing is each estate's own responsibility once one does.

## Usage

```ts
import {
  supplierApplicationLifecycle,
  supplierOrganisationSchema,
  supplierCapabilityInputSchema,
  defineCategoryRegistry,
} from "@baobab-platform/supplier-domain"

const registry = defineCategoryRegistry([
  { key: "fresh-produce", label: "Fresh Produce" },
  { key: "packaged-foods", label: "Packaged Foods" },
])

supplierApplicationLifecycle.assertTransition("draft", "submitted")
```

A consuming estate whose qualification process genuinely differs from the
proven default can define its own status union and transition table and
call `createLifecycle` directly instead of using
`supplierApplicationLifecycle`.
