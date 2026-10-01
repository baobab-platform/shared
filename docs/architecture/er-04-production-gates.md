# ER-04 production gates

**Authority:** owner rulings of 2026-10-01 on ADR-BCP-025 §2.9 and on the Shared workload registry (shared#148). This page records them as explicit gates. They are not implementation choices.

ER-04 and ER-05 are implemented and tested with controlled test reporters. Their production evidence stays **NOT OPERATIONALLY PROVEN** until every gate below is closed.

## Decision 1: the workload registry is production authority

Shared owns each workload's ID, credential profile, audience, scopes and lifecycle. `PROVISIONED` means registered but not proven end to end. `ACTIVE` means the identity provider can issue or exchange the credential, the actual resource server accepts it, and the audience and scope constraints are proven.

Therefore:

- A production Control Plane loads the canonical registry at startup and **fails closed** when it is missing or invalid. It never disables lifecycle enforcement and keeps serving.
- A workload that is not `ACTIVE` has no runtime authority at the Control Plane.
- Existing `ACTIVE` entries are reconciled against the deployed identity provider and resource-server path **before** enforcement is switched on: `baobab-cms-workload`, `baobab-erp-workload`, `baobab-pulse-workload`, `baobab-trade-workload`, `thamani-backend`, `zuribeans-backend`. An entry that cannot meet the `ACTIVE` definition has its status or evidence fixed. Enforcement is never weakened.
- `baobab-cp-workload` and `baobab-subscriptions-workload` stay `PROVISIONED`. Loading the registry does not promote them.

## Decision 2: the reporter is the infrastructure deployment controller

- The reporter is infrastructure-owned deployment tooling, registered as `baobab-deployment-controller-production` (`PROVISIONED`).
- **No admission webhook.** Production is ECS/Fargate and EKS is deferred.
- It authenticates with a federated workload token and holds **no static secret**.
- It reads desired releases (`desired-release:read`) and reports observations (`deployment:observe`) for `production` / `af-south-1` only.
- It reports the artifact digest it observes **actually running** in ECS, not the release it intended to deploy. Infrastructure post-deployment verification already requires the task digest, service version and health.
- It reports **after each verified deployment and periodically**. Observations expire within `release-policy.yaml` `observation.ttl_seconds.maximum` (3600 s), and `RELEASE_UNOBSERVED` grace is 900 s, so a deploy-time-only reporter would read as unobserved. A five-minute cycle matches the 300 s drift sweep.
- Neither an engine nor the Control Plane attests that a deployment succeeded.

## Gate sequence

```
Workload registry authority (Shared)
        ↓
Production CP loads and enforces it (fail closed)
        ↓
Existing ACTIVE workloads reconciled
        ↓
Deployment controller identity configured; no-static-secret exchange proven
        ↓
CP accepts aud=baobab-control-plane, deployment:observe, production, af-south-1
        ↓
Deployment controller PROVISIONED → ACTIVE
        ↓
First actual ECS observation received
        ↓
ER-04 / ER-05 operationally proven
        ↓
CP → Subscriptions → Payments live proofs; later PROVISIONED → ACTIVE promotions
```

## Unchanged

ADR-BCP-025 amendment A4 stands: drift, events and metrics are not capability routing exclusion. **ER-06 stays off.**
