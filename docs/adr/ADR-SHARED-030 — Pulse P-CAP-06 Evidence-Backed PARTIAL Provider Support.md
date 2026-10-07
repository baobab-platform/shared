# ADR-SHARED-030 — Pulse P-CAP-06 Evidence-Backed PARTIAL Provider Support

**Status:** Accepted — Normative Provider-Promotion Governance  
**Date:** 2026-10-07  
**Repository:** `baobab-platform/shared`  
**Decision ID:** ADR-SHARED-030  
**Depends On:** ADR-SHARED-017, ADR-SHARED-025, ADR-SHARED-026, ADR-SHARED-029  
**Applies To:** `baobab-platform/baobab-pulse` P-CAP-06  
**Refined By:** ADR-SHARED-031 (P-CAP-07 IMPLEMENTED readiness authority)

## 1. Decision

ADR-SHARED-029 intentionally prohibited provider support at the first Pulse
capability census and defined a staged promotion path ending in:

```text
canonical contract
  -> CONTRACTED intent
  -> exact adapter
  -> authenticated/context-bound authority
  -> durability/idempotency
  -> tests
  -> PARTIAL
  -> IMPLEMENTED
  -> certification
  -> activation
```

P-CAP-03 through P-CAP-05 have now supplied the repository implementation
evidence needed to enter the PARTIAL stage.

Shared therefore permits `baobab-pulse` to declare one or more first-party
providers with `PARTIAL` support for exactly the two capabilities accepted by
the first census:

```text
intelligence.evidence.search
intelligence.research-mission.manage
```

This decision does not change either capability's canonical contract, lifecycle
or maturity.

## 2. What this supersedes

ADR-SHARED-029 remains the historical and semantic authority for the first
Intelligence capability census.

This ADR supersedes only the temporary invariant:

> "At the census date, Pulse SHALL NOT declare provider support."

That sentence described the census-time state and the deliberate P-CAP-02
ceiling. It was never intended to permanently prevent the later P-CAP-06 stage
that ADR-SHARED-029 itself names.

The resulting chronology is:

```text
ADR-SHARED-029 / P-CAP-01..02
    provider support = forbidden

P-CAP-03..05
    implementation evidence accumulates

ADR-SHARED-030 / P-CAP-06
    PARTIAL support = permitted
    IMPLEMENTED     = forbidden
```

## 3. Permitted provider-support state

During P-CAP-06, RTD-10 permits only:

```yaml
providers:
  - provider_key: baobab-pulse.<provider>
    support:
      - capability_key: intelligence.evidence.search
        implementation_status: PARTIAL
        implementation_evidence: [...]

      - capability_key: intelligence.research-mission.manage
        implementation_status: PARTIAL
        implementation_evidence: [...]
```

The declaration must remain valid under the canonical
`provider-declaration.schema.json` and the general capability-catalogue
validator.

## 4. RTD-10 promotion rules

The Shared-owned RTD-10 conformance validator SHALL enforce all of the
following for P-CAP-06.

| Rule | Requirement |
|---|---|
| Provider ownership | every provider key begins `baobab-pulse.` |
| Canonical vocabulary | every supported capability exists in Shared catalogue |
| Census boundary | support is limited to the two ADR-SHARED-029 capabilities |
| Status ceiling | every support entry is exactly `PARTIAL` |
| Evidence | every support entry carries non-empty implementation evidence |
| Evidence existence | every declared evidence path exists in Pulse repository |
| No dual state | a capability cannot be both planned and provider support |
| Complete tranche | once a provider block is present, both first-census capabilities are represented |
| Namespace | proposed future capabilities still remain under `intelligence.*` |

These rules are cross-repository governance, not a local Pulse override.

## 5. Why PARTIAL is justified

### 5.1 intelligence.evidence.search

Repository evidence now includes:

- exact Shared v1 contract models/tests;
- authenticated canonical HTTP route;
- provider-neutral workload-authentication boundary;
- caller-bound Control Plane context redemption;
- rejection of caller-selected tenant authority;
- rejection of caller-selected classification authority;
- canonical PostgreSQL EvidenceSet hydration;
- Qdrant only as a rebuildable semantic projection;
- stale/orphan projection checks;
- live PostgreSQL + Qdrant integration proof.

