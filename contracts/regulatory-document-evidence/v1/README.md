# Regulatory document evidence events v1

This package is the RTD-07 asynchronous publication surface for the
document-side half of ADR-SHARED-022.

## Producer authority

```text
context  = documents
producer = baobab-trade-docs
event    = com.baobab-platform.documents.regulatory-evidence.offered.v1
status   = ACTIVE
```

ADR-SHARED-023 grants the producer authority.

## Meaning

The event means:

> Trade Docs recorded that these exact pinned DocumentVersions were offered
> against this pinned Regulations requirement.

It does **not** mean:

- Regulations has assessed them;
- the requirement is satisfied;
- the shipment is compliant;
- the document is legally sufficient;
- an operational hold/release should occur.

Those conclusions remain outside Trade Docs authority.

## Payload authority

The event payload schema remains in:

```text
contracts/regulatory-document-exchange/v1/events.schema.json
```

This package adds the AsyncAPI publication surface only. It does not duplicate
the RTD-06 domain schema.

## Command/event separation

A consumer that needs a Regulations assessment invokes the explicit RTD-06
assessment command/API.

```text
EvidenceOffered event
    !=
AssessDocumentaryEvidence command
```

## Subject

The CloudEvent subject identifies a primary Trade Docs DocumentVersion. The
payload remains authoritative for the complete set of offered
`document_version_references`.

## Runtime caveat

ACTIVE in the Shared event registry grants canonical producer authority. It
does not assert that a message broker, outbox relay or Trade Docs application
runtime has already been deployed.
