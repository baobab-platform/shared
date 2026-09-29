# Baobab Platform  
## Enterprise Architecture Production-Readiness Assessment

**Assessment date:** 25 September 2026  
**Architecture scope:** Baobab Platform ecosystem  
**Primary organisation:** `baobab-platform`  
**Assessment basis:** Current repository state on `main`, current accepted ADRs, current Shared contracts, CI state, open PRs, runtime implementation, cross-engine boundaries and prior Baobab architecture decisions.

---

# 1. Executive Summary

Baobab has progressed beyond an architectural prototype.

The platform now contains credible implementations of its central architectural ideas:

- canonical cross-engine contracts;
- a substantial Control Plane;
- workload identity;
- canonical organisation, tenant, market and capability modelling;
- deterministic capability resolution;
- independent engine databases;
- provider abstraction;
- transactional event patterns;
- governed organisation admission;
- subscription classification;
- dedicated subscription-billing and payment engines;
- a strong ERP anti-corruption boundary;
- multi-tenant commerce;
- a headless CMS;
- an intelligence/evidence engine;
- reusable polyglot CI;
- a coherent production-infrastructure architecture.

The architecture itself is therefore **not the principal problem**.

The principal problem has shifted to **enterprise convergence and operational closure**.

The present state can be represented as:

```text
                         BAOBAB PLATFORM
                               │
              ┌────────────────┴────────────────┐
              │                                 │
              ▼                                 ▼
        DESIGN AUTHORITY                  RUNTIME AUTHORITY
     baobab-platform/shared               baobab-cp
              │                                 │
              │                         Organisation / Tenant
              │                         Capability / Context
              │                         Provisioning / Routing
              │                                 │
              └────────────────┬────────────────┘
                               │
                  ┌────────────┼────────────┐
                  │            │            │
                  ▼            ▼            ▼
                IAM          Trade          ERP
                  │            │            │
                  ├────────────┼────────────┤
                  │            │            │
                  ▼            ▼            ▼
                CMS          Pulse     Subscriptions
                                            │
                                            ▼
                                         Payments

                               │
                               ▼
                        Infrastructure
                   ─────────────────────
                    architecture: strong
                    implementation: partial
```

The central enterprise-architecture conclusion is:

> **Baobab no longer requires fundamental redesign. It requires disciplined convergence of contracts, identity, runtime topology, infrastructure, observability, operational governance and engine certification.**

The platform should not yet be described as production-ready as a whole.

Several repositories are individually well engineered, but production readiness is a **system property**, not a collection of Dockerfiles and green CI pipelines.

The missing closed loop is:

```text
Canonical Contract
      │
      ▼
Engine Release
      │
      ▼
Approved Deployment
      │
      ▼
Engine Instance
      │
      ▼
Observed Health
      │
      ▼
Capability Resolution
      │
      ▼
Business Execution
      │
      ▼
Events / Telemetry
      │
      ▼
Reconciliation
      │
      ▼
Readiness / Drift
      │
      └──────────────► Control Plane
```

Baobab has pieces of this loop.

It does not yet have the complete loop operating consistently across all engines.

---

# 2. Assessment Method

This assessment distinguishes five architectural states.

| Level | Meaning |
|---|---|
| **L1 — Concept** | ADR/design exists but meaningful runtime implementation does not |
| **L2 — Foundation** | Runnable scaffold or significant core implementation exists |
| **L3 — Integrated** | Real integration with other Baobab components exists |
| **L4 — Pre-production** | Architecture is substantially complete but operational certification remains |
| **L5 — Production-ready** | Deployment, security, observability, DR, runbooks and runtime integration are proven |

The progress bars below are **architectural judgements**, not calculated percentages.

```text
Shared                 ████████░░  L4
Control Plane runtime  ████████░░  L4
CP governance plane    ████░░░░░░  L2
CP frontend            ██░░░░░░░░  L1
IAM                    ███████░░░  L3½
Trade                  ███████░░░  L3½
ERP                    ██████░░░░  L3
CMS                    ██████░░░░  L3
Pulse                  █████░░░░░  L2½
Subscriptions          █████░░░░░  L2½
Payments               ████░░░░░░  L2
Infrastructure         ████░░░░░░  L2
baobab-dev             ████████░░  L4
engine-template        ████░░░░░░  L2
────────────────────────────────────
PLATFORM OVERALL       ██████░░░░  ≈ L3
```

The most important interpretation of this chart is that **architecture and repository engineering are considerably more mature than production operations**.

---

# 3. Fresh Shared Audit — Including PR #98

## 3.1 Current state

The fresh audit found current Shared `main` at:

```text
b62fd5d66c...
```

PR #98 was merged at:

```text
4fc0ecd622...
```

and was immediately followed by:

```text
9a4f4f6250  chore(release): version shared packages
b62fd5d66c  Merge changeset release
```

Current important Shared workflows are green:

| Workflow | State |
|---|---|
| Foundation Repository Gates | PASS |
| Code Quality | PASS |
| Version Shared Packages | PASS |
| CI at PR #98 merge | PASS |

There are currently **no open Shared PRs**.

Shared now contains approximately:

```text
28 contract domains
329 contract files
```

including:

```text
identity
authorization
capability
product
subscriptions
payments
organisation
admission
control-plane
ERP
trade
procurement
shipment
supplier onboarding
buyer organisation
legal entity
infrastructure
events
```

This is a substantial canonical contract estate.

---

# 4. Shared PR #98 — Architectural Significance

PR #98 is more significant than an ordinary contract addition.

It formalises the missing governance boundary between:

```text
APPROVAL
```

and:

```text
PROVISIONING
```

The canonical flow is now:

```text
ClientApplication
      │
      ▼
AdmissionDecision
      │
      │ APPROVED
      ▼
TenantOnboardingRequest
      │
      ├── REQUESTED
      │
      ▼
   AUTHORISED
      │
      ▼
   FULFILLED
      │
      ▼
Tenant Provisioning
      │
      ▼
Readiness
      │
      ▼
Activation
```

The critical invariant is:

```text
APPROVED ≠ PROVISIONED ≠ READY ≠ ACTIVE
```

That distinction is enterprise-grade and should be preserved everywhere.

PR #98 establishes:

| Concern | Rule |
|---|---|
| Requester | Cannot be the applicant or admission decider |
| Authoriser | Cannot be the requester or applicant |
| Decision | Immutable |
| Desired state | Derived substantially from the AdmissionDecision |
| Classification | Cannot be changed by onboarding requester |
| Markets | Cannot silently widen beyond approved scope |
| Products | Cannot silently change |
| Live requests | At most one per AdmissionDecision |
| Fulfilment | Records tenant creation but does not activate it |
| Events | Canonical `tenant-onboarding.*` events |
| Authorization | Dedicated `onboarding:request` and `onboarding:authorise` scopes |

This significantly improves the admission architecture.

---

# 5. Important CP Correction Following PR #98

The previous audit treated the onboarding handoff as largely unimplemented.

That is no longer accurate.

Current CP includes:

```text
TenantOnboardingRequest domain
PostgreSQL persistence
request service
authorisation service
API handlers
scoped routes
audit
canonical events
separation-of-duty tests
```

