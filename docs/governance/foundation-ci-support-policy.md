# Foundation CI support policy

## Supported consumers

Foundation CI is distributed from the private `baobab-platform/shared` repository. GitHub permits this reuse only where the caller can access private organization workflows. The supported production estate is therefore:

- private Baobab repositories;
- internal repositories where the organization plan and policy permit access; and
- exact immutable commit-SHA references.

Public repositories are not supported callers while `shared` remains private. A public repository must be made private before its Foundation caller is enabled. The rollout inventory must treat a workflow that never starts as an access/configuration failure, not as a successful or not-applicable gate.

## Promotion requirements

A Foundation revision is promotable only after all of the following are green:

1. workflow and contract static validation in `shared`;
2. the `shared` self-consumer run;
3. one representative private consumer for every activated runtime or artifact class;
4. verification of the exact emitted result check name; and
5. consumer references pinned to the promoted commit SHA.

The stable reusable entry point remains `.github/workflows/foundation-repository-gates.yml`. Consumers must not reference its internal component workflows directly. Product entrypoints (`foundation-product-*.yml`) are supported wrappers over the same orchestrator.

### Current promoted release

See `docs/governance/foundation-ci-promotion-v2.2.0.md`.

- **Tag:** `v2.2.0`
- **Peeled SHA:** `ddd2c56f52b60472f0af1fd2e896e9cdd14bb636` — consumers pin this SHA in both `uses:` and `foundation_ref`.
- **Requires:** `baobab-dev` 1.4.4 or newer in every profile. Bump the declared image in the same change as the repin.
- **Previous release:** `v2.1.0` (`53ed9cd`, see `foundation-ci-promotion-v2.1.0.md`).
- **`v2.0.0`:** tagged before the promotion criteria were met; superseded. Do not pin it.

## Required check

The consumer's caller job id becomes part of GitHub's displayed check context. Use a consistent caller job id of `foundation`. Rulesets must be configured from the check emitted by a successful pilot run, rather than from a guessed display name.

Expected aggregate name pattern (self-consumer):

```text
foundation / Foundation / Result
```

## Evidence artifacts (Phase 5)

Foundation uploads retained workflow artifacts so waived controls and fallback SAST decisions are inspectable after the run.

| Artifact name | Produced by | Content |
|---|---|---|
| `foundation-exceptions` | `Foundation / Result` | `foundation-exceptions.json` — active exceptions, profile, gate results |
| `foundation-sast-decision` | SAST planner | `foundation-sast-decision.json` — mode, visibility, reason |
| `foundation-dependency-adapters` | Native dependency adapters | Adapter status per ecosystem |
| Container SBOM (existing) | Container product | SPDX via anchore/sbom-action |

**Retention:** 90 days (GitHub Actions default override on each upload).
**Ownership:** Foundation maintainers own schema and retention policy; consuming repositories own the content of declared exceptions and must keep them current.
**Release policy:** set `release_require_zero_exceptions: true` on container/release callers so active waivers cannot silently ship.

## Failure ownership

A run that does not create jobs is a Foundation distribution or GitHub configuration defect. A started gate reporting `misconfigured` is a repository contract defect. A started applicable gate reporting `failed` is a policy or repository defect. Only an explicit classifier decision may make a control not applicable.

For SAST: a private repository without an approved `security.ghas` record must never reach a CodeQL upload. It receives an explicit **SAST / Fallback** decision, or fails classification if it declares `codeql` without the approval. CodeQL running there anyway is a Foundation distribution defect.
