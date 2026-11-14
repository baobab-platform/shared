# DEV-10 / DEV-14 — CP #460 toolchain and v1.5.1 consumer reconciliation (14 November 2026)

**Authority:** EA v2.3, EA-DEV DEV-10/14, BA-SEC-DEP-001. **Evidence class:** source reconciliation and GitHub workflow observation; **not** hosted Codespaces or protected acceptance.

## Observed source

- [CP #460](https://github.com/baobab-platform/baobab-cp/pull/460) candidate head `2017e97cc14825d422aab323a88a35a5e700a73e` now aligns Console Node **26.13.0**, pnpm **12.16.1**, Corepack **0.36.0**, and `@types/node 26.6.5` to its pinned workspace and Docker builder/runtime candidates.
- CP `.devcontainer/devcontainer.json` now selects the published `ghcr.io/baobab-platform/baobab-dev:1.5.1@sha256:faf9022ef06288767651a0ec1071d5199bc2b645f2cf7ada50477774dd297eed`, retains explicitly layered Go 1.27 and Node 26, private port defaults, and token-safe private package bootstrap.
- `.baobab/environment.yaml` minimum version is **1.5.1**; Codespaces regression now rejects the superseded 1.4.4 image; the image-registry workflow reads the actual configured image and checks its exact digest with GHCR access, rather than validating an unrelated hardcoded 1.4.4 image.
- Independent publisher evidence already registered: [v1.5.1 RC2](https://github.com/baobab-platform/baobab-dev/actions/runs/43493272371) and [v1.5.1 GA](https://github.com/baobab-platform/baobab-dev/actions/runs/43559737080). This register does not claim a newly executed standalone Cosign or OCI verification beyond the cited publication evidence.
- CP #480 independently proposed the same `1.5.1` Codespaces image, minimum version and source regression changes. **Do not merge duplicate file changes twice**; reconcile/close #480 only after #460 passes its final-head required checks and merges.

## Current checks and remaining holds

The earlier CP #460 head `d35d419` passed seven workflows including Console, Go, Security, Foundation and Codespaces. **Do not carry those results to updated head.** An earlier current-head CP policy workflow failed before creating jobs; follow-up source commit removes comments after the reusable `with:` mapping. Other CI was queued or running; no latest-head green claim is made.

- **DEV-10 remains PARTIAL / BLOCKED:** fresh user Codespace start, effective Node/Go bootstrap and private BXS npm read; failure-negative and teardown; pnpm 12 multi-document lockfile security-alert visibility; complete cross-owner consumer matrix; fleet rollback; separate DEV-12 physical PostgreSQL migration.
- **DEV-14 remains PARTIAL / BLOCKED:** recorded historical Pulse 20 PASS and Payments 18 PASS / 5 BLOCKED are unchanged; no new ENG-ONB runtime receipt, certification or provider authority arises from a tooling/image pin.
- Development-only `linux-libc-dev` bounded CVE acceptance expires **2026-11-26T00:00:00Z**. Do not convert its inventory/allowance into a remediated status or a production waiver.
- Do not conflate an Actions GHCR read-only token with actual logged-in Codespaces user entitlement. Never record source or CI source tests as external-provider certification.
- CP #460 and #480 must be resolved using up-to-date CI and independently reviewed final-head evidence. Their changes cannot authorize protected staging/production.

## Follow-up

Upon a qualified CP #460 merge, append its actual merge SHA and final-head workflow IDs and refresh DEV-10/14 register **source baseline only**, retaining blocked runtime cases and original receipt timestamps. Run real disposable Codespaces and per-engine native tests separately; document digest, source, identity, private-package read, refusals, cleanup and rollback.
