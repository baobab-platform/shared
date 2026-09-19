# Baobab RFQ contracts v1

Gate ZB-01 initial publication (ADR-SHARED-008 SS5). Defines a buyer-
initiated Request for Quotation: line items, response deadline, publish/
close lifecycle. Governed under the `commercial` domain in
`contracts/capability/v1/namespace-registry.yaml`.

## Contract surfaces

- `asyncapi.yaml` carries the two events this domain currently defines:
  RFQ published and RFQ closed.
- `domain.schema.json` defines the `RFQ` resource, its line items and
  identifiers/enumerations.
- `events.schema.json` defines the event payloads.

All events use `contracts/events/v1/envelope.schema.json`. No message broker
exists yet anywhere in this ecosystem to actually carry them -- same
position `contracts/erp/v1` and `contracts/product/v1` are already in -- so
this contract exists for producers and future consumers to build against
ahead of one existing, not because one does.

## What this contract deliberately does not do

- **Does not model supplier invitation or response routing.** Which
  suppliers see an RFQ and how they are notified is a separate, larger
  concept for a later gate.
- **Does not model the quotation response itself.** See
  `contracts/quotation/v1` -- a Quotation may reference an `rfq_id` but is
  a distinct resource with its own lifecycle.
- **Does not choose a message broker or storage engine.** Each hosting
  estate's own decision, same as `contracts/erp/v1` and `contracts/product/v1`.
