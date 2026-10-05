# ADR-SHARED-021 — Canonical Cross-Engine Object Reference, Authority, Scope and Historical Pinning Contract

**Status:** Accepted — Normative Shared Contract Architecture  
**Date:** 2026-10-05  
**Repository:** baobab-platform/shared  
**Decision ID:** ADR-SHARED-021  
**Decision Type:** Cross-Engine Identity / Reference / Authority / Historical Replay  
**Implements:** RTD-05 from ADR-SHARED-019  
**Depends On:** ADR-0004, ADR-SHARED-012, ADR-SHARED-013, ADR-SHARED-014, ADR-SHARED-017, ADR-SHARED-019, ADR-SHARED-020  
**Initial Consumers:** Baobab Regulations, Baobab Trade Docs, Baobab Pulse, Baobab Trade/TMS/ERP where they cite engine-owned canonical objects  
**Canonical Contract:** contracts/cross-engine-reference/v1/domain.schema.json

---

## 1. Executive Decision

Shared SHALL define one reusable CrossEngineObjectReference for references to canonical Baobab domain objects whose authority belongs to an engine.

Its minimum identity is:

~~~text
CrossEngineObjectReference
├── owner_engine_id
├── object_type
├── object_id
├── reference_mode
├── object_version?   # required only for VERSION_PINNED
├── scope
└── tenant_id?        # required exactly for tenant scope
~~~

The reference SHALL preserve:

1. who owns the object;
2. what semantic object type it is;
3. which durable owner-domain identifier is referenced;
4. whether resolution is current or historically pinned;
5. the exact owner-defined version when version pinning is required;
6. whether the object is platform- or tenant-scoped;
7. the tenant boundary for tenant-scoped objects.

It SHALL NOT copy the foreign aggregate.

It SHALL NOT become an ExternalReference.

It SHALL NOT become a Control Plane CanonicalEntity.

It SHALL NOT bind durable identity to an engine deployment.

---

## 2. Why RTD-05 Is Required

ADR-SHARED-019 established:

> **References connect engines; references do not transfer authority.**

RTD-02 reconciled Pulse.

RTD-03 reconciled Regulations.

RTD-04 established the correct TradeDocument v2 identity/version/content boundary.

The remaining gap is executable identity.

Without RTD-05, each engine could independently invent fields such as:

~~~text
document_id
document_version_id
regulatory_decision_id
regulations_reference
pulse_reference
evidence_set_ref
source_engine
owner
version
revision
~~~

with incompatible semantics.

That would recreate cross-engine coupling through ad hoc IDs even though the bounded contexts themselves were separated correctly.

---

## 3. The Identity Problem

The platform already has several things called references or identities.

They are not interchangeable.

| Concept | Purpose | Authority |
|---|---|---|
| CanonicalEntity | Control Plane registry representation of a canonical business concept | Control Plane registry |
| ExternalReference | Identity of a native object in an external/provider system | Control Plane mapping architecture + external system |
| EvidenceReference | Metadata view/reference inside the Control Plane organisation-evidence bounded context | Control Plane evidence model |
| Event subject | Transport/event occurrence subject identifier | Producing event contract |
| CrossEngineObjectReference | Portable reference to a canonical object owned by another Baobab engine | Referenced owner engine |

RTD-05 exists to prevent these concepts from collapsing.

---

## 4. Fundamental Identity Separation

The following SHALL remain true:

~~~text
CrossEngineObjectReference
    !=
ExternalReference

CrossEngineObjectReference
    !=
CanonicalEntity

CrossEngineObjectReference
    !=
engine_instance_id

CrossEngineObjectReference
    !=
event subject

CrossEngineObjectReference
    !=
EvidenceReference

CrossEngineObjectReference
    !=
copied foreign aggregate
~~~

---

## 5. Architectural Position

~~~text
                    CONTROL PLANE
             engine / tenant / capability
                    governance
                       │
                       │ topology grammar
                       ▼
             CrossEngineObjectReference
              owner + type + id + pin
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
  REGULATIONS       TRADE DOCS       PULSE
 RegulatoryDecision TradeDocument   EvidenceSet
 DocumentRequirement DocumentVersion Analysis
 EvidenceRequirement ContentArtifact Insight
        │              │              │
        └──────────────┼──────────────┘
                       │
                  references only
                       │
                       ▼
                consuming engine
