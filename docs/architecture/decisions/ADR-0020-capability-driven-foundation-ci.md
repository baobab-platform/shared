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

## Amendment 1 (2026-10-01): the `control-plane` repository trait

The `capabilities` vocabulary gains `control-plane`, a technical role distinct from `engine`.

- `engine`: implements one or more Baobab domain capabilities. An `active` engine must carry `.baobab/capability-provider.yaml` (ADR-SHARED-017, G-FCI-1).
- `control-plane`: owns platform governance, capability resolution and desired-state authority. It provides no resolvable capability, so it needs no provider declaration and may not carry one: capability resolution cannot itself be a capability resolved through the Control Plane.

The two traits are mutually exclusive. A `control-plane` repository still receives the contract-consumer-lock (EA-01C), runtime, container and security gates. Classification is by trait, never by repository name. A function extracted from the Control Plane may become a capability only if it passes the ADR-SHARED-017 capability test without circular dependence on resolution, and then belongs to an engine.
