# ADR-SHARED-019 — Regulatory Intelligence, Trade Documents and Evidence Cross-Engine Boundary

**Status:** Accepted — Normative Cross-Engine Boundary Architecture  
**Date:** 2026-10-05  
**Repository:** `baobab-platform/shared`  
**Decision Type:** Cross-Engine Authority / Evidence / Reference / Event Direction Architecture  
**Contract Authority:** `baobab-platform/shared`  
**Runtime Authorities:** `baobab-platform/baobab-regulations`, `baobab-platform/baobab-trade-docs`, `baobab-platform/baobab-pulse` within the boundaries defined here  
**Applies To:** `baobab-regulations`, `baobab-trade-docs`, `baobab-pulse`, `baobab-trade`, `baobab-tms`, `baobab-cp`, Digital Estates and any provider consuming or producing regulatory, documentary or intelligence facts  
**Refines:** ADR-SHARED-018 §8.4 and the `documents` / `regulations` event-context target authority  
**Does Not Replace:** ADR-0004, ADR-SHARED-012, ADR-SHARED-013, ADR-SHARED-017 or ADR-SHARED-018  
**Related Engine Decisions:**

- `baobab-pulse`: ADR-PULSE-001, ADR-PULSE-003, ADR-PULSE-004, ADR-PULSE-005, ADR-PULSE-006, ADR-PULSE-009
- `baobab-regulations`: ADR-REG-0001, ADR-REG-0003, ADR-REG-0005, ADR-REG-0011, ADR-REG-0021, ADR-REG-0026, ADR-REG-0027
- `baobab-trade-docs`: ADR-TDOC-0001, ADR-TDOC-0002
- `baobab-cp`: ADR-BCP-023 Organisation Evidence, Verification, Trust and Compliance Record Model

---

## 1. Executive Decision

Baobab SHALL treat **Baobab Regulations**, **Baobab Trade Docs** and **Baobab Pulse** as three independent but deliberately composable bounded contexts.

Their relationship is:

```text
                         EXTERNAL WORLD

      legal authorities · customs · issuers · registries · publications
                              │
                 ┌────────────┴────────────┐
                 │                         │
                 ▼                         ▼
        BAOBAB REGULATIONS          BAOBAB TRADE DOCS
        normative meaning           document execution
                 │                         │
                 │                         │
                 └────────────┬────────────┘
                              │
                              ▼
                         BAOBAB PULSE
                    intelligence / analysis
```

The platform SHALL preserve the following governing distinction:

```text
REGULATIONS asks:
What is required, permitted, prohibited or unresolved?

TRADE DOCS asks:
What document exists, which version is it, what happened to it,
and what did an external authority or issuer communicate?

PULSE asks:
What does the available evidence mean for risk, opportunity,
forecasting, research and decision support?
```

No engine SHALL acquire another engine's authority merely because it stores, projects, cites, analyses, verifies or acts upon that engine's output.

The cross-engine model SHALL be **reference-first, provenance-preserving and authority-preserving**:

```text
reference another engine's canonical object
                    ≠
copy its canonical ownership
                    ≠
reinterpret its authority
```

---

## 2. Context

Baobab Pulse was designed before the platform introduced Baobab Regulations and Baobab Trade Docs.

The Pulse ADR programme therefore necessarily described several concerns that were, at that time, only generic intelligence concerns:

- regulatory source acquisition;
- government gazettes and regulatory publications;
- regulatory lifecycle states;
- source documents;
- raw evidence preservation;
- regulatory evidence profiles;
- customs and trade observations;
- provenance;
- regulatory change observation.

Those decisions remain useful, but two specialist bounded contexts have since emerged.

Baobab Regulations now owns the governed chain from authoritative regulatory material to machine-actionable regulatory meaning and regulatory decisions.

Baobab Trade Docs now owns the executable lifecycle of trade and customs documents, document versions, documentary content, submissions and authority responses.

Without a platform-level decision, the three engines could independently implement overlapping versions of:

```text
Source
SourceArtefact
Document
Evidence
Verification
RegulatoryState
Classification
Requirement
Decision
Provenance
```

and accidentally turn legitimate domain-specific views into competing systems of truth.

This ADR prevents that outcome.

---

## 3. Core Authority Model

### 3.1 Three different authority planes

The platform SHALL recognise three different authority planes.

```text
NORMATIVE PLANE
Baobab Regulations

DOCUMENTARY / EXECUTION PLANE
Baobab Trade Docs

INTELLIGENCE PLANE
Baobab Pulse
```

