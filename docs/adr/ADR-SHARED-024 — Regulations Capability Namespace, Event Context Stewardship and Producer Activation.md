# ADR-SHARED-024 — Regulations Capability Namespace, Event Context Stewardship and Producer Activation

**Status:** Accepted — Normative Namespace and Event Governance  
**Date:** 2026-10-06  
**Repository:** baobab-platform/shared  
**Decision ID:** ADR-SHARED-024  
**Decision Type:** Capability Namespace / Event Context Stewardship / Producer Authority / Contract Activation  
**Implements:** RTD-08 from ADR-SHARED-019  
**Resolves:** G-REG-NS  
**Depends On:** ADR-SHARED-007, ADR-SHARED-018, ADR-SHARED-019, ADR-SHARED-021, ADR-SHARED-022, ADR-SHARED-023  
**Engine Authority:** baobab-platform/baobab-regulations  
**Capability Domain:** regulations  
**Event Context:** regulations

---

## 1. Executive Decision

Baobab SHALL register:

~~~text
regulations
~~~

as a canonical capability domain and SHALL activate:

~~~text
regulations
~~~

as an ACTIVE Shared event context stewarded by:

~~~text
baobab-regulations
~~~

RTD-08 activates exactly two already-contracted Regulations-owned RTD-06 facts:

~~~text
com.baobab-platform.regulations.document-requirements.determined.v1

com.baobab-platform.regulations.requirement-satisfaction.evaluated.v1
~~~

with:

~~~text
producer = baobab-regulations
lifecycle = ACTIVE
~~~

RTD-08 does **not** migrate the existing `tax` or `customs` capability domains.

RTD-08 does **not** promote any proposed `regulations.*` capability key into the capability catalogue.

RTD-08 does **not** activate the wider illustrative REG-0024 event vocabulary until canonical Shared payload contracts exist.

---

## 2. Why RTD-08 Exists

Before RTD-08, the platform had a deliberate intermediate state:

~~~text
regulations event context
  status = RESERVED
  target steward = baobab-regulations

G-REG-NS
  decision pending

RTD-06 Regulations events
  DEFINED_NOT_ACTIVATED
~~~

That was correct while the capability namespace and producer boundary were unresolved.

The architecture is now mature enough to remove the ambiguity.

---

## 3. G-REG-NS Resolution

G-REG-NS is resolved **YES**:

> Regulations SHALL be a canonical top-level capability domain.

The registered domain is:

~~~text
regulations
~~~

Its semantic scope includes:

- regulatory context;
- applicability;
- regulatory obligations and requirements;
- regulatory evidence sufficiency;
- regulatory assessment;
- RegulatoryDecision-related capabilities;
- regulatory change and impact capabilities where separately contracted.

---

## 4. What the Regulations Namespace Does Not Mean

Registering:

~~~text
regulations
~~~

does not mean Regulations owns every concern that can be described as regulated.

In particular:

~~~text
regulations != tax execution
regulations != Customs workflow
regulations != accounting
regulations != TradeDocument lifecycle
regulations != shipment execution
~~~

---

## 5. Tax Namespace Decision

The existing:

~~~text
tax
~~~

capability domain remains registered and unchanged.

RTD-08 does not move existing tax registration, calculation, reconciliation or related contracted capability semantics into Regulations.

A future architecture decision may refine the split between:

~~~text
regulatory tax meaning
    vs
tax execution/calculation/accounting
~~~

but RTD-08 does not perform that migration.

---

## 6. Customs Namespace Decision

The existing:

~~~text
customs
~~~

capability domain remains registered and unchanged.

RTD-08 does not decide migration of:

- Customs declaration workflow;
- Customs submission;
- authority-response workflow;
- clearance lifecycle;
- transit execution.

ADR-SHARED-019 remains authoritative:

| Concern | Authority |
|---|---|
| applicable classification / tariff rule / origin rule / prohibition / regulatory requirement | Regulations |
| TradeDocument / DocumentVersion | Trade Docs |
| Customs declaration workflow | Trade Docs, subject to later capability/event migration |
| sovereign Customs assessment/release | external Customs authority |
| operational trade enforcement | owning Trade/TMS engine |

---

## 7. Namespace Registration Is Not Capability Catalogue Promotion

