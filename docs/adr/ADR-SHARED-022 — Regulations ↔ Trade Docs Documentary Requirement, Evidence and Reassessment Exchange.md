# ADR-SHARED-022 — Regulations ↔ Trade Docs Documentary Requirement, Evidence and Reassessment Exchange

**Status:** Accepted — Normative Cross-Engine Contract Architecture  
**Date:** 2026-10-05  
**Repository:** baobab-platform/shared  
**Decision ID:** ADR-SHARED-022  
**Decision Type:** Cross-Engine API / Event / Evidence / Requirement Choreography  
**Implements:** RTD-06 from ADR-SHARED-019  
**Depends On:** ADR-0004, ADR-SHARED-018, ADR-SHARED-019, ADR-SHARED-020, ADR-SHARED-021  
**Runtime Authorities:** baobab-regulations and baobab-trade-docs  
**Canonical Contract:** contracts/regulatory-document-exchange/v1/

---

## 1. Decision

Baobab SHALL implement the Regulations ↔ Trade Docs boundary as a reference-first choreography:

~~~text
Trade / TMS
    │ business facts
    ▼
Regulations
    │
    ├── RegulatoryDecision
    └── documentary requirements
             │
             ▼
         Trade Docs
   documents / versions / verification
             │
             ▼
      documentary evidence
             │
             ▼
         Regulations
   legal sufficiency assessment
             │
             ▼
 requirement satisfaction
             │
             ▼
 refreshed RegulatoryDecision?
~~~

The authority split is:

| Concern | Authority |
|---|---|
| legal applicability | Regulations |
| DocumentRequirement / PermitRequirement / EvidenceRequirement | Regulations |
| requirement version and legal time | Regulations |
| requirement satisfaction | Regulations |
| TradeDocument | Trade Docs |
| DocumentVersion | Trade Docs |
| document type/family | Trade Docs |
| issuer claim | Trade Docs |
| documentary verification facts | Trade Docs |
| documentary temporal-validity facts | Trade Docs |
| documentary assertions/extractions | Trade Docs |
| legal sufficiency of documentary facts | Regulations |
| shipment/order operational state | Trade / TMS |
| sovereign permit/certificate/release | competent external authority |

The hard boundary is:

~~~text
DocumentRequirement != TradeDocument
DocumentVersion != RequirementSatisfaction
DocumentVerification != RequirementSatisfaction
EvidenceOffered != EvidenceAccepted
RequirementSatisfaction != ShipmentRelease
~~~

---

## 2. Why RTD-06 Is Required

RTD-03 corrected Regulations ownership.

RTD-04 corrected TradeDocument contracts.

RTD-05 created the canonical CrossEngineObjectReference.

RTD-06 turns those decisions into executable hand-off contracts. Without it, the engines could still invent ad hoc fields such as document_id, permit_id, requirement_id, verified=true or compliant=true with incompatible authority semantics.

---

## 3. Canonical Package

The Shared package is:

~~~text
contracts/regulatory-document-exchange/v1
~~~

It contains:

- domain.schema.json;
- events.schema.json;
- event-surfaces.yaml;
- regulations.openapi.yaml;
- trade-docs.openapi.yaml;
- examples.

Shared owns the wire contract. Regulations and Trade Docs retain runtime/domain authority.

---

## 4. Regulations → Trade Docs Requirement Projection

Regulations exposes RegulatoryDocumentRequirementProjection.

It is a read projection of a Regulations-owned requirement:

~~~text
requirement_reference
regulatory_decision_reference
requirement_kind
requirement_code
purpose_code
acceptable_document_types[]
required_issuer_roles[]
required_data_elements[]
unsatisfied_effect_code
effective_from
effective_to
determined_at
~~~

Trade Docs may use the projection to execute documentary workflow. It SHALL NOT reinterpret or mutate the legal requirement.

Requirement kinds are:

~~~text
DOCUMENT
PERMIT
EVIDENCE
~~~

and their owner object types are:

~~~text
DOCUMENT_REQUIREMENT
PERMIT_REQUIREMENT
EVIDENCE_REQUIREMENT
~~~

All are owned by baobab-regulations.

---

## 5. Requirement and Decision Pinning

A requirement used in consequential workflow SHALL be historically pinned.

