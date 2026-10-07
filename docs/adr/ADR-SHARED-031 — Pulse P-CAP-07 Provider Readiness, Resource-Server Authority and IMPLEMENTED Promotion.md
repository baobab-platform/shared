# ADR-SHARED-031 — Pulse P-CAP-07 Provider Readiness, Resource-Server Authority and IMPLEMENTED Promotion

**Status:** Accepted — Normative Provider-Readiness Governance  
**Date:** 2026-10-07  
**Repository:** `baobab-platform/shared`  
**Decision ID:** ADR-SHARED-031  
**Depends On:** ADR-SHARED-017, ADR-SHARED-025, ADR-SHARED-026, ADR-SHARED-029, ADR-SHARED-030  
**Applies To:** `baobab-platform/baobab-pulse` P-CAP-07

## 1. Decision

P-CAP-07 is the full repository provider-readiness decision for the first
canonical Intelligence tranche.

Shared permits `baobab-pulse.core` to promote:

- `intelligence.evidence.search@1`
- `intelligence.research-mission.manage@1`

from `PARTIAL` to `IMPLEMENTED` only after Pulse demonstrates all of the
following against this Shared revision:

1. a production-capable logical HTTP composition root;
2. a concrete provider-neutral resource-server authenticator;
3. a concrete caller-bound Control Plane context-validation adapter;
4. exact route-level Intelligence scope enforcement;
5. explicit classification-clearance enforcement;
6. durable canonical persistence where the contract mutates state;
7. source, contract-test and integration-test evidence for both capabilities.

`IMPLEMENTED` remains a repository implementation statement only.

It is not:

- EA-09 certification;
- CapabilityProvider activation;
- ProviderCapabilitySupport runtime activation;
- an EngineInstance;
- a CapabilityBinding;
- a CapabilityGrant;
- health;
- deployment observation;
- tenant entitlement; or
- permission for production traffic.

Those remain later authorities, beginning with P-CAP-08.

## 2. Why P-CAP-06 was not sufficient

ADR-SHARED-030 correctly stopped at `PARTIAL`.

At that point Pulse had canonical routes and durable domain behavior, but the
production trust path still had four gaps:

```text
external caller token
       |
       X no concrete Pulse resource-server verifier
       |
       v
Pulse capability route
       |
       X no registered Pulse validator relationship
       |
       v
Control Plane PlatformContext validation
       |
       X default ASGI composition had no CapabilityApiRuntime
       |
       v
capability service
       |
       X classification authority stopped at TENANT
```

P-CAP-07 closes those repository-readiness gaps without collapsing
implementation, certification and activation into one state.

## 3. Trust model

The permanent inbound trust model is:

```text
                    IAM / token authority
                           |
                 signed access token
                 aud = baobab-pulse
                           |
                           v
                 +-------------------+
                 |  Baobab Pulse     |
                 | resource server   |
                 +-------------------+
                    |             |
          verifies caller      retains subject token
          issuer/aud/scopes           |
                    |                 |
                    |                 v
                    |       baobab-pulse-workload
                    |       aud=baobab-control-plane
                    |       scope=context:validate
                    |                 |
                    |                 v
                    |       +----------------------+
                    +------>| Baobab Control Plane |
                            | context validation    |
                            +----------------------+
                                      |
                                      v
                             trusted tenant/context
                                      |
                                      v
                             capability execution
```

Two authenticated principals participate:

| Principal | Purpose | Authority |
|---|---|---|
| subject caller | invokes a Pulse capability | operation/classification scopes on `aud=baobab-pulse` |
| `baobab-pulse-workload` | asks CP to validate the subject's context | `context:validate` on `aud=baobab-control-plane` |

They are deliberately not the same credential.

The Pulse workload must never substitute its own tenant or principal for the
subject whose context is being redeemed.

## 4. Pulse becomes a registered context validator

Shared changes the canonical workload entry for:

`baobab-pulse-workload`

to permit:

`context:validate`

and registers:

`validates_audiences: [baobab-pulse]`

This means the Pulse workload may present to the Control Plane only subject
tokens whose resource-server audience is the registered Pulse audience.

It does not let Pulse choose an arbitrary audience in the request.

The validation request remains exactly:

```json
{
  "context_id": "...",
  "subject_token": "..."
}
```

The Control Plane independently verifies the subject token and binds it to the
stored context owner.

## 5. Intelligence operation scopes

P-CAP-07 introduces the canonical resource-server scopes:

| Scope | Audience | Meaning |
|---|---|---|
| `intelligence:evidence:search` | `baobab-pulse` | invoke `intelligence.evidence.search` |
| `intelligence:research-mission:manage` | `baobab-pulse` | invoke `intelligence.research-mission.manage` |
| `intelligence:restricted` | `baobab-pulse` | supplemental RESTRICTED classification clearance |

The operation scopes are necessary but not sufficient.

They grant no tenant selection.

Every canonical Pulse request still requires a caller-bound PlatformContext.

## 6. Classification authority

P-CAP-07 resolves the P-CAP-06 classification ceiling without adding a
Pulse-specific field to generic PlatformContext.

Authority is composed as follows:

```text
validated PlatformContext
        +
exact capability scope
        +
optional intelligence:restricted
        =
effective Pulse invocation authority
```

The classification ceiling is:

| Token authority | Maximum Intelligence classification |
|---|---|
| no exact capability scope | no invocation |
| exact capability scope | CONFIDENTIAL |
| exact capability scope + `intelligence:restricted` | RESTRICTED |

PUBLIC, BAOBAB_INTERNAL and TENANT are naturally below CONFIDENTIAL.

`intelligence:restricted` has no independent operation meaning. A token
holding only that scope cannot search evidence or manage a ResearchMission.

This avoids two unsafe alternatives:

- trusting a request body field such as `requester_clearance`;
- treating tenant membership or a generic context as implicit RESTRICTED
  clearance.

## 7. Authentication requirements

A conforming Pulse production resource-server adapter must fail closed unless
the subject token proves at least:

- accepted signature;
- trusted configured issuer;
- `aud=baobab-pulse`;
- subject;
- issued-at and expiry;
- bounded token lifetime;
- token identifier;
- `actor_type=workload`;
- the exact capability scope required by the route.

Provider-native realm/session constructs are not canonical authority.

Pulse may implement these checks through a standards-based OIDC/JWKS adapter.
That does not make Keycloak, Hydra, Kratos or another identity product part of
the canonical capability contract.

## 8. Context validation requirements

A conforming Pulse Control Plane adapter must:

1. authenticate as `baobab-pulse-workload`;
2. request a token for `baobab-control-plane` with `context:validate`;
3. call the canonical PlatformContext validation operation;
4. send the actual caller's subject token only in the POST body;
5. never log, persist, trace or audit that subject token;
6. treat foreign, expired or unavailable contexts fail closed;
7. use only CP-returned tenant/context facts for capability execution.

A caller-supplied `X-Baobab-Tenant-Id` remains non-authoritative.

## 9. Capability-specific readiness

### 9.1 intelligence.evidence.search

An IMPLEMENTED provider must demonstrate:

```text
authenticated token
  -> exact evidence-search scope
  -> caller-bound CP context
  -> derived classification ceiling
  -> tenant-scoped semantic retrieval
  -> canonical PostgreSQL hydration
  -> stale/orphan filtering
  -> Shared-v1 response
```

Qdrant remains a rebuildable retrieval projection and cannot become evidence
authority.

### 9.2 intelligence.research-mission.manage

An IMPLEMENTED provider must demonstrate:

```text
authenticated token
  -> exact research-mission scope
  -> caller-bound CP context
  -> derived classification ceiling
  -> CREATE / GET
       |
       +-- CREATE:
       |      idempotency
       |      mission persistence
       |      audit
       |      HELD event candidate
       |
       +-- GET:
              structural tenant filter
              classification filter
```

A GET above the caller's classification ceiling must not disclose existence.

## 10. Provider declaration requirements

Once Pulse consumes this P-CAP-07 authority, RTD-10 requires both first-census
capabilities to be:

`implementation_status: IMPLEMENTED`

The provider must also be:

- non-simulated;
- `production_permitted: true`;
- equipped with a logical HTTP invocation reference owned by
  `baobab-pulse`;
- backed for each capability by at least source, contract-test and
  integration-test evidence.

The logical invocation reference is not a hostname, deployment or routing
record.

## 11. IMPLEMENTED is not ACTIVE

The state separation remains:

```text
Pulse repository
IMPLEMENTED
    |
    | P-CAP-08 / EA-09
    v
CERTIFIED
    |
    | Control Plane governed registration/activation
    v
Provider support ACTIVE
    |
    | binding + grant + instance + health
    v
RESOLVABLE
```

P-CAP-07 stops at the first box.

