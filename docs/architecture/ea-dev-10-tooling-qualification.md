# DEV-10 tooling and contract qualification

Observed 2026-10-25. This is a scoped engineering increment of the accepted
EA-DEV plan, not completion of clean Codespaces or fleet upgrade acceptance.
DEV-06/INT-07 remains deferred until Subscriptions onboarding.

## Implemented source

The Foundation environment check now parses the effective Dev Container image,
selected Compose workspace or Dockerfile stage ancestry. A comment, README,
unused service/stage, image-prefix lookalike, duplicate field or escaping local
path cannot satisfy the declared image. Required capabilities must belong to
the selected profile, including frontend-e2e inheritance. The capability lists
are checked against the owner-pinned provider configuration, not guessed from
an image name. This read-only preflight prints SOURCE_ONLY and never runs Docker,
installs tools or grants provider authority. Unsupported Compose include/extends
forms fail explicitly rather than becoming an implicit pass.

Shared now pins Node **24.21.0** in `.node-version` and its bootstrap checks that
exact version before install; pnpm remains **11.24.0**. Editor readiness waits
for `postCreateCommand`, including dependency installation. Prebuild continues
to run source tests without user registry authentication. Existing npm user
configuration uses literal environment references and never writes token values.
A new Actions test installs the actual immutable private experience-tokens 0.3.1
archive from a frozen consumer lock into a fresh store inside the pinned frontend
image, then verifies the installed CSS. It does not substitute workspace packages,
a public registry, an unlocked resolution or a metadata-only probe.

[baobab-dev #48](https://github.com/baobab-platform/baobab-dev/pull/48) fixes
uv-versus-Poetry selection, missing/ambiguous locks and tools, root/frontend frozen
Node installation, exact pnpm/Yarn pins, optional exact Node checks and
noninteractive Corepack. Failed npm ci never falls back to npm install.
Requirements installations require hashes. Eight controlled-process regressions
exercise the actual lifecycle script. Owner CI additionally runs its real locked
uv project installation inside the published image with a correctly owned native-user workspace.

## Versioned source and image matrix

[The checked matrix](../../.baobab/dev10-toolchain-matrix.json) names twelve
immutable source snapshots. Eleven declarations satisfy the source image/profile
check; TMS has no declaration at its inspected source. SOURCE_VALIDATED is not
Codespaces readiness, language feature execution, successful database migration
or a safe newly released image. `scripts/check_dev10_matrix.py` checks the source
cohort, flags, provider commit, exact configuration hashes and profile capabilities.

The initial published-image observation is
[owner run 40181062042](https://github.com/baobab-platform/baobab-dev/actions/runs/40181062042),
review candidate `274b6faf31fcfdddc31cbc2edcb7d302a1453cdf`.
It resolved full image 1.4.4 to
`sha256:9603f0e7402aa85771e904db1c20f2ecc02f705131b266cb4ec3d1c24ea58ae4`
and installed the locked uv dependencies. Its final verifier failed under an
unmapped raw host UID (passwd/Flutter-cache errors), and a following successful
unit command masked that failure. This was a false-green lifecycle job; it is
not onboarding evidence. The provider fix uses strict inner-shell failure
propagation, the image native user/owned copy, and a separate exit-42 verifier
fault-injection test. Actual observed tools were Python
3.14.4, uv 0.12.18, Node 24.21.0, pnpm 11.24.0 and PostgreSQL client 17.11.
The current provider source configuration instead says Python 3.14.6 and uv
0.12.23. The matrix keeps source configuration separate from published bytes;
no unobserved release is inferred. This initial observation is historical and
does not replace final-head CI of a later provider candidate.

| Consumer group | Source requirement / gap | Upgrade validation required |
| --- | --- | --- |
| Shared, Thamani, ZuriBeans, Trade | Node/pnpm or npm are project-owned; exact Node files were absent at the audited source. This Shared increment adds its pin. | Frozen install, actual type/unit/build tests, owned BFF/browser suites and private archive access under each consumer's CI identity. |
| CP | Go 1.27.0; a separate Go feature is declared over the base image. | Actual Go toolchain, go test and owner PostgreSQL/identity integration gates. |
| Pulse | Python >=3.14 with a 3.14 file pin. | Locked installation and actual native PostgreSQL/Qdrant owner suites. |
| ERP | Java 17 / Python >=3.11; PostgreSQL 17. | OSGi build, native PG/JDBC, real iDempiere Gate D and ERP-A at the upgrade candidate. |
| Subscriptions | Java 21 required, while full image supplies 17; Dev Container PostgreSQL is still 16 though the engine targets 17. | Explicit JDK 21 layering, a new isolated PG17 store and real owner tests before onboarding. Never reuse the PG16 physical volume. |
| Payments | Rust >=1.88 required; it is absent from the declared base/profile and Dev Container features. | Explicit supported Rust provisioning and actual owner build, unit/PG and simulated lifecycle suites. |
| Infrastructure | Infra image is a separate Terraform/AWS profile, not an application-language image. | Terraform validation, owner integration/run descriptors and isolated disposable resources. |
| TMS | No environment declaration at the inspected source. | Owner declares its accepted actual runtime and runs its real implementation when available. |

## Unresolved gates

The provider PR is **unmerged**. Dependency installation or any successful targeted experiment does not override
failing lifecycle/full CI. Initial security checks found certifi PYSEC-2026-4320 and fixed
high-severity Go stdlib/x/net vulnerabilities embedded in Docker buildx/compose,
GitHub CLI, Task, Terraform and yq. The Python lock has been regenerated with the
published uv 0.12.18 to patch certifi without a lock-format upgrade. Provider
container security and toolchain lock drift still require final green checks.
No scan suppression or skipped required test supplies acceptance.

Toolchain resolution currently re-resolves mutable upstream latest entries in
normal publish CI and reports drift. A versioned candidate update must reconcile
its lock through the owner workflow, pass all image/profile/security gates, and
run affected consumers before release/promotion. An unrelated weekly update PR
is not silently merged as proof that these requirements passed.

A fresh hosted Codespace and its user's GHCR/npm entitlements remain unobserved.
Actions credentials and image/package reads are a distinct identity. Fleet
Foundation adoption requires each caller to review and pin the new Shared commit;
existing immutable Foundation references keep their old implementation. The
published baobab-dev image also retains its old baked scripts until an approved
release; the provider repository invokes its checked-out lifecycle directly.
All production/protected acceptance flags remain false, and DEV-10 has no
completion date.

## Upgrade and rollback procedure

1. Record reviewed source commits, project language/package-manager pins, image
   index and architecture digests, native store versions and prior receipts.
2. Create an upgrade branch and isolated candidate image; keep current consumers
   on their reviewed pins. Resolve/version the provider lock through its owner,
   check signatures/provenance and run all image architectures and security gates.
3. For every affected consumer, run its actual mandatory owner CI and frozen
   private dependency install. Observe a fresh private Codespace separately with
   its intended user identity, no credential values in logs or source, and no
   interactive Corepack prompt. Source-only matrix rows cannot satisfy this step.
4. Qualify PostgreSQL physical migration/restore in a separate owned drill. A new
   PG17 client/image does not convert a PG16 data directory. Retain the original
   volume and verified restore/rollback path; do not delete it for a tooling test.
5. Promote only the reviewed source/image/project-lock tuple. Rollback restores
   that tuple, rebuilds the disposable workspace and reruns frozen installation.
   Revoke run-owned credentials, remove run-owned resources and retain receipts;
   database restore/rollback remains independently owned and evidenced.
