# Foundation CI v2.3.0 promotion record

**Status:** **Promoted** — tag `v2.3.0` peels to `31de2bc3dcd56128c019c640dc7e12c10ae9ca69` (verified with `git rev-list -n1 'v2.3.0^{}'`).
**Candidate revision:** `31de2bc3dcd56128c019c640dc7e12c10ae9ca69` (`shared` `main`, merge of #77)
**Previous release:** `v2.2.0` (`ddd2c56`, see `foundation-ci-promotion-v2.2.0.md`)
**Date:** 2026-09-24
**Policy reference:** `docs/governance/foundation-ci-support-policy.md`

**Order of promotion.** The tag was pushed at about 05:48 UTC, while the pilot cohort was still running, rather than after it as the support policy requires. It points at the correct candidate, and every requirement below was subsequently met on that exact revision, so the tag stands; it is not moved or re-cut. Future tags must wait for the pilot record.

## What changed since `v2.2.0` (consumer-facing)

| Item | Detail |
|------|--------|
| Security scopes (M2) | The security family runs at `pr` scope on pull requests (secrets over the PR's own commits, dependency review applicable), `branch` scope on other events (the ref's full history) and `deep` scope under `security-deep` (every fetched ref, dependency review off). Results: `Security / PR`, `Security / Branch`, `Security / Deep`. |
| SAST provider (H2) | `.baobab/repository.yaml` declares `security.sast_provider: codeql \| fallback \| disabled`. CodeQL on a private repository needs an approved `security.ghas`; `disabled` needs an approved `exceptions.sast`. Without CodeQL the check is `SAST / Fallback`. |
| Removed | `legacy_metadata_enabled` and the `.nabhold/environment.yaml` bridge. |
| Deprecated | `advanced_security_enabled`: selects CodeQL only when nothing is declared, and never on a private repository without `security.ghas`. |
| Drift guard | `foundation-org-conformance.yml` evaluates the organisation weekly (not a consumer-facing input). |

**Breaking for callers.** A caller that passes `legacy_metadata_enabled` fails workflow validation once it pins this revision. To upgrade: repin, drop `legacy_metadata_enabled` and `advanced_security_enabled`, and declare `security.sast_provider` with the outcome the old input produced (`codeql` for `true`, `fallback` for `false`).

## Promotion requirements (support policy)

| # | Requirement | Status |
|---|-------------|--------|
| 1 | Workflow and contract static validation in `shared` | **Green** — Foundation Static Validation ([run 35961360210](https://github.com/baobab-platform/shared/actions/runs/35961360210)) and CI ([run 35961360379](https://github.com/baobab-platform/shared/actions/runs/35961360379)), push to `main` on `31de2bc`. |
| 2 | `shared` self-consumer Foundation run | **Green** — Foundation Repository Gates ([run 35961360782](https://github.com/baobab-platform/shared/actions/runs/35961360782)), push to `main` on `31de2bc`, with `shared` declaring `sast_provider: fallback`. |
| 3 | One representative consumer per activated runtime or artifact class | **Green** — all 12 pilots pass `foundation / Foundation / Result` on the candidate (table below). |
| 4 | Exact emitted result check name | **Verified:** `foundation / Foundation / Result`, unchanged. New non-required checks: `Security / PR`, `SAST / Fallback` (observed on #77). |
| 5 | Consumer references pinned to the promoted commit SHA | **In progress** — each pilot PR below pins `31de2bc`; they merge after this record. |

## Pilot cohort (requirement 3)

Each pilot PR (branch `ci/foundation-v2.3.0-candidate`) pins the candidate, drops the removed and deprecated inputs, and declares `security.sast_provider`.

| Class | Repository | Pinned via | Result on candidate |
|---|---|---|---|
| Python, container artifact (`container_ignore_unfixed: true`) | baobab-dev | [#42](https://github.com/baobab-platform/baobab-dev/pull/42) | **Green** — [run 35961511445](https://github.com/baobab-platform/baobab-dev/actions/runs/35961511445) |
| Node / Next.js digital estate, `sast_provider: codeql` | zuribeans | [#88](https://github.com/baobab-platform/zuribeans/pull/88) | **Green** — [run 35961460659](https://github.com/baobab-platform/zuribeans/actions/runs/35961460659) |
| Node / Next.js digital estate | nabhold | [#26](https://github.com/baobab-platform/nabhold/pull/26) | **Green** — [run 35961467083](https://github.com/baobab-platform/nabhold/actions/runs/35961467083) |
| Go engine, `sast_provider: codeql` | baobab-cp | [#143](https://github.com/baobab-platform/baobab-cp/pull/143) | **Green** — [run 35961484729](https://github.com/baobab-platform/baobab-cp/actions/runs/35961484729) |
| Node CMS engine, container artifact | baobab-cms | [#16](https://github.com/baobab-platform/baobab-cms/pull/16) | **Green** — [run 35961517446](https://github.com/baobab-platform/baobab-cms/actions/runs/35961517446) |
| Java / Maven + Python, container artifact | baobab-erp | [#39](https://github.com/baobab-platform/baobab-erp/pull/39) | **Green** — [run 35961525126](https://github.com/baobab-platform/baobab-erp/actions/runs/35961525126) |
| Java / Keycloak, container artifact | baobab-iam | [#39](https://github.com/baobab-platform/baobab-iam/pull/39) | **Green** — [run 35961492619](https://github.com/baobab-platform/baobab-iam/actions/runs/35961492619) |
| Engine contract only (no runtime yet) | baobab-payments | [#7](https://github.com/baobab-platform/baobab-payments/pull/7) | **Green** — [run 35961533236](https://github.com/baobab-platform/baobab-payments/actions/runs/35961533236) |
| Python engine, container artifact | baobab-pulse | [#19](https://github.com/baobab-platform/baobab-pulse/pull/19) | **Green** — [run 35961536839](https://github.com/baobab-platform/baobab-pulse/actions/runs/35961536839) |
| Engine contract only (no runtime yet) | baobab-subscriptions | [#7](https://github.com/baobab-platform/baobab-subscriptions/pull/7) | **Green** — [run 35961543590](https://github.com/baobab-platform/baobab-subscriptions/actions/runs/35961543590) |
| Node commerce engine, container artifact | baobab-trade | [#103](https://github.com/baobab-platform/baobab-trade/pull/103) | **Green** — [run 35961550662](https://github.com/baobab-platform/baobab-trade/actions/runs/35961550662) |
| Terraform (`infra` profile) | infrastructure | [#10](https://github.com/baobab-platform/infrastructure/pull/10) | **Green** — [run 35961471134](https://github.com/baobab-platform/infrastructure/actions/runs/35961471134) |

`engine-template`, `thamani` and `equator-estate` remain deferred (see `.baobab/org-conformance.yaml`).

## Emitted check context

```text
foundation / Foundation / Result
```
