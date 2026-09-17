# Baobab buyer-organisation contracts v1

Gate ZB-01 initial publication (ADR-SHARED-008 SS5). Defines the buyer-side
counterparty a tenant trades with: registration, status lifecycle. Governed
under the `customer` domain in `contracts/capability/v1/namespace-registry.yaml`.

## Contract surfaces

- `asyncapi.yaml` carries the two events this domain currently defines:
  buyer organisation registered and status changed.
- `domain.schema.json` defines the `BuyerOrganisation` resource and its
  identifiers/enumerations.
- `events.schema.json` defines the event payloads.

All events use `contracts/events/v1/envelope.schema.json`. No message broker
exists yet anywhere in this ecosystem to actually carry them -- same position
`contracts/erp/v1` and `contracts/product/v1` are already in -- so this
contract exists for producers and future consumers to build against ahead of
one existing, not because one does.

## What this contract deliberately does not do

- **Does not mint a canonical Organisation ID.** `canonical_organisation_id`
  is reserved and nullable on every payload, mirroring
  `contracts/supplier-onboarding/v1`'s identical boundary: no canonical
  Organisation authority exists yet.
- **Does not redefine or replace an engine-owned Customer/Business Partner
  record.** A BuyerOrganisation here is the platform-level counterparty
  identity; engine-specific customer records remain each engine's own
  concern.
- **Does not model credit terms, payment methods or commercial agreements.**
  Those are separate, larger concepts intentionally left for a later gate.
- **Does not choose a message broker or storage engine.** Each hosting
  estate's own decision, same as `contracts/erp/v1` and `contracts/product/v1`.