Routes include:

```text
POST /v1/tenant-onboarding-requests

POST /v1/tenant-onboarding-requests/{id}/authorisation

POST /v1/tenant-onboarding-requests/{id}/fulfilment

POST /v1/tenant-onboarding-requests/{id}/cancellation
```

This is real implementation.

However, CP's own decision log still identifies a material remaining gap:

> Tenant registration does not yet require an AUTHORISED TenantOnboardingRequest.

The architecture therefore currently permits two conceptual paths:

```text
CORRECT TARGET

APPROVED
   │
   ▼
REQUESTED
   │
   ▼
AUTHORISED
   │
   ▼
Tenant Provisioning
```

and potentially:

```text
LEGACY / DIRECT PATH

Tenant Registration
       │
       └────────► provisioning
```

The second path must eventually be closed or strictly limited to explicit migration/bootstrap scenarios.

---

# 6. Shared — Strengths, Weaknesses and Required Enhancements

## Strengths

Shared is one of Baobab's strongest repositories.

It provides:

- canonical JSON Schema;
- OpenAPI;
- AsyncAPI;
- CloudEvents profile;
- identity contracts;
- capability contracts;
- admission lifecycle;
- organisation model;
- subscription classification;
- billing and payment contracts;
- engine registration schema;
- reusable Foundation CI;
- action pinning;
- dependency governance;
- contract publication;
- package versioning;
- polyglot CI infrastructure.

The contract-first model is sound:

```text
ADR
 │
 ▼
Shared Contract
 │
 ▼
Engine Implementation
 │
 ▼
Consumer Contract Tests
```

## Weakness

The largest Shared problem is no longer Shared itself.

It is **consumer adoption**.

Current contract lag against Shared `main` is:

| Consumer | Shared commits behind |
|---|---:|
| CP | **2** |
| Subscriptions | **11** |
| Payments | **17** |
| IAM | **235** |
| Trade | **264** |
| ERP | **264** |
| Pulse | **264** |
| CMS | **No lock** |

The CP lag is low risk because the two commits are release/versioning commits after PR #98.

The remaining figures are not.

## Critical recommendation

Introduce a **Contract Currency SLO**.

For example:

```text
Critical engines:
Shared drift must never exceed an approved compatibility window.

Contract-changing Shared PR
        │
        ▼
Compatibility impact calculated
        │
        ▼
Consumer update PRs generated
        │
        ▼
Contract suites executed
        │
        ▼
Consumers converge
```

CI should expose contract currency as a platform metric.

---

# 7. Engine Registration — Fresh Shared Finding

Shared now has a generic:

```text
EngineRegistration
```

contract and CP consumes it generically.

That is excellent.

However, only:

```text
subscriptions/v1/capabilities.json
payments/v1/capabilities.json
```

currently exist.

Trade, ERP, CMS, Pulse and IAM do **not** yet publish equivalent `capabilities.json` manifests.

This leaves Baobab in an inconsistent state:

```text
NEW ENGINES
Subscriptions / Payments
       │
       ▼
generic EngineRegistration

LEGACY CORE ENGINES
Trade / ERP / CMS / Pulse / IAM
       │
       ▼
historical/manual registration patterns
```

This should be normalised.

Every engine should eventually publish:

```text
EngineDefinition
├── engine_key
├── repository
├── capabilities[]
├── provider
├── contract support
├── workload identity
├── supported isolation
├── residency characteristics
├── health contract
├── dependencies
└── operational metadata
```

The current Shared registration schema is a good start but does not yet fully represent an operational engine.

---

# 8. Target Engine Model

The enterprise model should distinguish:

```text
ENGINE
  │
  ├── logical product/runtime type
  │
  ▼
ENGINE RELEASE
  │
  ├── version
  ├── image digest
  ├── SBOM
  ├── contracts
  ├── provenance
  └── migration requirements
  │
  ▼
ENGINE INSTANCE
  │
  ├── environment
  ├── region
  ├── residency
  ├── isolation
  ├── endpoint
  └── release
  │
  ▼
HEALTH OBSERVATION
  │
  ├── checked_at
  ├── expires_at
  ├── status
  ├── latency
  └── reasons
```

These concepts should not be conflated.

---

# 9. Control Plane — Runtime Assessment

## Strengths

CP is now a substantial runtime.

Current major capabilities include:

```text
Organisation
LegalEntity
CorporateRelationship
CorporateGroup
PlatformRelationship
PlatformAccount
Tenant
Market
MarketParticipation
DigitalEstate
CanonicalEntity
ExternalReference
Mapping
Context
Product
ProductSubscription
Capability
CapabilityGrant
CapabilityProvider
ProviderCapabilitySupport
CapabilityBinding
Engine
EngineInstance
IsolationProfile
Provisioning
Readiness
Admission
TenantOnboardingRequest
Subscription classification
Billing projection reconciliation
```

Its resolver enforces significant constraints around:

```text
tenant
scope
contract compatibility
instance lifecycle
environment
region
residency
isolation
health
effective dates
binding
```

CP CI is currently healthy:

```text
Go CI                     PASS
Foundation Repository     PASS
Security                  PASS
Code Quality              PASS
```

No CP PRs are currently open.

## Strength: generic provider registration

CP can consume Shared `capabilities.json` manifests and create:

```text
Engine
Capability
CapabilityProvider
ProviderCapabilitySupport
```

without special-casing an engine by name.

This is exactly the correct direction.

---

# 10. Control Plane — Runtime Gaps

## 10.1 EngineInstance lifecycle is incomplete

CP models EngineInstance but lacks a complete operational governance API around:

```text
register instance
activate instance
drain instance
maintenance
fail instance
retire instance
```

## 10.2 EngineRelease is not first-class enough

Production requires:

```text
Engine
   │
   ▼
EngineRelease
   │
   ▼
EngineInstance
```

The deployed image/version must become explicit platform state.

## 10.3 Health observation is incomplete

ADR-BCP-006 correctly says health is ephemeral.

Current implementation instead primarily persists:

```text
EngineInstance.health_status
```

without a first-class:

```text
HealthObservation
├── checked_at
├── expires_at
├── source
├── latency
└── reason
```

The current resolver accepts:

```text
ACTIVE + UNKNOWN health
```

as eligible.

That is too weak for critical capabilities.

Target policy:

```text
PAYMENT EXECUTION
      │
      ▼
Recent HEALTHY observation?
      │
  ┌───┴───┐
  │       │
 YES      NO
  │       │
  ▼       ▼
allow   fail closed
```

Read-only intelligence may tolerate degraded health.

Payment authorisation should not.

Health tolerance must therefore be **capability-specific**.

---

# 11. CP Special-Case Routing Must Be Temporary

CP's new billing projector is well designed in many respects:

- contract validation;
- idempotency;
- retry/backoff;
- authoritative revision;
- billing-policy verification;
- reconciliation.

But it currently targets:

```text
BILLING_ENGINE_URL
```

directly.

Target architecture must instead become:

```text
CP
 │
 ▼
Resolve:
billing.subscription.manage
 │
 ▼
CapabilityBinding
 │
 ▼
CapabilityProvider
 │
 ▼
EngineInstance
 │
 ▼
Subscriptions
```