### 5.2 intelligence.research-mission.manage

Repository evidence now includes:

- exact Shared v1 CREATE/GET contract models/tests;
- authenticated/context-bound canonical route;
- durable PostgreSQL ResearchMission persistence;
- structural tenant isolation;
- idempotent CREATE semantics;
- semantic replay conflict detection;
- mutation audit provenance;
- transactional held-event candidate persistence;
- concurrent duplicate convergence;
- live PostgreSQL integration proof.

This evidence exceeds CONTRACTED intent and meets the meaning of PARTIAL
implementation support in ADR-SHARED-017.

## 6. Why IMPLEMENTED remains forbidden

P-CAP-06 is not the full provider-readiness decision.

Current evidence still shows material gaps, including:

1. the module-level Pulse ASGI application starts without a configured
   `CapabilityApiRuntime`;
2. production IAM workload-authentication adapter wiring is not demonstrated;
3. production Control Plane context-authority adapter wiring is not demonstrated;
4. canonical evidence search is conservatively capped at TENANT classification
   until an explicit higher-classification authority contract exists;
5. the ResearchMission Intelligence event is stored only as
   `HELD_UNREGISTERED`;
6. EA-09 certification has not occurred;
7. Control Plane provider registration/activation/binding/grants have not
   occurred.

Therefore RTD-10 SHALL reject `IMPLEMENTED` for either capability during
P-CAP-06.

## 7. No runtime-registration implication

Shared's capability tooling already follows the required separation:

```text
PARTIAL provider support
        |
        X  generate-registration
        |
        v
not registrable as IMPLEMENTED support
```

Only `IMPLEMENTED` support is eligible for transitional EngineRegistration
generation.

Thus P-CAP-06 cannot accidentally activate Pulse by changing its declaration.

## 8. No event activation

This ADR does not change ADR-SHARED-025's event-context decision.

The `intelligence` event context remains RESERVED unless and until a separate
Shared event-registration decision establishes a stable producer contract and
real consumer.

The local held candidate:

```text
com.baobab-platform.intelligence.research-mission.created.v1
```

remains non-publishable.

## 9. No certification or Control Plane authority

A provider declaration answers only:

> what canonical capability does this repository implement, to what repository
> implementation status, and with what evidence?

It does not answer:

- whether the provider is certified;
- whether any EngineInstance exists;
- whether support is ACTIVE;
- whether a tenant has a binding or grant;
- whether an endpoint is healthy;
- whether runtime resolution may select the provider.

EA-09 and Control Plane remain authoritative for those facts.

## 10. Future transition

P-CAP-07 is the next governed step.

A future Shared decision may permit `IMPLEMENTED` only after a fresh review of
the remaining readiness gaps. P-CAP-07 must not infer readiness merely because
P-CAP-06 is PARTIAL.

P-CAP-08 remains the earliest certification/registration/activation stage.

## 11. Invariants

**INT-PROMO-001**  
P-CAP-06 support may reference only canonical Shared Intelligence capabilities.

**INT-PROMO-002**  
P-CAP-06 may support only the two first-census capabilities.

**INT-PROMO-003**  
P-CAP-06 provider support is exactly PARTIAL.

**INT-PROMO-004**  
Every PARTIAL support claim carries repository-local implementation evidence.

**INT-PROMO-005**  
PARTIAL support is not certification, activation, binding, grant, routing or
health.

**INT-PROMO-006**  
A capability cannot simultaneously be planned CONTRACTED intent and declared
provider support.

**INT-PROMO-007**  
P-CAP-06 does not activate an Intelligence producer event.

**INT-PROMO-008**  
IMPLEMENTED requires the later P-CAP-07 readiness decision.

## 12. Final decision

> Pulse has now earned repository-level PARTIAL support for the two canonical
> Intelligence capabilities created by ADR-SHARED-029. Shared RTD-10 therefore
> advances from the census-time no-support rule to an evidence-backed PARTIAL
> ceiling, while continuing to reject IMPLEMENTED support, event activation,
> certification and runtime activation until their own governed increments.
