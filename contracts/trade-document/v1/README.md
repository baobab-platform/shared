# Baobab TradeDocument contracts v1

> **Compatibility notice — superseded before activation:** This v1 package is the
> pre-Trade-Docs scaffold published during Gate ZB-01. It is preserved unchanged
> at the schema/event-shape level because accepted Thamani ADR-THA-0018 forbids
> silently mutating it into the richer TDOC model. New implementations must use
> `contracts/trade-document/v2` (ADR-SHARED-020 / RTD-04). The v1 events remain
> PROPOSED and have no authorised producer.

Gate ZB-01 initial publication (ADR-SHARED-008 SS5). Defines trade,
inspection and proof-of-delivery document metadata: type, issuing party,
issue/verify/reject lifecycle. Governed under the `documents` domain in
`contracts/capability/v1/namespace-registry.yaml`.

## Contract surfaces

- `asyncapi.yaml` carries the three events this domain currently defines:
  trade document issued, verified, rejected.
- `domain.schema.json` defines the `TradeDocument` resource and its
  identifiers/enumerations.
- `events.schema.json` defines the event payloads.

All events use `contracts/events/v1/envelope.schema.json`. No message broker
exists yet anywhere in this ecosystem to actually carry them -- same
position `contracts/erp/v1` and `contracts/product/v1` are already in -- so
this contract exists for producers and future consumers to build against
ahead of one existing, not because one does.

## What this contract deliberately does not do

- **Does not choose or own a document management system.**
  `storage_reference` is an opaque URI; where and how the artifact itself
  is stored is each hosting estate's own decision.
- **Does not model tax-authority filings.** Those belong to the `tax`
  domain (ADR-SHARED-008), a separate concept for a later gate.
- **Does not choose a message broker.** Each hosting estate's own
  decision, same as `contracts/erp/v1` and `contracts/product/v1`.
