# EA v2.2 — Cross-repository evidence audit and open-work inventory
## Snapshot: 15 October 2026

**Status:** Accepted audit snapshot for EA v2.2 planning; evidence, NOT independent production certification.  
**Plan:** [EA v2.2](EA-implementation-plan-v2.2-ADR-SHARED-036-integration-reconciliation.md)  
**Authority:** [ADR-SHARED-036 Accepted](../adr/ADR-SHARED-036%20%E2%80%94%20Cross-Repository%20Integration%20Testing%2C%20Tenant-Neutral%20Consumption%20and%20Production%20Deployment.md); v2.1 Accepted decisions retained  
**Sources:** Connected GitHub APIs: each listed repository's current main commit; organisation-wide open PR query (55); open branch names and comparison of selected relevant branch heads to main; individual owning PR status and CI where stated.  
**Limitations:** A repository branch list is not equivalent to a verified full-code audit of every line; comparisons were performed for relevant non-bot integration/authority branches (listed below), while the 54 routine dependency/CI PRs are classified from their PR titles and listing. No AWS deployment, private PSP or independent corporation-register session was available. A git branch may be old or contain already superseded implementation. Treat all unmerged branches as CANDIDATE, never proven live.

## 1. Definitive main commit baseline

| Repository | Reviewed main SHA | Significant current state |
|---|---|---|
| [shared](https://github.com/baobab-platform/shared) | 68d841e9cc8e96b3efb9b071a9c72da87fcee194 | ADR-SHARED-036 accepted through PR #310; v2.1 accepted historical baseline |
| [infrastructure](https://github.com/baobab-platform/infrastructure) | a7e5b842b87060695fa7ac47b0d2106e0a0a2331 | L3 Compose/CI, protected staging Terraform/source; L4 ADR-036 runner not merged |
| [baobab-cp](https://github.com/baobab-platform/baobab-cp) | 8c129a16912cb7a2d90b0ccfbaab420aafcdb47b | CP #400 money-movement authority, Organisation-first and authority code; no authentic founding activation |
| [baobab-iam](https://github.com/baobab-platform/baobab-iam) | 5dae8c44e943fc0106c1d4a8867a1c8a999a2234 | Native/federated IAM; Nabhold human audience client only in open PR #116 |
| [nabhold](https://github.com/baobab-platform/nabhold) | 09425a818b8a7f032c146088c2f58d64a8e86147 | PR #55 confidential OIDC BFF source merged; client disabled by default |
| [baobab-payments](https://github.com/baobab-platform/baobab-payments) | 0eb75baa4aeabaa103a527ecaf63200c17324c69 | PR #38 Gate D1 HTTP/CP/real Postgres/deterministic HyperSwitch suite; D2 real PSP staging outstanding |
| [baobab-erp](https://github.com/baobab-platform/baobab-erp) | 67bdcede1e52a31a9dce09276a148f8fff130eea | PR #99 six catalogued iDempiere authority classes Gate D; remaining classes and protected live acceptance |
| [baobab-trade](https://github.com/baobab-platform/baobab-trade) | 5e1cc718354e02c92658cf8779fa00068dbe6af1 | PR #149 cart COMMIT/lease fence; incomplete full order/merchant/payment E2E |
| [baobab-subscriptions](https://github.com/baobab-platform/baobab-subscriptions) | 52c69906343d7b1afee08a88b8d3afe118af0428 | P0-04A scope/contract convergence; full live capability/financial integration not proven |
| [baobab-trade-docs](https://github.com/baobab-platform/baobab-trade-docs) | 73cd1c168be39305c2e238b1f0a5b72da7821539 | P0-04A convergence; native document issuance and protected acceptance outstanding |
| [baobab-cms](https://github.com/baobab-platform/baobab-cms) | b72ff38dc5aefb2e6b859b06044f592b86c8fd24 | Organisation-first/scope fixes, no live G05 CP/CMS binding acceptance |
| [thamani](https://github.com/baobab-platform/thamani) | 965f09159abf43467a55cd212ba6748750e36ec9 | Existing estate code; clarified B2B/B2C logistics is not automatically reconciled in accepted local ADR |
| [zuribeans](https://github.com/baobab-platform/zuribeans) | e2f65f9895a3e6a6ed986a9a2b0aecec16947d5a | B2B UI and provider consumption work; no full protected integrated journey |
| [baobab-pulse](https://github.com/baobab-platform/baobab-pulse) | 6f4271d7b43db8d9c81e04d4f5dcc4cf50b27172 | Evidence/reference progress; P-CAP-08 certification/handoff needs exact evidence |
| [baobab-regulations](https://github.com/baobab-platform/baobab-regulations) | 89a113104410121deca43e9ce48ea865bacbfbe8 | Requirement/evaluation framework; official-source/provider promotion not accepted |
| [equator-estate](https://github.com/baobab-platform/equator-estate) | 5c43dcedc6f43cd2f9cafdecb446f2decca3cac5 | Early independent estate source; mature provider suite and incorporation claims remain unproven |

Commit SHAs are point-in-time source pins, not implied contract compatibility, vulnerability attestations, deployed image digests or proof of linked IaC.

## 2. Open pull request census (organisation-wide)

**55 open PRs discovered** via organisation-wide search on 15 October 2026 **before the new EA v2.2 documentation PR #311 was created**. One substantive source PR affects the immediate Nabhold/G04 critical path; 54 are developer-toolchain, dependency or Foundation CI candidates. These are **not merged**, and their PR head and CI may change. Do not accidentally reference them as active code.

| Repository | Open PRs identified | Relevance and classification |
|---|---|---|
| IAM | [#116](https://github.com/baobab-platform/baobab-iam/pull/116), [#115](https://github.com/baobab-platform/baobab-iam/pull/115) | **#116 substantive G04B-04:** green five final-head workflows, open; #115 action dependency update |
| CP | [#396](https://github.com/baobab-platform/baobab-cp/pull/396), [#397](https://github.com/baobab-platform/baobab-cp/pull/397), [#398](https://github.com/baobab-platform/baobab-cp/pull/398), [#399](https://github.com/baobab-platform/baobab-cp/pull/399) | Actions and frontend dependencies, including Node 26 / @types Node 26; do not assume production runtime migration |
| Shared | [#290](https://github.com/baobab-platform/shared/pull/290)–[#294](https://github.com/baobab-platform/shared/pull/294) | Five automation/action updates; none changes canonical EA status until merged |
| Infrastructure | [#29](https://github.com/baobab-platform/infrastructure/pull/29)–[#33](https://github.com/baobab-platform/infrastructure/pull/33) | Five workflow/action updates. INT-01 shall adopt approved SHA pins, not blanket-merge bots |
| ERP | [#97](https://github.com/baobab-platform/baobab-erp/pull/97) | Maven dependency candidate; unrelated to acceptance of six native ERP operations |
| Trade | [#139](https://github.com/baobab-platform/baobab-trade/pull/139), [#141](https://github.com/baobab-platform/baobab-trade/pull/141), [#142](https://github.com/baobab-platform/baobab-trade/pull/142), [#144](https://github.com/baobab-platform/baobab-trade/pull/144) | Four toolchain updates incl. TS 7/Node 26; review compatibility and security |
| ZuriBeans | [#95](https://github.com/baobab-platform/zuribeans/pull/95), [#108](https://github.com/baobab-platform/zuribeans/pull/108)–[#113](https://github.com/baobab-platform/zuribeans/pull/113) | Seven framework/Playwright/Medusa/Node candidates, not current integrated acceptance |
| Pulse | [#47](https://github.com/baobab-platform/baobab-pulse/pull/47)–[#54](https://github.com/baobab-platform/baobab-pulse/pull/54), excluding #46 | Eight dependencies/Actions including qdrant-haystack 12; require adapter migration tests |
| Thamani | [#16](https://github.com/baobab-platform/thamani/pull/16), [#22](https://github.com/baobab-platform/thamani/pull/22), [#24](https://github.com/baobab-platform/thamani/pull/24) | Foundation gate and frontend/Node update candidates; not B2B/B2C architecture approval |
| CMS | [#27](https://github.com/baobab-platform/baobab-cms/pull/27), [#28](https://github.com/baobab-platform/baobab-cms/pull/28), [#29](https://github.com/baobab-platform/baobab-cms/pull/29), [#31](https://github.com/baobab-platform/baobab-cms/pull/31), [#32](https://github.com/baobab-platform/baobab-cms/pull/32) | Five major developer/dependency candidates including GraphQL 17, TS7, ESLint10, Vitest5 |
| Equator & Estate | [#2](https://github.com/baobab-platform/equator-estate/pull/2), [#3](https://github.com/baobab-platform/equator-estate/pull/3)–[#8](https://github.com/baobab-platform/equator-estate/pull/8), [#15](https://github.com/baobab-platform/equator-estate/pull/15), [#18](https://github.com/baobab-platform/equator-estate/pull/18) | Nine tooling/CI/dependency candidates, not an operationally certified property service |
| baobab-dev | [#46](https://github.com/baobab-platform/baobab-dev/pull/46), [#47](https://github.com/baobab-platform/baobab-dev/pull/47) | Two toolchain/container/workflow upgrade candidates |

There are no additional open PRs in the searched Payments, Subscriptions, Trade Docs or Regulations repositories at this snapshot. Classification is based on PR metadata/title and selected substantive diff inspection, **not** an assertion that every dependency patch was line-by-line security audited. Prioritise changes that affect the L4 runner and lock manifest and review major versions individually.

## 3. Non-merged branches compared to actual main

Relevant branch comparison checks (ahead/behind are GitHub commit counts relative to each repository's main, **not** acceptance evidence):

| Repository / branch | Ahead / behind | Candidate work and disposition |
|---|---|---|
| Infrastructure / feat/integrated-testing-strategy | **2 / 24** | Older integration testing strategy/docs/CI; its L4 = staging terminology conflicts with ADR-SHARED-036's L4 real-component nonproduction. **Reconcile/reimplement**, do not merge blindly |
| Infrastructure / feat/mp2c-staging-foundation-v2 | **14 / 18** | Staging Terraform and workflow prototypes; not approved actual AWS account state |
| Infrastructure / feat/foundation-4-github-codespaces | **0 / 52** | Already contained in main ancestry; not new INT-01 |
| CP / feat/phase-b-c-platform-testing | **1 / 421** | Ancient divergent L2 test proposals; compare concepts to current main before any reuse |
| IAM / feat/phase-b-c-platform-testing | **1 / 129** | Ancient divergent integration tests; not current IAM security semantics |
| IAM / feat/g04b-04-nabhold-human-cp-profile | **4 / 0** | Substantive OPEN PR #116; source/CI accepted as PR-only candidate; merge separately |
| Nabhold / feat/codespaces-ci-governance | **0 / 64** | Behind main, no new integration code |
| Nabhold / feat/foundation-4-github-codespaces | **0 / 54** | Behind main, no new integration code |
| Shared / claude/ea-register-refresh-p0-04 | **0 / 22** | Superseded by newer main, not authority |
| Shared / feat/foundation-4-github-codespaces | **0 / 830** | Historic, not new capability |
| Payments / feat/la-05e-payment-beneficiary-pep-seam | **5 / 28** | Divergent early CP/payment legal-actor tests; superseded in part by #38, do not claim D2 |
| ERP / feat/la05d6-governed-inbox-native-order | **15 / 40** | Divergent native O2C/inbox prototypes; compare against merged ERP #99 before replaying |
| Thamani / feat/b2c-digital-estate-foundation | **0 / 53** | Historical branch, not new B2B/B2C logistics acceptance |
| CMS / feat/nabhold-g05-attested-organisation | **2 / 3** | Candidate stronger G05 content/Organisation tests; review/rebase against merged scope fixes before promotion |
| Pulse / feat/p-cap-08-certification-handoff | **17 / 13** | Candidate certification governance, explicitly NOT CP provider activation; no automatic promotion |
| Regulations / feat/r-cap-10-provider-acceptance | **6 / 2** | Candidate durable requirements, true PostgreSQL RLS/OPA checks and DEFER_PROMOTION; real source/issuer/CP qualification still pending |

Other historical and bot branches exist. The comparison subset concentrates on branches that could change the EA-INT critical path or provider-readiness decisions, and does not assert every historical branch was recompiled, tested or reviewed exhaustively. Reuse candidate commits by new reviewed PRs with current Shared pins and accepted ADR consistency, not by copying stale readiness badges.

## 4. Updated runtime and assurance findings

### 4.1 Payments: correct EA-R03 closure accounting

CP main #400 exposes an independent legal-authority resolver. Payments main #38 implements the D1 public HTTP route enforcement for create/confirm, capture, cancel/void and refund with selected actual infrastructure pieces and a deterministic provider fixture. This closes the prior dashboard's claim that **all Payments native HTTP enforcement is still unimplemented**. It does **not** close D2 protected staging, actual HyperSwitch/PSP merchant credential certification, real financial business actors, disbursement, external reversals or every remaining Payments operation. Preserve exact operation catalogue and two independent vetoes.

### 4.2 IAM and Nabhold: source merge vs approved humans

Nabhold BFF source #55 is merged. IAM #116 defines a dormant confidential CP-audience client, exact scope/redirect policy, local unit/Keycloak tests and a protected observation procedure but no actual approved issuer+subject Principal, client secret or real protected session. The open PR has green five workflows on 4ee06ef2a8d9912eca87c3d050a94e26b2f584f8. A passing code path must not be reported as real executive access. INT-02/03 may create explicitly synthetic principals under isolated IAM/CP.

### 4.3 Cross-tenant and legal admission

CP-026/027 and Shared canonical contracts support Organisation-first/progressive admission. Signed founding identity/registration evidence, approved Nabhold/Thamani control/mandates, external customer source records and protected IAM permissions are still not proven. In the new external API-only fixture, EXTERNAL_CLIENT and Tenant records are **synthetic** and must have no invented DigitalEstate. No founding-business company form is automatically upgraded to VERIFIED.

### 4.4 Current production environment

The only independently established deployment-placement fact from earlier source assessment is initial region **af-south-1**. This audit retrieved committed Terraform, policies and workflows—not an accepted AWS staging account ID, role ARNs, remote state bucket, KMS, production deployments or passed protected G17 ceremonies. No code-only document may claim those services are live.

### 4.5 Provider boundary health

CMS can test content resolution but cannot self-certify CP bindings. ERP's real JVM tests for six catalogued classes are narrower than full iDempiere production acceptance. Pulse P-CAP-08 candidate branch does not promote a provider. Regulations R-CAP-10 candidate branch expressly defers promotion pending official-law provenance, IAM resource server and CP integration. Trade Docs/Subscriptions require own execution-point coverage. No provider simply inherits ACTIVE status from a registered capability or an external branch.

## 5. Residual gaps and the earliest coherent execution baseline

| Rank | Action | State and dependency |
|---|---|---|
| 0 | Merge this Accepted EA v2.2 reconciliation; register authoritative evidence | Shared source only; no external credentials |
| 1 | INT-01 Infrastructure L4 harness | Not implemented; L3 present, divergent old prototype |
| 2 | Final review/merge of IAM #116, keep client dormant; INT-02 CP/IAM | Actual IAM/CP processes and synthetic fixtures |
| 3 | INT-03 Nabhold OIDC+BFF+CMS, CP binding/negative security | No approved real IAM Principal or protected CMS issuer yet |
| Parallel | Continue CP legal evidence, Payments D2/Subscriptions/Trade Docs/native PEP, scanner/custody source | Authentic source/cloud credentials are separate blockers |
| Next | Thamani B2B/B2C owner ADR; ZuriBeans B2B; external API-only zero-estate | Reusable harness and qualified contract |
| Later | Equator & Estate Co., Pulse/Regulations and finance/event mesh | Per-capability source readiness |
| Protected | Actual staging, independent legal/PSP/provider approvals and signed go/no-go | External Account/IAM/provider details; never substituted by CI |

**Audit conclusion:** Architecture is accepted; key code progress is genuine but uneven; platform-wide reproducible cross-engine integration is **not yet proven**, unrestricted production tenant onboarding is **not authorised**, and ADR-SHARED-036 does not change that evidence state.