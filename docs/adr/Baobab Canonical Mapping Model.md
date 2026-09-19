# Baobab Canonical Mapping Model

**Document Type:** Platform Architecture Specification  
**Status:** Proposed Canonical Architecture  
**Architecture Domain:** Control Plane / Canonical Identity / Context / Mapping / Engine Integration  
**Applies To:** Baobab Platform, all Baobab engines, all digital estates, `baobab-platform/shared`, integration services, future products and external integrations  
**Target Maturity:** Production-grade, multi-tenant, multi-market, multi-region, polyrepo, polyglot enterprise platform

---

## 1. Purpose

The Baobab Canonical Mapping Model defines how the Baobab Platform identifies, relates, resolves, scopes and governs business concepts that are represented independently across:

- the Baobab Control Plane;
- digital estates;
- Payload CMS;
- MedusaJS;
- iDempiere;
- future Baobab engines;
- external SaaS platforms;
- partner systems;
- data platforms;
- regional deployments;
- market-specific configurations.

The fundamental architectural requirement is:

> **Canonical identity is global; operational representation is local; context determines which representation is valid.**

The model prevents individual engines from becoming the enterprise source of identity and prevents Baobab from coupling itself to engine-specific database models.

The platform therefore standardises **contracts and identity**, not implementation technologies.

Existing Baobab architecture already separates the tenant boundary from organisation structure: tenancy answers whose security and operational boundary applies, whereas the organisation model describes the organisation itself. That separation remains foundational to this model.

The earlier architecture also established that specialised engines retain operational ownership of their native representations while shared platform contracts provide identity, tenancy, organisation, APIs, events and governance.

This specification supersedes earlier references to ERPNext/Frappe as Baobab's ERP implementation. The current ERP engine is **iDempiere**. The canonical model deliberately remains implementation-neutral so that changing an engine does not require redesigning the platform.

---

# 2. Scope

The Canonical Mapping Model defines the following first-class platform concepts:

1. `CanonicalEntity`
2. `ExternalReference`
3. `Mapping`
4. `MappingScope`
5. `Market`
6. `DigitalEstate`
7. `Engine`
8. `EngineInstance`
9. `Capability`
10. `CapabilityBinding`
11. `Context`
12. `IsolationProfile`

It additionally defines:

- identifiers;
- ownership;
- authority;
- cardinalities;
- temporal validity;
- inheritance;
- precedence;
- mapping resolution;
- lifecycle states;
- conflict management;
- data integrity;
- auditability;
- contract versioning;
- API behaviour;
- event behaviour;
- security;
- tenancy;
- isolation;
- caching;
- observability;
- migration;
- governance.

The model does **not** make Baobab the operational system of record for commerce, content, ERP or other engine-owned business transactions.

---

# 3. Architectural Goals

The model MUST support all of the following without redesigning the platform:

- multiple legal entities;
- one or many tenant boundaries;
- multiple businesses under a group;
- multiple digital estates per business;
- multiple domains per estate;
- B2B and B2C commerce;
- multiple markets;
- overlapping markets;
- multiple countries per market;
- multiple markets within one country;
- multiple currencies;
- different transaction and accounting currencies;
- multiple languages and locales;
- local and regional catalogues;
- multiple sales channels;
- different warehouses and fulfilment strategies;
- multiple ERP organisations;
- multiple engine instances;
- different isolation levels;
- geographic deployment;
- data residency;
- engine replacement;
- engine migration;
- phased tenant migration;
- blue/green engine instances;
- acquisitions;
- divestitures;
- mergers;
- legal-entity restructuring;
- new digital channels;
- mobile applications;
- external partners;
- future Baobab products.

The architecture MUST NOT assume that:

- tenant equals legal entity;
- country equals market;
- market equals digital estate;
- digital estate equals domain;
- engine equals capability;
- capability equals implementation;
- one canonical entity has only one external representation;
- one external entity has only one canonical relationship;
- one currency applies everywhere;
- every tenant requires the same isolation strategy;
- every engine uses the same database;
- every digital estate uses the same technology;
- every deployment is in the same geographic region.

---

# 4. Core Architectural Principles

## 4.1 Canonical identity before integration identity

Every business concept that crosses a platform boundary MUST be addressable by a Baobab canonical identity.

Engine-native identifiers MUST NOT become canonical enterprise identifiers.

For example:

```text
Baobab canonical product
        │
        ├── Payload document
        ├── Medusa product
        ├── iDempiere M_Product
        └── Analytics representation
```

The native identifiers remain authoritative within their respective systems.

---

## 4.2 Engines own operational state

Operational ownership remains with the appropriate engine.

Examples:

```text
Payload CMS
    → editorial content
    → pages
    → media metadata
    → localisation content

MedusaJS
    → commerce catalogue
    → carts
    → orders
    → sales channels
    → commerce pricing execution

iDempiere
    → accounting
    → financial postings
    → ERP inventory
    → business partners
    → ERP organisations
    → procurement
```

The Control Plane owns relationships between those representations, not their internal transactional models.

---

## 4.3 Mappings are explicit

Cross-system relationships MUST be represented explicitly.

No service may infer identity equality merely because two systems use:

- the same name;
- the same SKU;
- the same email address;
- the same business registration number;
- the same slug;
- the same domain;
- coincidentally matching numeric IDs.

Matching attributes may be used for reconciliation, but not as permanent canonical identity.

---

## 4.4 Context is explicit

Context MUST accompany operations that require scoped interpretation.

Context MUST NOT depend solely on ambient process state, database connection state or implicit global variables.

---

## 4.5 Scope is composable

Baobab MUST avoid Cartesian-product configuration models.

Tenant, market, region, currency, estate, channel and other dimensions are independently modelled and composed during context resolution.

---

## 4.6 Configuration inherits; identity does not

Configuration may inherit from broader scopes.

Canonical identity MUST NOT be inherited.

An object either has a canonical identity or it does not.

---

## 4.7 History is preserved

Mappings that have participated in material transactions MUST generally be retired rather than deleted.

Historical resolution MUST remain possible.

---

## 4.8 Isolation is independent of business structure

Isolation strength is selected according to requirements.

A legal entity may commonly represent the default tenant boundary, but neither concept is defined in terms of the other.

---

# 5. High-Level Domain Model

```text
                         CanonicalEntity
                              │
                 ┌────────────┴────────────┐
                 │                         │
          ExternalReference             Mapping
                 │                         │
                 │                  MappingScope
                 │                         │
                 └─────────────┬───────────┘
                               │
                            Context
                               │
         ┌─────────────────────┼─────────────────────┐
         │                     │                     │
       Market             DigitalEstate       CapabilityBinding
                                                     │
                                              ┌──────┴──────┐
                                              │             │
                                         Capability      Engine
                                                           │
                                                    EngineInstance
                                                           │
                                                    IsolationProfile
```

This diagram represents relationships, not table inheritance.

---

# 6. Identifier Architecture

Baobab SHOULD use opaque, globally unique canonical identifiers.

Recommended implementation:

- UUIDv7 where supported;
- alternatively another collision-resistant sortable identifier;
- human-readable keys kept separately.

Example:

```text
id: 019c...
canonical_key: product:thamani:ethiopia-guji-60kg
```

The machine identifier MUST be immutable.

The canonical key SHOULD also normally be immutable after publication, even when the display name changes.

Identifiers MUST NOT expose:

- database sequence assumptions;
- tenant count;
- confidential business structure;
- engine implementation details.

Every externally serialised canonical object SHOULD expose:

```text
id
canonical_key
type
status
schema_version
```

---

# 7. CanonicalEntity

## 7.1 Definition

`CanonicalEntity` is the Baobab-wide identity of a concept that must remain recognisable across one or more systems, domains, markets, estates or time periods.

It answers:

> **What thing are these different representations referring to?**

It does not necessarily contain the complete operational record.

---

## 7.2 Examples

Canonical entity types may include:

```text
Organisation
LegalEntity
BusinessUnit
Party
Person
Product
ProductFamily
Service
Brand
Location
Warehouse
Asset
Document
Campaign
Catalogue
CustomerAccount
SupplierAccount
Contract
Market
DigitalEstate
Currency
Country
OperatingRegion
GeographicRegion
```

Not every internal engine row should receive a canonical identity.

Canonicalisation is warranted where cross-boundary identity matters.

---

## 7.3 Recommended fields

```text
CanonicalEntity
---------------
id
canonical_key
entity_type
subtype
display_name
owner_tenant_id
owner_legal_entity_id
authority
status
classification
schema_version
metadata
effective_from
effective_to
created_at
created_by
updated_at
updated_by
retired_at
retired_by
version
```

---

## 7.4 Authority

`authority` identifies which Baobab domain controls the semantic definition.

Examples:

```text
control-plane
organisation-registry
trade
erp
content
identity
external
```

Authority does not necessarily mean physical storage location.

---

## 7.5 Cardinalities

```text
CanonicalEntity 1 ─── 0..* ExternalReference

CanonicalEntity 1 ─── 0..* Mapping

CanonicalEntity * ─── * CanonicalEntity
                       through explicit relationships
```

A canonical entity MAY exist before any external representation exists.

---

## 7.6 Invariants

A canonical entity MUST:

- have exactly one immutable canonical ID;
- have exactly one entity type at a time;
- have a lifecycle state;
- have an authority;
- be tenant-scoped where ownership requires it;
- never silently change semantic identity.

A product cannot simply be changed into a warehouse by updating `entity_type`.

---

# 8. ExternalReference

## 8.1 Definition

`ExternalReference` identifies a native object in a system outside the canonical registry.

Examples:

```text
Payload document ID
Medusa product ID
Medusa customer ID
iDempiere M_Product_ID
iDempiere C_BPartner_ID
external CRM ID
government registry number
legacy-system identifier
```

---

## 8.2 Recommended fields

```text
ExternalReference
-----------------
id
system_namespace
engine_id
engine_instance_id
environment
native_entity_type
native_id
native_key
native_uri
source_authority
fingerprint
status
metadata
first_seen_at
last_verified_at
created_at
updated_at
```

---

## 8.3 Composite uniqueness

At minimum:

```text
engine_instance_id
+
native_entity_type
+
native_id
```

SHOULD uniquely identify an active native reference.

Additional namespace information MAY be required for APIs whose IDs are only locally unique.

---

## 8.4 External reference ≠ mapping

This distinction is mandatory.

`ExternalReference` says:

> this object exists in system X.

`Mapping` says:

> this object corresponds to canonical entity Y under these semantics and scope.

Keeping them separate enables reconciliation before identity is confirmed.

---

# 9. Mapping

## 9.1 Definition

`Mapping` is a governed relationship between canonical identity and another representation, or between two canonical concepts where an explicit translation relationship is required.

It answers:

> **How does this canonical concept correspond to another representation under a particular context?**

---

## 9.2 Recommended fields

```text
Mapping
-------
id
mapping_type
canonical_entity_id
external_reference_id
target_canonical_entity_id
scope_id
direction
cardinality
authority
confidence
resolution_priority
status
effective_from
effective_to
supersedes_mapping_id
metadata
mapping_version
created_at
created_by
approved_at
approved_by
retired_at
retired_by
```

Exactly one of:

```text
external_reference_id
target_canonical_entity_id
```

would normally be populated, unless a specialised mapping type explicitly allows otherwise.

---

## 9.3 Mapping types

Initial recognised types SHOULD include:

```text
IDENTITY
REPRESENTATION
ORGANISATIONAL
CONTENT
COMMERCE
ERP
CATALOGUE
PRICING
TAX
WAREHOUSE
FULFILMENT
PAYMENT
DOMAIN
LOCALE
CURRENCY
CHANNEL
CAPABILITY
INTEGRATION
MIGRATION
ALIAS
SUCCESSOR
```

---

## 9.4 Direction

Mappings declare direction:

```text
BIDIRECTIONAL
CANONICAL_TO_EXTERNAL
EXTERNAL_TO_CANONICAL
SOURCE_TO_TARGET
```

Identity equivalence should usually be bidirectionally resolvable.

Transformational mappings may not be.

---

## 9.5 Cardinalities

The model MUST support:

```text
1 : 1
1 : N
N : 1
N : M
```

Example:

```text
one canonical product
        →
several Medusa representations

several storefront domains
        →
one DigitalEstate

several regional ERP organisations
        →
one canonical operating structure
```

---

## 9.6 Mapping confidence

For imported or reconciled mappings:

```text
CONFIRMED
PROBABLE
CANDIDATE
REJECTED
```

Production runtime resolution MUST NOT normally consume `CANDIDATE` mappings.

---

## 9.7 Mapping precedence

Mappings may carry:

```text
resolution_priority
```

but specificity MUST normally outrank manual arbitrary priority.

Recommended precedence:

```text
validity
  ↓
status
  ↓
scope specificity
  ↓
explicit override
  ↓
resolution priority
  ↓
deterministic tie-break
```

Ambiguous equally specific authoritative mappings SHOULD cause resolution failure rather than random selection.

---

# 10. MappingScope

## 10.1 Definition

`MappingScope` defines the dimensions within which a mapping is applicable.

A mapping without an appropriate scope is potentially dangerous because identical canonical concepts may legitimately have different representations in different operating contexts.

---

## 10.2 Scope dimensions

The model SHOULD support:

```text
tenant
legal_entity
organisation
business_unit
operating_region
geographic_region
market
country
estate
property/domain
channel
currency
locale
catalogue
customer_segment
engine
engine_instance
environment
deployment_region
```

Not every MappingScope populates every field.

---

## 10.3 Scope matching

A mapping matches Context when every explicitly declared scope dimension is compatible with that Context.

Example:

```text
mapping scope:
    tenant = thamani
    market = kenya-b2b

context:
    tenant = thamani
    legal_entity = thamani-global
    market = kenya-b2b
    country = KE
    currency = KES
```

The mapping matches.