Direct endpoint configuration may remain as a bootstrap mechanism.

It should not become normal production engine discovery.

---

# 12. CP Administrative Governance Plane

This remains the largest functional CP gap.

Accepted ADRs describe:

```text
AdministrativePermission
AdministrativeScope
AdministrativeGrant
Delegation
Separation of Duties

ChangeIntent
Changeset
ImpactAnalysis
ChangePlan
ApprovalDecision
ExecutionOperation

EvidenceClaim
EvidenceRecord
EvidenceSource
VerificationCase
VerificationCheck
ComplianceAssessment
```

Current runtime search still finds little or no implementation of the generic:

```text
AdministrativeGrant
Changeset
ChangePlan
ExecutionOperation
EvidenceClaim
VerificationCase
```

model.

Existing administrative operations instead rely heavily on historical scopes and platform-admin role checks.

That is acceptable during transition.

It is not the target architecture.

---

# 13. CP Controlled-Mutation Target

High-impact changes should follow:

```text
Business Intent
      │
      ▼
ChangeIntent
      │
      ▼
Changeset
      │
      ▼
Validation
      │
      ▼
Impact Analysis
      │
      ▼
Immutable Plan
      │
      ▼
Risk Classification
      │
      ▼
Approval
      │
      ▼
Durable Operation
      │
      ▼
Desired State
      │
      ▼
Reconciliation
      │
      ▼
Readiness
      │
      ▼
Verification
      │
      ▼
Complete
```

The approval must bind to the exact plan digest.

A modified plan must invalidate its earlier approval.

---

# 14. CP Frontend — Current State

ADR-BCP-019 is accepted and detailed.

There is currently:

```text
no frontend/ directory
```

in `baobab-cp`.

Therefore CP frontend maturity remains **L1 — architecture defined, implementation not started**.

That frontend is not optional long term.

Baobab has reached a level of platform complexity at which:

```text
curl
SQL
manual Keycloak operations
developer scripts
GitHub-only administration
```

cannot safely remain the primary platform-operation experience.

---

# 15. CP Frontend — Required Architecture

The repository target remains:

```text
baobab-cp/
├── api/
├── cmd/
├── internal/
│
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   ├── components/
│   │   ├── features/
│   │   ├── server/
│   │   └── generated/control-plane/
│   ├── tests/
│   ├── package.json
│   ├── next.config.ts
│   └── Dockerfile
│
└── ...
```

The existing Go layout should **not** be moved under `/backend`.

One repository should contain multiple independently deployable components.

---

# 16. CP Frontend Technology Baseline

The accepted baseline remains:

| Concern | Decision |
|---|---|
| Runtime | Node.js 24 LTS |
| Framework | Next.js Active LTS |
| React | Stable line |
| Language | TypeScript strict |
| Package manager | pnpm |
| Router | App Router |
| Rendering | Server-first |
| Authentication | BFF-mediated OIDC |
| Testing | Unit + integration + Playwright |
| Accessibility | WCAG 2.2 AA |
| Observability | OpenTelemetry compatible |

This remains technically sound.

As of this audit, Node 24 is an LTS release, and the Node project recommends production applications stay on supported LTS lines.

Next.js 16 is currently Active LTS; Next.js itself recommends production use of an Active or Maintenance LTS major rather than canary releases.

---

# 17. CP Frontend Security Model

The browser must never become an administrative security boundary.

Target:

```text
Browser
   │
   │ secure HttpOnly session
   ▼
CP Console BFF
   │
   │ server-side OAuth token custody
   ▼
Control Plane API
   │
   │ final authorization
   ▼
CP Domain
```

Avoid:

```text
localStorage privileged access token
sessionStorage privileged access token
generic BFF proxy
browser-supplied actor ID
browser-supplied organisation authority
```

A hidden UI control is not authorization.

Every consequential command must be authorised again by CP.

---

# 18. CP Console Information Architecture

Recommended top-level IA:

```text
Home

Applications

Organisations
Corporate Structure
Platform Accounts

Tenants
Markets
Services
Digital Estates

People & Access

Changes
Approvals

Provisioning
Operations
Readiness

Activity
Audit

Diagnostics

Settings
```

The interface should use progressive disclosure.

### Level 1 — Business view

```text
Organisation
Market
Service
Status
Readiness
Issue
Required action
```

### Level 2 — Administration

```text
Tenant
Subscription
Capability
Scope
Isolation
Residency
Approvals
```

### Level 3 — Diagnostics

```text
Provider
EngineInstance
Binding
Contract version
Resolution trace
Correlation ID
Drift
Health observation
```

Most business administrators should rarely need Level 3.

---

# 19. CP Console Experiences

Three distinct experiences should coexist.

```text
                       CP CONSOLE
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
      Applicant       Platform Ops     Organisation Admin
      Workspace        Workspace          Workspace
```

### Applicant workspace

```text
registration
application
organisation claims
legal evidence
market requirements
product requirements
status
information requests
```

### Platform Operations

```text
review
verification
admission
corporate structure
PlatformAccount
onboarding
tenants
capabilities
changesets
approvals
operations
readiness
audit
```

### Organisation Administration

```text
organisation profile
permitted tenant configuration
markets
Digital Estates
delegated administration
readiness
audit within scope
```

---

# 20. CP Frontend Recommended Implementation Sequence

The frontend should **not** be built as a giant UI before the governance APIs exist.

Recommended sequence:

```text
F0  Contract/admin API foundation
     │
F1  frontend/ skeleton
     │
F2  BFF + IAM login/session
     │
F3  Applicant workspace
     │
F4  Admission/onboarding operator workflow
     │
F5  Organisation / corporate structure
     │
F6  Tenants / markets / PlatformAccounts
     │
F7  Administrative grants
     │
F8  Changesets / approvals
     │
F9  Operations / readiness / reconciliation
     │
F10 Audit / diagnostics
     │
F11 accessibility / performance / security hardening
```

The first real vertical slice should be:

```text
Applicant
   │
   ▼
Application
   │
   ▼
Claims / Evidence
   │
   ▼
Review
   │
   ▼
AdmissionDecision
   │
   ▼
TenantOnboardingRequest
   │
   ▼
Authorisation
   │
   ▼
Provisioning
   │
   ▼
Readiness
```

---

# 21. IAM Assessment

## Strengths

IAM has a mature architectural foundation around Keycloak.

Implemented areas include:

```text
identity authority
OIDC/OAuth
workload identity
workforce SSO
privileged MFA
client definitions
engine integration
identity lifecycle
revocation
security events
backup architecture
incident-response runbooks
```

Current CI is green.

## Weaknesses

IAM remains **235 Shared commits behind**.

That is the largest concern after operational testing.

## Critical production gap: immutable image

Current upstream lock contains:

```text
Keycloak 26.7.4
digest = UNRESOLVED
```

That is explicitly not a valid production pin.

It must be replaced by a real immutable digest before release.

## Operational gaps

IAM's own production-hardening record correctly acknowledges:

```text
penetration testing          not performed
cross-buyer isolation        partial
general HTTP rate limiting   external/infrastructure
DR exercise                  not performed
load testing                 not performed
login-storm capacity test    not performed
incident drill               not performed
```