They are related but not interchangeable.

### 3.2 Authority matrix

| Concern | Canonical authority | Notes |
|---|---|---|
| Sovereign law, regulation, ruling or official authority act | External competent authority | Baobab never manufactures sovereign authority |
| Canonical regulatory source representation | Baobab Regulations | Preserves external authority and provenance |
| Regulatory instrument / provision / interpretation / rule | Baobab Regulations | Derived Baobab meaning remains distinct from source authority |
| Applicability / obligation / permission / prohibition | Baobab Regulations | Normative determination |
| Regulatory classification for a specific legal context | Baobab Regulations | Includes governed customs classification where regulatory meaning is involved |
| Document requirement | Baobab Regulations | Requirement is not the document instance |
| Requirement satisfaction | Baobab Regulations | May depend on Trade Docs facts and other evidence |
| TradeDocument identity | Baobab Trade Docs | Stable documentary identity |
| DocumentVersion / content / rendition | Baobab Trade Docs | Version and provenance governed by Trade Docs |
| Document lifecycle | Baobab Trade Docs | Draft, issued, superseded, revoked and equivalent type-specific states |
| Customs document case / declaration submission workflow | Baobab Trade Docs | Does not make Trade Docs the customs authority |
| External customs / issuer response artefact | Baobab Trade Docs | Preserves the authority response and its provenance |
| Shipment / order operational enforcement | Owning operational engine | Usually Trade/TMS/other PEP; not Regulations or Pulse |
| Observation / EvidenceSet / Analysis / Insight | Baobab Pulse | Intelligence authority |
| Risk / Opportunity / Forecast / Recommendation | Baobab Pulse | Decision support, not operational or regulatory authority |
| Human/business decision record | Authorised human/policy; Pulse may record | Pulse recording a decision does not make it the decision authority |

### 3.3 External authority is never replaced

The following SHALL remain distinct:

```text
authority published something
        ≠
Regulations represented it
        ≠
Regulations interpreted it
        ≠
Regulations evaluated it

issuer issued a document
        ≠
Trade Docs stored it
        ≠
Trade Docs extracted it
        ≠
Trade Docs verified selected properties

Pulse observed any of the above
        ≠
Pulse became authoritative for the underlying fact
```

---

## 4. Regulatory Intelligence Boundary

### 4.1 Pulse retains regulatory intelligence

This ADR SHALL NOT remove regulation or customs from Pulse's intelligence scope.

Pulse MAY continue to represent:

- observations about regulatory publication and change;
- market reactions to regulatory changes;
- trade statistics containing HS or customs classifications as source data;
- regulatory risk;
- regulatory opportunity;
- forecasts;
- impact analysis;
- strategic recommendations;
- research claims citing regulatory material.

Example:

```text
Pulse observation:
"Dataset X reports trade under HS revision Y / code Z."

        ≠

Regulations decision:
"For consignment C, at legal time T, the applicable classification is Z."
```

The former is an observation about a source dataset.

The latter is regulatory meaning.

### 4.2 Pulse regulatory projections are not canonical regulatory truth

A Pulse `RegulatoryObservation`, regulatory evidence profile, regulatory delta or research claim SHALL be treated as an intelligence representation.

It SHALL NOT replace:

- RegulatoryInstrument;
- Provision;
- RegulatoryRule;
- Applicability;
- RegulatoryRequirement;
- RegulatoryAssessment;
- RegulatoryDecision;
- any equivalent canonical Regulations aggregate.

### 4.3 Regulatory change

Regulations SHALL own the canonical regulatory change once the underlying legal/regulatory change has been acquired and governed.

Pulse MAY consume that change and produce:

```text
Signal
Risk
Opportunity
Forecast
Recommendation
CommercialImpactAnalysis
```

Pulse SHALL NOT independently promote an observed publication into an effective regulatory obligation without the Regulations governance boundary.

---

## 5. Regulations and Trade Docs Boundary

### 5.1 Requirement is not document

The following is a hard invariant:

```text
DocumentRequirement
        !=
TradeDocument
```

Regulations determines:

```text
Certificate X is required
Permit Y is required
Proof of origin is required
Declaration Z must be submitted
Document must satisfy conditions A, B and C
```

Trade Docs owns the concrete documentary lifecycle:

```text
document obtained / generated
        ↓
version established
        ↓
content preserved
        ↓
issuer / provenance recorded
        ↓
verification performed
        ↓
submitted
        ↓
authority response received
```

### 5.2 Document authenticity is not regulatory sufficiency

The following are different determinations:

