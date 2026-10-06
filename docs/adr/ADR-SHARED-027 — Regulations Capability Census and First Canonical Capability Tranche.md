# ADR-SHARED-027 — Regulations Capability Census and First Canonical Capability Tranche

**Status:** Accepted — Normative Capability Census Decision  
**Date:** 2026-10-06  
**Repository:** baobab-platform/shared  
**Decision ID:** ADR-SHARED-027  
**Implements:** First post-RTD capability census for the regulations namespace  
**Depends On:** ADR-SHARED-017, ADR-SHARED-019, ADR-SHARED-022, ADR-SHARED-024, ADR-SHARED-026  
**Refines:** ADR-SHARED-026 §16 and INV-RTD10-016  
**Semantic Owner:** baobab-regulations  
**Contract Authority:** baobab-platform/shared

> **R-CAP-07 follow-on — 2026-10-06:** The census-time prohibition in this ADR
> applied before a canonical implementation increment existed. R-CAP-01 through
> R-CAP-06 subsequently established the exact routes, contract proof, durable
> assessment state and canonical event outbox. RTD-10 now permits
> evidence-backed `PARTIAL` provider support for the two catalogued capability
> keys. This does not change their DRAFT/EXPERIMENTAL capability lifecycle,
> certify an implementation, or activate runtime support.

---

## 1. Decision

The first evidence-based census of baobab-regulations accepts exactly two
canonical Regulations capabilities:

~~~text
regulations.requirement.resolve
regulations.evidence.assess
~~~

Both are catalogued as:

~~~text
lifecycle = DRAFT
maturity  = EXPERIMENTAL
owner     = baobab-regulations
~~~

Both are **contracted capability vocabulary only**.

At the census date, baobab-regulations SHALL NOT declare provider support for
either capability.

---

## 2. Why These Two Capabilities Are Different

RTD-06 already created complete Shared-owned request and response contracts for:

~~~text
POST /documentary-requirements/resolve
POST /documentary-evidence/assessments
~~~

Therefore the platform already has stable provider-neutral semantics for two
specific things a Regulations provider may eventually do.

The census converts those existing contract surfaces into canonical capability
vocabulary. It does not invent a new runtime surface.

---

## 3. Capability Census Method

A proposed capability is evaluated across six evidence layers:

| Layer | Question |
|---|---|
| Authority | Is the bounded-context owner clear? |
| Semantics | Is the capability narrower than an engine/product name? |
| Shared contract | Is there a provider-neutral request/response contract? |
| Repository implementation | Does source code implement the canonical contract? |
| Tests | Is implementation behavior demonstrated? |
| Runtime claim | Is there an actual provider route/adapter worthy of provider support? |

Canonical vocabulary and provider implementation are separate decisions.

~~~text
canonical capability contract
        !=
provider implementation
        !=
provider certification
        !=
Control Plane activation
        !=
tenant entitlement
~~~

---

## 4. Census Results

| Capability | Prior state | Shared contract | Runtime evidence | Census verdict |
|---|---|---|---|---|
| regulations.requirement.resolve | implicit in RTD-06 | complete | no Regulations handler | **CONTRACTED / DRAFT** |
| regulations.evidence.assess | implicit in RTD-06 | complete | no canonical handler | **CONTRACTED / DRAFT** |
| regulations.context.resolve | PROPOSED | absent | partial scaffold; context-ID redemption explicitly unimplemented | remain **PROPOSED** |
| regulations.decision.evaluate | PROPOSED | absent | EvaluationService + offline ReferenceEvaluator + golden tests | remain **PROPOSED**; highest next contracting priority |
| regulations.change.subscribe | PROPOSED | absent | no subscription runtime | remain **PROPOSED** |
| regulations.pack.compose | PROPOSED | absent | no pack-composition runtime | remain **PROPOSED** |

No additional speculative capability key is created by this census.

---

## 5. regulations.requirement.resolve

### Meaning

Resolve one exact, already-established Regulations-owned documentary, permit or
evidence requirement projection under trusted tenant context.

### Canonical Shared contract

Request:

~~~text
regulatory-document-exchange/v1
  requirementResolveRequest
~~~

Response:

~~~text
regulatory-document-exchange/v1
  requirementResolveResponse
~~~

### Important exclusions

This capability is not:

~~~text
regulations.context.resolve
regulations.decision.evaluate
document creation
document verification
document workflow
broad legal applicability resolution
~~~

