# Baobab Platform Enterprise Architecture Implementation Plan

**Revision:** EA Implementation Plan v2.0  
**Date:** 30 September 2026  
**Programme:** Baobab Platform Enterprise Architecture Convergence  
**Canonical Contract Authority:** `baobab-platform/shared`  
**Runtime / Platform Authority:** `baobab-platform/baobab-cp`  
**Identity Authority:** `baobab-platform/baobab-iam`  
**Scope:** Shared, Control Plane, IAM, Trade, ERP, CMS, Pulse, Subscriptions, Payments, engine-template and Infrastructure  
**Digital Estates:** Nabhold, ZuriBeans and Thamani remain implementation-frozen until the EA Foundation Unfreeze Gate defined in this plan is satisfied.

---

# 1. Executive Decision

The original Baobab Enterprise Architecture implementation plan remains directionally correct, but its sequencing no longer reflects the platform that exists on 30 September 2026.

Baobab has moved materially beyond the original assessment in several areas:

```text
Canonical Capability Catalogue          IMPLEMENTED AND EXPANDING
CapabilityCatalogueSync                 IMPLEMENTED
Provider-neutral identity resolution    IMPLEMENTED
HealthObservation                       IMPLEMENTED
ProviderMigration                       IMPLEMENTED
EngineMigrationTask                     IMPLEMENTED
AdministrativeGrant                     IMPLEMENTED / TRANSITIONING
Changeset                               IMPLEMENTED
ApprovalDecision                        IMPLEMENTED
ExecutionOperation                      IMPLEMENTED
Evidence / Verification                 SUBSTANTIALLY IMPLEMENTED
Engine provider declarations            PARTIALLY IMPLEMENTED
Federated workload IAM                  IMPLEMENTATION IN PROGRESS
```

The principal programme risk has therefore changed.

It is no longer mainly:

```text
"important architectural concepts do not exist"
```

It is increasingly:

```text
Shared advances
        │
        ▼
consumer repositories lag
        │
        ▼
semantic drift emerges
        │
        ▼
runtime implementation becomes asymmetric
        │
        ▼
integration assumptions become unsafe
```

The revised implementation programme SHALL therefore prioritise:

```text
CONVERGE
    ↓
RECONCILE
    ↓
IMPLEMENT AUTHORITY
    ↓
COMPLETE IDENTITY
    ↓
COMPLETE RUNTIME TOPOLOGY
    ↓
HARDEN ENGINES
    ↓
STANDARDISE EVENTS
    ↓
OBSERVE
    ↓
GOVERN
    ↓
QUALIFY
    ↓
DEPLOY INFRASTRUCTURE
    ↓
CERTIFY LIVE OPERATION
```

The most important sequencing change is deliberate:

> **Production infrastructure deployment SHALL be the final implementation stage, not an early dependency.**

Baobab should first make its contracts, identities, capability model, runtime topology, governance, engine behaviour, events, security and certification rules coherent in source code and integration environments.

Only then should those behaviours be projected into permanent cloud infrastructure.

Infrastructure must host an architecture that is sufficiently stable to deserve deployment. It must not become an expensive laboratory for unresolved cross-repository semantics.

---

# 2. Fresh Audit Baseline

The revised plan is based on the repository state audited on 30 September 2026.

## 2.1 Current principal baselines

| Repository / PR | Audited state |
|---|---|
| `baobab-platform/shared` | `e89a14541f2c683a7846aeea7b6c0eedb29e165c` |
| `baobab-platform/baobab-cp` | `b20ab9d5269ce11a7e86577abcd1528ca95d67a3` |
| `baobab-platform/infrastructure` | `4996cc9e0410f0d4ffb08ce71bd19432fdc158c1` |
| IAM PR #42 | Open, mergeable, Foundation green; CI still completing at audit |
| Shared PR #148 | Open |
| Shared PR #150 | **Merged** |

Shared #150 materially changes the EA baseline.

The Shared Canonical Capability Catalogue now contains **16 canonical capabilities**, including:

```text
billing.subscription.manage
billing.usage.record

commerce.cart.manage
commercial.quotation.manage
commercial.rfq.manage

content.entry.resolve

customer.buyer-application.manage
customer.buyer-membership.manage

finance.order-consequence.process

identity.authentication.perform
identity.workload-token.issue

payment.intent.cancel
payment.intent.create
payment.payment.authorize
payment.payment.capture
payment.refund.create
```

This represents significant progress in EA-02.

It also increases the importance of EA-01 because every canonical contract added to Shared creates a new convergence obligation for consuming engines.

---

# 3. Current Contract-Convergence Risk

Current consumer distance from Shared `main` is substantial:

| Consumer | Approximate commits behind current Shared |
|---|---:|
| Control Plane | 17 |
| IAM `main` | 371 |
| Trade | 400 |
| ERP | 400 |
| Pulse | 400 |
| Subscriptions | 147 |
| Payments | 153 |
| CMS | no complete canonical lock found |

These figures measure repository history distance, not automatically semantic incompatibility.

They nevertheless demonstrate that:

> **Shared is evolving materially faster than many consumers are reconciling their contract pins.**

This is now the single clearest reason why EA-01 must precede further platform expansion.

---

# 4. Architectural Invariants to Preserve

The revision SHALL NOT reopen settled architecture without explicit superseding ADRs.

The following principles remain foundational:

```text
Shared canonical contracts
        ≠
engine implementation

Capability
        ≠
Provider
        ≠
Engine
        ≠
EngineRelease
        ≠
EngineInstance

Organisation
        ≠
Tenant

Corporate ownership
        ≠
platform authorization

Legal Entity
        ≠
Tenant
        ≠
Market

Digital Estate
        ≠
Tenant

Authentication
        ≠
business authorization

IAM
        ≠
Control Plane administrative authority

Capability definition
        ≠
provider support

Provider support
        ≠
certification

Certification
        ≠
activation

Activation
        ≠
health

Health
        ≠
business lifecycle

Evidence
        ≠
verification

Approval
        ≠
execution

Execution success
        ≠
readiness

Events provide speed
        +
reconciliation provides correctness
```

These separations SHALL continue to guide implementation.

---