A scope with:

```text
market = south-africa-b2b
```

does not.

---

## 10.4 Specificity

A more constrained scope SHOULD outrank a broader compatible scope.

Example:

```text
Tenant default
    ↓
Legal entity
    ↓
Operating region
    ↓
Market
    ↓
Estate
    ↓
Channel
```

This hierarchy is not simply based on number of fields. Baobab SHOULD maintain an explicit dimension precedence policy.

---

## 10.5 Exclusions

Scopes SHOULD support explicit exclusions where necessary:

```text
include_countries = [KE, UG, TZ]
exclude_countries = [TZ]
```

However, excessive exclusion logic is a smell. Distinct markets are preferable when commercial behaviour materially differs.

---

# 11. Market

## 11.1 Definition

A `Market` is a commercial operating context.

A Market is **not synonymous with country or region**.

Examples:

```text
South Africa B2B
South Africa Consumer
Kenya Wholesale
East Africa Distributor
EAC Institutional
EU Export
Global Corporate
```

A single country may contain multiple markets.

A single market may span multiple countries.

---

## 11.2 Recommended fields

```text
Market
------
id
canonical_key
name
market_type
owner_tenant_id
legal_entity_id
operating_region_id
parent_market_id
default_country
countries[]
default_currency
allowed_currencies[]
accounting_context
default_locale
supported_locales[]
timezone
tax_profile_id
pricing_policy_id
catalogue_policy_id
payment_policy_id
fulfilment_policy_id
regulatory_profile_id
status
effective_from
effective_to
metadata
```

---

## 11.3 Parent-child markets

Markets MAY form hierarchies:

```text
East Africa B2B
├── Kenya B2B
├── Uganda B2B
└── Tanzania B2B
```

A parent market can supply defaults.

Children can override them.

---

## 11.4 Commerce engine relationships

Medusa currently models regions with currency and country-specific settings, and sales channels represent online/offline product-selling channels. These native concepts should therefore be mapped to Baobab Market/Channel concepts rather than treated as Baobab's canonical definitions.

Thus:

```text
Baobab Market
      │
      ├── Medusa Region
      └── Medusa Sales Channel(s)
```

is legitimate.

Baobab MUST NOT assume `Market == Medusa Region`.

---

# 12. DigitalEstate

## 12.1 Definition

`DigitalEstate` represents a coherent digital presence owned or operated for a business.

A DigitalEstate is an experience boundary, not necessarily a tenant boundary or legal boundary.

Examples:

```text
Thamani B2C Estate
ZuriBeans Estate
Baobab-Platform Corporate Estate
future mobile commerce estate
dealer portal
supplier portal
```

---

## 12.2 Recommended fields

```text
DigitalEstate
-------------
id
canonical_key
name
owner_tenant_id
owner_legal_entity_id
brand_id
estate_type
parent_estate_id
default_market_id
default_locale
default_currency
status
metadata
created_at
updated_at
```

---

## 12.3 Digital properties

Domains, apps and other entry points SHOULD be separate child resources:

```text
DigitalEstate
     │
     └── DigitalProperty 1..*
            │
            ├── domain
            ├── subdomain
            ├── mobile application
            ├── partner portal
            └── API channel
```

This avoids equating an estate with its current hostname.

---

## 12.4 Cardinalities

```text
LegalEntity 1 ─── 0..* DigitalEstate

DigitalEstate 1 ─── 1..* DigitalProperty

DigitalEstate * ─── * Market

DigitalEstate * ─── * CapabilityBinding
```

A single market can be served by several estates.

A single estate can serve multiple markets.

---

# 13. Engine

## 13.1 Definition

`Engine` describes a platform implementation type capable of providing one or more capabilities.

Examples:

```text
Payload CMS
MedusaJS
iDempiere
future intelligence engine
future document engine
future logistics engine
```

Engine describes a product/implementation class, not a running deployment.

---

## 13.2 Recommended fields

```text
Engine
------
id
engine_key
name
engine_type
vendor
technology
distribution
ownership
supported_capabilities[]
supported_contract_versions[]
protocols[]
support_status
minimum_supported_version
recommended_version
metadata
```

---

## 13.3 Engine types

Suggested controlled values:

```text
CONTENT
COMMERCE
ERP
IDENTITY
INTELLIGENCE
SEARCH
WORKFLOW
DOCUMENT
PAYMENTS
LOGISTICS
ANALYTICS
INTEGRATION
OTHER
```

Engine types are descriptive.

CapabilityBinding determines actual runtime responsibility.

---

## 13.4 Critical rule

The platform MUST represent:

```text
Capability: commerce.orders
Provider: Engine = MedusaJS
```

rather than encode:

```text
commerce.orders == MedusaJS
```

This preserves replaceability.

---

# 14. EngineInstance

## 14.1 Definition

`EngineInstance` is a concrete deployable/running installation or logical endpoint of an Engine.

Examples:

```text
Medusa production ZA
Medusa staging
iDempiere production
Payload production EU
dedicated tenant-specific ERP instance
```

---

## 14.2 Recommended fields

```text
EngineInstance
--------------
id
engine_id
instance_key
name
environment
deployment_region
endpoint
internal_endpoint
version
contract_versions[]
tenant_strategy
isolation_profile_id
data_residency_profile
health_status
lifecycle_status
credentials_reference
configuration_reference
observability_reference
started_at
deprecated_at
retire_at
metadata
```

Secrets MUST NOT be stored directly in the registry.

Only references to a secret-management facility are permitted.

---

## 14.3 Cardinalities

```text
Engine 1 ─── 0..* EngineInstance

EngineInstance 1 ─── 1 IsolationProfile

EngineInstance 1 ─── 0..* CapabilityBinding

EngineInstance 1 ─── 0..* ExternalReference
```

---

# 15. Capability

## 15.1 Definition

`Capability` describes **what the platform can do**, independently from the software providing it.

Capabilities form the stable architectural interface between estates/business requirements and engines.

---

## 15.2 Naming convention

Capabilities SHOULD use hierarchical namespaces:

```text
content.pages
content.media
content.editorial

commerce.catalogue
commerce.pricing
commerce.cart
commerce.checkout
commerce.orders
commerce.customers
commerce.promotions

erp.accounting
erp.procurement
erp.inventory
erp.business-partners
erp.financial-reporting

identity.authentication
identity.authorisation

intelligence.market-signals
```

---

## 15.3 Recommended fields

```text
Capability
----------
id
capability_key
name
domain
description
contract_id
contract_version
criticality
state
dependencies[]
metadata
```

---

## 15.4 Capability dependencies

A capability MAY declare dependencies:

```text
commerce.checkout
    requires:
        commerce.catalogue
        commerce.pricing
        commerce.cart
```

Dependency declaration supports deployment validation.

It MUST NOT automatically imply implementation coupling.

---

# 16. CapabilityBinding

## 16.1 Definition

`CapabilityBinding` determines which EngineInstance provides a Capability for a particular scope.

This is the core of Baobab's pluggable-engine architecture.