~~~

The reference is a Shared wire/value contract.

Shared is not the runtime owner of the referenced objects.

---

## 6. Canonical Contract Location

The executable contract is:

~~~text
contracts/cross-engine-reference/v1/domain.schema.json
~~~

The package is intentionally small.

RTD-05 does not create:

- a database;
- an aggregate store;
- an object registry;
- a universal resolver service;
- a new capability provider;
- an event context.

---

## 7. Owner Engine

Every reference SHALL name owner_engine_id using Shared control-plane/v1/domain.schema.json#/$defs/engineId.

Examples:

~~~text
baobab-regulations
baobab-trade-docs
baobab-pulse
baobab-cp
~~~

The field answers:

> **Which Baobab engine owns canonical domain authority for this object?**

---

## 8. Owner Engine Is Not Runtime Routing

The owner engine SHALL NOT be treated as a concrete deployment.

Therefore RTD-05 deliberately excludes engine_instance_id from durable reference identity.

A reference such as:

~~~text
owner_engine_id = baobab-regulations
~~~

must remain valid if the Control Plane changes:

- engine instance;
- cluster;
- region;
- deployment;
- replica;
- failover target;
- provider binding.

Runtime routing is resolved separately through the Control Plane/capability architecture.

### Registered owner rule

The JSON Schema validates the canonical engineId grammar.

Runtime use SHALL additionally establish that owner_engine_id identifies a registered Baobab engine.

A syntactically valid but unknown engine slug SHALL NOT become authoritative merely because it matches the pattern.

---

## 9. Why Engine Instance Is Excluded

This is prohibited:

~~~text
RegulatoryDecision reference
    owner = ei_abc123
~~~

because:

~~~text
engine deployment lifecycle
    !=
domain object lifecycle
~~~

A deployment can disappear while the canonical object remains valid.

---

## 10. Object Type

Every reference SHALL name object_type using a stable uppercase semantic code.

Examples:

~~~text
REGULATORY_DECISION
DOCUMENT_REQUIREMENT
EVIDENCE_REQUIREMENT
TRADE_DOCUMENT
DOCUMENT_VERSION
CONTENT_ARTIFACT
EVIDENCE_SET
ANALYSIS
INSIGHT
CAPABILITY
~~~

---

## 11. Object Type Namespace

The semantic namespace is the pair:

~~~text
(owner_engine_id, object_type)
~~~

Therefore:

~~~text
(baobab-regulations, REGULATORY_DECISION)
~~~

is distinct from any same-named type another engine might define.

---

## 12. Shared Does Not Own Every Engine Taxonomy

The base contract SHALL NOT contain a closed enum of every cross-engine object type.

That would turn Shared into the taxonomic authority for every engine's internal domain model.

Instead:

- the generic schema defines stable syntax;
- engine/domain ADRs define semantic meaning;
- domain-specific Shared contracts SHOULD constrain object_type with const when a specific type is required.

---

## 13. Object ID

Every reference SHALL carry object_id.

The value is the durable domain identifier governed by the owner.

Examples:

~~~text
tdoc_...
tdocv_...
regdec_...
evset_...
~~~

The reference contract defines a portable safe grammar.

It does not mint the ID.

---

## 14. Object ID Does Not Become CanonicalEntity ID

The object ID SHALL NOT acquire Control Plane registry semantics merely because its grammar is compatible.

Hard invariant:

~~~text
Trade Docs tdoc_...
    !=
Control Plane CanonicalEntity ID
~~~

unless a separate platform decision explicitly establishes identity equivalence for a particular domain.

If a TradeDocument is separately represented as a CanonicalEntity, that is a separate identity relationship.

---

## 15. Three Reference Modes

RTD-05 SHALL make historical semantics explicit through:

~~~text
CURRENT
IDENTITY_PINNED
VERSION_PINNED
~~~

