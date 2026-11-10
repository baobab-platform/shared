# Baobab supplier-onboarding contracts v1

This package defines the estate-owned supplier intake and qualification
domain: applications, decisions, qualification status changes, and
capability verification outcomes, KYB evidence metadata and KYB decisions. It generalizes the concrete contract
`baobab-platform/zuribeans` has already proved in production code (ADR-0006,
`supplier_organisations` / `supplier_status_events` / `supplier_capabilities`)
so any digital estate hosting a supplier-facing intake can build against a
stable shape instead of reinventing it.

## Contract surfaces

- `asyncapi.yaml` carries the six events this domain currently defines:
  application submitted, application decided, qualification updated, and
  capability verified.
- JSON Schemas define the payloads and shared domain types
  (`domain.schema.json`), including additive KYB evidence and decision events.
- KYB contracts carry evidence references and hashes only; document bytes, bank
  account data, raw provider responses and internal reviewer notes are forbidden.
- `system-of-record.yaml` declares ownership, direction, consistency and
  conflict policy for this domain's own concepts — it does not amend
  `contracts/erp/v1/system-of-record.yaml`.

All events use `contracts/events/v1/envelope.schema.json`. Infrastructure, Trade and ERP now have RabbitMQ/outbox work, but the existence
of a broker is not evidence of activated supplier-onboarding event routes.
A hosting estate must independently qualify producer custody, authorised
consumers, durable delivery, replay and negative paths.

## What this contract deliberately does not do

- **Does not mint a canonical Organisation ID.** `canonical_organisation_id`
  is reserved and nullable on every payload. `contracts/erp/v1/system-of-record.yaml`
  assigns the platform "Organisation" concept's `canonical_owner` to
  `control-plane` (ADR-BCP-018). This v1 package retains a nullable
  `canonical_organisation_id` for compatibility. If populated it must be
  CP-attested; the hosting estate must not mint or infer it.
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