```text
DocumentIntegrity
DocumentAuthenticity
IssuerVerification
DocumentValidity
RequirementSatisfaction
```

Trade Docs MAY establish documentary facts such as:

```text
hash matches
issuer credential verified
version 4 is current
document was issued at T
document concerns consignment C
document has not been revoked
```

Regulations determines whether those facts satisfy a regulatory requirement in the relevant:

- jurisdiction;
- regime;
- commodity context;
- consignment context;
- legal time;
- knowledge time.

Therefore:

```text
Trade Docs VERIFIED
        ≠
Regulations SATISFIED
```

### 5.3 Customs authority response

A customs authority response remains an external-authority artefact.

Trade Docs MAY own the canonical Baobab record of:

- submission;
- acknowledgement;
- rejection;
- authority message;
- release message;
- external reference;
- received bytes / structured payload where lawful;
- response provenance.

But:

```text
Trade Docs recorded RELEASED
        ≠
Trade Docs became the customs authority
```

### 5.4 Regulations consumes documentary facts by reference

Regulations SHALL consume Trade Docs facts using cross-engine references and explicit evidence snapshots.

It SHALL NOT create a competing TradeDocument aggregate.

A regulatory evaluation MAY persist an immutable evaluation snapshot sufficient for replay, but that snapshot does not become the current document master.

---

## 6. Evidence Semantics

### 6.1 "Evidence" is contextual, not one universal aggregate

The platform SHALL not treat the word **evidence** as proof that all engines must share one database or one aggregate.

There are at least four relevant evidence contexts:

| Evidence context | Owner | Purpose |
|---|---|---|
| Regulatory evidence | Regulations | Supports source authority, interpretation, rule derivation, applicability and regulatory decisions |
| Documentary evidence | Trade Docs | Documents, document versions, authority messages and verification facts used in documentary/customs workflow |
| Analytical evidence | Pulse | Supports analyses, claims, insights, forecasts, risks, opportunities and recommendations |
| Organisation verification evidence | Control Plane / ADR-BCP-023 | Supports organisation, legal-entity and related verification workflows |

These MAY share principles and reference contracts.

They SHALL NOT silently become one canonical domain.

### 6.2 Shared `contracts/evidence/v1` is not the universal evidence store

The existing Shared `contracts/evidence/v1` package is governed by ADR-BCP-023 and currently models organisation verification evidence whose runtime owner is the Control Plane.

This ADR SHALL NOT reinterpret that package as the canonical persistence model for Regulations, Trade Docs or Pulse.

A future general cross-engine evidence-reference contract MAY reuse compatible vocabulary, but it SHALL preserve domain ownership.

### 6.3 Document is not Evidence

Hard invariant:

```text
TradeDocument
    !=
Evidence
```

A TradeDocument or DocumentVersion MAY be referenced as evidence.

The evidence relationship adds:

- purpose;
- relevance;
- role;
- validity scope;
- decision or claim context;
- provenance edge.

It does not change document ownership.

### 6.4 Evidence is not truth

The platform retains the principle already present in the Control Plane evidence model:

```text
Evidence
    !=
Truth
```

Likewise:

```text
source authority
    !=
perfect accuracy

integrity
    !=
authenticity

authenticity
    !=
applicability

verification
    !=
regulatory satisfaction

regulatory decision
    !=
sovereign decision
```

### 6.5 Evidence immutability and replay

If an object was used in a consequential decision or published intelligence product, the consuming engine SHALL preserve enough reference/version/snapshot information to reproduce what it used.

A later source update SHALL NOT rewrite historical decision evidence.

The current master and the historical decision snapshot SHALL remain distinguishable.

---

## 7. Cross-Engine Reference Semantics

### 7.1 Reference, do not copy ownership

Cross-engine contracts SHALL refer to canonical objects owned by another engine rather than re-declare those objects locally.

Conceptually:

```text
CrossEngineObjectReference
├── owner_engine
├── object_type
├── object_id
├── object_version? / revision?
├── tenant_id? / scope?
├── observed_at? / resolved_at?
└── integrity / provenance hints where required
```

This is a conceptual shape. The executable Shared schema is a follow-up contract task.

### 7.2 Existing ExternalReference is not this abstraction

ADR-SHARED-013 `ExternalReference` records a **native external-system object**.

A cross-engine reference to a canonical Regulations, Trade Docs or Pulse object SHALL NOT misuse ExternalReference merely because both contain the word "reference".

```text
ExternalReference
    = native external-system identity

CrossEngineObjectReference
    = canonical Baobab object owned by another engine
```

