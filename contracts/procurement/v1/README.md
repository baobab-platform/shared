# Baobab procurement contracts v1

Gate ZB-01 initial publication (ADR-SHARED-008 SS5). Defines a tenant's
internal request to purchase: line items, approvals, request/approve/
reject/convert lifecycle. Governed under the `procurement` domain in
`contracts/capability/v1/namespace-registry.yaml`.

## Contract surfaces

- `asyncapi.yaml` carries the four events this domain currently defines:
  procurement request created, approved, rejected, converted.
- `domain.schema.json` defines the `ProcurementRequest` resource, its line
  items, approvals and identifiers/enumerations.
- `events.schema.json` defines the event payloads.

All events use `contracts/events/v1/envelope.schema.json`. No message broker
exists yet anywhere in this ecosystem to actually carry them -- same
position `contracts/erp/v1` and `contracts/product/v1` are already in -- so
this contract exists for producers and future consumers to build against
ahead of one existing, not because one does.

## What this contract deliberately does not do

- **Does not model the downstream commitment a converted request becomes.**
  `converted_reference` is deliberately opaque; a purchase order or
  contract's own canonical shape is a separate, larger concept for a later
  gate.
- **Does not model multi-level or delegated approval workflow.**
  `approvals` is a flat append-only list; workflow routing is each engine's
  own concern.
- **Does not choose a message broker or storage engine.** Each hosting
  estate's own decision, same as `contracts/erp/v1` and `contracts/product/v1`.
