# ADR-SHARED-007 — Canonical Capability Contracts, Composition Registry and Cross-Engine Provider Model

**Status:** Proposed — Normative Platform Contract  
**Date:** 2026-09-10  
**Decision Owners:** NABHOLD / Baobab Platform Architecture  
**Repository:** `nabhold/shared`  
**Contract Authority:** `nabhold/shared`  
**Runtime Authority:** `nabhold/baobab-cp`  
**Identity Authority:** `nabhold/baobab-iam`  
**Provider Implementations:** Baobab domain engines and approved external providers  
**Applies To:** All Baobab repositories, Digital Estates, engines, provider adapters, APIs, events and integration contracts  
**Parent Architecture Decision:** ADR-BCP-002 — Capability-Centric Baobab Platform Architecture and Digital Estate Consumption Model  
**Architecture Style:** Contract-first, capability-centric, implementation-neutral, polyrepo/polyglot  
**Decision Type:** Foundational cross-platform contract architecture  
**Migration Posture:** Remodel before production; obsolete pre-production contracts MAY be replaced rather than indefinitely preserved

---

# 1. Executive Decision

`nabhold/shared` SHALL become the **canonical contract authority for the Baobab capability model**.

It SHALL define the portable, implementation-neutral contracts by which:

- capabilities are identified;
- capabilities are versioned;
- capabilities are classified;
- capability dependencies are declared;
- capability compositions are defined;
- commercial products map to compositions;
- capability grants are represented;
- capability scopes are expressed;
- providers declare capability support;
- provider contract compatibility is represented;
- capability bindings are represented;
- capability resolutions are exchanged;
- lifecycle events are emitted;
- errors and reason codes are standardised;
- Digital Estates and engines communicate without vendor coupling.

`nabhold/shared` SHALL NOT become a runtime service.

It SHALL NOT execute capability resolution.

It SHALL NOT contain tenant runtime state.

It SHALL NOT implement business workflows.

It SHALL NOT determine whether a tenant is entitled to a capability.

It SHALL NOT determine which engine instance wins a resolution.

Those are runtime responsibilities of `baobab-cp`.

The governing relationship SHALL be:

```text
              NABHOLD/SHARED
          canonical language/contracts
                    │
                    ▼
              BAOBAB CONTROL PLANE
            runtime interpretation/state
                    │
           ┌────────┼────────┐
           │        │        │
           ▼        ▼        ▼
        Trade      ERP     Pulse ...
           │        │        │
           └────────┼────────┘
                    │
                    ▼
              Digital Estates
```

The architectural maxim is:

> **Shared defines what a capability means. Control Plane determines whether and where it is available. Providers implement it. Digital Estates consume it.**

---

# 2. Context

ADR-BCP-002 establishes Baobab as a capability-centric platform.

That architecture depends upon a vocabulary that remains stable across:

```text
Go
TypeScript
Java
Python
Digital Estates
MedusaJS
iDempiere
Haystack
Payload
Keycloak integrations
future engines
external providers
```

Without a single contract authority, different repositories could independently define:

```text
Capability
CapabilityGrant
CapabilityBinding
Provider
Context
Scope
Composition
Resolution
```

and gradually assign different meanings to identical words.

That is unacceptable.

The capability architecture SHALL therefore be **contract-first**.

---

# 3. Problem Statement

The platform must solve four distinct problems without conflating them:

```text
WHAT can Baobab do?
        │
        ▼
Capability

WHAT package requires those capabilities?
        │
        ▼
Composition

MAY this tenant/context consume them?
        │
        ▼
Grant

HOW and WHERE are they implemented?
        │
        ▼
Provider + Binding + EngineInstance
```

The contracts governing these concepts must remain portable across repositories.

---

# 4. Architectural Separation

The following separation is normative:

| Concept | Contract Authority | Runtime Authority |
|---|---|---|
| Capability vocabulary | Shared | CP registry |
| Capability contract | Shared | Provider implementation |
| Capability version | Shared | CP compatibility evaluation |
| Capability dependency | Shared | CP resolution/validation |
| Capability composition | Shared | CP activation |
| Capability scope schema | Shared | CP evaluation |
| Capability grant schema | Shared | CP state |
| Provider declaration schema | Shared | CP topology |
| Capability binding schema | Shared | CP state |
| Resolution schema | Shared | CP resolver |
| Identity contract | Shared | IAM |
| Business behaviour | Domain contract | Domain engine |
| Business authorization | Domain contract | Domain engine |

Shared SHALL define semantics.

Runtime systems SHALL implement them.

---

# 5. What Shared SHALL Become

At target state, `nabhold/shared` SHALL be:

> **The authoritative, versioned, implementation-neutral contract repository defining the language through which every Baobab component describes identities, contexts, capabilities, providers, compositions, events and cross-engine interoperability.**

It SHALL function as Baobab's **platform protocol repository**.

It SHALL NOT function as Baobab's shared business-logic library.

This distinction is fundamental.

---

# 6. Shared SHALL Remain Non-Deployable

There SHALL be no production service called:

```text
shared-service
```

or:

```text
capability-registry-service
```

inside this repository merely because the repository defines registry schemas.

The runtime registry belongs in CP.

Shared SHALL contain artefacts such as:

```text
JSON Schema
OpenAPI
AsyncAPI
protobuf only if later adopted
canonical YAML registries
generated language types
SDK contract packages
validation tools
test fixtures
compatibility tooling
documentation
```

but no authoritative runtime database or HTTP server.

---

# 7. Canonical Capability Model

The following conceptual graph SHALL be authoritative:

```text
Product / Solution
       │
       ▼
CapabilityComposition
       │
       ▼
CapabilityDefinition
       │
       ├──────────────► CapabilityDependency
       │
       ▼
CapabilityGrant
       │
       ▼
CapabilityBinding
       │
       ▼
CapabilityProvider
       │
       ▼
Engine / EngineInstance
```