If the referenced object itself points to a customs authority ID, provider ID or other native system object, that native identity MAY independently use the ExternalReference / mapping architecture.

### 7.3 Authority travels with the reference

A consumer SHALL NOT strip the authority semantics from a reference.

Example:

```text
RegulatoryDecision reference
owner_engine = baobab-regulations

TradeDocumentVersion reference
owner_engine = baobab-trade-docs

EvidenceSet reference
owner_engine = baobab-pulse
```

The consumer may project or cache the object, but SHALL retain the owner and version identity required to distinguish source truth from consumer projection.

### 7.4 No cross-engine database access

References SHALL resolve through governed APIs, events, capability bindings or approved projections.

This ADR does not permit:

```text
Pulse reading Regulations tables
Regulations reading Trade Docs tables
Trade Docs reading Pulse tables
```

---

## 8. Event Directionality

### 8.1 Events state facts; APIs/capabilities request work

ADR-SHARED-018 remains governing.

An event SHALL state a fact that already occurred.

Commands and evaluation requests SHALL use governed APIs/capabilities or an explicitly modelled command mechanism, not event names pretending to be facts.

### 8.2 Regulations → Trade Docs

Regulations MAY publish canonical facts such as:

```text
regulatory decision completed
document requirement determined
classification assigned
requirement changed
decision superseded / invalidated
```

Trade Docs consumes those facts to drive documentary workflow.

The event payload SHOULD carry identifiers and bounded summary data; the canonical Regulations object remains retrievable from Regulations.

Trade Docs SHALL NOT copy the complete legal reasoning graph into its document aggregate.

### 8.3 Trade Docs → Regulations

Trade Docs MAY publish facts such as:

```text
trade document issued
trade document superseded
trade document verified
trade document verification changed
document submitted
authority response received
document revoked / expired
customs case state changed
```

Regulations MAY consume those facts to:

- reassess a requirement;
- invalidate a prior evidence assessment;
- trigger regulatory re-evaluation;
- update requirement satisfaction.

Trade Docs SHALL NOT publish an event asserting that a legal requirement is satisfied unless that satisfaction is itself a Regulations-owned decision.

### 8.4 Regulations → Pulse

Pulse MAY consume:

- regulatory source changes;
- regulatory change events;
- classification decisions;
- regulatory assessments;
- regulatory decisions;
- regulatory impact facts.

Pulse uses them as intelligence inputs.

It MAY derive:

- risk;
- opportunity;
- forecast;
- commercial impact;
- strategic recommendation.

Those derivatives remain Pulse-owned.

### 8.5 Trade Docs → Pulse

Pulse MAY consume document/customs lifecycle facts for:

- delay analysis;
- corridor performance;
- document rejection patterns;
- customs processing time;
- operational risk;
- evidence-backed research.

Pulse SHALL use only the facts it is authorised to access and SHALL preserve tenant/classification restrictions.

### 8.6 Pulse → Regulations

Pulse MAY:

- request a regulatory assessment through the appropriate capability/API;
- provide referenced business/intelligence context;
- identify a candidate source or suspected regulatory change for governed acquisition;
- provide analytical hypotheses.

Pulse SHALL NOT publish a Pulse insight as if it were a canonical regulatory rule or regulatory decision.

A candidate regulatory source discovered by Pulse enters Regulations only through the Regulations source-acquisition and promotion boundary.

### 8.7 Pulse → Trade Docs

Pulse MAY create recommendations about documentary or customs workflow.

Such a recommendation SHALL NOT directly mutate a TradeDocument, CustomsCase or authority submission unless a separately authorised automation policy and the owning engine's command boundary permit the action.

Default:

```text
Pulse Recommendation
       ↓
human / authorised policy
       ↓
Trade Docs command
```

### 8.8 Pulse is not on the critical regulatory execution path

Pulse SHALL NOT be required synchronously for:

- determining whether a regulatory rule applies;
- producing a RegulatoryDecision;
- determining whether required documentary evidence is present;
- submitting a customs declaration;
- processing an authority response;
- enforcing a regulatory hold.

The critical path is:

```text
operational context
       ↓
Regulations
       ↓
Trade Docs / operational PEP
```

Pulse may observe and analyse that path asynchronously.

This prevents intelligence-provider, model-provider, vector-store or research-pipeline availability from becoming a customs or compliance availability dependency.

---

## 9. Event Context Ownership

### 9.1 `regulations`

The target steward for the Shared `regulations` event context SHALL be:

```text
baobab-regulations
```