# 5. Revised Programme Priorities

The programme priorities are now:

| Priority | Programme concern |
|---|---|
| **P0** | Canonical contract convergence |
| **P0** | Identity and workload-token contract reconciliation |
| **P0** | Complete IAM Ory migration foundation |
| **P0** | EngineRelease and runtime topology |
| **P0** | Provider lifecycle and governed activation |
| **P0** | Engine implementation against canonical capabilities |
| **P1** | AdministrativeGrant enforcement transition |
| **P1** | Changeset adoption for consequential mutations |
| **P1** | Canonical event delivery |
| **P1** | Engine observability contracts and readiness |
| **P1** | Pre-deployment certification framework |
| **P1** | Regulations architecture reconciliation |
| **P2** | CP Console completion |
| **EXECUTION-LAST** | Permanent infrastructure deployment |

`EXECUTION-LAST` does **not** mean infrastructure is unimportant.

It means infrastructure implementation must consume a sufficiently stable architecture rather than define one accidentally.

---

# 6. EA-01 — Canonical Contract Convergence

## Objective

Every Baobab engine SHALL explicitly declare:

```text
which Shared revision it consumes
which contracts it implements
which contract majors it supports
which compatibility tests prove that claim
```

and CI SHALL prevent silent divergence.

## Current assessment

Control Plane has the strongest contract-consumption discipline.

Subscriptions and Payments have meaningful pinned contract tests.

Trade, ERP and Pulse still contain old Shared pins and legacy organisation references.

CMS lacks equivalent canonical contract-lock completeness.

IAM's open migration branch is materially better than IAM `main`.

## Required implementation

### EA-01A — Standardise `contracts.lock.yaml`

Adopt one common structure across all engines.

At minimum:

```yaml
schema: baobab-contract-consumer-lock
version: "1.0"

source:
  repository: baobab-platform/shared
  commit: <immutable-sha>

contracts:
  - <canonical-contract-path>

policy:
  updates: explicit_pull_request
  compatibility: validate_before_merge
```

Repository-specific metadata MAY extend this contract but SHALL NOT replace it.

### EA-01B — Eliminate operational legacy namespace references

Remove active references to:

```text
nabhold/shared
nabhold/baobab-cp
nabhold/baobab-trade
nabhold/baobab-erp
nabhold/baobab-pulse
.nabhold/
ghcr.io/nabhold/
```

Historical ADR prose may preserve historical names where historically relevant.

Operational configuration may not.

### EA-01C — Contract compatibility automation

Every engine SHALL have CI that proves:

```text
lock syntax valid
        ↓
Shared SHA exists
        ↓
declared contracts exist
        ↓
vendored copies match where applicable
        ↓
schemas parse
        ↓
implementation fixtures conform
```

### EA-01D — Contract drift reporting

Foundation SHOULD produce:

```text
consumer Shared pin
current approved Shared baseline
number of revisions behind
changed consumed contracts
compatibility classification
```

A repository being 200 commits behind Shared is not automatically a release failure.

A consumed schema being incompatibly behind SHALL be.

### EA-01E — Automated contract-update PRs

After compatibility is proven, Shared changes SHOULD be able to create explicit update PRs for consumers.

Never auto-merge cross-contract changes.

## EA-01 exit criteria

```text
all active engines have a canonical lock

no active lock references nabhold/shared

all consumed contracts have compatibility tests

CMS has a lock

Shared drift is machine reported

no unresolved incompatible consumed-contract drift
```

This gate is mandatory before platform capability expansion resumes at full speed.

---

# 7. EA-02 — Canonical Capability Catalogue and Provider Convergence

## Objective

Complete the chain:

```text
Canonical Capability
        ↓
Provider Declaration
        ↓
Implementation Evidence
        ↓
Certification
        ↓
Provider Registration
        ↓
Provider Activation
        ↓
EngineInstance
        ↓
CapabilityBinding
        ↓
CapabilityResolution
```

## Current assessment

The canonical capability catalogue is now real and contains 16 entries.

Control Plane now synchronises canonical definitions from Shared and refuses providers that originate unknown capabilities.

This is excellent progress.

Provider declarations currently exist for:

```text
Payments
Subscriptions
Trade
ERP
```

IAM, CMS and Pulse now have canonical capability foundations that should enable their declarations after their contracts are reconciled with runtime reality.

## Required implementation

### EA-02A — Finish engine capability census

Complete provider declarations for:

```text
IAM
CMS
Pulse
```

only where implementation evidence supports the claim.

Do not claim `IMPLEMENTED` because an ADR exists.

### EA-02B — Foundation enforcement

Implement `G-FCI-1`.

Foundation SHALL validate `.baobab/capability-provider.yaml` when present.

For an active engine, its absence SHALL become a conformance failure after migration grace expires.

Foundation SHALL verify:

```text
engine_id
provider key
canonical capability existence
contract majors
evidence path existence
implementation status
simulation status
production_permitted consistency
```

It SHALL NOT certify the provider.

### EA-02C — Provider registration lifecycle

Provider registration SHALL result in:

```text
DRAFT
```

by default.

Never:

```text
git declaration
        =
production ACTIVE
```

Provider activation SHALL require a governed lifecycle.

### EA-02D — Provider activation Changeset

Add a canonical Changeset kind such as:

```text
PROVIDER_ACTIVATION
```

or its accepted equivalent.

The plan SHALL inspect:

```text
provider declaration
capability support
contract compatibility
certification status
production_permitted
eligible EngineRelease
eligible EngineInstance
health
migration conflicts
```

before allowing `ACTIVE`.

### EA-02E — Binding integrity

Remediate every:

```text
capability.binding_without_provider
```

and finally validate:

```text
capability_binding_active_provider_check
```

An ACTIVE binding SHALL always identify:

```text
canonical capability
canonical provider
supported contract major
eligible instance
```

---

# 8. EA-02 / EA-04 Identity Contract Reconciliation

Shared #150 has now merged:

```text
identity.authentication.perform
identity.workload-token.issue
```

This is progress, but `identity.workload-token.issue` currently encodes:

```text
grant_type = client_credentials
client_secret
realm
```

while Shared's own workload registry already defines:

```text
credential_type = federated_workload_token
```

for Control Plane and Subscriptions.

IAM #42 implements an Ory path based on:

```text
platform-projected JWT
        ↓
RFC 7523 JWT bearer trust
        ↓
Hydra
        ↓
short-lived Baobab access token
```

The canonical capability therefore cannot permanently mean:

```text
workload token
=
client_credentials
```

## Required corrective gate — EA-ID-CONTRACT-01

Reconcile the newly merged identity contract before IAM declares production support.

The canonical capability SHALL mean:

> obtain a Baobab-conformant workload access token.

The implementation mechanism MAY include:

```text
client_credentials
private_key_jwt
federated JWT assertion
future mTLS-bound mechanisms
```

without changing the canonical capability key.

The contract SHALL separate:

```text
Baobab workload-token semantics
```

from:

```text
specific OAuth provider mechanics.
```

This correction is now a high-priority Shared/IAM reconciliation task.

---

# 9. EA-03 — Engine Release and Runtime Topology

## Objective

The Control Plane SHALL know:

```text
what SHOULD run
what IS running
which immutable software release is running
where it is running
whether the deployment matches desired state
whether it is healthy
whether its declared capability contracts remain eligible
```

## Existing implementation

Already real:

```text
Engine
CapabilityProvider
EngineInstance
HealthObservation
ProviderMigration
EngineMigrationTask
CapabilityBinding
CapabilityResolution
```

## Missing architectural spine

`EngineRelease` and `DeploymentObservation` remain architecture rather than runtime state.

ADR-BCP-025 or an accepted successor SHALL therefore be closed before infrastructure deployment.

## EA-03A — Accept release identity architecture

Define an immutable `EngineRelease` around:

```text
engine_release_id
engine_id
source_revision
artifact_digest
image_digest
build provenance
SBOM digest
declared contract majors
provider declaration digest
created_at
status
```

Mutable tags SHALL NOT identify releases.

### Correct

```text
sha256:...
```

### Incorrect

```text
latest
main
production
v2
```

when those can be moved.

## EA-03B — DeploymentObservation

Implement:

```text
DeploymentObservation
├── engine_instance_id
├── observed_release_id
├── observed_artifact_digest
├── environment
├── region
├── isolation context
├── observed_at
├── expires_at
├── observer
└── evidence
```

Observation is not desired state.

## EA-03C — Release-specific capability compatibility

Provider declaration:

```text
baobab-payments.sandbox supports payment.capture@1
```

is not enough.

A specific immutable release must prove it implements that support.

## EA-03D — Remove runtime direct-address assumptions

The existing CP billing projection uses:

```text
BILLING_ENGINE_URL
```

This is transitional.

Target invocation SHALL use:

```text
CapabilityResolution
        ↓
provider
        ↓
eligible instance
        ↓
logical invocation descriptor
```

Direct URLs MAY remain bootstrap/development tools but SHALL not be production authority.

## EA-03 exit criteria

```text
EngineRelease implemented

immutable artifact identity enforced

DeploymentObservation implemented

provider support can be tied to a release

CapabilityResolution can select release/instance eligibility

direct CP→engine production addressing removed
```

---

# 10. EA-04 — Workload Identity Completion

## Objective

Every service-to-service actor SHALL have one explicit canonical identity with:

```text
owner
runtime
environment
audience
scope
credential mode
rotation authority
lifecycle
```

No browser credential reuse.

No universal workload identity.

No static-secret fallback for workloads designated federated.

## Current implementation

Shared already defines:

```text
baobab-cp-workload
        → baobab-subscriptions

baobab-subscriptions-workload
        → baobab-payments
```

Both remain:

```text
PROVISIONED
```

which is correct.

IAM PR #42 now contains the substantive Ory migration foundation.

Current Foundation execution on the latest audited #42 head is green.

PR #42 remains open.

Shared #148 remains open.

## EA-04A — Complete IAM #42

Before merge:

```text
all CI green
all review findings resolved or explicitly disposed
Ory adapter tests green
federated workload tests green
container security green
contract pin reconciled
```

## EA-04B — Merge activation evidence semantics

Shared #148 should establish:

```text
provider trust exists
        ≠
workload ACTIVE
```

Activation SHALL require:

```text
identity provisioned
+
token minted
+
claims conform
+
audience conform
+
scope conform
+
actual resource server accepts token
```

## EA-04C — Prove CP → Subscriptions

Test:

```text
baobab-cp-workload
        ↓
IAM / Ory
        ↓
short-lived token
        ↓
baobab-subscriptions
        ↓
issuer valid
audience valid
actor_type=workload
scope valid
canonical registry ACTIVE
```

Only then change its lifecycle from:

```text
PROVISIONED → ACTIVE
```

## EA-04D — Prove Subscriptions → Payments

Repeat the same evidence for:

```text
baobab-subscriptions-workload
        ↓
baobab-payments
```

Do not activate it before the Payments consumer verifies the real token.

## EA-04E — Existing workload migration

Legacy client-credential workloads should migrate independently.

Provider migration SHALL not require changing:

```text
client_id
canonical workload identity
audience
business authorization model
```

unless an explicit security decision demands it.

---

# 11. EA-05 — Control Plane Governance Completion

## Objective

Move from:

```text
governance architecture exists
```

to:

```text
governance architecture is authoritative
```

## Current progress

The platform now has:

```text
AdministrativeGrant
EffectiveAuthority
Changeset
ChangePlan
ApprovalDecision
ExecutionOperation
Evidence
VerificationCase
VerificationResult
ProviderMigration
```

This is substantially ahead of the initial EA assessment.

## EA-05A — AdministrativeGrant becomes enforcement authority

Current IAM role bundles remain transitional.

The target is:

```text
authentication
        ↓
Principal
        ↓
AdministrativeGrant evaluation
        ↓
EffectiveAuthority
        ↓
administrative command
```

not:

```text
role name
        ↓
unbounded platform authority
```

Shadow comparison should remain until decision parity is demonstrated.

## EA-05B — Complete mutation inventory

Classify every CP mutation as:

```text
DIRECT_SAFE_MUTATION

MAKER_CHECKER_LIFECYCLE

CHANGESET

SPECIALISED_OPERATION
```

