# ADR-SHARED-017 — Canonical Capability Catalogue, Provider Declaration, Engine Registry and Runtime Capability Convergence

**Status:** Proposed — Normative Target Architecture  
**Date:** 2026-09-29  
**Repository:** `baobab-platform/shared`  
**Decision Type:** Foundational Cross-Platform Capability Architecture / Enterprise Architecture Workstream Refinement  
**Reframes:** `EA-02 — Engine Registry`  
**New EA-02 Name:** **Canonical Capability Catalogue, Provider Support, Engine Registry and Runtime Resolution Convergence**  
**Contract Authority:** `baobab-platform/shared`  
**Runtime Authority:** `baobab-platform/baobab-cp`  
**Identity Authority:** `baobab-platform/baobab-iam`  
**Certification Authority:** EA-09 platform certification governance  
**Provider Implementations:** Baobab engines and approved external providers  
**Applies To:** All Baobab engines, CapabilityProviders, capability contracts, engine templates, provider declarations, engine releases, engine instances, capability bindings, product compositions and Digital Estate consumers  

**Depends On:**

- ADR-BCP-002 — Capability-Centric Baobab Platform Architecture and Digital Estate Consumption Model
- ADR-BCP-003 — Capability Registry, Grants, Scopes, Bindings and Deterministic Resolution Model
- ADR-BCP-006 — Capability Provider Lifecycle, Engine Topology, Health, Failover and Migration Model
- ADR-BCP-007 — Control Plane APIs and Capability Resolution
- ADR-SHARED-007 — Canonical Capability Contracts, Composition Registry and Cross-Engine Provider Model
- ADR-SHARED-008 — Capability Domain Registration and Canonical Event Convention
- ADR-SHARED-011 — Subscription Classification, Billing and Payment Contracts
- ADR-SHARED-012 — Topology Identifiers and External System Registry
- ADR-SHARED-016 — Provider Migration Execution and Engine Migration Tasks
- ADR-0020 — Capability-Driven Foundation CI

**Related Proposed Decision:**

- ADR-BCP-025 — Engine Release, Artifact Identity and Deployment Observation Model

**Refines / Amends In Part:**

- ADR-SHARED-007 provider-registration operationalisation
- ADR-BCP-003 capability-registry ingestion model
- ADR-BCP-006 definition of `Engine`
- EA-02 implementation scope
- `baobab-platform/engine-template/.baobab/capability-provider.yaml.example`

---

# 1. Executive Decision

EA-02 SHALL no longer be interpreted merely as:

> **Build an Engine Registry.**

That formulation is now too narrow for the architecture Baobab has actually implemented.

EA-02 SHALL retain its programme identifier for historical continuity but SHALL be redefined as:

> **EA-02 — Canonical Capability Catalogue, Provider Support, Engine Registry and Runtime Resolution Convergence.**

EA-02 SHALL establish a complete, machine-readable and governable chain from architectural capability intent to runtime capability resolution:

```text
Potential Capability
        │
        ▼
Architectural Proposal
        │
        ▼
Canonical Capability Definition
        │
        ▼
Provider Implementation Declaration
        │
        ▼
Implementation Evidence
        │
        ▼
EA-09 Certification
        │
        ▼
Control Plane Provider Registration
        │
        ▼
Engine / EngineRelease / EngineInstance
        │
        ▼
CapabilityBinding
        │
        ▼
CapabilityResolution
```

The governing separation SHALL be:

```text
WHAT can Baobab do?
        │
        ▼
Canonical Capability
        │
        │       Shared authority
        │
        ▼
WHO implements it?
        │
        ▼
CapabilityProvider
        │
        │       Engine/provider declaration
        │
        ▼
HAS that implementation been proven?
        │
        ▼
Certification
        │
        │       EA-09 governance
        │
        ▼
WHERE is it actually available?
        │
        ▼
EngineInstance / Release / Health
        │
        │       Control Plane runtime state
        │
        ▼
WHO may consume it here?
        │
        ▼
Grant + Scope + Binding
        │
        ▼
CapabilityResolution
```

No one layer SHALL imply another.

In particular:

```text
Capability exists
        ≠
Provider implements capability
        ≠
Implementation is certified
        ≠
Provider is production permitted
        ≠
Provider is active
        ≠
Engine instance is healthy
        ≠
Tenant is entitled
        ≠
Binding exists
        ≠
Capability is resolvable
```

This ADR therefore transforms EA-02 from a registry task into a **platform capability-governance and provider-conformance architecture**.

---

# 2. Why EA-02 Must Be Redefined

The original enterprise architecture programme classified EA-02 simply as **Engine Registry**.

The previous progress audit found the generic `EngineRegistration` contract and generic Control Plane engine/provider registrar to be real, but assessed EA-02 as only partially complete because manifests were not universal.

That audit further concluded that the generic registration path could converge:

```text
Engine
Capabilities
CapabilityProvider
ProviderCapabilitySupport
```

but at that time identified only Payments and Subscriptions through `capabilities.json`, and therefore concluded that Trade, ERP, CMS, Pulse and IAM lacked equivalent manifests.

A fresh audit on **29 September 2026** demonstrates that this conclusion needs refinement.

The architecture was directionally correct.

The discovery model was incomplete.

---

# 3. Fresh Audit Baseline — 29 September 2026

The current audited baselines are:

| Repository | Current `main` |
|---|---|
| `baobab-platform/shared` | `8d9e84a80fb17298b0646e56798e48e62ab4cb52` |
| `baobab-platform/baobab-cp` | `1669760c65ec61da078db0f909e683c173d45171` |
| `baobab-platform/engine-template` | `f7116d485b38...` |
| `baobab-platform/baobab-trade` | `170c54e37527...` |

Control Plane now pins Shared exactly at:

```text
8d9e84a80fb17298b0646e56798e48e62ab4cb52
```

so EA-01 contract currency between these two repositories is currently very strong.

The fresh audit also shows significant progress elsewhere:

```text
HealthObservation                    implemented

ProviderMigration execution          implemented

EngineMigrationTask                  implemented

Provider invocation reference        implemented

ACTIVE binding provider enforcement  implemented transitionally

Market activation Changeset          implemented

Mapping activation Changeset         implemented

Shared context-resolution routes     converged

CP OpenAPI nonconforming routes       zero
CP OpenAPI unimplemented routes       zero
```

Only the two legacy capability-resolution routes remain explicitly undescribed in the OpenAPI drift ledger.

This changes the architectural context in which EA-02 now operates.

---

# 4. The Most Important Fresh EA-02 Finding

Shared currently contains exactly three domain capability-manifest files:

```text
contracts/payments/v1/capabilities.json
contracts/subscriptions/v1/capabilities.json
contracts/trade/v1/capabilities.yaml
```

They currently describe:

```text
Payments       4 canonical capabilities
Subscriptions  2 canonical capabilities
Trade          3 capability entries
```

for a total of only nine explicitly enumerated capability entries.

Yet the organisation currently contains eight recognised engine repositories:

```text
baobab-trade
baobab-erp
baobab-cms
baobab-pulse
baobab-iam
baobab-payments
baobab-subscriptions
baobab-regulations
```

The platform therefore possesses substantially more implemented or architecturally intended capability than its canonical capability catalogue exposes.

EA-02 remains under-representative.

---

# 5. The Earlier Audit Also Exposed a Discovery Defect

The earlier audit concluded that only Payments and Subscriptions had capability manifests because it searched for:

```text
capabilities.json
```

However:

```text
contracts/trade/v1/capabilities.yaml
```

has existed since **14 September 2026**.

This is not merely an audit mistake.

It reveals an architectural defect:

> **Capability discovery currently depends partly upon filename and serialization convention instead of an explicit canonical catalogue/index.**

The same defect exists in runtime registration.

Current CP startup registration scans embedded Shared resources and effectively applies:

```text
if path ends with "/capabilities.json"
    parse EngineRegistration
```

Consequently:

```text
payments/v1/capabilities.json       discovered
subscriptions/v1/capabilities.json discovered
trade/v1/capabilities.yaml         ignored
```

even though all three are capability-related Shared artifacts.

This SHALL NOT remain the long-term architecture.

---

# 6. Three Different Capability Manifest Shapes Now Exist

The audit finds three materially different declaration patterns.

## 6.1 Payments and Subscriptions

These use a combined Shared `EngineRegistration` document containing:

```text
repository
capabilities[]
provider
support[]
```

That document combines:

```text
canonical capability semantics
+
provider implementation
+
provider support
```

into one artifact.

## 6.2 Trade

Trade currently uses:

```text
version
capabilities[]
```

and does not use the same EngineRegistration structure.

It therefore expresses capability semantics but not equivalent canonical provider registration.

## 6.3 Engine Template

The engine template now contains:

```text
.baobab/capability-provider.yaml.example
```

with another shape:

```text
engine
provider
supports[]
planned[]
```

This is directionally valuable but currently has **no canonical Shared schema** behind it.

It must therefore be treated as a provisional template, not yet as an authoritative platform contract.

---

# 7. Current Architecture Is Correct in Principle but Mixed in Representation

The platform already has the right core concepts.

Shared defines:

```text
Capability
CapabilityDependency
CapabilityProvider
ProviderCapabilitySupport
CapabilityBinding
CapabilityResolution
HealthObservation
```

and explicitly states:

> A Capability describes WHAT the platform can do, never HOW or WHERE.

It also correctly states that provider support is never inferred merely from engine association.

CP already persists:

```text
Capability
CapabilityProvider
ProviderCapabilitySupport
Engine
EngineInstance
CapabilityBinding
HealthObservation
ProviderMigration
```

The problem is therefore no longer the absence of the conceptual model.

The problem is **convergence**:

```text
Architecture
    ✓

Canonical schemas
    ✓ mostly

Runtime data model
    ✓ mostly

Universal declarations
    ✕

Canonical catalogue/index
    ✕

One declaration format
    ✕

Certification connection
    ✕

Complete capability census
    ✕

Runtime ingestion architecture
    transitional
```

---

# 8. A Second Semantic Drift Must Be Resolved: What Is an Engine?

ADR-BCP-006 currently describes:

```text
Engine
=
underlying technology/runtime family
```

with examples such as:

```text
medusa
idempiere
payload
haystack
keycloak
```

Accepted ADR-SHARED-012 subsequently defines:

```text
engine_id
=
registered Baobab engine/service,
named by repository
```

with examples:

```text
baobab-trade
baobab-erp
baobab-cms
```

and explicitly states:

```text
Engine != technology family
```

Current CP persistence follows the latter model.

`RegisterEngine()` inserts:

```text
topology.engine.code = repository
```

for example:

```text
baobab-payments
```

This ADR resolves the discrepancy in favour of the current Shared-012 / CP model.

From this ADR onward:

> **Engine means a first-class Baobab service/engine family.**

Examples:

```text
baobab-trade
baobab-erp
baobab-cms
baobab-pulse
baobab-iam
baobab-payments
baobab-subscriptions
baobab-regulations
```

Underlying implementation technology SHALL be separate:

```text
MedusaJS
iDempiere
Payload
Haystack
Ory
HyperSwitch
Kill Bill
OPA
```

Conceptually:

```text
Engine
baobab-payments
       │
       ▼
Provider
baobab-payments.hyperswitch
       │
       ▼
Implementation technology
HyperSwitch
```

Therefore:

```text
Engine ≠ Provider ≠ Implementation Technology
```

ADR-BCP-006 SHALL be amended accordingly.

---

# 9. `engineKey` Becomes Legacy/Ambiguous Vocabulary

Current `capability/v1/domain.schema.json` defines:

```text
engineKey
```

as technology-family identity.

Current registration documents use values such as:

```text
sandbox-payments
temporary-billing
```

which are neither canonical engine IDs nor clearly technology families.

This field has therefore accumulated ambiguous semantics.

Target architecture SHALL use explicit terminology:

```text
engine_id
    = Baobab engine/service identity

provider_key
    = provider implementation identity

implementation_key
    = optional underlying implementation family
```

Examples:

```text
engine_id:
baobab-trade

provider_key:
baobab-trade.medusa

implementation_key:
medusa
```

and:

```text
engine_id:
baobab-iam

provider_key:
baobab-iam.ory

implementation_key:
ory
```

The existing v1 `engine_key` field MAY remain during migration for compatibility but SHALL be deprecated in the next capability contract major revision.

---

# 10. Industry Reference Points

This architecture is not unusual in mature platform engineering.

Backstage uses source-controlled YAML descriptors as ingestible declarations, while catalogue processors derive relations and status rather than asking repository files themselves to be the runtime status authority. Its documentation explicitly treats catalogue status and derived relations as processor-generated/read-only information.

Kubernetes similarly separates declared desired state from observed runtime state: `spec` represents intent while `status` represents current observed state, and controllers continuously reconcile the latter toward the former.

OpenFeature's provider architecture separates the application-facing contract from the underlying provider implementation, specifically so implementations can change without major application refactoring.

OASIS TOSCA likewise models reusable capabilities independently from the concrete relationships that satisfy requirements; orchestration can later match requirements to available capabilities.

Baobab SHALL adopt the underlying principles, not the products or their exact schemas:

```text
declaration ≠ observed runtime state

capability ≠ implementation

repository metadata ≠ runtime authority

requirements ≠ provider selection

source-controlled intent
      +
runtime reconciliation
```

---

# 11. Revised EA-02 Scope

EA-02 SHALL now consist of eight explicit responsibilities.

| EA-02 Component | Responsibility |
|---|---|
| **EA-02A Capability Census** | Discover real and intended capability across every engine |
| **EA-02B Capability Taxonomy** | Normalize names, domains, granularity and authority |
| **EA-02C Canonical Capability Catalogue** | Define authoritative Shared capability records |
| **EA-02D Provider Declaration** | Standardize engine/provider support manifests |
| **EA-02E Provider Registration** | Converge validated provider support into CP |
| **EA-02F Certification Integration** | Connect EA-09 proof to provider support |
| **EA-02G Runtime Activation & Binding** | Allow only certified/eligible support into runtime routing |
| **EA-02H Drift & Coverage Governance** | Detect missing, duplicate, stale and conflicting capability declarations |

EA-02 is complete only when all eight are complete.

---

# 12. EA-02A — Capability Census

Every existing engine SHALL undergo a formal capability census.

The census SHALL distinguish:

```text
implemented
partially implemented
contracted but unimplemented
architecturally proposed
candidate for future extraction
obsolete / superseded
```

The first census SHALL cover at minimum:

| Engine | Initial capability families requiring inventory |
|---|---|
| **Trade** | Catalogue, cart/checkout, pricing, promotions, orders, RFQ, quotation, B2B organisation commerce, commercial inventory, fulfilment, returns, cross-border trade, customs, tax, trade documents, landed cost, commercial terms |
| **ERP** | General Ledger, AP, AR, financial inventory, costing, procurement accounting, Business Partner master, Product master, warehouse/accounting consequences, order-to-cash, localisation, governed export/reporting |
| **CMS** | Content management, resolution, publication, localisation, media, navigation, SEO, taxonomy, structured content |
| **Pulse** | Evidence, research, observations, signals, analysis, insight, risk, opportunity, forecasting, recommendation, semantic retrieval, intelligence products |
| **IAM** | Human authentication, workload authentication, sessions, credentials, recovery, MFA/passkeys, federation, identity lifecycle, verification and delegated identity administration |
| **Payments** | Intent, authorization, capture, cancellation, refund, routing, webhook processing, reconciliation, payout where accepted |
| **Subscriptions** | Billing projection, recurring billing, usage metering, rating, credits/adjustments, billing account, invoice projection, payment obligation |
| **Regulations** | Rule query, applicability, obligation, assessment, decision, explanation, history, change, impact, evidence bundle, cross-border evaluation |

This table is a census starting point.

It SHALL NOT by itself create canonical capability keys.

---

# 13. A Feature Is Not Automatically a Capability

EA-02 SHALL resist capability explosion.

A candidate should normally be promoted to canonical capability only where it is meaningfully:

```text
consumable
contractable
grantable or composable
replaceable
testable
auditable
provider-neutral
```

Valid conceptual examples:

```text
payment.payment.capture

billing.usage.record

commerce.order.create

regulations.assessment.evaluate
```

Invalid examples:

```text
medusa.database.lock

payload.after-change-hook

haystack.pipeline-node.execute

idempiere.table.update
```

A capability describes platform value.

It does not expose implementation mechanics.

---

# 14. Canonical Capability Identity SHALL Remain Provider-Neutral

Capability keys SHALL continue to use:

```text
<domain>.<resource>.<action>
```

They SHALL NOT contain:

```text
vendor names
framework names
tenant names
Digital Estate names
country names
deployment regions
provider names
```

Therefore:

```text
commerce.order.create
```

survives:

```text
Medusa
    ↓
another commerce provider
```

Likewise:

```text
identity.authentication.perform
```

must survive:

```text
Keycloak
    ↓
Ory
```

without forcing consumers to rename the capability.

---

# 15. Capability Ownership Does Not Imply Provider Monopoly

Shared's `CapabilityDefinition.owner` identifies the repository responsible for semantic stewardship.

For example:

```text
owner = baobab-payments
```

does not mean:

```text
only baobab-payments may ever provide this capability
```

The distinction SHALL be:

```text
semantic owner
       ≠
provider
```

A capability may eventually have multiple certified providers.

---

# 16. Capability Proposal State SHALL Remain Outside Runtime Lifecycle

Potential capabilities need visibility before runtime registration.

However, EA-02 SHALL NOT overload the current runtime lifecycle:

```text
DRAFT
ACTIVE
SUSPENDED
DEPRECATED
RETIRED
```

with architecture-workflow meanings such as:

```text
CANDIDATE
PROPOSED
CONTRACTING
```

Instead:

```text
Candidate / Proposed
        │
        │ architecture workflow
        ▼
Canonical Shared definition
        │
        │ runtime-capability lifecycle begins here
        ▼
DRAFT
ACTIVE
...
```

The distinction SHALL be explicit.

---

# 17. Planned Capabilities

Engine repositories MAY declare potential capabilities in:

```text
planned_capabilities
```

using architecture states such as:

```text
CANDIDATE
PROPOSED
CONTRACTING
CONTRACTED
```

These declarations exist for:

```text
architecture visibility
roadmap analysis
capability census
future extraction planning
contract-gap detection
```

They SHALL NOT create CP Capability records.

They SHALL NOT create ProviderCapabilitySupport.

They SHALL NOT satisfy Product compositions.

They SHALL NOT participate in CapabilityResolution.

---

# 18. Canonical Capability Catalogue

Shared SHALL maintain an explicit catalogue.

The target structure SHOULD resemble:

```text
contracts/
└── capability/
    └── v1/
        ├── capability.schema.json
        ├── provider.schema.json
        ├── provider-declaration.schema.json
        ├── catalogue.schema.json
        ├── catalogue.yaml
        ├── namespace-registry.yaml
        └── ...

contracts/
├── trade/v1/capabilities.yaml
├── payments/v1/capabilities.yaml
├── subscriptions/v1/capabilities.yaml
├── content/v1/capabilities.yaml
├── intelligence/v1/capabilities.yaml
├── identity/v1/capabilities.yaml
├── erp/v1/capabilities.yaml
└── regulations/v1/capabilities.yaml
```

The actual serialization MAY remain JSON where appropriate.

What is prohibited is **implicit discovery by extension or glob convention**.

---

# 19. `catalogue.yaml`

Shared SHALL expose one explicit catalogue/index enumerating every canonical capability definition.

Conceptually:

```yaml
schema_version: 1

capabilities:
  - capability_key: payment.payment.capture
    source: ../../payments/v1/capabilities.yaml
    owner: baobab-payments

  - capability_key: billing.usage.record
    source: ../../subscriptions/v1/capabilities.yaml
    owner: baobab-subscriptions
```

The catalogue SHALL be:

```text
complete
deterministic
CI validated
duplicate free
namespace validated
contract validated
```

No runtime component SHALL have to discover capability definitions by recursively guessing filenames.

---

# 20. Shared Owns Capability Semantics

Canonical domain capability files SHALL contain capability definitions.

They SHALL NOT be required to contain provider runtime state.

The target responsibility is:

```text
Shared capability file
        │
        └── WHAT the capability means
```

not:

```text
Shared capability file
        └── what provider is currently active in production
```

This clarifies the mixed Payments/Subscriptions registration files currently in use.

---

# 21. Engine-Local Capability Provider Declaration

Every engine SHALL eventually carry:

```text
.baobab/capability-provider.yaml
```

The canonical schema SHALL live in Shared.

The file SHALL answer:

> **Which canonical Baobab capabilities does this provider implementation implement or formally plan to implement?**

It SHALL NOT declare:

```text
CapabilityGrant
CapabilityBinding
tenant entitlement
EngineInstance
runtime health
deployment observation
actual routing
certification success
```

---

# 22. The Three `.baobab` Contracts SHALL Remain Distinct

Every engine SHOULD ultimately have:

```text
.baobab/
├── repository.yaml
├── environment.yaml
└── capability-provider.yaml
```

Their meanings are:

| File | Question |
|---|---|
| `repository.yaml` | What kind of repository is this, and which Foundation controls apply? |
| `environment.yaml` | Which development toolchain capabilities are required? |
| `capability-provider.yaml` | Which canonical Baobab domain capabilities does this engine/provider implement or intend? |

These SHALL never be conflated.

In particular:

```text
repository.yaml.capabilities
```

are Foundation technical traits, while:

```text
environment.yaml.validation.required_capabilities
```

are `baobab-dev` development capabilities, while:

```text
capability-provider.yaml
```

contains actual platform/domain capability references.

---

# 23. Provider Declaration SHALL Support Multiple Providers

An engine repository MAY have more than one provider implementation.

Payments already demonstrates why:

```text
baobab-payments.sandbox
baobab-payments.hyperswitch
```

IAM migration demonstrates another:

```text
baobab-iam.keycloak
baobab-iam.ory
```

Therefore the canonical provider declaration SHOULD allow:

