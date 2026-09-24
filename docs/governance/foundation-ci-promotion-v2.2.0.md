# Foundation CI v2.2.0 promotion record

**Status:** Candidate — requirements 1 to 4 are green. **Ready to tag**; the tag is not yet cut.
**Candidate revision:** `ddd2c56f52b60472f0af1fd2e896e9cdd14bb636` (`shared` `main`, merge of #75)
**Proposed tag:** `v2.2.0`
**Previous release:** `v2.1.0` (`53ed9cd`, see `foundation-ci-promotion-v2.1.0.md`)
**Date opened:** 2026-09-24
**Policy reference:** `docs/governance/foundation-ci-support-policy.md`

The tag must point at the candidate revision itself, because that is the SHA the pilots run against. This record lands after the candidate and is not part of the release.

## What changed since `v2.1.0` (consumer-facing)

| Item | Detail |
|------|--------|
| Environment floor | Every `baobab-dev` profile (`full`, `frontend`, `frontend-e2e`, `infra`) now requires **1.4.4** or newer, up from 1.2.6 (and 1.4.0-rc.0 for `infra`) (#75). |

**Breaking for callers on older images.** A caller that declares `baobab-dev` below 1.4.4 fails the environment gate with `profile <name> requires baobab-dev >= 1.4.4` once it pins this revision. To upgrade, bump `.baobab/environment.yaml`, the devcontainer and any CI job images to 1.4.4 in the same change as the repin. No workflow inputs changed.

## Promotion requirements (support policy)

| # | Requirement | Status |
|---|-------------|--------|
| 1 | Workflow and contract static validation in `shared` | **Green** — Foundation Static Validation ([run 35945105902](https://github.com/baobab-platform/shared/actions/runs/35945105902)), push to `main` on `ddd2c56`. The path-filtered `CI` workflow did not trigger on `main` for this change; it passed on the #75 pull request. |
| 2 | `shared` self-consumer Foundation run | **Green** — Foundation Repository Gates ([run 35945106588](https://github.com/baobab-platform/shared/actions/runs/35945106588)), push to `main` on `ddd2c56`. `shared` itself declares `1.4.4-frontend`. |
| 3 | One representative consumer per activated runtime or artifact class | **Green** — all 12 pilots pass `foundation / Foundation / Result` on the candidate (table below). |
| 4 | Exact emitted result check name | **Verified:** `foundation / Foundation / Result` (caller job id `foundation`), unchanged from `v2.1.0`. |
| 5 | Consumer references pinned to the promoted commit SHA | **Pending the tag** — each pilot PR below pins `ddd2c56` and moves to 1.4.4; they merge after the tag. |

## Pilot cohort (requirement 3)

Each pilot PR (branch `ci/foundation-v2.2.0-candidate`) moves the repository to `baobab-dev` 1.4.4 and pins the candidate.

| Class | Repository | Pinned via | Result on candidate |
|---|---|---|---|
| Python, container artifact (`container_ignore_unfixed: true`) | baobab-dev | [#41](https://github.com/baobab-platform/baobab-dev/pull/41) | **Green** — [run 35945192855](https://github.com/baobab-platform/baobab-dev/actions/runs/35945192855) |
| Node / Next.js digital estate | zuribeans | [#87](https://github.com/baobab-platform/zuribeans/pull/87) | **Green** — [run 35945164523](https://github.com/baobab-platform/zuribeans/actions/runs/35945164523) |
| Node / Next.js digital estate | nabhold | [#25](https://github.com/baobab-platform/nabhold/pull/25) | **Green** — [run 35945170168](https://github.com/baobab-platform/nabhold/actions/runs/35945170168) |
| Go engine | baobab-cp | [#142](https://github.com/baobab-platform/baobab-cp/pull/142) | **Green** — [run 35945184952](https://github.com/baobab-platform/baobab-cp/actions/runs/35945184952) |
| Node CMS engine, container artifact | baobab-cms | [#15](https://github.com/baobab-platform/baobab-cms/pull/15) | **Green** — [run 35945199318](https://github.com/baobab-platform/baobab-cms/actions/runs/35945199318) |
| Java / Maven + Python, container artifact | baobab-erp | [#38](https://github.com/baobab-platform/baobab-erp/pull/38) | **Green** — [run 35945206061](https://github.com/baobab-platform/baobab-erp/actions/runs/35945206061) |
| Java / Keycloak, container artifact | baobab-iam | [#38](https://github.com/baobab-platform/baobab-iam/pull/38) | **Green** — [run 35945212528](https://github.com/baobab-platform/baobab-iam/actions/runs/35945212528) |
| Engine contract only (no runtime yet) | baobab-payments | [#6](https://github.com/baobab-platform/baobab-payments/pull/6) | **Green** — [run 35945218982](https://github.com/baobab-platform/baobab-payments/actions/runs/35945218982) |
| Python engine, container artifact | baobab-pulse | [#18](https://github.com/baobab-platform/baobab-pulse/pull/18) | **Green** — [run 35945225335](https://github.com/baobab-platform/baobab-pulse/actions/runs/35945225335) |
| Engine contract only (no runtime yet) | baobab-subscriptions | [#6](https://github.com/baobab-platform/baobab-subscriptions/pull/6) | **Green** — [run 35945230833](https://github.com/baobab-platform/baobab-subscriptions/actions/runs/35945230833) |
| Node commerce engine, container artifact | baobab-trade | [#102](https://github.com/baobab-platform/baobab-trade/pull/102) | **Green** — [run 35945239547](https://github.com/baobab-platform/baobab-trade/actions/runs/35945239547) |
| Terraform (`infra` profile) | infrastructure | [#9](https://github.com/baobab-platform/infrastructure/pull/9) | **Green** — [run 35945175079](https://github.com/baobab-platform/infrastructure/actions/runs/35945175079) |

`engine-template`, `thamani` and `equator-estate` are outside the current rollout and still pin earlier Foundation revisions. They must move to 1.4.4 when they repin to `v2.2.0` or later.

## Cutting the tag (operator checklist)

```bash
git fetch origin
git tag -a v2.2.0 ddd2c56f52b60472f0af1fd2e896e9cdd14bb636 -m "Foundation CI v2.2.0"
git push origin v2.2.0
git rev-list -n1 'v2.2.0^{}'   # must print ddd2c56f52b60472f0af1fd2e896e9cdd14bb636
```

Then:

1. Set **Status** to `Promoted` and record the peeled SHA.
2. Merge the pilot PRs (requirement 5).
3. Point the support policy and the caller template at `v2.2.0`.

## Emitted check context

```text
foundation / Foundation / Result
```