It resolves an exact pinned requirement; it does not discover the entire
applicable law for an arbitrary transaction.

---

## 6. regulations.evidence.assess

### Meaning

Assess bounded documentary facts and exact Trade Docs DocumentVersion references
against one pinned Regulations requirement.

### Canonical Shared contract

Request:

~~~text
documentEvidenceAssessmentRequest
~~~

Response:

~~~text
documentEvidenceAssessmentResult
~~~

Potential canonical fact event:

~~~text
com.baobab-platform.regulations.requirement-satisfaction.evaluated.v1
~~~

### Authority boundary

The capability owns the legal/regulatory sufficiency assessment.

It does not mutate:

~~~text
TradeDocument
DocumentVersion
CustomsCase
shipment
order
ERP state
~~~

Therefore:

~~~text
Trade Docs VERIFIED
        !=
Regulations SATISFIED
~~~

continues to hold.

---

## 7. Why lifecycle Is DRAFT

A capability can be canonical vocabulary without being available for runtime
resolution.

DRAFT is intentional because:

- Shared contracts exist;
- semantic ownership is clear;
- no baobab-regulations provider implements the exact capability contract yet;
- no provider support should be registered;
- no tenant should resolve the capability through the Control Plane yet.

The capability may move to ACTIVE only through later governed implementation and
activation work.

---

## 8. Why Provider Support Is Not Declared

Current baobab-regulations implementation has:

- domain aggregates;
- an EvaluationService;
- an offline ReferenceEvaluator;
- tenant/context guards;
- golden tests.

It does **not** yet have:

- the RTD-06 Regulations routes;
- exact request/response adapters for the new canonical capabilities;
- production OPA-backed evaluation;
- durable outbox/event publication for those operations;
- contract/integration tests proving those route contracts.

Therefore a providers[].support entry would be an overclaim.

The Regulations provider declaration SHALL instead list the two new canonical
keys under:

~~~text
planned_capabilities
proposal_status: CONTRACTED
~~~

until implementation evidence exists.

---

## 9. regulations.context.resolve Census Verdict

The proposal remains valid but is not contract-ready.

The live implementation explicitly supports inline tenant context and explicitly
rejects unresolved context-ID-only requests with:

~~~text
CONTEXT_REDEMPTION_NOT_IMPLEMENTED
~~~

The architectural target in ADR-REG-0017 is materially broader:

- trusted Control Plane context redemption;
- legal-entity resolution;
- actor roles;
- transaction geography;
- jurisdiction roles;
- regime membership;
- classifications;
- legal/knowledge time;
- fail-closed ambiguity.

The current implementation is therefore a scaffold, not an implementation of the
proposed capability.

Verdict:

~~~text
PROPOSED
not canonical
not provider support
~~~

---

## 10. regulations.decision.evaluate Census Verdict

This is the strongest uncontracted proposal.

Evidence exists for:

- RegulatoryDecision domain model;
- EvaluationService orchestration;
- deterministic ReferenceEvaluator;
- rule-set identifier input;
- legal/knowledge time;
- DecisionOutcome;
- RecommendedDisposition;
- golden-path tests;
- persistence port.

However the ReferenceEvaluator explicitly states that it is:

~~~text
not production OPA
offline scaffold / golden-case evaluator
~~~

and the current FastAPI surface exposes only health/readiness routes.

There is no Shared canonical general decision-evaluation request/response
contract.

Verdict:

~~~text
PROPOSED
next contracting priority
not canonical yet
not provider support
~~~

The next contracting increment SHOULD define a general provider-neutral
RegulatoryDecision evaluation contract before any provider support is claimed.

---

## 11. regulations.change.subscribe Census Verdict

ADR-REG-0023 and ADR-REG-0024 establish the architecture, but the repository
does not yet contain the runtime subscription/change-notification capability.

The RTD-08 Regulations events are specific documentary exchange facts; they are
not evidence that a general regulatory-change subscription capability exists.

Verdict:

~~~text
PROPOSED
not canonical
not implemented
~~~

---

## 12. regulations.pack.compose Census Verdict

ADR-REG-0029 describes jurisdiction/corridor/regime packs, but no pack composer
runtime is present.

The repository has a packs domain location but not an executable composition
capability with Shared request/response contracts.

Verdict:

~~~text
PROPOSED
not canonical
not implemented
~~~

---

## 13. Capability Naming Decision

