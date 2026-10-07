# Intelligence capability contracts v1

This package contains the first canonical Baobab capability vocabulary for the
`intelligence` namespace.

The initial tranche is accepted by **ADR-SHARED-029** after an evidence-based
census of `baobab-platform/baobab-pulse`.

## Canonical capabilities

| Capability | Meaning | Provider support at census |
|---|---|---|
| `intelligence.evidence.search` | Search authorised intelligence evidence without exposing vector-store implementation | None |
| `intelligence.research-mission.manage` | Create or retrieve a governed Pulse research mission | None |

Both are **contracted vocabulary only** at the census point.

```text
canonical capability
        !=
provider implementation
        !=
certification
        !=
Control Plane activation
        !=
tenant entitlement
```

## Security boundary

The Shared request contracts deliberately do **not** accept:

```text
tenant_id
requester_clearance
X-Baobab-Tenant-Id as authority
```

as caller-selected authority.

A conforming provider must derive tenant scope, principal authority and
classification clearance from authenticated platform context. The current Pulse
scaffold still has local trust shortcuts, so its routes are not evidence of
canonical provider support yet.

## Provider neutrality

The contract contains no:

```text
Haystack pipeline
Qdrant point id
embedding vector
model provider
generator class
database topology
```

Haystack and Qdrant remain replaceable implementation details behind Pulse
application ports.

## Cross-engine boundary

RTD-09 projections of Regulations and Trade Docs facts are **inputs to
intelligence**, not new intelligence capabilities. Pulse may preserve references,
derive intelligence and publish later intelligence facts, but it does not acquire
authority over the upstream object.

Likewise, this package does not turn Pulse into the authority for:

- regulatory applicability or legal sufficiency;
- TradeDocument creation or verification;
- commerce, ERP, IAM or CMS operational state;
- Control Plane tenant/context identity.

## Promotion path

```text
Shared canonical contract
        ↓
Pulse planned CONTRACTED declaration
        ↓
exact contract adapter + authenticated context boundary
        ↓
durability / idempotency / contract tests where required
        ↓
provider support PARTIAL
        ↓
provider support IMPLEMENTED
        ↓
EA-09 certification
        ↓
Control Plane activation / bindings / grants
```