The repository is refreshingly honest.

Those tests now need execution rather than further ADR writing.

---

# 22. Missing Workload Identities for New Engines

Shared's canonical workload registry currently contains identities for:

```text
CMS
ERP
Pulse
Trade
Thamani
ZuriBeans
```

but not:

```text
Subscriptions
Payments
```

This conflicts with the new runtime architecture.

Target call chain:

```text
Control Plane
     │
     │ workload token
     ▼
Subscriptions
     │
     │ workload token
     ▼
Payments
```

Subscriptions currently expects:

```text
aud = baobab-subscriptions
caller = baobab-control-plane
```

Payments expects:

```text
aud = baobab-payments
caller = baobab-subscriptions
```

But the existing `baobab-control-plane` client is bearer-only and does not have a service account, while `baobab-subscriptions` does not yet have its own workload client.

This must be solved as a coherent S2S identity design.

Recommended pattern:

```text
baobab-cp-workload
baobab-subscriptions-workload
baobab-payments-workload
```

with explicit audiences/scopes and separate identities from browser/workforce clients.

---

# 23. Trade Assessment

## Strengths

Trade is the most developed business engine.

It includes:

```text
MedusaJS 2.x
Node 24 runtime policy
tenant-context integration
Control Plane client
mapping resolution
market resolution
workload-token support
workforce OIDC
ZuriBeans buyer OIDC
B2B module
Thamani module
inventory bridge
payment bridge
fulfilment bridge
tax bridge
ERP integration
trade readiness
transactional outbox
security testing
tenant isolation tests
production conformance
release readiness
```

The repository has one of the strongest production-control manifests in Baobab.

Current CI is green across:

```text
CI
Security
Release Readiness
Foundation
Code Quality
```

## Weaknesses

### Contract lag

```text
264 Shared commits behind
```

This is too large for a platform core engine.

### Identity integration is optional

Trade's workload-token integration is technically sound but remains opt-in.

A production engine should not silently operate without its canonical CP workload identity.

### Readiness depth

Production readiness should include dependency facts such as:

```text
PostgreSQL
Redis
CP
IAM
ERP bridge
event backbone
critical providers
```

rather than merely configuration presence.

### Open stacked integration work

Current open draft stack:

```text
#85–#98
```

covering ZB-04 buyer onboarding, CP verification, invitations, ERP projection, KYB and certification.

This is substantial unmerged state.

The stack should be reconciled against the newer generic organisation/admission model before final merge.

---

# 24. Trade Recommended Enhancements

1. Update to current Shared contracts.
2. Reconcile the ZB-04 PR stack against ADR-BCP-018/024.
3. Require workload identity in production.
4. Publish Trade `capabilities.json`.
5. Register Trade through generic EngineRegistration.
6. Expose richer `/health/ready`.
7. Standardise event publication through the common broker.
8. Add production-grade provider certification for:
   - payment;
   - fulfilment;
   - tax;
   - search;
   - inventory integrations.
9. Complete real cross-engine certification against CP + ERP + IAM.
10. Remove obsolete `nabhold/*` repository references where they are namespace drift rather than stable package identifiers.

---

# 25. ERP Assessment

## Strengths

ERP has some of the best architectural discipline in Baobab.

Its design correctly treats iDempiere as a vendor platform behind a Baobab boundary.

The repository includes:

```text
iDempiere runtime
OSGi extensions
Baobab application layer
tenant mapping
canonical mapping
provisioning
workload-token provider
outbox
inbox
signed delivery
reconciliation
order-to-cash
trade projection
Business Partner projection
finance foundations
production templates
explicit ADR conformance ledger
```

Its conformance document distinguishes:

```text
foundation
partial
planned
```

rather than pretending every ADR is implemented.

That practice should be copied by every engine.

## Major gap

A complete canonical operation has still not been proven against a fully live iDempiere deployment because the REST extension installation chain remains incomplete.

This is one of the largest functional blockers in Baobab.

## Additional gaps

```text
canonical ERP API != current application API

ERP event envelope != current Shared event envelope

mapping model drift

no production EngineInstance

buy-side workflow incomplete

live CP integration incomplete

finance baseline partly unresolved

DR not executed
```

ERP is also **264 Shared commits behind**.

---

# 26. ERP Required Production Sequence

```text
Current Shared convergence
        │
        ▼
Canonical IDs/mappings
        │
        ▼
Canonical event envelope
        │
        ▼
Canonical ERP HTTP boundary
        │
        ▼
Real iDempiere REST extension
        │
        ▼
End-to-end live integration test
        │
        ▼
ZuriBeans provisioning
        │
        ▼
Order-to-cash certification
        │
        ▼
Procure-to-pay certification
        │
        ▼
Finance reconciliation
        │
        ▼
DR / recovery certification
```

Do not shortcut directly from unit-tested adapter code to production certification.

---

# 27. CMS Assessment

## Strengths

CMS has matured significantly.

Implemented capabilities include:

```text
Payload CMS
PostgreSQL
multi-tenant collections
Digital Estate awareness
Market projections
canonical mapping abstraction
transactional outbox
audit
reconciliation
S3-compatible media
health endpoints
real Baobab IAM OIDC login
```

Its OIDC implementation is particularly solid:

```text
authorization code flow
PKCE
state
nonce
JWKS verification
issuer verification
audience verification
human actor enforcement
issuer+subject identity
zero-privilege JIT provisioning
```

This is production-grade thinking.

## Critical weakness

CMS has:

```text
no contracts.lock.yaml
```

This should be corrected.

A first-class Baobab engine should never be unable to state exactly which canonical contracts it implements.

## CP mapping gap

CMS's current production mapping abstraction defaults to:

```text
UnavailableMappingResolver
```

There is no real CP mapping HTTP adapter.

That prevents complete canonical identity integration.

## Configuration hardening

Development defaults include patterns such as:

```text
PAYLOAD_SECRET = change-me-in-production
CORS = *
MinIO default credentials
```

Production configuration must fail fast if unsafe defaults remain.

---

# 28. CMS Production Recommendations

```text
contracts.lock.yaml
       │
       ▼
Shared compatibility CI
       │
       ▼
real CP mapping client
       │
       ▼
workload identity
       │
       ▼
production configuration validator
       │
       ▼
S3/KMS integration
       │
       ▼
RabbitMQ relay
       │
       ▼
backup + restore test
       │
       ▼
multi-estate isolation certification
```

CMS should also publish its own engine/capability manifest.

---

# 29. Pulse Assessment

## Strengths

Pulse has a strong clean-architecture foundation.

It correctly separates:

```text
canonical truth
from
semantic projection
```

Target implemented pattern:

```text
PostgreSQL
canonical evidence
       │
       ▼
Qdrant
rebuildable semantic index
```

Current implementation includes:

```text
Python 3.14
FastAPI
Haystack anti-corruption layer
canonical intelligence aggregates
evidence model
PostgreSQL
Qdrant
tenant-safe semantic retrieval
classification enforcement
transactional outbox
contract validation
real PG/Qdrant CI tests
```

The tenant-isolation design is particularly important:

```text
tenant restriction
       │
       ▼
Qdrant query construction
```