```yaml
engine:
  engine_id: baobab-payments

providers:
  - provider_key: baobab-payments.sandbox
    ...

  - provider_key: baobab-payments.hyperswitch
    ...
```

rather than assuming exactly one provider forever.

---

# 24. Provider Support SHALL Reference Canonical Capabilities

A provider support declaration SHALL never redefine the capability.

It SHALL reference:

```text
capability_key
contract_versions
implementation_status
```

Conceptually:

```yaml
support:
  - capability_key: payment.payment.capture
    contract_versions:
      - 1
    implementation_status: IMPLEMENTED
```

The invariant SHALL be:

```text
supports.capability_key
        ⇒
Capability exists in Shared catalogue
```

Unknown canonical keys SHALL fail validation.

---

# 25. Implementation Status SHALL Not Be Runtime Lifecycle

The engine repository MAY truthfully state:

```text
PARTIAL
IMPLEMENTED
```

for an implementation.

It MAY NOT self-declare:

```text
CERTIFIED
ACTIVE
HEALTHY
```

because those belong to other authorities.

The states answer different questions:

| State class | Owner | Question |
|---|---|---|
| Proposal state | Architecture | Should this capability exist? |
| Capability lifecycle | Shared / governance | Is this canonical capability available as platform vocabulary? |
| Implementation status | Engine repository | Has code been implemented? |
| Certification status | EA-09 | Has the implementation been independently proven? |
| Provider lifecycle | Control Plane | Is provider support administratively active? |
| Health | Runtime observation | Is it currently healthy? |

---

# 26. Certification Cannot Be Self-Declared

An engine repository SHALL NOT be permitted to make this authoritative:

```yaml
certified: true
```

EA-09 SHALL own certification.

The eventual certification unit SHOULD be finer than “engine certified”.

It SHOULD identify at least:

```text
provider
capability
contract major
engine release
test/certification evidence
certification status
certified_at
expires_at or revocation state where applicable
```

Conceptually:

```text
ProviderCapabilityCertification
├── provider_id
├── capability_id
├── contract_major
├── engine_release_id
├── evidence_digest
├── status
├── certified_at
└── revoked_at
```

This is necessary because one engine may have:

```text
Capability A  CERTIFIED

Capability B  PREVIEW

Capability C  PARTIAL
```

at the same time.

EA-09 should therefore evolve from broad **Engine Certification** toward:

> **Engine, Provider and Capability Certification.**

---

# 27. Provider Declaration Does Not Activate Provider Support

The promotion flow SHALL be:

```text
Engine repository
capability-provider.yaml
        │
        ▼
Schema validation
        │
        ▼
Shared capability compatibility
        │
        ▼
Implementation tests
        │
        ▼
EA-09 certification
        │
        ▼
Governed provider registration
        │
        ▼
ProviderSupport = ACTIVE
```

Not:

```text
git commit says active
        │
        ▼
production provider active
```

---

# 28. Control Plane SHALL Stop Creating Canonical Capability Semantics from Provider Registration

Current `RegisterEngine()` can create unknown capabilities while processing an engine registration.

That was useful for bootstrapping.

It SHALL NOT be the target architecture.

The target SHALL separate:

```text
CapabilityCatalogueSync
```

from:

```text
ProviderRegistration
```

The correct direction is:

```text
Shared
canonical catalogue
       │
       ▼
CP capability registry

Engine/provider declaration
       │
       ▼
CP provider/support registry
```

A provider registration SHALL reference existing canonical capability keys.

It SHALL NOT originate their semantics.

---

# 29. CP Capability Registry SHALL Become a Projection of Shared

CP SHALL maintain a runtime projection of Shared capability definitions.

It MAY persist:

```text
capability_id
capability_key
name
description
domain
lifecycle
maturity
contract majors
canonical_revision
source_digest
```

but:

```text
Shared
```

remains semantic authority.

Current behaviour:

```sql
ON CONFLICT (code) DO NOTHING
```

for capability definitions is insufficient as the final convergence model because canonical lifecycle/maturity/contract metadata may legitimately evolve.

Target synchronisation SHALL therefore:

```text
compare canonical revision
validate compatibility
update allowed mutable projection fields
refuse incompatible semantic mutation under unchanged identity
record provenance
```

without permitting engines to redefine the capability.

---

# 30. Canonical Registration SHALL Not Depend on File Extension

Current implicit behaviour:

```text
/contracts/*/capabilities.json
```

SHALL be deprecated.

Target ingestion SHALL use an explicit registry artifact.

For example:

```text
contracts/capability/v1/catalogue.yaml
```

or a generated immutable bundle:

```text
capability-registry.bundle.json
```

The important requirement is not the exact name.

The invariant is:

> **Registry membership SHALL be explicit, not inferred from filesystem naming convention.**

---

# 31. Runtime Registration SHALL Ultimately Decouple from CP Builds

Current CP embeds Shared capability registration files at build time.

That means, structurally:

```text
new provider registration
        │
        ▼
Shared contract update
        │
        ▼
CP rebuild
        │
        ▼
CP restart registration
```

That is acceptable during pre-production bootstrap.

It is not the desired long-term operating model.

Target state SHOULD become:

```text
Engine Release Pipeline
        │
        ▼
Provider Declaration Artifact
        │
        ▼
EA-09 Certification
        │
        ▼
Governed Registration Command
        │
        ▼
Control Plane
```

CP SHALL not crawl GitHub at runtime.

It SHALL ingest:

```text
validated
authenticated
provenanced
governed
```

registration artifacts.

---

# 32. Transitional EngineRegistration

The existing Shared:

```text
capability/v1/registration.schema.json
```

MAY remain during migration.

It SHOULD be treated as a **registration bundle**, not as the permanent source-of-truth authoring format.

A compatibility adapter MAY generate the existing shape from:

```text
Shared capability definition
        +
engine provider declaration
```

until CP supports the separated model directly.

This avoids a disruptive rewrite.

---

# 33. Runtime Registration SHALL Default to Non-Active State

Provider registration SHALL not automatically produce production-routable state.

A newly registered provider SHOULD enter:

```text
DRAFT
```

or equivalent non-routing state.

Promotion to:

```text
ACTIVE
```

SHALL require:

```text
valid capability support
+
eligible contract versions
+
required certification
+
production permission
+
governed activation
```

and, once EA-03 is complete:

```text
approved engine release
+
eligible deployment observation
```

---

# 34. Current `production_permitted` Semantics Are Preserved

The existing pattern is useful.

For example:

```text
baobab-payments.sandbox
simulated = true
production_permitted = false
```

and:

```text
baobab-subscriptions.temporary-billing
simulated = true
production_permitted = false
```

are honest declarations.

EA-02 SHALL retain the concept that a provider implementation may exist and function without being eligible for production.

Thus:

```text
implemented
    ≠
production permitted
```

---

# 35. CapabilityProviderSupport

The runtime relationship remains:

```text
ProviderCapabilitySupport
├── provider_id
├── capability_id
├── contract_versions[]
├── lifecycle
├── effective_from
├── effective_to
└── metadata
```

No support SHALL be inferred from:

```text
repository identity
engine identity
technology
provider name
```

This invariant from ADR-SHARED-007 and ADR-BCP-006 remains correct.

---

# 36. Binding Must Name Provider

The recent migration:

```text
000077_binding_provider_enforcement.sql
```

is directionally correct.

It establishes:

```text
ACTIVE binding
        ⇒
provider_id present
```

for newly changed rows while historical anomalies are exposed by:

```text
capability.binding_without_provider
```

The current constraint remains `NOT VALID`.

EA-02 completion SHALL require:

```text
binding_without_provider = empty
```

followed by:

```text
VALIDATE CONSTRAINT capability_binding_active_provider_check
```

or an equivalent fully enforced invariant.

At completion:

```text
ACTIVE CapabilityBinding
        │
        ├── canonical capability
        ├── canonical provider
        ├── eligible engine instance
        └── compatible contract major
```

SHALL always be explicit.

---

# 37. EngineRelease and EA-03

EA-02 defines **provider-level capability support**.

EA-03 must eventually prove **release-level capability compatibility**.

This distinction matters:

```text
Provider family says:
"I implement payment.capture@1"

EngineRelease says:
"this exact immutable release implements payment.capture@1"
```

ADR-BCP-025 proposes:

```text
EngineRelease
DeploymentObservation
immutable artifact digest
source revision
release-specific contract compatibility
```

That proposal is conceptually consistent with this ADR.

EA-02 SHALL NOT wait for BCP-025 before performing the capability census and provider-declaration work.

However:

> Full production certification and release-specific runtime compatibility SHALL depend upon an accepted EngineRelease/DeploymentObservation model, whether BCP-025 or its accepted successor.

---

# 38. Desired Architecture

```text
                         BAOBAB SHARED
                Canonical Capability Catalogue
                             │
              ┌──────────────┴──────────────┐
              │                             │
              ▼                             ▼
    CapabilityDefinition          CapabilityContract
              │
              │ referenced by
              ▼
       ENGINE REPOSITORY
 .baobab/capability-provider.yaml
              │
              ├── Provider declaration
              ├── supported capabilities
              ├── contract majors
              ├── implementation status
              ├── provenance
              └── planned capabilities
              │
              ▼
        IMPLEMENTATION / CI
              │
              ▼
          EA-09 CERTIFICATION
              │
              ▼
         CONTROL PLANE
        ┌───────────────┐
        │ Engine        │
        │ Provider      │
        │ Support       │
        └───────┬───────┘
                │
                ▼
           EngineRelease
                │
                ▼
          EngineInstance
                │
                ▼
         CapabilityBinding
                │
                ▼
      CapabilityResolution
```

---

# 39. Runtime Eligibility

A capability MAY be visible in architecture while remaining completely non-routable.

Runtime resolution SHALL require, conceptually:

```text
Capability lifecycle eligible
AND
Capability maturity policy allows
AND
CapabilityGrant effective
AND
Provider exists
AND
Provider lifecycle eligible
AND
ProviderCapabilitySupport effective
AND
required contract major supported
AND
provider production policy allows environment
AND
required certification valid
AND
CapabilityBinding ACTIVE
AND
binding scope matches context
AND
EngineInstance eligible
AND
isolation compatible
AND
residency compatible
AND
health policy satisfied
AND
release compatibility satisfied when EA-03 lands
```

Only then:

```text
RESOLVED
```

---

# 40. Potential Capabilities Must Be Visible Without Becoming Runtime State

This ADR specifically supports capabilities that may later move to new engines.

Examples already visible in platform architecture include:

```text
financial ledger
procurement sourcing
warehouse execution
```

These SHALL be discoverable as architecture candidates without requiring repositories such as:

```text
baobab-ledger
baobab-procurement
baobab-wms
```

to exist first.

The architectural direction is:

```text
Capability first
Provider later
Engine extraction later still
```

not:

```text
Create engine
      ↓
invent capabilities afterward
```

---

# 41. Future Engine Extraction Becomes Cheap

Consider procurement sourcing.

Initially:

```text
procurement.sourcing.manage
        │
        ▼
baobab-erp.idempiere
```

Later:

```text
procurement.sourcing.manage
        │
        ▼
baobab-procurement.core
```

The following SHOULD remain unchanged:

```text
capability key
canonical contract
Product composition
CapabilityGrant
Digital Estate consumer contract
```

Only provider/binding/topology changes.

Likewise warehouse execution may migrate from an ERP-backed implementation to a WMS provider without renaming the capability.

---

# 42. Ledger Does Not Automatically Require a `ledger.*` Namespace

Future engine names SHALL NOT dictate capability namespace names.

A planned Ledger Engine could provide capabilities under:

```text
finance.*
settlement.*
```

if those accurately describe the business semantics.

Likewise a WMS may provide:

```text
inventory.*
logistics.*
fulfilment.*
```

The architecture SHALL not create a top-level namespace simply because an engine repository exists.

---

# 43. Regulations Reveals a Current Namespace Gap

`baobab-regulations` ADRs consistently propose:

```text
regulations.*
```

capabilities.

Current Shared `namespace-registry.yaml` does not contain:

```text
regulations
```

This is a real EA-02 gap.

Before Regulations capabilities become canonical:

```text
regulations
```

SHALL undergo the architecture review required by ADR-SHARED-007 and, if accepted, be added consistently to:

```text
namespace-registry.yaml
capabilityDomain enum
validation tooling
canonical catalogue
```

This ADR considers `regulations` an appropriate candidate namespace but does not automatically activate the proposed Regulations capabilities.

---

# 44. IAM Provider Migration Example

The Keycloak-to-Ory programme demonstrates why capability identity must be independent.

Target:

```text
identity authentication capability
          │
          ├────────── baobab-iam.keycloak
          │
          └────────── baobab-iam.ory
```

During migration:

```text
same capability
same consumer semantics
different provider
```

No capability should become:

```text
identity.keycloak.login
```

or:

```text
identity.ory.login
```

Provider replacement is exactly what the provider abstraction exists to isolate.

---

# 45. Multi-Process Implementations Do Not Automatically Create Multiple Engines

Some providers may use multiple deployable implementation components.

Ory, for example, separates Kratos and Hydra.

EA-02 SHALL not automatically turn every process boundary into a new canonical Capability or Baobab Engine.

The default rule SHALL be:

> Engine identity follows Baobab service/domain authority; implementation components remain implementation topology unless they independently satisfy the criteria for a Baobab engine boundary.

Detailed component deployment belongs to EA-03.

This prevents the capability catalogue from mirroring vendor process diagrams.

---

# 46. CapabilityProvider Manifest — Target Shape

The canonical schema SHOULD evolve toward a structure such as:

```yaml
schema:
  name: baobab-capability-provider-declaration
  version: "1.0"

engine:
  engine_id: baobab-payments

providers:
  - provider_key: baobab-payments.sandbox
    provider_type: BAOBAB_ENGINE
    implementation_key: sandbox
    simulated: true
    production_permitted: false

    invocation:
      service_reference: service://baobab-payments/payments
      protocol: http

    support:
      - capability_key: payment.intent.create
        contract_versions: [1]
        implementation_status: IMPLEMENTED

      - capability_key: payment.payment.capture
        contract_versions: [1]
        implementation_status: IMPLEMENTED

planned_capabilities:
  - proposed_key: payment.payout.execute
    proposal_status: CANDIDATE
    provenance:
      repository: baobab-platform/baobab-payments
      decision: ADR-PAY-0021
```

The exact schema SHALL be introduced in Shared through implementation of this ADR.

---

# 47. Implementation Evidence

A provider declaration MAY reference implementation evidence.

Examples:

```text
source path
test path
contract test
integration test
simulation
conformance fixture
```

Conceptually:

```yaml
evidence:
  - type: source
    path: src/service.rs

  - type: test
    path: tests/payment_capture.rs
```

