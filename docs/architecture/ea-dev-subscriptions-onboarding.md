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
CI evidence below proves the bounded component increment; remaining mandatory
legacy checks still gate the Infrastructure merge. This is not full onboarding
completion. In particular the COMMERCIAL fixture cannot manufacture the INTERNAL
positive prerequisite, so DEV-06/INT-07 remains deferred.

## Independently verified native component receipt

[Infrastructure native run 40230444543](https://github.com/baobab-platform/infrastructure/actions/runs/40230444543) executed reviewed head `73d56d3eccea6ee222b23e4404eed4e0fa1de3e9`, tested PR merge `3e9588b6499ded01663d226443ef1f5c2c4d3972`. Owner pins are the CP and Subscriptions merge commits above, Shared #396 and IAM `0ad103606b9705fcb33c468ea01b54d8ce76f9ae`.

[Artifact 12611814810](https://github.com/baobab-platform/infrastructure/actions/runs/40230444543/artifacts/12611814810) archive SHA-256: `47d69eecad20fd54e36072135e1e3b67b20420062ed2db9e51dbb05f12a02888`. The downloaded ZIP digest was independently compared with GitHub metadata. Original report SHA-256: `562ef7b5d043b1e1b0a3bfabd31d338d80ec3959b4743e6a0ef9e193df99f8fa`. The original report and base lifecycle receipt match their original-byte companion hashes; source pins and tested merge identity agree.

Original report bytes are retained in [the distinct immutable evidence directory](evidence/subscriptions-2026-10-25/final-40230444543/). Actual artifact expiry is `2026-11-08T20:25:29Z`, from GitHub metadata.

All nineteen cells were inspected: **16 native PASS / 3 independent BLOCKED**, no failures. Passes cover native issuer client readback, current CP state, COMMERCIAL engine persistence, tenant/audience/client/scope/classification denials, revision checks before replay, expiry, revocation while unexpired, durable event replay/conflict, restart, CP outage/recovery and teardown. Monetary readiness remains BLOCKED/simulated. Independent native store readback confirms one projection and one durable event receipt.

The three unchanged blocked obligations are current INTERNAL positive eligibility, its controlled revoked-eligibility differential (which needs that positive first), and genuine Kill Bill native provider qualification. Full onboarding, INTERNAL, INT-07, provider, protected and production qualification flags remain false; no money moved. This component inventory overlaps other engineering inventories and must not be added to DEV-09's canonical 48-case register.

Cleanup COMPLETE covers only run-owned containers, built images, volumes, networks and private state. Added issuer clients were deleted and tokens observed inactive before physical cleanup. Host/third-party base-image destruction is not claimed.

Earlier failed attempts remain failed and satisfy no final-head gate. Corrected harness defects included source-lock selection, OAuth client authentication and the owner lifecycle-receiver flag. Regressions now prevent those configuration errors from silently passing.

DEV-09 remains **42 PASS / 6 BLOCKED**. Its INTERNAL blocker recognises the connected workload read while retaining missing eligibility. DEV-06/INT-07 stays deferred until that actual prerequisite is proven.
