# Foundation: first-party private GitHub Packages consumers

**Decision alignment:** Accepted ADR-SHARED-040; Node.js 24, pnpm 11,
strong package provenance and repository-level authority boundaries.

## Problem and resolution

BXS v0.2.0 passed independent SHA512 publication verification, but consumer
Foundation and Security gates couldn't install private npm packages. pnpm 11
rejects committed project-level token interpolation. The reusable Foundation
container also invoked Docker without the required ephemeral BuildKit secret.

This increment makes **no policy exception**. Every enabled dependency
audit, runtime check, vulnerability scan, SBOM and OCI label verification
continues as before.

For repos explicitly declaring the Baobab GitHub Packages scope in
`.npmrc`, the Foundation Node dependency adapter configures a short-lived
**runner home** credential using only the workflow job's `github.token`;
permissions are scoped to `contents:read` and `packages:read`. The
credential is never committed. The container gate passes only the BuildKit
`npm_token` secret for that package scope, leaving all other Docker builds
unchanged. Build Dockerfiles MUST consume the secret through a temporary
mount (prefer tmpfs user configuration) and must not create a layer, ARG
or runtime ENV containing the token.

Forked PRs attempting to use the private package scope are denied in both
adapters and container builds. A same-repository actor must open the PR.

The publication and verification workflows remain separate. No Foundation
gate creates a privileged token, publishes packages, disables audit, or
provides downstream domain authorisation.

## Adoption steps

1. Merge and pass all Shared governance/quality workflows.
2. Select a stable immutable release SHA, update the affected estate's
   Foundation caller(s) to the *same* SHA, including the declared
   `foundation_ref`, while preserving required checks.
3. Verify actual private registry and container runtime under the new SHA.
4. Complete the normal consumer CI, browser axe, performance, visuals,
   Secrets and security scans; merge only on new-head green evidence.

**Not demonstrated by this source PR alone:** protected production acceptance,
published tagged Foundation promotion or any enterprise permission grant.