This is preferable to an ambiguous optional version string.

---

## 16. CURRENT

A CURRENT reference means:

~~~text
owner + object type + object id
        │
        ▼
resolve current owner state
~~~

It deliberately contains no object version.

This is suitable only where current-state semantics are intended.

---

## 17. CURRENT Is Dynamic

The following is prohibited:

~~~text
stored CURRENT reference
    =
historical snapshot
~~~

The owner may legitimately change current state after the reference was stored.

Therefore CURRENT is suitable only where current-state semantics are intended.

---

## 18. IDENTITY_PINNED

IDENTITY_PINNED means the object identifier itself names an immutable historical object.

Example:

~~~text
TradeDocument
    tdoc_A

DocumentVersion
    tdocv_A_003
~~~

A reference to tdocv_A_003 does not need another version token if Trade Docs guarantees that the DocumentVersion identity is immutable.

---

## 19. Why IDENTITY_PINNED Exists

Without this mode the platform would create redundant structures such as:

~~~text
DocumentVersion ID = tdocv_A_003
object_version = 3
~~~

even though the object identity already denotes the historical version.

RTD-05 therefore distinguishes immutable version-object identity from a version of a mutable/stable aggregate identity.

---

## 20. VERSION_PINNED

VERSION_PINNED means:

~~~text
stable object ID
+
exact owner-defined version/revision
=
historical state
~~~

The version value is opaque to consumers.

---

## 21. Version Kind

The v1 contract permits owner-defined version semantics classified as:

~~~text
VERSION
REVISION
SEQUENCE
ETAG
CONTENT_HASH
OTHER
~~~

The classification communicates how the owner identifies the state.

It does not transfer interpretation authority to the consumer.

---

## 22. Version Value Is Opaque

Consumers SHALL NOT assume that VERSION 12 is newer than VERSION 11 or that a lexically later revision is semantically newer unless the owning domain defines that ordering.

The consumer preserves the value.

The owner interprets it.

---

## 23. CONTENT_HASH Caution

CONTENT_HASH SHALL only be used as an object-version kind where the owning domain has defined what representation is hashed.

This is not sufficient:

~~~text
SHA-256 = abc...
~~~

without answering:

~~~text
hash of what canonical bytes?
~~~

RTD-05 therefore does not define a universal object-content digest field.

---

## 24. Scope

Every reference SHALL declare:

~~~text
scope = platform | tenant
~~~

This prevents tenant context from becoming optional ambiguity.

---

## 25. Tenant Scope

If scope = tenant then tenant_id is mandatory.

The value uses the canonical Control Plane tenant identifier.

---

## 26. Platform Scope

If scope = platform then tenant_id SHALL be absent.

The platform SHALL NOT invent a default tenant for a platform object.

---

## 27. Tenant Boundary Is Authority Metadata

A tenant-scoped reference means:

> **the referenced object's canonical authority exists inside this tenant boundary.**

It does not mean:

> **the holder of this JSON object is permitted to read that tenant.**

---

## 28. Reference Is Not Authorisation

Hard invariant:

~~~text
reference possession
    !=
permission
~~~

The owner MUST still enforce authenticated principal, tenant ownership, capability/authorization policy, classification, purpose, data minimisation and other applicable access controls.

---

## 29. Cross-Tenant Use

A consumer SHALL NOT resolve a tenant-scoped reference under a different tenant merely because the reference contains a valid object ID.

~~~text
caller tenant A
        │
        ▼
reference tenant B
        │
        ▼
DENY / explicit governed cross-tenant workflow
~~~

Ordinary resolution never silently crosses tenants.

### Enclosing tenant consistency

When a tenant-scoped reference appears inside another tenant-scoped contract or event, its tenant_id SHALL match the enclosing tenant unless an explicit cross-tenant contract authorises otherwise.

For example:

~~~text
event tenantid = tn_A
reference scope = tenant
reference tenant_id = tn_B
~~~

is invalid for an ordinary tenant-scoped event.

This rule prevents a structurally valid reference from smuggling a foreign tenant identifier into a trusted enclosing context.

