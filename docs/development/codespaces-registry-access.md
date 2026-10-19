# Baobab Shared Contracts: secure Codespaces environment
Use the v1.4.4 [baobab-dev published image](https://github.com/baobab-platform/baobab-dev/releases/tag/v1.4.4),
pinned to the full multi-language image digest `sha256:9603f0e7402aa85771e904db1c20f2ecc02f705131b266cb4ec3d1c24ea58ae4`. Before creating
the Codespace, an organisation package owner must add `baobab-platform/shared` to the
**Manage Codespaces access** permission on the GHCR **baobab-dev** package
(or verify inherited access). **Manage Actions access** is separate and
required for this repository's workflow to authenticate GHCR.
Shared is the canonical local publisher. Internal `workspace:^`
dependencies must resolve from local `packages/*`; no fake registry reads
should replace local packages. Publisher release credentials must never be
injected into interactive Codespaces, and no publication occurs on startup.
The prebuild performs only credential-free offline tests. After the editor
opens, post-create sets only a *literal* user npmrc token reference, verifies
external exact private npm releases when present, then installs the frozen
pnpm lockfile. Credentials: use repository-approved GITHUB_TOKEN or a
restricted Codespaces secret named BAOBAB_PACKAGES_READ_TOKEN with
read:packages and required organisation SSO authorisation.
Never write the raw token to the repository npmrc, .env or image.

After creating a **new** Codespace (approval of requested read-only
cross-repository permissions is required):
```bash
node scripts/codespaces/bootstrap.mjs
baobab-verify --contract
pnpm lint
```
A successful Actions GHCR digest inspection does not establish Codespaces
image/package access. Never make packages public, enable TLS bypass, or
weaken pinned lockfile/version checks to make the image load.