rather than:

```text
unrestricted vector search
       │
       ▼
post-filter results
```

That is the correct security architecture.

## Weaknesses

Pulse remains **264 Shared commits behind**.

Its production capability remains mostly scaffold-level.

Missing include:

```text
real source adapters
real embedding providers
production data domains
worker/scheduler deployment
full aggregate persistence
entity resolution
production model governance
agent execution
production SLOs
```

Pulse should not become an autonomous business-decision authority.

Its correct role remains:

```text
evidence
intelligence
analysis
recommendation
```

with business authority remaining in domain engines or CP.

---

# 30. Subscriptions Assessment

Subscriptions has progressed dramatically.

It is no longer a placeholder.

## Implemented strengths

Current Java runtime includes:

```text
HTTP API
PostgreSQL persistence
JWT workload authentication
contract validation
idempotency
tenant isolation
authoritative revision
audit
transactional outbox
usage records
readiness
billing projection lifecycle
```

Its most important architectural success is correct treatment of INTERNAL subscriptions.

```text
INTERNAL
├── monetary charge = ZERO
├── billing required = false
├── usage metering = true
└── payment execution = NEVER
```

This preserves governance without charging internal platform entities.

The service also deliberately refuses unsupported production behavior.

## Missing major commercial capabilities

Its own ADR-alignment ledger correctly reports major areas as not started:

```text
pricing catalogue
billing periods
proration
charges
credits
tax
billing accounts
payer model
invoice projection
financial obligation handoff
```

Kill Bill is not yet integrated.

Also absent:

```text
outbox relay
consumer inbox
metrics
cross-engine reconciliation
HA
backup/PITR certification
restore drill
```

Therefore Subscriptions should remain:

```text
experimental
```

until the production billing provider exists.

---

# 31. Payments Assessment

Payments likewise has progressed from concept to real engine scaffold.

## Strengths

Current Rust service includes:

```text
PaymentIntent
confirmation
authorization
capture
cancel
refund
workload JWT validation
idempotency
tenant isolation
context validation
canonical events
RFC 9457 errors
safe logging
sandbox provider
non-root distroless container
CI
```

Its fail-closed posture is excellent.

The service intentionally refuses:

```text
staging
production
```

while state is in memory and the provider is simulated.

That is the correct decision.

## Major gaps

Production remains blocked by:

```text
no durable persistence
no HyperSwitch
no Superposition
no production PSP
no webhook ingestion
no outbox relay
no metrics
no settlement integration
no DR
```

Payments therefore remains L2.

A green Rust CI pipeline should not be confused with a deployable payment platform.

---

# 32. Payment Production Target

```text
Trade / Subscriptions
        │
        ▼
Payment obligation
        │
        ▼
CP capability resolution
        │
        ▼
baobab-payments
        │
        ▼
HyperSwitch
        │
        ├── PSP A
        ├── PSP B
        └── PSP C
        │
        ▼
Payment outcome
        │
        ├── Trade / Subscriptions
        └── ERP reconciliation
```

Payment provider activation should require explicit certification per market.

---

# 33. IAM → Subscriptions → Payments Trust Chain

Target:

```text
              BAOBAB IAM
                  │
          workload identities
                  │
     ┌────────────┼─────────────┐
     │            │             │
     ▼            ▼             ▼
 CP workload   Subs workload  Payments workload
     │            │
     ▼            ▼
Subscriptions → Payments
```

Every hop needs:

```text
distinct client ID
short-lived credential
audience restriction
least-privilege scope
environment restriction
rotation ownership
audit
revocation
```

No engine should authenticate another engine using generic static secrets.

---

# 34. Event Architecture Assessment

Baobab's event architecture is conceptually sound but operationally fragmented.

Current state:

| Engine | Outbox | Inbox | Common broker relay |
|---|---|---|---|
| CP | Yes | Partial/use-case dependent | Incomplete platform-wide |
| Trade | Yes | Domain dependent | Not yet uniform |
| ERP | Yes | Yes | Own/legacy transport |
| CMS | Yes | Limited | Not yet common |
| Pulse | Yes | Limited | Not production |
| Subscriptions | Yes | Not yet | **Missing** |
| Payments | Event records | Not yet | **Missing** |

Target pattern:

```text
Domain transaction
      │
      ▼
Transactional Outbox
      │
      ▼
Relay
      │
      ▼
RabbitMQ
      │
      ▼
Consumer Inbox
      │
      ▼
Deduplication
      │
      ▼
Domain Handler
      │
      ▼
Reconciliation
```

At-least-once delivery must be assumed.

Exactly-once business behavior should be achieved through idempotency, not by pretending the transport is exactly once.

---

# 35. Canonical Event Requirements

Every cross-engine event should carry:

```text
specversion
event type
event ID
source
subject
time
dataschema
tenant/context scope
correlation ID
causation where appropriate
data
```

Events should contain bounded canonical facts.

Avoid:

```text
database row dumps
provider-specific payloads
secret values
opaque business side effects
```

---

# 36. Infrastructure Assessment

Infrastructure remains the largest production-readiness gap.

## Strengths

Its ADR set is comprehensive and covers:

```text
AWS account/environment topology
network trust zones
compute
container registry
DNS/TLS
APISIX
PostgreSQL
Redis
RabbitMQ
workload identity
tenant isolation
observability
backup
release promotion
security
cost governance
```

The architecture is credible.

## Weakness

The implementation does not yet match it.

The Terraform implementation remains extremely limited.

The existing runbook explicitly describes the implemented environment as a **local Foundation environment**, not production infrastructure.

That means no engine can yet be certified as part of an operational production platform.

---

# 37. Infrastructure Has Fallen Behind the Engine Estate

Infrastructure documentation recognises:

```text
CP
IAM
Trade
ERP
CMS
Pulse
```

but currently contains no meaningful awareness of:

```text
Subscriptions
Payments
```

The production topology must be revised.

Target:

```text
                        AWS
                         │
                 APISIX / Edge
                         │
         ┌───────────────┼─────────────────┐
         │               │                 │
         ▼               ▼                 ▼
        CP              IAM              Trade
         │                                 │
         ├──────────────┐                  ├───── ERP
         │              │                  ├───── Payments
         ▼              ▼                  └───── CMS
   Subscriptions       Pulse
         │
         ▼
      Payments

Supporting managed infrastructure:
PostgreSQL / Redis / RabbitMQ / S3 / KMS / Secrets / OTel
```

---

# 38. Production Infrastructure Required Capabilities

Infrastructure implementation should include at minimum:

### Organisation/account layer

```text
production account
staging account
development/shared-services strategy
```

### Networking

```text
VPC
private subnets
public ingress boundary
security groups
egress controls
private database access
service discovery
```

### Compute

```text
ECS/Fargate
task definitions
autoscaling
graceful deployment
health probes
rolling or blue/green deployment
```

### Persistence

```text
RDS PostgreSQL 17
ElastiCache Redis
RabbitMQ
S3
KMS
backup vault
```

### Identity

```text
IAM task roles
GitHub Actions deployment roles
Secrets Manager
workload credentials
```

### Operations

```text
OpenTelemetry
logs
metrics
tracing
alerts
dashboards
runbooks
incident integration
```

