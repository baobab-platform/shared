# Regulatory document exchange contracts v1

RTD-06 defines the executable boundary between Baobab Regulations and Baobab
Trade Docs.

It does **not** merge their domains.

## Authority

```text
Regulations
  requirement meaning
  applicability
  legal sufficiency
  RegulatoryDecision

Trade Docs
  TradeDocument / DocumentVersion
  documentary verification
  documentary temporal-validity facts
  content-artifact references
  documentary workflow

Trade / TMS / ERP
  operational enforcement / business state

External authorities
  sovereign/legal effect
```

## Choreography

```text
Trade / TMS
    │ business facts
    ▼
Regulations
    │
    ├── RegulatoryDecision
    └── RegulatoryDocumentRequirementSet
             │
             ▼
         Trade Docs
   obtain / associate / version /
    verify documentary evidence
             │
             ├── evidence-offered fact
             │
             ▼
         Regulations
   documentary-evidence assessment
             │
             ▼
 RequirementSatisfaction result
             │
             ▼
 refreshed RegulatoryDecision?
```

## Contract surfaces

- `domain.schema.json`
  - Regulations-owned requirement projections
  - Trade Docs-owned documentary fact bundles
  - evidence-assessment command/result shapes
  - pinned RTD-05 cross-engine references
- `regulations.openapi.yaml`
  - resolve exact requirement projection
  - assess documentary evidence
- `trade-docs.openapi.yaml`
  - resolve exact documentary fact bundles for pinned DocumentVersions
- `events.schema.json`
  - planned cross-engine event payloads
- `event-surfaces.yaml`
  - event names, target producers and future activation gate

## Hard separation

```text
DocumentRequirement != TradeDocument

DocumentVersion verification != RequirementSatisfaction

evidence offered != evidence accepted

RequirementSatisfaction != shipment release

event != command
```

The evidence-assessment operation is a command/API call. The
`documents.regulatory-evidence.offered` event is only a fact that evidence was
offered; it must never be interpreted as a request to evaluate.

## Historical pinning

Requirements, decisions and evidence used for consequential assessment are
pinned through `contracts/cross-engine-reference/v1`.

A mutable/current reference is not sufficient historical proof.

DocumentVersion uses `IDENTITY_PINNED` because the version ID itself denotes
an immutable semantic state.

## Trusted context

All synchronous operations redeem a Control Plane `context_id`. The owner
must verify the caller and ensure every nested tenant-scoped reference matches
that trusted context tenant.

Callers cannot select legal time or knowledge time in the evidence-assessment
request. Those remain Regulations-owned semantics derived from the pinned
RegulatoryDecision/Requirement context.

## Planned events are not activated

RTD-06 deliberately does **not** add an AsyncAPI file or event-registry entries.

That is intentional:

- RTD-07 activates the `documents` producer/steward path.
- RTD-08 activates the `regulations` context/platform event contracts.

Until those steps land, the event names in `event-surfaces.yaml` are defined
contract candidates, not publishable platform events.

## Existing document events

Regulations may later consume already-defined document facts such as:

- `document-version.verification-changed.v2`
- `document-version.validity-changed.v2`

as reassessment triggers once producer activation exists.

Those events are facts, not reassessment commands. Regulations decides whether
a linked requirement must be reassessed.

## Deferred

RTD-06 does not define:

- DocumentDossier;
- CustomsCase;
- CustomsDeclaration/submission workflow;
- Customs authority-response contracts;
- detailed document semantic-data extraction;
- document generation;
- event producer activation;
- the `regulations` capability namespace decision.

Those remain later TDOC/RTD architecture.
