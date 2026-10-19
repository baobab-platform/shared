# Nabhold INT-03 dependency reconciliation — 19 October 2026

**Evidence class:** source/check/repository audit, not protected staging or
production acceptance. Governing: Accepted EA v2.2 and ADR-SHARED-036, existing
provider/capability/IAM authority and Nabhold Go-Live v2.0/ADR-NAB-0014.

Nabhold's [fresh detailed audit](https://github.com/baobab-platform/nabhold/blob/cd4f5af810fb7b8869af3c80017d88492f27bede/docs/go-live/evidence/progress-audit-2026-10-19.md)
records the inspected source baselines, gate matrix, open-PR/check inventory,
dependency ordering, Codespaces configuration and exact local/CI limitations.
This immutable audit revision is reviewable before [Nabhold #75](https://github.com/baobab-platform/nabhold/pull/75)
merges; that PR also records subsequent source/CI deltas. Neither record is
an acceptance decision or change to Shared’s normative test inventory.

| Lane | Reconciled finding | Evidence / remaining exit |
|---|---|---|
| INT-02 | Existing frozen synthetic Actions qualification is accepted | [Qualification register](int02-pulse-qualification-register.md), #35 merged at `03ad3f488e19ad446328ba6827363730e4252409`, run `39108198886` completed/success; newly merged source pins are not automatically qualified |
| Native C4-03 | Live-runner source exists; actual registered Kratos/Hydra→protected CP B–E not accepted | Approved registrations, current principals, validator/audience, protected credentials/CA, withdrawal, cleanup and provenance remain |
| IAM C4-03E/C4-04A | #126's mandatory gofmt failure repaired; reviewed merged source | `5bc1a7c4200a7b5dd029452c9d305408fb4a286e`; 46 checks completed with success/applicable skips. Integrity-only verification/transient observation. Automated ready-triggered review arrived after merge with two file-input findings; corrective #128 (`190cc179231ddb13b3ae7640e48d4748bd58c6e8`) has local focused/race tests passing; mandatory CI/completed review required |
| C4-04B/C | Independent CP-governed support/activation and protected consumer acceptance remain | No second provider registry, no health-to-entitlement inference, PARTIAL support and CRITICAL-grant denial retained |
| Nabhold identity/BFF | Existing OIDC, encrypted TLS Redis, current IAM/CP self-read and identity-smoke receipt code are merged | Actual connected network/client/CP Principal/TLS Redis/browser smoke still required; G04B-04 executive context remains an unwired deny-by-default seam |
| IAM subject profile | #127 fixes missing built-in basic access-token subject scope; persistent-client reconciliation and actual legacy variants added | Current candidate `2c001bf9b894f6239f3e02c7c0107376e8843e8c`; mandatory final-head real-variant CI required. `openid` is a request meta-value, not a fourth stored scope. Dormant product client stays disabled |
| Infrastructure handoff | #36 prepares private client/env/per-run Redis ACL/AES/epoch inputs and explicit PREPARED_NOT_PROVISIONED metadata | Current candidate `1c1b2a3f7fbeba089523c8a524b3532f9c36061b` fixes staging-directory cleanup; 12 source/security/actual Node-parser interoperability tests and 92 existing INT-02 source tests pass locally; no connected INT-03 proof claimed |
| CMS | Canonical content/Organisation/current CP and hierarchical scope source present, provider PARTIAL/non-production | Actual independently qualified provider, binding/context, published/preview and publish/unpublish/isolation/outage assertions remain |
| CMS dependency repair | Separate #37/#38 updates broke the exact Vitest/coverage peer | Paired repair #38 passed all 29 head checks/review and merged at `e2001e5fcc26301dd019575b49db6f782e71714e`; 259 tests, types/lint and clean install pass locally; #37 closed as superseded |
| Finance F1 / ERP | Three DRAFT wire contracts and native iDempiere authority proofs exist | Proposed ADR-SHARED-033 is not silently accepted; canonical F1 provider, FinanceBaseline and real Nabhold trial balance/reconciliation remain |
| Subscriptions | Temporary provider remains simulated/non-production | Production billing/native financial and reconciliation acceptance remains; estate/CP must not become a billing system |

## PR review boundaries

All open PRs and head check inventories in Nabhold, Shared, IAM, CP, ERP,
Subscriptions, CMS and Infrastructure were queried; selected relevant diffs
and failure logs were reviewed. This is not a blanket semantic approval of
every dependency update. Nabhold #73/#74 merged at `68fea868` / `55af5bd3`
after all 28 head checks completed successfully/applicably skipped. #71/#72
received artifact-version comment and coherent Foundation ref repairs and
merged at `d684134f` / `eb67b9f7` after all 29 head checks completed
successfully/applicably skipped. No green old candidate head justifies bypassing
a new failed/pending mandatory check.

CP's proposed Node 26/type major updates conflict with the Node 24 baseline;
networknt 3.x in ERP currently fails current schema/Jackson API compilation;
CMS GraphQL/TypeScript/ESLint major updates require accepted provider/toolchain
compatibility. Those changes must be repaired/reviewed separately, not merged
to improve an open-PR count. Old Shared workflow failure logs must be reconciled
against current main before assigning an engine defect.

## Next dependency closure

Complete current prerequisite PR reviews/checks, then provide and execute the
actual privately networked Nabhold identity smoke using separate synthetic
non-admin human identity and CP mapping. Independently bind the receipt's
declared sources to running images, then qualify CMS and extend to all
NAB-01/02/03/04 assertions in the existing normative matrix. Keep actual native
C4 qualification explicit; retained Keycloak compatibility is not a substitute
for the unverified Ory path. Real Nabhold legal verification/SoD/progressive
admission, protected R0 binding/staging and G17 retain independent inputs and
acceptance owners. No R0–R3 release, EA Gate D/E or production GO is asserted.

The merged Nabhold/ZuriBeans/Thamani/Shared/CP Codespaces image/package work
remains intact. Its private ports and approved package-read access do not
create shared lab DNS, protected identity credentials or a provider binding.
No new canonical contract, role, namespace, provider support or tenant authority
is introduced by this audit.