Its target semantics are canonical regulatory meaning and evaluation facts.

The context may move from `RESERVED` to `ACTIVE` only when the corresponding Shared contracts and producer conformance are implemented.

### 9.2 `documents`

The target steward for the Shared `documents` event context SHALL be:

```text
baobab-trade-docs
```

for trade-document lifecycle facts governed by ADR-TDOC-0001/0002.

The existing proposed:

```text
com.baobab-platform.documents.trade-document.issued.v1
com.baobab-platform.documents.trade-document.verified.v1
com.baobab-platform.documents.trade-document.rejected.v1
```

shall not be activated with an ambiguous producer.

A follow-up contract PR SHALL reconcile their payloads and lifecycle semantics with ADR-TDOC-0001/0002 before assigning `baobab-trade-docs` as producer.

### 9.3 `customs`

This ADR does not make every customs fact a Regulations or Trade Docs fact.

The platform SHALL distinguish:

```text
regulatory meaning / classification / applicability
        → Regulations

customs document / declaration submission / authority message workflow
        → Trade Docs

shipment or trade operational enforcement
        → owning Trade/TMS/other PEP

external customs ruling / release authority
        → competent customs authority
```

The existing `customs` context SHALL be reviewed in the follow-up contract task so event-type ownership reflects the fact being stated, not historical engine placement.

### 9.4 Pulse event context

A future Pulse cross-engine event context SHALL describe intelligence facts rather than engine internals.

It SHALL be registered under ADR-SHARED-018 before Pulse emits canonical cross-engine intelligence event types.

The context name SHALL be domain-oriented and shall not be inferred solely from the repository name.

---

## 10. Synchronous Interaction Model

Events are not sufficient for every interaction.

### 10.1 Regulations capability

Consumers needing an authoritative current answer SHALL use the Regulations capability/API for:

- classification;
- applicability;
- obligation determination;
- regulatory assessment;
- requirement satisfaction;
- decision retrieval / replay.

### 10.2 Trade Docs capability

Consumers needing authoritative documentary state SHALL use Trade Docs for:

- document retrieval;
- document version;
- document content metadata;
- documentary verification;
- submission state;
- customs case state;
- authority-response retrieval.

### 10.3 Pulse capability

Consumers needing intelligence SHALL use Pulse for:

- evidence-backed analysis;
- risk;
- opportunity;
- forecasting;
- research;
- recommendations.

### 10.4 Capability resolution

The Control Plane remains authoritative for:

- tenant/context resolution;
- capability grants;
- provider resolution;
- engine topology;
- engine-instance resolution.

No consumer SHALL hard-code a direct service URL because this ADR names an engine authority.

---

## 11. Temporal and Freshness Rules

### 11.1 Regulatory time

Regulations remains authoritative for legal time, knowledge time and regulatory version applicability.

### 11.2 Documentary time

Trade Docs remains authoritative for:

- document issue time;
- version time;
- submission time;
- authority-response time;
- revocation / expiry lifecycle time.

### 11.3 Analytical time

Pulse may maintain observation time, acquisition time, analysis time and data vintage.

### 11.4 Staleness

A consuming engine SHALL NOT assume that a previously obtained cross-engine reference still means the same thing if material context changed.

Examples:

- route changed;
- commodity changed;
- legal time crossed an effective-date boundary;
- document was superseded;
- issuer verification was revoked;
- regulatory rule set changed.

The owner engine determines whether the object remains current/applicable.

---

## 12. Failure and Disagreement Semantics

### 12.1 Engine unavailable

A consumer SHALL distinguish:

```text
owner engine unavailable
        ≠
object not found
        ≠
object invalid
        ≠
requirement unsatisfied
```

### 12.2 Indeterminate regulatory result

Trade Docs SHALL NOT convert a Regulations `INDETERMINATE` outcome into `SATISFIED`.

The operational PEP applies the configured fail-safe disposition.

### 12.3 Documentary conflict

If Trade Docs has conflicting document/issuer facts, it SHALL preserve the discrepancy.

Regulations SHALL receive that uncertainty explicitly rather than a convenient selected value.

### 12.4 Analytical uncertainty

Pulse confidence is an intelligence property.

It SHALL NOT downgrade or upgrade the legal authority of a source or regulatory decision merely because a model confidence score is high or low.

---

## 13. Canonical Example — Required Phytosanitary Certificate

