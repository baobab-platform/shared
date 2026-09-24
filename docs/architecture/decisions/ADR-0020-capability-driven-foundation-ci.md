# ADR-0020: Capability-driven Foundation CI

- Status: Accepted
- Date: 2026-09-20

## Context

Baobab is a polyrepo, polyglot estate whose repositories have mixed visibility. The original Foundation workflow assumed a development container, handled only Node and Go lockfiles, and combined repository governance with broad security and image scanning. Static assumptions caused irrelevant work in some repositories and left other runtimes without first-class validation.

## Decision

Keep `.github/workflows/foundation-repository-gates.yml` as the stable entry point and move internal responsibilities into narrow reusable workflows. Resolve capabilities from `.baobab/repository.yaml` first and strong repository evidence second. Treat `.baobab/repository.yaml` as a governance declaration, not a deployment manifest.

Foundation exposes a stable `Foundation / Result` check. Application correctness remains in each repository's CI. Consumer workflows remain pinned to immutable `shared` commit SHAs.

Private repositories do not run GitHub features that their visibility or licence cannot support. They receive an explicit coverage notice and portable baseline scanners; CodeQL coverage is never implied when SARIF upload is unavailable.

A temporary legacy bridge accepts `.nabhold/environment.yaml` during controlled migration. It is not a permanent alias and must be removed after organisation rollout.

## Consequences

- New languages extend the classifier and one focused gate rather than redesigning the entry point.
- Irrelevant runtime jobs become not applicable instead of false failures.
- Repository declarations can be reviewed independently of application configuration.
- The private `shared` repository requires organisation Actions access to consumer repositories.
- Rollout must occur through new immutable pins and representative pilots.