Any high-impact mutation without a governed classification is architecture debt.

## EA-05C — Expand Changeset adoption

Prioritise:

```text
provider activation
provider deprecation
high-impact capability binding
tenant suspension
high-impact subscription reclassification
production market lifecycle
engine release promotion
```

## EA-05D — Universal operation semantics

Long-running work SHALL expose:

```text
operation_id
status
step
progress
error
retryability
revision
created_at
updated_at
```

The Console must not invent its own job state.

---

# 12. Engine Conformance and Hardening Programme

Engine hardening should now occur **before permanent infrastructure deployment**.

This is a deliberate reversal of the old Stage C → Stage D ordering.

Each engine should become logically production-shaped while still executable in CI/local integration environments.

---

# 13. Trade Hardening

Trade currently declares its original canonical commerce capabilities as contracted rather than implemented.

Priority sequence:

```text
buyer application contract conformance
buyer membership contract conformance
commerce.cart.manage
commercial.rfq.manage
commercial.quotation.manage
tax/customs boundary reconciliation
ERP consequence integration
event reliability
provider declaration update
certification evidence
```

Trade SHALL stop treating native Medusa behaviour as automatically equivalent to a Baobab capability.

A canonical capability is implemented only when the Shared contract is implemented.

---

# 14. ERP Hardening

ERP must converge on:

```text
finance.order-consequence.process
inventory availability
BusinessPartner projection
canonical mappings
Shared CloudEvents
idempotency
iDempiere live adapter
```

The final ERP provider path must exercise actual iDempiere semantics rather than only a fake REST peer.

Open integration PRs shall be reconciled against current Shared before merge.

---

# 15. CMS Hardening

Shared now contains:

```text
content.entry.resolve
```

CMS should therefore become the next natural EA-02 provider-declaration adopter.

Required:

```text
canonical contracts.lock.yaml

content.entry.resolve conformance

provider declaration:
baobab-cms.payload

contract tests

workload IAM integration

CP canonical mappings

event outbox/relay

observability
```

CMS editorial Payload APIs must remain implementation detail.

Baobab consumers should use Baobab contracts.

---

# 16. Pulse Hardening

Pulse should not be forced into artificial production maturity.

Before canonical intelligence capabilities are promoted, select the first real production vertical.

Then implement:

```text
intelligence.research-mission.manage
intelligence.evidence.search
```

against Shared contracts.

Provider-neutral semantics SHALL outlive Haystack.

---

# 17. Subscriptions Hardening

The temporary provider is correctly marked:

```text
simulated = true
production_permitted = false
```

Required progression:

```text
temporary provider
        ↓
Kill Bill adapter
        ↓
canonical contract conformance
        ↓
workload authentication
        ↓
payment execution port
        ↓
events
        ↓
reconciliation
        ↓
production certification
```

Commercial billing SHALL remain blocked until the real provider exists.

---

# 18. Payments Hardening

The sandbox is useful and honestly declared.

Required progression:

```text
sandbox
        ↓
HyperSwitch adapter
        ↓
provider-neutral payment contracts
        ↓
real persistence
        ↓
idempotent commands
        ↓
webhook/event verification
        ↓
refund/capture reconciliation
        ↓
production certification
```

No production binding may resolve to the sandbox.

---

# 19. EA-06 — Canonical Event Fabric

## Objective

Every event-producing engine SHALL follow one reliability model.

Target:

```text
Domain Transaction
        │
        ▼
Transactional Outbox
        │
        ▼
Relay
        │
        ▼
Canonical CloudEvent
        │
        ▼
RabbitMQ Topology
        │
        ▼
Consumer Inbox
        │
        ▼
Idempotent Handler
        │
   ┌────┴────┐
   ▼         ▼
Success     Failure
             │
             ▼
           Retry
             │
             ▼
        DLQ / Quarantine
             │
             ▼
            Replay
             │
             ▼
       Reconciliation
```

Subscriptions explicitly says its relay is not built.

This SHALL be closed before infrastructure deployment.

## Required common controls

```text
canonical event envelope

transactional publication

consumer deduplication

bounded retry

DLQ

quarantine

replay

schema compatibility

correlation/causation IDs

tenant isolation

observability

reconciliation
```

Shared should provide conventions and contracts.

Each engine owns its local persistence and relay implementation.

---

# 20. EA-10 — Observability Before Deployment

Observability instrumentation SHALL be implemented before cloud deployment.

Deployment itself should only connect already-instrumented systems.

Every engine SHALL emit:

```text
structured logs
metrics
distributed traces
health observations
readiness
correlation IDs
security-relevant events
```

Canonical semantic conventions should be agreed before permanent dashboards exist.

## Required platform views

Eventually:

```text
engine health
provider health
capability resolution
contract drift
event lag
DLQ state
provisioning
tenant readiness
IAM
billing
payments
security
Changesets
operations
```

But dashboard implementation SHOULD consume stable telemetry semantics rather than define them.

---

# 21. EA-09 — Certification Must Be Split in Two

The old plan makes certification appear entirely post-infrastructure.

That would unnecessarily delay most meaningful qualification.

EA-09 SHALL therefore be divided.

## EA-09A — Pre-Deployment Conformance Certification

This happens before permanent infrastructure.

It can prove:

| Control | Pre-deployment |
|---|---|
| Contract lock | Yes |
| Shared compatibility | Yes |
| Capability provider declaration | Yes |
| Build reproducibility | Yes |
| Immutable image | Yes |
| SBOM | Yes |
| provenance | Yes |
| SAST | Yes |
| dependency scan | Yes |
| container scan | Yes |
| secret scan | Yes |
| workload token profile | Yes |
| liveness/readiness | Yes |
| idempotency | Yes |
| event outbox | Yes |
| relay behaviour | Yes |
| migrations | Yes |
| tenant-isolation unit/integration tests | Yes |
| authorization negative tests | Yes |
| restore procedure automation | Yes |
| runbooks | Yes |

These can be exercised using:

```text
CI
Docker Compose
Testcontainers
ephemeral databases
ephemeral RabbitMQ
local Ory
local APISIX
integration harnesses
```

