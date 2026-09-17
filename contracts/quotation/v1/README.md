# Baobab Quotation contracts v1

Gate ZB-01 initial publication (ADR-SHARED-008 SS5). Defines a supplier's
priced response to an RFQ (or a direct offer): line items, validity window,
submit/accept/reject lifecycle. Governed under the `commercial` domain in
`contracts/capability/v1/namespace-registry.yaml`.

## Contract surfaces

- `asyncapi.yaml` carries the three events this domain currently defines:
  quotation submitted, accepted, rejected.
- `domain.schema.json` defines the `Quotation` resource, its line items and
  identifiers/enumerations.
- `events.schema.json` defines the event payloads.

All events use `contracts/events/v1/envelope.schema.json`. No message broker
exists yet anywhere in this ecosystem to actually carry them -- same
position `contracts/erp/v1` and `contracts/product/v1` are already in -- so
this contract exists for producers and future consumers to build against
ahead of one existing, not because one does.

## What this contract deliberately does not do

- **Does not cross-reference a canonical supplier identity.**
  `supplier_reference` is deliberately opaque: `contracts/supplier-onboarding/v1`'s
  `canonical_organisation_id` is still unassigned, so no canonical supplier
  ID exists to reference.
- **Does not model contract negotiation, counter-offers or amendment
  history.** Those are separate, larger concepts for a later gate.
- **Does not choose a message broker or storage engine.** Each hosting
  estate's own decision, same as `contracts/erp/v1` and `contracts/product/v1`.
