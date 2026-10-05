# Baobab TradeDocument contracts v2

RTD-04 reconciles the original pre-activation `trade-document/v1` scaffold with
ADR-SHARED-019 and the accepted Trade Docs domain decisions ADR-TDOC-0001 and
ADR-TDOC-0002.

## Why v2 exists

The v1 package pre-dates the dedicated `baobab-trade-docs` engine. It makes
several assumptions that the later architecture explicitly rejects:

- it says Control Plane mints `trade_document_id`;
- it treats `VERIFIED` and `REJECTED` as document lifecycle states;
- it has no `DocumentVersion`;
- it stores one `storage_reference` on the TradeDocument root;
- it uses a closed document-type enum;
- it models one-off shipment/procurement foreign keys instead of typed subject
  associations;
- it has no content-artifact or document-relationship model.

The v1 schemas are preserved because accepted Thamani ADR-THA-0018 explicitly
forbids silently mutating that contract into the richer TDOC model. Its events
remain PROPOSED and must not be implemented by new consumers.

## v2 authority model

```text
Trade Docs
  TradeDocument identity
  DocumentVersion
  content-artifact association
  document relationships
  document lifecycle
  documentary verification projection
  temporal-validity projection
  provenance

Regulations
  document / permit / evidence requirements
  legal applicability
  regulatory sufficiency
  RegulatoryDecision

Control Plane
  tenant/platform context
  canonical organisations
  capability/provider resolution

External issuers / Customs
  external legal authority

Trade / TMS / ERP
  underlying business facts and operational enforcement
```

## Core separations

```text
TradeDocument != File
TradeDocument != DocumentVersion
DocumentVersion != ContentArtifact
Document Lifecycle != Verification State
Verification != Regulatory Sufficiency
Document Number != Canonical Document ID
TradeDocument ID != Control Plane CanonicalEntity ID
```

## Contract surfaces

- `domain.schema.json` defines TradeDocument identity, immutable versions,
  content artifacts, business identifiers, issuer claims, typed subject
  associations, document-to-document relationships, and separate mutable
  verification/temporal-validity projections.
- `events.schema.json` defines minimal fact payloads.
- `asyncapi.yaml` defines the canonical `documents.*.v2` fact events. ADR-SHARED-023 / RTD-07 activates `baobab-trade-docs` as producer for these reconciled v2 types.
- `examples/` contains both resource fixtures and event envelopes validated
  by Shared CI.

## Deliberate deferrals

RTD-04 does not define:

- the generic cross-engine canonical object-reference contract (RTD-05);
- Regulations ↔ Trade Docs requirement/evidence APIs and events (RTD-06);
- DocumentDossier;
- CustomsCase / CustomsDeclaration workflow contracts;
- authority adapters/responses;
- signatures/trust policy beyond opaque signature references;
- transferable-record control/endorsement;
- the full governed DocumentTypeRegistry.

Those need their own TDOC decisions and/or later RTD work.

## Extensibility

`document_type` is now a governed code pattern rather than a closed enum.
A type registry may later govern available values without requiring the base
TradeDocument schema to be replaced whenever a new document class is added.

## Storage

`storage_reference` belongs to `ContentArtifact`, not TradeDocument.
One immutable DocumentVersion can therefore have several representations
(JSON, XML, PDF, source scan, signed envelope) with independent digests and
storage locations.

## Cross-engine references

The v2 subject-association fields remain intentionally bounded and opaque.
They are not the RTD-05 `CrossEngineObjectReference`.

RTD-05 is now defined by `contracts/cross-engine-reference/v1`
(ADR-SHARED-021). New APIs/events that need portable cross-engine object
identity must use that contract. This RTD-05 change does not silently mutate
the already-published v2 subject-association wire shape; a later compatible
TradeDocument contract evolution may embed the Shared reference where needed.

## RTD-07 producer activation

ADR-SHARED-023 assigns:

```text
context  = documents
steward  = baobab-trade-docs
producer = baobab-trade-docs
```

for the reconciled TradeDocument v2 fact events in this package.

The legacy v1 events remain PROPOSED and producerless because their
`verified/rejected` semantics conflate verification/workflow outcomes with
document lifecycle.

ACTIVE contract status grants canonical producer authority. It does not claim
that a Trade Docs runtime, transactional outbox or broker transport has already
been deployed.