---

## 16.2 Recommended fields

```text
CapabilityBinding
-----------------
id
capability_id
engine_instance_id
scope_id
priority
binding_mode
status
effective_from
effective_to
fallback_binding_id
configuration
contract_version
created_at
created_by
approved_at
approved_by
```

---

## 16.3 Binding modes

```text
PRIMARY
SECONDARY
FALLBACK
READ_ONLY
MIGRATION_SOURCE
MIGRATION_TARGET
SHADOW
```

`SHADOW` is particularly useful for validating a replacement engine without directing authoritative production operations to it.

---

## 16.4 Cardinalities

```text
Capability 1 ─── 0..* CapabilityBinding

EngineInstance 1 ─── 0..* CapabilityBinding

MappingScope 1 ─── 0..* CapabilityBinding
```

For a given Context, one binding SHOULD normally resolve as the authoritative `PRIMARY`.

Multiple bindings can coexist during migration or resilience scenarios.

---

# 17. Context

## 17.1 Definition

`Context` is the resolved runtime interpretation of an operation.

It is not merely request metadata.

It represents the security, commercial, organisational, geographic and technical circumstances under which an action occurs.

---

## 17.2 Recommended Context envelope

```json
{
  "context_version": "1.0",
  "tenant_id": "...",
  "legal_entity_id": "...",
  "organisation_id": "...",
  "business_unit_id": "...",
  "operating_region_id": "...",
  "market_id": "...",
  "country_code": "KE",
  "estate_id": "...",
  "digital_property_id": "...",
  "channel_id": "...",
  "currency": "KES",
  "accounting_currency": "ZAR",
  "locale": "en-KE",
  "timezone": "Africa/Nairobi",
  "actor_id": "...",
  "subject_id": "...",
  "request_id": "...",
  "correlation_id": "...",
  "causation_id": "...",
  "trace_id": "...",
  "environment": "production",
  "contract_version": "..."
}
```

Only appropriate fields need be populated.

---

## 17.3 Trusted versus untrusted context

Context MUST distinguish claims supplied by a client from fields resolved by trusted platform infrastructure.

For example:

```text
request hostname
      ↓ untrusted input
Domain Resolver
      ↓
trusted estate identity
      ↓
Authorised market
      ↓
resolved trusted Context
```

A caller MUST NOT be allowed to select arbitrary `tenant_id` merely by sending an HTTP header.

---

## 17.4 Context provenance

For sensitive resolution, Baobab SHOULD record provenance:

```text
tenant_id:
    source = identity_token

estate_id:
    source = hostname

market_id:
    source = estate_market_binding

currency:
    source = user_selection
    constrained_by = market.allowed_currencies
```

This materially improves auditability and troubleshooting.

---

## 17.5 Context propagation

The same Context or a deliberately reduced derivative MUST propagate through:

- synchronous HTTP calls;
- asynchronous jobs;
- event messages;
- webhooks;
- workflow execution;
- auditing;
- observability traces.

Sensitive fields SHOULD be filtered when crossing trust boundaries.

---

# 18. IsolationProfile

## 18.1 Definition

`IsolationProfile` defines the technical isolation guarantees required or implemented for a scoped workload.

Business organisation and technical isolation are deliberately separated.

---

## 18.2 Isolation dimensions

Isolation is not one scalar setting.

Recommended dimensions include:

```text
compute
database
schema
row/data
cache
queue
object-storage
search
network
secrets
encryption-key
identity
observability
backup
deployment
geography
```

---

## 18.3 Recommended fields

```text
IsolationProfile
----------------
id
profile_key
name
classification
compute_isolation
database_isolation
storage_isolation
cache_isolation
queue_isolation
network_isolation
secret_isolation
encryption_isolation
observability_isolation
backup_isolation
deployment_isolation
data_residency
cross_tenant_access_policy
requirements
controls
status
version
```

---

## 18.4 Typical levels

Convenient presets MAY be defined:

```text
SHARED_LOGICAL
SHARED_SCHEMA
DEDICATED_SCHEMA
DEDICATED_DATABASE
DEDICATED_INSTANCE
DEDICATED_DEPLOYMENT
DEDICATED_REGION
```

However, implementations SHOULD ultimately use individual dimensions rather than depend solely on one label.

---

## 18.5 Engine-native isolation

Baobab MUST translate the platform isolation requirement into native engine semantics.

iDempiere, for example, distinguishes a Client/Tenant from organisational entities within that client, and its Business Partner model may represent customers, vendors or employees. Baobab SHOULD map these native concepts rather than force Baobab's organisation model to mirror iDempiere's exactly.

Likewise, Payload's multi-tenant tooling can scope documents using tenant fields and tenant-aware filtering, but this remains a Payload implementation detail rather than the definition of a Baobab Tenant.

---

# 19. Cardinality Model

The primary cardinalities are:

| Source | Relationship | Target |
|---|---|---|
| CanonicalEntity | 1 → 0..* | ExternalReference via Mapping |
| CanonicalEntity | * ↔ * | CanonicalEntity via typed relationship |
| ExternalReference | 1 → 0..* | Mapping |
| Mapping | * → 1 | MappingScope |
| Tenant | 1 → 0..* | DigitalEstate |
| LegalEntity | 1 → 0..* | DigitalEstate |
| Market | * ↔ * | DigitalEstate |
| Market | 0..1 → 0..* | Child Market |
| Engine | 1 → 0..* | EngineInstance |
| EngineInstance | 1 → 0..* | ExternalReference |
| EngineInstance | 1 → 0..* | CapabilityBinding |
| Capability | 1 → 0..* | CapabilityBinding |
| MappingScope | 1 → 0..* | Mapping |
| MappingScope | 1 → 0..* | CapabilityBinding |
| IsolationProfile | 1 → 0..* | EngineInstance |
| DigitalEstate | 1 → 1..* | DigitalProperty |
| Context | runtime | resolves Mapping/Binding |

No database foreign-key layout should be inferred literally from this conceptual table without considering bounded contexts.

---

# 20. Inheritance Architecture

Configuration resolution MUST support hierarchical inheritance without coupling identity hierarchies to configuration hierarchies.

## 20.1 Recommended precedence

A practical default hierarchy is:

```text
Platform
   ↓
Tenant
   ↓
Legal Entity
   ↓
Operating Region
   ↓
Market
   ↓
Digital Estate
   ↓
Digital Property / Channel
   ↓
Actor/Customer Segment
   ↓
Request Override
```

The exact hierarchy MUST be governed centrally.

Engines may introduce engine-specific configuration below the appropriate Baobab scope.

---

# 21. Inheritance Rules

## 21.1 Explicit beats inherited

An explicitly configured value at a more specific compatible scope overrides an inherited value.

---

## 21.2 Absence means inherit

Missing values mean:

```text
consult parent/default
```

They MUST NOT automatically mean `null`.

---

## 21.3 Explicit null is distinct

The system SHOULD support:

```text
UNSET
INHERIT
EXPLICIT_NULL
VALUE
```

