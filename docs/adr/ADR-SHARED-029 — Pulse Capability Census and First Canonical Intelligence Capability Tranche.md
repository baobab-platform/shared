# ADR-SHARED-029 — Pulse Capability Census and First Canonical Intelligence Capability Tranche

**Status:** Accepted — Normative Capability Census Decision  
**Date:** 2026-10-07  
**Repository:** `baobab-platform/shared`  
**Decision ID:** ADR-SHARED-029  
**Implements:** First post-RTD capability census for the `intelligence` namespace  
**Depends On:** ADR-SHARED-017, ADR-SHARED-019, ADR-SHARED-021, ADR-SHARED-025, ADR-SHARED-026  
**Semantic Owner:** `baobab-pulse`  
**Contract Authority:** `baobab-platform/shared`

---

## 1. Decision

The first evidence-based census of `baobab-pulse` accepts exactly two
canonical Intelligence capabilities:

```text
intelligence.evidence.search
intelligence.research-mission.manage
```

Both are catalogued as:

```text
lifecycle = DRAFT
maturity  = EXPERIMENTAL
owner     = baobab-pulse
```

At the census date, **Pulse SHALL NOT declare provider support for either
capability**.

The canonical contract exists first. Provider implementation is a separate,
later claim.

---

## 2. Why these two capabilities

The earlier EA-02B candidate review reserved these exact keys after finding
consumer-facing Pulse routes and provider-neutral local models.

The current census revalidates them against the live repository and the newer
RTD-09/RTD-10 cross-engine architecture.

| Candidate | Repository evidence | Census verdict |
|---|---|---|
| `intelligence.evidence.search` | real route, application service, semantic retrieval port, PostgreSQL canonical hydration, Qdrant projection | **CONTRACTED / DRAFT** |
| `intelligence.research-mission.manage` | real domain aggregate and create/get route, but intentionally minimal/in-memory verification slice | **CONTRACTED / DRAFT** |
| RTD-09 upstream fact projection | durable consumer/projection boundary for Regulations and Trade Docs facts | **Not a capability** |
| Haystack pipeline execution | anti-corruption implementation detail | **Not a capability** |
| Qdrant vector projection | rebuildable retrieval projection | **Not a capability** |
| model/embedding execution | replaceable infrastructure port | **Not a capability** |
| signals, trends, anomalies, risks, opportunities, forecasts, recommendations, intelligence products | domain concepts exist to varying degrees; no proven consumer contract/runtime surface | **Defer** |

No speculative third capability is created.

---

## 3. Census method

Each candidate is tested against the ADR-SHARED-017 capability criteria:

```text
consumer-facing
contractable
grantable/composable
replaceable
testable
auditable
provider-neutral
bounded by clear semantic authority
```

The census also applies a seventh practical distinction learned from the
Regulations census:

```text
route exists
    !=
canonical contract implemented
    !=
production-worthy provider support
```

---

## 4. intelligence.evidence.search

### Meaning

Search the authorised intelligence evidence corpus and return canonical evidence
identities with retrieval freshness.

### Existing implementation evidence

Pulse already contains:

- `POST /evidence/search`;
- `EvidenceRetrievalService`;
- `SemanticRetrievalPort`;
- PostgreSQL-backed canonical EvidenceSet hydration;
- Qdrant as a retrieval projection rather than canonical evidence authority;
- stale/orphan projection checks.

That is substantial implementation evidence.

### Why provider support is still not declared

The live HTTP scaffold still binds tenant context from a caller-provided
`X-Baobab-Tenant-Id` header, and its local request accepts
`requester_clearance`.

Those are unsuitable as canonical trust semantics.

The Shared v1 contract therefore deliberately removes both authority selectors.

A conforming provider must derive:

```text
tenant scope
principal authority
classification clearance
capability entitlement
```

from authenticated platform context.

Until Pulse implements and tests that exact boundary, claiming canonical provider
support would overstate the runtime.

### Provider neutrality

The canonical contract exposes:

```text
canonical_object_id
evidence_set_id
retrieval score
staleness
```

and never:

```text
Qdrant point id
vector
embedding
Haystack type
model provider
```

The retrieval score is explicitly **not** Pulse confidence, evidence quality or
regulatory sufficiency.

---

## 5. intelligence.research-mission.manage

### Meaning

Create or retrieve a governed ResearchMission that frames an intelligence
question and its scope/classification/confidence requirements.

### Existing implementation evidence

Pulse already has:

- a first-class `ResearchMission` aggregate;
- lifecycle states from PROPOSED through PUBLISHED/SUSPENDED/CANCELLED and
  insufficient-evidence/supersession outcomes;
- local request/response models;
- `POST /research-missions`;
- `GET /research-missions/{id}`;
- a `ResearchMissionService` behind a PipelinePort.

### Why provider support is still not declared

The repository itself describes this HTTP surface as a minimal verification
slice.

The research-mission repository is currently in-memory, and the reference
research pipeline explicitly exists to prove the architecture rather than to be
the first production research product.

Therefore:

```text
domain model     yes
route            yes
canonical contract now yes
canonical provider support no
```

The contract is intentionally modest: CREATE and GET. It does not pretend that
the full planned mission lifecycle is implemented as a durable external
capability.

---

## 6. RTD-09 does not create more capabilities

ADR-SHARED-025 and RTD-09 establish Pulse as an asynchronous consumer of facts
owned by Regulations and Trade Docs.

```text
Regulations facts ─┐
                   ├──► Pulse projection ─► Pulse analysis
Trade Docs facts ──┘
```

The projection is not a consumer-invoked business ability.

It does not become:

```text
intelligence.regulations.consume
intelligence.trade-docs.project
intelligence.fact.ingest
```

