# Baobab supplier-onboarding contracts v1

This package defines the estate-owned supplier intake and qualification
domain: applications, decisions, qualification status changes, and
capability verification outcomes. It generalizes the concrete contract
`baobab-platform/zuribeans` has already proved in production code (ADR-0006,
`supplier_organisations` / `supplier_status_events` / `supplier_capabilities`)
so any digital estate hosting a supplier-facing intake can build against a
stable shape instead of reinventing it.

## Contract surfaces

- `asyncapi.yaml` carries the four events this domain currently defines:
  application submitted, application decided, qualification updated, and
  capability verified.
- JSON Schemas define the payloads and shared domain types
  (`domain.schema.json`).
- `system-of-record.yaml` declares ownership, direction, consistency and
  conflict policy for this domain's own concepts — it does not amend
  `contracts/erp/v1/system-of-record.yaml`.

All events use `contracts/events/v1/envelope.schema.json`. No message
broker exists yet anywhere in this ecosystem to actually carry them —
same position `contracts/erp/v1` is already in — so this contract exists
for producers and future consumers to build against ahead of one existing,
not because one does.

## What this contract deliberately does not do

- **Does not mint a canonical Organisation ID.** `canonical_organisation_id`
  is reserved and nullable on every payload. `contracts/erp/v1/system-of-record.yaml`
  keeps the platform "Organisation" concept's `canonical_owner` explicitly
  `unassigned` (CI-enforced there) until a real contract is approved; this
  domain must never imply that decision has been made.
- **Does not redefine or replace the ERP-owned "Supplier" concept.**
  `contracts/erp/v1/system-of-record.yaml` already declares `Supplier`:
  `canonical_owner: erp`, "Business Partner vendor role". A `Supplier
  Application` here is a pre-approval, estate-owned applicant — a distinct
  concept the applicant becomes an input to, never the same record.
- **Does not model product proposals or market eligibility.** Those are
  larger, separate concepts (see the wider supplier-onboarding directive
  this contract is Phase 1 of) intentionally left for a later contract once
  a real product-submission workflow exists to validate the shape against.
- **Does not choose a message broker, storage engine, or document
  management system.** Those are each hosting estate's own decision, same
  as `contracts/erp/v1` makes no such choice for ERP.
