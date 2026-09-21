# Foundation CI v2.0.0 promotion record

**Status:** Candidate — **tag not yet cut** (self-consumer CI red on `main`).  
**Candidate revision:** `1f39f6871a0f832127c0a44e3111807320f29b46` (merge of Phase 1 + Phase 2 on `main`).  
**Proposed tag:** `v2.0.0`  
**Date opened:** 2026-09-22  
**Policy reference:** `docs/governance/foundation-ci-support-policy.md`

## What this revision contains (consumer-facing)

| Item | Detail |
|------|--------|
| Executable caller template | `templates/caller-foundation-repository-gates.yml` supplies required `foundation_ref`, full permissions, explicit security/migration inputs |
| Visibility-aware SAST | CodeQL only when opted in; private without GHAS → **SAST / Not available** (no failed upload) |
| Dependency review | Public always available for PRs when enabled; private requires `advanced_security_enabled` |
| Aggregate check | Caller job id **`foundation`** → displayed context includes **`Foundation / Result`** |

## Promotion requirements (support policy)

| # | Requirement | Status |
|---|-------------|--------|
| 1 | Workflow and contract static validation in `shared` | **Blocked** — `Foundation Static Validation` / `CI` runs on `main` conclude `failure` (runs complete in seconds; job logs unavailable via API 404). Investigate runner / org Actions health before treating as content failure. |
| 2 | `shared` self-consumer Foundation run | **Blocked** — run [35669145507](https://github.com/baobab-platform/shared/actions/runs/35669145507): `foundation / classify / classify` failed; downstream gates skipped; `foundation / Foundation / Result` failed. |
| 3 | Representative private consumers per activated class | **Pending** — after (1)(2) green: pilot `baobab-platform/zuribeans` (Node/digital-estate), `baobab-platform/baobab-dev` (infra/docs). Expand matrix per support policy. |
| 4 | Exact emitted result check name verified | **Recorded from failed self-run naming** (structure is correct even when conclusion is failure): see below. Re-confirm on first green pilot. |
| 5 | Consumer references pinned to promoted SHA | **Pending** — after tag: update pilots; template keeps `REPLACE_WITH_FULL_SHARED_COMMIT_SHA` until pin is verified, then consumers paste the tagged SHA. |

## Emitted check context (from self-consumer job names)

Use a caller job id of **`foundation`**. Observed nested check names on the self-consumer:

- `foundation / classify / classify`
- `foundation / baseline`
- `foundation / reproducibility`
- `foundation / runtime`
- `foundation / environment`
- `foundation / security`
- `foundation / container`
- **`foundation / Foundation / Result`** ← require this in branch protection / rulesets

Rulesets must be configured from a **successful** pilot run’s emitted name, not only from this list.

## Pilot matrix (to execute when CI is green)

| Consumer | Class | Actions |
|----------|--------|---------|
| `baobab-platform/shared` | Self-consumer | Foundation green; record check names |
| `baobab-platform/zuribeans` | Node / digital-estate / private | Pin candidate or `v2.0.0` SHA; `advanced_security_enabled: false` unless GHAS on; confirm **SAST / Not available** not CodeQL upload failure |
| `baobab-platform/baobab-dev` | Docs / infra | Pin SHA; Foundation green |
| (optional) one Python service | Python | Pin SHA |
| (optional) one Go engine | Go | Pin SHA |

## Tag cut procedure (after greens)

```bash
# On main, after requirements 1–4 are green:
git fetch origin
git checkout main && git pull
CANDIDATE=$(git rev-parse HEAD)   # or the verified pilot SHA
git tag -a v2.0.0 -m "Foundation CI v2.0.0 — consumer readiness (executable template, visibility-aware SAST)"
git push origin v2.0.0
# Peel annotated tag for consumers:
git rev-list -n1 v2.0.0^{}
```

Consumers pin the **peeled commit SHA**, not the tag object SHA.

## Do not promote if

- `Foundation / Result` is red on `shared`
- Static validation or policy fixtures fail
- Private pilot still fails CodeQL upload with `advanced_security_enabled: false`
- Check context names change without a docs update

## Related PRs

- Phase 1: #64 — executable caller template
- Phase 2: #65 — visibility-aware SAST / CodeQL fallback
- Phase 3: this promotion record