This evidence answers:

> Why does this repository claim the implementation exists?

It does **not** answer:

> Is it certified?

EA-09 retains that authority.

---

# 48. Provenance

Every promoted capability/provider claim SHOULD retain provenance.

At minimum:

```text
owning repository
source commit
manifest digest
Shared catalogue revision
governing ADR where applicable
registration timestamp
```

Eventually, with EA-03:

```text
EngineRelease
artifact digest
build provenance
```

SHOULD also become available.

This makes provider support explainable rather than inferred.

---

# 49. One Provider May Support Many Capabilities

Valid:

```text
baobab-trade.medusa
        │
        ├── commerce.cart.manage
        ├── commerce.order.create
        ├── catalogue.product.read
        ├── pricing.price.resolve
        └── inventory.availability.read
```

Likewise:

```text
one capability
        │
        ├── Provider A
        └── Provider B
```

Both cardinalities SHALL remain supported.

---

# 50. Provider Support Is Not Binding

This distinction remains mandatory.

```text
ProviderCapabilitySupport
```

means:

> This provider can implement this capability.

```text
CapabilityBinding
```

means:

> This provider/instance is eligible for this capability in this context.

Therefore:

```text
Support ≠ Binding
```

No engine/provider manifest SHALL contain tenant-specific bindings.

---

# 51. Provider Support Is Not Grant

Likewise:

```text
Provider supports capability
```

does not imply:

```text
tenant may consume capability
```

Entitlement remains:

```text
CapabilityGrant
```

derived from platform/product/subscription governance.

This keeps commercial entitlement independent from implementation topology.

---

# 52. Provider Support Is Not Health

Engine manifests SHALL never carry:

```text
health: HEALTHY
```

as authoritative runtime state.

Health is observed, time-bounded state.

The current implemented `HealthObservation` model SHALL remain authoritative for this concern.

This follows the same architectural separation used by Kubernetes between desired declaration and observed status.

---

# 53. Capability Catalogue Is Not a CMDB Dump

EA-02 SHALL not attempt to model every:

```text
database
queue
library
container
internal class
framework hook
```

as a capability.

Repository and deployment inventory belong elsewhere.

The capability catalogue exists to describe stable platform functionality and its provider relationships.

---

# 54. Explicit Registry, Not Filesystem Convention

The following pattern is rejected:

```text
scan filesystem
    │
    ├── if *.json then maybe registry
    ├── if *.yaml maybe something else
    └── infer semantics from location/name
```

The required pattern is:

```text
explicit catalogue
      │
      ├── definition A
      ├── definition B
      └── definition C
```

The catalogue MAY point to YAML or JSON.

Serialization is not architecture.

---

# 55. Capability Catalogue Validation

Shared CI SHALL eventually enforce at minimum:

```text
every indexed capability exists

every capability validates against schema

every capability key is globally unique

every domain is registered

every owner is valid

every referenced request schema exists

every referenced response schema exists

every error/event schema exists

every dependency references a known capability

required dependency graph is acyclic

no provider/vendor appears in capability key

no tenant appears in capability key

no country/region appears in capability key unless semantics require and architecture approves

catalogue contains no unindexed capability definition
```

---

# 56. Engine Provider Declaration Validation

Foundation/engine CI SHALL enforce:

```text
engine_id matches canonical repository/service identity

provider_key conforms to provider grammar

provider ownership is consistent with engine

supported capability exists in Shared

supported contract major exists

IMPLEMENTED support carries required evidence

PARTIAL support cannot be promoted

simulated provider cannot be production permitted

planned capability cannot appear in runtime support

same provider/capability cannot be declared twice

provider invocation is logical, never a physical hostname or credential
```

---

# 57. Organisation-Wide Coverage Report

EA-02 SHALL produce a machine-generated coverage report.

Conceptually:

| Engine | Capability census | Canonical definitions | Provider manifest | Implemented | Certified | Production active |
|---|---:|---:|---:|---:|---:|---:|
| Trade | ✓ | partial | pending | many | partial | partial |
| ERP | ✓/partial | missing | missing | partial | no | no |
| CMS | ✓/partial | missing | missing | substantial | no | no |
| Pulse | ✓ | missing | missing | scaffold | no | no |
| IAM | ✓ | missing | missing | transitional | no | transitional |
| Payments | ✓ | 4 | legacy mixed manifest | 4 sandbox | no | no |
| Subscriptions | ✓ | 2 | legacy mixed manifest | 2 temporary | no | no |
| Regulations | architectural | proposed only | example only | no runtime | no | no |

The actual report SHALL be generated from repository/contract evidence, not hand-maintained indefinitely.

---

# 58. Missing Capability Detection

CI SHOULD report:

```text
engine implementation exists
but no canonical capability exists
```

as architecture debt.

Initially this MAY be advisory because automated code-to-capability inference is imperfect.

The durable mechanism is the formal census and manifest.

---

# 59. Unknown Capability Claims SHALL Fail

This condition SHALL be a hard failure:

```text
provider claims support
        │
        ▼
capability_key unknown to Shared
```

An engine cannot unilaterally create platform vocabulary.

The correct sequence is:

```text
propose capability
      ↓
architecture review
      ↓
Shared contract
      ↓
provider support
```

---

# 60. Capability Contract Compatibility

Provider support SHALL declare contract majors.

For example:

```text
payment.payment.capture

provider support:
[1]
```

Resolution to a consumer requiring:

```text
2
```

SHALL be impossible.

Once EngineRelease lands, release-specific compatibility SHALL further constrain this.

---

# 61. Capability Lifecycle and Maturity Remain Separate

Current Shared semantics are retained:

```text
Lifecycle:
DRAFT
ACTIVE
SUSPENDED
DEPRECATED
RETIRED
```

and:

```text
Maturity:
EXPERIMENTAL
PREVIEW
SUPPORTED
DEPRECATED
RETIRED
```

Example:

```text
lifecycle = ACTIVE
maturity  = EXPERIMENTAL
```

means:

> The capability exists and may be explicitly used where policy permits, but its contract is not yet generally supported.

Maturity SHALL not be used as health.

Lifecycle SHALL not be used as certification.

---

# 62. Updated EA Programme Audit

The fresh audit changes several previous classifications.

| EA Workstream | Current Assessment | Material Change Since Earlier Audit |
|---|---|---|
| **EA-01 Contract convergence** | **Strong** | CP now pins current Shared `8d9e84a`; OpenAPI `unimplemented=[]`, `nonconforming=[]`; only two capability resolution routes remain undescribed |
| **EA-02 Capability/Engine Registry** | **Partial, but architecture substantially present** | Generic registry exists; provider enforcement improved; Trade capability file was previously missed; declaration formats and coverage remain fragmented |
| **EA-03 Runtime topology & health** | **Strong partial** | `HealthObservation`, ProviderMigration and EngineMigrationTask now exist; `EngineRelease` and `DeploymentObservation` remain only in Proposed BCP-025 |
| **EA-04 Workload identity/trust** | **Transitional** | Core identity/workload principles remain; Keycloak→Ory reinforces need for provider-neutral capability identity |
| **EA-05 Governance plane** | **Improved materially** | Market and Mapping activation now go through Changesets; AdministrativeGrant remains shadow rather than response authority |
| **EA-06 Event fabric** | **Partial** | Strong envelope/outbox foundations remain; lifecycle coverage still needs universalisation |
| **EA-07 Production infrastructure** | **Deferred by programme decision** | Not addressed by this ADR |
| **EA-08 Observation/reconciliation** | **Partial** | Health and logical reconciliation improved; actual DeploymentObservation remains absent |
| **EA-09 Certification** | **Foundation only** | CI/conformance is strong but there is still no first-class provider/capability/release certification record |
| **EA-10 Observability/SLO** | **Partial** | Health freshness model improved; production SLO proof remains later work |
| **EA-11 DR/resilience** | **Designed / incompletely proven** | No change relevant to EA-02 decision |
| **EA-12 CP Console** | **Foundation progressing** | Backend authority continues to mature before deep topology/capability UI |
| **EA-13 Regulations** | **Architecture strong, runtime absent** | Dedicated Regulations repo/ADR family exists, but no canonical `regulations` namespace or runtime capability registration yet |

