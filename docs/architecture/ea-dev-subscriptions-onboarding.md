# Subscriptions development onboarding

Governing: Accepted EA-DEV, ADR-SHARED-043/044 and ADR-SUB-0003/0014–0018.

The two named development-only proof-bootstrap clients have distinct secrets,
audiences and scope ceilings. They are ACTIVE solely to produce disposable
synthetic evidence, following the existing ADR-043 exception; this is not a
production credential/profile promotion. The production federated identities
remain PROVISIONED. No payment scope, provider certification, capability grant,
commercial terms approval or positive financial decision is added.

CP produces billing commands and canonical event notifications; Subscriptions
separately reads current CP INTERNAL and ProductSubscription authority. Read
the original CP state on every operation, before idempotent replay. Events are
invalidation hints, never grants. Commercial v1 remains deny-only.

Connected qualification must observe actual IAM-issued signed credentials,
current CP primary Organisation/classification/revision, Subscriptions-owned
PostgreSQL persistence, own/foreign tenant, wrong audience/client/scope, expiry,
revocation, changed classification/revision, durable event replay/conflict,
outage/recovery, and owned-resource/issuer teardown. No fake endpoint or locally
signed JWT may satisfy a native result. Unobserved cases stay BLOCKED.

This source allocation is not completed Subscriptions onboarding or DEV-09.
DEV-06/INT-07 remains deferred until its prerequisite is actually observed;
its original binding/resource and negative cases are unchanged. DEV-10 is paused.


## Reviewed owner source increments — 25 October 2026

[Shared #396](https://github.com/baobab-platform/shared/pull/396) merged as
`ae48e8cf6e4cd47314f36d9d318a33f30d409453` after all applicable final-head
canonical, Foundation/security and review gates passed. Its sensitive scope
exception is limited to the exact named development assessor and two read/preflight
scopes; the complete registry row remains validator-pinned.

[CP #439](https://github.com/baobab-platform/baobab-cp/pull/439) merged as
`8644cefd64e2dfe869c58f5ef6ab1667e731a1e2`, reviewed head
`c6922d62ca105fc0a9c346f9a61bd3836ce80c6b`. All 32 final-head checks completed:
26 successful, six applicable skips. Owner PG17 bootstrap tests exercise fixture
creation/replay, revision progression, suspension, protected and expired-lease
refusals. Only the separate guarded development binary creates canonical fixture
IDs; the orchestrator and engine cannot write CP tables.

[Subscriptions #51](https://github.com/baobab-platform/baobab-subscriptions/pull/51)
merged as `bdba962514b2ee5083dc95feba1343b02391f60a`, reviewed head
`93d3eb3cec0237d96e551971070948a8d9b8285a`; the merged and reviewed trees match.
All 26 final-head checks completed: 19 successful, seven applicable skips.
Java21/PG17, offline packaged-JAR, owner-schema, security/container and source
checks pass. The 24-file/17-entry original-byte bundle agrees with 158 independent
owner wire vectors. Commercial v1 cannot return an authorised financial outcome.

The projection gate matches current CP tenant, subscription, product, revision,
classification and primary Organisation before ensure/resume/usage, including
before successful replay. Resume checks the incoming command revision. Tests
prove only one current-state network call for COMMERCIAL usage, outside the
store transaction, and refusal if the complete projection changes during that
check. This removes duplicated remote calls under DB locks; it is not a measured
latency claim or distributed atomic CP/engine transaction guarantee.

The current-issuer port checks verified JWT subject/client/audience/scopes against
actual issuer status on every request, with bounded TLS transport/body/deadline,
no redirects and no positive cache. Old signature-only deployments are not
reclassified as revocation-qualified. Maintenance/configuration and rollback:
[engine runbook](https://github.com/baobab-platform/baobab-subscriptions/blob/bdba962514b2ee5083dc95feba1343b02391f60a/docs/development/connected-onboarding.md).

[Infrastructure #59](https://github.com/baobab-platform/infrastructure/pull/59)
adds the connected disposable native suite. Its fixed sixteen native observations
must pass independently of three BLOCKED INTERNAL/provider obligations. Native
CI and final-head evidence are still pending; source merge is not onboarding
completion. In particular the COMMERCIAL fixture cannot manufacture the INTERNAL
positive prerequisite, so DEV-06/INT-07 remains deferred.