Every requirement projection identifies the pinned RegulatoryDecision that produced or contextualised it.

Trade Docs SHALL NOT interpret a stored requirement as whatever the law or requirement happens to be now.

Legal time and knowledge time remain Regulations-owned. The evidence-assessment command deliberately does not let the caller choose them.

---

## 6. Trade Docs → Regulations Documentary Facts

Trade Docs exposes DocumentEvidenceFactBundle.

It is a bounded projection, not a copy of the complete TradeDocument aggregate.

It contains:

~~~text
DocumentVersion reference
document type
document family
issuer claim
issued/effective dates
verification snapshot
temporal-validity snapshot
subject references
documentary assertions
content-artifact references
facts_observed_at
~~~

The evidentiary identity is the exact DocumentVersion, using:

~~~text
owner = baobab-trade-docs
type = DOCUMENT_VERSION
reference_mode = IDENTITY_PINNED
~~~

A mutable TradeDocument root is not sufficient historical evidence identity.

---

## 7. Verification and Validity Are Facts, Not Legal Conclusions

Trade Docs supplies point-in-time documentary facts such as:

~~~text
verification = VERIFIED
temporal_validity = CURRENTLY_VALID
~~~

These do not mean:

~~~text
requirement = SATISFIED
~~~

An authentic, current document may still be for the wrong consignment, wrong commodity, wrong issuer, wrong jurisdiction or wrong legal regime.

---

## 8. Documentary Assertions and Provenance

Requirements may name required data elements such as:

~~~text
CONSIGNMENT_REFERENCE
ORIGIN_COUNTRY
COMMODITY_DESCRIPTION
QUANTITY
CERTIFICATE_NUMBER
~~~

Trade Docs therefore supplies bounded DocumentaryAssertion projections.

Every assertion records its origin:

~~~text
ISSUER_ASSERTED
BAOBAB_EXTRACTED
BAOBAB_GENERATED
EXTERNAL_NORMALIZED
~~~

This distinction is normative.

~~~text
OCR/extracted value != issuer assertion
normalized value != source-original assertion
verification != regulatory sufficiency
~~~

A documentary assertion may point to the exact ContentArtifact from which it was obtained.

Regulations determines whether that assertion is acceptable evidence for the legal requirement.

---

## 9. Subject References

A document may be associated with shipment, consignment, order, organisation, product or another domain object.

RTD-06 uses RTD-05 CrossEngineObjectReference values for portable cross-engine subject identity.

A subject reference identifies the subject. It does not copy the subject aggregate.

---

## 10. Requirement Resolution API

Regulations exposes:

~~~text
POST /v1/documentary-requirements/resolve
~~~

Input:

~~~text
context_id
requirement_reference
~~~

Output:

~~~text
RegulatoryDocumentRequirementProjection
~~~

This is a read/resolve operation. POST is used because the pinned reference is structured and may contain version/scope semantics; it does not make the operation a mutation.

---

## 11. Documentary Evidence Resolution API

Trade Docs exposes:

~~~text
POST /v1/regulatory-document-evidence/resolve
~~~

Input:

~~~text
context_id
DocumentVersion references[]
~~~

Output:

~~~text
DocumentEvidenceFactBundle[]
~~~

This endpoint exposes documentary facts. It does not perform legal evaluation.

---

## 12. Documentary Evidence Assessment Command

An authorised workflow calls Regulations:

~~~text
POST /v1/documentary-evidence/assessments
~~~

with:

~~~text
context_id
RegulatoryDecision reference
Requirement reference
assessment_reason
DocumentEvidenceFactBundle[]
~~~

This is explicitly a command.

It SHALL require Idempotency-Key because retries must not create duplicate assessment effects.

Assessment reasons include:

~~~text
INITIAL_EVIDENCE
EVIDENCE_CHANGED
VERIFICATION_CHANGED
VALIDITY_CHANGED
MANUAL_REVIEW
REGULATORY_REASSESSMENT
~~~

These describe why the command was issued. They do not determine the legal result.

---

## 13. Assessment Result

Regulations returns DocumentEvidenceAssessmentResult:

~~~text
assessment_reference
regulatory_decision_reference
requirement_reference
outcome
accepted_document_version_references[]
rejected_evidence[]
reason_codes[]
resulting_regulatory_decision_reference?
evaluated_at
~~~