---

# 39. PostgreSQL Production Policy

PostgreSQL 17 remains a supported major release, and the PostgreSQL project currently lists 17.11 as its current minor, with PostgreSQL 17 supported through November 2029. The project recommends running the current minor of the chosen major.

Baobab should therefore define:

```text
Platform DB baseline:
PostgreSQL 17.x

Operational rule:
remain on current supported 17.x minor
through controlled patching
```

until a deliberate major-version upgrade ADR is approved.

Every engine should own its own schema/database boundary.

No cross-engine SQL joins.

---

# 40. CI/CD and Supply Chain

The reusable Shared Foundation CI is one of Baobab's strongest assets.

It should become the only normal paved road.

Every repository should receive:

```text
format
lint
typecheck/compile
unit tests
contract tests
security tests
dependency review
secret scan
SAST
container build
container scan
SBOM
provenance
reproducibility checks
migration tests
Foundation conformance
```

Production deployment should use GitHub Actions OIDC into AWS rather than long-lived AWS credentials stored as GitHub secrets. GitHub explicitly recommends OIDC for obtaining short-lived cloud credentials and supports AWS federation with trust-policy conditions.

Target:

```text
GitHub Actions
      │
      │ OIDC
      ▼
AWS IAM Role
      │
      ▼
Deploy immutable artifact
```

---

# 41. baobab-dev Assessment

`baobab-dev` is relatively mature.

It provides:

```text
polyglot development environment
DevContainer support
shared configuration
registry integrity
security gates
published development image
GHCR contract verification
```

The Dev Container approach is sound: the Dev Container Specification exists specifically to provide repeatable development environments and can also be used in CI/test automation.

Baobab should continue to distinguish:

```text
development container
```

from:

```text
production container
```

Development images may contain compilers and tooling.

Production images should not.

---

# 42. engine-template Assessment

The engine template should become strategically important.

At present it is not yet a reliable paved-road source.

Current issues include:

```text
open Foundation CI v2 PR
recent secret-scan failure
incomplete repository manifest alignment
```

Before another major Baobab engine is created, the template should itself pass a full engine-certification baseline.

Future engine creation should become:

```text
engine-template
      │
      ▼
Repository generated
      │
      ├── .baobab/repository.yaml
      ├── contracts.lock.yaml
      ├── capability manifest
      ├── Dockerfile
      ├── DevContainer
      ├── CI
      ├── security
      ├── health
      ├── metrics
      ├── runbooks
      └── ADR scaffold
```

---

# 43. Organisation Rename Audit

The GitHub organisation rename:

```text
nabhold
   ↓
baobab-platform
```

has not fully propagated.

Examples remain in:

```text
contracts.lock.yaml
package names
Java group IDs
OSGi package namespaces
documentation
Infrastructure ADRs
workflow comments
```

Do **not** globally search-and-replace.

Every occurrence belongs to one of three categories.

| Category | Action |
|---|---|
| GitHub repository reference | Change to `baobab-platform/*` |
| Business entity / Nabhold Group Africa | Preserve |
| Stable package/protocol namespace | Explicit compatibility decision required |

For example:

```text
nabhold/baobab-cp
```

as a GitHub repository reference is obsolete.

But:

```text
org.nabhold.baobab.erp
```

may be a stable Java/OSGi namespace and changing it could create compatibility churn.

Treat that separately.

---

# 44. Regulatory / Market Onboarding Architecture

There is currently no `baobab-regulatory` engine.

That should remain future architecture until the engine-management spine is stable.

However, the target boundary is now clear.

```text
Control Plane
owns:
organisation
market participation
onboarding orchestration
readiness
authorisation

Regulatory Engine
owns:
jurisdiction rules
regulatory applicability
compliance requirements
registrations
renewals
regulator adapters

Pulse
owns:
regulatory intelligence
change detection
evidence/research

Trade / ERP / Payments
own:
operational compliance execution
```

Do not make CP a giant regulatory rules engine.

---

# 45. Future Regulatory Flow

```text
Organisation approved
       │
       ▼
MarketParticipation requested
       │
       ▼
Regulatory capability resolved
       │
       ▼
Regulatory Assessment
       │
       ├── registration
       ├── licence
       ├── tax
       ├── import/export
       ├── sector regulation
       └── data requirements
       │
       ▼
Evidence / Verification
       │
       ▼
Compliance Readiness
       │
       ▼
MarketParticipation ACTIVE
```

This should eventually become one of the consumers of CP's Changeset and Evidence architecture.

---

# 46. Digital Estates Are Consumers, Not Platform Authorities

ZuriBeans, Thamani, Nabhold and future estates should remain leaf experiences.

They may compose capabilities.

They must not redefine:

```text
Tenant
Organisation
Market
CanonicalEntity
Capability
Pricing authority
Inventory ownership
Authentication authority
Provider routing
ERP ownership
```

Typical relationship:

```text
ZuriBeans
   │
   ├── CP
   ├── IAM
   ├── Trade
   ├── ERP
   ├── CMS
   └── Pulse

Thamani
   │
   ├── CP
   ├── IAM
   ├── Trade
   ├── ERP
   ├── CMS
   ├── Subscriptions where relevant
   └── Payments
```

A Digital Estate remains an experience.

It is not a tenant, legal entity or engine.

---

# 47. First Production Certification Vertical

The most useful first integrated certification remains ZuriBeans.

Not because other estates are less important, but because it already exercises the largest relevant platform slice.

Target certification scenario:

```text
Applicant / platform admin
        │
        ▼
Organisation admission
        │
        ▼
Tenant onboarding
        │
        ▼
IAM identities
        │
        ▼
ZuriBeans Buyer
        │
        ▼
Trade
        │
        ▼
ERP
        │
        ▼
Events
        │
        ▼
Reconciliation
```

Once this vertical is reliable, Thamani can add the B2C and payment dimensions.

---

# 48. Architecture Principles That Must Become Enforced Rules

The following should move from “good architecture” to **automatically enforced platform rules**.

### Authority

```text
one canonical owner per fact
```

### Databases

```text
no cross-engine database access
```

### Identity

```text
all S2S calls use workload identity
```

### Contracts

```text
all cross-repository payloads originate in Shared
```

### Routing

```text
engines do not choose providers themselves
```

### Tenancy

```text
tenant ID is not authorization
```

### Corporate structure

```text
ownership != access
```

### Events

```text
at-least-once + idempotent consumer
```

### Production config

```text
unsafe default => startup failure
```

### Release

```text
mutable tag != deployable production identity
```

### Health

```text
stale health != healthy
```

### Governance

```text
approval != activation
```

### Evidence

```text
claim != evidence != verification != fact
```

---

# 49. Observability Architecture

Baobab needs one telemetry model across all engines.

Target:

```text
                    OpenTelemetry
                         │
          ┌──────────────┼──────────────┐
          │              │              │
          ▼              ▼              ▼
        Logs          Metrics         Traces
          │              │              │
          └──────────────┼──────────────┘
                         │
                         ▼
                 Operational Platform
```

Required correlation dimensions:

```text
correlation_id
trace_id
tenant_id where safe
organisation_id where safe
engine
engine_instance
capability
operation
provider
release
environment
region
```