This is a hard invariant:

~~~text
namespace registered
    !=
capability catalogued
    !=
provider support implemented
    !=
capability ACTIVE
    !=
tenant entitled
    !=
provider bound
~~~

The namespace merely permits canonical keys such as:

~~~text
regulations.context.resolve
regulations.decision.evaluate
regulations.change.subscribe
~~~

to enter the normal Shared capability-governance process.

---

## 8. Existing Regulations Provider Declaration

The baobab-regulations repository already carries proposed capability keys.

Those SHALL remain:

~~~text
proposed_key
~~~

until:

1. Shared catalogue semantics are approved;
2. a canonical capability contract exists;
3. provider implementation evidence exists where required;
4. normal Control Plane/provider registration rules are satisfied.

RTD-08 does not skip those gates.

---

## 9. Event Context Activation

The Shared context becomes:

~~~text
regulations
  status: ACTIVE
  stewards:
    - baobab-regulations
  capability_domains:
    - regulations
~~~

ADR-SHARED-024 is the activation authority.

---

## 10. Event Authority Model

| Concern | Authority |
|---|---|
| regulations context stewardship | baobab-regulations |
| document requirements determined | baobab-regulations |
| requirement satisfaction evaluated | baobab-regulations |
| documentary evidence offered | baobab-trade-docs |
| TradeDocument state | baobab-trade-docs |
| operational shipment/order state | owning Trade/TMS engine |
| external legal effect | competent external authority |
| event contract schemas | Shared |

---

## 11. Activated Event — Document Requirements Determined

RTD-08 activates:

~~~text
com.baobab-platform.regulations.document-requirements.determined.v1
~~~

Meaning:

> Regulations has determined a set of documentary/permit/evidence requirements for a pinned RegulatoryDecision context.

The event carries a Regulations-owned requirement-set projection.

---

## 12. Document Requirements Event Is Not a Trade Docs Command

The event means:

~~~text
these requirements were determined
~~~

It does not mean:

~~~text
create document X now
upload certificate Y
submit Customs declaration Z
~~~

Those are workflow commands/capability invocations.

---

## 13. Activated Event — Requirement Satisfaction Evaluated

RTD-08 activates:

~~~text
com.baobab-platform.regulations.requirement-satisfaction.evaluated.v1
~~~

Meaning:

> Regulations has evaluated documentary evidence against a pinned regulatory requirement and committed a requirement-satisfaction result.

---

## 14. Satisfaction Event Is Not Operational Enforcement

The event may say:

~~~text
SATISFIED
UNSATISFIED
INDETERMINATE
NOT_APPLICABLE
REVIEW_REQUIRED
~~~

It SHALL NOT directly:

- release a shipment;
- hold a shipment;
- cancel an order;
- create a tax posting;
- mutate a TradeDocument;
- submit to a regulator.

Operational engines remain Policy Enforcement Points.

---

## 15. Cross-Engine Choreography

~~~text
Trade / TMS
    │
    │ business facts
    ▼
Regulations
    │
    ├── RegulatoryDecision
    └── document requirements
             │
             │ requirements-determined event
             ▼
         Trade Docs
    obtain / associate / verify
             │
             │ evidence-offered event
             ▼
         Regulations
    explicit assessment command
             │
             ▼
 requirement-satisfaction result
             │
             │ satisfaction-evaluated event
             ▼
 authorised consumers / PEPs
~~~

---

## 16. Event Directionality

~~~text
Regulations → Trade Docs
  requirement facts

Trade Docs → Regulations
  documentary facts / evidence offered

Regulations → Trade/TMS/Pulse/Trade Docs
  requirement-satisfaction facts
~~~

Direction does not transfer domain ownership.

---

## 17. Shared AsyncAPI Surface

The Regulations-owned publication surface is:

~~~text
contracts/regulatory-document-assessment/v1/asyncapi.yaml
~~~

The RTD-06 payload authority remains:

~~~text
contracts/regulatory-document-exchange/v1/events.schema.json
~~~

This avoids duplicating payload schemas.

---

## 18. Why Owner-Specific AsyncAPI Packages Are Separate

RTD-06 spans two runtime owners:

~~~text
baobab-trade-docs
baobab-regulations
~~~

