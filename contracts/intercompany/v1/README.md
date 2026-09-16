# Baobab IntercompanyTransaction contracts v1

Gate ZB-01 initial publication (ADR-SHARED-008 SS5). Defines a movement
between legal entities of the same tenant: transfer pricing, mirrored
documents, stock transfer, elimination, per ADR-BCP-012's internal-trade
model. Governed under the `internal-trade` domain in
`contracts/capability/v1/namespace-registry.yaml`.

## Contract surfaces

- `asyncapi.yaml` carries the two events this domain currently defines:
  intercompany transaction initiated and settled.
- `domain.schema.json` defines the `IntercompanyTransaction` resource and
  its identifiers/enumerations.
- `events.schema.json` defines the event payloads.

All events use `contracts/events/v1/envelope.schema.json`. No message broker
exists yet anywhere in this ecosystem to actually carry them -- same
position `contracts/erp/v1` and `contracts/product/v1` are already in -- so
this contract exists for producers and future consumers to build against
ahead of one existing, not because one does.

## What this contract deliberately does not do

- **Does not enforce `from_legal_entity_id != to_legal_entity_id`.**
  Runtime validation, not this JSON Schema, is responsible for rejecting a
  self-referential transaction.
- **Does not model elimination accounting or consolidation entries.**
  `ELIMINATED` is a status only; the accounting mechanics belong to
  `baobab-erp`/iDempiere.
- **Does not model in-transit ownership directly.** See
  `contracts/inventory-ownership/v1` for the ownership-record shape a
  `STOCK_TRANSFER` transaction may reference via `reference_document_id`.
- **Does not choose a message broker or storage engine.** Each hosting
  estate's own decision, same as `contracts/erp/v1` and `contracts/product/v1`.