The requirement-satisfaction outcomes are:

~~~text
SATISFIED
UNSATISFIED
INDETERMINATE
NOT_APPLICABLE
REVIEW_REQUIRED
~~~

These are Regulations-owned conclusions.

The assessment result SHALL NOT alter document lifecycle, verification, shipment state, order state or accounting state.

---

## 14. New RegulatoryDecision

Documentary evidence may materially change the wider regulatory decision.

The result may therefore point to a new or superseding RegulatoryDecision.

This does not mutate the historical decision that existed before the evidence assessment.

---

## 15. Planned Cross-Engine Events

RTD-06 defines three event payload surfaces.

Trade Docs fact:

~~~text
com.baobab-platform.documents.regulatory-evidence.offered.v1
~~~

Regulations facts:

~~~text
com.baobab-platform.regulations.document-requirements.determined.v1

com.baobab-platform.regulations.requirement-satisfaction.evaluated.v1
~~~

Their payloads are defined now, but they are not activated now.

---

## 16. Evidence Offered Is Not an Assessment Command

The Trade Docs event means:

> specific pinned DocumentVersions were offered against a pinned Regulations requirement.

It does not mean:

> Regulations has evaluated them.

It SHALL NOT be interpreted as an implicit command to assess.

Async evaluation, when desired, still needs an explicit command/capability invocation.

---

## 17. Requirements Determined Event

The Regulations requirements-determined fact carries a pinned requirement-set projection.

It tells Trade Docs what Regulations determined for a specific decision context.

It does not allow Trade Docs to amend the requirement.

---

## 18. Satisfaction Evaluated Event

The Regulations satisfaction-evaluated fact carries the Regulations-owned assessment result.

It may inform Trade Docs workflow, Trade/TMS enforcement or Pulse analytics after those consumers are authorised.

The event itself does not perform those consumers' state transitions.

---

## 19. Event Activation Is Deferred

event-surfaces.yaml records each event as:

~~~text
DEFINED_NOT_ACTIVATED
~~~

RTD-06 SHALL NOT create an AsyncAPI registration for these events and SHALL NOT add them to the platform event registry.

Activation belongs to:

~~~text
RTD-07 → documents producer/steward activation
RTD-08 → regulations context/platform event activation
~~~

This preserves explicit governance gates.

---

## 20. Existing Document Events

TradeDocument v2 already defines proposed document facts including:

~~~text
document-version.verification-changed.v2
document-version.validity-changed.v2
~~~

Once activated, Regulations may consume them as reassessment triggers.

A trigger means something material changed.

It does not itself determine that a requirement became satisfied or unsatisfied.

---

## 21. Reassessment Flow

~~~text
DocumentVersion verification/validity changes
                │
                ▼
          Trade Docs fact
                │
                ▼
 Regulations identifies linked requirement
                │
                ▼
       explicit reassessment
                │
                ▼
 RegulatoryEvidenceAssessment
                │
                ▼
 RegulatoryDecision may change
~~~

---

## 22. Supersession and Historical Replay

When a Regulations requirement changes:

- the old pinned reference remains historical;
- new workflows use the new requirement;
- existing workflows may be reassessed;
- old references are never rewritten.

When a new DocumentVersion exists:

- old assessments retain the old version reference;
- new assessments may cite the new version;
- historical results never silently point to latest.

If a pinned historical object cannot be resolved, the system SHALL NOT substitute current state.

---

## 23. Trusted Platform Context

All synchronous operations carry context_id.

The resource server must validate/redeem it against the authenticated caller under the Control Plane context-authority model.

context_id is not a bearer credential.

Every tenant-scoped nested CrossEngineObjectReference must match the trusted context tenant.

Ordinary RTD-06 operations do not permit cross-tenant exchange.

---

## 24. Security and Minimisation

Reference possession grants no access.

Trade Docs must authorise documentary retrieval.

Regulations must authorise requirement and assessment access.

Raw document bytes normally remain behind Trade Docs. The integration sends bounded facts and references rather than complete foreign aggregates.

Sensitive content must be retrieved only where needed and authorised.

---

## 25. Requirement/Decision Consistency