Supporting concepts include:

```text
CapabilityScope
CapabilityContract
CapabilityResolution
CapabilityMaturity
CapabilityLifecycle
ProviderContract
ReasonCode
```

---

# 8. CapabilityDefinition Contract

The canonical capability contract SHALL contain semantics equivalent to:

```yaml
capability:
  key: commerce.order.create
  name: Create Commerce Order
  domain: commerce
  description: >
    Creates an order using the canonical Baobab commerce
    order contract.

  maturity: SUPPORTED
  lifecycle: ACTIVE

  contracts:
    - version: "1.0"
      request: commerce/order/create/request/v1
      response: commerce/order/create/response/v1

  dependencies:
    - capability: inventory.availability.read
      type: OPTIONAL

  classification:
    data: TENANT_CONFIDENTIAL

  metadata: {}
```

The schema SHALL require at minimum:

```text
capability_key
name
description
domain
lifecycle
maturity
contract versions
```

---

# 9. Capability Naming Convention

Canonical capability keys SHALL follow:

```text
<domain>.<resource>.<action>
```

where practical.

Examples:

```text
commerce.order.create
commerce.order.cancel

commerce.catalogue.read

pricing.negotiated.resolve

inventory.availability.read

supplier.onboarding.manage

finance.invoice.issue
finance.receivable.read

logistics.shipment.create
logistics.shipment.track

documents.trade.verify

intelligence.fx.query
intelligence.commodity.query
```

Keys SHALL:

- use lowercase ASCII;
- use dot-separated namespaces;
- describe business capability;
- avoid implementation names;
- avoid tenant names;
- avoid Digital Estate names;
- avoid region names unless inherently part of capability semantics.

Invalid examples:

```text
medusa.order.create
idempiere.invoice.create
zuribeans.supplier.create
thamanii.checkout
south-africa-medusa-order
```

---

# 10. Capability Identity SHALL Be Stable

Capability identity SHALL survive implementation changes.

If:

```text
commerce.order.create
```

moves from Provider A to Provider B, its canonical capability key SHALL remain unchanged unless the business semantics themselves change incompatibly.

Vendor replacement is not a reason to rename a capability.

---

# 11. Domain Namespace Governance

Capability namespaces SHALL be centrally governed.

Initial namespace candidates include:

```text
identity
tenant
organisation
counterparty
supplier
customer
commercial
contract
commerce
catalogue
pricing
inventory
procurement
trade
logistics
fulfilment
documents
finance
payment
settlement
content
intelligence
audit
integration
```

New top-level domains SHALL require architectural review.

Repositories SHALL NOT independently create conflicting top-level namespaces.

---

# 12. Capability Granularity

Capabilities SHALL be meaningful business or platform operations.

They SHALL not be so coarse that:

```text
commerce.manage
```

becomes the entire commerce system.

Nor SHALL they normally become microscopic implementation details such as:

```text
commerce.order.internal-db-row-lock
```

A capability SHOULD correspond to something that can reasonably be:

- contracted;
- granted;
- resolved;
- implemented;
- tested;
- audited.

---

# 13. Capability Maturity

The canonical maturity enumeration SHALL initially be:

```text
EXPERIMENTAL
PREVIEW
SUPPORTED
DEPRECATED
RETIRED
```

Meaning:

| State | Meaning |
|---|---|
| EXPERIMENTAL | Architecture or behaviour may change materially |
| PREVIEW | Usable by selected consumers but not generally stable |
| SUPPORTED | Production-supported contract |
| DEPRECATED | Still available but replacement/migration expected |
| RETIRED | No longer available for new resolution |

Maturity SHALL NOT represent provider health.

---

# 14. Capability Lifecycle

Lifecycle SHALL be separate from maturity.

Recommended lifecycle states:

```text
DRAFT
ACTIVE
SUSPENDED
DEPRECATED
RETIRED
```

For example:

```text
maturity = SUPPORTED
lifecycle = SUSPENDED
```

is meaningful.

---

# 15. Capability Contracts

Each capability SHALL identify one or more compatible contract versions.

Conceptually:

```yaml
contracts:
  - major: 1
    request_schema: ...
    response_schema: ...
    error_schema: ...
    event_schemas:
      - ...
```

A capability definition SHALL NOT embed arbitrary provider-native request schemas as canonical contracts.

---

# 16. Semantic Versioning

Canonical capability contracts SHALL use explicit semantic versioning.

General rule:

```text
MAJOR.MINOR.PATCH
```

### PATCH

Documentation or compatible clarification.

### MINOR

Backward-compatible extension.

### MAJOR

Breaking change.

A provider claiming support for a contract SHALL declare exactly what versions it supports.

---

# 17. Compatibility

Shared SHALL define compatibility rules.

For example:

```text
Consumer requires:
    commerce.order.create >=1.2 <2.0

Provider supports:
    1.3

Result:
    COMPATIBLE
```

But:

```text
Consumer requires:
    >=2.0 <3.0

Provider supports:
    1.3

Result:
    INCOMPATIBLE
```

CP SHALL evaluate these rules at runtime or provisioning time.

Shared SHALL define them.

---

# 18. CapabilityDependency Contract

Capabilities MAY depend on other capabilities.

Canonical dependency types SHOULD initially include:

```text
REQUIRED
OPTIONAL
CONDITIONAL
```

Conceptual schema:

```yaml
dependency:
  capability: payment.authorize
  version_constraint: ">=1.0 <2.0"
  type: REQUIRED
```

Conditional dependencies SHALL declare an explicit condition contract.

They SHALL NOT rely on undocumented prose.

---

# 19. Circular Dependencies

Mandatory dependency graphs SHALL be acyclic.