The census rejects using generic capability names when the Shared contract is
narrower.

Rejected:

~~~text
regulations.decision.evaluate
~~~

as the canonical name for the RTD-06 evidence assessment contract.

Reason:

A general RegulatoryDecision evaluation capability is broader than assessing
one documentary requirement.

Accepted:

~~~text
regulations.evidence.assess
~~~

Likewise:

~~~text
regulations.requirement.resolve
~~~

is distinct from:

~~~text
regulations.context.resolve
~~~

This preserves composability and prevents a narrow contract from masquerading as
a broader implementation.

---

## 14. RTD-10 Evolution

ADR-SHARED-026 originally prohibited promotion of any regulations capability
because RTD-10 preceded this census.

That prohibition was intentionally temporary.

This ADR refines the rule:

~~~text
before capability census:
    no regulations capability promotion

after ADR-SHARED-027:
    canonical CONTRACTED capability keys are permitted
    only when present in Shared catalogue

still forbidden:
    premature providers[].support
    non-catalogued capability_key
    capability activation inferred from catalogue membership
~~~

The RTD-10 validator SHALL enforce this refined rule.

---

## 15. Provider Declaration State After Census

Target Regulations declaration:

~~~text
planned_capabilities:

  regulations.requirement.resolve
      proposal_status: CONTRACTED

  regulations.evidence.assess
      proposal_status: CONTRACTED

  regulations.context.resolve
      proposal_status: PROPOSED

  regulations.decision.evaluate
      proposal_status: PROPOSED

  regulations.change.subscribe
      proposal_status: PROPOSED

  regulations.pack.compose
      proposal_status: PROPOSED
~~~

No providers block is created by this census.

---

## 16. Capability Promotion Path

For each contracted capability:

~~~text
Shared canonical contract
        │
        ▼
planned CONTRACTED
        │
        ▼
runtime adapter implementation
        │
        ▼
contract tests
        │
        ▼
provider support PARTIAL
        │
        ▼
complete implementation evidence
        │
        ▼
provider support IMPLEMENTED
        │
        ▼
EA-09 certification
        │
        ▼
Control Plane registration / activation
        │
        ▼
bindings + grants + resolution
~~~

RTD-10 and the catalogue must never collapse these phases.

---

## 17. Next Regulations Contracting Priority

The next recommended capability-contract increment is:

~~~text
regulations.decision.evaluate
~~~

because its domain/application implementation is materially ahead of the other
uncontracted proposals.

Before canonicalization it needs, at minimum:

1. provider-neutral Shared request/response schemas;
2. trusted context-reference semantics;
3. rule-set/version semantics;
4. legal-time and knowledge-time requirements;
5. deterministic replay/idempotency semantics;
6. regulatory outcome vs technical error separation;
7. explicit evidence/provenance references;
8. no operational enforcement mutation;
9. OpenAPI surface;
10. contract examples and conformance tests.

---

## 18. Non-Goals

This census does not:

- certify baobab-regulations;
- activate any capability;
- create a provider;
- declare production readiness;
- implement OPA;
- implement Control Plane context redemption;
- implement change subscriptions;
- implement jurisdiction-pack composition;
- expand Trade Docs ownership;
- make Pulse part of the evaluation path.

---

## 19. Invariants

~~~text
REG-CAP-001
Catalogue membership defines canonical capability vocabulary.

REG-CAP-002
Canonical capability vocabulary does not imply provider implementation.

REG-CAP-003
regulations.requirement.resolve is narrower than regulations.context.resolve.

REG-CAP-004
regulations.evidence.assess is narrower than regulations.decision.evaluate.

REG-CAP-005
No provider support is declared for the first contracted tranche at census time.

REG-CAP-006
Only Shared-contract-backed capability semantics are promoted by this census.

REG-CAP-007
The offline ReferenceEvaluator is evidence of partial implementation direction,
not evidence of a production provider.

REG-CAP-008
RTD-08 event activation does not prove regulations.change.subscribe.

REG-CAP-009
Trade Docs verification remains distinct from Regulations evidence satisfaction.

REG-CAP-010
Control Plane remains authority for provider activation, bindings, grants and resolution.
~~~

---

## 20. Final Decision

> **The first Regulations capability census promotes only the two narrow capabilities whose provider-neutral Shared contracts already exist: requirement resolution and documentary-evidence assessment. Everything broader remains proposed until its contract and implementation evidence are equally explicit.**