## 12. Intelligence event remains held

P-CAP-07 does not activate the reserved Intelligence producer event context.

The local ResearchMission candidate:

`com.baobab-platform.intelligence.research-mission.created.v1`

remains `HELD_UNREGISTERED`.

This is not a blocker to IMPLEMENTED for
`intelligence.research-mission.manage@1` because the canonical capability
contract declares no required event schema.

Publishing that candidate would require its own Shared event-governance
decision and a demonstrated consumer contract.

## 13. Capability lifecycle and maturity remain separate

This ADR does not automatically change:

```text
capability lifecycle = DRAFT
capability maturity  = EXPERIMENTAL
```

Those are properties of the canonical capability contract.

`IMPLEMENTED` is a provider repository implementation status.

The three concepts remain independent.

## 14. Cross-repository sequencing

P-CAP-07 must be implemented in this order:

```text
1. Shared
   scopes + workload validator relation + RTD readiness authority
        |
        v
2. Control Plane
   consume Shared registry so Pulse validator is recognized
        |
        v
3. IAM
   consume Shared registry; issue/configure Pulse validator and resource scopes
        |
        v
4. Pulse
   production adapters + composition + classification enforcement
   + IMPLEMENTED declaration
```

Pulse must not merge its IMPLEMENTED claim before the upstream authority changes
it relies on have merged.

## 15. No automatic consumer grants

Defining Pulse resource-server scopes does not allocate them to every existing
workload.

P-CAP-07 establishes the provider trust boundary.

Which Trade, Digital Estate, orchestration or other workload receives a Pulse
capability scope is a separate consumer/integration decision.

This prevents a provider-readiness increment from silently expanding caller
authority.

## 16. RTD-10 contract pins

An Intelligence consumer/provider claiming P-CAP-07 readiness must pin, in
addition to the existing Intelligence and RTD contracts:

- `contracts/authorization/v1/scope-registry.yaml`
- `contracts/identity/v1/workload-registry.yaml`

This makes the exact authority vocabulary and validator relationship part of the
reviewable Pulse contract lock.

## 17. Rejected alternatives

### Put classification clearance in PlatformContext

Rejected. PlatformContext is cross-platform tenant/context authority, not a
container for every engine's data-classification policy.

### Accept requester_clearance in the capability body

Rejected. It would let the caller select its own authority.

### Infer RESTRICTED from tenant membership

Rejected. Tenant membership is not sufficient evidence for the highest
classification.

### Let Pulse trust its own tenant header

Rejected. Tenant authority remains Control Plane-owned.

### Mark IMPLEMENTED before production adapters exist

Rejected. That would repeat the overclaim P-CAP-06 was designed to prevent.

### Activate the ResearchMission event as part of readiness

Rejected. Event activation has independent producer/consumer governance and is
not required by the v1 capability contract.

## 18. Invariants

**INT-READY-001**  
Pulse subject tokens are accepted only for the registered
`baobab-pulse` audience.

**INT-READY-002**  
The exact capability scope is required for each canonical operation.

**INT-READY-003**  
Caller-selected tenant and classification authority are forbidden.

**INT-READY-004**  
Pulse validates context ownership through the Control Plane using the actual
subject token.

**INT-READY-005**  
Base capability scope permits classifications through CONFIDENTIAL only after
successful caller-bound context validation.

**INT-READY-006**  
RESTRICTED additionally requires `intelligence:restricted`.

**INT-READY-007**  
ResearchMission GET never discloses an object above the caller's effective
classification ceiling.

**INT-READY-008**  
Both first-census capabilities must be IMPLEMENTED together under P-CAP-07.

**INT-READY-009**  
Each IMPLEMENTED claim carries source, contract-test and integration-test
evidence.

**INT-READY-010**  
IMPLEMENTED is not certification, activation, health, binding, grant or
resolvability.

**INT-READY-011**  
P-CAP-07 does not publish a previously held Intelligence event.

**INT-READY-012**  
No existing caller receives a new Pulse capability scope merely because this
provider becomes ready.

## 19. Final decision

> P-CAP-07 closes the first Pulse provider's repository-readiness gap by making
> resource-server authentication, caller-bound Control Plane context
> validation, route authority and classification clearance explicit,
> provider-neutral and machine-testable. Once those paths are implemented and
> evidenced, the two first-census capabilities may be declared IMPLEMENTED.
> Certification and runtime activation remain P-CAP-08.
