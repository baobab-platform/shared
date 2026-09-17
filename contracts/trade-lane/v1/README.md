# Baobab TradeLane contracts v1

Gate ZB-01 initial publication (ADR-SHARED-008 SS5). Defines a governed
origin/destination market relationship a tenant may trade along, per
ADR-BCP-011's cross-market trading model. Governed under the `market`
domain in `contracts/capability/v1/namespace-registry.yaml`.

## Contract surfaces

- `asyncapi.yaml` carries the two events this domain currently defines:
  trade lane activated and suspended.
- `domain.schema.json` defines the `TradeLane` resource and its
  identifiers/enumerations.
- `events.schema.json` defines the event payloads.

All events use `contracts/events/v1/envelope.schema.json`. No message broker
exists yet anywhere in this ecosystem to actually carry them -- same
position `contracts/erp/v1` and `contracts/product/v1` are already in -- so
this contract exists for producers and future consumers to build against
ahead of one existing, not because one does.

## What this contract deliberately does not do

- **Does not mint or validate `market_id`.** Market registration is
  `contracts/control-plane/v1`/`baobab-cp`'s own concern
  (`market.market` per `baobab-cp` migration `000006`); this package only
  references market IDs as opaque strings.
- **Does not model per-market participation flags** (SOURCING,
  PROCUREMENT, SELLING, etc. from ADR-BCP-011) -- those live on the
  market-participation record itself, not on the lane connecting two
  markets. `permitted_capability_keys` is a coarser, lane-level allow-list
  only.
- **Does not choose a message broker or storage engine.** Each hosting
  estate's own decision, same as `contracts/erp/v1` and `contracts/product/v1`.
