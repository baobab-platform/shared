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