The earlier programme correctly judged EA-02 partial, but the reason is now clearer:

> The missing element is not primarily an Engine table. It is an end-to-end capability catalogue and provider-conformance system.

---

# 63. Relationship to EA-01

EA-01 answers:

> Are repositories using the correct canonical contracts?

EA-02 answers:

> What capabilities do those contracts represent, and which providers implement them?

Therefore:

```text
EA-01
Contract convergence
       │
       ▼
EA-02
Capability/provider convergence
```

EA-02 depends on EA-01 but does not duplicate it.

---

# 64. Relationship to EA-03

EA-02 deals with:

```text
logical support
```

EA-03 deals with:

```text
runtime/release topology
```

Therefore:

```text
EA-02:
Provider X supports Capability Y

EA-03:
Instance Z is running Release R
which actually supports Capability Y@1
```

Both are required for production resolution.

---

# 65. Relationship to EA-05

The following changes are consequential platform mutations:

```text
activate capability
activate provider support
retire provider support
approve production provider
change canonical provider registration
```

These SHOULD fall under the governance principles of:

```text
Changeset
plan
approval
execution
verification
```

where risk warrants.

EA-02 SHALL not create a second mutation-governance model.

---

# 66. Relationship to EA-06

EA-02 SHOULD eventually emit canonical lifecycle events such as:

```text
capability.registered
capability.lifecycle-changed

provider.registered
provider.lifecycle-changed

provider-capability.support-added
provider-capability.support-changed
provider-capability.support-retired
```

Exact event names belong in Shared AsyncAPI and SHALL follow the existing reverse-DNS convention.

---

# 67. Relationship to EA-09

EA-09 becomes one of EA-02's main production gates.

Conceptually:

```text
Repository declaration
        │
        ▼
IMPLEMENTED
        │
        ▼
EA-09
        │
        ▼
CERTIFIED
        │
        ▼
EA-02 runtime promotion
        │
        ▼
ACTIVE support
```

This creates separation of duties between:

```text
author
certifier
operator
```

---

# 68. Relationship to EA-12

The future CP Console SHOULD expose at least three distinct views:

```text
Capability Catalogue
Provider Support
Runtime Topology
```

These SHALL not be collapsed.

An operator should be able to answer:

```text
What does this capability mean?

Who implements it?

Which implementations are certified?

Which are active?

Where are they running?

Which tenants are bound?

What would be affected by retirement?
```

without inspecting SQL or repository files.

---

# 69. Provider Migration

ADR-SHARED-016 now provides a strong migration mechanism.

EA-02 makes that mechanism more valuable.

A provider migration becomes:

```text
Capability identity
       unchanged
          │
          ▼
Old Provider
          │
       migration
          │
          ▼
New Provider
```

rather than:

```text
old capability
      ↓
new capability
```

This is precisely why provider-neutral capability identity is a strategic platform asset.

---

# 70. Rejected Alternative — Keep EA-02 as Engine Registry

Rejected because:

```text
engine exists
```

does not answer:

```text
what capability it provides
which contract versions
which provider implementation
whether implementation exists
whether it is certified
whether it is production permitted
```

It under-models the architecture.

---

# 71. Rejected Alternative — Infer Capability From Engine

Rejected:

```text
baobab-trade exists
therefore it supports commerce.*
```

This would make capability availability implicit, untestable and impossible to migrate safely.

---

# 72. Rejected Alternative — Engine Repository Owns Canonical Capability Semantics

Rejected.

Engine repositories implement capabilities.

Shared defines their cross-platform semantics.

Otherwise:

```text
Trade definition
ERP definition
CMS definition
...
```

would gradually diverge.

---

# 73. Rejected Alternative — CP Crawls GitHub Repositories

Rejected.

CP is a runtime control plane, not a source-control crawler.

SCM discovery belongs in CI/platform engineering.

Runtime registration SHALL use validated artifacts or governed APIs.

---

# 74. Rejected Alternative — Treat Planned Capabilities as DRAFT Runtime Capabilities

Rejected.

A candidate idea is not yet platform vocabulary.

Architecture proposals SHALL remain distinguishable from runtime DRAFT capability definitions.

---

# 75. Rejected Alternative — Every Engine Self-Certifies

Rejected.

Implementation ownership and certification authority SHALL remain separate.

---

# 76. Rejected Alternative — One Capability Per Engine

Examples such as:

```text
commerce.manage
erp.manage
iam.manage
```

are too coarse to support:

```text
composition
provider replacement
granular entitlement
contract compatibility
partial certification
```

---

# 77. Rejected Alternative — Every Internal Feature Is a Capability

Also rejected.

Capabilities are architectural consumer contracts, not class/method inventories.

---

# 78. Migration Plan

## EA-02 Phase 0 — Decision and Semantic Lock

1. Accept or amend this ADR.
2. Reconcile `Engine` semantics across BCP-006, Shared-012 and CP.
3. Deprecate ambiguous `engine_key` technology semantics for future v2 contracts.
4. Define `engine_id`, `provider_key` and `implementation_key` precisely.
5. Stop further ad hoc capability-manifest formats.

**Exit condition:**

```text
one glossary
one authority model
no new conflicting manifest shapes
```

---

## EA-02 Phase 1 — Canonical Catalogue

Implement in Shared:

```text
catalogue schema
explicit catalogue/index
provider-declaration schema
catalogue validation
```

Normalize:

```text
Payments
Subscriptions
Trade
```

into one canonical capability-definition shape.

**Exit condition:**

```text
all existing canonical capability definitions are explicitly indexed
```

---

## EA-02 Phase 2 — Cross-Engine Capability Census

Perform the census for:

```text
Trade
ERP
CMS
Pulse
IAM
Payments
Subscriptions
Regulations
```

Classify every candidate as:

```text
canonical now
proposed
candidate
implementation detail
duplicate
owned elsewhere
future extraction
```

**Exit condition:**

Every current engine has an approved capability inventory.

---

## EA-02 Phase 3 — Canonical Provider Declarations

Each engine adopts:

```text
.baobab/capability-provider.yaml
```

conforming to Shared.

The existing engine-template provisional file SHALL be rewritten to conform to the accepted schema.

The stale `baobab-regulations/.baobab/capabilities.yaml.example` SHALL not become a competing standard.

**Exit condition:**

Every engine has one validated provider declaration or an explicit documented reason why it currently has no implemented provider.

---

## EA-02 Phase 4 — Shared/Engine Cross-Validation

CI SHALL validate:

```text
provider capability exists
contract majors exist
provider identity valid
engine identity valid
no duplicate provider support
planned != implemented
implementation evidence paths exist
```

**Exit condition:**

A provider declaration cannot merge while contradicting Shared.

---

