# Cross-engine object reference contracts v1

RTD-05 implements ADR-SHARED-019 §7 and §19.1.

This package defines the portable value object used when one Baobab engine
needs to refer to a canonical object whose authority belongs to another
engine.

## The three identities must remain distinct

```text
CrossEngineObjectReference
    = canonical Baobab domain object owned by an engine

ExternalReference
    = native object in an external/provider system

CanonicalEntity
    = Control Plane canonical-registry representation where applicable
```

Examples:

```text
RegulatoryDecision
owner = baobab-regulations
    → CrossEngineObjectReference

DocumentVersion
owner = baobab-trade-docs
    → CrossEngineObjectReference

Medusa order ID
system = medusa
    → ExternalReference

A Control Plane CanonicalEntity representing some concept
    → CanonicalEntity
```

One object may participate in more than one identity architecture, but the
identities must not be collapsed.

## Canonical shape

A reference carries only:

- `owner_engine_id`;
- `object_type`;
- `object_id`;
- `reference_mode`;
- optional `object_version` when `VERSION_PINNED`;
- `scope`;
- `tenant_id` exactly when tenant-scoped.

It deliberately does **not** carry:

- engine instance/deployment identity;
- system namespace;
- ExternalReference ID;
- Control Plane CanonicalEntity ID;
- arbitrary metadata;
- permissions;
- copied foreign payload;
- an embedded object snapshot.

## Pinning modes

### CURRENT

```text
object_id
    ↓
resolve owner's current state
```

No `object_version` is allowed.

This is suitable only where current-state semantics are intended.

### IDENTITY_PINNED

The object ID itself names an immutable historical object.

Typical example:

```text
DocumentVersion
tdocv_...
```

Adding another version token would be redundant if the owning domain already
guarantees immutable identity.

### VERSION_PINNED

The object has a durable aggregate ID and a separate owner-defined version or
revision.

```text
object_id = aggregate identity
object_version = exact historical state
```

The version value is opaque to consumers.

## Historical replay

Consequential decisions, published intelligence, evidence assessments and
other historical records should use a pinned reference where later owner
changes would otherwise alter meaning.

A `CURRENT` reference is not historical evidence merely because it was stored
in a historical record.

## Tenant scope

Tenant-scoped objects require `tenant_id`.

Platform-scoped objects prohibit `tenant_id`.

A reference is not an authorisation token. Possessing a reference never grants
access to the object or another tenant.

When a tenant-scoped reference appears inside an ordinary tenant-scoped event
or contract, its `tenant_id` must match the enclosing tenant unless a specific
governed cross-tenant contract explicitly says otherwise.

## Owner identity

`owner_engine_id` uses the canonical Shared Control Plane `engineId`
grammar, for example:

```text
baobab-regulations
baobab-trade-docs
baobab-pulse
baobab-cp
```

It deliberately excludes `engine_instance_id`: a durable reference must not
break merely because a deployment is replaced.

The schema validates the canonical engine ID grammar. Runtime use must also
establish that `owner_engine_id` is an actually registered engine; a
syntactically valid unknown slug has no authority.

## Object type

The base schema does not centrally enumerate every domain type.

The pair:

```text
(owner_engine_id, object_type)
```

forms the semantic type namespace.

Domain-specific Shared contracts should narrow `object_type` with a
`const` when they require a specific foreign type. This keeps the generic
reference reusable without turning Shared into the owner of every engine's
domain taxonomy.

## Observation timestamps

`observed_at` and `resolved_at` are not object identity.

When they matter, use `crossEngineReferenceObservation`, which wraps the
reference rather than mutating its identity semantics.

## Integrity

The base v1 reference intentionally does not define a generic content hash.
Different owners canonicalise content differently and a digest without a
defined canonical representation is ambiguous.

Domain contracts may pair the reference with governed integrity metadata
where appropriate, for example a Trade Docs `ContentArtifact` digest.

## Resolution

There is no universal Shared/Control Plane object resolver created by RTD-05.

The owner remains authoritative. References resolve through:

- owner APIs;
- governed events/projections;
- capability/provider bindings;
- explicitly approved adapters.

Direct cross-engine database access is not authorised by this contract.

## RTD programme relationship

- RTD-04 established the TradeDocument v2 foundation.
- **RTD-05 defines this reference contract.**
- RTD-06 will use it for Regulations ↔ Trade Docs requirement/evidence
  choreography.
- RTD-09 will use it for Pulse projections/consumers where appropriate.