## EA-09B — Operational Certification

This happens only after infrastructure deployment.

It proves environment-dependent facts:

```text
real cloud isolation
load
latency/SLO
real backup restore
regional recovery
credential compromise response
provider outage
network failure
actual deployment observation
actual RPO/RTO
actual scaling
actual secret rotation
```

This distinction lets infrastructure remain last without weakening certification discipline.

---

# 22. Certification Model

Implement a first-class certification record along the lines of:

```text
ProviderCapabilityCertification
├── provider_id
├── capability_id
├── contract_major
├── engine_release_id
├── evidence_digest
├── certification_type
├── environment_class
├── status
├── certified_at
├── expires_at
└── revoked_at
```

An engine SHALL NOT make:

```yaml
certified: true
```

authoritative inside its own provider declaration.

Certification belongs to platform governance.

---

# 23. EA-11 — Recovery Engineering Before Infrastructure

The recovery *implementation* should be designed before cloud deployment.

The recovery *drill* follows deployment.

Before deployment every stateful component SHALL have:

```text
backup format

restore command

restore ordering

dependency ordering

key recovery rules

event replay rules

schema migration rules

point-in-time recovery procedure

data integrity verification

RPO target

RTO target
```

These procedures should be executable against ephemeral/local environments first.

After infrastructure exists, the same procedures are tested against the real platform.

---

# 24. EA-12 — Control Plane Console

The Console should continue only behind stable APIs.

Current frontend foundations are useful:

```text
Next.js shell
design system
generated CP client
server-side client boundary
health route
accessibility testing
container
```

Next sequence:

```text
FE-03 Authentication / BFF
        ↓
EffectiveAuthority
        ↓
Organisation Administration
        ↓
People / Access
        ↓
Changesets
        ↓
Approvals
        ↓
Operations
        ↓
Readiness
        ↓
Diagnostics
        ↓
Certification
```

The browser SHALL never become a second Control Plane.

Authorization remains server-side.

The Console SHALL present canonical read models rather than infer platform truth from UI state.

---

# 25. EA-13 — Regulatory Architecture Reconciliation

Shared now contains an accepted G-REG-NS resolution stating:

```text
no regulations capability domain

tax remains Trade-owned

customs remains Trade-owned

separate Regulations engine not required
```

At the same time, `baobab-regulations` contains ADR-REG-0001 through ADR-REG-0030 describing a separate regulatory engine.

Those ADRs are currently Proposed.

This contradiction must be resolved explicitly.

## EA-13A — Architecture decision gate

Choose one architecture formally.

### Path A — Trade remains regulatory execution authority

Then:

```text
G-REG-NS remains authoritative

tax.* → Trade

customs.* → Trade

baobab-regulations remains experimental/research

ADR-REG family is rejected, archived or superseded
```

### Path B — Baobab Regulations becomes a platform engine

Then a new accepted cross-platform ADR must supersede the current G-REG-NS resolution and define:

```text
Regulations semantic authority

Trade enforcement authority

canonical regulations namespace

provider relationship

context boundary

capability ownership

event boundary

evidence authority
```

Until this decision is made:

> **Do not implement Regulations as a production platform dependency.**

This is an architecture decision, not an engine coding problem.

---

# 26. Infrastructure Architecture vs Infrastructure Deployment

The revised plan deliberately distinguishes:

```text
Infrastructure Architecture
```

from:

```text
Infrastructure Deployment
```

Infrastructure ADRs, Terraform module design, environment contracts, network topology and deployment interfaces MAY be developed earlier.

Actual permanent deployment SHALL remain last.

Before deployment, infrastructure code may be validated through:

```text
terraform fmt
terraform validate
tflint
checkov / equivalent
terraform test
module tests
policy tests
plan inspection
cost review
security review
```

But:

```text
terraform apply
```

against permanent staging/production environments remains the final implementation stage.

---

# 27. Revised Execution Programme

The new implementation order SHALL be:

```text
┌──────────────────────────────────────┐
│ Phase 0 — Architecture Baseline Lock │
└──────────────────┬───────────────────┘
                   ▼
┌──────────────────────────────────────┐
│ Phase 1 — EA-01 Contract Convergence │
└──────────────────┬───────────────────┘
                   ▼
┌──────────────────────────────────────┐
│ Phase 2 — EA-02 Capability Closure   │
│ + EA-13 Decision Reconciliation      │
└──────────────────┬───────────────────┘
                   ▼
┌──────────────────────────────────────┐
│ Phase 3 — EA-04 Identity Completion  │
└──────────────────┬───────────────────┘
                   ▼
┌──────────────────────────────────────┐
│ Phase 4 — EA-03 Runtime Spine        │
└──────────────────┬───────────────────┘
                   ▼
┌──────────────────────────────────────┐
│ Phase 5 — EA-05 Governance Authority │
└──────────────────┬───────────────────┘
                   ▼
┌──────────────────────────────────────┐
│ Phase 6 — Engine Hardening           │
│ Trade / ERP / CMS / Pulse /          │
│ Subscriptions / Payments / IAM       │
└──────────────────┬───────────────────┘
                   ▼
┌──────────────────────────────────────┐
│ Phase 7 — EA-06 Events               │
│ + EA-10 Observability                │
└──────────────────┬───────────────────┘
                   ▼
┌──────────────────────────────────────┐
│ Phase 8 — EA-09A Conformance         │
│ + EA-11 Recovery Engineering         │
│ + EA-12 Console                      │
└──────────────────┬───────────────────┘
                   ▼
┌──────────────────────────────────────┐
│ Phase 9 — Integrated Qualification   │
│ Local / CI / Ephemeral Platform      │
└──────────────────┬───────────────────┘
                   ▼
┌──────────────────────────────────────┐
│ Phase 10 — Infrastructure Deployment │
│             LAST IMPLEMENTATION      │
└──────────────────┬───────────────────┘
                   ▼
┌──────────────────────────────────────┐
│ Operational Certification            │
│ Validation, not architecture build   │
└──────────────────┬───────────────────┘
                   ▼
              PRODUCTION
```

---

# 28. Phase 0 — Architecture Baseline Lock

