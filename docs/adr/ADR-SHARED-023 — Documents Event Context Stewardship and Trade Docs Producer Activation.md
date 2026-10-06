# ADR-SHARED-023 — Documents Event Context Stewardship and Trade Docs Producer Activation

**Status:** Accepted — Normative Event Governance  
**Date:** 2026-10-05  
**Repository:** baobab-platform/shared  
**Decision ID:** ADR-SHARED-023  
**Decision Type:** Event Context Stewardship / Producer Authority / Contract Activation  
**Implements:** RTD-07 from ADR-SHARED-019  
**Depends On:** ADR-SHARED-018, ADR-SHARED-019, ADR-SHARED-020, ADR-SHARED-021, ADR-SHARED-022  
**Engine Authority:** baobab-platform/baobab-trade-docs  
**Event Context:** documents

---

## 1. Decision

The Shared event context:

~~~text
documents
~~~

SHALL be stewarded by:

~~~text
baobab-trade-docs
~~~

for canonical trade-document and documentary-evidence facts governed by the accepted Trade Docs architecture.

RTD-07 assigns canonical producer authority to baobab-trade-docs for:

1. the reconciled TradeDocument v2 fact family; and
2. the RTD-06 document-side regulatory-evidence-offered fact.

RTD-07 does **not** activate Regulations-owned events.

RTD-07 does **not** activate the legacy TradeDocument v1 issued/verified/rejected family.

---

## 2. Why This Decision Is Required

Before RTD-07, the platform had:

~~~text
documents context
    status = ACTIVE
    stewards = []

TradeDocument v2 contracts
    lifecycle = PROPOSED

RTD-06 document evidence event
    DEFINED_NOT_ACTIVATED
~~~

That was deliberate while the canonical Trade Docs model was still being reconciled.

RTD-04 completed the TradeDocument v2 semantic correction.

RTD-05 established portable cross-engine identity.

RTD-06 established the Regulations ↔ Trade Docs exchange.

Therefore the platform now has sufficient contract clarity to assign producer authority.

---

## 3. Authority Model

| Concern | Authority after RTD-07 |
|---|---|
| documents event-context stewardship | baobab-trade-docs |
| TradeDocument v2 fact production | baobab-trade-docs |
| DocumentVersion fact production | baobab-trade-docs |
| ContentArtifact fact production | baobab-trade-docs |
| DocumentRelationship fact production | baobab-trade-docs |
| Documentary verification/validity fact production | baobab-trade-docs |
| Regulatory evidence offered fact | baobab-trade-docs |
| Regulatory requirement meaning | baobab-regulations |
| Requirement satisfaction | baobab-regulations |
| RegulatoryDecision | baobab-regulations |
| Operational enforcement | owning Trade/TMS/ERP engine |
| sovereign issuance/release | competent external authority |

---

## 4. Activated TradeDocument v2 Events

The following become ACTIVE:

~~~text
com.baobab-platform.documents.content-artifact.registered.v2

com.baobab-platform.documents.document-relationship.created.v2

com.baobab-platform.documents.document-version.created.v2

com.baobab-platform.documents.document-version.issued.v2

com.baobab-platform.documents.document-version.validity-changed.v2

com.baobab-platform.documents.document-version.verification-changed.v2

com.baobab-platform.documents.trade-document.created.v2

com.baobab-platform.documents.trade-document.issued.v2

com.baobab-platform.documents.trade-document.superseded.v2

com.baobab-platform.documents.trade-document.voided.v2
~~~

For every type:

~~~text
producer = baobab-trade-docs
lifecycle = ACTIVE
~~~

---

## 5. Activated RTD-06 Document-Side Event

RTD-07 also activates:

~~~text
com.baobab-platform.documents.regulatory-evidence.offered.v1
~~~

with:

~~~text
producer = baobab-trade-docs
context  = documents
lifecycle = ACTIVE
~~~

Its payload remains governed by ADR-SHARED-022 / RTD-06.

Its AsyncAPI publication surface is:

~~~text
contracts/regulatory-document-evidence/v1/asyncapi.yaml
~~~

---

## 6. Why Regulatory Evidence Offered Belongs to documents

The fact means:

> Trade Docs recorded that specific pinned DocumentVersions were offered against a pinned Regulations requirement.

The event describes documentary workflow state.

It does not describe a Regulations decision.

Therefore:

~~~text
documents.regulatory-evidence.offered
    → documents context

regulations.requirement-satisfaction.evaluated
    → regulations context
~~~

---

## 7. Event Direction

~~~text
Trade Docs
   │
   ├── DocumentVersion verification changed
   ├── DocumentVersion validity changed
   ├── TradeDocument issued
   └── Regulatory evidence offered
             │
             ▼
      authorised consumers
             │
     ┌───────┼────────┐
     ▼       ▼        ▼
 Regulations Pulse   Trade/TMS