merely because code exists.

Those names would leak integration plumbing into the canonical capability
catalogue.

---

## 7. Authority boundaries with other engines

The census preserves the following ownership.

| Concern | Authority |
|---|---|
| Tenant, PlatformContext, capability resolution | Control Plane |
| Human/workload authentication | IAM |
| Commerce/order operational truth | Trade |
| ERP/accounting operational truth | ERP |
| Content publication truth | CMS |
| Regulatory applicability, legal sufficiency, RegulatoryDecision | Regulations |
| TradeDocument / DocumentVersion lifecycle and document verification | Trade Docs |
| Intelligence evidence, research and derived intelligence | Pulse |

Pulse may reference upstream facts and derive intelligence from them.

It does not rewrite their authority.

---

## 8. Regulations is not an intelligence sub-capability

The recent Regulations capability programme now has canonical:

```text
regulations.requirement.resolve
regulations.evidence.assess
regulations.decision.evaluate
```

Pulse SHALL NOT duplicate those as:

```text
intelligence.regulatory.query
intelligence.regulatory.assess
intelligence.regulatory.decide
```

when the semantic act belongs to Regulations.

Pulse may analyse the resulting facts and decisions asynchronously.

---

## 9. Research/analysis domain concepts remain future candidates

Pulse's domain contains richer concepts such as:

```text
Observation
Signal
Trend
Anomaly
Analysis
Insight
Opportunity
Risk
Forecast
Recommendation
DecisionRecord
IntelligenceProduct
```

Their existence does not automatically create one capability per aggregate.

A later census may promote a capability only when there is a real external
consumer act, a Shared contract and implementation evidence at a useful
granularity.

This prevents a catalogue that merely mirrors class names.

---

## 10. Haystack, Qdrant and model providers are implementation details

ADR-PULSE-010 deliberately places Haystack behind an anti-corruption layer.

Therefore these are invalid canonical capability identities:

```text
haystack.pipeline.execute
qdrant.semantic.search
openai.analysis.generate
pulse.pipeline.run
```

The valid boundary is:

```text
intelligence business capability
        │
        ▼
Pulse application port
        │
        ▼
replaceable implementation
```

---

## 11. Capability contract design

### 11.1 Evidence search

Request:

```text
query_text
evidence_set_id?
top_k?
```

Trusted authority is deliberately absent from the request.

Response:

```text
candidates[]
  canonical_object_id
  evidence_set_id
  score
  is_stale
```

### 11.2 Research mission management

The initial contract has two bounded operations:

```text
CREATE
GET
```

This expresses the implemented external acts without pretending the entire
ResearchMission lifecycle is externally manageable today.

---

## 12. Provider declaration after census

The target Pulse declaration is:

```yaml
planned_capabilities:
  - capability_key: intelligence.evidence.search
    proposal_status: CONTRACTED

  - capability_key: intelligence.research-mission.manage
    proposal_status: CONTRACTED
```

There is no `providers[].support` block from this census.

---

## 13. Promotion path

```text
Shared canonical contract
        │
        ▼
Pulse planned CONTRACTED
        │
        ▼
exact canonical route/adapter
        │
        ▼
IAM-authenticated + CP-bound trusted context
        │
        ▼
durability/idempotency where the operation requires it
        │
        ▼
contract/integration tests
        │
        ▼
provider support PARTIAL
        │
        ▼
provider support IMPLEMENTED
        │
        ▼
EA-09 certification
        │
        ▼
Control Plane activation/binding/grants
```

Catalogue membership never skips these phases.

---

## 14. Invariants

**INT-CAP-001**  
Canonical intelligence capability keys use the `intelligence` namespace, never
`pulse`.

**INT-CAP-002**  
Pulse provider identity and Haystack/Qdrant/model technology never define
capability identity.

**INT-CAP-003**  
RTD-09 upstream fact projections are consumer plumbing, not capabilities.

**INT-CAP-004**  
A Pulse-derived intelligence object does not transfer authority over its source
object.

**INT-CAP-005**  
Evidence-search similarity score is not intelligence confidence, evidentiary
quality or regulatory sufficiency.

**INT-CAP-006**  
Caller-selected tenant or clearance values are not canonical authority.

**INT-CAP-007**  
The first census declares no provider support.

**INT-CAP-008**  
ResearchMission existence does not imply full lifecycle capability support.

**INT-CAP-009**  
Signals, risks, opportunities and forecasts are not catalogued merely because
domain classes exist.

**INT-CAP-010**  
Pulse never duplicates Regulations, Trade Docs, Trade, ERP, CMS, IAM or Control
Plane authority under an `intelligence.*` alias.

---

## 15. Next implementation increments

Recommended sequence:

```text
P-CAP-01  Shared census/contract (this ADR)
P-CAP-02  Pulse CONTRACTED provider declaration + contract pin
P-CAP-03  authenticated/context-bound canonical evidence.search adapter
P-CAP-04  durable canonical research-mission repository + adapter
P-CAP-05  idempotency/audit/event semantics for mutation operations
P-CAP-06  evidence-backed PARTIAL provider declaration
P-CAP-07  full provider-support/readiness decision
P-CAP-08  EA-09 certification and CP registration/activation
```

A later capability census should occur only after additional consumer-facing
intelligence services actually exist.

---

## 16. Final decision

> **The first Pulse capability census promotes only the two consumer-facing,
> provider-neutral abilities already reserved by EA-02B: evidence search and
> research-mission management. It deliberately refuses to turn Pulse domain
> classes, Haystack pipelines, Qdrant projections or RTD-09 upstream projections
> into capabilities. Canonical contract comes first; provider support must be
> earned separately.**
