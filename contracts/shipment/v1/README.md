# Baobab Shipment contracts v1

Gate ZB-01 initial publication (ADR-SHARED-008 SS5). Defines a physical
movement of goods: mode, tracking events, planned/in-transit/customs-hold/
delivered/exception lifecycle. Governed under the `logistics` domain in
`contracts/capability/v1/namespace-registry.yaml`. Event types use the
`trade` bounded context (ADR-SHARED-008 SS3's own worked example:
`shipment.created` -> `com.baobab-platform.trade.shipment.created.v1`).

## Contract surfaces

- `asyncapi.yaml` carries the three events this domain currently defines:
  shipment created, status changed, delivered.
- `domain.schema.json` defines the `Shipment` resource, its tracking events
  and identifiers/enumerations.
- `events.schema.json` defines the event payloads.

All events use `contracts/events/v1/envelope.schema.json`. No message broker
exists yet anywhere in this ecosystem to actually carry them -- same
position `contracts/erp/v1` and `contracts/product/v1` are already in -- so
this contract exists for producers and future consumers to build against
ahead of one existing, not because one does.

## What this contract deliberately does not do

- **Does not model customs declarations or clearance detail.** Those
  belong to the `customs` domain (ADR-SHARED-008), a separate concept for
  a later gate; `CUSTOMS_HOLD` here is a shipment-level status only.
- **Does not model carrier booking, rating or cost.** `carrier_reference`
  is deliberately opaque.
- **Does not choose a message broker or storage engine.** Each hosting
  estate's own decision, same as `contracts/erp/v1` and `contracts/product/v1`.
