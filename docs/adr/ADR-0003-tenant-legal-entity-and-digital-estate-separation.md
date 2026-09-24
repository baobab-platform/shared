# ADR-0003: Separate Tenant, Legal Entity, and Digital Estate Identity

| | |
|---|---|
| **Status** | Accepted |
| **Date** | 2026-09-01 |
| **Owner** | Chief Software Engineer, Baobab-Platform Group Africa |
| **Repository** | `baobab-platform/shared` |
| **Supersedes** | ADR-0001 §§2.1–2.3 where they equate Baobab consumption with digital-estate purpose or exclude Baobab-Platform from tenancy |
| **Depends on** | ADR-0002; Control Plane v1 contracts |

---

## 1. Context

ADR-0001 correctly separated independently deployed digital estates from the
Baobab product platform, but it concluded that Baobab-Platform was not a tenant because
its digital estate had no Baobab product dependency. That conclusion joined two
questions which must remain independent:

1. Does a legal entity operate a website or other digital estate?
2. Does an organisation consume a Baobab product under an isolated operational
   and security boundary?

Baobab-Platform Group Africa requires the Baobab ERP Engine for its own holding-company
operations. Its corporate digital estate remains separately owned and deployed.
The existing contracts also use incompatible identifiers: the legal-entity
registry uses uppercase kebab-case IDs such as `THAMANI-GLOBAL`, while the
Control Plane applies one lowercase resource grammar to legal entities, tenants
and products.

## 2. Decision

### 2.1 Distinct concepts

- A **legal entity** is a canonical business identity declared in
  `contracts/legal-entity/registry.yaml`.
- A **tenant** is a Control Plane-owned security, data-isolation and
  product-entitlement boundary.
- A **digital estate** is an independently deployed customer- or
  stakeholder-facing application owned by its repository.
- An **iDempiere Client or Organisation**, an ERPNext Company, and equivalent
  vendor records are ERP-domain representations behind an engine boundary.

A legal entity is the default tenant boundary, but legal entity and tenant are
not synonyms. A digital estate neither creates nor prohibits tenancy. Product
consumption requires a tenant; merely owning an estate does not.

### 2.2 Baobab-Platform

`BAOBAB-PLATFORM` is approved for Baobab tenancy because it consumes `baobab-erp`, not
because `baobab-platform/baobab-platform` exists. The Control Plane must provision a distinct
opaque `tenant_id`, map it to `BAOBAB-PLATFORM`, and enforce the ERP entitlement.
Baobab-Platform, ZuriBeans and Thamani remain independent tenant boundaries unless an
explicit, authorised cross-organisational capability is approved.

### 2.3 Identifier grammar

| Identifier | Canonical form | Example | Authority |
|---|---|---|---|
| Legal entity | Uppercase kebab case | `THAMANI-GLOBAL` | `baobab-platform/shared` registry |
| Tenant | Opaque lowercase resource ID prefixed `tn_` | `tn_01k4example` | `baobab-platform/baobab-cp` |
| Product | Lowercase engine/product ID; kebab case preferred | `baobab-erp` | Shared product/interface contracts and CP entitlement registry |

New tenant IDs must not embed company names, countries, markets or jurisdictions.
Control Plane v1 may accept its former lowercase aliases during a documented
compatibility window, but it must emit and persist canonical legal-entity IDs
for new registrations. A legacy alias is never a second canonical identity.

### 2.4 Cardinality and mappings

Implementations must not enforce permanent identity equality between a tenant
and a legal entity. Version 1 carries one default legal-entity reference for
compatibility, while explicit mappings may later support:

- one tenant serving several authorised legal entities;
- one legal entity using several tenants for isolation or regional topology;
- several ERP organisations inside one tenant boundary;
- a dedicated ERP instance or database without changing canonical identity.

Every mapping is auditable, versioned and resolvable. Human-readable display
names are never mapping keys.

## 3. Consequences

### Positive

- Baobab-Platform can consume ERP without coupling ERP tenancy to its website.
- Legal reorganisation and deployment isolation do not force identifier reuse.
- ERP vendor identifiers stay behind the Baobab ERP boundary.
- The three initial organisations can be provisioned by one configuration-driven
  mechanism while remaining isolated.

### Costs

- Control Plane and current consumers must migrate legacy identifiers.
- Contract tests must distinguish canonical IDs from accepted v1 aliases.
- Product entitlement intent in Shared must be reconciled with enforced Control
  Plane state; Shared does not become a runtime entitlement database.

## 4. Rejected alternatives

- **Digital estate equals tenant.** Rejected because estate deployment and
  product consumption have different ownership, lifecycle and security rules.
- **Legal entity equals tenant.** Rejected because future isolation and
  organisational mappings require independent identities.
- **Use legal-entity names in tenant IDs.** Rejected because names,
  jurisdictions and corporate structures can change.
- **Use ERP vendor IDs as canonical identifiers.** Rejected because it couples
  the platform to the current ERP product and prevents clean replacement.

## 5. Follow-up

1. Update `baobab-cp` validation and persistence to accept canonical legal IDs,
   mint opaque tenant IDs and validate registry membership.
2. Migrate Trade and ERP consumer locks to the released Shared revision.
3. Publish the organisation model separately; this ADR does not collapse
   organisation into either legal entity or tenant.
4. Publish canonical ERP and cross-engine event contracts before implementing
   the iDempiere boundary.