Otherwise it becomes impossible to distinguish:

> no configuration was supplied

from:

> explicitly disable the inherited configuration.

---

## 21.4 Restrictions narrow downward

A child context MUST NOT normally expand a security restriction inherited from its parent unless policy explicitly permits this.

Example:

```text
Tenant:
    currencies = [ZAR, USD]

Market:
    currencies = [ZAR]
```

is valid.

A child trying to introduce an unauthorised currency may require explicit approval.

---

## 21.5 Parent lifecycle constrains child lifecycle

An active child MUST NOT depend operationally upon an inactive parent.

Retiring a parent with active children MUST be blocked or require an explicit migration plan.

---

# 22. Context Resolution

A canonical request-resolution flow SHOULD be:

```text
Incoming Request
      │
      ▼
Authenticate
      │
      ▼
Resolve Tenant
      │
      ▼
Resolve Digital Property
      │
      ▼
Resolve Digital Estate
      │
      ▼
Resolve Legal Entity
      │
      ▼
Resolve Market
      │
      ▼
Resolve Country / Locale / Currency
      │
      ▼
Validate Authorisation
      │
      ▼
Construct Context
      │
      ▼
Resolve Capability
      │
      ▼
Resolve CapabilityBinding
      │
      ▼
Resolve Entity Mappings
      │
      ▼
Invoke Engine
```

Different entry points may begin with different evidence.

For example, machine APIs may derive tenant and estate from authenticated credentials rather than hostname.

---

# 23. Mapping Resolution Algorithm

Given:

```text
canonical entity
target system/capability
context
effective timestamp
```

the resolver SHOULD:

1. validate Context;
2. identify candidate mappings;
3. remove mappings outside temporal validity;
4. remove inactive mappings;
5. remove mappings whose scope does not match Context;
6. evaluate engine/capability compatibility;
7. rank by scope specificity;
8. apply explicit resolution priority;
9. reject ambiguous authoritative results;
10. return resolved mapping plus resolution provenance.

Resolution responses SHOULD include:

```text
mapping_id
canonical_entity_id
external_reference_id
scope_id
resolution_reason
effective_timestamp
mapping_version
```

This gives downstream debugging meaningful evidence.

---

# 24. Deterministic Resolution

Resolution MUST be deterministic.

The same:

```text
canonical identity
+ context
+ effective timestamp
+ contract version
```

SHOULD produce the same authoritative result while the underlying registry version remains unchanged.

Silent non-determinism is unacceptable for pricing, financial and compliance-sensitive workflows.

---

# 25. Temporal Semantics

Every material mapping SHOULD support temporal validity.

Recommended:

```text
effective_from inclusive
effective_to exclusive
```

That gives interval semantics:

```text
[effective_from, effective_to)
```

No two mutually exclusive authoritative mappings SHOULD overlap for the same canonical subject and equivalent scope unless the mapping type explicitly allows multiple simultaneous representations.

---

# 26. Lifecycle Model

All major registry entities SHOULD use controlled lifecycle states.

Recommended common lifecycle:

```text
DRAFT
   ↓
VALIDATED
   ↓
ACTIVE
   ↓
DEPRECATED
   ↓
RETIRED
```

Additional exceptional states:

```text
SUSPENDED
REJECTED
MIGRATING
QUARANTINED
```

---

# 27. Lifecycle Semantics

## DRAFT

May be edited freely.

Must not participate in authoritative production resolution.

## VALIDATED

Structurally and semantically valid, awaiting activation.

## ACTIVE

Eligible for runtime resolution.

## DEPRECATED

Still valid for existing consumers but SHOULD NOT be selected for new bindings where a successor exists.

## SUSPENDED

Temporarily disabled.

## MIGRATING

Participating in an explicitly managed transition.

## QUARANTINED

Detected inconsistency, reconciliation problem or security concern prevents normal resolution.

## RETIRED

No longer used for new transactions but retained for historical resolution.

---

# 28. Deletion Policy

Hard deletion MUST be exceptional.

Hard deletion is generally acceptable only for:

- erroneous unactivated drafts;
- test data;
- expired ephemeral resources whose retention is not required;
- privacy-driven deletion where legally required and architecturally appropriate.

Production mappings with audit or transactional history SHOULD be retired.

---

# 29. Engine Replacement Lifecycle

Suppose Medusa is eventually replaced.

The model supports:

```text
commerce.orders
      │
      ├── CURRENT
      │      Medusa Instance A
      │
      └── MIGRATION_TARGET
             Commerce Engine B
```

A migration can progress:

```text
1. register new Engine
2. register EngineInstance
3. establish SHADOW bindings
4. synchronise canonical mappings
5. validate behaviour
6. mark migration target
7. move selected scopes
8. activate PRIMARY binding
9. deprecate former binding
10. preserve historic mappings
11. retire previous instance
```

Digital estates do not need architectural redesign.

---

# 30. Market Expansion Lifecycle

Entering Kenya should require configuration and mapping, not platform redesign.

Example:

```text
Create Market:
    kenya-b2b

Bind:
    legal entity
    operating region
    countries
    currencies
    locales
    tax profile
    fulfilment policy

Create/Bind Digital Property:
    thamani.co.ke

Bind capabilities:
    content → Payload
    commerce → Medusa
    ERP → iDempiere

Create mappings:
    Medusa region/channel
    Payload localisation/context
    iDempiere organisation/warehouse
```

Then activate after validation.

---

# 31. Currency Model

The architecture MUST distinguish at least:

```text
Presentation Currency
Transaction Currency
Settlement Currency
Accounting Currency
Reporting Currency
```

These MAY all differ.

Currency MUST therefore be contextual, not treated as a simple tenant property.

---

# 32. Locale and Language

Baobab SHOULD use BCP 47-compatible locale identifiers where practical:

```text
en-ZA
en-KE
sw-KE
sw-TZ
```

DigitalEstate and Market define supported locales.

Payload supports field-level localisation and configurable locale fallback; Baobab should map its canonical locale policy to Payload rather than expose Payload's configuration as the enterprise model.

Fallback SHOULD be deliberate:

```text
sw-KE
  → en-KE
  → en
```

rather than accidental.

---

# 33. Party Mapping

Baobab SHOULD eventually canonicalise external persons and organisations using a `Party` abstraction.

```text
Party
├── Person
└── Organisation
```

Roles:

```text
Customer
Supplier
Distributor
Employee
Partner
Prospect
```

This maps naturally to systems such as iDempiere, where Business Partners can serve customer, vendor and employee roles.

It prevents enterprise duplication such as:

```text
ABC Ltd Customer
ABC Ltd Supplier
```

being incorrectly considered two organisations.

---

# 34. Source-of-Truth Matrix

Every canonical domain MUST publish ownership rules.

Example:

| Domain | Canonical identity authority | Operational authority |
|---|---|---|
| Tenant | Control Plane | Control Plane |
| Legal Entity | Organisation Registry | Control Plane |
| Market | Control Plane | Control Plane |
| Digital Estate | Control Plane | Digital-estate repository + Control Plane registry |
| Product identity | Canonical Registry | Domain-defined |
| Editorial content | Canonical identity + Payload ref | Payload |
| Commerce product | Canonical identity | Medusa |
| Cart | Medusa | Medusa |
| Commerce order | Medusa | Medusa |
| Financial document | iDempiere | iDempiere |
| Accounting posting | iDempiere | iDempiere |
| ERP inventory | iDempiere | iDempiere |
| Cross-system mapping | Control Plane | Mapping Registry |
| Capability contracts | `baobab-platform/shared` | `baobab-platform/shared` |
| Capability runtime binding | Control Plane | Control Plane |

A source-of-truth matrix MUST exist before integrating a new domain.

---

# 35. Contract Ownership

`baobab-platform/shared` owns the **grammar**.

The Control Plane owns **runtime state**.

Therefore:

```text
baobab-platform/shared
    └── says what a Mapping is

Control Plane
    └── stores actual mappings

Engine repository
    └── implements its contract adapter
```

Shared contracts MUST NOT contain live tenant credentials, mutable mappings or operational secrets.

---

# 36. Recommended `baobab-platform/shared` Structure

```text
shared/
├── contracts/
│   ├── canonical/
│   ├── mapping/
│   ├── context/
│   ├── organisation/
│   ├── tenancy/
│   ├── markets/
│   ├── estates/
│   ├── engines/
│   ├── capabilities/
│   └── isolation/
│
├── schemas/
│   ├── json-schema/
│   ├── openapi/
│   ├── asyncapi/
│   └── examples/
│
├── events/
│   ├── mapping/
│   ├── engines/
│   ├── markets/
│   └── capabilities/
│
├── standards/
│   ├── identifiers/
│   ├── api/
│   ├── events/
│   ├── context/
│   ├── versioning/
│   ├── security/
│   └── compatibility/
│
└── adr/
```

---

# 37. API Architecture

The Mapping Registry SHOULD expose versioned administrative and resolution APIs.

Illustrative endpoints:

```text
POST   /v1/canonical-entities
GET    /v1/canonical-entities/{id}

POST   /v1/external-references
GET    /v1/external-references/{id}

POST   /v1/mappings
PATCH  /v1/mappings/{id}
POST   /v1/mappings/{id}/activate
POST   /v1/mappings/{id}/retire

POST   /v1/resolution/mappings
POST   /v1/resolution/capabilities
POST   /v1/resolution/context

GET    /v1/markets/{id}
GET    /v1/digital-estates/{id}
GET    /v1/engines
GET    /v1/engine-instances
```

Resolution endpoints SHOULD favour POST when Context becomes too rich or sensitive for query strings.

---

# 38. Idempotency

Registry write endpoints MUST support idempotency where retried network operations could create duplicates.

For example:

```text
Idempotency-Key
```

plus request fingerprinting.

Duplicate engine webhook delivery MUST NOT produce duplicate mappings.

---

# 39. Optimistic Concurrency

Mutable registry resources SHOULD expose a version or ETag.

Updates MAY require:

```text
If-Match
```

or equivalent revision checks.

This prevents two administrators from silently overwriting mapping changes.

---

# 40. Event Architecture

Material lifecycle changes SHOULD emit events.

Examples:

```text
baobab.canonical-entity.created.v1
baobab.canonical-entity.retired.v1

baobab.mapping.created.v1
baobab.mapping.activated.v1
baobab.mapping.superseded.v1
baobab.mapping.retired.v1

baobab.market.activated.v1

baobab.engine-instance.registered.v1
baobab.engine-instance.deprecated.v1

baobab.capability-binding.activated.v1
baobab.capability-binding.changed.v1
```

---

# 41. Event Envelope

Events SHOULD use a common envelope:

```json
{
  "specversion": "...",
  "id": "...",
  "type": "baobab.mapping.activated.v1",
  "source": "baobab-control-plane",
  "time": "...",
  "tenant_id": "...",
  "subject": "...",
  "correlation_id": "...",
  "causation_id": "...",
  "contract_version": "...",
  "data": {}
}
```

CloudEvents compatibility is worth adopting or closely following.

---

# 42. Transactional Outbox

Registry state changes and integration events MUST avoid the dual-write problem.

The Control Plane SHOULD use the transactional outbox pattern:

```text
DB transaction
     │
     ├── update mapping
     └── append outbox event
              │
              ▼
        event publisher
```

This is preferable to:

```text
update DB
then
hope publishing succeeds
```

A surprisingly common architecture pattern, and not one worth preserving.

---

# 43. Consistency Model

The canonical registry requires **strong consistency** for:

- canonical identity creation;
- mapping uniqueness;
- authoritative mapping activation;
- capability binding conflicts;
- temporal overlap constraints.

Cross-engine synchronisation may be **eventually consistent**.

The specification MUST explicitly distinguish those two categories.

---

# 44. Reconciliation

A production mapping platform requires reconciliation processes.

The system SHOULD periodically detect:

```text
orphan canonical entities
orphan external references
missing native resources
duplicate native references
unverified mappings
conflicting mappings
scope overlaps
expired mappings still referenced
engine resources not mapped
canonical resources not represented where expected
```

Results SHOULD enter:

```text
healthy
warning
quarantined
```

states rather than being silently corrected.

---

# 45. Drift Detection

For critical mappings, store a non-sensitive fingerprint of selected engine-native attributes.

Example:

```text
ExternalReference.fingerprint
```

A change can trigger reconciliation if the external entity's identity-defining characteristics unexpectedly change.

This must not be confused with synchronising all operational data into the Control Plane.

---

# 46. Security

The Mapping Registry is security-sensitive.

If an attacker can rewrite:

```text
Tenant A product
    →
Tenant B ERP record
```

ordinary application authorisation becomes irrelevant.

Therefore Mapping operations SHOULD have stronger controls than common CRUD operations.

Required controls SHOULD include:

- authentication;
- tenant-aware authorisation;
- RBAC and/or ABAC;
- change auditing;
- privileged operations;
- separation of duties for critical mappings;
- immutable audit history;
- secret isolation;
- rate limiting;
- anomaly detection;
- strict API validation.

---

# 47. Cross-Tenant Mapping Rules

Cross-tenant mappings MUST be prohibited by default.

Exceptions require an explicit relationship type and policy.

Possible legitimate cases include:

```text
group consolidation
shared services
intercompany transactions
central procurement
master-data syndication
```

Such mappings MUST never arise implicitly from shared names or IDs.

---

# 48. Mapping Approval

Critical mappings SHOULD support four-eyes approval.

For example:

```text
DRAFT
  ↓ creator

VALIDATED
  ↓ validator

ACTIVE
  ↓ authorised approver
```

Particularly for:

- accounting mappings;
- tax mappings;
- payment mappings;
- cross-tenant mappings;
- ERP organisation mappings;
- data-residency bindings.

---

# 49. Audit Requirements

Every mapping mutation SHOULD record:

```text
who
what
when
tenant
previous value
new value
reason
request ID
correlation ID
origin
approval
effective date
```