For example:

```text
A requires B
B requires C
C requires A
```

SHALL fail validation.

CI SHALL validate capability graphs.

---

# 20. CapabilityComposition Contract

A composition SHALL define a reusable set of capability requirements.

Conceptually:

```yaml
composition:
  key: profile.b2b
  version: "1.0.0"

  required:
    - organisation.account.manage
    - commercial.quotation.manage
    - commerce.pricing.negotiated
    - commerce.order.manage

  optional:
    - supplier.onboarding.manage
    - finance.credit.manage

  dependencies:
    - composition: platform.core
```

Compositions SHALL remain declarative.

---

# 21. Composition Types

The canonical model SHOULD permit categories such as:

```text
PLATFORM
PRODUCT
PROFILE
ADD_ON
INTERNAL
```

Examples:

```text
platform.core

solution.baobab-xbt

profile.b2b
profile.b2c
profile.crossborder
profile.logistics
profile.commodity-trade

addon.advanced-intelligence
```

The categories SHALL aid governance but SHALL not create arbitrary inheritance hierarchies.

---

# 22. Composition Graph

Compositions MAY include other compositions.

Example:

```text
solution.baobab-xbt
│
├── platform.core
├── commercial.core
└── finance.core

profile.b2b
│
├── organisation.accounts
├── negotiated-pricing
└── contract-management
```

Composition inclusion SHALL be acyclic.

---

# 23. Baobab XBT Registry

Shared SHALL permit XBT to be represented as a canonical composition.

For example:

```yaml
key: solution.baobab-xbt
version: 1.0.0

includes:
  - platform.core
  - commercial.core
  - finance.core
  - intelligence.core

optional_profiles:
  - profile.b2b
  - profile.b2c
  - profile.crossborder
  - profile.logistics
  - profile.commodity-trade
```

This SHALL NOT create a runtime XBT service.

---

# 24. CapabilityScope Contract

Shared SHALL define a canonical scope vocabulary.

The base scope SHOULD include:

```text
tenant_id
legal_entity_id
organisation_id
business_unit_id
digital_estate_id
digital_property_id
channel_id
market_id
country_code
jurisdiction_code
currency_code
customer_segment_id
catalogue_id
operating_region_id
geographic_region_id
deployment_region
environment
isolation_profile_id
```

Not every field SHALL be mandatory.

Scope semantics SHALL be explicit.

---

# 25. Common Scope Dimensions

Shared SHOULD define:

```text
CommonScopeDimensions
```

for semantic reuse.

Then specialised contracts MAY derive or compose:

```text
MappingScope
CapabilityScope
PolicyScope
```

without treating these as the same business object.

---

# 26. Scope Matching Semantics

The contract SHALL define matching rules.

For each dimension:

```text
UNSPECIFIED
EXACT
INCLUDE
EXCLUDE
```

where applicable.

For example:

```yaml
countries:
  include:
    - ZA
    - UG
  exclude: []
```

A provider binding that excludes Kenya SHALL not resolve for a Kenyan operation merely because its tenant scope matches.

---

# 27. Scope Specificity

Shared SHALL define how specificity is calculated.

Example conceptual ordering:

```text
tenant
  <
tenant + market
  <
tenant + legal_entity + market
  <
tenant + legal_entity + estate + market
```

CP SHALL implement this algorithm.

The algorithm SHALL NOT be reinvented independently in every language.

---

# 28. CapabilityGrant Contract

The canonical grant contract SHALL express:

```text
id
tenant
capability
scope
source
source_reference
status
effective_from
effective_to
constraints
version
audit metadata
```

Recommended status values:

```text
PENDING
ACTIVE
SUSPENDED
REVOKED
EXPIRED
```

Grant status SHALL not be inferred solely from timestamps.

---

# 29. Grant Source

Canonical grant sources SHOULD include:

```text
PLATFORM_BASELINE
PRODUCT_SUBSCRIPTION
CONTRACT
TRIAL
MANUAL_APPROVAL
INTERNAL_POLICY
MIGRATION
```

The list SHALL be extensible through governed versioning.

---

# 30. Product-to-Capability Expansion

Shared SHALL define how a product/composition can be expanded into capability requirements.

Conceptually:

```text
ProductSubscription
       │
       ▼
Composition
       │
       ▼
Flatten dependency graph
       │
       ▼
Validate versions
       │
       ▼
Capability requirements
       │
       ▼
CP creates grants
```

Shared SHALL provide the declarative definition.

CP SHALL perform runtime expansion and persistence.

---

# 31. CapabilityProvider Contract

The canonical provider declaration SHALL express:

```text
provider_key
provider_type
engine_key
capabilities
supported_contracts
supported_regions
supported_markets
supported_isolation_profiles
configuration_schema
health_contract
lifecycle
metadata
```

A provider declaration SHALL state what it **can** provide.

A binding SHALL state where it **does** provide it.

---

# 32. Provider Types

Initial provider types MAY include:

```text
BAOBAB_ENGINE
EXTERNAL_SERVICE
PLATFORM_NATIVE
ADAPTER
```

Provider type SHALL not affect canonical capability semantics.

---

# 33. Provider Declaration Example

```yaml
provider:
  key: baobab-trade.medusa

  type: BAOBAB_ENGINE

  engine: medusa

  capabilities:
    - key: commerce.order.create
      contracts:
        - "1.0"

    - key: commerce.catalogue.read
      contracts:
        - "1.0"

    - key: inventory.availability.read
      contracts:
        - "1.0"
```

This declares support.

It does not grant a tenant access.

---

# 34. Provider Configuration Schema

Providers MAY require configuration.

Example:

```text
currency defaults
sales channel
warehouse
provider account
external API profile
```

Shared SHALL define the schema reference.

CP MAY persist configuration or secure references as appropriate.

