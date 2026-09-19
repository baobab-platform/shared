<!-- Target path: baobab-platform/shared/templates/README.md -->

<!-- FIX 2026-09-05: v1.2.0 was cut 2026-09-04 (commit 38defb1) and covers
foundation-repository-gates.yml, closing the gap the 2026-09-04 fix note
below flagged as still-untagged. Updated step 3's pin table and the
caller-foundation-repository-gates.yml description accordingly — verified
live via `git ls-tree v1.2.0 -- .github/workflows/foundation-repository-gates.yml`
and `git rev-list -n1 v1.2.0^{}` against the real repo on 2026-09-05.

FIX 2026-09-04: two corrections to the checked-in version of this
file, both verified live against the real repo on 2026-09-04:
1. Added the caller-foundation-repository-gates.yml entry to the list
   below — it exists in templates/ but was never described here.
2. Replaced the "one tagged release, v1.0.0" claim and its per-file pin
   table in step 3, which was stale: v1.1.0 was cut 2026-08-25 (same day
   as v1.0.0) and already covers release.yml and the three security-*.yml
   workflows. Only caller-foundation-repository-gates.yml is still
   untagged (its underlying workflow, foundation-repository-gates.yml,
   landed on main after v1.1.0 and has no covering tag yet as of
   2026-09-04) — see this project's sharables audit, §7 item 2, for the
   recommendation to cut a v1.2.0 covering it. -->

# Caller Templates

Most files here are thin wrappers for a consuming repository's own
`.github/workflows/`. Reusable workflows can only carry a `workflow_call`
trigger — the real trigger (`push`, `pull_request`, `issues`, ...) and any
job-level `permissions:` elevation always live in the caller repo, not in
`baobab-platform/shared`. The one exception is `dependabot.yml`, which isn't a
workflow at all — see its own entry below for why it's copied differently.

- `caller-greetings.yml` — org-standard first-interaction bot. Toolchain-
  agnostic, works for any repo.
- `caller-pages-zensical.yml` — docs build/deploy. Assumes uv + Zensical
  (the BAOBAB-PLATFORM default). A repo on a different documentation toolchain
  needs a different reusable workflow, not a modified copy of this one —
  raise that as a new shared/ addition rather than forking this template.
- `caller-enforce-action-pinning.yml` — CI check that fails if any
  `uses:` reference in the consuming repo isn't pinned to a full-length
  commit SHA. Recommended for every repo, not just this one — see
  README.md's "Immutable Dependencies" policy.
- `dependabot.yml` — org-standard Dependabot config for tracking GitHub
  Actions dependencies. Unlike the other files here, this isn't a
  reusable-workflow caller — Dependabot config can't be centralized that
  way (see README.md's "Dependency Updates" section) — so it's copied
  verbatim rather than delegated via `uses:`.
- `caller-enforce-dependabot-config.yml` — CI check that fails if the
  consuming repo's `.github/dependabot.yml` has drifted from the org's
  structural requirements (missing ecosystem entry, missing schedule,
  etc.). Pairs with `dependabot.yml` above the way
  `caller-enforce-action-pinning.yml` pairs with the pinning policy —
  copy once, then let this catch drift afterwards.
- `caller-release.yml` — creates a GitHub Release from a pushed version
  tag, with release notes drawn from the caller's own CHANGELOG.md. Not
  a fit for a repository whose release is inseparable from a bespoke
  artifact pipeline (container build/sign/attest, package publish) — see
  release.yml's own header.
- `caller-security-secrets-scan.yml` — fails CI if gitleaks finds a
  secret anywhere in the calling repository's git history. Toolchain-
  agnostic, works for any repo — recommended for every repo, same as
  action-pinning.
- `caller-security-codeql.yml` — runs GitHub CodeQL SAST for whichever
  languages the caller declares. Only adopt this in a repo that has at
  least one CodeQL-supported language — see the template's own header.
- `caller-security-python.yml` — runs Bandit (SAST) and pip-audit
  (dependency vulnerability audit) for a uv-managed Python repo. Assumes
  the "security" dependency-group convention documented in
  baobab-platform/baobab's pyproject.toml.
- `caller-foundation-repository-gates.yml` — enforces this org's
  Foundation baseline (the `.baobab-platform/environment.yaml` / devcontainer
  profile checks — see `contracts/development-environment/schema.yaml`
  for what each profile requires). Recommended for every repo that uses
  `baobab-dev`. Its underlying workflow is covered as of `v1.2.0` — see
  step 3 below.

Steps:

1. Copy the relevant `caller-*.yml` into `<repo>/.github/workflows/<name>.yml`.
2. Resolve every `TODO`.
3. Pin the `baobab-platform/shared/...@<sha>` reference to a full-length commit
   SHA — this is required by org policy, not optional, and applies to
   `baobab-platform/shared` references exactly as it does to third-party actions
   (see README.md's "Immutable Dependencies" section). Verify the SHA
   live against the upstream tag/branch rather than trusting what's
   already in the template, since it may be stale by the time you copy
   it. **As of 2026-09-05, `baobab-platform/shared` has three tagged releases:**
   `v1.0.0` (2026-08-25), `v1.1.0` (2026-08-25, same day — a security
   fix that added `release.yml` and the three `security-*.yml`
   workflows), and `v1.2.0` (2026-09-04, commit `38defb1`, which adds
   `foundation-repository-gates.yml`). Pin to the earliest tag that
   actually contains the file you're copying:
   - `v1.0.0` covers `greetings.yml`, `pages-zensical.yml`,
     `enforce-action-pinning.yml`, `enforce-dependabot-config.yml`.
   - `v1.1.0` covers everything `v1.0.0` covers, plus `release.yml`,
     `security-secrets-scan.yml`, `security-codeql.yml`,
     `security-python.yml`.
   - `v1.2.0` covers everything `v1.1.0` covers, plus
     `foundation-repository-gates.yml` (used by
     `caller-foundation-repository-gates.yml`).

   Don't trust a tag name alone — a template pinned to a real, resolvable
   tag can still be wrong if that tag predates the file (confirm with
   `git ls-tree <tag> -- .github/workflows/<file>`, not just that the tag
   resolves).
4. Confirm the consuming repo's Settings → Actions → General → Actions
   permissions allows `baobab-platform/shared` (only relevant if that repo has an
   explicit allow-list rather than "Allow all actions").

`dependabot.yml` follows a different, simpler process: copy it into
`<repo>/.github/dependabot.yml`, resolve its TODOs, and that's it — there's
no `uses:` reference to pin, since (as above) Dependabot config isn't
delegated the way workflows are. Its drift-check counterpart,
`caller-enforce-dependabot-config.yml`, does still get steps 1–4 above,
since it *is* a normal reusable-workflow caller.