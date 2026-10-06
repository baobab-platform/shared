# Regulations capability contracts v1

This package contains the first canonical Baobab capability vocabulary for the
`regulations` namespace.

The initial tranche was accepted by ADR-SHARED-027 after an evidence-based
census of `baobab-platform/baobab-regulations`.

## Canonical capabilities

| Capability | Meaning | Runtime implementation at census |
|---|---|---|
| `regulations.requirement.resolve` | Resolve one exact pinned Regulations-owned documentary/permit/evidence requirement projection | Not implemented as a provider |
| `regulations.evidence.assess` | Assess documentary facts against one pinned regulatory requirement | Not implemented as a provider |

Both capabilities are **contracted but not implemented provider support**.

Their request/response semantics already exist in the Shared RTD-06 package:

`contracts/regulatory-document-exchange/v1`

A canonical catalogue entry therefore means only that the vocabulary and wire
contract exist. It does not imply:

- an active provider;
- a deployed Regulations route;
- certification;
- Control Plane registration;
- a CapabilityBinding or CapabilityGrant;
- tenant entitlement;
- operational health.

## Important separations

```text
regulations.requirement.resolve
    !=
regulations.context.resolve

regulations.evidence.assess
    !=
regulations.decision.evaluate
```

The first pair is narrow and already contract-backed by RTD-06. The second pair
describes broader Regulations runtime capabilities whose canonical Shared
contracts remain future work.

## Provider declaration

Until `baobab-regulations` implements these contracts, its provider declaration
must list them only under `planned_capabilities` with
`proposal_status: CONTRACTED`.

There must be no `providers[].support` entry for these capabilities yet.