Secrets SHALL NOT be embedded in canonical contracts.

---

# 35. CapabilityBinding Contract

The canonical binding contract SHALL express:

```text
binding_id
capability_key
provider_key
engine_instance_id
scope
mode
priority
contract_version
effective_from
effective_to
status
configuration
version
```

Binding SHALL NOT contain tenant entitlement semantics except through its applicability scope.

---

# 36. Binding Modes

Initial canonical modes SHALL include:

```text
PRIMARY
FALLBACK
SHADOW
MIGRATION
DISABLED
```

Meaning SHALL be formally defined.

### PRIMARY

Normal provider.

### FALLBACK

May be used only when configured fallback conditions are satisfied.

### SHADOW

Receives permitted shadow traffic/results but SHALL not determine authoritative business outcome.

### MIGRATION

Used during controlled provider migration.

### DISABLED

Retained administratively but excluded from resolution.

---

# 37. Provider Health Contract

Provider health SHALL use a standard contract.

Recommended states:

```text
UNKNOWN
HEALTHY
DEGRADED
UNAVAILABLE
```

Health SHALL remain separate from provider lifecycle.

---

# 38. CapabilityResolution Contract

The canonical resolution result SHALL contain semantics equivalent to:

```yaml
resolution:
  resolution_id: ...
  context_id: ...

  principal_id: ...
  tenant_id: ...
  legal_entity_id: ...
  digital_estate_id: ...

  capability:
    key: commerce.order.create
    version: "1.0"

  grant_id: ...
  binding_id: ...

  provider:
    provider_id: ...
    engine_id: ...
    engine_instance_id: ...

  contract_version: "1.0"

  resolved_at: ...
  expires_at: ...

  correlation_id: ...
  provenance: ...
```

The response SHALL not expose raw secrets.

---

# 39. Resolution Decision Status

Canonical resolution results SHALL distinguish:

```text
RESOLVED
DENIED
UNAVAILABLE
AMBIGUOUS
INCOMPATIBLE
```

The exact status vocabulary SHALL be versioned.

---

# 40. Canonical Reason Codes

Shared SHALL maintain machine-readable reason codes.

Examples:

```text
CAPABILITY_UNKNOWN
CAPABILITY_INACTIVE

TENANT_UNKNOWN
TENANT_INACTIVE

LEGAL_ENTITY_INVALID

ESTATE_INVALID

GRANT_NOT_FOUND
GRANT_SUSPENDED
GRANT_REVOKED
GRANT_EXPIRED

DEPENDENCY_UNSATISFIED

BINDING_NOT_FOUND
BINDING_AMBIGUOUS
BINDING_EXPIRED

PROVIDER_UNAVAILABLE
PROVIDER_INCOMPATIBLE

CONTRACT_VERSION_UNSUPPORTED

ISOLATION_POLICY_MISMATCH
RESIDENCY_POLICY_MISMATCH
REGION_MISMATCH
MARKET_MISMATCH

IDENTITY_INVALID
AUTHORIZATION_DENIED

INTERNAL_RESOLUTION_ERROR
```

Applications SHALL NOT depend on free-form error messages.

---

# 41. Error Envelope

All capability-related APIs SHOULD use a canonical error envelope.

Conceptually:

```json
{
  "error": {
    "code": "BINDING_AMBIGUOUS",
    "message": "No deterministic capability provider could be selected.",
    "correlation_id": "...",
    "details": {}
  }
}
```

Human-readable messages MAY change.

Reason-code semantics SHALL be stable within a major contract version.

---

# 42. Event Vocabulary

Shared SHALL define capability lifecycle events.

At minimum:

```text
capability.registered
capability.updated
capability.deprecated
capability.retired

capability.grant.created
capability.grant.activated
capability.grant.suspended
capability.grant.revoked
capability.grant.expired

capability.provider.registered
capability.provider.updated
capability.provider.deprecated
capability.provider.retired

capability.binding.created
capability.binding.activated
capability.binding.updated
capability.binding.suspended
capability.binding.retired

capability.composition.created
capability.composition.updated
capability.composition.deprecated
```

---

# 43. Event Envelope

Events SHALL use the existing canonical event-envelope principles in Shared.

Capability events SHALL include where applicable:

```text
event_id
event_type
event_version
occurred_at
producer
correlation_id
causation_id
tenant_id
legal_entity_id
subject_id
schema_version
payload
```

Cross-tenant data SHALL not leak through event metadata.

---

# 44. Contract Ownership

Each capability SHALL declare an owning Baobab domain.

Example:

```text
commerce.order.create
owner: baobab-trade
```

Ownership means responsibility for:

- canonical semantics;
- contract evolution proposals;
- provider implementation conformance;
- compatibility testing.

Ownership SHALL NOT mean that Shared ceases to be the contract authority.

---

# 45. Cross-Domain Capabilities

Some capabilities span multiple domains.

These SHALL not automatically be assigned to CP.

Instead:

```text
business orchestration
       │
       ▼
appropriate domain/application service
       │
       ├── capability A
       ├── capability B
       └── capability C
```

CP SHALL resolve capabilities.

It SHALL not become the workflow coordinator merely because multiple capabilities participate.

---

# 46. Provider Conformance

A provider claiming a capability SHALL pass contract conformance tests.

For example:

```text
Provider declares:
commerce.order.create@1.x
        │
        ▼
Canonical contract tests
        │
        ├── request validation
        ├── response validation
        ├── error validation
        ├── tenancy propagation
        ├── correlation propagation
        └── event compatibility
        │
        ▼
CERTIFIED / FAILED
```

Provider registration SHOULD be prevented or marked unusable when mandatory conformance fails.

---

# 47. Consumer Conformance

Digital Estate APIs and other consumers SHOULD likewise validate their requests against canonical capability contracts.