Audit records SHOULD be append-only from the application's perspective.

---

# 50. Data Classification

Canonical resources SHOULD have classification metadata:

```text
PUBLIC
INTERNAL
TENANT_CONFIDENTIAL
RESTRICTED
```

Mapping metadata MUST NOT become a dumping ground for personally identifiable information or secrets.

---

# 51. Caching

Resolution results are excellent cache candidates.

Cache keys MUST contain every dimension capable of changing the resolution.

Conceptually:

```text
canonical_id
target capability/system
scope/context fingerprint
effective time bucket where appropriate
registry revision
```

Caches MUST be tenant-scoped.

---

# 52. Cache Invalidation

Material lifecycle events SHOULD invalidate affected cached resolutions.

A registry revision/epoch MAY provide coarse-grained safety.

Stale mappings are unacceptable for:

- financial postings;
- payments;
- security decisions;
- regulated routing.

Such workflows MAY bypass caches or use very short TTLs.

---

# 53. Availability

The runtime resolver can become a critical dependency.

Production deployment SHOULD eventually support:

- multiple application replicas;
- PostgreSQL high availability appropriate to environment;
- health/readiness probes;
- connection pooling;
- bounded timeouts;
- circuit breakers where clients call other services;
- cached safe mappings;
- graceful degradation where permitted.

Failure behaviour MUST depend on criticality.

For a financial mapping:

```text
fail closed
```

is preferable to guessing.

---

# 54. Observability

Every resolution SHOULD support correlation with distributed tracing.

Recommended measurements:

```text
mapping_resolution_total
mapping_resolution_failures
mapping_resolution_ambiguity
mapping_cache_hit_ratio
mapping_resolution_latency
external_reference_unverified
mapping_conflicts
capability_resolution_failures
context_resolution_failures
quarantined_mapping_count
```

Logs SHOULD include IDs rather than excessive entity data.

---

# 55. Service-Level Objectives

Production SLOs should eventually be established independently for:

```text
Context Resolution
Mapping Resolution
Capability Resolution
Registry Mutation
Registry Availability
Event Publication
Reconciliation Freshness
```

Read resolution will generally warrant stricter availability targets than administrative mutation.

---

# 56. Database Integrity

The Control Plane implementation SHOULD use relational constraints wherever the database can express real invariants.

Examples:

- uniqueness;
- non-overlapping active mappings where applicable;
- valid lifecycle transitions;
- foreign-key integrity inside the bounded context;
- check constraints for mutually exclusive targets;
- non-empty canonical keys;
- temporal validity.

Application-only validation is insufficient for critical invariants.

---

# 57. Metadata

Most resources MAY expose:

```text
metadata
```

but metadata SHOULD be:

- schema-constrained where practical;
- size limited;
- prohibited from holding secrets;
- prohibited from replacing first-class fields;
- versioned when relied upon operationally.

If everybody starts querying the same metadata key, it has become part of the domain model and should be promoted accordingly.

---

# 58. Schema Versioning

Every published contract MUST be versioned.

Distinguish:

```text
resource version
contract/schema version
mapping version
engine software version
```

These are different things.

A Mapping changing from revision 7 to 8 does not imply Mapping Contract v1 changed.

---

# 59. Contract Compatibility

Contract evolution SHOULD prefer:

- additive optional fields;
- stable meaning;
- explicit deprecation;
- tolerant readers where appropriate;
- compatibility tests.

Breaking changes require a new major contract version.

Repositories consuming canonical contracts SHOULD run compatibility checks in CI.

---

# 60. Mapping Migration

Mappings MUST be migrated explicitly when systems change.

Never silently mutate:

```text
external_reference.engine_instance
```

to make old mappings point at a new system.

Instead:

```text
old mapping
   ↓ RETIRED / SUPERSEDED

new mapping
   ↓ ACTIVE

supersedes = old mapping
```

This preserves provenance.

---

# 61. Disaster Recovery

Canonical identity and mappings are control-plane assets and SHOULD be considered critical business metadata.

Backups MUST support:

- point-in-time recovery where feasible;
- encrypted backup;
- tenant-safe restore procedures;
- restoration tests;
- registry/event consistency recovery;
- audit preservation.

Backups that have never been restoration-tested are optimism stored on disk.

---

# 62. Data Residency

EngineInstance and IsolationProfile SHOULD carry deployment/data-residency constraints.

Capability resolution MUST be able to exclude an otherwise valid engine instance when Context requires data to remain within an authorised geography.

Example:

```text
Context:
    residency = EU

Engine A:
    deployment = eu-west
    eligible = yes

Engine B:
    deployment = af-south
    eligible = no
```

This permits future regulatory requirements without changing canonical identity.

---

# 63. Example — Product

```text
CanonicalEntity
    canonical_key:
      product:thamani:ethiopia-guji-60kg

         │
         ├── Mapping
         │     → Payload
         │       collection: products
         │       document: 874
         │
         ├── Mapping
         │     → Medusa
         │       product: prod_01...
         │
         └── Mapping
               → iDempiere
                 table: M_Product
                 record: 1000492
```

Market mappings can then overlay:

```text
South Africa B2C
    Medusa Region ZA
    ZAR
    iDempiere Org ZA

Kenya B2C
    Medusa Region KE
    KES
    iDempiere Org KE
```

There remains one canonical product identity.

---

# 64. Example — Digital Estate

```text
DigitalEstate:
    Thamani B2C

DigitalProperties:
    thamani.example
    thamani.co.ke
    mobile://thamani

Markets:
    ZA-B2C
    KE-B2C

Capabilities:
    content.pages
        → Payload prod

    commerce.catalogue
        → Medusa prod

    commerce.orders
        → Medusa prod

    erp.accounting
        → iDempiere prod
```

The `.co.ke` hostname can resolve Kenya context without turning the Kenyan domain into a separate legal business.

---

# 65. Example — iDempiere

Baobab:

```text
Canonical Legal Entity:
    Thamani Global

Canonical Market:
    Kenya B2C
```

may map to iDempiere:

```text
AD_Client
AD_Org
M_Warehouse
M_PriceList
C_BPartner
M_Product
```

but the exact relationship depends on the business deployment strategy.

Baobab MUST therefore not encode:

```text
LegalEntity == AD_Client
```

as a universal invariant.

It is a **Mapping decision** under an IsolationProfile and organisational design.

That distinction is critical.

---

# 66. Example — Payload

Baobab may have:

```text
Estate:
    Thamani

Market:
    Kenya

Locale:
    sw-KE
```

Payload may represent this with:

```text
tenant
collection
document
localized fields
```

Payload supports both tenant-aware content and field-level localisation, making these useful implementation mechanisms while preserving the canonical Baobab concepts above them.

---

# 67. Anti-Patterns

The following are prohibited architectural shortcuts.

## 67.1 Shared database integration

```text
Medusa → iDempiere tables
Payload → Medusa tables
Control Plane → engine tables
```

Not permitted as an integration contract.

---

