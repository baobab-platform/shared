# ADR-SHARED-016 — Provider Migration Execution and Engine Migration Tasks

| | |
|---|---|
| **Status** | Proposed |
| **Date** | 2026-09-28 |
| **Repository** | `baobab-platform/shared` |
| **Depends on** | baobab-cp ADR-BCP-006 §§44-58, 84, 94-95, 119-132; ADR-BCP-021 §§14-29, 47-61; ADR-BCP-022 §§44-67; ADR-SHARED-012; ADR-SHARED-015 |
| **Applies to** | `baobab-cp`, and every engine whose provider can be the source or target of a provider migration |

## Context

`control-plane/v1` describes the provider migration's plan and lifecycle (`provider-migration.schema.json`, `provider-migration-lifecycle.yaml`), but nothing executes a migration past PLAN. The lifecycle says every advance past PLAN is a controlled mutation that runs as a durable operation, but it does not say how approval gates the stages, or what a stage does.

A STATELESS_REBIND migration moves bindings only, so the Control Plane can execute it by itself.

A STATEFUL_CUTOVER migration is different: its cohorts freeze writes, move business state, reconcile it and unfreeze. ADR-BCP-006 constrains how that can happen:
- the Control Plane selects providers and never owns their business state (§128);
- provider-specific logic belongs in adapters near the provider, never in the Control Plane (§§129-132);
- exactly one system stays authoritative for each mutable domain (§55), and dual write needs its own decision (§56);
- engine instances will attest their workload identity (§95).

Engines never touch the Control Plane's database. So the Control Plane needs a way to ask a specific engine instance to do canonical migration work, and to learn the outcome, without carrying the business data itself.

## Decision

**A provider migration executes as stage commands under one plan approval. The stateful steps of a STATEFUL_CUTOVER cohort are engine migration tasks: canonical work items that the assigned engine instance claims and reports on under its workload identity.**

### 1. Approval binds the plan once

- `POST /provider-migrations/{id}/approve` records an `ApprovalDecision` with subject `PROVIDER_MIGRATION`, bound to the current plan's id, version and digest (ADR-BCP-021 §50).
- The approver is the verified caller. It is never the principal who created the migration, and it holds `provider-migration:approve`.
- One APPROVED decision authorises the whole approved sequence of that plan. A replan, which yields a new digest, needs a new decision, and a blocked plan cannot be approved.

### 2. Each stage is an explicit, durable command

