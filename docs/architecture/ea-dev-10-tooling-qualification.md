# DEV-10 tooling and contract qualification

## 2026-11-02 — DEV10-R1 merged source integration (current observation)

This dated addendum supersedes **only** the 25 October *source merge and
matrix-source snapshot claims* below; historical failures and the original
v1.4.4 published image digest remain an audit record, not current runtime
qualification. [baobab-dev PR #48](https://github.com/baobab-platform/baobab-dev/pull/48)
and [PR #50](https://github.com/baobab-platform/baobab-dev/pull/50)
are both **merged** into one observed `main` commit
[`eb9fb92f043c782acff5d87c77301d9a9e8b80dd`](https://github.com/baobab-platform/baobab-dev/commit/eb9fb92f043c782acff5d87c77301d9a9e8b80dd).
Their final reviewed PR heads were
`415a7c20a4602f4f01103522ae42b1a39b08b96c` (40 successful, 9 skipped)
and `1aa22c2668eda2a49ce5581da5b2383069599b37`
(38 successful, 9 skipped), respectively. The merged-main push's GitHub
Pages job failed and image CI was still running when observed; do not
retroactively claim green merged-main publish or a newly signed image.

The canonical provider's **merged source** still pins Python 3.14.6,
Node 24, pnpm 11.24.0, Java 17 and Playwright 1.62.1; PostgreSQL client
major 17 remains correct. SHA-256 of merged source `config/versions.lock`
is `3927b97b904cf8871b6d00d08d80ea63a2b514d2c7425d694bc481d51360d2ac`;
the capability declaration SHA-256 remains
`fa04f8ecc4d0a7eb351e7785e421d9d3b325999829c7c27ef93cecbf67e34b12`.
The R1 checker now tests these actual merged bytes, not the previous main
source SHA.

The source census has **13** explicitly inspected repository `main` commits
and now includes **Nabhold**, plus correction of two earlier stale claims:
Subscriptions already declares `postgres:17-alpine` but **still needs Java21
runtime support**; Payments already layers an unversioned Rust feature but
still has PostgreSQL 16, without qualified exact Rust/Cargo native evidence.
TMS's environment-contract implementation exists at **open, unmerged
PR #29**; no merged TMS declaration is inferred.

**Preferred next-upgrade target, not an installed version:**
[`.baobab/dev10-target-toolchains.json`](../../.baobab/dev10-target-toolchains.json).
As of 2 November: Python **3.14.10**, Node **26.13.0 Active LTS**,
pnpm **12.16.1 stable** (`latest`, not `next-12`),
Java **21**, PostgreSQL **17** (observed 17.11),
Playwright **1.64.1**, Corepack **0.36.0**. Node 26 does **not** bundle
Corepack; the upgrade must install and verify an independent pinned Corepack
package. No silent Node 24/Java 17 fallback is approved. If native
Medusa/other runtimes fail under Node 26 or Java21, retain the old effective
owner pin only on a recorded, reproducible, separately reviewed exception.
The candidate images and consumer lock migrations belong to **DEV10-R4**;
R1 source reconciliation does not rewrite 13 independent owner repositories.

The 295 linux-libc-dev vulnerability advisory matches remain a
**bounded development-only risk decision**, not global CVE remediation,
cryptographic VEX approval or a protected release. Refer to
[owner security issue #54](https://github.com/baobab-platform/baobab-dev/issues/54);
the temporary risk decision expires **13 November 2026 00:00 UTC** and
the Foundation exception expires **12 November 2026**. Do not promote
staging or production through this exception.

None of the eight unchanged DEV-10 acceptance cases have qualified
hosted user Codespaces, private user registry access, actual provider
upgrade, native consumers, physical database migration or rollback.
All remain BLOCKED until independently observed.

---

Observed 2026-10-25. This is a scoped engineering increment of the accepted
EA-DEV plan, not completion of clean Codespaces or fleet upgrade acceptance.
DEV-06 development engineering has since qualified through Shared #400 and
Infrastructure #60. Certified-provider INT-07 acceptance remains separate;
this tooling increment does not block safe DEV-05 CMS engineering.

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