## 67.2 Natural-key identity

```text
same SKU = same product
same email = same customer
```

Not sufficient for canonical identity.

---

## 67.3 Giant mapping matrix

Avoid:

```text
tenant × entity × country × market × currency × locale ×
channel × warehouse × ERP org × engine × estate
```

as a single configuration table.

Use composable scope dimensions.

---

## 67.4 Engine leakage

Avoid public Baobab APIs such as:

```text
getMedusaProductMapping()
```

Prefer:

```text
resolveRepresentation(
    capability="commerce.catalogue"
)
```

Engine-specific administrative adapters can still exist internally.

---

## 67.5 Ambiguous fallback

Never resolve an ambiguous critical mapping by:

```text
ORDER BY id LIMIT 1
```

Failure is better than silently selecting the wrong company.

---

## 67.6 Git as runtime registry

Canonical schemas belong in Git.

Mutable production mappings do not.

---

# 68. Validation Rules

Before a Mapping can become ACTIVE:

1. canonical source exists;
2. external reference exists or is verifiably provisioned;
3. MappingScope is valid;
4. tenant policy permits the relationship;
5. target EngineInstance is active;
6. applicable CapabilityBinding exists where required;
7. no prohibited overlap exists;
8. temporal interval is valid;
9. contract versions are compatible;
10. required approval is complete;
11. isolation requirements are met;
12. reconciliation checks succeed.

---

# 69. Capability Resolution Rules

Given Context and Capability:

```text
resolve(capability, context)
```

MUST:

1. find active bindings;
2. filter temporal validity;
3. filter compatible scope;
4. filter environment;
5. filter residency;
6. filter isolation;
7. filter health where policy permits;
8. rank specificity;
9. select PRIMARY;
10. apply FALLBACK only according to policy.

Financial capabilities SHOULD NOT automatically fail over to an alternative ERP without explicit consistency guarantees.

---

# 70. Control Plane Boundary

The Control Plane should contain:

```text
Canonical Registry
Mapping Registry
Market Registry
Estate Registry
Engine Registry
Capability Registry
Context Resolution
Isolation Registry
Policy/Configuration
Audit
```

It SHOULD NOT absorb:

```text
commerce order processing
CMS document management
ERP accounting
warehouse execution
content authoring
payment transaction execution
```

This keeps Baobab a control plane rather than an accidental new ERP.

---

# 71. Deployment Independence

Every engine MUST remain independently:

- buildable;
- deployable;
- versionable;
- testable;
- observable;
- scalable;
- replaceable.

The Mapping Model connects engines semantically without combining their release cycles.

---

# 72. Polyrepo Contract

Every participating repository SHOULD contain:

```text
contract dependency/version
adapter implementation
contract compatibility tests
health contract
event compatibility tests
mapping adapter tests
context propagation tests
```

No repository should silently copy canonical schemas.

They should consume published versions from `baobab-platform/shared`.

---

# 73. Testing Requirements

The mapping architecture requires more than unit tests.

At minimum:

```text
Unit tests
Contract tests
Schema tests
Mapping resolution tests
Precedence tests
Temporal tests
Isolation tests
Tenant escape tests
Context tampering tests
Engine adapter tests
Migration tests
Reconciliation tests
Concurrency tests
Property-based tests
Performance tests
Disaster recovery tests
```

Property-based testing is particularly useful for validating scope-resolution behaviour across many dimension combinations.

---

# 74. Architectural Acceptance Criteria

The Canonical Mapping Model is successful when all of these statements are true:

- A Payload document can be replaced without changing product canonical identity.
- A Medusa product can move between engine instances without changing product canonical identity.
- iDempiere mappings can change without commerce applications querying ERP tables.
- A business can enter a new country by adding Market/context configuration.
- A business can operate multiple markets in the same country.
- One estate can serve multiple markets.
- Multiple estates can serve one market.
- Currency is contextually resolved.
- Tenant and legal entity remain independent concepts.
- Mappings support 1:1, 1:N, N:1 and N:M.
- Mapping history remains queryable.
- Engine replacement does not force estate redesign.
- Capability providers can vary by tenant or market.
- Isolation strength can vary by requirement.
- Cross-tenant mapping is denied by default.
- Every authoritative resolution is deterministic and auditable.
- Contracts can evolve independently of resource versions.
- Runtime state is separate from canonical schema definitions.

---

# 75. Canonical Architectural Decision

The following decision SHOULD be adopted as an ADR:

> **Baobab SHALL use canonical identities to represent cross-platform business concepts. Operational systems SHALL retain their native identities and domain models. Explicit, scoped, temporal mappings SHALL relate canonical identities to operational representations. Runtime Context SHALL determine applicable mappings and CapabilityBindings. No engine implementation SHALL constitute the canonical definition of a Baobab capability, tenant, legal entity, market or digital estate.**

---

# 76. Final Reference Architecture

```text
                        BAOBAB CONTROL PLANE
                                 │
             ┌───────────────────┼────────────────────┐
             │                   │                    │
      Canonical Registry   Mapping Registry     Context Resolver
             │                   │                    │
             ├───────────────────┼────────────────────┤
             │                   │                    │
      Market Registry      Estate Registry     Capability Registry
             │                   │                    │
             └───────────────────┼────────────────────┘
                                 │
                         Engine Registry
                                 │
                    ┌────────────┼────────────┐
                    │            │            │
                 Payload       Medusa     iDempiere
                 Content       Commerce       ERP
                    │            │            │
                    └────────────┼────────────┘
                                 │
                     APIs / Events / Adapters
                                 │
          ┌──────────────────────┼──────────────────────┐
          │                      │                      │
      Thamani Estate       ZuriBeans Estate       Baobab-Platform Estate
          │                      │                      │
          └──────────────────────┼──────────────────────┘
                                 │
              Markets • Regions • Channels • Currencies
                                 │
                         Isolation Policies

────────────────────────────────────────────────────────────────────

                       baobab-platform/shared

 Canonical Contracts • JSON Schema • OpenAPI • AsyncAPI • Events
 Versioning • Compatibility • Security Standards • ADRs • Workflows
```

The relationship between the two is deliberately simple:

```text
baobab-platform/shared
        │
        │ defines
        ▼
Canonical Mapping Contract
        │
        │ implemented by
        ▼
Baobab Control Plane
        │
        │ resolves
        ▼
Context + Capability + Canonical Identity
        │
        ├──────────────┬───────────────┐
        ▼              ▼               ▼
     Payload         Medusa         iDempiere
        │              │               │
        └──────── operational representations
```

---

# 77. Governing Maxim

The model can ultimately be reduced to five rules:

**1. Canonical identity is global.**

**2. Operational representation is local.**

**3. Context determines applicability.**

**4. Capabilities are stable; providers are replaceable.**

**5. Mappings are explicit, scoped, temporal, governed and auditable.**

If these five rules remain intact, Baobab can grow from a handful of legal businesses and three engines into a substantially larger multi-market enterprise platform without turning today's technology choices into tomorrow's architectural prison.