Before more implementation:

1. Commit this revised EA implementation plan into Shared.
2. Mark the prior execution ordering as superseded by this revision.
3. Do not supersede the original assessment's historical findings.
4. Record current Shared and CP baselines.
5. Classify every relevant ADR as:
   - Accepted;
   - Proposed;
   - Superseded;
   - Rejected;
   - Historical.
6. Reconcile the Regulations contradiction.
7. Add an EA implementation dashboard under Shared.

Exit:

```text
one implementation plan
one current workstream status
one dependency graph
no ambiguity about normative ADR status
```

---

# 29. Phase 1 — Foundation Convergence

Primary repos:

```text
shared
baobab-cp
baobab-iam
baobab-trade
baobab-erp
baobab-cms
baobab-pulse
baobab-subscriptions
baobab-payments
engine-template
```

Complete:

```text
contract locks
Shared pin updates
namespace cleanup
compatibility tests
Foundation contract validation
provider declaration enforcement
```

No new large platform feature should outrun this phase.

---

# 30. Phase 2 — Capability Closure

Complete:

```text
provider declarations
catalogue reconciliation
identity contract correction
CMS capability declaration
IAM capability declaration
Pulse capability decision
provider DRAFT lifecycle
provider activation Changeset
binding integrity
```

At phase exit:

```text
WHAT exists → Shared

WHO implements → engine declaration

WHETHER certified → certification authority

WHETHER active → Control Plane
```

with no layer impersonating another.

---

# 31. Phase 3 — Identity Completion

Complete:

```text
IAM #42

Shared #148

provider-neutral workload token profile

Ory provisioning

federated workload trust

CP → Subscriptions evidence

Subscriptions → Payments evidence

workload lifecycle enforcement
```

Existing Keycloak traffic may remain until migration evidence satisfies the accepted IAM migration gates.

No big-bang IAM cutover.

---

# 32. Phase 4 — Runtime Spine

Implement:

```text
EngineRelease
DeploymentObservation
release compatibility
instance eligibility
provider lifecycle
capability-based invocation
health freshness
release provenance
```

This phase gives the platform a meaningful answer to:

> What exactly is running?

before permanent infrastructure exists.

---

# 33. Phase 5 — Governance Authority

Complete the transition from shadow governance to enforced governance:

```text
AdministrativeGrant

EffectiveAuthority

Changeset

ImpactAnalysis

ApprovalDecision

ExecutionOperation

Evidence

Verification

ProviderActivation

release promotion
```

The platform must govern itself before the Console or cloud infrastructure magnifies its authority.

---

# 34. Phase 6 — Engine Hardening

Bring all engines to canonical behaviour.

Do not require cloud deployment.

Use local integration topologies.

Required minimum:

```text
canonical contracts

provider declaration

workload identity

events

health

observability

idempotency

migration tests

security tests

integration tests

reconciliation

release metadata
```

Real production provider adapters should be implemented here.

---

# 35. Phase 7 — Event and Observability Convergence

Build one event-reliability model.

Build one telemetry semantic model.

No engine-specific invented event reliability stack.

No environment-specific observability assumptions.

---

# 36. Phase 8 — Conformance Certification, Recovery and Console

This phase certifies source/runtime behaviour that does not require permanent infrastructure.

It also gives operators the interface required to inspect:

```text
authority
changes
operations
readiness
certification
drift
health
```

before production.

---

# 37. Phase 9 — Integrated Platform Qualification

Create a complete ephemeral Baobab test topology.

For example:

```text
                    Test / CI Platform
                           │
       ┌───────────────────┼────────────────────┐
       ▼                   ▼                    ▼
      IAM                 CP                RabbitMQ
       │                   │                    │
       ├──────────────┐     │     ┌──────────────┤
       ▼              ▼     ▼     ▼              ▼
     Trade           ERP   CMS   Subs          Payments
       │                           │              │
       └───────────────────────────┴──────────────┘
```

Pulse may be included where required.

Qualification SHALL prove:

```text
identity
canonical context
capability resolution
provider selection
engine invocation
events
reconciliation
failure behaviour
tenant isolation
Changesets
operations
security negatives
```

without depending on permanent cloud infrastructure.

---

# 38. EA Foundation Unfreeze Gate for Digital Estates

Nabhold, ZuriBeans and Thamani SHALL remain frozen until this gate passes.

The hold MAY be lifted for Digital Estate implementation when all of the following are true:

```text
EA-01 contracts converged

EA-02 capability authority stable

EA-04 identity architecture merged

EA-03 EngineRelease/runtime model implemented

EA-05 governance authority substantially active

required engine APIs canonical and versioned

event contracts stable

integration qualification passes

no Digital Estate needs to invent platform authority
```

At this point:

```text
Nabhold
ZuriBeans
Thamani
```

may resume frontend/integration implementation.

They still SHALL NOT be declared production-ready until live infrastructure certification passes.

This distinction matters:

```text
Digital Estate development unfreeze
        ≠
production go-live authorization
```

---

# 39. Phase 10 — Infrastructure Deployment

## This is the final implementation stage.

By this point infrastructure should not be deciding application architecture.

It should instantiate an already-defined platform.

Deploy first to a real staging environment:

```text
AWS account/environment boundary

network

compute

RDS PostgreSQL

Redis

RabbitMQ

S3

KMS

Secrets

APISIX

IAM roles

OTel

logging

metrics

tracing

backups

DNS

TLS

container registries

deployment identities
```

Each deployed EngineInstance SHALL register or be observed against:

```text
EngineRelease
artifact digest
source revision
provider
capability support
region
isolation profile
health
```

Terraform remains an infrastructure implementation mechanism.

It SHALL NOT become the runtime tenant lifecycle API.

---

# 40. Deployment Loop

The final deployment architecture shall be:

```text
Control Plane Desired State
          │
          ▼
Governed Infrastructure Request
          │
          ▼
Infrastructure Provisioner
          │
          ▼
AWS
          │
          ▼
DeploymentObservation
          │
          ▼
Control Plane
          │
          ▼
Reconciliation
          │
          ▼
HealthObservation
          │
          ▼
Readiness
```

Desired state and observed state SHALL remain separate.