This creates:

```text
Consumer
    │ canonical contract
    ▼
Provider
```

rather than:

```text
Consumer
    │ vendor-specific assumptions
    ▼
Provider
```

---

# 48. Generated Types

Because Baobab is polyglot, Shared SHOULD generate language bindings where beneficial.

Potential outputs include:

```text
Go
TypeScript
Java
Python
```

Generated code SHALL be derived from canonical contracts.

Generated code SHALL NOT become the canonical source.

The source contract remains authoritative.

---

# 49. Generated Artefact Rule

The pipeline SHALL be:

```text
Canonical Schema
      │
      ├──► Go types
      ├──► TypeScript types
      ├──► Java models
      ├──► Python models
      └──► documentation
```

Never:

```text
Go struct
   │
   └── manually rewrite four other languages
```

That invites drift.

---

# 50. Suggested Repository Structure

`nabhold/shared` SHOULD evolve toward:

```text
shared/
├── contracts/
│   │
│   ├── capability/
│   │   └── v1/
│   │       ├── capability.schema.json
│   │       ├── dependency.schema.json
│   │       ├── scope.schema.json
│   │       ├── grant.schema.json
│   │       ├── provider.schema.json
│   │       ├── binding.schema.json
│   │       ├── composition.schema.json
│   │       ├── resolution.schema.json
│   │       └── error.schema.json
│   │
│   ├── context/
│   ├── identity/
│   ├── authorization/
│   ├── tenancy/
│   ├── mapping/
│   ├── commerce/
│   ├── erp/
│   ├── trade/
│   ├── logistics/
│   ├── documents/
│   ├── intelligence/
│   └── events/
│
├── registry/
│   ├── capabilities/
│   ├── compositions/
│   └── reason-codes/
│
├── openapi/
├── asyncapi/
│
├── generated/
│   ├── go/
│   ├── typescript/
│   ├── java/
│   └── python/
│
├── tools/
│   ├── validate/
│   ├── compatibility/
│   ├── generate/
│   └── lint/
│
├── fixtures/
│
└── docs/
    ├── adr/
    ├── capability-catalogue/
    └── contract-governance/
```

The exact directory names MAY vary.

The responsibility boundaries SHALL not.

---

# 51. Canonical Registry vs Runtime Registry

The distinction SHALL be explicit.

## Shared

Contains declarative definitions such as:

```text
commerce.order.create exists
version 1 is defined
its canonical contract is X
its owner is Y
```

## Control Plane

Contains runtime state such as:

```text
Capability ID 123 represents commerce.order.create
Tenant A has grant G
Provider P supports it
Binding B applies in South Africa
Engine Instance E serves it
```

Shared SHALL not contain tenant runtime state.

---

# 52. Registry Validation

CI SHALL validate:

```text
duplicate capability keys
invalid namespaces
invalid versions
missing owners
missing schemas
broken schema references
circular dependencies
circular compositions
unknown capabilities
invalid reason codes
breaking changes without major version
invalid provider declarations
```

A registry failing validation SHALL not be published.

---

# 53. Contract Change Classification

Every contract change SHALL be classified as:

```text
NON_BREAKING
BREAKING
DEPRECATION
DOCUMENTATION_ONLY
```

CI SHOULD automatically detect obvious structural breaking changes.

Human architecture review SHALL remain required for semantic breaking changes.

---

# 54. Deprecation Policy

Capability deprecation SHALL be explicit.

A deprecated capability SHOULD identify:

```text
deprecated_at
replacement
migration_guidance
minimum_support_until
```

Where no replacement exists, that SHALL be stated.

Deprecated does not mean immediately unavailable.

---

# 55. Retirement Policy

Before retirement, architecture tooling SHOULD be able to determine:

```text
Which compositions include this capability?
Which providers implement it?
Which grants reference it?
Which Digital Estates depend on it?
```

Retirement SHALL not proceed blindly.

---

# 56. Supplier-Domain Remodel

The existing supplier-domain implementation inside Shared SHALL be reviewed against this ADR.

Shared MAY retain:

```text
Supplier schemas
Supplier identifiers
Supplier events
Supplier lifecycle vocabulary
Supplier capability contracts
Supplier verification contract
```

Shared SHALL NOT become authoritative for runtime logic such as:

```text
whether supplier X passes vetting
whether an application is approved
how certification is evaluated
how a supplier state transition executes
```

Those require an explicit domain owner.

---

# 57. Business Logic Prohibition

The following SHALL NOT be placed in Shared merely for reuse:

```text
pricing calculations
supplier approval algorithms
inventory allocation
payment routing logic
trade workflow execution
invoice posting logic
shipment state machines
commodity scoring
customer refund rules
```

Reuse does not justify collapsing domain ownership.

---

# 58. Canonical Data vs Canonical Behaviour

Shared MAY define:

```text
canonical request
canonical response
canonical event
canonical state vocabulary
canonical identifier
```

Shared SHALL NOT necessarily implement:

```text
the behaviour producing that state
```

Example:

```text
Shared:
SupplierStatus = APPROVED

Domain:
logic determining whether supplier becomes APPROVED
```

---

# 59. IAM Relationship

Shared SHALL define IAM/CP interoperability contracts without moving capability authorization into IAM.

The relationship SHALL remain:

```text
IAM
 │
 │ authenticated identity + coarse scopes
 ▼
CP
 │
 │ tenant/context + capability entitlement
 ▼
Domain
 │
 │ business authorization
 ▼
Action
```

Capability contracts SHALL NOT require a one-to-one Keycloak role for every capability.

---

# 60. Identity Context Contract

Shared SHOULD define a canonical identity-context reference usable by CP.

Conceptually:

```text
IdentityContext
├── principal_id
├── subject
├── principal_type
├── authentication_assurance
├── client_id
├── workload_identity
├── scopes
└── token_provenance
```

Tenant/legal-entity authority SHALL not be inferred solely from unverified client claims.

---

# 61. Digital Estate Contract

Shared SHOULD define the minimum canonical Digital Estate identity needed for capability consumption.

Conceptually:

```text
DigitalEstateRef
├── estate_id
├── estate_key
├── tenant_id
├── legal_entity_context
├── channel
└── properties
```

Digital Estate business configuration SHALL remain outside Shared unless it is cross-platform contract vocabulary.

---

# 62. B2B and B2C SHALL NOT Be Tenant Types

The contract model SHALL NOT define:

```text
tenant_type = B2B
```

or:

```text
tenant_type = B2C
```

as a universal architectural constraint.

A tenant MAY operate both.

B2B/B2C SHALL instead emerge through:

```text
composition
channel
capabilities
context
```

---

# 63. Domestic and Cross-Border SHALL NOT Be Tenant Types

Similarly:

```text
domestic
cross-border
```

SHALL not define mutually exclusive tenant classes.

A tenant MAY conduct both.

The difference SHALL be represented through capability composition and operation context.

---

# 64. Legal Footprint SHALL NOT Equal Market Footprint

Canonical contracts SHALL preserve the distinction:

```text
LegalEntity
        ≠
Market
        ≠
Country
        ≠
OperatingRegion
        ≠
Transaction Geography
```

This is mandatory for cross-border businesses.

---

# 65. XBT Example — ZuriBeans

```text
solution.baobab-xbt
        +
profile.b2b
        +
profile.crossborder
        +
profile.commodity-trade
        +
profile.supplier-management
```

The flattened capability graph may include:

```text
organisation.account.manage
supplier.onboarding.manage
commercial.rfq.manage
commercial.quotation.manage
pricing.negotiated.resolve
commerce.order.manage
inventory.availability.read
trade.execution.manage
logistics.shipment.manage
documents.trade.manage
finance.invoice.manage
finance.receivable.manage
finance.settlement.manage
intelligence.commodity.query
intelligence.fx.query
```

Nothing in these canonical names SHALL depend on ZuriBeans.

---

# 66. XBT Example — Coal Haulier

```text
solution.baobab-xbt
        +
profile.b2b
        +
profile.crossborder
        +
profile.logistics
```

Potential capabilities:

```text
organisation.customer.manage
commercial.contract.manage
pricing.service.resolve
logistics.transport-order.manage
logistics.load.manage
logistics.dispatch.manage
logistics.route.manage
logistics.border-milestone.manage
logistics.delivery.manage
documents.pod.manage
finance.invoice.manage
finance.receivable.manage
finance.job-profitability.calculate
intelligence.route-risk.assess
```

No capability SHALL require that the haulier possess a legal entity in every country traversed.

---

# 67. XBT Example — Petroleum Trader

```text
solution.baobab-xbt
        +
profile.b2b
        +
profile.crossborder
        +
profile.commodity-trade
```

Potential capabilities:

```text
counterparty.onboarding.manage
counterparty.due-diligence.manage
commercial.opportunity.manage
commercial.offer.manage
commercial.contract.manage
trade.execution.manage
logistics.shipment.manage
documents.inspection.manage
documents.trade.manage
finance.settlement.manage
finance.trade-profitability.calculate
intelligence.commodity.query
intelligence.fx.query
intelligence.regulatory.query
intelligence.risk.assess
```

Again, these are platform capabilities rather than oil-specific provider APIs.

---

# 68. Thamani Example

```text
platform.core
      +
profile.b2c
      +
profile.supplier-management
```

Potential capabilities:

```text
identity.customer.authenticate
customer.profile.manage
commerce.catalogue.read
commerce.cart.manage
commerce.checkout.execute
commerce.promotion.apply
payment.authorize
fulfilment.order.manage
returns.manage
supplier.onboarding.manage
content.publish
```

This demonstrates that the same capability architecture does not require every consumer to be B2B or cross-border.

---

# 69. Provider Replacement

The contract architecture SHALL permit:

```text
Digital Estate
      │
      ▼
Canonical Capability
      │
      ▼
CP
      │
      ├── Provider A today
      │
      └── Provider B tomorrow
```

without changing the meaning of the Digital Estate's requested capability.

This is a principal measure of architectural success.

---

# 70. External Providers

Future capabilities MAY be implemented by approved third-party services.

Example:

```text
counterparty.sanctions.screen
             │
             ▼
       external provider
```

Shared SHALL define the canonical contract.

The provider adapter SHALL translate it.

Digital Estates SHALL not become coupled directly to the third-party contract unless explicitly approved.

---

# 71. Contract Test Kits

Shared SHOULD publish conformance test kits.

Example:

```text
Capability Contract
       │
       ├── request fixtures
       ├── response fixtures
       ├── invalid fixtures
       ├── error fixtures
       ├── event fixtures
       └── compatibility tests
```

Provider repositories SHALL execute these tests in CI.

---

# 72. Polyrepo Governance

A Shared contract release SHALL be consumable independently by repositories.

The platform SHALL avoid requiring every repository to be released simultaneously for backward-compatible contract changes.

Breaking changes SHALL use controlled migration.

---

# 73. Contract Publication

Shared SHOULD publish versioned artefacts suitable for the ecosystem, for example:

```text
GitHub releases
language packages
schema bundles
OpenAPI bundles
AsyncAPI bundles
checksums
release notes
```

Exact registries SHALL be decided separately.

---

# 74. Dependency Pinning

Consumers SHALL pin compatible Shared contract versions.

They SHALL NOT silently consume unreviewed breaking changes from `main`.

---

# 75. Contract Provenance

Generated artefacts SHOULD expose:

```text
shared release version
source schema version
generation timestamp
source commit
```

This SHALL aid audit and debugging.

---

# 76. Security Classification

Capability contracts SHALL be able to declare expected data classification.

Recommended baseline:

```text
PUBLIC
INTERNAL
TENANT_CONFIDENTIAL
RESTRICTED
```

Classification metadata SHALL inform—but not replace—runtime security policy.

---

# 77. Sensitive Fields

Schemas SHALL identify sensitive fields where practical.

Examples:

```text
PII
financial
credential reference
commercial confidential
restricted
```

Logging guidance SHOULD be derivable from schema metadata.

---

# 78. Correlation and Traceability

Cross-engine capability contracts SHALL propagate:

```text
correlation_id
```

and SHOULD support:

```text
causation_id
trace context
```

according to platform observability standards.

---

# 79. Idempotency

Mutation capabilities SHOULD declare whether they require an idempotency key.

Example:

```text
commerce.order.create
requires_idempotency = true
```

Canonical idempotency semantics SHALL be defined once rather than reinvented per engine.

---

# 80. Pagination

Read/list capability contracts SHALL use canonical pagination conventions.

Shared SHALL define:

```text
cursor semantics
page limits
ordering
continuation
```

rather than allowing every engine to expose incompatible conventions.

---

# 81. Money

Financial contracts SHALL use canonical money representation.

Conceptually:

```text
Money
├── amount
└── currency
```

Floating-point representation SHALL NOT be used for canonical monetary values.

Exact representation SHALL be specified in the relevant financial contract ADR.

---

# 82. Units and Quantities

Commodity and logistics capabilities SHALL use canonical quantity/unit contracts.

Examples include:

```text
kg
metric tonne
litre
barrel
kilometre
```

The contract SHALL distinguish:

```text
quantity
unit
```

and SHALL NOT encode them in ambiguous free-form strings.

---

# 83. Countries and Currencies

Canonical contracts SHOULD use standards-based codes.

Examples:

```text
country: ISO 3166-1 alpha-2
currency: ISO 4217
```

Exceptions SHALL be explicitly documented.

---

# 84. Time

Canonical timestamps SHALL use an unambiguous UTC-capable representation.

Business timezone SHALL remain explicit where business semantics require it.

---

# 85. Contract Documentation

Every capability SHALL be documentable as:

```text
Name
Purpose
Owner
Consumers
Request
Response
Errors
Events
Dependencies
Scope
Security
Idempotency
Version
Maturity
Lifecycle
Provider implementations
Examples
```

This SHOULD generate a browsable Baobab Capability Catalogue.

---

# 86. Capability Catalogue

The capability catalogue SHALL eventually answer:

```text
What can Baobab do?

Which capabilities exist?

Which are supported?

Which contracts define them?

Which domain owns them?

Which providers implement them?

Which compositions require them?
```

The catalogue SHALL be generated from canonical registry data rather than maintained manually in a disconnected spreadsheet.

---

# 87. Capability Catalogue Illustration

```text
BAOBAB CAPABILITY CATALOGUE

Commerce
├── catalogue.read
├── order.create
├── order.cancel
└── checkout.execute

Pricing
├── standard.resolve
└── negotiated.resolve

Supplier
├── onboarding.manage
└── verification.manage

Finance
├── invoice.issue
├── receivable.read
└── settlement.manage

Logistics
├── shipment.manage
├── route.manage
└── delivery.manage

Intelligence
├── fx.query
├── commodity.query
├── market.query
└── risk.assess
```

---

# 88. Architectural Validation Matrix

Before a capability is accepted into Shared, reviewers SHALL ask:

| Question | Required |
|---|---|
| Is it implementation-neutral? | Yes |
| Is it tenant-neutral? | Yes |
| Is ownership clear? | Yes |
| Is the contract versioned? | Yes |
| Are request/response semantics defined? | Yes |
| Are errors defined? | Yes |
| Is scope defined? | Yes |
| Are dependencies known? | Yes |
| Can providers conform-test it? | Yes |
| Does it duplicate another capability? | No |
| Does it put business logic in Shared? | No |
| Does it expose vendor-native concepts unnecessarily? | No |

---

# 89. Architectural Smell Tests

The following SHALL trigger review.

### Vendor in canonical capability name

```text
medusa.*
idempiere.*
payload.*
```

### Tenant in capability name

```text
zuribeans.*
thamani.*
```

### Runtime logic in Shared

```text
approveSupplier()
allocateInventory()
calculateInvoice()
```

### Capability without contract

```text
"we support logistics"
```

### Provider without explicit capability declaration

```text
"this engine probably handles it"
```

### Grant inferred from binding

```text
binding exists therefore tenant is allowed
```

All are architectural smells.

---

# 90. Migration Policy

Because Baobab has no production data, Shared contracts MAY be remodelled aggressively where necessary.

The team SHALL prefer:

```text
correct canonical model now
```

over:

```text
permanent compatibility with incorrect prototypes
```

However, contract migration SHALL remain deliberate and documented.

---

# 91. Implementation Gates

## Gate 0 — Inventory

Catalogue existing Shared:

```text
schemas
contracts
events
supplier-domain code
tenancy contracts
authorization contracts
control-plane contracts
ERP contracts
mapping contracts
```

Classify each as:

```text
KEEP
REMODEL
MOVE
DEPRECATE
DELETE
```

---

## Gate 1 — Capability Core Schemas

Implement:

```text
CapabilityDefinition
CapabilityDependency
CapabilityScope
CapabilityGrant
CapabilityProvider
CapabilityBinding
CapabilityComposition
CapabilityResolution
```

---

## Gate 2 — Registry

Create canonical capability and composition registry structures.

---

## Gate 3 — Versioning and Compatibility

Implement schema validation and breaking-change detection.

---