- `POST /provider-migrations/{id}/advance` names one lifecycle transition. It needs If-Match (the migration's revision), an Idempotency-Key and `provider-migration:execute`. It returns 202 with an `ExecutionOperation` of type `PROVIDER_MIGRATION_ADVANCE`.
- Every forward transition requires all of the following:
  - an APPROVED decision on the current digest;
  - a current plan that is not blocked, not expired and not stale (ADR-BCP-021 §§29-30):
    - **Expiry** applies up to and including `prepare`. Once execution has started, the approved plan stays in force until the migration ends, because a migration may rightly run for days.
    - **Staleness** is judged against authoritative state other than this migration's own effects: its MIGRATION bindings, shifted cohorts and retired sources. A change made outside the migration is what makes the plan stale, for example a new binding in scope, a target instance that became ineligible, or a context that no longer belongs to its cohort. A stale plan cannot advance, and the operator rolls back or cancels.
  - no other operation of the migration still running;
  - for the transitions that move authority (`canary` and `shift`), a cutover window that is open, where the request names one. Preparation, validation and retirement may run outside it.
- `cancel` and `roll_back` need no approval. Leaving or undoing a change is always available to the authorised operator.
- The operator may cancel only before any cohort's authority has moved.
- The approver of the current plan never advances it forward (`PROVIDER_MIGRATION_SELF_EXECUTION`, 403): approval and execution are held by different people for each migration, not only by permission. `cancel` and `roll_back` stay available to any executor.

`provider-migration-lifecycle.yaml` gains `stage_steps`, which fixes the plan operations each transition runs:

| Transition | Runs |
|---|---|
| `prepare` | `VERIFY_TARGET_READINESS`, then every `CREATE_MIGRATION_BINDING` |
| `shadow` | `START_SHADOW` |
| `canary` | `STOP_SHADOW` when shadowing, then the first cohort's steps up to and including `UNFREEZE_COHORT_WRITES` (STATEFUL_CUTOVER) or `SHIFT_COHORT` (STATELESS_REBIND) |
| `validate` | the current cohort's `VALIDATE_COHORT` |
| `shift` | the next cohort's steps, as for `canary` |
| `retire_old` | every `RETIRE_SOURCE_BINDING` |
| `complete` | nothing: it records completion once every source binding is retired |
| `cancel` | compensation: the MIGRATION bindings created by `prepare` are removed, and shadowing stops |
| `roll_back` | compensation by `rollback_strategy` (section 5) |

- A forward transition moves the stage when its command is accepted; `cancel` and `roll_back` move it when they finish. The operation reports the steps' progress, and it is RUNNING while it waits on engine migration tasks.
- A failed step fails the operation and sets `failure_reason`:
  - if no engine migration task had been issued, the transition is undone entirely and the stage is as it was, so the operator may issue it again;
  - otherwise the migration stays in the transition's stage with its cohort in its safe state (frozen, or still on the source), and the operator rolls back.
- An advance asked to stop through `/admin/operations/{id}/cancel` ends CANCELLED at its next resumption, its open tasks cancelled, leaving the same safe state.
- A step never runs twice with effect: every step is idempotent on its `step_id` and the migration.

### 3. Local steps and engine steps

**The Control Plane runs these steps itself**, on its own authoritative state:
- `VERIFY_TARGET_READINESS`, `CREATE_MIGRATION_BINDING` and `START_SHADOW`/`STOP_SHADOW` (binding modes);
- `SHIFT_COHORT`, which moves the cohort's source bindings to the target instances the plan fixed;
- `VALIDATE_COHORT`, which checks that resolution for the cohort's contexts selects the target, and that the target is HEALTHY;
- `RETIRE_SOURCE_BINDING`.

It never calls a provider.

**Engines run these steps**, as engine migration tasks: `FREEZE_COHORT_WRITES`, `MIGRATE_COHORT_DATA`, `RECONCILE_COHORT_DATA` and `UNFREEZE_COHORT_WRITES`.
- Each task is assigned to exactly one engine instance, in a role (SOURCE or TARGET), with the cohort, capabilities, provider and counterpart the plan fixed.
- The cohort's contexts are named by opaque identifiers only.
- A task never carries credentials, endpoints or business data.

Tasks are assigned as follows:

| Step | Assigned to | Meaning |
|---|---|---|
| `FREEZE_COHORT_WRITES` | SOURCE | The source refuses writes for the cohort's contexts in the migrated capabilities. It keeps refusing after the shift, because it is no longer authoritative. |
| `MIGRATE_COHORT_DATA` | TARGET | The target's migration adapter moves the cohort's state from the named source counterpart, adapter to adapter. The Control Plane never carries it. |
| `RECONCILE_COHORT_DATA` | SOURCE and TARGET, one task each | Each reports `record_count` and `content_digest` over the cohort's canonical projection. The step succeeds only when both sides match: equal digests where each side serves the cohort from one instance, and equal total counts in every case, since digests over different partitions are not comparable. A mismatch fails the step with `MIGRATION_RECONCILIATION_MISMATCH`, and the cohort stays frozen. |
| `UNFREEZE_COHORT_WRITES` | TARGET | Once the shift has made the target authoritative, the target accepts the cohort's writes. |

At every moment one side at most accepts the cohort's writes:
- the source, until the freeze;
- neither, from the freeze to the unfreeze;
- the target, after the unfreeze.

This satisfies §55 without dual write.

### 4. The engine migration task protocol

An `EngineMigrationTask` (`emt_…`) has a status of PENDING, CLAIMED, SUCCEEDED, FAILED or CANCELLED, plus an attempt count and a lease.

The workload routes, all requiring `provider-migration:task`:
- `GET /engine-migration-tasks` lists the caller's PENDING and CLAIMED tasks;
- `POST /engine-migration-tasks/{id}/claim` takes a lease;
- `POST /engine-migration-tasks/{id}/report` records SUCCEEDED or FAILED, with a result.

**Identity.** The caller's engine instances are never taken from the request. They are the instances whose Control Plane registration names the caller's workload client as the instance's attested workload. This implements §95 attestation under workload identity, with no static secrets. An instance with no attested workload has no claimant, so its tasks time out safely. A task assigned to any other instance does not exist for the caller (404).

**Leases.** A claim holds a lease, 300 seconds by default.
- A lease that expires unreported returns the task to PENDING with its attempt incremented. The task is at-least-once, so engine work is idempotent on the task id.
- Only the claimant reports, while its lease holds.
- A report is final, and replaying the same report is idempotent.

**Results.**
- A report carries `record_count` and `content_digest` (`sha256:`) where the step defines them.
- A FAILED report carries a registered `provider_migration_task_failure` reason code.
- Free text is at most 500 characters and never business data or card data.
- Results never contain customer records.

**Deadlines.** A task still unreported when its step's deadline passes (the cutover window's end, or 24 hours) fails with `MIGRATION_TASK_TIMEOUT`. The cohort is left frozen, which is the safe state, and the operator rolls back.

