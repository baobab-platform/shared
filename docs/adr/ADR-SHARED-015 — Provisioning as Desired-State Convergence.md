# ADR-SHARED-015 — Provisioning as Desired-State Convergence

| | |
|---|---|
| **Status** | Accepted |
| **Date** | 2026-09-26 |
| **Repository** | `baobab-platform/shared` |
| **Depends on** | Provisioning Technical Specification §§21-27, 42-44; baobab-cp ADR-BCP-017, ADR-BCP-019 §§28-33, ADR-BCP-021 §§14-29, 47-61, ADR-BCP-022 §§44-67; ADR-SHARED-012 |
| **Applies to** | `baobab-cp` and every consumer of `control-plane/v1` provisioning, plan, approval and operation contracts |

## Context

The administrative OpenAPI did not describe tenant provisioning (Console gap B2). Describing the Control Plane's routes as they stood would have made its implementation canonical, and that implementation diverges from the specification:

- **Desired state.** The request body was an engine-level manifest: capability grants, bindings to named engine instances, and trade lanes. A caller could therefore wire engines directly, bypassing the planner. The specification's desired state is business intent (products and profiles, market participation, estates, isolation and residency), and the AUTHORISED TenantOnboardingRequest already carries most of it.
- **No plan approval.** One call planned and applied. The specification (§25) and ADR-BCP-019/021 require a side-effect-free plan, reviewed and approved, before anything changes.
- **Conflated states.** The run states (PLAN, APPLY, RECONCILE, READY, ACTIVE, FAILED, CANCELLED) mix phase, command, process status and business state.
- **Old identifiers.** Engine names predated ADR-SHARED-012.

Shared also held a misnamed `provisioning-plan.schema.json` whose only definition was the process aggregate. It paired a coarse state with a `current_phase`, which meant two overlapping state machines.

## Decision

**Shared describes tenant provisioning as declarative desired-state convergence, not as direct engine configuration.**

1. **Desired state comes from the AUTHORISED TenantOnboardingRequest.**
   - `ProvisioningDesiredState` holds the tenant, products and their profiles, market participation, digital estates, legal entities, and isolation and residency requirements.
   - It records its provenance (onboarding request, admission decision, desired-state version) and a digest.
   - It never names engines, engine instances, providers, capability grants or bindings. Those are consequences of planning.
   - It is persisted independently of any plan, so a failed plan can be replanned (for example onto another engine instance) without changing intent.
   - Creating a provisioning names its source (`tenant_onboarding_request_id`). It never accepts a manifest.
2. **Planning is side-effect free.** It reads, resolves, calculates and analyses, and never creates or changes runtime resources, grants, IAM or providers (ADR-BCP-021 §20).
   - The result is an immutable `ProvisioningPlan`: a `ChangePlan` (ADR-BCP-021 §21) with a version, `plan_digest`, `base_revision`, canonical operation steps, blockers, warnings, readiness requirements, security checks, impact analysis and risk class.
   - Plan steps may name topology, and when they do it is in ADR-SHARED-012 identifiers (`baobab-trade`, `medusa`, `ei_…`).
   - The Control Plane's former engine-level manifest becomes an internal execution artefact derived from the plan.
3. **Approval binds the exact plan.**
   - An `ApprovalDecision` (ADR-BCP-021 §50) records the plan id, version and digest, the decision (APPROVED, REJECTED or CHANGES_REQUESTED) and the verified approver.
   - A changed digest needs a new decision. The approver is never the requester.
   - An AUTHORISED onboarding request authorises business intent. It does not pre-approve any plan derived from it.
4. **Apply is a separate, asynchronous command.**
   - It runs only an approved plan that is not stale and whose digest matches the approval.
   - It returns 202 with an `ExecutionOperation` (ADR-BCP-021 §59, ADR-BCP-022 §58), located at `/admin/operations/{operation_id}`.
   - Retry and cancel are operation commands (`/admin/operations/{id}/retry` and `/cancel`), never provisioning subresources.
5. **Three lifecycles stay distinct.**
   - **TenantProvisioning** follows Technical Specification §22: DRAFT, VALIDATING, PLANNED, REGISTERING, CONFIGURING_CONTEXT, PROVISIONING_ENTITLEMENTS, PROVISIONING_PROVIDERS, VALIDATING_SECURITY, VERIFYING_READINESS, BLOCKED, REMEDIATING, READY and ACTIVE, with FAILED, CANCELLED and DEPROVISIONED as terminal states.
   - **ExecutionOperation** follows ADR-BCP-022 §59.
   - **Readiness** is UNKNOWN, NOT_READY, BLOCKED, DEGRADED or READY.
   - BLOCKED means a known, remediable condition. FAILED means an operational failure. REMEDIATING is the deliberate resolution of known blockers, not a retry.
6. **Routes.** Under `/tenants/{tenant_id}/provisioning`:
   - create (plan only), list and read;
   - `/plan`, `/approve` and `/apply`;
   - `/readiness` and `/drift`.

   Operations have their own routes: `/admin/operations/{operation_id}`, with `/retry` and `/cancel`.
7. **Legacy projection.** The coarse `provisioning-state-machine.yaml` states become a deprecated projection of the canonical lifecycle, mapped in `tenant-provisioning-lifecycle.yaml`, for consumers of the existing provisioning events. New consumers use the canonical state.

## Consequences

- `control-plane/v1` gains:
  - `provisioning-desired-state.schema.json`, `change-plan.schema.json`, `approval-decision.schema.json`, `execution-operation.schema.json` and `tenant-provisioning.schema.json`;
  - `tenant-provisioning-lifecycle.yaml`;
  - a rewritten `provisioning-plan.schema.json` holding the real plan.

  `ChangePlan`, `ApprovalDecision` and `ExecutionOperation` are generic, and the Changeset programme (ADR-BCP-021, Console gap G6) reuses them unchanged instead of provisioning growing a private approval model.
- `openapi.yaml` 1.8.0 describes the eight provisioning operations and the three operation operations. The scopes `provisioning:approve`, `operation:read` and `operation:control` are registered.
- The Control Plane migrates:
  - `POST` stops at PLANNED and no longer accepts a manifest;
  - its run states map onto the canonical lifecycle;
  - approval and asynchronous apply use durable operations;
  - retry and cancel move to operations;
  - its manifest becomes internal.

  Its current routes stay in its drift test's undescribed list until each conforms.
- The onboarding request's desired state gains the specification's richer fields (legal entities, estates, market activities, product profiles) additively when admission starts to capture them. Until then those parts of `ProvisioningDesiredState` are empty.
- The existing provisioning events keep their coarse states. A later change may add the canonical state to them additively.
