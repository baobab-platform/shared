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

## Product separation (Phase 4)

`foundation-repository-gates.yml` remains the **stable compatibility orchestrator**. It accepts a `profile` input and activates only the matching gate family. Distinct product entrypoints call the same orchestrator so consumers can adopt one family without the full aggregate.

| Product | Workflow | Profile | Gate families |
|---|---|---|---|
| Compatibility (all) | `foundation-repository-gates.yml` | `full` (default) | contract + security + container |
| Contract | `foundation-product-contract.yml` | `contract` | classify, baseline, reproducibility, runtime, environment |
| Security (PR) | `foundation-product-security.yml` (`mode: pr`) | `security-pr` | classify, security (portable Trivy, native adapters, secrets, dependency review, SAST) |
| Security (deep) | `foundation-product-security.yml` (`mode: deep`) | `security-deep` | same jobs; intended for schedule / monitoring |
| Container / release | `foundation-product-container.yml` | `container` | classify, container policy, build, scan, SBOM |

Branch protection requires the single combined result **`foundation / Foundation / Result`**, emitted when a caller job with id `foundation` calls `foundation-repository-gates.yml` directly. Product wrappers add a level of reusable-workflow nesting, so their checks are named `foundation / foundation / Foundation / Result` and are **not** the required check. Use them only for additional, non-required runs such as scheduled deep security.

Existing callers that omit `profile` continue to receive `full` behaviour.

### Security trigger matrix

| Trigger | Authoritative product | Typical inputs |
|---|---|---|
| `pull_request` | Security PR and/or Contract | `dependency_review_enabled: true` when available; `advanced_security_enabled` only with GHAS |
| `push` to default branch | Contract and/or full compatibility | Match repository policy |
| `schedule` (weekly) | Security deep | Prefer `foundation-product-security.yml` with `mode: deep`; do not treat a deep-scan failure as a PR regression without triage |
| Release / tag pipeline | Container | `foundation-product-container.yml` when `container_artifact` is true; prefer `release_require_zero_exceptions: true` |
| Manual `workflow_dispatch` | Any product | Operator chooses profile or product workflow |

Dedicated org security templates (CodeQL, Bandit, secrets scan) remain available. Foundation security is the governance baseline; language-specific templates may add depth but must not contradict Foundation availability rules for private repositories.

## Dependency adapters and evidence (Phase 5)

Portable Trivy remains the language-independent dependency baseline. Phase 5 adds **ecosystem-native adapters** in `reusable-foundation-dependency-adapters.yml`, selected from classifier capabilities and `package_managers`:

| Ecosystem | Adapter |
|---|---|
| Node (`pnpm` / `npm` / `yarn`) | manager `audit` at high severity |
| Python (`uv` / `pip` / `poetry`) | `pip-audit` |
| Go | `govulncheck` |
| Rust | `cargo-audit` |
| Java | notice only (Trivy remains baseline until a native adapter is wired) |
| Terraform | lockfile presence notice; Trivy misconfig remains baseline |

### Evidence artifacts

| Artifact | Purpose |
|---|---|
| `foundation-exceptions` | Machine-readable exception summary + gate results |
| `foundation-sast-decision` | Explicit SAST mode/reason when CodeQL does not run |
| `foundation-dependency-adapters` | Adapter execution status |
| Container SBOM | Existing SPDX upload from the container product |

Retention is **90 days**. Foundation owns schemas; consumers own exception content. Release/container product defaults `release_require_zero_exceptions: true` so active waivers cannot ship without an explicit override.

## Visibility-aware behaviour

GitHub dependency review is activated only for pull requests in repositories where the feature is available. A private repository without GitHub Advanced Security receives an explicit notice and retains the language-independent Trivy filesystem, secret, and misconfiguration scan. This is an availability distinction, not a false claim of equivalent CodeQL or dependency-review coverage.

### SAST / CodeQL decision matrix

| Repository visibility | `advanced_security_enabled` | Languages classified | Result |
|---|---|---|---|
| public | `true` | yes | CodeQL runs per language |
| public | `false` | any | **SAST / Not available** (portable Trivy remains baseline) |
| private | `false` | any | **SAST / Not available** — does not attempt CodeQL upload |
| private | `true` | yes | CodeQL runs; caller asserts GHAS is licensed and enabled |
| any | any | none | **SAST / No languages** |
| any | any | waived exception | **SAST / Waived** |

Private repositories must not set `advanced_security_enabled: true` unless GitHub Advanced Security is actually enabled. The planner uses visibility plus the caller opt-in so a private repo without the opt-in cannot accidentally invoke CodeQL and fail on SARIF upload. When CodeQL does not run, the workflow emits a visible `SAST / Not available` (or Waived / No languages) check instead of a silent skip.

Dependency review uses the same visibility rule: available on public repositories, or on private repositories only when `advanced_security_enabled` is true. If a PR enables dependency review on a private repo without that claim, the job fails with an actionable error.

The `shared` repository may remain private. Organisation Actions access must permit Baobab repositories to call reusable workflows from it. Consumers continue to pin the exact `shared` commit SHA; they must not replace immutable pins with `main`.

## Stable result

Branch protection should require `Foundation / Result`. The aggregator succeeds only when every activated required job succeeds or is legitimately skipped. A failure, cancellation, or configuration failure remains a failure. Profile-gated jobs that are skipped because they are outside the selected product do not fail the aggregate. The aggregate job also publishes `foundation-exceptions.json` and fails when `release_require_zero_exceptions` is true and any exception remains active.

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
6. Migrate remaining repositories in cohorts; adopt product entrypoints where PR latency or schedule semantics require separation.
7. Disable and then remove the legacy metadata bridge.