Avoid high-cardinality business identifiers in metrics.

---

# 50. Platform SLO Model

SLOs should exist at multiple levels.

```text
Platform
   │
   ├── Control Plane
   │
   ├── Engine
   │
   ├── Capability
   │
   └── Digital Estate
```

Examples:

| Area | Potential SLI |
|---|---|
| CP | resolution success / latency |
| IAM | authentication success / latency |
| Trade | checkout/order success |
| ERP | projection reconciliation latency |
| CMS | content API availability |
| Pulse | evidence retrieval latency |
| Subscriptions | projection convergence lag |
| Payments | authorization success/latency |
| Events | outbox age / queue lag |
| Provisioning | desired→observed convergence |

---

# 51. Reconciliation Must Become a Platform Primitive

Every distributed state relationship should be reconciled.

Examples:

```text
CP ↔ IAM
CP ↔ EngineInstance
CP ↔ Subscriptions
Trade ↔ ERP
CMS ↔ CP mappings
ERP ↔ Trade projections
Outbox ↔ broker
broker ↔ consumer inbox
Payments ↔ ERP settlement
```

A system that relies only on events eventually drifts.

A robust platform uses:

```text
events for speed
+
reconciliation for correctness
```

---

# 52. Backup and Disaster Recovery

A documented DR architecture is not a completed DR programme.

Every stateful engine needs:

```text
RPO
RTO
backup method
backup frequency
encryption
retention
restore procedure
cross-region strategy
reconciliation after restore
tested recovery evidence
```

Certification should require a real restore.

```text
Backup exists
   ≠
Recovery proven
```

---

# 53. Security Certification

Before production:

```text
SAST
dependency review
container scan
secret scan
SBOM
penetration test
tenant-isolation test
privilege-escalation test
workload-token misuse test
OIDC flow test
rate-limit test
credential compromise drill
```

Critical cross-tenant negative cases should be automated.

Example:

```text
Tenant A token
       │
       ▼
Tenant B object
       │
       ▼
DENIED
```

This must be tested across every engine.

---

# 54. Current Severity Matrix

| Priority | Gap | Impact |
|---|---|---|
| **P0** | Production infrastructure not implemented | Platform cannot be operationally certified |
| **P0** | Major Shared contract divergence | Cross-engine semantics can silently drift |
| **P0** | Missing Subs/Payments workload identities | New S2S chain cannot operate canonically |
| **P0** | Health freshness model incomplete | CP can route against unobserved health |
| **P0** | Payments cannot run staging/production | No production payment execution |
| **P0** | Subscriptions has no production provider | No commercial billing |
| **P0** | ERP not proven against complete live iDempiere path | Financial operations unproven |
| **P0** | IAM image digest unresolved | Identity artifact not immutable |
| **P1** | CP AdministrativeGrant not implemented | Fine-grained platform authority incomplete |
| **P1** | Changeset/operation framework not implemented | High-impact changes not uniformly governed |
| **P1** | Evidence/verification runtime incomplete | Organisation verification remains fragmented |
| **P1** | Core engines lack generic EngineRegistration manifests | Runtime registry incomplete |
| **P1** | EngineRelease/EngineInstance lifecycle incomplete | Runtime topology governance incomplete |
| **P1** | Direct CP→Subscriptions URL | Bypasses capability-centric routing |
| **P1** | Event fabric fragmented | Reliability model inconsistent |
| **P1** | CMS lacks contract lock | Canonical contract provenance absent |
| **P1** | Trade/ERP open integration stacks | Important go-live work remains outside main |
| **P1** | IAM DR/load/pen tests incomplete | Operational security unproven |
| **P1** | Namespace rename residue | Documentation/tooling/provenance confusion |
| **P2** | CP Console not implemented | Human operations remain developer-centric |
| **P2** | Provider migration framework incomplete | Provider replacement/failover less governable |
| **P2** | Regulatory engine absent | Future market-entry automation |
| **P2** | engine-template incomplete | Future engines may inherit debt |

---

# 55. Enterprise Remediation Program

The remediation programme should be treated as a coordinated architecture initiative, not unrelated repo tickets.

## EA-01 — Canonical Contract Convergence

Objective:

```text
Every engine declares and proves
which Shared contracts it implements.
```

Deliverables:

```text
current contracts.lock.yaml
compatibility tests
automated drift report
contract-update PR automation
namespace cleanup
```

---

# 56. EA-02 — Canonical Engine Registry

Bring every engine onto the same model.

```text
IAM
Trade
ERP
CMS
Pulse
Subscriptions
Payments
       │
       ▼
EngineDefinition
       │
       ▼
CP Registry
```

Every engine should publish:

```text
capabilities.json
provider support
contracts
operational metadata
```

---

# 57. EA-03 — Release and Runtime Topology

Introduce first-class:

```text
EngineRelease
EngineInstance
HealthObservation
DeploymentObservation
ProviderMigration
```

CP should know:

```text
what should run
what is running
where
which release
with what health
```

---

# 58. EA-04 — Workload Identity Completion

Complete canonical workload identities for every S2S actor.

No engine-to-engine static secrets.

No browser token reuse.

No generic platform-wide workload identity.

---

# 59. EA-05 — CP Governance Plane

Implement ADR-BCP-020 through ADR-BCP-023:

```text
AdministrativeGrant
Delegation
Changeset
ImpactAnalysis
Approval
ExecutionOperation
Evidence
Verification
ComplianceAssessment
```

Transition historical broad admin roles toward scoped grants.

---

# 60. EA-06 — Canonical Event Fabric

Standardise:

```text
outbox
relay
RabbitMQ topology
CloudEvents envelope
inbox
dead-letter
quarantine
replay
reconciliation
```

across all engines.

---

# 61. EA-07 — Production Infrastructure

Infrastructure is the highest-value implementation programme.

Build actual production IaC matching the accepted Infrastructure ADRs.

Nothing else substitutes for this.

---

# 62. EA-08 — Deployment Observation and Reconciliation

Close the infrastructure-control-plane loop.

```text
CP desired state
      │
      ▼
Infrastructure provisioner
      │
      ▼
AWS deployment
      │
      ▼
Observed state
      │
      ▼
CP reconciliation
```

Do not make Terraform the runtime tenant lifecycle API.

Use Terraform for governed platform infrastructure and approved provisioning primitives.

---

# 63. EA-09 — Engine Production Certification

Every engine should pass a common certification matrix.

| Control | Required |
|---|---|
| Canonical contract lock | Yes |
| Current Shared compatibility | Yes |
| Engine manifest | Yes |
| Immutable image | Yes |
| SBOM/provenance | Yes |
| Workload identity | Yes |
| Liveness/readiness | Yes |
| Metrics/traces | Yes |
| Tenant isolation | Yes |
| Idempotency | Where mutating |
| Event reliability | Where event-producing |
| Migrations | Tested |
| Backup/restore | Tested |
| Runbooks | Yes |
| Security negatives | Yes |
| Load test | Yes |
| DR test | Stateful engines |

---

# 64. EA-10 — Observability and SLOs

Create:

```text
engine dashboards
platform dashboards
queue dashboards
contract drift dashboard
provisioning dashboard
tenant readiness dashboard
security dashboard
```

CP Console should consume governed read models from these systems rather than scraping telemetry backends directly.

---

# 65. EA-11 — DR and Regional Resilience

Move from ADRs to drills.

Run:

```text
database restore
IAM restore
broker recovery
engine redeployment
regional failover
credential compromise
provider failure
```

Record actual RPO/RTO.

---

# 66. EA-12 — CP Console

Develop the Console only in lockstep with its administrative APIs.

The Console should become the visible operational expression of the Baobab architecture.

It should make complex concepts understandable without simplifying them into incorrect ones.

---

# 67. EA-13 — Market and Regulatory Orchestration

After the core runtime-management spine is stable, introduce the regulatory engine if warranted.

It should consume the same:

```text
EngineRegistration
workload identity
events
health
observability
Changeset
evidence
```

framework as every other engine.

No special architecture.

---

# 68. Recommended Execution Order

```text
                   ┌──────────────────┐
                   │ EA-01 Contracts  │
                   └────────┬─────────┘
                            │
              ┌─────────────┴─────────────┐
              ▼                           ▼
       EA-02 Registry               EA-04 Identity
              │                           │
              └─────────────┬─────────────┘
                            ▼
                     EA-03 Runtime
                            │
                            ▼
                     EA-07 Infra
                            │
              ┌─────────────┼─────────────┐
              ▼             ▼             ▼
          Engines       Event Fabric    Observability
              │             │             │
              └─────────────┼─────────────┘
                            ▼
                    CP Governance
                            │
                            ▼
                      CP Console
                            │
                            ▼
                 Integrated Certification
                            │
                            ▼
                      Production
```

---

# 69. Recommended Release Stages

## Stage A — Foundation Convergence

Exit criteria:

```text
contracts current
namespace classified
engine-template fixed
all core engines registered
workload identities defined
```

## Stage B — Runtime Spine

Exit criteria:

```text
EngineRelease
EngineInstance
HealthObservation
capability-based routing
deployment observation
```

## Stage C — Infrastructure

Exit criteria:

```text
real AWS staging
RDS
Redis
RabbitMQ
S3
KMS
APISIX
IAM roles
OTel
backups
```

## Stage D — Engine Hardening

Exit criteria:

```text
ERP live integration
Subscriptions production provider
Payments production provider
CMS CP adapter
Trade merged integration
Pulse defined production vertical
```

## Stage E — Governance

Exit criteria:

```text
AdministrativeGrant
Changeset
Approval
Operation
Evidence
Verification
```

## Stage F — Console

Exit criteria:

```text
Applicant Workspace
Platform Operations
Organisation Admin
Readiness
Audit
Changes
Diagnostics
```

## Stage G — Certification

Exit criteria:

```text
security
load
DR
cross-tenant isolation
provider failure
reconciliation
ZuriBeans E2E
Thamani E2E
```

---

# 70. Production Readiness Dashboard — Target

The eventual CP Console should be able to present a platform dashboard such as:

```text
BAOBAB PLATFORM READINESS
────────────────────────────────────────────

Contracts                 READY
IAM                       BLOCKED
  └─ immutable digest     MISSING

Control Plane             DEGRADED
  └─ health freshness     MISSING

Trade                     DEGRADED
  └─ contract currency    OUTDATED

ERP                       BLOCKED
  └─ live iDempiere       UNVERIFIED

CMS                       DEGRADED
  └─ CP mapping client    MISSING

Pulse                     NOT READY
  └─ production provider  MISSING

Subscriptions             BLOCKED
  └─ Kill Bill            MISSING

Payments                  BLOCKED
  └─ HyperSwitch          MISSING
  └─ persistence          MISSING

Infrastructure            BLOCKED
  └─ production IaC       INCOMPLETE

────────────────────────────────────────────
TENANT ACTIVATION: BLOCKED
```

This is the operational end-state Baobab should target.

---

# 71. Definition of Platform Production-Ready

Baobab should not be declared production-ready because every repository has a green CI badge.

The platform is production-ready when the following chain is proven:

```text
Customer / Group
       │
       ▼
Admission
       │
       ▼
Verification
       │
       ▼
Authorised onboarding
       │
       ▼
Tenant provisioning
       │
       ▼
IAM provisioning
       │
       ▼
Engine resolution
       │
       ▼
Infrastructure deployment
       │
       ▼
Observed health
       │
       ▼
Capability execution
       │
       ▼
Cross-engine events
       │
       ▼
Reconciliation
       │
       ▼
Readiness
       │
       ▼
Operation
       │
       ▼
Backup / recovery
```

and when all of the following are known:

```text
Who owns each fact?
Who may change it?
Which contract defines it?
Which engine executes it?
Which instance is running?
Which release is running?
Is that instance healthy?
Is the tenant authorised?
Where is the data stored?
Can the system recover?
Can an operator explain the answer?
```

---

# 72. Final Enterprise Architecture Assessment

Baobab's architecture is fundamentally credible.

There is no evidence from this fresh audit that the platform should be dismantled or fundamentally redesigned.

Its strongest architectural decisions should be preserved:

```text
Shared canonical contracts

Control Plane authority

Organisation != Tenant

Corporate ownership != authorization

Market != region

Digital Estate != Tenant

IAM authentication != CP administrative authority

Capability != product

Provider != engine

Engine != EngineInstance

Claim != evidence

Evidence != verification

Approval != activation

Business lifecycle != operational health

Events for speed
+
reconciliation for correctness
```

The current risk is implementation asymmetry.

Some repositories—particularly CP, Shared and Trade—have advanced rapidly.

Others have not yet caught up with the platform contracts or production operating model.

The programme should therefore shift from primarily **inventing architecture** toward:

```text
converge
integrate
observe
govern
test
recover
certify
```

The target enterprise architecture is:

```text
                         BAOBAB PLATFORM

                     ┌─────────────────┐
                     │     SHARED      │
                     │ Contracts/Rules │
                     └────────┬────────┘
                              │
                              ▼
                     ┌─────────────────┐
                     │ CONTROL PLANE   │
                     │ Desired State   │
                     │ Governance      │
                     │ Resolution      │
                     └────────┬────────┘
                              │
             ┌────────────────┼────────────────┐
             │                │                │
             ▼                ▼                ▼
          IAM             INFRASTRUCTURE    ENGINES
             │                │                │
             │                │          ┌─────┼──────┐
             │                │          │     │      │
             │                │          ▼     ▼      ▼
             │                │        Trade  ERP    CMS
             │                │          │     │
             │                │          ▼     ▼
             │                │       Payments Pulse
             │                │
             │                ▼
             │        Engine Instances
             │                │
             └────────────────┼────────────────┐
                              │                │
                              ▼                ▼
                         TELEMETRY          EVENTS
                              │                │
                              └───────┬────────┘
                                      ▼
                               RECONCILIATION
                                      │
                                      ▼
                                 READINESS
                                      │
                                      ▼
                                  CP CONSOLE
```

When this loop is closed, Baobab moves from being a sophisticated multi-engine software architecture to being a **production-grade enterprise platform**.

That is the next phase of the programme.