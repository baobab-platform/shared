# DEV10-R2/R3 — hosted Codespaces user evidence and consumer gate

**Status:** source harness in PR, real Codespace not yet observed.
**Authority:** EA v2.3 / EA-DEV DEV-10, Shared development environment
contract, ADR-SHARED-043 and baobab-dev merged #48/#50.

## Reference inspection (2026-11-02)

| Repo | Image / profile | Private package scope | Found issue |
|---|---|---|---|
| Nabhold | pinned 1.4.4-frontend digest | Shared BXS packages | waits updateContent while postCreate authenticates |
| ZuriBeans | pinned 1.4.4-frontend digest | Shared BXS packages | same; Playwright 1.63.0 |
| Thamani | pinned 1.4.4-frontend digest | 6 Shared BXS packages | same; Playwright 1.62.1 |
| CP | pinned 1.4.4 full digest + Go1.27 Docker feature | console BXS packages | same; native Go proof separate |

All four configure user-level npmrc with only literal env-token references,
closed exact package-version lookup and frozen pnpm lock. GHCR Codespaces
permission is a **pre-container package permission**, whereas user-level npm
access is checked **after** create. A successful Actions GITHUB_TOKEN GHCR
inspection proves neither user-side gate. Any permission denials must
fail, never fall back to the public registry.

## Owner side — REAL hosted Codespace execution

The current GitHub connector can read/write repo/PR/CI metadata but cannot
create/run/delete Codespaces. No Actions workflow may be called a real user
Codespace check. A designated operator with actual Codespaces authority must:

1. Grant the target repository **Manage Codespaces access** to the exact
   private baobab-dev GHCR image and to every required Shared npm package.
   Grant cross-repo read-only access to Shared and baobab-dev; use the
   appropriate dedicated `BAOBAB_PACKAGES_READ_TOKEN` Codespaces secret or
   explicitly authorized GITHUB_TOKEN. Do **not** print token values.
2. Create a **new disposable hosted Codespace from an exact reviewed branch**,
   with private ports. Its Dev Container must `waitFor: postCreateCommand`.
   Document the actual creation ID/time privately and verify exact source,
   image digest pulled by Codespaces, non-root vscode and no token leakage.
3. Run the hosted workspace's real postCreate completion. From the fresh
   Codespace, fetch and pin the Shared harness at the reviewed Shared commit,
   and run (example; replace root/receipt directory with run-owned paths):

   ```sh
   node /workspaces/shared/scripts/dev10/codespace-readback.mjs \
     zuribeans /workspaces/zuribeans /tmp/dev10-r2-zuribeans
   ```

   This checks actual user npm reads of each declared external BXS package,
   frozen install, exact project/tool version, project image declaration and
   development contract. It **never claims image-runtime digest attestation**:
   the GHCR pull occurs before it runs.
4. Transfer only sanitized receipt and SHA256, plus independently obtained
   Codespaces creation/actual image digest and verified operator/teardown
   records, to the controlled evidence store. An output checksum is not a
   cryptographic signer identity.
5. Delete the run-owned Codespace, confirm absence independently; revoke any
   run-owned secret. Run again with a deliberately denied private-package
   permission and verify fail-closed status (no public fallback, no credentials
   in stderr/evidence). Neither a prebuild nor an Actions job can stand in.

## R3 owner compatibility obligations

- Nabhold/ZuriBeans/Thamani: Node26, pnpm12, all 6 BXS packages,
  frozen lock, Next16 server/build, unit/typecheck, Playwright **1.64.1**
  binary+test alignment, accessible/visual/Lighthouse performance budgets.
  Snapshot baselines must be deliberately reviewed, not auto-replaced.
- CP: Go1.27 toolchain, owner PostgreSQL/CP/IAM tests and console private
  package tests. No IAM/CP authority by virtue of image pull.
- Trade: Medusa Node26 acceptance, DB17/Redis, buyer commitment negative
  cases. Never broaden `>=24 <25` without evidence.
- ERP / Subscriptions: JDK21 Maven native builds and PG17. Do not reuse a
  PostgreSQL16 physical volume under a PostgreSQL17 image.
- Payments: exact stable Rust feature and Cargo.lock native tests; PG16
  development database migration is independently owned.
- Pulse: Python3.14.10, uv locked install and native owner suites.
- TMS: first-party Node24/26 tests and independent HYB MySQL/PG17 native
  provider qualification; TMS PR29 is separate.

R4's candidate image is **not** published/protected until both AMD64/ARM64,
strict CVE scans, signing/provenance, these owner gates and rollback pass.
The existing linux-libc-dev risk acceptance must not be mistaken for VEX
or protected release permission.
