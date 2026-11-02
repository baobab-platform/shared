# DEV10-R5 — Final engineering acceptance decision and evidence custody

**As observed 2026-11-02: HELD — not an acceptance certificate.**
Governing EA v2.3 and EA-DEV DEV-10. This engineering review follows merged
DEV10-R1 source reconciliation and merged R2 source evidence harness. It is
**not** DEV-13 staging/production approval, nor DEV-12 physical PostgreSQL migration.

## Decision

The R5 executable source checklist is in
[`.baobab/dev10-r5-acceptance.json`](../../.baobab/dev10-r5-acceptance.json).
The CLI and negative tests verify that the **packet remains truthful**;
a green R5 source-check workflow is evidence that false PASS claims are
rejected, **not** evidence that this entire gate passed. Running the CLI
with `--require-final` intentionally refuses until independent runtime,
security and user-review proofs exist, and a separately reviewed signed
evidence verifier is implemented. No editor, AI agent, or Actions runner
may declare themselves an independent attestation custodian.

## Evidence by wave

- **R1** — [Shared #426](https://github.com/baobab-platform/shared/pull/426)
  merged. Final owner baseline source SHA
  `eb9fb92f043c782acff5d87c77301d9a9e8b80dd`.
  No publish is inferred from this source state.
- **R2** — [Shared #427](https://github.com/baobab-platform/shared/pull/427)
  merged: user-hosted Codespace readback source tests. Actual new hosted-user
  creation, GHCR pre-start entitlement, private BXS npm read, denial
  negative, independent teardown and credentials revocation **not observed**.
  Consumer readiness PRs [Nabhold #101](https://github.com/baobab-platform/nabhold/pull/101),
  [ZuriBeans #154](https://github.com/baobab-platform/zuribeans/pull/154),
  [Thamani #48](https://github.com/baobab-platform/thamani/pull/48),
  [CP #456](https://github.com/baobab-platform/baobab-cp/pull/456)
  remain for user review; a green source CI is not a user Codespace.
- **R3** — Current candidate PRs:
  [Nabhold #102](https://github.com/baobab-platform/nabhold/pull/102),
  [ZuriBeans #155](https://github.com/baobab-platform/zuribeans/pull/155),
  [Thamani #49](https://github.com/baobab-platform/thamani/pull/49),
  [CP #457](https://github.com/baobab-platform/baobab-cp/pull/457),
  [Trade #187](https://github.com/baobab-platform/baobab-trade/pull/187),
  [ERP #124](https://github.com/baobab-platform/baobab-erp/pull/124),
  [Pulse #66](https://github.com/baobab-platform/baobab-pulse/pull/66),
  [Payments #47](https://github.com/baobab-platform/baobab-payments/pull/47).
  These are independent, **unmerged** owner tests, not blanket
  Node26/Java21/Rust native acceptance. Subscriptions,
  Infrastructure and [TMS #29](https://github.com/baobab-platform/baobab-tms/pull/29)
  still need explicit current-source native qualification.
- **R4** — Draft [baobab-dev #57](https://github.com/baobab-platform/baobab-dev/pull/57).
  Candidate Python3.14.10, Node26.13.0 Active LTS, native
  SHA256-pinned pnpm12.16.1, Corepack0.36.0, Java21, PostgreSQL17 and
  Playwright1.64.1. Both architectures (amd64/arm64) must pass full
  image builds, identity readbacks and unwaived scans. No signed,
  independently verified candidate digest or rollback is accepted.
- **R5 Security** — #57's strict Foundation container CVE gate **FAILED**
  as observed. [baobab-dev security #54](https://github.com/baobab-platform/baobab-dev/issues/54)
  retains vendor `linux-libc-dev` findings under **development-only,
  expiring** risk acceptance; the exception expires 12 November and
  developer risk decision 13 November. Pulse also has a real
  `msgpack 1.2.2` advisory `GHSA-j586-36cw-2gc2`, fixed in 1.2.3;
  [Pulse #66](https://github.com/baobab-platform/baobab-pulse/pull/66)
  cannot be counted green while this remains unresolved.

## Required independent receipts before a future acceptance

1. Final-head toolchain lock, digest and signed multiarch image with
   independent SBOM/provenance/cosign verification and all CVEs resolved
   or rigorously adjudicated **without** production waiver.
2. Real clean disposable **user** Codespace creation, exact pulled image
   digest, non-root ownership, private GHCR and BXS package read, frozen
   install, no interactive prompts, no public fallback; separate denied
   grants, independently confirmed deletion and token revocation.
3. All **13** owner repositories have real native CI, browser, Java, Rust,
   Go, Medusa, Pulse, ERP, TMS and providers as applicable; no simulated
   processor or carrier is counted as a real certified provider.
4. Candidate/source pins reproducible, private packages verified,
   rollback of image/lock/credentials/owned disposable resources rehearsed
   and independently witnessed. PostgreSQL physical PG16→17 must have its
   **own DEV-12** migration/restore evidence. Do not swap data volumes.
5. Independent security and architecture review, source owner acceptance,
   and your explicit review of every outstanding PR **before any merge**.
   Protected staging and production remain separate decisions.

## Evidence handling

Each receipt must identify actual source SHA, image digest, architecture,
provider/tenant scope, date, independent verifier, GitHub run or immutable
artifact reference, hash and teardown provenance. An Actions job's exit
code, a `receipt.sha256` hash, or a self-attested JSON boolean does not
constitute cryptographic identity or independent acceptance.

**No merges, no release image publication, no staging or production
activation are authorised by this packet.** The R5 gate remains
**HELD** by design; deficits are work items, not exceptions to waive.