---

## 30. Why Legal Entity and Market Are Not Generic Reference Fields

RTD-05 does not add legal_entity_id, market_id, digital_estate_id, jurisdiction or trade_lane to every reference.

Those dimensions belong to the referenced object's domain semantics or a domain-specific contract.

Putting every possible context dimension in the base reference would recreate a platform-wide mega-context value object.

The one universal isolation dimension is tenant scope.

---

## 31. Observation Time Is Not Identity

ADR-SHARED-019's conceptual reference shape mentioned observed_at and resolved_at.

RTD-05 deliberately keeps those values outside the canonical identity object.

The same object reference resolved at 10:00 and 11:00 must remain the same reference identity.

---

## 32. Reference Observation Wrapper

Where consumer-side timing matters, Shared defines:

~~~text
CrossEngineReferenceObservation
├── reference
├── observed_at
└── resolved_at?
~~~

This permits evidence capture timing, cache timing, decision trace timing and investigation/replay metadata without making timestamps part of object identity.

---

## 33. Reference Equality

For practical equality/deduplication, a reference's semantic identity is determined by:

~~~text
owner_engine_id
object_type
object_id
reference_mode
object_version?
scope
tenant_id?
~~~

observed_at and resolved_at are explicitly excluded because they belong to the observation wrapper.

---

## 34. Reference Does Not Embed Foreign Payload

The base object has additionalProperties=false and contains no payload, data, snapshot, metadata, attributes or foreign aggregate field.

This is intentional.

---

## 35. Why Arbitrary Metadata Is Prohibited

An open metadata bag would quickly become:

~~~text
CrossEngineObjectReference
├── owner
├── id
└── metadata
      ├── decision
      ├── hs_code
      ├── expiry
      ├── issuer
      ├── shipment
      └── copied upstream state
~~~

That would defeat the bounded-context architecture.

Domain-specific contracts may add explicitly governed fields around the reference.

---

## 36. Reference vs Snapshot

A reference points to owner truth.

A snapshot preserves a consumer's historical representation.

They are distinct:

~~~text
reference
    !=
snapshot
~~~

RTD-05 defines the reference.

A consequential domain may separately persist a governed snapshot where retention/replay requirements demand it.

---

## 37. Historical Replay

ADR-SHARED-019 requires historical decisions to preserve the object version/snapshot used.

RTD-05 provides two safe reference mechanisms:

~~~text
IDENTITY_PINNED
or
VERSION_PINNED
~~~

A consequential record SHALL NOT claim deterministic historical replay using only CURRENT where owner state can change.

---

## 38. Consequential Decision Rule

For a consequential decision depending on a mutable foreign object, CURRENT SHOULD be rejected by the domain contract.

Instead VERSION_PINNED or an immutable IDENTITY_PINNED reference is required.

RTD-06 SHOULD enforce this for Regulations ↔ Trade Docs evidence relationships.

---

## 39. Evidence Semantics

A cross-engine reference is not itself evidence.

~~~text
CrossEngineObjectReference
    !=
Evidence
~~~

It may identify an object that another domain uses as evidence.

The evidence relationship supplies purpose, relevance, assessment, sufficiency, provenance and decision context.

---

## 40. Example — Regulations Cites a DocumentVersion

~~~text
Trade Docs
TradeDocument TD-100
    └── DocumentVersion DV-3
             │
             │ IDENTITY_PINNED reference
             ▼
Regulations
RegulatoryEvidenceAssessment
             │
             ▼
RequirementSatisfaction
~~~

Regulations does not copy the TradeDocument aggregate to gain ownership.

---

## 41. Example — Pulse Cites RegulatoryDecision

~~~text
Regulations
RegulatoryDecision
      │
      │ IDENTITY_PINNED
      ▼
Pulse Evidence
      │
      ▼
Analysis
      │
      ▼
Risk / Opportunity / Recommendation
~~~

Pulse may contextualise the reference.

Pulse does not convert the RegulatoryDecision into Pulse regulatory truth.

---

## 42. Example — Dynamic Platform Reference

