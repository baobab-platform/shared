<!-- Target path: baobab-platform/shared/templates/README.md -->

<!-- FIX 2026-09-22: Phase 1 consumer readiness — caller-foundation-repository-gates.yml
was not executable as published (missing required foundation_ref input and
insufficient permissions). Template now supplies foundation_ref, full minimum
permissions, and explicit advanced_security_enabled / legacy_metadata_enabled.
A validation fixture lives at .github/foundation-tests/test_caller_template.py.
Tag table updated: latest tag remains v1.4.0; the audited main revision that
includes the corrected Foundation topology is not yet promoted — pin the SHA
from the uses: line after promotion, not a stale tag that predates the fix. -->

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
  Foundation baseline (capability classification, reproducibility, runtime,
  environment, security, container policy — see `docs/governance/foundation-ci-v2.md`).
  Recommended for every repo that participates in the Foundation contract.
  **The template is executable as published:** it supplies the required
  `foundation_ref` input, the minimum permissions (`contents`, `packages`,
  `actions`, `security-events`), and explicit defaults for
  `advanced_security_enabled` and `legacy_metadata_enabled`. Private
  repositories without GitHub Advanced Security must keep
  `advanced_security_enabled: false`.

Steps:

1. Copy the relevant `caller-*.yml` into `<repo>/.github/workflows/<name>.yml`.
2. Resolve every `TODO` / `REPLACE_*` placeholder.
3. Pin the `baobab-platform/shared/...@<sha>` reference to a full-length commit
   SHA — this is required by org policy, not optional, and applies to
   `baobab-platform/shared` references exactly as it does to third-party actions
   (see README.md's "Immutable Dependencies" section). Verify the SHA
   live against the upstream tag/branch rather than trusting what's
   already in the template, since it may be stale by the time you copy
   it. **As of 2026-09-22, `baobab-platform/shared` has tagged releases through
   `v1.4.0`.** The Foundation topology that includes the corrected caller
   contract is on `main` and is not yet published under a new tag; after the
   consumer-readiness promotion lands, pin to that new tag's peeled SHA.
   Until then:
   - Prefer the full-length SHA of the commit that contains the workflow you
     need (confirm with `git cat-file -e <sha>:.github/workflows/<file>`).
   - Historical coverage:
     - `v1.0.0` covers `greetings.yml`, `pages-zensical.yml`,
       `enforce-action-pinning.yml`, `enforce-dependabot-config.yml`.
     - `v1.1.0` covers everything `v1.0.0` covers, plus `release.yml`,
       `security-secrets-scan.yml`, `security-codeql.yml`,
       `security-python.yml`.
     - `v1.2.0` and later cover `foundation-repository-gates.yml` at the
       revisions present when those tags were cut. Re-verify before pinning
       that the tag includes the inputs and permissions you expect.

   Don't trust a tag name alone — a template pinned to a real, resolvable
   tag can still be wrong if that tag predates the file (confirm with
   `git ls-tree <tag> -- .github/workflows/<file>`, not just that the tag
   resolves).
4. Confirm the consuming repo's Settings → Actions → General → Actions
   permissions allows `baobab-platform/shared` (only relevant if that repo has an
   explicit allow-list rather than "Allow all actions").
5. For Foundation specifically: set `advanced_security_enabled: true` only
   when GHAS is enabled for the repository. Leave `legacy_metadata_enabled`
   true only while migrating from `.nabhold/environment.yaml`; new adopters
   with `.baobab/repository.yaml` should set it false.

`dependabot.yml` follows a different, simpler process: copy it into
`<repo>/.github/dependabot.yml`, resolve its TODOs, and that's it — there's
no `uses:` reference to pin, since (as above) Dependabot config isn't
delegated the way workflows are. Its drift-check counterpart,
`caller-enforce-dependabot-config.yml`, does still get steps 1–4 above,
since it *is* a normal reusable-workflow caller.