```text
1. Shipment / consignment context
           │
           ▼
2. Baobab Regulations
   determines:
   PHYTOSANITARY_CERTIFICATE_REQUIRED
           │
           │ RegulatoryDecision / DocumentRequirement ref
           ▼
3. Baobab Trade Docs
   obtains / receives document
           │
           ├── DocumentVersion
           ├── issuer claim
           ├── content hash
           ├── verification facts
           └── consignment association
           │
           ▼
4. Trade Docs emits document facts
           │
           ▼
5. Baobab Regulations
   evaluates:
   authentic?
   correct issuer?
   correct commodity?
   correct consignment?
   still valid?
   satisfies legal requirement?
           │
           ▼
6. RegulatoryDecision
   SATISFIED / UNSATISFIED / INDETERMINATE
           │
           ├────────► operational PEP
           │
           └────────► Pulse
                         │
                         ▼
                  delay / risk / trend /
                  commercial analysis
```

No step changes the authority of the preceding step.

---

## 14. Canonical Example — Regulatory Change Creates Commercial Opportunity

```text
Official authority publishes change
           │
           ▼
Regulations acquires + governs source
           │
           ▼
RegulatoryChange
           │
           ▼
Pulse consumes canonical change
           │
           ├── market data
           ├── internal demand data
           └── historical trade evidence
           │
           ▼
Opportunity / Risk / Recommendation
           │
           ▼
human / authorised business decision
```

Pulse does not need to parse the legal source independently in order to know the canonical regulatory meaning once Regulations has established it.

It may retain the underlying source citation for research reproducibility where rights permit.

---

## 15. Canonical Example — Pulse Discovers a Candidate Regulatory Change First

```text
Pulse research adapter discovers publication
           │
           ▼
Pulse SourceArtefact / Observation
   status: candidate intelligence
           │
           ▼
governed hand-off / source reference
           │
           ▼
Regulations acquisition boundary
           │
           ├── authority verification
           ├── rights checks
           ├── source registration
           ├── interpretation
           └── human / deterministic promotion
           │
           ▼
canonical RegulatoryChange
           │
           ▼
Pulse consumes canonical regulatory state
```

The discovery path does not allow Pulse to bypass Regulations promotion.

---

## 16. Data Duplication Rules

### 16.1 Permitted

Consumers MAY retain:

- reference identifiers;
- bounded snapshots used for historical replay;
- immutable event payloads;
- read models;
- caches;
- search projections;
- analytical embeddings;
- source citations.

### 16.2 Prohibited

Consumers SHALL NOT maintain a shadow canonical aggregate whose semantics compete with the owner.

Examples prohibited by default:

```text
Pulse canonical RegulatoryRule
Trade Docs canonical RegulatoryDecision
Regulations canonical TradeDocumentVersion
Pulse canonical CustomsCase
Trade Docs canonical Pulse Risk
```

### 16.3 Projection labelling

A projection MUST remain identifiable as a projection.

Projection loss SHALL be recoverable from canonical owner data where the architecture promises rebuildability.

---

## 17. Security, Tenancy and Classification

Every cross-engine reference and event SHALL preserve:

- tenant scope where applicable;
- data classification;
- authorised purpose;
- legal / contractual access restrictions;
- source rights;
- provenance;
- correlation / causation metadata under ADR-0004.

A reference does not grant access.

```text
know object id
    !=
authorised to resolve object
```

Pulse SHALL not use analytical retrieval to bypass Regulations or Trade Docs authorisation.

Regulations SHALL not expose restricted source material merely because a regulatory decision cites it.

Trade Docs SHALL not expose regulated-document content merely because an event names the document.

Events SHOULD carry identifiers and minimum necessary facts; sensitive content is retrieved through the owner engine under authorisation.

---

## 18. Relationship to Existing Shared Evidence Contracts

The platform currently has domain-specific Shared contracts that use the word evidence.

This ADR establishes the following rule:

> **Shared schemas may standardise portable reference and metadata semantics without centralising domain ownership.**

Accordingly:

- Control Plane organisation evidence remains governed by ADR-BCP-023.
- Regulatory evidence remains governed by Regulations.
- Trade-document evidence remains governed by Trade Docs.
- Analytical evidence remains governed by Pulse.
- Future Shared cross-engine schemas should compose these domains through references, not by creating one universal evidence database.

---

## 19. Contract Implications

This ADR deliberately defines architecture before changing executable contracts.

The following contract work SHALL follow.

### 19.1 Cross-engine object reference

Shared SHALL define a reusable canonical-object reference suitable for references to engine-owned Baobab objects.

It SHALL:

- name the owning engine;
- name object type;
- carry the canonical object identifier;
- support version/revision when materially required;
- preserve tenant/scope semantics;
- avoid embedding arbitrary copied domain payloads;
- remain distinct from ADR-SHARED-013 `ExternalReference`.

### 19.2 Regulations contracts

Shared SHALL introduce or promote canonical Regulations contracts for at least:

- regulatory decision reference;
- regulatory assessment / decision events;
- document requirement / evidence requirement references where cross-engine use requires them;
- classification decisions where externally consumed.

The existing repository-local `regulations.evaluation.*.v0` schemas SHALL not become platform contracts merely by being copied. They require reconciliation with ADR-0004 and ADR-SHARED-018.

### 19.3 Trade Docs contracts

The existing `contracts/trade-document/v1` package SHALL be reconciled with ADR-TDOC-0001 and ADR-TDOC-0002 before activation.

At minimum the follow-up must address:

- stable TradeDocument identity;
- DocumentVersion identity;
- lifecycle vs verification separation;
- issuer claim vs issuer verification;
- provenance;
- external authority identifiers;
- document relationships;
- submission / authority response references where required.

### 19.4 Pulse contracts

Pulse SHALL consume Regulations and Trade Docs through references/events rather than introducing local copies of their canonical contracts.

Future Pulse cross-engine events SHALL be registered under ADR-SHARED-018.

---

## 20. Required ADR Reconciliation

This Shared ADR becomes the platform-level authority for the relationship.

Follow-up engine ADR work SHALL make that authority explicit.

### 20.1 Pulse

A Pulse reconciliation ADR SHOULD state:

```text
REGULATORY and CUSTOMS remain valid intelligence domains,
but canonical regulatory meaning belongs to Regulations,
and canonical trade-document lifecycle belongs to Trade Docs.
```

The reconciliation SHOULD amend/supersede only the overlapping portions of ADR-PULSE-001/003/005 rather than discarding their general evidence architecture.

### 20.2 Regulations

ADR-REG-0026 and ADR-REG-0027 SHOULD be amended so:

- Trade Docs is explicit in the cross-engine integration topology;
- documentary instances/versions/workflows are not owned by Regulations;
- Regulations owns requirements and satisfaction decisions.

### 20.3 Trade Docs

Trade Docs SHALL consume Regulations decisions and requirements rather than introducing jurisdiction-specific legal rules internally.

---

## 21. Migration and Implementation Sequence

The recommended implementation sequence is:

| Step | Change | Repository |
|---|---|---|
| RTD-01 | Accept this cross-engine boundary ADR | Shared |
| RTD-02 | Add Pulse regulatory/trade-document reconciliation ADR | baobab-pulse |
| RTD-03 | Amend REG-0026 / REG-0027 integration and documentary ownership | baobab-regulations |
| RTD-04 | Reconcile Trade Docs Shared contracts with TDOC-0001/0002 | Shared + baobab-trade-docs |
| RTD-05 | Define canonical cross-engine object reference contract | Shared |
| RTD-06 | Define Regulations → Trade Docs and Trade Docs → Regulations contract/event surfaces | Shared + both engines |
| RTD-07 | Activate `documents` producer/steward ownership | Shared |
| RTD-08 | Activate `regulations` event context and platform contracts | Shared |
| RTD-09 | Add Pulse consumers/projections without making Pulse part of the enforcement path | baobab-pulse |
| RTD-10 | Add cross-repository contract/conformance tests | Shared + consumers |

Contract changes SHOULD be delivered in separately reviewable PRs after RTD-01 so the architecture remains understandable and reversible.

---

## 22. Non-Goals

This ADR does not:

- choose a message broker;
- force a shared database;
- make Pulse the AI provider for Regulations;
- make Regulations the document management system;
- make Trade Docs the legal rule engine;
- make Shared the runtime owner of evidence;
- define every future event type;
- replace Control Plane capability resolution;
- define sovereign legal authority;
- decide all customs ownership outside the three-engine boundary addressed here.

---

## 23. Rejected Alternatives

### A. Put all evidence in Pulse

Rejected.

Pulse is the System of Intelligence, not the canonical owner of every source artefact, trade document or regulatory proof used by the platform.

### B. Put all regulatory documents in Regulations

Rejected.

Regulations needs regulatory sources and evidence for legal meaning, but operational trade documents and customs workflow have a separate lifecycle and authority boundary.

### C. Put regulatory requirements in Trade Docs

Rejected.

That turns a document workflow engine into a jurisdiction-specific rule engine and duplicates Regulations.

### D. Let Pulse provide the AI layer for Regulations

