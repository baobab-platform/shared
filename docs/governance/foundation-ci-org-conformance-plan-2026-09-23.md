# Foundation CI: organisation conformance audit and implementation plan

**Date:** 2026-09-23
**Scope:** every repository in `github.com/baobab-platform` (16 repositories)
**Baseline:** *Baobab Shared CI Workflow Conformance Audit* (2026-09-21, commit `de8a628`)
**Shared revision re-audited:** `main` @ `f39afe5`, tag `v2.0.0` @ `80d7f25`, open PR #68 @ `148050f`

## 1. Summary

Since the baseline audit, `shared` has merged fixes for the audit's first three findings (#64 caller template, #65 visibility-aware SAST, #66 promotion record) and cut `v2.0.0`. PR #68 covers the Medium findings (product separation, native dependency adapters, exception evidence).

The organisation is still **not conformant**, and the gap is larger than the baseline audit showed. The baseline audit only looked at `shared`. Across the organisation:

1. **No GitHub Actions job has started on any runner since about 2026-09-20.** Every job ends in about 4 seconds with `runner_id: 0`, no steps, and no logs. This happens on public and private repositories, on `ubuntu-24.04` and `ubuntu-26.04`, and in GitHub's own managed *Code Quality* workflow. It is an organisation-level Actions or billing block, not a workflow defect. The change to `ubuntu-24.04` (#67) did not fix it.
2. **Foundation v2 has never passed a run.** Foundation Static Validation is 0/42. `v2.0.0` was tagged on a commit whose CI was red. This breaks the support policy, and the promotion record still says "tag not yet cut".
3. **12 of 15 consumer repositories call `nabhold/shared/...`**, the path from before the organisation rename. GitHub treats those workflow files as invalid: runs have no jobs and no `referenced_workflows`. **These repositories have had no Foundation coverage at all**, even before the runner block. 61 workflow files across 13 repositories carry this path, including all 9 files in `engine-template`, so every new repository inherits it.
4. **No consumer uses v2.** The live pins are 76 to 178 commits behind `main`, and all of them predate the `foundation_ref` input. The migration branches (`chore/foundation-ci-v2` in all 15 repositories) are well formed but pin `5d8445c`, which is 26 commits before `v2.0.0` and lacks the Phase 1 and Phase 2 fixes.
5. **`shared` `main` has a real code failure as well.** Commit `f39afe5` ("Update registry.yaml", pushed directly to `main`) renamed the legal entity `BAOBAB-PLATFORM` back to `NABHOLD`. `scripts/validate-governance-contracts.rb` still required `BAOBAB-PLATFORM`, so CI would have stayed red after the runner block was lifted. **Fixed on `claude/funny-darwin-ubfzsm`** (D1): the validator now requires `NABHOLD`.

The milestone is still **Foundation CI v2 consumer readiness**. It now depends first on execution (Phase 0) and distribution (Phase 5), not on more workflow features.

## 2. Status of the baseline audit findings

