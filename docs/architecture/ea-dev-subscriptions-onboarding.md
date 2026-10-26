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
adds the connected disposable native suite. Its fixed seventeen native observations
must pass independently of three BLOCKED INTERNAL/provider obligations. Fresh final-head native
CI evidence below proves the bounded component increment; all applicable
legacy checks also passed before the Infrastructure merge. This is not full onboarding
completion. In particular the COMMERCIAL fixture cannot manufacture the INTERNAL
positive prerequisite, so DEV-06/INT-07 remains deferred.

## Initial historical native component receipt — superseded for the current gate

[Infrastructure native run 40230444543](https://github.com/baobab-platform/infrastructure/actions/runs/40230444543) executed reviewed head `73d56d3eccea6ee222b23e4404eed4e0fa1de3e9`, tested PR merge `3e9588b6499ded01663d226443ef1f5c2c4d3972`. Owner pins are the CP and Subscriptions merge commits above, Shared #396 and IAM `0ad103606b9705fcb33c468ea01b54d8ce76f9ae`.

[Artifact 12611814810](https://github.com/baobab-platform/infrastructure/actions/runs/40230444543/artifacts/12611814810) archive SHA-256: `47d69eecad20fd54e36072135e1e3b67b20420062ed2db9e51dbb05f12a02888`. The downloaded ZIP digest was independently compared with GitHub metadata. Original report SHA-256: `562ef7b5d043b1e1b0a3bfabd31d338d80ec3959b4743e6a0ef9e193df99f8fa`. The original report and base lifecycle receipt match their original-byte companion hashes; source pins and tested merge identity agree.

Original report bytes are retained in [the distinct immutable evidence directory](evidence/subscriptions-2026-10-25/final-40230444543/). Actual artifact expiry is `2026-11-08T20:25:29Z`, from GitHub metadata.

All nineteen cells were inspected: **16 native PASS / 3 independent BLOCKED**, no failures. Passes cover native issuer client readback, current CP state, COMMERCIAL engine persistence, tenant/audience/client/scope/classification denials, revision checks before replay, expiry, revocation while unexpired, durable event replay/conflict, restart, CP outage/recovery and teardown. Monetary readiness remains BLOCKED/simulated. Independent native store readback confirms one projection and one durable event receipt.

The three unchanged blocked obligations are current INTERNAL positive eligibility, its controlled revoked-eligibility differential (which needs that positive first), and genuine Kill Bill native provider qualification. Full onboarding, INTERNAL, INT-07, provider, protected and production qualification flags remain false; no money moved. This component inventory overlaps other engineering inventories and must not be added to DEV-09's canonical 48-case register.

Cleanup COMPLETE covers only run-owned containers, built images, volumes, networks and private state. Added issuer clients were deleted and tokens observed inactive before physical cleanup. Host/third-party base-image destruction is not claimed.

Earlier failed attempts remain failed and satisfy no final-head gate. Corrected harness defects included source-lock selection, OAuth client authentication and the owner lifecycle-receiver flag. Regressions now prevent those configuration errors from silently passing.

DEV-09 remains **42 PASS / 6 BLOCKED**. Its INTERNAL blocker recognises the connected workload read while retaining missing eligibility. DEV-06/INT-07 stays deferred until that actual prerequisite is proven.


The initial receipt above predates the final credential-isolation review. The
harness initially reused CP's random database password for the separate engine
store. That defect was found before merging Infrastructure #59. Current source
allocates an independent Subscriptions secret and adds a seventeenth required
native observation: its own-store TCP login succeeds and the same engine
credential receives a specific authentication refusal at the running CP database.
A transport outage cannot satisfy it. The previous report/hash bytes remain
unchanged as historical evidence; fresh final-head native evidence is required
before this new obligation or the revised harness can pass its merge gate.


## Final credential-isolated native receipt — 25 October 2026

[Native run 40231471210](https://github.com/baobab-platform/infrastructure/actions/runs/40231471210)
executed reviewed Infrastructure head `fe67b431abd884c8d48f82f096c0ca6a223ad9fc`
as tested PR merge `5d503f655e8db486e8203109d4947c3fd39c51de`.
[Artifact 12613007751](https://github.com/baobab-platform/infrastructure/actions/runs/40231471210/artifacts/12613007751)
ZIP SHA-256 is `5924677ccb71eb969d9c5863771176e359e2bbf22220cbc293060c4b77748491`,
independently verified against GitHub metadata. Original report SHA-256 is
`993d8ac582291d334efc05c9a7533fc33f49df548f9dc11175b30c465f42d112`;
both original report and base lifecycle receipt match their original-byte hashes.
The new original report/hash pair is retained in
[its separate evidence directory](evidence/subscriptions-2026-10-25/final-40231471210/),
leaving the initial receipt unchanged. Metadata expiry: `2026-11-08T20:39:06Z`.

All **20 exact cells** were checked: **17 native PASS / 3 independent BLOCKED**,
with no failures. Owner source pins match the merged CP/Subscriptions/Shared
commits above and the same IAM baseline. The additional database differential
proves a successful own-store TCP login and specific CP authentication refusal
using the engine credential. The original sixteen native observations, three
blocked reasons, seven false qualification/money flags and scoped COMPLETE
owned-resource cleanup are preserved. Recovery inside the lab and independent
host recovery both passed. This replaces the earlier receipt for the current
harness gate without converting INTERNAL or provider obligations into passes.

Infrastructure #59 merged as `00e6cd37515d1be731fa9b1f8da03d43ad11f4bc` after all 38 final-head checks completed (32 successful, six applicable skips) and all six review threads were resolved. The actual merged tree matches the reviewed head. The register pins this actual merge; the receipt truthfully retains the distinct tested PR merge SHA.


## Current INTERNAL authority source correction — 26 October 2026

CP #440 separates historical classification explanation from a live subscription
authority decision. A current group-eligible explanation could previously return
a positive waiver decision even when the subscription was SUSPENDED, expired or
not yet effective. The corrected path requires the exact ACTIVE and effective
subscription/classification tuple, matching current primary Organisation and
fresh governed eligibility. Tenant-bound callers cannot cause a foreign lookup.

One tenant-scoped SQL join reads the subscription and its pointed-to immutable
classification; the authority path no longer loads the full classification
history. Tests deliberately omit the history implementation to prevent its
accidental reintroduction. This improves query shape without a latency claim.
The decision is a bounded sequence of current CP reads, not an atomic CP/engine
fence, and its short response lease starts before evaluation.

Owner PG17 tests use synthetic governed relationships and admission actors. They
exercise persisted status/date changes and control-relationship revocation with
unchanged classification/grants. Such source/owner evidence cannot establish
independently verified legal eligibility. The previous Infrastructure 17/3 receipt
is immutable at its original pins; it does not certify this new CP source.
Full INTERNAL/onboarding/INT-07, provider and protected/production gates stay
partial, DEV-06 remains deferred and DEV-10 remains paused.

Final-head owner [Go/PG17 CI run 40250742014](https://github.com/baobab-platform/baobab-cp/actions/runs/40250742014),
[job 121341861769](https://github.com/baobab-platform/baobab-cp/actions/runs/40250742014/job/121341861769),
executed reviewed head `3abbde23ccac29bda854b75d24f4228fb38c61a9` as
tested PR merge `c2b88669dcc303b9981574cea094245d45710956`. The named
`TestCurrentInternalAuthorityNativeStatusDatesAndRevocation` test emitted an
explicit PASS (no SKIP); all race-enabled owner tests, vet and formatting passed.
The local environment lacked PG17, so its skipped native test was never counted.
The named CI step requires a nonempty test database configuration.

The new runbook explains response/error semantics, effective-date boundaries,
query shape, source/runtime limits and safe rollback.

CP #440 merged as `181a03a6f4644fdcddcd5ba67ae674049fd6235b` after all 31 final-head checks completed (25 successful, six applicable skips), with no unresolved review threads. The actual merged tree matches reviewed head. The register appends a distinct immutable source baseline; no prior source baseline, original receipt bytes, runtime case result or acceptance flag is rewritten.

[Current INTERNAL authority operator runbook](https://github.com/baobab-platform/baobab-cp/blob/181a03a6f4644fdcddcd5ba67ae674049fd6235b/docs/development/current-internal-authority.md).
