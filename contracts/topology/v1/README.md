# Topology contracts v1: engine releases and deployment observation

**Authority:** ADR-BCP-025 (Engine Release, Artifact Identity and Deployment Observation Model), gate ER-01. Amendments A1–A4 are incorporated.
**Runtime owner:** `baobab-platform/baobab-cp` records releases, holds each engine instance's desired release, accepts deployment observations and detects release drift (gates ER-02 to ER-05). This package defines their shape and policy only.

The Control Plane is not a CD system. It never builds, pushes, deploys or rolls back software, and it never calls cluster APIs. Infrastructure tooling reads the desired release and reports what it observes running.

## Files

- `domain.schema.json`: grammars and closed vocabularies.
  - Release versions are semantic versions with no build metadata. Statuses: `CANDIDATE`, `APPROVED`, `DEPRECATED`, `REVOKED`.
  - Artifact digests (`sha256:` plus 64 lowercase hex), repositories, platforms and display tags.
  - Source revisions (full 40-hex SHA) and declaration digests.
  - `contractMajorVersion`: the canonical integer form of a capability contract version (section 2.1.1).
  - Deployment regions, observed-release states and drift reasons.
  - Bounded metric names and labels.
- `release.schema.json`:
  - `EngineRelease` and its `Artifact`s, `ProviderSupport` (provider, capability, contract majors; A1) and `Provenance`.
  - `EngineReleaseRecordRequest`. The Control Plane mints the id, the status and the recorder.
  - `EngineReleaseStatusChangeRequest`. A revocation names a disposition for every instance that desires the release.
  - `EngineInstanceDesiredRelease`, as infrastructure tooling reads it.
- `deployment-observation.schema.json`:
  - `DeploymentObservationSubmission`, which carries no field the Control Plane assigns.
  - `DeploymentObservation`, with `recorded_at`, `ingestion_sequence` and the reporting workload.
  - The derived `ObservedRelease`.
- `release-policy.yaml`: the values the ADR leaves to Shared:
  - the release lifecycle;
  - which statuses may become or be read as desired;
  - what approval requires per environment;
  - observation TTL bounds and ordering;
  - drift grace periods and severities.
- `events.schema.json` and `asyncapi.yaml`: the section 2.10 events, all platform-scoped:
  - `control-plane.engine-release.recorded.v1`;
  - `control-plane.engine-release.status-changed.v1`;
  - `control-plane.engine-instance.desired-release-changed.v1`, which carries the desired artifacts so tooling need not poll;
  - `control-plane.engine-instance.release-drift-detected.v1`.
- `examples/`: a `baobab-payments` lifecycle in staging, with releases in every status, a rolling upgrade observed `MIXED` then settled, and a revoked release still running, plus one envelope per event.

Related changes outside this package:
- `engineReleaseId` and `deploymentObservationId` in `control-plane/v1/domain.schema.json`.
- The `ENGINE_INSTANCE_RELEASE` drift object type and the drift record's `reason_code`.
- The `deployment:observe` scope.
- The `engine_release` and `release_drift` reason codes.

## Rules the Control Plane enforces

- **Content is identity (section 2.2).** A digest identifies an artifact, and belongs to at most one release of one engine. A tag never identifies anything, and a reference with a tag and no digest is refused.
- **Releases are immutable (section 2.1).** Only status moves, with an audited reason. Re-recording a version is accepted only as a byte-identical replay.
- **Support is per provider and comes from the declaration (A1, A2).** Every provider belongs to the release's engine, and every capability is catalogued. Support equals the `IMPLEMENTED` support of the `.baobab/capability-provider.yaml` whose digest the release records.
- **Approval is not certification (A3).** `APPROVED` means the release may be desired. Certification is EA-09's separate record.
- **Only approved releases become desired, and revocation never leaves one desired (sections 2.4–2.5).** A desired-state read never returns a release that is not `APPROVED` or `DEPRECATED`.
- **Reporters, not engines, observe (section 2.9).** Observations come from registered infrastructure workloads holding `deployment:observe`, for their registered environments and regions only. Expired, missing or future-dated observations mean `UNKNOWN`.
- **Observation stays observation (section 2.8, A4).** Release drift appears in readiness and events. It never changes capability resolution; that is gate ER-06, which is not accepted.
- **Readiness consequence (owner ruling, gate ER-05).** Each drift reason's `readiness_effect` in `release-policy.yaml` is separate from its severity:
  - `BLOCKED` (`REVOKED_RELEASE_RUNNING`, `UNKNOWN_ARTIFACT_RUNNING`, `DEPLOYMENT_LOCATION_MISMATCH`): a readiness blocking reason, with the drift's own `release_drift` code, but only where the affected instance serves a mandatory dependency.
  - `DEGRADED` (`RELEASE_MISMATCH`, `RELEASE_UNOBSERVED`): visible in the snapshot's `degrading_reasons`, never a blocker.
  - Blocking propagates up Provider → Capability → Product → Estate → Tenant only through mandatory dependencies, and only when every usable binding of the capability is on an affected instance; otherwise it degrades. One instance's drift therefore does not block every tenant. A tenant can be BLOCKED while capability resolution keeps working: that asymmetry is intended until ER-06 is accepted.

## Routes

The Control Plane's `openapi.yaml` serves the routes as their gates land:

- Gate ER-02:
  - `POST /engine-releases` records a release. It takes workload `engine-release:record` or admin `topology:write`.
  - `GET /engine-releases` and `GET /engine-releases/{release_id}` read releases under `topology:read`.
- Approval (CANDIDATE → APPROVED) has no route of its own. It is the control-plane/v1 `ENGINE_RELEASE_APPROVAL` changeset, served by the generic changeset routes: its approver holds `engine-release:approve` and is neither the requester nor the release's recorder.
- Gate ER-03:
  - `POST /engine-releases/{release_id}/status-changes` deprecates or revokes a release under admin `topology:write`. Revocation disposes of every instance that desires the release, in the same transaction.
  - An engine instance's desired release is set or cleared by the control-plane/v1 `ENGINE_INSTANCE_DESIRED_RELEASE` changeset. Its approver holds `desired-release:approve`.
  - `GET /engine-instances/{engine_instance_id}/desired-release` is how infrastructure tooling reads it, under workload `desired-release:read` (or admin `topology:read`).
- Gate ER-04:
  - `POST /deployment-observations` appends one observation, under workload `deployment:observe` only. An administrator is not a reporter, and an engine never reports itself.
  - The reporter's registration is its workload-registry entry: its `environment`, and its `deployment_regions` (required of exactly the workloads that may hold `deployment:observe`). An observation for another environment or region is refused as `DEPLOYMENT_OBSERVATION_OUT_OF_SCOPE`, never stored.
  - `GET /engine-instances/{engine_instance_id}/deployment-observations` lists an instance's observations, and `GET /engine-instances/{engine_instance_id}/observed-release` reads the derived observed release, both under admin `topology:read`.

Validated by `scripts/validate-topology-contracts.py`.
