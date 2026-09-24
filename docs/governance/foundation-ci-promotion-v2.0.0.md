# Foundation CI v2.0.0 promotion record

**Status:** Candidate — **tag not yet cut** (self-consumer CI red; investigating runner/log infrastructure).  
**Candidate revision (content):** `5fc8633d0357a36deb4a2fdc3e720c88960074d2` (includes Phase 1–3 docs on `main`).  
**Phase 1+2 functional baseline:** `1f39f6871a0f832127c0a44e3111807320f29b46`  
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
| 1 | Workflow and contract static validation in `shared` | **Blocked** — jobs on `ubuntu-26.04` fail in ~4s; API log download returns HTTP 404 (matches GitHub Actions log BlobNotFound pattern). Mitigation branch switches Foundation static validation to `ubuntu-24.04`. |
| 2 | `shared` self-consumer Foundation run | **Blocked** — same pattern: classify fails immediately; no recoverable logs. |
| 3 | Representative private consumers | **Pending** greens on (1)(2) |
| 4 | Exact emitted result check name | **Recorded:** `foundation / Foundation / Result` |
| 5 | Consumer pins to promoted SHA | **Pending** tag cut |

## Finish Phase 3 (operator checklist)

When Foundation Static Validation + Foundation Repository Gates are **green** on `main`:

```bash
git fetch origin && git checkout main && git pull
SHA=$(git rev-parse HEAD)
git tag -a v2.0.0 -m "Foundation CI v2.0.0 — consumer readiness"
git push origin v2.0.0
echo "Consumers pin: $(git rev-list -n1 v2.0.0^{})"
```

Then:

1. Set this document **Status** to `Promoted` and record the peeled SHA.
2. Pilot `baobab-platform/zuribeans` and `baobab-platform/baobab-dev` with that SHA.
3. Move CHANGELOG Foundation entries under `# [2.0.0] - YYYY-MM-DD`.

## Emitted check context

```text
foundation / Foundation / Result
```

## Related PRs

- Phase 1: #64 — executable caller template
- Phase 2: #65 — visibility-aware SAST
- Phase 3 record: #66 — promotion gating docs
- Runner mitigation: fix/foundation-runner-ubuntu-24.04
