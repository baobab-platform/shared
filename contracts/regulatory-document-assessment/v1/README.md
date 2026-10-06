# Regulatory document assessment events v1

This package is the RTD-08 asynchronous publication surface for the
Regulations-owned half of ADR-SHARED-022.

## Producer authority

```text
context  = regulations
producer = baobab-regulations
status   = ACTIVE
```

ADR-SHARED-024 grants the producer authority.

## Events

```text
com.baobab-platform.regulations.document-requirements.determined.v1

com.baobab-platform.regulations.requirement-satisfaction.evaluated.v1
```

The first states the documentary requirements Regulations determined for a
pinned RegulatoryDecision context.

The second states the Regulations-owned result of evaluating documentary
evidence against a pinned requirement.

## What these events do not mean

They do not:

- create or mutate a TradeDocument;
- mark a DocumentVersion verified;
- submit a Customs declaration;
- release or hold a shipment;
- create accounting/tax postings;
- transfer sovereign authority from an external regulator.

## Payload authority

The payload schemas remain in:

```text
contracts/regulatory-document-exchange/v1/events.schema.json
```

This package adds the Regulations-owned AsyncAPI publication surface only.

## Event / command separation

The synchronous assessment operation remains the command:

```text
POST /v1/documentary-evidence/assessments
```

The event:

```text
regulations.requirement-satisfaction.evaluated
```

is a committed fact emitted after Regulations completes the assessment.

## Namespace relationship

RTD-08 also resolves G-REG-NS by registering the `regulations` capability
domain. This does not automatically catalogue or activate any
`regulations.*` capability key.

The existing `tax` and `customs` capability domains are not migrated by
this step.

## Runtime caveat

ACTIVE in the Shared event registry grants canonical producer authority. It
does not assert that a production Regulations outbox, relay or broker binding
has already been deployed.