---

# 41. Post-Deployment Operational Certification

Once staging exists, no major architecture implementation should remain.

The remaining work is proof.

Run:

```text
real workload IAM

real provider calls

cross-engine E2E

tenant isolation

load testing

failure injection

RabbitMQ loss/recovery

database restore

IAM recovery

credential compromise drill

secret rotation

provider outage

engine replacement

release rollback

backup restore

regional failure scenario

RPO measurement

RTO measurement
```

Any failure may require remediation, but the platform should no longer require foundational architectural invention.

---

# 42. Revised Stage Model

## Stage A — Semantic Convergence

Exit:

```text
contracts current
capability catalogue stable
provider declarations present
namespace decisions resolved
identity contracts reconciled
```

## Stage B — Identity and Runtime Authority

Exit:

```text
Ory path ready
workload identity proven
EngineRelease
EngineInstance
HealthObservation
DeploymentObservation model
capability resolution
```

## Stage C — Governance

Exit:

```text
AdministrativeGrant authoritative
Changeset
Approval
ExecutionOperation
Evidence
Verification
ProviderActivation
```

## Stage D — Engine Conformance

Exit:

```text
Trade canonical capabilities
ERP canonical boundary
CMS content resolution
IAM provider migration
Subscriptions production provider
Payments production provider
Pulse production boundary
```

## Stage E — Reliability

Exit:

```text
event relay
inbox
DLQ
replay
reconciliation
observability
health
runbooks
```

## Stage F — Pre-Deployment Certification

Exit:

```text
security
contract conformance
migration tests
tenant-isolation tests
workload identity
release provenance
SBOM
reproducibility
recovery automation
```

## Stage G — Integrated Qualification

Exit:

```text
complete ephemeral platform E2E
cross-engine flows
governance
failure paths
Digital Estate platform APIs stable
```

## Stage H — Infrastructure Deployment

Exit:

```text
real staging
all platform services deployed
observed runtime topology
backups active
telemetry active
```

## Stage I — Operational Certification

Exit:

```text
load
restore
DR
RPO/RTO
provider failure
security drills
ZuriBeans E2E
Thamani E2E
Nabhold administration E2E
```

Then:

```text
PRODUCTION AUTHORIZATION
```

---

# 43. Updated Programme Dependency Graph

```text
                      EA-01
              Contract Convergence
                      │
            ┌─────────┴─────────┐
            ▼                   ▼
          EA-02               EA-04
       Capabilities          Identity
            │                   │
            └─────────┬─────────┘
                      ▼
                    EA-03
              Runtime Topology
                      │
                      ▼
                    EA-05
                 Governance
                      │
                      ▼
              Engine Hardening
                      │
            ┌─────────┴─────────┐
            ▼                   ▼
          EA-06               EA-10
          Events           Observability
            │                   │
            └─────────┬─────────┘
                      ▼
                    EA-09A
             Pre-deploy Cert
                      │
                ┌─────┴─────┐
                ▼           ▼
              EA-11       EA-12
             Recovery     Console
                │           │
                └─────┬─────┘
                      ▼
            Integrated Qualification
                      │
                      ▼
               DIGITAL ESTATE
                 UNFREEZE
                      │
                      ▼
                    EA-07
              INFRA DEPLOYMENT
                  **LAST**
                      │
                      ▼
                    EA-08
             Live Observation
                      │
                      ▼
                    EA-09B
            Operational Cert
                      │
                      ▼
                 PRODUCTION
```

EA-08 is architecturally implemented before deployment through its data model and interfaces, but its **live reconciliation proof** necessarily follows infrastructure deployment.

---

# 44. New Platform Readiness Dashboard

The readiness dashboard should now distinguish architecture from deployment.

```text
BAOBAB EA READINESS
─────────────────────────────────────────────────────

EA-01 Contract Convergence             BLOCKED
  Trade Shared pin                     STALE
  ERP Shared pin                       STALE
  Pulse Shared pin                     STALE
  CMS contract lock                    MISSING

EA-02 Capability Governance            ADVANCED
  Canonical catalogue                  16 capabilities
  Provider declarations                PARTIAL
  Foundation enforcement               MISSING
  Provider activation governance       MISSING

EA-03 Runtime Topology                  PARTIAL
  EngineInstance                       READY
  HealthObservation                    READY
  ProviderMigration                    READY
  EngineRelease                        MISSING
  DeploymentObservation                MISSING

EA-04 Identity                         ADVANCED
  provider-neutral identity            READY
  Ory migration                        OPEN PR
  federated workload path              IMPLEMENTED/UNPROVEN
  CP workload                          PROVISIONED
  Subscriptions workload               PROVISIONED

EA-05 Governance                       ADVANCED
  AdministrativeGrant                  IMPLEMENTED
  Changeset                            IMPLEMENTED
  ExecutionOperation                   IMPLEMENTED
  Evidence / Verification              IMPLEMENTED
  legacy authority transition          INCOMPLETE

EA-06 Event Fabric                     PARTIAL
  canonical envelope                   READY
  transactional outbox                 MIXED
  relay                                INCOMPLETE
  inbox/DLQ/replay                     INCONSISTENT

EA-09A Pre-deployment certification    NOT COMPLETE

EA-10 Observability                    PARTIAL

EA-11 Recovery Engineering             NOT COMPLETE

EA-12 Console                          FOUNDATION

EA-13 Regulations                      DECISION REQUIRED

Infrastructure Deployment              DEFERRED BY PLAN

─────────────────────────────────────────────────────
DIGITAL ESTATE DEVELOPMENT              HOLD
PRODUCTION ACTIVATION                   BLOCKED
```

---

# 45. Definition of EA Foundation Complete

Baobab reaches **EA Foundation Complete** when the platform can answer, from canonical artefacts and executable runtime state:

```text
What capabilities exist?

Which Shared contract defines each one?

Which provider implements it?

Which immutable engine release implements it?

Has that implementation been certified?

Which EngineInstance is eligible?

Which workload may invoke it?

For which tenant/legal entity/market?

Which authority approved the change?

Is the instance healthy?

What happens when it fails?

Which event proves the result?

How is state reconciled?

Can the operation be replayed?

Can the engine recover?

Can an operator explain why the platform made the decision?
```