Rejected as a mandatory dependency.

Both engines may use Haystack, Qdrant, model providers and similar patterns, but technology reuse does not imply shared domain authority.

### E. Use one universal Evidence aggregate

Rejected.

Evidence semantics are purpose- and domain-specific. Shared should standardise references and portable metadata, not erase bounded contexts.

### F. Copy full cross-engine objects into every event

Rejected.

It causes authority drift, schema duplication, stale state and accidental multi-master ownership.

### G. Put Pulse synchronously in the compliance path

Rejected.

Regulatory/customs execution must not depend on research, vector retrieval or probabilistic intelligence availability.

---

## 24. Consequences

### Positive

- Removes ambiguity created by Pulse predating Regulations and Trade Docs.
- Preserves valuable Pulse evidence architecture without allowing it to become regulatory authority.
- Makes Regulations ↔ Trade Docs composition explicit before Trade Docs runtime implementation begins.
- Gives Shared a clear basis for cross-engine reference contracts.
- Prevents duplicate TradeDocument and RegulatoryDecision aggregates.
- Preserves PDP/PEP separation.
- Makes events facts rather than cross-engine commands.
- Keeps AI technology choices replaceable and bounded.
- Improves historical replay and auditability by requiring versioned references.

### Costs

- Existing Pulse ADR wording requires reconciliation.
- Regulations integration ADRs require updates.
- The initial Shared TradeDocument contract must evolve before activation.
- New Shared reference and event contracts are required.
- Consumers must resolve references through APIs/capabilities rather than joining databases.
- Cross-repository conformance testing becomes necessary.

These costs are intentional. They are materially cheaper now than after three engines independently implement overlapping domain truth.

---

## 25. Platform Invariants

The following SHALL be mechanically testable as implementation matures.

```text
INV-RTD-001
Only Regulations produces canonical regulatory decisions.

INV-RTD-002
Only Trade Docs produces canonical trade-document lifecycle facts
for the documents context once activated.

INV-RTD-003
Pulse does not publish canonical regulatory rules, classifications
or compliance decisions.

INV-RTD-004
Trade Docs contains no jurisdiction-specific legal requirement logic
except implementation of an authoritative Regulations decision or
external-authority protocol.

INV-RTD-005
Regulations does not maintain a competing TradeDocument aggregate.

INV-RTD-006
Cross-engine canonical references retain owner identity.

INV-RTD-007
ExternalReference is not used as a substitute for a canonical
cross-engine object reference.

INV-RTD-008
Events carry minimum necessary facts and references; they do not
silently replicate foreign canonical aggregates.

INV-RTD-009
Pulse is not a synchronous dependency of regulatory enforcement.

INV-RTD-010
Historical decisions preserve the object versions/snapshots used
for replay.

INV-RTD-011
Document verification does not imply regulatory requirement
satisfaction.

INV-RTD-012
No consumer gains direct database access to another engine through
this architecture.
```

---

## 26. Final Boundary

The canonical relationship is:

```text
                  ┌──────────────────────────────┐
                  │       EXTERNAL AUTHORITY     │
                  │ law · customs · issuer truth │
                  └──────────────┬───────────────┘
                                 │
             ┌───────────────────┴───────────────────┐
             │                                       │
             ▼                                       ▼
┌─────────────────────────┐             ┌─────────────────────────┐
│   BAOBAB REGULATIONS    │             │    BAOBAB TRADE DOCS    │
│                         │             │                         │
│ regulatory source       │             │ TradeDocument           │
│ instrument / provision  │             │ DocumentVersion         │
│ interpretation / rule   │◄───────────►│ content / provenance    │
│ applicability           │ references  │ verification facts      │
│ obligation / requirement│             │ submissions             │
│ RegulatoryDecision      │             │ authority responses     │
└────────────┬────────────┘             └────────────┬────────────┘
             │                                       │
             └───────────────────┬───────────────────┘
                                 │ events / references
                                 ▼
                    ┌─────────────────────────┐
                    │      BAOBAB PULSE       │
                    │                         │
                    │ Observation             │
                    │ Evidence / EvidenceSet  │
                    │ Analysis / Insight      │
                    │ Risk / Opportunity      │
                    │ Forecast                │
                    │ Recommendation          │
                    └─────────────────────────┘
```

The governing sentence is:

> **Regulations determines regulatory meaning. Trade Docs executes and preserves documentary truth and customs-document workflow. Pulse turns authorised evidence from those and other domains into intelligence. References connect the engines; references do not transfer authority.**