The Regulations runtime SHALL verify that the requirement reference is valid for the supplied pinned RegulatoryDecision.

JSON Schema cannot prove that semantic relationship.

A syntactically valid requirement from another decision is not accepted merely because its ID is well formed.

---

## 26. Documentary Assertion Semantics

Trade Docs SHALL preserve assertion origin.

Example:

~~~text
issuer states origin = UG
    → ISSUER_ASSERTED

OCR extracts origin = UG
    → BAOBAB_EXTRACTED
~~~

Those may ultimately agree, but they are not the same evidentiary proposition.

Regulations decides which form is sufficient under the applicable requirement.

---

## 27. Failure Semantics

The integration SHALL distinguish:

~~~text
document not found
owner unavailable
document unverified
document expired
requirement not found
requirement superseded
requirement/decision mismatch
tenant mismatch
assessment indeterminate
review required
~~~

Owner unavailable is not object absent.

Regulations unavailable is not legal prohibition.

Trade Docs unavailable is not documentary absence.

---

## 28. No Direct Database Coupling

This is prohibited:

~~~text
Regulations SELECT TradeDocs tables

TradeDocs SELECT Regulations tables
~~~

Resolution occurs through owner APIs, governed events/projections and capability/provider routing.

---

## 29. No Shadow Aggregates

Regulations SHALL NOT create a competing TradeDocument aggregate.

Trade Docs SHALL NOT create a competing DocumentRequirement or RegulatoryDecision aggregate.

A cache/projection may exist, but it retains owner/reference semantics and cannot become the new source of truth.

---

## 30. Existing Regulations v0 Events

baobab-regulations currently contains local draft audit schemas:

~~~text
regulations.evaluation.requested.v0
regulations.evaluation.completed.v0
~~~

RTD-06 does not promote those schemas by copying them into Shared.

They remain local draft artefacts until explicitly retired or replaced.

Cross-engine contracts use the canonical Shared envelope and naming model.

---

## 31. Regulations Event Naming Reconciliation

ADR-REG-0024 contains pre-Shared examples using:

~~~text
io.baobab.regulations.*
~~~

For platform wire contracts, that naming is superseded by ADR-SHARED-008 and ADR-SHARED-018:

~~~text
com.baobab-platform.regulations.*
~~~

The engine-local ADR/documentation must be amended accordingly.

---

## 32. Command/Event Separation

Good command:

~~~text
POST /documentary-evidence/assessments
~~~

Good fact:

~~~text
requirement-satisfaction.evaluated
~~~

Rejected:

~~~text
event: please-assess-documentary-evidence
~~~

Commands request work. Events state committed facts.

---

## 33. Idempotency, Correlation and Tracing

Evidence assessment requires Idempotency-Key.

Synchronous APIs support X-Correlation-ID and traceparent.

Once events are activated, they use the canonical Shared CloudEvents envelope and deduplicate delivery by source + id.

Exactly-once broker delivery is not assumed.

---

## 34. Capability Namespace Non-Decision

RTD-06 does not resolve the separate G-REG-NS capability namespace work.

The API contracts are provider-neutral wire contracts.

Capability registration, provider declaration and runtime binding remain separate architecture/activation tasks.

---

## 35. Deferred Trade Docs Domains

RTD-06 deliberately does not define:

- DocumentDossier;
- CustomsCase;
- CustomsDeclaration workflow;
- Submission aggregate;
- AuthorityResponse aggregate;
- transferable-record control;
- complete signature/trust architecture;
- document-generation contracts.

Those need later Trade Docs ADRs.

---

## 36. Minimum Conformance Proof

Before production use, conformance must prove at least:

1. pinned Regulations requirement resolves;
2. wrong-tenant requirement is denied;
3. pinned DocumentVersion resolves;
4. wrong-tenant DocumentVersion is denied;
5. CURRENT DocumentVersion reference is rejected;
6. evidence assessment requires idempotency;
7. caller cannot supply legal_time/knowledge_time;
8. verified document can still be UNSATISFIED;
9. expired document can trigger reassessment;
10. historical assessment retains exact DocumentVersion;
11. requirement supersession does not rewrite history;
12. no direct cross-engine database dependency exists;
13. extracted assertions retain their origin;
14. event surfaces remain unactivated until RTD-07/08.