A consumer may refer to a platform capability as current state:

~~~text
owner_engine_id = baobab-cp
object_type = CAPABILITY
object_id = documents.trade-document.manage
reference_mode = CURRENT
scope = platform
~~~

No tenant is permitted.

No version is permitted.

---

## 43. ExternalReference Boundary

ADR-SHARED-013 remains unchanged.

An ExternalReference says:

> **a native object exists in an external/provider system.**

A CrossEngineObjectReference says:

> **a Baobab engine owns this canonical domain object.**

---

## 44. Example — Both Reference Systems May Exist

~~~text
Baobab Trade canonical Order
        │
        ├── CrossEngineObjectReference
        │      owner = baobab-trade
        │      type  = ORDER
        │      id    = canonical order id
        │
        └── Mapping
               │
               ▼
          ExternalReference
          system = medusa
          native_id = order_...
~~~

The two references solve different problems.

---

## 45. CanonicalEntity Boundary

A Control Plane CanonicalEntity is a registry object.

A domain object may optionally have a registry representation.

RTD-05 does not require every engine object to become a CanonicalEntity before another engine can reference it.

Otherwise every ordinary cross-engine relationship would gain unnecessary Control Plane synchronisation and registry growth.

---

## 46. No Mandatory CanonicalEntity Registration

This is rejected:

~~~text
Trade Docs creates DocumentVersion
        │
        ▼
must synchronously register CanonicalEntity
        │
        ▼
only then can Regulations reference it
~~~

Instead:

~~~text
Trade Docs creates DocumentVersion
        │
        ▼
owner-domain ID exists
        │
        ▼
CrossEngineObjectReference may cite it
~~~

CanonicalEntity registration remains a separate decision where needed.

---

## 47. Existing Pulse Reference

Pulse currently has a local value object conceptually equivalent to:

~~~text
Reference
├── object_type
├── object_id
└── version?
~~~

That was valid before RTD-05.

It is now incomplete for cross-engine use because it does not preserve owner engine, tenant scope or explicit current-vs-pinned semantics.

RTD-09 SHOULD migrate Pulse cross-engine references to the Shared contract or a strict adapter around it.

Pulse may retain a local internal reference type for strictly Pulse-owned relationships if it is not exposed as a competing cross-engine wire contract.

---

## 48. Existing Trade Docs SubjectAssociation

RTD-04 deliberately left SubjectAssociation.subject_reference opaque and documented that it is not the final cross-engine reference.

After RTD-05:

- cross-engine subject associations SHOULD use or embed the Shared reference in a later compatible contract version;
- Trade Docs-local subjects may retain local IDs where no cross-engine portability is required.

RTD-05 does not silently mutate trade-document/v2 after publication.

---

## 49. Regulations References

Regulations ADRs already use the conceptual term CrossEngineObjectReference.

RTD-05 now gives that concept an executable Shared shape.

RTD-06 SHALL use this shape for document requirement references, evidence requirement references, TradeDocument/DocumentVersion references and RegulatoryDecision references where consumed by Trade Docs.

---

## 50. Resolution Architecture

RTD-05 SHALL NOT create one universal all-Baobab-object resolver.

Such a service would become a new authority bottleneck.

---

## 51. Governed Resolution Paths

References may resolve through:

- owning-engine APIs;
- owner events and approved projections;
- capability/provider bindings;
- explicit anti-corruption adapters;
- governed caches/projections.

The owner remains authoritative.

---

## 52. Capability Resolution Is Different

Capability resolution answers:

> **Which provider/engine instance should serve a capability in this context?**

Cross-engine object reference answers:

> **Which canonical owner-domain object is being cited?**

Therefore:

~~~text
capability binding
    !=
object identity
~~~

A consumer may resolve a capability to discover a route and then use the reference with that route.

---

## 53. No Direct Database Resolution

This remains prohibited:

~~~text
Regulations
    SELECT *
    FROM trade_docs.document_versions
~~~

or:

~~~text
Pulse
    JOIN regulations.regulatory_decisions
~~~

CrossEngineObjectReference provides no permission for cross-engine table access.