## Gate 4 — Reason Codes

Implement canonical reason-code registry.

---

## Gate 5 — Events

Implement capability lifecycle AsyncAPI contracts.

---

## Gate 6 — Generated Types

Generate supported language bindings.

---

## Gate 7 — Conformance Tooling

Implement consumer/provider contract tests.

---

## Gate 8 — Supplier Domain Cleanup

Separate contracts from runtime domain behaviour.

---

## Gate 9 — CP Adoption

Migrate `baobab-cp` to consume the canonical Shared definitions.

CP SHALL NOT maintain competing hand-written semantic equivalents.

---

## Gate 10 — Provider Adoption

Migrate:

```text
baobab-trade
baobab-erp
baobab-pulse
baobab-cms
```

to declare and conform to capabilities they actually provide.

---

## Gate 11 — IAM Validation

Ensure capability architecture does not leak into Keycloak role proliferation.

---

## Gate 12 — Digital Estate Validation

Validate at least:

```text
ZuriBeans
Thamani
coal-haulage reference model
petroleum-trading reference model
```

against the capability catalogue.

---

## Gate 13 — Documentation

Generate capability catalogue and architecture documentation.

---

## Gate 14 — Production Readiness

Require:

```text
schema validation
compatibility tests
provider conformance
consumer conformance
dependency validation
composition validation
security review
multi-tenant tests
documentation
```

---

# 92. Definition of Done

This ADR SHALL be considered implemented when:

1. Shared contains a canonical capability model.
2. Capability identity is implementation-neutral.
3. Capability scopes are canonical.
4. Capability grants have canonical contracts.
5. Capability bindings have canonical contracts.
6. Providers declare supported capabilities and versions.
7. Capability compositions are declarative and validated.
8. Baobab XBT can be represented without creating an XBT orchestration service.
9. B2B, B2C, domestic and cross-border scenarios can be composed without tenant-type hard-coding.
10. CP consumes Shared contracts.
11. Engines conform to capability contracts.
12. Digital Estates can consume canonical interfaces without knowing provider vendors.
13. Shared contains no authoritative runtime capability state.
14. Shared contains no inappropriate business workflow implementation.
15. CI prevents incompatible contract drift.

---

# 93. Non-Goals

This ADR does NOT:

- assign every future capability;
- create a workflow engine;
- create an ESB;
- create another runtime service;
- make Shared responsible for tenant state;
- replace domain-specific ADRs;
- define every logistics process;
- define every commodity process;
- define every B2C workflow;
- make CP the owner of business entities;
- make IAM the business authorization system.

It establishes the **language and governance model** under which those capabilities can evolve safely.

---

# 94. Consequences

## Positive

The decision provides:

- one platform vocabulary;
- reduced polyrepo drift;
- vendor independence;
- Digital Estate portability;
- provider replaceability;
- explicit compatibility;
- safer multi-engine integration;
- composable B2B/B2C models;
- composable domestic/cross-border models;
- stronger SaaS packaging;
- machine-verifiable contracts;
- clearer architecture governance.

## Costs

The decision requires:

- contract discipline;
- schema governance;
- generated artefacts;
- compatibility tooling;
- provider conformance tests;
- refactoring existing Shared structures;
- repository-wide adoption.

These costs are accepted.

---

# 95. Rejected Alternatives

## Shared as generic utility library

Rejected.

Shared is strategically more important as a canonical contract authority.

## CP owns all schema definitions

Rejected.

This would couple cross-platform contracts to one runtime implementation.

## Each engine defines its own capability vocabulary

Rejected.

This destroys portability.

## Digital Estates use provider-native APIs as canonical APIs

Rejected.

This recreates vendor coupling.

## Shared implements reusable business workflows

Rejected.

This creates a distributed monolith disguised as reuse.

---

# 96. Final Architecture

```text
                     NABHOLD / BAOBAB

                    CONTRACT AUTHORITY
                    nabhold/shared
                          │
             ┌────────────┼────────────┐
             │            │            │
        Capabilities    Contexts     Events
             │            │            │
             └────────────┼────────────┘
                          │
                          ▼
                  BAOBAB CONTROL PLANE
                     runtime authority
                          │
        ┌─────────────────┼──────────────────┐
        │                 │                  │
     Grants            Bindings          Resolution
        │                 │                  │
        └─────────────────┼──────────────────┘
                          │
                          ▼
                   CAPABILITY PROVIDERS
             ┌────────────┼───────────────┐
             │            │               │
           Trade         ERP            Pulse
             │            │               │
           Medusa      iDempiere       Haystack
             │            │               │
             └────────────┼───────────────┘
                          │
                          ▼
                    DIGITAL ESTATES

       ZuriBeans | Thamani | Coal | Oil | Future
```

---

# 97. Decision

**ACCEPTED TARGET CONTRACT ARCHITECTURE, subject to formal approval.**

Upon approval:

1. this ADR SHALL govern capability-contract development in `nabhold/shared`;
2. Shared SHALL remain the canonical contract authority;
3. CP SHALL become the runtime authority implementing these contracts;
4. engine repositories SHALL implement provider contracts rather than invent competing capability semantics;
5. Digital Estates SHALL consume canonical capabilities rather than vendor identities;
6. existing Shared structures SHALL be audited and remodelled before production;
7. supplier-domain runtime behaviour SHALL be reviewed and relocated where necessary;
8. capability registry validation SHALL become mandatory CI;
9. breaking capability changes SHALL require explicit versioning and architecture review;
10. Baobab XBT SHALL be representable as capability composition rather than another orchestration service.

---

# 98. Architectural Maxim

> **Shared defines the language. CP makes the platform decision. Providers perform the work. Digital Estates consume the capability.**

Together with ADR-BCP-002, this is the foundation of Baobab's capability-centric architecture.