~~~

Consumers may react to the event.

They do not acquire producer authority.

---

## 8. Producer Authority Is Singular Per Event Type

For every activated event in RTD-07:

~~~text
producer = baobab-trade-docs
~~~

The event registry is the canonical producer-authority index.

A consumer, adapter, Digital Estate or broker SHALL NOT republish the same canonical event type as if it were the authoritative producer.

Derived consumer events require their own event type and authority.

---

## 9. Stewardship Is Semantic, Not Deployment Ownership

The documents context steward owns event semantics.

It does not imply ownership of:

- every storage provider;
- every broker;
- every Digital Estate;
- every document issuer;
- every external Customs authority;
- every fact contained inside a document.

---

## 10. ACTIVE Contract Does Not Mean Runtime Exists

RTD-07 activates **contract authority**.

It does not assert that baobab-trade-docs currently has:

- production application code;
- a transactional outbox;
- a deployed broker;
- a relay worker;
- production subscriptions;
- production operational monitoring.

Therefore:

~~~text
event lifecycle ACTIVE
    !=
runtime implementation complete

producer authority
    !=
deployed publisher
~~~

This distinction is normative.

---

## 11. Legacy v1 Events Remain PROPOSED

The pre-Trade-Docs v1 event family remains:

~~~text
com.baobab-platform.documents.trade-document.issued.v1
com.baobab-platform.documents.trade-document.verified.v1
com.baobab-platform.documents.trade-document.rejected.v1
~~~

with:

~~~text
lifecycle = PROPOSED
producer absent
~~~

RTD-07 SHALL NOT assign baobab-trade-docs as producer for them.

---

## 12. Why v1 Is Not Activated

The v1 model predates ADR-TDOC-0001/0002 and contains semantic defects.

In particular:

~~~text
VERIFIED
REJECTED
~~~

were treated too closely to TradeDocument lifecycle.

The corrected architecture requires:

~~~text
DocumentLifecycleState
    !=
VerificationState

TradeDocument
    !=
DocumentVersion

TradeDocument
    !=
ContentArtifact
~~~

Activating v1 would grant producer authority to a known-wrong contract.

---

## 13. v2 Is the Production Contract Target

New Trade Docs event implementations SHALL target:

~~~text
contracts/trade-document/v2
~~~

not:

~~~text
contracts/trade-document/v1
~~~

The v1 package remains compatibility history.

It may later be formally retired through a separate lifecycle decision.

---

## 14. Verification Event Semantics

This event:

~~~text
documents.document-version.verification-changed.v2
~~~

means a Trade Docs verification projection changed.

It does not mean:

~~~text
regulatory requirement satisfied
shipment compliant
document legally sufficient for every purpose
~~~

Those conclusions belong to Regulations or another owning domain.

---

## 15. Validity Event Semantics

This event:

~~~text
documents.document-version.validity-changed.v2
~~~

reports documentary temporal-validity state.

A transition to EXPIRED or REVOKED can be a reassessment trigger.

It does not itself create a Regulations decision.

---

## 16. Reassessment Choreography

~~~text
Trade Docs
DocumentVersion validity changes
          │
          ▼
documents.document-version.validity-changed.v2
          │
          ▼
Regulations consumer
          │
          ▼
identify linked pinned requirement
          │
          ▼
explicit reassessment command
          │
          ▼
Regulations evaluates
~~~

This preserves:

~~~text
fact event
    !=
command
    !=
decision
~~~

---

## 17. Evidence Offered Semantics

The evidence-offered event SHALL preserve:

- pinned RegulatoryDecision reference;
- pinned Regulations requirement reference;
- pinned DocumentVersion references;
- tenant;
- occurrence time.

It SHALL NOT contain:

- requirement satisfaction outcome;
- compliance boolean;
- shipment disposition;
- Regulations decision result.

---

## 18. Cross-Engine Reference Requirement

Cross-engine references inside the evidence-offered event SHALL use ADR-SHARED-021.

DocumentVersion references SHALL be:

~~~text
owner_engine_id = baobab-trade-docs
object_type = DOCUMENT_VERSION
reference_mode = IDENTITY_PINNED
~~~

Regulations requirement/decision references SHALL remain owned by baobab-regulations.

---

## 19. Tenant Consistency

For tenant-scoped document events:

~~~text
CloudEvent.tenantid
    =
payload tenant
    =
every nested tenant-scoped CrossEngineObjectReference.tenant_id
~~~

unless a future explicitly governed cross-tenant event contract says otherwise.

RTD-07 introduces no such cross-tenant exception.