---

## 54. Caching and Projection

A consumer MAY cache/project the referenced object if architecture permits.

The projection SHALL retain at minimum:

- owner engine;
- object type;
- object ID;
- reference mode;
- pinned version where applicable;
- tenant boundary.

The projection SHALL NOT become the canonical owner.

---

## 55. Current Reference Cache Rule

A cached CURRENT reference resolution has a cache time.

It does not acquire historical pinning merely because the cache is old.

If historical meaning matters, the consumer must preserve a pinned owner state or governed snapshot.

---

## 56. Failure Semantics

Reference resolution SHALL distinguish conceptually:

~~~text
object does not exist
    !=
owner unavailable
    !=
not authorised
    !=
tenant mismatch
    !=
version unavailable
    !=
version retired/purged
    !=
reference malformed
~~~

RTD-05 does not force one HTTP API, but domain APIs SHALL not collapse these into misleading business conclusions.

---

## 57. Owner Unavailable Is Not Object Missing

This is prohibited:

~~~text
owner timeout
    →
OBJECT_NOT_FOUND
~~~

Infrastructure unavailability must not be converted into semantic absence.

This is especially important in regulatory enforcement.

---

## 58. Version Unavailable Is Not Current Version

This is prohibited:

~~~text
requested historical version missing
    →
return latest
~~~

A VERSION_PINNED resolution either resolves the exact state or fails explicitly.

---

## 59. IDENTITY_PINNED Owner Contract

An owner exposing an object as IDENTITY_PINNED must guarantee that the referenced identity is historically stable/immutable for the relevant semantics.

A consumer SHALL NOT invent IDENTITY_PINNED merely because it prefers not to carry a version.

---

## 60. Version Pinning Owner Contract

A VERSION_PINNED owner must define:

- what the version kind means;
- how exact historical resolution works;
- whether the version can be retained/replayed;
- what failure means if retention has expired.

---

## 61. Event Direction

Events may carry CrossEngineObjectReferences where a foreign object is relevant.

They SHOULD carry the reference and minimum event-specific facts.

They SHOULD NOT carry a complete foreign aggregate merely to avoid resolution.

---

## 62. Event Subject Is Still Separate

An event may contain a compact subject for event routing/diagnostics.

That does not replace the structured cross-engine reference when the payload needs portable owner/scope/version semantics.

---

## 63. Security and Data Minimisation

The reference itself SHOULD contain no:

- personal data;
- credentials;
- document content;
- sensitive regulatory evidence;
- financial values;
- arbitrary labels.

It identifies an object.

Sensitive content stays behind owner authorisation.

---

## 64. Enumeration Resistance

An authorised caller possessing one valid reference SHALL not thereby gain a generic way to enumerate adjacent owner objects.

Owner APIs should prefer specific retrieval/resolution paths with proper authorization over open sequential ID traversal.

---

## 65. Provenance

Authority travels with owner_engine_id.

Historical identity travels with reference_mode and object_version where applicable.

Consumer observation context may travel separately through CrossEngineReferenceObservation.

These are necessary provenance components but are not a complete provenance graph.

---

## 66. Why No Generic Integrity Field in v1

ADR-SHARED-019 allowed integrity/provenance hints where required.

RTD-05 intentionally does not define a generic object hash because the platform has not defined one universal canonical serialization for arbitrary engine objects.

A digest is meaningful only with a defined byte/semantic representation.

Specialised contracts may pair a reference with Trade Docs ContentArtifact digest, signed credential digest, event payload hash or other governed integrity metadata.

---

## 67. Interoperability with Trade Docs ContentArtifact

~~~text
CrossEngineObjectReference
    owner = baobab-trade-docs
    type = CONTENT_ARTIFACT
    id = tdoca_...

Trade Docs ContentArtifact
    digest_algorithm = SHA-256
    digest_value = ...
~~~

The hash remains a property of the artifact contract.

The reference does not duplicate it.

---

## 68. Interoperability with Evidence

A Regulations evidence record may conceptually store a CrossEngineObjectReference to a DocumentVersion plus Regulations-owned fields such as evidentiary purpose, assessment, sufficiency, legal basis and decision relationship.

