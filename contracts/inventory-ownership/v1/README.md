# Baobab InventoryOwnershipRecord contracts v1

Gate ZB-01 initial publication (ADR-SHARED-008 SS5). Defines which legal
entity owns a quantity of stock at a location, distinct from physical
custody -- the ownership dimension ADR-BCP-012's intercompany model needs
(a stock transfer between legal entities of the same tenant can move
custody and ownership independently, e.g. in-transit stock). Governed
under the `inventory` domain in `contracts/capability/v1/namespace-registry.yaml`.

## Contract surfaces

- `asyncapi.yaml` carries the two events this domain currently defines:
  inventory ownership recorded and transferred.
- `domain.schema.json` defines the `InventoryOwnershipRecord` resource and
  its identifiers/enumerations.
- `events.schema.json` defines the event payloads.

All events use `contracts/events/v1/envelope.schema.json`. No message broker
exists yet anywhere in this ecosystem to actually carry them -- same
position `contracts/erp/v1` and `contracts/product/v1` are already in -- so
this contract exists for producers and future consumers to build against
ahead of one existing, not because one does.

## What this contract deliberately does not do

- **Does not mint a canonical Location/Warehouse ID.** `location_reference`
  is deliberately opaque; physical location modelling is each engine's own
  concern (e.g. `baobab-erp`/iDempiere's warehouse model).
- **Does not model physical custody or movement.** That is
  `contracts/shipment/v1`'s concern; this package tracks the ownership
  claim only, which may diverge from physical location during transit.
- **Does not choose a message broker or storage engine.** Each hosting
  estate's own decision, same as `contracts/erp/v1` and `contracts/product/v1`.
