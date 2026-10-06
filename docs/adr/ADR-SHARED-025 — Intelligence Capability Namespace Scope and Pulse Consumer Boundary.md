# ADR-SHARED-025 — Intelligence Capability Namespace Scope and Pulse Consumer Boundary

**Status:** Accepted — Normative Namespace and Consumer-Boundary Governance  
**Date:** 2026-10-06  
**Repository:** `baobab-platform/shared`  
**Decision ID:** ADR-SHARED-025  
**Decision Type:** Capability Namespace / Event Context Reservation / Cross-Engine Consumer Boundary  
**Implements:** Shared side of RTD-09 from ADR-SHARED-019  
**Depends On:** ADR-SHARED-007, ADR-SHARED-018, ADR-SHARED-019, ADR-SHARED-021, ADR-SHARED-023, ADR-SHARED-024  
**Initial Engine:** `baobab-pulse`

---

## 1. Decision

The canonical capability domain for Baobab intelligence is:

```text
intelligence
```

not:

```text
pulse
```

`baobab-pulse` is an engine/provider identity. `intelligence` is the business-capability namespace.

The namespace covers:

- evidence and research;
- observations;
- analysis;
- signals, trends and anomalies;
- risk and opportunity;
- forecasting and scenarios;
- recommendations;
- intelligence products.

It is intentionally provider-neutral and SHALL NOT encode Haystack, Qdrant, a model provider or any other implementation technology.

---

## 2. Namespace Status

The `intelligence` namespace already exists in Shared and remains registered.

RTD-09 refines its scope; it does not create a second namespace.

The following relationship is canonical:

```text
capability namespace
    intelligence
        │
        └── intended initial provider
                baobab-pulse
```

This does not make Pulse permanently exclusive. Another engine may later implement a catalogued intelligence capability if governance permits it.

---

## 3. No Capability Promotion

RTD-09 SHALL NOT add an `intelligence.*` capability to the canonical Shared catalogue merely because the namespace exists.

```text
namespace registered
    !=
capability catalogued
    !=
provider contracted
    !=
provider implemented
    !=
provider activated
    !=
tenant entitled
```

Capability discovery and promotion require a later implementation census.

Examples already appearing in earlier architecture prose such as:

```text
intelligence.fx.query
intelligence.commodity.query
intelligence.route-risk.assess
intelligence.regulatory.query
intelligence.risk.assess
```

remain illustrative until separately catalogued through ADR-SHARED-007 governance.

---

## 4. Why Not `pulse.*` Capabilities

Repository/service names describe implementation ownership.

Capability names describe reusable business ability.

Therefore:

```text
baobab-pulse
    implements/provides
intelligence.<resource>.<action>
```

is valid.

```text
pulse.<resource>.<action>
```

is rejected as a canonical capability namespace.

---

## 5. Event Context Reservation

RTD-09 reserves the future event context:

```text
intelligence
```

with:

```text
status   = RESERVED
steward  = baobab-pulse
domain   = intelligence
```

No event type is activated by this decision.

This is deliberate:

```text
RESERVED intelligence context
        │
        ├── no producer event registered
        ├── no AsyncAPI activated
        └── no runtime publisher claim
```

---

## 6. Why Reserve the Event Context Now

Pulse already contains local event scaffolding using repository-oriented names such as:

```text
com.baobab-platform.pulse.*
```

The platform event model requires business-context-oriented naming.

Future canonical Pulse-owned events SHOULD therefore use:

```text
com.baobab-platform.intelligence.<fact>.vN
```

once their payloads and consumers are proven.

RTD-09 reserves this context before production publication so the platform does not later need to migrate a repository-named `pulse` event family.

---

## 7. No `pulse` Event Context

Shared SHALL NOT register an event context named:

```text
pulse
```

The service name remains valid in logical producer identity:

```text
urn:baobab-platform:service:baobab-pulse
```

but not as the canonical business context segment.

---

## 8. RTD-09 Is Consumer-Side

RTD-09 makes Pulse a consumer/projection engine for active facts already owned by:

```text
baobab-regulations
baobab-trade-docs
```

The synchronous regulatory/documentary path remains:

```text
Trade / TMS
     │
     ▼
Regulations
     ↔
Trade Docs
     │
     ▼
Operational PEP
```

Pulse observes asynchronously:

```text
Regulations events ─┐
                    ├──► Pulse projection/evidence ─► Analysis
Trade Docs events ──┘
```

Pulse SHALL NOT become a required hop on the enforcement path.

---

## 9. Consumed Authorities

Pulse may consume, among other active facts:

### Regulations

```text
com.baobab-platform.regulations.document-requirements.determined.v1
com.baobab-platform.regulations.requirement-satisfaction.evaluated.v1
```

### Trade Docs

```text
com.baobab-platform.documents.document-version.verification-changed.v2
com.baobab-platform.documents.document-version.validity-changed.v2
com.baobab-platform.documents.regulatory-evidence.offered.v1
```

RTD-09 does not transfer ownership of any referenced object to Pulse.

---

## 10. Cross-Engine References

All portable upstream object identity SHALL follow ADR-SHARED-021.

Pulse projections preserve:

- `owner_engine_id`;
- `object_type`;
- `object_id`;
- reference mode/version pinning;
- tenant scope.

Pulse SHALL NOT convert a Regulations or Trade Docs identifier into a locally-owned canonical identity.

---

## 11. Projection Is Not Authority