The reference does not own those meanings.

---

## 69. Interoperability with Pulse

Pulse Evidence may conceptually use referenced_object = CrossEngineObjectReference plus Pulse-owned analytical role, relevance, direction, quality, weight and evidence-set membership.

This preserves the useful Pulse Evidence abstraction while making cross-engine ownership explicit.

---

## 70. RTD-06 Contract Shape Consequence

RTD-06 SHOULD prefer relationships such as:

~~~text
DocumentRequirement
├── requirement_id
├── Regulations semantics
└── ...

DocumentEvidenceSubmission
├── requirement_reference
│     owner = baobab-regulations
│     type  = DOCUMENT_REQUIREMENT
│
└── document_version_reference
      owner = baobab-trade-docs
      type  = DOCUMENT_VERSION
      mode  = IDENTITY_PINNED
~~~

rather than copying either aggregate.

---

## 71. Equality and Deduplication

Two references are semantically equal when their identity fields are equal:

| Field | Equality component |
|---|---|
| owner_engine_id | Yes |
| object_type | Yes |
| object_id | Yes |
| reference_mode | Yes |
| object_version | Yes when present |
| scope | Yes |
| tenant_id | Yes when present |
| observed_at | No |
| resolved_at | No |

---

## 72. Serialization Stability

Field names in v1 are canonical Shared wire names.

Engine-local languages may use idiomatic names internally, but cross-engine JSON serialisation SHALL use the Shared field names.

---

## 73. Version Evolution of This Contract

Breaking changes to the reference shape require cross-engine-reference/v2.

Examples of breaking changes:

- changing meaning of reference modes;
- changing required identity fields;
- changing tenant scope semantics;
- changing version semantics incompatibly.

---

## 74. Migration Guidance

Initial migration sequence:

~~~text
RTD-05 Shared contract
      │
      ├── RTD-06 Regulations/Trade Docs contracts adopt it
      │
      ├── RTD-09 Pulse cross-engine references adopt it
      │
      └── later consumers adopt as they expose cross-engine pointers
~~~

RTD-05 SHALL NOT trigger an uncontrolled organisation-wide rewrite of every field named *_reference.

Migration is driven by cross-engine semantics, not string naming.

---

## 75. Contract Validation

Shared CI SHALL validate at minimum:

1. JSON Schema 2020-12 and immutable contract URI.
2. owner engine uses canonical engineId.
3. object type remains extensible.
4. required identity fields remain required.
5. engine instance is absent.
6. ExternalReference fields are absent.
7. CanonicalEntity field is absent.
8. arbitrary payload/metadata is absent.
9. tenant scope requires tenant ID.
10. platform scope forbids tenant ID.
11. CURRENT forbids object_version.
12. IDENTITY_PINNED forbids object_version.
13. VERSION_PINNED requires object_version.
14. pinned helper rejects CURRENT.
15. observation timestamps remain outside identity.
16. examples validate.
17. negative fixtures are rejected.

---

## 76. Rejected Alternatives

### A. Reuse ExternalReference

Rejected. ExternalReference models external/provider-native identity and mapping. RTD-05 models engine-owned Baobab canonical objects.

### B. Require CanonicalEntity for every referenced object

Rejected. It would create unnecessary Control Plane coupling and registry growth.

### C. Put engine_instance_id in the reference

Rejected. Deployment identity is not durable domain identity.

### D. Use only object_type + object_id

Rejected. Authority and tenant boundary would be lost.

### E. Use an optional version string with no mode

Rejected. Consumers could not distinguish current-state reference from historical pinning.

### F. Require version for every pinned reference

Rejected. Immutable version objects such as DocumentVersion already encode historical identity in their object ID.

### G. Embed copied foreign payload

Rejected. That transfers ownership and creates stale shadow aggregates.

### H. Add arbitrary metadata

Rejected. It becomes an escape hatch for copied domain state.

### I. Build a universal Control Plane object resolver

Rejected. Control Plane governs topology/context/mapping, not every engine's domain objects.