| # | Baseline finding | Status on `main` | Status with PR #68 | Remaining gap |
|---|---|---|---|---|
| H1 | Caller template not executable | **Fixed** (#64, fixture `test_caller_template.py`) | — | Consumers never adopted it. `baobab-dev` still grants only `contents: read`, and v1.4.0 needs `packages: read`, so it gets `startup_failure`. |
| H2 | CodeQL availability is caller-asserted | **Partial** (#65) | Unchanged | `private + advanced_security_enabled: true` is still a trusted boolean. There is no `sast_provider` and no reviewed, repository-level declaration. |
| H3 | Revision not promoted | **Not met.** `v2.0.0` was tagged with requirements 1 to 3 blocked. | — | Tag cut on red CI. Record is stale. No pilots have run. |
| M1 | Foundation aggregates separate products | Open | **Addressed with defects** (§4) | Wrappers change the emitted check name. |
| M2 | Scheduled deep-security boundary | Open | **Nominal only** | `security-pr` and `security-deep` run the same jobs. There is no changed-scope or full-history split. |
| M3 | No native dependency adapters | Open | **Addressed with defects** (§4) | The Python adapter does nothing. `cargo-audit` is not checksum-verified. |
| M4 | Weak exception observability | Open | **Addressed** | `foundation-exceptions.json`, step summary, `release_require_zero_exceptions`. |
| L1 | No single fixture command | **Fixed on `claude/funny-darwin-ubfzsm`** | — | `scripts/test-foundation.sh` plus `.github/foundation-tests/requirements.txt`. Before this, CI got `jsonschema` only indirectly through `check-jsonschema`, and local runs had nothing declared. |

## 3. Organisation inventory

Visibility comes from the GitHub API. "Live pin" is the ref on the default branch. Every migration branch pins `5d8445c` with the full v2 permission set, `advanced_security_enabled: false`, and `legacy_metadata_enabled: false`.

| Repository | Vis. | Detected stack | Live Foundation caller | Stale `nabhold/` files | `.baobab/repository.yaml` on `main` / migration | Migration-branch issue |
|---|---|---|---|---|---|---|
| shared | pub | pnpm, contracts | self @ `github.sha` | 0 | yes | — (CI red: §1.5) |
| baobab-cp | pub | Go, container | `nabhold/…@d6c751a` → **invalid** | 5 | no / yes | — |
| zuribeans | pub | Node/pnpm, container | `baobab-platform/…@bf72e37` (v1.4.0^2), `contents`+`packages` only | 0 | no / yes | — |
| baobab-dev | priv | Python/uv | `baobab-platform/…@f7466cc` (v1.4.0), `contents` only → **startup_failure** | 0 | no / yes | — |
| baobab-cms | priv | Node, container | `nabhold/…@d6c751a` → **invalid** | 1 | no / yes | — |
| baobab-erp | priv | undetected at root | `nabhold/…@d6c751a` → **invalid** | 4 | no / yes | `dependency_review_enabled: true` without GHAS |
| baobab-iam | priv | container | `nabhold/…@d6c751a` → **invalid** | 8 | no / yes | `dependency_review_enabled: true` without GHAS |
| baobab-payments | priv | undetected at root | `nabhold/…@317538b` → **invalid** | 7 | no / yes | — |
| baobab-pulse | priv | Python/uv, container | `nabhold/…@d6c751a` → **invalid** | 7 | no / yes | — |
| baobab-subscriptions | priv | undetected at root | `nabhold/…@317538b` → **invalid** | 8 | no / yes | — |
| baobab-trade | priv | Node, container | `nabhold/…@d6c751a` → **invalid** | 4 | no / yes | `dependency_review_enabled: true` without GHAS |
| equator-estate | priv | container (digital estate) | `nabhold/…@c518b9a` → **invalid** | 1 | no / yes | — |
| infrastructure | priv | undetected at root | `nabhold/…@d6c751a` → **invalid** | 1 | no / yes | — |
| nabhold | priv | Node/pnpm, container | `nabhold/…@c518b9a` → **invalid** | 2 | no / yes | — |
| thamani | priv | Node/pnpm, container | `nabhold/…@c518b9a` → **invalid** | 4 | no / yes | `dependency_review_enabled: true` without GHAS |
| engine-template | priv | template | `foundation.yml.example` only | 9 | no / **no** | Template ships no repository declaration. New engines start non-conformant. |

Other drift:

* Six repositories (erp, pulse, trade, equator-estate, infrastructure, nabhold) have open Dependabot branches that bump the `nabhold/shared` path. Merging them keeps the invalid reference. Close them.
* In the four private repositories flagged above, a pull request will fail by design with "Dependency review is required but unavailable on this private repository". Each one needs `false` plus a reviewed `dependency-review` exception, or GHAS.
* On `main`, 35 of 36 `runs-on` values were `ubuntu-26.04`. #67 changed only `foundation-static-validation.yml`, and PR #68 moves seven more jobs to `ubuntu-24.04`. The standard is now **`ubuntu-26.04`** (§6, D5). This branch moves the last job back and adds a fixture that rejects any other label.

## 4. PR #68 review: fix before merge

1. **The Python adapter does nothing.** `pip-audit -l uv.lock` is not a lockfile audit: `-l` is `--local`, so the extra argument is rejected. The `|| pip-audit` fallback then audits the runner's own environment, which passes every time. The same applies to `poetry.lock`. Fix: `uv export --frozen --no-hashes --format requirements-txt > req.txt && pip-audit -r req.txt --disable-pip`, `poetry export` for Poetry, and remove every `|| pip-audit` fallback.
2. **`cargo-audit` is downloaded without checksum verification.** This contradicts the checksum-verified Trivy pattern that `reusable-foundation-security.yml` uses. Pin a SHA-256 and verify it, or use `taiki-e/install-action` pinned to a SHA.
3. **The aggregator now accepts every `skipped`.** `failed = … !%w[success skipped]` removes the baseline's "unexplained skip is a failure" guarantee for all profiles. Only jobs that the selected profile excludes may be skipped. Compute the expected set per profile and fail on any other skip.
4. **`security-pr` and `security-deep` are identical.** To close M2, the profiles must behave differently:
   * PR: gitleaks limited to the PR commit range, dependency review on, native adapters on changed manifests.
   * Deep: gitleaks over full history, dependency review off, full Trivy and container scan.
   * Both publish different result names, for example `Security / PR` and `Security / Deep`, so branch protection never depends on a check that only runs on a schedule.
5. **Product wrappers change the check context.** Caller job `foundation` → wrapper job `foundation` → `Foundation / Result` is emitted as `foundation / foundation / Foundation / Result`, although the docs say the name stays the same. Branch protection will require only the single combined result from the compatibility entrypoint (D3). So the wrappers are optional extras, and the docs must say they do **not** produce the required check.
6. **Nesting depth.** Caller → product → gates → security → adapters or secrets-scan is five levels of reusable workflows. Check this against GitHub's current nesting limit before merge, and add a wiring assertion for the depth.
7. **Runner labels.** PR #68 changes seven jobs to `ubuntu-24.04`, and its new `reusable-foundation-dependency-adapters.yml` uses `ubuntu-24.04`. Change all of them to `ubuntu-26.04`. Once this branch is merged, the runner-label fixture will fail PR #68 until that is done.
8. Minor: `actions/setup-python@ad3497a…` has no version comment. Add one so the pinning audit stays readable.

## 5. Implementation plan

Phases are ordered by dependency. Nothing after Phase 0 can be verified until jobs start again.

### Phase 0: restore Actions execution (organisation admin, blocking)

The owner needs admin access to the `baobab-platform` organisation. This cannot be fixed from a pull request.

* **Decision D2: subscribe `baobab-platform` to GitHub Team.** A Free organisation that the migration created without a payment method or spending limit fits these symptoms. After subscribing, set the Actions spending limit or budget so jobs are not stopped at the included-minutes quota.
* If jobs still do not start after subscribing, check the organisation's **Billing & plans** page (Actions spending limit, failed payment, account lock) and **Settings → Actions → General** (Actions allowed, allowed-actions policy, runner-group access for GitHub-hosted runners). Compare with the pre-migration `nabhold` organisation, where the last green run was on 2026-09-19 22:44 UTC.
* Open one failed job in the web UI. The job-level banner states the reason even when the API returns 404 for logs.
* Set **Settings → Actions → General → Access** on `shared` so the organisation's repositories can use its reusable workflows. This matters if `shared` is ever made private again (#53 and #54 mention this).
* **Done when:** a trivial `workflow_dispatch` job on `shared` runs on a runner and succeeds.

### Phase 1: `shared` `main` green

1. ✅ *(this branch)* `scripts/validate-governance-contracts.rb` now requires legal entity `NABHOLD`, matching `contracts/legal-entity/registry.yaml` after `f39afe5` (D1).
   * Still to review: other places where the rename's search-and-replace changed business identifiers instead of GitHub paths. From `git show 3017473`, suspects are `contracts/tenancy/tenancy.yaml` and `contracts/development-environment/schema.yaml` (both have "BAOBAB-PLATFORM GROUP AFRICA" headers), `contracts/identity/v1/workload-registry.yaml`, and the legal-entity/digital-estate separation ADR.
2. ✅ *(this branch)* Every workflow runs on `ubuntu-26.04` (D5). `test_workflow_wiring.py` fails on any other `runs-on` label.
3. ✅ *(this branch)* Added `.github/foundation-tests/requirements.txt` and `scripts/test-foundation.sh`. The script runs all Python and Ruby fixtures and fails if `ruby`, `python3` or the Python dependencies are missing. `foundation-static-validation.yml` calls it.
4. Protect `main` with a ruleset (require PRs, plus Foundation Static Validation and CI). `f39afe5` went straight to `main`.
5. **Done when:** CI, Foundation Static Validation and the Foundation Repository Gates self-consumer are all green on `main`.

### Phase 2: harden and merge PR #68

Fix items 1 to 8 in §4. Add fixtures for the following:

* Python adapter: a lockfile containing a known-vulnerable pin must fail.
* Aggregator: a skipped job that the profile does not exclude must fail.
* PR and deep profiles: they select different secret-scan scope and emit different result names.

**Done when:** the self-consumer passes under `full`, `contract`, `security-pr`, `security-deep` and `container` through `workflow_dispatch`, and the emitted check names are recorded in the support policy.

### Phase 3: close H2 (SAST provider decided in the repository contract)

* GitHub Team does not include Code Security (CodeQL and dependency review on private repositories); that is a separate paid add-on. So private repositories default to `fallback`. CodeQL runs only in the public repositories: `shared`, baobab-cp and zuribeans.
* Add `security.sast_provider: codeql | fallback | disabled` to `.baobab/repository.schema.json`. The classifier resolves it together with `github.event.repository.visibility`:
  * `private` + `codeql` requires a `security.ghas` approval record (`approved_by`, `reason`, `expires`), validated like exceptions.
  * Private repositories default to `fallback`. The result is `SAST / Fallback`, and the portable Trivy evidence is uploaded as `foundation-sast-decision.json`.
* Keep `advanced_security_enabled` for one minor version as a deprecated override. When it disagrees with the declaration, emit `::warning::`.
* Apply the same resolution to dependency review, so both controls come from one availability decision.
* **Done when:** fixtures cover all six combinations of {public, private} × {codeql, fallback, disabled}, and a private repository cannot reach CodeQL upload without an approval in its contract.

### Phase 4: honest re-promotion

* Do not move `v2.0.0`. Mark it in the promotion record and the CHANGELOG as *"tagged before promotion criteria were met; superseded"*.
* Promote **`v2.1.0`** (D4), following `foundation-ci-support-policy.md` exactly:
  1. Static validation passes.
  2. The self-consumer passes.
  3. The pilot cohort (Phase 5A) is green on the candidate SHA.
  4. The emitted check names are recorded.
  5. Only then, the tag is cut.
* Update `templates/caller-foundation-repository-gates.yml` so its TODO names the promoted SHA. Update `foundation-ci-promotion-*.md` to *Promoted* and record the peeled SHA.
* **Done when:** the tag points at a commit with green runs for requirements 1 to 4, all linked from the record.

### Phase 5: consumer rollout

Every repository needs the same three changes:

1. Rebase `chore/foundation-ci-v2` onto `main`, and repin `uses:` and `foundation_ref` to the candidate SHA (pilots) or the promoted SHA (everyone else).
2. Rewrite **every** `nabhold/shared/` reference to `baobab-platform/shared/` at the same promoted SHA, not only in `foundation.yml`. Close the Dependabot PRs that bump the `nabhold/` path.
3. Merge. Confirm `foundation / Foundation / Result` is green on `main`. Then remove `.nabhold/environment.yaml`.

**5A: pilots** (the cohort from `foundation-ci-v2.md`, run against the candidate SHA before the tag):

| Pilot role | Repository | Extra work |
|---|---|---|
| Go engine | baobab-cp (public) | 5 stale files. Its public repository makes it the CodeQL-on check. |
| Node service | zuribeans (public) | Replaces the v1.4.0^2 pin. Also checks the original CodeQL failure no longer happens. |
| Python service | baobab-dev (private) | Fixes the live `startup_failure`. SAST fallback path. |
| Digital estate | equator-estate (private) | Container product with `release_require_zero_exceptions`. |
| Infrastructure | infrastructure (private) | Terraform capability. Confirm the classifier detects it, since nothing was found at the repository root. |

**5B: remaining services:** baobab-cms, baobab-erp\*, baobab-iam\*, baobab-payments, baobab-pulse, baobab-subscriptions, baobab-trade\*, nabhold, thamani\*.
\* Set `dependency_review_enabled: false` and declare a reviewed `dependency-review` exception before merging. GitHub Team alone does not make dependency review available on private repositories (D2).

**5C: `engine-template`:**

* Add `.baobab/repository.yaml` with placeholder capabilities.
* Rename `foundation.yml.example` to a live `foundation.yml` pinned to the promoted SHA.
* Fix all 9 `nabhold/` references.
* Add a CI check that the template's pin equals the latest promoted tag.

**Done when:** all 15 consumers show a green `Foundation / Result` on `main` at the promoted SHA, and none has a `nabhold/shared` reference or a `.nabhold/` directory.

### Phase 6: enforcement

* Add an organisation ruleset that requires the **single combined result** `foundation / Foundation / Result` (D3), emitted by the compatibility entrypoint with `profile: full` on `pull_request` and `push`. Do not require any product-wrapper check or any check that only runs on a schedule.
* Remove the legacy metadata bridge (`legacy_metadata_enabled`, Gate 11) in the next minor version after Phase 5 completes.
* Replace the per-repository weekly `full` schedule with `foundation-product-security.yml` in `mode: deep`. Its failures go to triage and never block merges.

### Phase 7: drift guard (prevents a repeat of this audit)

Add a scheduled `shared` workflow, `foundation-org-conformance.yml`. It reads every organisation repository's workflows through the API and reports:

* any `nabhold/` or other non-`baobab-platform/shared` reference;
* pins that are not at the latest promoted tag, or older than N minor versions;
* missing `foundation_ref`, or `foundation_ref` different from the `uses:` SHA;
* missing caller permissions;
* private repositories with `dependency_review_enabled: true` and no GHAS or exception;
* a missing `.baobab/repository.yaml`.

It writes the report as a job summary and an artifact, and fails on High findings. This replaces the manual sweep done for this report.

## 6. Decisions

Recorded 2026-09-23.

| # | Decision | Outcome |
|---|---|---|
| D1 | Organisation vs legal entity | `baobab-platform` is the GitHub organisation, replacing `nabhold`. The legal-entity id in `contracts/legal-entity/registry.yaml` stays `NABHOLD`, as restored by `f39afe5`, and the validator follows it. |
| D2 | GitHub plan / GHAS | `baobab-platform` subscribes to **GitHub Team**. No Code Security add-on is assumed, so private repositories use SAST fallback and dependency review stays off with a reviewed exception. |
| D3 | Branch protection | Require **only the single combined result**, `foundation / Foundation / Result`. |
| D4 | Re-promotion version | **`v2.1.0`**. |
| D5 | Runner label | All workflows run on **`ubuntu-26.04`**. A fixture enforces this. |

## 7. How this was verified

* Shallow clones of all 16 repositories (default branch plus `chore/foundation-ci-v2`). References resolved against the full history of `shared`.
* Workflow run and job metadata from the GitHub API for `shared`, `baobab-iam`, `baobab-dev` and `nabhold`. Runs of `shared` CI and Foundation Static Validation compared from 2026-08-25 onwards.
* Local fixtures: `test_caller_template.py`, `test_workflow_wiring.py` and `test_policy.rb` pass. `test_contracts.py` passes once `jsonschema` is installed. All `scripts/validate-*.rb` pass except `validate-governance-contracts.rb`, which fails on `f39afe5` and passes with the `80d7f25` registry.
* This branch: `scripts/test-foundation.sh` passes in a clean virtualenv built from `requirements.txt`. All seven `scripts/validate-*.rb` pass. A `runs-on: ubuntu-24.04` injected into a workflow makes the runner-label fixture fail.
* Not verified: the exact reason for the organisation-level Actions block. The API returns no annotation and 404 for logs, so it needs an organisation admin (Phase 0).