---

## 37. Invariants

~~~text
INV-RTX-001 Regulations owns documentary requirement semantics.
INV-RTX-002 Trade Docs owns documentary object/version semantics.
INV-RTX-003 DocumentRequirement is not TradeDocument.
INV-RTX-004 DocumentVerification is not RequirementSatisfaction.
INV-RTX-005 EvidenceOffered is not EvidenceAccepted.
INV-RTX-006 Assessment commands are not disguised as events.
INV-RTX-007 Document evidence uses pinned DocumentVersion references.
INV-RTX-008 Requirements/decisions used for consequential workflow are pinned.
INV-RTX-009 Caller does not choose Regulations legal_time or knowledge_time.
INV-RTX-010 Documentary assertions preserve assertion origin.
INV-RTX-011 Extracted values do not automatically become issuer assertions.
INV-RTX-012 Trade Docs fact bundles contain no regulatory conclusion.
INV-RTX-013 Regulations assessment results contain no operational mutation.
INV-RTX-014 Tenant-scoped nested references match trusted/enclosing tenant.
INV-RTX-015 Reference possession grants no access.
INV-RTX-016 Historical pinned versions are never silently replaced with current state.
INV-RTX-017 Owner unavailability is not object absence.
INV-RTX-018 Requirement/decision consistency is validated by Regulations.
INV-RTX-019 Trade Docs does not reinterpret requirement legal meaning.
INV-RTX-020 Regulations does not create a shadow TradeDocument aggregate.
INV-RTX-021 No direct cross-engine database reads are authorised.
INV-RTX-022 Document validity change is a reassessment trigger, not a regulatory decision.
INV-RTX-023 Event subject does not replace RTD-05 references.
INV-RTX-024 Events carry minimum necessary facts/reference projections.
INV-RTX-025 RTD-06 event surfaces remain unregistered until RTD-07/08.
INV-RTX-026 Local Regulations v0 audit events are not promoted as platform contracts.
INV-RTX-027 Canonical platform event names use com.baobab-platform.*.
INV-RTX-028 Idempotency is required for evidence-assessment mutation.
INV-RTX-029 Regulatory outcome remains separate from operational enforcement.
INV-RTX-030 External sovereign authority is not transferred to either engine.
~~~

---

## 38. Rejected Alternatives

**Let Trade Docs decide compliance.** Rejected because documentary facts are not legal authority.

**Let Regulations own documents.** Rejected because that creates a competing document engine.

**Send complete PDFs in every event.** Rejected because it violates minimisation and turns transport into a content store.

**Use CURRENT document references for historical decisions.** Rejected because replay becomes nondeterministic.

**Treat verification as satisfaction.** Rejected because authentic/current evidence may still be legally insufficient.

**Publish assessment requests as events.** Rejected because commands and facts have different semantics.

**Activate events inside RTD-06.** Rejected because RTD-07/08 are explicit governance gates.

**Copy local Regulations v0 events into Shared.** Rejected because they predate canonical envelope/naming and the RTD authority split.

---

## 39. Consequences

### Positive

- Executable Regulations ↔ Trade Docs integration without shared persistence.
- Legal and documentary authorities remain explicit.
- Historical replay uses exact pinned references.
- Documentary extraction provenance survives transport.
- Events and commands remain distinct.
- RTD-07/08 can activate already-defined event semantics without redesign.
- RTD-10 can build cross-repository conformance tests against a stable contract.

### Costs

- More explicit API calls and reference handling.
- Consumers must distinguish unavailability from absence.
- Trade Docs must expose bounded documentary fact projections.
- Regulations must maintain requirement/evidence-assessment identity.
- Historical pinning requires retention discipline.
- Event activation is still separate work.

---

## 40. Final Decision

~~~text
Regulations
  decides what documentary proof is required
        │
        ▼
Trade Docs
  supplies exact document-version facts
        │
        ▼
Regulations
  decides whether those facts satisfy the requirement
        │
        ▼
Operational engine
  enforces its own business-state transition
~~~

> **Trade Docs supplies documentary truth; Regulations supplies regulatory meaning. RTD-05 references connect them, RTD-06 contracts choreograph them, and neither engine acquires the other's authority.**