### J. Centrally enumerate every engine object type in Shared

Rejected. Shared standardises the reference grammar, not all domain taxonomies.

---

## 77. Invariants

~~~text
INV-XREF-001
Every CrossEngineObjectReference names the owning engine.

INV-XREF-002
owner_engine_id is an engine identity, never engine_instance_id.

INV-XREF-003
The pair (owner_engine_id, object_type) defines the semantic type namespace.

INV-XREF-004
object_id is governed by the owner domain.

INV-XREF-005
CrossEngineObjectReference is not ExternalReference.

INV-XREF-006
CrossEngineObjectReference is not CanonicalEntity.

INV-XREF-007
CrossEngineObjectReference does not embed the foreign aggregate.

INV-XREF-008
CrossEngineObjectReference carries no arbitrary metadata bag.

INV-XREF-009
Tenant-scoped references require tenant_id.

INV-XREF-010
Platform-scoped references prohibit tenant_id.

INV-XREF-011
Reference possession does not grant access.

INV-XREF-012
CURRENT references contain no object_version.

INV-XREF-013
CURRENT references are not historical snapshots.

INV-XREF-014
IDENTITY_PINNED references contain no redundant object_version.

INV-XREF-015
IDENTITY_PINNED is valid only where owner identity is historically immutable.

INV-XREF-016
VERSION_PINNED requires object_version.

INV-XREF-017
Consumers treat owner version values as opaque unless the owner contract defines ordering.

INV-XREF-018
Historical consequential decisions use pinned references where foreign state is mutable.

INV-XREF-019
A missing historical version is never silently replaced with current state.

INV-XREF-020
Owner unavailability is not object absence.

INV-XREF-021
Observation/resolution time is not part of reference identity.

INV-XREF-022
Cross-engine reference resolution does not authorise direct database access.

INV-XREF-023
Runtime capability/provider resolution remains separate from object identity.

INV-XREF-024
A domain projection retains owner identity and pinning semantics.

INV-XREF-025
Shared does not become runtime owner of referenced domain objects.

INV-XREF-026
A generic reference does not encode legal entity, market or jurisdiction as universal fields.

INV-XREF-027
Integrity metadata is domain-specific unless canonical representation is governed.

INV-XREF-028
Event subject does not replace structured reference semantics.

INV-XREF-029
Cross-tenant resolution requires explicit governed authority; it is never inferred from a reference.

INV-XREF-030
RTD-06 must compose Regulations and Trade Docs through references rather than copied aggregates.

INV-XREF-031
A syntactically valid owner_engine_id is not authoritative unless the engine is registered.

INV-XREF-032
A tenant-scoped reference embedded in an ordinary tenant-scoped contract/event matches the enclosing tenant.
~~~

---

## 78. Consequences

### Positive

- One portable reference grammar across engines.
- Owner authority survives transport and projection.
- Historical references become explicit and testable.
- Immutable version objects do not need redundant version fields.
- Dynamic references are no longer mistaken for snapshots.
- Tenant isolation travels with the reference.
- ExternalReference and CanonicalEntity semantics remain intact.
- Deployment changes do not invalidate durable object references.
- RTD-06 can model Regulations ↔ Trade Docs relationships cleanly.
- Pulse can retain its useful evidence model while adopting stronger cross-engine ownership semantics.

### Costs

- Existing local references need adapters/migration when exposed cross-engine.
- Consumers must choose a reference mode deliberately.
- Owners must document immutable-ID or version-resolution guarantees.
- Pinned historical state may require retention infrastructure.
- Domain-specific contracts still need to constrain object types and access patterns.

These are intentional costs of preserving authority and replayability.

---

## 79. Final Decision

The platform reference model is:

~~~text
ExternalReference
    native external/provider-system object

CanonicalEntity
    Control Plane canonical registry identity

CrossEngineObjectReference
    canonical Baobab domain object owned by an engine
~~~

and the cross-engine rule is:

> **A reference preserves owner, identity, tenant boundary and historical pinning semantics. It does not copy payload, grant access, bind to a deployment or transfer authority.**
