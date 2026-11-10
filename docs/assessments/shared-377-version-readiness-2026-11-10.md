# Shared #377 — source-version PR audit and release separation

**Audit:** 10 November 2026. **Scope:** version metadata, changelog provenance, package compatibility and GitHub workflow trigger boundaries. This is a source-version review; **no staging, stable package publication, provider activation or estate deployment is claimed**.

## Exact delta

| Package | Before Shared main | Proposed | Changeset |
| --- | --- | --- | --- |
| `@baobab-platform/experience-ui` | `0.3.1` | `0.3.2` | `.changeset/bxs-adaptive-visual-fidelity.md` — CSS long-text, forced colours and danger-button semantics |
| `@baobab-platform/supplier-domain` | `0.2.1-staging.0` | `0.2.1` | `.changeset/fix-supplier-zod-memory.md` — raise minimum Zod to address GHSA-mrhx-c7xc-m3w5 |

The release PR modifies only the two package versions, two changelogs and deletes their two consumed changeset files; no domain source, IAM/CP permission, workspace lock, runtime endpoint, CI permission or package publish workflow is changed.

At the source baseline, `supplier-domain` already specifies `zod: ^4.6.7`; the locked dependency resolves to `4.6.7`. Its published version number therefore labels the **already-reviewed remediation**; the PR must not be described as independently patching Zod at publish time. The reviewed Shared main already includes the compatible TypeScript 7, Vitest 5, tsup 9 and grouped dependency updates, including real Storybook/Chromium checks. Do not rewrite those changes in this release PR.

## Safety and publication authority

- `.github/workflows/version-packages.yml` is triggered on eligible **main-branch** changes but invokes Changesets only to propose versions. Its documented rule is **no npm/OCI publish, tag or production release** from the versioning workflow.
- `.github/workflows/publish-shared.yml` is triggered by an independent repository release tag `v*.*.*` or by an expressly authorised workflow dispatch, and performs its own publish verification. Its package publication is not a side effect of merging this PR.
- `.github/workflows/staging-release.yml` handles the separate reviewed staging tag and prerelease rules; this PR does not create a staging receipt.
- `docs/governance/baobab-dependency-security-maintenance-policy-v1.0.md` keeps immutable source/lock evidence, final-head CI, security checks, recipient consumption and protected release approvals separate.
- No tag or workflow dispatch is authorised or initiated by this PR review. **Do not publish stable packages** without registry entitlement, staging/provenance and consumer evidence plus appropriate release approval.

## Evidence and acceptance

Source-version approval is separate from publication. The release PR must pass its final-head **Foundation, Experience, DEV-10/private-consumer and Codespaces registry** workflows, with any security jobs; completed CodeQL alone is insufficient. The earlier GitHub Actions bot head `b96aacffbf73304cc6a33e2c11ead447e2afcfc0` had three successful CodeQL checks, but four other pull-request workflows returned `action_required` without jobs. That is **NOT PASSED** and must be resolved before merge.

Review the new commit's own GitHub Actions executions, branch protection, negative/consumer outcomes and package manifests before promoting the *source version*. Even when source-verification succeeds, the actual publishing step is independently withheld until specifically approved and separately evidenced.