A single mixed-owner AsyncAPI publication package would blur producer authority.

Therefore:

~~~text
regulatory-document-evidence/v1
    → Trade Docs producer surface

regulatory-document-assessment/v1
    → Regulations producer surface
~~~

---

## 19. Producer Authority

Every event activated by RTD-08 has exactly one canonical producer:

~~~text
baobab-regulations
~~~

A Digital Estate, Trade Docs, Trade, Pulse, a broker relay or an adapter SHALL NOT republish the same canonical event type as if it were its authoritative producer.

---

## 20. Event Source Identity

Canonical examples use:

~~~text
urn:baobab-platform:service:baobab-regulations
~~~

The logical producer identity SHALL NOT be replaced by:

- pod name;
- deployment hostname;
- region;
- engine_instance_id;
- cloud-provider resource identifier.

---

## 21. CloudEvents Envelope

The active events SHALL continue to use the canonical Shared CloudEvents-compatible envelope.

RTD-08 does not introduce a Regulations-specific envelope.

---

## 22. Tenant Consistency

For tenant-scoped Regulations events:

~~~text
CloudEvent.tenantid
    =
payload tenant
    =
every nested tenant-scoped CrossEngineObjectReference.tenant_id
~~~

unless a future explicit cross-tenant contract says otherwise.

RTD-08 introduces no such exception.

---

## 23. Historical Pinning

Consequential Regulations event payloads use pinned references where historical identity matters.

Examples:

~~~text
REGULATORY_DECISION
DOCUMENT_REQUIREMENT
PERMIT_REQUIREMENT
EVIDENCE_REQUIREMENT
REGULATORY_EVIDENCE_ASSESSMENT
DOCUMENT_VERSION
~~~

The event SHALL NOT silently reinterpret a historical reference as current state.

---

## 24. Legal Time and Knowledge Time

Document-requirements-determined includes Regulations-owned temporal context through the requirement set.

Trade Docs and consumers do not choose or rewrite:

~~~text
legal_time
knowledge_time
~~~

---

## 25. Evidence Sufficiency Remains Regulations-Owned

Trade Docs may publish:

~~~text
document verified
document valid
evidence offered
~~~

Only Regulations may publish the canonical RTD-06 requirement-satisfaction result.

Therefore:

~~~text
DocumentVerification
    !=
RequirementSatisfaction
~~~

---

## 26. Wider REG-0024 Event Vocabulary Is Not Activated

ADR-REG-0024 describes additional candidate facts such as:

~~~text
regulatory change verified
future-effective change
impact confirmed
reassessment required
decision issued
decision superseded
requirement changed
runtime stale
~~~

RTD-08 does not activate those event types merely because the context is now ACTIVE.

Each future canonical event requires:

1. Shared payload contract;
2. event naming reconciliation;
3. producer semantics;
4. lifecycle registration;
5. conformance tests.

---

## 27. Local v0 Events Remain Local Draft

The baobab-regulations repository contains:

~~~text
regulations.evaluation.requested.v0
regulations.evaluation.completed.v0
~~~

They remain local draft audit schemas.

RTD-08 does not copy or promote them.

---

## 28. Naming Convention

Platform event names use:

~~~text
com.baobab-platform.<context>.<fact>.vN
~~~

Older illustrative:

~~~text
io.baobab.regulations.*
~~~

names remain superseded for Shared platform wire contracts.

---

## 29. Command/Event Separation

Assessment remains the explicit command/API:

~~~text
POST /v1/documentary-evidence/assessments
~~~

The resulting event is:

~~~text
com.baobab-platform.regulations.requirement-satisfaction.evaluated.v1
~~~

This preserves:

~~~text
command
    !=
event
~~~

---

## 30. Runtime Publication Model

Where an event corresponds to persisted authoritative Regulations state, runtime implementation SHOULD use a transactional outbox or equivalent state/event-intent atomicity.

~~~text
BEGIN

persist Regulations state
persist outbox occurrence

COMMIT
~~~

Then:

~~~text
relay
  ↓
transport/broker
~~~

---

## 31. ACTIVE Contract Does Not Mean Runtime Exists

RTD-08 activates **producer authority**, not deployment evidence.

It does not assert the current Regulations repository already has:

- production event outbox;
- broker integration;
- relay worker;
- subscriptions;
- DLQ;
- replay service;
- full production observability.

---

## 32. Consumer Semantics

Consumers SHALL assume at-least-once delivery unless a stronger transport contract is separately established.

Deduplication remains based on:

~~~text
(source, id)
~~~

A retry is not a new business occurrence.

---

## 33. Pulse Relationship

Pulse may later consume Regulations facts asynchronously for:

- risk;
- opportunity;
- forecasting;
- regulatory-change intelligence;
- strategic analysis.

Pulse does not become a Regulations producer.

RTD-09 governs Pulse projection alignment.

---

## 34. Trade Docs Relationship

Trade Docs may consume document-requirements-determined and requirement-satisfaction-evaluated where authorised.

Trade Docs does not gain authority to alter the requirements or legal conclusion.

---

## 35. Trade/TMS Relationship

Trade/TMS may consume Regulations facts to decide operational action under its own policy-enforcement authority.

A Regulations event is an input to enforcement, not the enforcement mutation itself.

---

## 36. External Authority Relationship

Baobab Regulations represents/evaluates regulatory meaning.

It does not become the sovereign source of:

- statutes;
- official permits;
- regulator rulings;
- Customs release;
- official sanctions designations.

External authority remains preserved in provenance.

---

## 37. Event Context and Capability Domain Are Related but Distinct

RTD-08 activates both:

~~~text
capability domain = regulations
event context     = regulations
~~~

but they are different registries.

The capability domain governs:

~~~text
regulations.<resource>.<action>
~~~

The event context governs:

~~~text
com.baobab-platform.regulations.<fact>.vN
~~~

One does not automatically create entries in the other.

---

## 38. Context Registry State After RTD-08

~~~text
regulations
  status: ACTIVE
  stewards:
    - baobab-regulations
  capability_domains:
    - regulations
~~~

---

## 39. Event Registry State After RTD-08

| Event | Lifecycle | Producer |
|---|---|---|
| regulations.document-requirements.determined.v1 | ACTIVE | baobab-regulations |
| regulations.requirement-satisfaction.evaluated.v1 | ACTIVE | baobab-regulations |
| documents.regulatory-evidence.offered.v1 | ACTIVE | baobab-trade-docs |

No other Regulations event is activated by RTD-08.

---

## 40. Capability Registry State After RTD-08

The namespace registry contains:

~~~text
regulations
~~~

The capability-domain enum contains:

~~~text
regulations
~~~

RTD-08 does not itself add a capability catalogue row.

---

## 41. Required CI Enforcement

Shared CI SHALL prove at least:

1. `regulations` exists in the namespace registry;
2. `regulations` exists in capabilityDomain enum;
3. namespace registry and enum remain identical;
4. `tax` remains registered;
5. `customs` remains registered;
6. Regulations event context is ACTIVE;
7. baobab-regulations is its steward;
8. its capability_domains contains regulations;
9. ADR-SHARED-024 appears in context authority;
10. exactly the two RTD-08 event types exist in the new AsyncAPI package;
11. both event registry entries are ACTIVE;
12. both name baobab-regulations as producer;
13. both RTD-06 event surfaces are ACTIVE;
14. their activation authority is ADR-SHARED-024;
15. canonical example envelopes validate;
16. event source identifies baobab-regulations;
17. nested tenant references match event tenant;
18. Trade Docs evidence-offered remains produced by baobab-trade-docs;
19. no legacy local v0 event is promoted;
20. the wider speculative REG-0024 vocabulary is not implicitly activated.

---

## 42. Rejected Alternatives

### A. Activate event context without resolving G-REG-NS

Rejected.

Shared explicitly made namespace registration a gate.

### B. Move tax into Regulations now

Rejected.

That is a larger compatibility migration and is not required for RTD-08.

### C. Move customs into Regulations now

Rejected.

Customs regulatory meaning and Customs operational workflow are deliberately decomposed.

### D. Auto-catalogue every proposed Regulations capability

Rejected.

Namespace approval is not implementation proof.

### E. Activate every event named in REG-0024

Rejected.

Illustrative event names are not canonical payload contracts.

### F. Promote local v0 evaluation events