A Pulse read/projection record is a derived analytical view.

```text
Pulse projection of RegulatoryDecision
    !=
RegulatoryDecision
```

```text
Pulse projection of DocumentVersion validity
    !=
DocumentVersion validity authority
```

Upstream owner references and source-event identity SHALL survive projection.

---

## 12. Minimal Projection Rule

Pulse SHOULD project only what is needed for intelligence:

- event occurrence identity;
- producing engine;
- event type/time;
- tenant;
- owner-preserving references;
- small analytical state code where useful;
- digest/provenance needed for idempotency/replay.

Pulse SHOULD NOT copy complete foreign aggregates merely to simplify local querying.

---

## 13. Evidence Semantics

Pulse may use an upstream reference as analytical evidence.

The relationship means:

> this upstream fact supports, contradicts or contextualises a Pulse analytical claim.

It does not mean:

> Pulse owns or legally validates the upstream object.

---

## 14. Event Delivery and Idempotency

Consumers SHALL assume at-least-once delivery.

A Pulse projection consumer MUST deduplicate using the canonical event occurrence identity:

```text
(source, id)
```

Receiving the same event again SHALL not create a second analytical fact.

Receiving the same occurrence identity with materially different payload digest SHALL fail closed as a provenance conflict.

---

## 15. Tenant Isolation

For tenant-scoped events:

```text
event tenant
    =
projection tenant
    =
nested tenant-scoped CrossEngineObjectReference tenant
```

A mismatch SHALL be rejected.

Pulse SHALL never use an event to bypass tenant isolation.

---

## 16. Source Authenticity

Pulse SHALL whitelist canonical producer/type pairs for upstream facts.

Examples:

```text
regulations.* RTD-08 facts
    producer = baobab-regulations

documents.* RTD-07 facts
    producer = baobab-trade-docs
```

A syntactically valid event type from the wrong logical producer SHALL be rejected.

---

## 17. No Synchronous Dependency

Pulse consumer/projection code SHALL not call Regulations or Trade Docs synchronously merely to make the event consumable.

If additional authoritative detail is needed for later analysis, it may be obtained through an explicit authorised workflow; enforcement SHALL not wait on Pulse.

---

## 18. Failure Isolation

```text
Pulse down
    !=
Regulations down

Pulse projection stale
    !=
document invalid

Pulse Qdrant unavailable
    !=
regulatory evidence unavailable
```

Regulatory/documentary execution remains independent of Pulse availability.

---

## 19. Qdrant and Haystack

Qdrant remains a rebuildable semantic projection.

Haystack remains an embedded, replaceable orchestration dependency.

Neither technology defines:

- the intelligence namespace;
- cross-engine reference identity;
- event authority;
- regulatory truth;
- documentary truth.

---

## 20. Future Pulse-Produced Events

RTD-09 does not activate them.

Candidate future facts may include:

```text
intelligence.observation.published
intelligence.insight.published
intelligence.risk.identified
intelligence.opportunity.detected
intelligence.forecast.published
intelligence.recommendation.published
```

Each requires:

1. stable canonical payload;
2. proven producer semantics;
3. real consumer;
4. Shared registration;
5. event-context activation decision.

---

## 21. Capability Census

A later capability census SHALL inspect the live Pulse implementation before cataloguing any `intelligence.*` key.

Possible capability areas include:

- evidence retrieval;
- research execution;
- semantic retrieval;
- analysis;
- forecasting;
- risk assessment;
- opportunity detection;
- recommendation generation.

These are categories for investigation, not approved capability names.

---

## 22. Invariants

```text
INV-INT-001
The canonical capability domain is intelligence, not pulse.

INV-INT-002
baobab-pulse is an engine/provider identity, not a capability namespace.

INV-INT-003
RTD-09 catalogues no intelligence capability.

INV-INT-004
The intelligence event context is RESERVED, not ACTIVE.

INV-INT-005
No intelligence event type is registered by RTD-09.

INV-INT-006
No pulse event context is registered.

INV-INT-007
Pulse consumes Regulations/Trade Docs asynchronously.

INV-INT-008
Pulse is never required for regulatory/documentary enforcement.

INV-INT-009
Upstream canonical references preserve owner identity.

INV-INT-010
Pulse projections are not foreign canonical aggregates.

INV-INT-011
Pulse Evidence may reference upstream facts without transferring authority.

INV-INT-012
Canonical producer/type pairs are validated on ingestion.

INV-INT-013
Tenant-scoped references match event tenant.

INV-INT-014
At-least-once delivery is deduplicated by source + event id.

INV-INT-015
Occurrence identity with conflicting payload fails closed.

INV-INT-016
Haystack/Qdrant are implementation details, not namespace semantics.

INV-INT-017
Future intelligence events require separate activation.

INV-INT-018
Capability promotion requires live implementation evidence.
```

---

## 23. Final Decision

```text
Shared namespace
    intelligence
        │
        └── intended initial provider
                baobab-pulse

Shared event context
    intelligence
        status = RESERVED
        steward = baobab-pulse
        events = none

Runtime RTD-09
    Regulations ─┐
                 ├──► Pulse read projections / analytical evidence
    Trade Docs ──┘

Enforcement path
    unchanged and Pulse-free
```

> **Pulse is the intelligence engine, but the platform namespace is intelligence. RTD-09 reserves future ownership without inventing capabilities or producer events, and makes Pulse a downstream analytical consumer rather than an enforcement dependency.**