---

## 20. Logical Event Source

The logical event producer source SHALL identify baobab-trade-docs rather than a deployment host.

Canonical examples use:

~~~text
urn:baobab-platform:service:baobab-trade-docs
~~~

A deployment hostname, pod name, region or engine_instance_id is not the durable event source identity.

---

## 21. Event Identity and Retry

The canonical deduplication identity remains:

~~~text
(source, id)
~~~

Retry SHALL preserve the same event occurrence ID.

A relay retry is not a new domain event.

---

## 22. Transactional Publication Requirement

When runtime publication is implemented, canonical Trade Docs state changes that require events SHOULD use the transactional-outbox model.

Conceptually:

~~~text
BEGIN

persist Trade Docs state

persist outbox event

COMMIT
~~~

Then:

~~~text
outbox relay
    ↓
broker/transport
~~~

This follows platform event architecture and avoids:

~~~text
database committed
event silently lost
~~~

or:

~~~text
event published
database transaction rolled back
~~~

---

## 23. Consumer Delivery Semantics

Consumers SHALL assume at-least-once delivery unless a stronger, specifically governed transport contract exists.

Consumers must be idempotent.

Broker-level exactly-once marketing claims do not replace domain deduplication.

---

## 24. No Direct Regulations Activation

RTD-07 SHALL NOT register:

~~~text
com.baobab-platform.regulations.document-requirements.determined.v1

com.baobab-platform.regulations.requirement-satisfaction.evaluated.v1
~~~

Those remain RTD-08 responsibilities.

---

## 25. No Customs Stewardship Migration

RTD-07 activates only:

~~~text
documents
~~~

It does not transfer:

~~~text
customs
~~~

event-context stewardship.

Customs declaration, authority-response, transit and clearance event migration requires separate reconciliation because legacy Customs ownership remains more complex.

---

## 26. Pulse Relationship

Pulse may later consume ACTIVE documents events for intelligence.

Example:

~~~text
Document validity changed
        │
        ▼
Pulse observes
        │
        ▼
risk / opportunity / trend
~~~

Pulse does not become a documents producer.

RTD-09 governs Pulse consumer/projection alignment.

---

## 27. Digital Estate Relationship

A Digital Estate may:

- display document state;
- subscribe to document facts;
- call Trade Docs APIs;
- present notifications.

It SHALL NOT mint canonical documents events under the same event types.

---

## 28. External Issuer Relationship

An external authority may issue a certificate.

Trade Docs may then record:

~~~text
TradeDocument
DocumentVersion
verification
artifact/provenance
~~~

and publish Baobab document facts.

This does not make Trade Docs the external legal issuer.

---

## 29. Event Registry State After RTD-07

The intended registry split is:

| Event family | Lifecycle | Producer |
|---|---|---|
| TradeDocument v2 | ACTIVE | baobab-trade-docs |
| DocumentVersion v2 | ACTIVE | baobab-trade-docs |
| ContentArtifact v2 | ACTIVE | baobab-trade-docs |
| DocumentRelationship v2 | ACTIVE | baobab-trade-docs |
| regulatory-evidence.offered.v1 | ACTIVE | baobab-trade-docs |
| legacy TradeDocument v1 | PROPOSED | none |
| Regulations RTD-06 events | not registered | none until RTD-08 |

---

## 30. Context Registry State After RTD-07

~~~text
documents
  status: ACTIVE
  stewards:
    - baobab-trade-docs
~~~

Authority includes:

- ADR-SHARED-019;
- ADR-SHARED-020;
- ADR-SHARED-023;
- ADR-TDOC-0001;
- ADR-TDOC-0002.

---

## 31. Contract Evolution

Breaking changes to active event semantics require a new major event version.

Active v2 event meaning SHALL NOT be silently rewritten.

Compatible optional fields may follow normal Shared compatibility policy.

---

## 32. Event Retirement

A future retirement of legacy v1 or active v2 types must be explicit.

Historical events are not rewritten.

Lifecycle transition may conceptually be:

~~~text
ACTIVE
  ↓
DEPRECATED
  ↓
RETIRED
~~~

where migration has been governed.

---

## 33. Runtime Readiness Still Outstanding

RTD-07 intentionally leaves application/runtime work such as:

- Trade Docs service runtime;
- persistence;
- outbox;
- relay;
- broker binding;
- observability;
- consumer subscriptions;
- replay tooling;
- DLQ handling;
- production conformance evidence.

Those are implementation/readiness tasks, not reasons to leave producer authority ambiguous.

---

## 34. Required CI Enforcement

Shared CI SHALL prove:

1. documents context is ACTIVE;
2. baobab-trade-docs is a documents steward;
3. ADR-SHARED-023 is recorded as authority;
4. all reconciled v2 event types are ACTIVE;
5. every active v2 type names baobab-trade-docs as producer;
6. legacy v1 types remain PROPOSED;
7. legacy v1 types remain producerless;
8. regulatory-evidence.offered is ACTIVE;
9. its producer is baobab-trade-docs;
10. its AsyncAPI is present;
11. its envelope/payload example validates;
12. all nested tenant references match event tenant;
13. Regulations RTD-06 events remain unregistered;
14. event-registry / AsyncAPI one-to-one validation still passes.

---

## 35. Rejected Alternatives

### A. Activate both v1 and v2

Rejected.

It would grant production authority to known-incompatible semantics.

### B. Delete v1 immediately

Rejected.

RTD-07 is an activation decision, not an uncontrolled compatibility deletion.

### C. Leave documents with no steward

Rejected.

The semantic owner is now known.

### D. Make Shared the producer

Rejected.

Shared distributes contracts; it is not a document runtime.

### E. Let each Digital Estate publish documents events

Rejected.

That would create multiple competing canonical producers.

### F. Let Regulations publish document events

Rejected.

Regulations owns regulatory meaning, not TradeDocument state.

### G. Activate Regulations events in the same step

Rejected.

RTD-08 exists as a separate governance gate.

### H. Move customs stewardship now

Rejected.

Customs requires a distinct migration analysis.

---

## 36. Invariants

~~~text
INV-DOC-EVT-001
baobab-trade-docs is the canonical steward of the documents event context.

INV-DOC-EVT-002
Every active RTD-07 documents event has exactly one producer.

INV-DOC-EVT-003
That producer is baobab-trade-docs.

INV-DOC-EVT-004
TradeDocument v2 is the implementation target.

INV-DOC-EVT-005
Legacy TradeDocument v1 remains PROPOSED.

INV-DOC-EVT-006
Legacy v1 remains producerless.

INV-DOC-EVT-007
Verification state is not document lifecycle.

INV-DOC-EVT-008
Document verification is not regulatory sufficiency.

INV-DOC-EVT-009
Validity change is a fact, not a Regulations decision.

INV-DOC-EVT-010
Evidence offered is a fact, not an assessment command.

INV-DOC-EVT-011
Evidence offered is not evidence accepted.

INV-DOC-EVT-012
Document events do not mutate Regulations-owned requirements.

INV-DOC-EVT-013
Documents producer authority does not transfer sovereign issuer authority.

INV-DOC-EVT-014
Event ACTIVE does not assert deployed runtime implementation.

INV-DOC-EVT-015
Logical producer identity is independent of deployment instance.

INV-DOC-EVT-016
Nested tenant-scoped references match event tenant.

INV-DOC-EVT-017
Cross-engine identity uses ADR-SHARED-021.

INV-DOC-EVT-018
Historical pinned references are not replaced with current state.

INV-DOC-EVT-019
A consumer cannot republish the same canonical type as producer.

INV-DOC-EVT-020
RTD-07 does not activate regulations events.

INV-DOC-EVT-021
RTD-07 does not migrate customs stewardship.

INV-DOC-EVT-022
Shared is contract authority, not runtime producer.

INV-DOC-EVT-023
Digital Estates are consumers, not canonical documents producers.

INV-DOC-EVT-024
Pulse may consume document facts but is not in the producer path.

INV-DOC-EVT-025
Runtime publication should preserve transactional state/event intent consistency.
~~~

---

## 37. Consequences

### Positive

- documents now has a clear canonical steward;
- active event types have unambiguous producer authority;
- consumers can build against stable event ownership;
- legacy bad semantics remain quarantined;
- Regulations reassessment can consume documentary changes without authority leakage;
- RTD-09 can add Pulse consumers safely;
- later conformance testing has explicit producer expectations.

### Costs

- baobab-trade-docs must eventually implement the active contracts correctly;
- runtime readiness work remains;
- v1 compatibility history remains temporarily present;
- separate RTD-08 and Customs migration work is still required.

---

## 38. Final Decision

The documents event architecture is now:

~~~text
baobab-trade-docs
      │
      │ canonical document facts
      ▼
documents event context
      │
      ├── TradeDocument v2
      ├── DocumentVersion v2
      ├── ContentArtifact v2
      ├── DocumentRelationship v2
      └── RegulatoryEvidenceOffered v1
             │
             ▼
      authorised consumers
~~~

while:

~~~text
legacy v1
    remains PROPOSED

Regulations events
    remain RTD-08

Customs migration
    remains separate
~~~

> **RTD-07 resolves producer ambiguity without collapsing domain authority: Trade Docs produces documentary facts; Regulations still decides regulatory meaning.**