### 5. Rollback

`roll_back` first releases a cohort a failed advance left frozen but never shifted (SOURCE `UNFREEZE_COHORT_WRITES`, REVERSE). It then returns every cohort whose authority moved, most recent first, according to the request's `rollback_strategy`:

- **REBIND_SOURCE:**
  1. freeze the target (TARGET `FREEZE_COHORT_WRITES`);
  2. move the bindings back;
  3. unfreeze the source (SOURCE `UNFREEZE_COHORT_WRITES`).

  This is valid only while the source still holds the authoritative state, which is the plan's claim for this strategy.
- **RESTORE_AND_REBIND_SOURCE:**
  1. freeze the target;
  2. migrate the cohort back (SOURCE `MIGRATE_COHORT_DATA`, with the target as its counterpart);
  3. reconcile;
  4. move the bindings back;
  5. unfreeze the source.
- **FORWARD_FIX_ONLY:** `roll_back` is refused once any cohort's authority has moved (`MIGRATION_NOT_REVERSIBLE`). Before that, it runs only the release (`rollback_release`) and the removal.

Rollback tasks carry `direction: REVERSE`. The migration ends ROLLED_BACK once every cohort is back on the source and the MIGRATION bindings are removed.

### 6. Authority

The Shared registries gain the following:
- the scopes `provider-migration:approve` (human), `provider-migration:execute` (human) and `provider-migration:task` (workload);
- the permissions `provider-migration.approve` and `provider-migration.execute` (OPERATIONS, HIGH, platform, not delegable);
- the reason-code category `provider_migration_task_failure`: MIGRATION_RECONCILIATION_MISMATCH, MIGRATION_TASK_TIMEOUT, MIGRATION_TASK_REJECTED and MIGRATION_ADAPTER_UNAVAILABLE.

`provider-migration.plan` no longer says advancing is a changeset. It is approved by `provider-migration.approve` and advanced by `provider-migration.execute`. One administrator may hold both permissions, but never for the same migration: its approver never advances it forward (section 2).

## Consequences

- `control-plane/v1` changes:
  - it gains `engine-migration-task.schema.json`;
  - `ApprovalDecision` and `ExecutionOperation` gain the `PROVIDER_MIGRATION` subject and the `PROVIDER_MIGRATION_ADVANCE` type;
  - `provider-migration-lifecycle.yaml` gains `stage_steps`, `engine_steps` and `rollback_steps`;
  - `openapi.yaml` describes the two administrative and three workload operations. This is a minor version bump, and every change is additive.
- The Control Plane implements execution for both modes. Its engine instance registration records each instance's attested workload client, which is set through the controlled registration workflow (ADR-BCP-006 §94), never by the engine itself.
- Each engine that can be a migration source or target implements a migration adapter for its providers:
  - it polls or claims tasks for its instances;
  - it enforces the cohort write freeze;
  - it moves and reconciles state through its own adapters;
  - it reports outcomes.

  Until an engine does, a STATEFUL_CUTOVER migration involving it fails safely at its first task (`MIGRATION_TASK_TIMEOUT`, cohort frozen), never with two writers.
- Percentage rollout, dual write and automatic stage progression stay out of scope. Each needs its own decision.
- The ADR-BCP-006 §108 migration events (`provider.migration.stage-changed` and others, in the `com.baobab-platform` namespace) are a follow-up. Engines learn their work from the task API, not from events.