Rejected.

They predate the canonical Shared event envelope and RTD boundary.

### G. Let Trade Docs publish satisfaction events

Rejected.

Trade Docs owns documentary facts, not legal sufficiency.

### H. Let Shared publish Regulations events

Rejected.

Shared is contract authority, not runtime producer.

---

## 43. Invariants

~~~text
INV-REG-EVT-001
regulations is a canonical Shared capability domain.

INV-REG-EVT-002
Namespace registration does not activate any capability.

INV-REG-EVT-003
tax remains a separate registered capability domain.

INV-REG-EVT-004
customs remains a separate registered capability domain.

INV-REG-EVT-005
regulations event context is ACTIVE.

INV-REG-EVT-006
baobab-regulations is the regulations context steward.

INV-REG-EVT-007
Every RTD-08 event has exactly one canonical producer.

INV-REG-EVT-008
That producer is baobab-regulations.

INV-REG-EVT-009
Document requirements are Regulations-owned facts.

INV-REG-EVT-010
Requirement satisfaction is a Regulations-owned fact.

INV-REG-EVT-011
Document verification is not requirement satisfaction.

INV-REG-EVT-012
Evidence offered is not evidence accepted.

INV-REG-EVT-013
Regulations events do not mutate TradeDocument state.

INV-REG-EVT-014
Regulations events do not directly mutate operational shipment/order state.

INV-REG-EVT-015
Commands are not disguised as events.

INV-REG-EVT-016
Cross-engine historical identity uses ADR-SHARED-021 references.

INV-REG-EVT-017
Tenant-scoped nested references match event tenant.

INV-REG-EVT-018
Legal time and knowledge time remain Regulations-owned.

INV-REG-EVT-019
Local v0 Regulations events are not platform contracts.

INV-REG-EVT-020
Wider REG-0024 illustrative facts require separate canonical contracts.

INV-REG-EVT-021
ACTIVE event authority does not assert runtime deployment.

INV-REG-EVT-022
Consumers cannot republish the canonical Regulations event type as producer.

INV-REG-EVT-023
External sovereign authority is not transferred to Regulations.

INV-REG-EVT-024
Pulse may consume Regulations events but is not in the enforcement critical path.

INV-REG-EVT-025
Trade Docs remains producer of documents.regulatory-evidence.offered.

INV-REG-EVT-026
Shared remains wire-contract authority but not runtime producer.

INV-REG-EVT-027
Capability-domain registration and event-context registration remain distinct governance concepts.

INV-REG-EVT-028
Historical pinned references are not silently replaced with current state.

INV-REG-EVT-029
Regulations unavailability is not legal prohibition.

INV-REG-EVT-030
An event delivery retry is not a new regulatory fact.
~~~

---

## 44. Consequences

### Positive

- G-REG-NS is finally resolved.
- Regulations has a canonical capability namespace.
- Regulations event ownership is no longer reserved/ambiguous.
- RTD-06 choreography is fully activated on both engine sides.
- Trade Docs and Regulations retain distinct producer authority.
- RTD-09 can safely introduce Pulse consumers.
- RTD-10 can test the complete cross-engine event boundary.

### Costs

- Capability census/catalogue work still remains.
- Existing tax/customs namespaces still need future architecture review if migration is desired.
- Regulations runtime must eventually implement active contracts.
- Additional REG-0024 event facts remain uncontracted until separately designed.

---

## 45. Final Decision

~~~text
                 SHARED
         contracts / namespaces
                 │
                 ▼
        regulations capability domain
                 │
                 ▼
         BAOBAB REGULATIONS
        canonical event producer
                 │
        ┌────────┴─────────┐
        ▼                  ▼
document-requirements   requirement-satisfaction
    determined               evaluated
        │                  │
        └────────┬─────────┘
                 ▼
        authorised consumers
~~~

while:

~~~text
tax namespace
    remains unchanged

customs namespace
    remains unchanged

proposed regulations.* capabilities
    remain proposed until normal catalogue gates

wider REG-0024 events
    remain unactivated until canonical contracts exist
~~~

> **RTD-08 activates Regulations as a first-class platform domain without making it a universal compliance monolith: Regulations owns regulatory meaning and evaluation; other engines retain their own execution authority.**
