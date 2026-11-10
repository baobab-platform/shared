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
- **Not a canonical Organisation authority.** `canonicalOrganisationId` remains
  nullable for versioned compatibility. Canonical Organisation identity and
  its mappings are owned by CP (ADR-BCP-018); a hosting estate may only
  use CP-attested identity and must never mint or infer it from local registration.
- **Not the ERP-owned "Supplier".** `contracts/erp/v1/system-of-record.yaml`
  already declares a `Supplier` concept: `canonical_owner: erp`, "Business
  Partner vendor role" in iDempiere terms, minted only once a real ERP
  adapter exists. The `SupplierOrganisation` in this package is a
  pre-approval, estate-owned applicant — not that entity. An application
  becoming an ERP Supplier is a future provisioning step this package does
  not perform.
- **Not an event bus or deployment proof.** Six canonical supplier-onboarding
  event types are declared in `contracts/supplier-onboarding/v1/`.
  RabbitMQ infrastructure elsewhere does not prove any supplier route has
  been activated. Each hosting estate owns its producer, outbox, authorised
  delivery, replay and negative-path qualification.
- **Not an approval authority.** The bundled lifecycle table checks transition
  shape, not KYB, a legal-actor mandate, or reviewer authority. In particular,
  `supplierApplicationLifecycle.assertTransition("qualification", "approved")`
  does not prove current KYB is verified. A domain-owned service must check
  authoritative KYB, evidence and permission before any supplier approval
  (ADR-SHARED-007 §§56–58; ADR-SHARED-010).

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