If those answers require:

```text
tribal knowledge

a README guess

a frontend assumption

a static URL

a hard-coded vendor name

an undocumented role

or manually inspecting several databases
```

the EA foundation is not complete.

---

# 46. Definition of Infrastructure-Ready

Infrastructure deployment may begin only when:

```text
Shared contracts converged

runtime topology model stable

EngineRelease implemented

identity path stable

governance authority stable

engine contracts stable

event model stable

observability semantics stable

recovery procedure defined

pre-deployment certification substantially green

integrated ephemeral platform passes
```

This is the new infrastructure entry gate.

---

# 47. Definition of Production-Ready

Production readiness remains stricter than repository readiness.

The final proof chain becomes:

```text
Canonical Contracts
        ↓
Capabilities
        ↓
Provider Implementation
        ↓
Immutable EngineRelease
        ↓
Certification
        ↓
Identity
        ↓
Governed Activation
        ↓
CapabilityBinding
        ↓
EngineInstance
        ↓
Infrastructure Deployment
        ↓
DeploymentObservation
        ↓
HealthObservation
        ↓
Capability Execution
        ↓
Canonical Events
        ↓
Reconciliation
        ↓
Readiness
        ↓
Backup / Recovery
        ↓
Operational Certification
        ↓
Production
```

---

# 48. Programme Governance

Every EA implementation gate SHOULD produce:

```text
one bounded architectural outcome

one or more repository PRs

explicit governing ADR references

tests

contract evidence

migration implications

rollback implications

documentation

updated EA dashboard
```

Cross-repository changes should be stacked according to authority.

Normally:

```text
Shared contract
        ↓
Control Plane/runtime support
        ↓
Engine implementation
        ↓
Certification
        ↓
consumer adoption
```

Do not reverse this by allowing a Digital Estate to invent a contract and later forcing Shared to describe it.

---

# 49. Rules for ADR Adherence

Before implementing a gate:

```text
1. identify governing ADRs
2. confirm their status
3. identify superseding ADRs
4. distinguish accepted from proposed
5. inspect current implementation
6. implement the smallest conforming change
7. update conformance evidence
```

Accepted ADRs govern implementation.

Proposed ADRs inform design but SHALL NOT silently override accepted platform decisions.

Where accepted ADRs conflict, create an explicit reconciliation or superseding decision.

Do not resolve architectural conflict merely through code.

---

# 50. What Should Stop

The programme should now actively avoid:

```text
more broad architecture ADRs without implementation need

new capabilities without contractability

new engines without authority analysis

provider-specific semantics in Shared capability keys

direct engine URLs becoming production architecture

tenant authority inside IAM

engine self-certification

provider declaration implying activation

frontends defining backend authority

Digital Estates compensating for missing platform contracts

cloud deployment before runtime semantics settle
```

Baobab has enough architecture to proceed.

The work is now primarily convergence and execution.

---

# 51. Immediate Execution Queue

The first implementation sequence arising from this revision should be:

| Order | Gate | Main repositories |
|---:|---|---|
| 1 | EA plan v2 committed and prior sequence superseded | Shared |
| 2 | Current Shared contract convergence audit and lock remediation | Shared + all engines |
| 3 | Correct `identity.workload-token.issue` provider neutrality | Shared + IAM |
| 4 | Complete IAM #42 | IAM |
| 5 | Complete Shared #148 lifecycle semantics | Shared |
| 6 | Add IAM provider declaration | IAM |
| 7 | Add CMS provider declaration and contract lock | CMS |
| 8 | Implement Foundation provider-declaration validation | Shared |
| 9 | Finalise/accept EngineRelease architecture | CP + Shared |
| 10 | Implement EngineRelease | CP |
| 11 | Implement DeploymentObservation model/interfaces | CP + Shared |
| 12 | Implement provider activation Changeset | CP + Shared |
| 13 | Complete AdministrativeGrant enforcement transition | CP |
| 14 | Harden Trade canonical capability conformance | Trade |
| 15 | Harden ERP canonical boundary | ERP |
| 16 | Implement CMS canonical content resolution | CMS |
| 17 | Harden Subscriptions production provider | Subscriptions |
| 18 | Harden Payments production provider | Payments |
| 19 | Resolve Pulse production capability scope | Pulse + Shared |
| 20 | Standardise event relay/inbox/DLQ/replay | engines + Shared |
| 21 | Standardise observability semantics | engines + Shared |
| 22 | Implement EA-09A certification records and gates | Shared + CP |
| 23 | Complete recovery automation | engines |
| 24 | Complete CP operational Console | CP |
| 25 | Run full ephemeral platform qualification | all platform repos |
| 26 | Pass Digital Estate Unfreeze Gate | platform governance |
| 27 | Finalise validated IaC plans | Infrastructure |
| 28 | **Deploy infrastructure** | Infrastructure |
| 29 | Run live operational certification | all |
| 30 | Authorise production Digital Estate rollout | governance |

---

# 52. Final Assessment

Baobab does not need another wholesale redesign.

The architecture is converging around a credible operating model:

```text
Shared
defines meaning

Control Plane
defines platform authority and desired state

IAM
authenticates actors

Engines
execute capabilities

Events
propagate facts

Reconciliation
restores correctness

Certification
proves implementation

Infrastructure
hosts proven runtime units

Console
makes governed state understandable

Digital Estates
consume the platform
```

The next phase must therefore resist architecture inflation.

The platform should focus on:

```text
contract convergence

authority convergence

provider neutrality

runtime identity

release identity

engine conformance

event reliability

governance enforcement

certification

integration qualification
```

and only then:

```text
infrastructure deployment.
```

The revised strategy is consequently:

> **Do not deploy the architecture in order to discover whether it is coherent. Make the architecture coherent, executable and certifiable first; deploy it last.**

That sequencing is now appropriate for the maturity Baobab Platform has reached.

---

# 53. Revised Programme Motto

```text
DEFINE ONCE
CONVERGE EVERYWHERE
PROVE BEFORE ACTIVATION
DEPLOY LAST
OPERATE WITH EVIDENCE
```