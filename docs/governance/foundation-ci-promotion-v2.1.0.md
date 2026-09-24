# Foundation CI v2.1.0 promotion record

**Status:** Candidate — requirements 1 to 4 are green. **Ready to tag**; the tag is not yet cut.
**Candidate revision:** `53ed9cdba8fc33e2f184d1ba29b990f71b74f85f` (`shared` `main`, merge of #73)
**Proposed tag:** `v2.1.0` (decision D4 in `foundation-ci-org-conformance-plan-2026-09-23.md`)
**Date opened:** 2026-09-24
**Policy reference:** `docs/governance/foundation-ci-support-policy.md`

The tag must point at the candidate revision itself, because that is the SHA the pilots run against. This record and later documentation-only commits land after the candidate and are not part of the release.

## Relationship to `v2.0.0`

`v2.0.0` (peeled `80d7f2556ba05d4a9524acd525152892a55316fa`) was tagged before the promotion criteria were met: static validation and the self-consumer were red on that revision (see `foundation-ci-promotion-v2.0.0.md`). It is **superseded** by `v2.1.0` and must not be moved or reused. No consumer pins it.

## What changed since `v2.0.0` (consumer-facing)

| Item | Detail |
|------|--------|
| Product separation | Optional `profile` input (`full` \| `contract` \| `security-pr` \| `security-deep` \| `container`) and the `foundation-product-*.yml` entrypoints (#68). |
| Container base-image policy | Recognises build stages and resolves global `ARG` defaults in `FROM` (#69, #70). |
| Environment gate | Runs in `ghcr.io/baobab-platform/baobab-dev:1.4.3` (#71). |
| Reproducibility gate | No longer crashes when `package.json` has no `packageManager` (#72). |
| Container gate | Opt-in `container_ignore_unfixed` input: findings with no fixed version are reported but do not fail the gate (#73). Default `false`. |

All input changes are additive, so a caller on `b1e2937` or `468f0e6` repins by changing the SHA in `uses:` and `foundation_ref` only.

## Promotion requirements (support policy)

| # | Requirement | Status |
|---|-------------|--------|
| 1 | Workflow and contract static validation in `shared` | **Green** — Foundation Static Validation ([run 35941045413](https://github.com/baobab-platform/shared/actions/runs/35941045413)) and CI ([run 35941045708](https://github.com/baobab-platform/shared/actions/runs/35941045708)), push to `main` on `53ed9cd`. |
| 2 | `shared` self-consumer Foundation run | **Green** — Foundation Repository Gates ([run 35941045992](https://github.com/baobab-platform/shared/actions/runs/35941045992)), push to `main` on `53ed9cd`. |
| 3 | One representative consumer per activated runtime or artifact class | **Green** — all 12 pilots pass `foundation / Foundation / Result` on the candidate (table below). |
| 4 | Exact emitted result check name | **Verified:** `foundation / Foundation / Result` (caller job id `foundation`), read from the pilot check runs. |
| 5 | Consumer references pinned to the promoted commit SHA | **In progress** — repin PRs below; merge after the pilot runs are green. |

## Pilot cohort (requirement 3)

Each consumer below runs Foundation at the candidate SHA through a one-line repin PR (branch `ci/foundation-v2.1.0-candidate`), except `baobab-dev`, whose `main` already pins the candidate.

| Class | Repository | Pinned via | Result on candidate |
|---|---|---|---|
| Python, container artifact (`container_ignore_unfixed: true`) | baobab-dev | `main` (baobab-dev#35) | **Green** — [run 35942099243](https://github.com/baobab-platform/baobab-dev/actions/runs/35942099243) |
| Node / Next.js digital estate | zuribeans | [#86](https://github.com/baobab-platform/zuribeans/pull/86) | **Green** — [run 35943000146](https://github.com/baobab-platform/zuribeans/actions/runs/35943000146) |
| Node / Next.js digital estate | nabhold | [#24](https://github.com/baobab-platform/nabhold/pull/24) | **Green** — [run 35943004867](https://github.com/baobab-platform/nabhold/actions/runs/35943004867) |
| Go engine | baobab-cp | [#141](https://github.com/baobab-platform/baobab-cp/pull/141) | **Green** — [run 35943019306](https://github.com/baobab-platform/baobab-cp/actions/runs/35943019306) |
| Node CMS engine, container artifact | baobab-cms | [#14](https://github.com/baobab-platform/baobab-cms/pull/14) | **Green** — [run 35943026527](https://github.com/baobab-platform/baobab-cms/actions/runs/35943026527) |
| Java / Maven + Python, container artifact | baobab-erp | [#37](https://github.com/baobab-platform/baobab-erp/pull/37) | **Green** — [run 35943032756](https://github.com/baobab-platform/baobab-erp/actions/runs/35943032756) |
| Java / Keycloak, container artifact | baobab-iam | [#37](https://github.com/baobab-platform/baobab-iam/pull/37) | **Green** — [run 35943040487](https://github.com/baobab-platform/baobab-iam/actions/runs/35943040487) |
| Engine contract only (no runtime yet) | baobab-payments | [#5](https://github.com/baobab-platform/baobab-payments/pull/5) | **Green** — [run 35943049299](https://github.com/baobab-platform/baobab-payments/actions/runs/35943049299) |
| Python engine, container artifact | baobab-pulse | [#17](https://github.com/baobab-platform/baobab-pulse/pull/17) | **Green** — [run 35943058434](https://github.com/baobab-platform/baobab-pulse/actions/runs/35943058434) |
| Engine contract only (no runtime yet) | baobab-subscriptions | [#5](https://github.com/baobab-platform/baobab-subscriptions/pull/5) | **Green** — [run 35943064134](https://github.com/baobab-platform/baobab-subscriptions/actions/runs/35943064134) |
| Node commerce engine, container artifact | baobab-trade | [#101](https://github.com/baobab-platform/baobab-trade/pull/101) | **Green** — [run 35943071121](https://github.com/baobab-platform/baobab-trade/actions/runs/35943071121) |
| Terraform | infrastructure | [#8](https://github.com/baobab-platform/infrastructure/pull/8) | **Green** — [run 35943009358](https://github.com/baobab-platform/infrastructure/actions/runs/35943009358) |

`equator-estate`, a pilot in the 2026-09-23 plan, is deferred: frontend digital estates other than zuribeans and nabhold are out of the current rollout priority. The digital-estate class is covered by zuribeans and nabhold, and the container class by baobab-dev, baobab-cms, baobab-erp, baobab-iam, baobab-pulse and baobab-trade.

## Cutting the tag (operator checklist)

When every pilot row above is green on the candidate:

```bash
git fetch origin
git tag -a v2.1.0 53ed9cdba8fc33e2f184d1ba29b990f71b74f85f -m "Foundation CI v2.1.0"
git push origin v2.1.0
git rev-list -n1 'v2.1.0^{}'   # must print 53ed9cdba8fc33e2f184d1ba29b990f71b74f85f
```

Then:

1. Set **Status** to `Promoted` and record the peeled SHA.
2. Merge the repin PRs (requirement 5).
3. Point the TODO in `templates/caller-foundation-repository-gates.yml` at `v2.1.0`.
4. Move the Foundation entries in `CHANGELOG.md` under `# [2.1.0] - YYYY-MM-DD`.

## Emitted check context

```text
foundation / Foundation / Result
```
