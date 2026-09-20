# Foundation CI v2

Foundation CI enforces Baobab-wide governance and reproducibility contracts. It does not replace application tests, builds, migrations, releases, or deployments.

## Repository contract

Every governed repository declares `.baobab/repository.yaml`. The declaration is authoritative; strong file evidence may add a capability but never removes a declared one. The contract is intentionally limited to lifecycle, capabilities, development-environment participation, package-manager intent, produced artifacts, and controlled exceptions.

During the organisation rollout only, consumers without the new contract may use existing `.baobab/environment.yaml` or `.nabhold/environment.yaml` metadata. Such runs emit a migration warning. Set `legacy_metadata_enabled: false` in a pilot consumer to prove full migration. The bridge is scheduled for removal after all consumer pins have moved to the v2 Foundation commit.

## Capability evidence

| Capability | Strong evidence |
|---|---|
| Python | `pyproject.toml` at the root or in a module |
| Node | root `package.json` |
| Go | root `go.mod` |
| Java | Maven POM or Gradle build metadata |
| Container | a Dockerfile in the repository |

The classifier publishes Boolean workflow outputs. Downstream jobs use those outputs to activate only relevant controls.

## Visibility-aware behaviour

GitHub dependency review is activated only for pull requests in repositories where the feature is available. A private repository without GitHub Advanced Security receives an explicit notice and retains the language-independent Trivy filesystem, secret, and misconfiguration scan. This is an availability distinction, not a false claim of equivalent CodeQL or dependency-review coverage.

The `shared` repository may remain private. Organisation Actions access must permit Baobab repositories to call reusable workflows from it. Consumers continue to pin the exact `shared` commit SHA; they must not replace immutable pins with `main`.

## Stable result

Branch protection should require `Foundation / Result`. The aggregator succeeds only when every activated required job succeeds or is legitimately skipped. A failure, cancellation, or configuration failure remains a failure.

## Ownership boundary

| Foundation CI | Repository CI |
|---|---|
| Metadata and lifecycle | Unit and framework tests |
| Action pinning and least privilege | Domain integration tests |
| Lockfile consistency | Database migrations |
| Development-environment compatibility | Application builds and E2E |
| Baseline security and container policy | Release and deployment logic |

## Rollout

1. Merge and verify `shared`.
2. Record the immutable merge SHA.
3. Pilot one Go engine, one Node service, one Python service, one digital estate, and one infrastructure repository.
4. Add `.baobab/repository.yaml`, rename legacy `.nabhold/` metadata, and update the pinned workflow SHA in each pilot.
5. Correct genuine repository defects without weakening Foundation policy.
6. Migrate remaining repositories in cohorts.
7. Disable and then remove the legacy metadata bridge.