## EA-02 Phase 5 — Control Plane Catalogue Convergence

Split current engine registration responsibilities:

```text
CapabilityCatalogueSync
        +
ProviderRegistration
```

Deprecate provider registration as a creator of unknown canonical capabilities.

Remove extension-based capability discovery.

**Exit condition:**

CP capability registry is demonstrably a projection of explicit Shared catalogue state.

---

## EA-02 Phase 6 — Certification Integration

Introduce first-class certification linkage.

At minimum:

```text
provider
capability
contract major
evidence
release when available
certification state
```

**Exit condition:**

No provider capability becomes production active solely because a manifest claims implementation.

---

## EA-02 Phase 7 — Runtime Activation Hardening

Require:

```text
ACTIVE binding
    ⇒
provider present

ACTIVE provider support
    ⇒
canonical capability present
    AND support valid
    AND certification policy satisfied
```

Validate the currently `NOT VALID` provider-binding constraint once historical rows are remediated.

**Exit condition:**

No production binding lacks an explicit provider.

---

## EA-02 Phase 8 — Coverage and Drift Governance

Generate organisation-wide coverage reports and fail CI on:

```text
unknown canonical support
duplicate capability ownership
unregistered namespace
invalid contract major
orphan provider
unindexed canonical capability
provider support without capability
runtime active support no longer backed by valid declaration/certification
```

**Exit condition:**

EA-02 can be audited mechanically.

---

# 79. Migration of Existing Artifacts

| Current Artifact | Target Treatment |
|---|---|
| `payments/v1/capabilities.json` | Split canonical capability definitions from provider support; retain generated legacy registration bundle temporarily |
| `subscriptions/v1/capabilities.json` | Same |
| `trade/v1/capabilities.yaml` | Normalize to canonical capability-definition schema and explicit catalogue indexing |
| CP `/capabilities.json` glob | Deprecate |
| `registration.schema.json` | Retain as transitional/generated registration bundle or evolve to v2 |
| `engine-template/capability-provider.yaml.example` | Replace with schema-conformant generic provider example |
| `regulations/.baobab/capabilities.yaml.example` | Remove/replace; do not create competing declaration convention |
| `provider_capability_support` CP table | Retain; becomes authoritative runtime projection |
| `capability.binding_without_provider` | Retain as migration/drift diagnostic until empty |
| `engine_key` technology field | Deprecate/rename in future capability contract major |

---

# 80. Canonical Invariants

EA-02 SHALL eventually make the following machine-testable:

```text
supports(capability)
    ⇒ canonical(capability)

ACTIVE ProviderCapabilitySupport
    ⇒ capability exists

ACTIVE ProviderCapabilitySupport
    ⇒ provider exists

ACTIVE ProviderCapabilitySupport
    ⇒ implementation is eligible

production ProviderCapabilitySupport
    ⇒ production_permitted

production ProviderCapabilitySupport
    ⇒ required certification valid

ACTIVE CapabilityBinding
    ⇒ provider_id exists

ACTIVE CapabilityBinding
    ⇒ provider supports bound capability

ACTIVE CapabilityBinding
    ⇒ required contract major supported

CapabilityResolution = RESOLVED
    ⇒ grant effective

CapabilityResolution = RESOLVED
    ⇒ binding effective

CapabilityResolution = RESOLVED
    ⇒ provider eligible

CapabilityResolution = RESOLVED
    ⇒ instance eligible

CapabilityResolution = RESOLVED
    ⇒ health policy satisfied

planned capability
    ⇒ never runtime resolvable

implementation technology changes
    ⇒ capability identity unchanged
```

---

# 81. Completion Criteria for EA-02

EA-02 SHALL be considered complete only when:

1. All eight current engines have completed capability censuses.
2. Every canonical capability is explicitly indexed in Shared.
3. Every canonical capability validates against one schema family.
4. Every engine/provider declaration conforms to a Shared schema.
5. Planned capabilities are visible but non-routable.
6. CP no longer depends on filename extension/globbing for registry membership.
7. CP capability semantics converge from Shared rather than from engine registrations.
8. All production-relevant providers have explicit ProviderCapabilitySupport.
9. All active bindings name providers.
10. The binding provider constraint is fully validated.
11. Provider support cannot self-certify.
12. EA-09 certification can be linked to provider/capability/contract version.
13. Provider registration is decoupled from arbitrary CP rebuilds.
14. Capability names remain provider/tenant/region neutral.
15. Engine identity semantics are reconciled across Shared, CP and BCP-006.
16. Capability lifecycle, provider lifecycle, certification, health and implementation status remain distinct.
17. Organisation-wide coverage/drift reports are generated automatically.
18. No current engine's material platform capability is invisible merely because its manifest uses a different file format.
19. The `regulations` namespace decision is resolved before Regulations runtime activation.
20. Future engine extraction can occur by changing Provider/Binding relationships without renaming stable capabilities.

---

# 82. Consequences

## Positive

Baobab gains:

```text
accurate capability visibility
provider neutrality
safe provider replacement
future engine extraction
fine-grained certification
better architectural audits
less hidden capability
clearer product composition
explicit provider compatibility
cleaner migration
better Console topology
machine-verifiable governance
```

The platform can answer:

```text
What can Baobab do today?

What is experimental?

What is planned?

Who provides each capability?

Which implementation is certified?

Which provider is active?

Which exact runtime serves it?

Which tenants can consume it?

What breaks if a provider is retired?
```

from canonical data rather than repository archaeology.

## Negative / Cost

The change introduces:

```text
more explicit metadata
capability census work
schema migration
Shared catalogue maintenance
engine manifest maintenance
CP registry migration
EA-09 certification integration
```

This is intentional.

The current architecture already possesses the conceptual complexity.

This ADR makes that complexity explicit and governable instead of implicit and fragmented.

---

# 83. Architectural Outcome

Before this ADR:

```text
Engine Registry
     │
     ├── some capabilities
     ├── some provider declarations
     └── some runtime topology
```

After this ADR:

```text
                    CAPABILITY ARCHITECTURE

Architecture intent
       │
       ▼
Potential Capability
       │
       ▼
Canonical Shared Capability
       │
       ▼
Provider Declaration
       │
       ▼
Implementation
       │
       ▼
Certification
       │
       ▼
ProviderCapabilitySupport
       │
       ▼
EngineRelease
       │
       ▼
EngineInstance
       │
       ▼
CapabilityBinding
       │
       ▼
CapabilityResolution
       │
       ▼
Consumer
```

That is the revised EA-02.

---

# 84. Final Decision

Baobab SHALL preserve the capability-centric architecture established by ADR-BCP-002, ADR-BCP-003 and ADR-SHARED-007.

It SHALL NOT replace those decisions with an engine-centric catalogue.

Instead, EA-02 SHALL be expanded so that the engine registry becomes one part of a larger canonical capability-governance system.

The permanent governing model is:

> **Capabilities describe what Baobab can do. Shared defines what those capabilities mean. Engines and providers declare what they implement. EA-09 proves implementations. The Control Plane registers and governs runtime availability. Engine releases and observations prove what is actually running. Bindings make eligible providers available in context. Grants determine entitlement. Resolution brings all of those facts together.**

And the governing implementation principle is:

> **A capability may exist before a provider; a provider may exist before certification; a certified provider may exist before activation; an active provider may exist without a tenant binding; and none of those facts alone is sufficient for runtime resolution.**

This separation is the foundation upon which Baobab can add, replace, extract, migrate and regionalise engines without losing stable platform semantics.