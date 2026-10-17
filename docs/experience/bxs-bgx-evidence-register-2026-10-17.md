# BXS / BGX implementation and operational evidence register — 17 October 2026

**Governing architecture:** [Accepted ADR-SHARED-040](../adr/ADR-SHARED-040%20%E2%80%94%20Baobab%20Experience%20System,%20Frontend%20Engineering%20and%20Geospatial%20Presentation.md).  
**Nabhold release constraint:** `baobab-platform/nabhold/docs/go-live/NAB-GOLIVE-MP-001.md`, Accepted v2.0, G12/G15/G16/G17.  
**Evidence types never conflated:** Accepted decision → source → merged main → CI → versioned source → published package + SHA512/export verification → exact pinned consumer + browser acceptance → authenticated real components → protected staging → production approval.

This register supplements the historical BXS-01–05 inventory in `docs/experience/README.md`. Its snapshot is not itself a certification, and **no status is promoted by mere passage of time**.

## Current verdict by user-requested gate

| Gate | Verified source evidence | Status / blocking reason | Required next receipt |
|---|---|---|---|
| Shared Experience package publication | Baseline publish [39028924001](https://github.com/baobab-platform/shared/actions/runs/39028924001) and registry integrity [39029098417](https://github.com/baobab-platform/shared/actions/runs/39029098417), 17 Oct 2026, source `15c072d2b7a4`, published tokens/geo-core/UI **0.2.0** | **PARTIAL — newer versions not shown published.** Latest verified publish workflow logs list only those three 0.2.0 archives. Source PRs #336, #339 and #342 are **not** publication receipts. | Authorised `Publish Shared Packages` workflow_dispatch on current main and successful `Verify Experience Registry Releases` workflow_dispatch, retaining release run IDs, versions, `dist.integrity` SHA512, compiled export and manifest checks. |
| BXS-05 versioned adoption | [Nabhold #66](https://github.com/baobab-platform/nabhold/pull/66), [ZuriBeans #116](https://github.com/baobab-platform/zuribeans/pull/116), [Thamani #29](https://github.com/baobab-platform/thamani/pull/29), [CP #412](https://github.com/baobab-platform/baobab-cp/pull/412) | **PARTIAL — source/browser fixes merged; newer versions unadopted.** Current main manifests still pin Experience 0.2.0: Nabhold tokens+geo-core, ZuriBeans tokens+UI, Thamani tokens+UI+geo-core, CP frontend tokens+UI. New source-only releases cannot be substituted with Git main links or floating versions. | Exact published versions and frozen lockfile per consumer; independent runtime/browser Storybook/Playwright keyboard, denied/unknown, screenshots at narrow/mobile/desktop, manual AT, security, performance budgets, and merge receipts. |
| BGX-01 synthetic Thamani | [Thamani #28](https://github.com/baobab-platform/thamani/pull/28) and [#29](https://github.com/baobab-platform/thamani/pull/29) | **MERGED SOURCE/SYNTHETIC ACCEPTANCE**, not a production Thamani customer route or real carrier proof. | Approved customer BFF and real TMS/Trade Docs capability receipts; eventually G16 staging acceptance. |
| BGX-02 optional geo | [Shared #334](https://github.com/baobab-platform/shared/pull/334) MapLibre, [#340](https://github.com/baobab-platform/shared/pull/340) optional deck.gl, [#342](https://github.com/baobab-platform/shared/pull/342) deck.gl 0.1.0 source version | **MERGED SOURCE ONLY.** No confirmed newer GitHub Packages publication, no accepted consumer MapLibre/deck.gl pin, no real-browser provider tile/origin/CSP WebGL-failure screenshots or controlled staging source. | Registry verification first; Thamani authorised server projection → consented client MapLibre/deck.gl with source-listed fallback, licensed HTTPS origin, CSP, strict no-credential egress, 390px/1440px browser/axe/keyboard/visual/performance and revocation tests. |
| BGX-03 real IAM → CP → TMS/provider | [Thamani #31](https://github.com/baobab-platform/thamani/pull/31), synthetic admission and negative tests. [Infrastructure #35](https://github.com/baobab-platform/infrastructure/pull/35) remains open; last real integration log: `L4-CP-01=PASS L4-CP-02=BLOCKED L4-CP-03=PASS L4-IAM-01=PASS L4-IAM-02=PASS`, with integration job failure. | **NOT PROVED.** `baobab-tms` README states Foundation-0, no headless service; tracking ADR-TMS-0007 and ETA/optimisation ADRs Proposed, not certified, and no actual native object-level TMS provider evidenced. A synthetic BFF admission contract cannot manufacture this. | Accepted canonical tracking contracts and provider implementation; live issuer/audience/MFA, CP active context/binding, native TMS object PEP, positive/denied/revoked/wrong-audience/expiry/cross-tenant/grant-switch evidence, current certified provider and real-component CI. |
| Nabhold G12 / G15 / G16 | Nabhold accepted master plan G12 portfolio and reporting grants, G15 BFF composition, G16 AWS staging/EA-09. [Nabhold #66](https://github.com/baobab-platform/nabhold/pull/66) explicitly calls the Africa map editorial geography, not a market grant. | **PRESERVED AS ARCHITECTURAL BOUNDARIES; PROTECTED STAGING NOT PROVED.** No validated AWS staging-account OIDC plan/apply roles, remote-state, KMS/Secrets, protected environments, runtime binding/operation and signed EA-09/G17 evidence in this BXS/BGX scope. | Real af-south-1 account ownership/roles, protected environment, secrets/identity, CP capability, exact deployment digest, rollback/recovery/observability, accepted legal/provider sources and signed G17/go-no-go. |

## Package versions: do not conflate source and registry

| Shared package | Current main manifest | Most recent positively evidenced registry publication in this audit |
|---|---|---|
| `experience-tokens` | 0.3.1 | 0.2.0 only |
| `experience-ui` | 0.3.1 | 0.2.0 only |
| `experience-geo-core` | 0.3.1 | 0.2.0 only |
| `experience-geo-maplibre` | 0.2.0 | **Not yet verified published** |
| `experience-charts` | 0.1.0 | **Not yet verified published** |
| `experience-geo-deckgl` | 0.1.0 | **Not yet verified published** |

The absence of a found publication receipt is a **verification gap**, not a categorical claim that the package cannot exist in GitHub Packages. A fresh successful registry query with SHA512 and compiled exports may close it.

## BXS-01 through BXS-05 remaining gaps, disposition and owner

| Work item | Implemented source | Missing acceptance / disposition |
|---|---|---|
| BXS-01 ownership, contracts, inventory | Accepted Shared ADR-SHARED-040; versioned Shared packages; consumer evidence register | **ONGOING governance:** maintain ADR index, packages/consumer matrix and source-of-truth links as versions progress; no implicit group tenant authority. Shared owns contract register. |
| BXS-02 tokens and branding | Deterministic CSS and contrast/semantic token tests; 0.3.1 source | **PARTIAL:** publish/verify updated tokens; each estate must review design-system release, brand contrast/viewport states, reduced motion and no brand leakage. Consumer owners. |
| BXS-03 geography and provenance | Strict dates, anti-meridian/polar/bounds, evidence/estimate model, editorial Nabhold map; optional MapLibre/deck.gl source | **PARTIAL:** approved licensed map/worker origins, geo resource egress/CSP, uncertainty and unknown state, human review for disputed geography and external real-source provenance; exact consumer CI. Shared + respective estate. |
| BXS-04 Base UI primitives and accessibility | Controlled Dialog/Tabs, Storybook Chromium, keyboard/axe, CP and ZuriBeans consumer adoption source | **PARTIAL:** real assistive-technology/manual navigation audit and exact upgraded package/browser/mobile acceptance per estate; do not assume Storybook automatically certifies every route. Shared + estate. |
| BXS-05 consumer migration | Nabhold #66, Thamani #29, ZuriBeans #116, CP #412 merged with CI | **PARTIAL:** bounded old-version adoption only; new pinned version rollout, page/route inventory, production-shell integration, LCP/INP/CLS performance thresholds and per-consumer screenshot/keyboard/negative proofs remain. Estate owners. |
| BGX-02 real deck.gl browser | Shared model/negative tests, 0.1.0 source | **OPEN:** actual deck.gl + MapLibre browser at exact pinned versions with WebGL available/unavailable, consent/unmount/denial/keyboard and origin-policy tests in opted-in consumer. |
| BGX-03 TMS authority | Accepted TMS charter only; Thamani synthetic BFF preflight; substantial IAM/CP INT-02 but L4-CP-02 blocked | **BLOCKED:** actual authoritative transport service/contract, certified tracking events and current native object enforcement. Never fabricate production events to make CI green. |
| BGX-04 protected operation | Design decisions and source checks | **BLOCKED:** G16 staging identity, AWS OIDC, secret custody, tenant-bound live provider, observability/recovery and signed acceptance. |

## Dependency-ordered implementation and no-bypass policy

1. **Release:** maintainers deliberately dispatch [Publish Shared Packages](https://github.com/baobab-platform/shared/actions/workflows/publish-shared.yml) from audited `main`, then [Verify Experience Registry Releases](https://github.com/baobab-platform/shared/actions/workflows/verify-experience-registry.yml). Publication job is separate from `Version Shared Packages`; a green Changesets source version is insufficient.
2. **BXS consumer migration:** stage scoped PRs per estate after verified package release. Pinned versions, lockfiles and platform Node24 remain mandatory; test all consumer shells and visual/a11y/performance/denial contracts; never pin to Git main.
3. **BGX-02:** opt-in Thamani client MapLibre/deck.gl behind already-authorised BFF projection, no browser TMS credentials, no tracking claims or public donation tile SLA; require real browser acceptance.
4. **BGX-03:** implement and register **accepted** TMS tracking provider and real IAM/CP/TMS integration, remove Infrastructure PR #35 L4-CP-02 block with real current certified provider, establish revocation/cross-tenant/live negative proofs.
5. **BGX-04 / G16:** protected staging account/roles, provider/market/licence/privacy and operational receipts; only then consider independent EA-09 and G17 production permission.

**Release blocker principle:** neither a code merge, source package version, presentation screenshot, artificial principal, fixture provider or CI pass may be re-labelled as a published tarball, authenticated real-provider proof, protected staging or production GO. No unapproved credentials, bypasses or fake AWS values.

---

## 18 October 2026 — verified publication and consumer rollout

**This addendum supersedes the 17 October publication/consumer statuses above.**
It does **not** supersede the still-open BGX-02 real renderer, BGX-03
authoritative TMS or G16 protected staging requirements.

### Published and SHA512-verified Shared artifacts

The approved [Publish Shared Packages run 39073176845](https://github.com/baobab-platform/shared/actions/runs/39073176845)
completed on `main` commit `83e5a4a5db7111fa4fbd3603559b1ef6136eaae3`.
The subsequent independent
[Verify Experience Registry Releases run 39073362603](https://github.com/baobab-platform/shared/actions/runs/39073362603)
successfully validated published manifests, SHA512 archive digests and required
compiled exports for **all six** immutable versions:

| Published package | Verified version | Status |
|---|---|---|
| `experience-tokens` | 0.3.1 | Published; SHA512 and required exports verified |
| `experience-ui` | 0.3.1 | Published; SHA512 and required exports verified |
| `experience-geo-core` | 0.3.1 | Published; SHA512 and required exports verified |
| `experience-geo-maplibre` | 0.2.0 | Published; SHA512 and required exports verified |
| `experience-geo-deckgl` | 0.1.0 | Published; SHA512 and required exports verified |
| `experience-charts` | 0.1.0 | Published; SHA512 and required exports verified |

### Exact consumer adoption and independent acceptance

| Consumer | Merged commit / PR | Approved direct pins | Mandatory acceptance |
|---|---|---|---|
| Nabhold | [#67](https://github.com/baobab-platform/nabhold/pull/67), `61ed6789e4204ade7cad4923cf39a209d419a6fb` | Tokens 0.3.1, Geo Core 0.3.1 | 20 successful checks, including map viewport/keyboard/quality/security/Foundation |
| ZuriBeans | [#117](https://github.com/baobab-platform/zuribeans/pull/117), `1aa32959429ce97b9fb284f26350636a4a54352a` | Tokens 0.3.1, UI 0.3.1 | 22 successful checks, including Storybook, B2B browser/visual/accessibility/security |
| Thamani | [#32](https://github.com/baobab-platform/thamani/pull/32), `85d60ab2ba6f3d2f51a2b7e37be35b9f12683465` | Tokens/UI/Geo Core 0.3.1 | 23 successful checks, including reviewed mobile/desktop screenshot updates, logistics denial and browser acceptance |
| Control Plane Console | [#413](https://github.com/baobab-platform/baobab-cp/pull/413), `a0fef3a05718bb7f3f41dc47746521d0bd91921e` | Tokens 0.3.1, UI 0.3.1 | 23 successful checks, including console build, QA, Foundation, security and operations evidence |

The UI package resolves the published Geo Core 0.3.1 transitively where a
consumer does not import that contract directly. All four lockfiles have
published SHA512 digests, frozen pnpm 11.24.0 reproducibility, and narrowly
versioned release-age exceptions. Previous 0.2.0 lockfile records were
removed. Temporary privileged workflows used for lockfile reconciliation
removed themselves and are not present in merged `main`.

**No unused consumer dependency was added merely to consume a newly
published artifact.** MapLibre 0.2.0, deck.gl 0.1.0 and Charts 0.1.0 are
published but require their own capability-scoped, tested opt-in consumers.

### Gates explicitly still open

1. **BGX-02 operational geography:** consented Thamani MapLibre + deck.gl
   browser integration, lawful tile/style/worker origins, CSP, degraded-mode
   text/keyboard alternative, privacy, real provider and performance tests.
2. **BGX-03:** independently implemented/certified TMS tracking provider with
   live IAM → CP → TMS PEP, including expiry/revocation/cross-tenant denials;
   synthetic Thamani admission preflight is not this evidence.
3. **BGX-04 / Nabhold G12/G15/G16:** protected staging IAM/workload roles,
   Secrets/KMS/state, source privacy/residency, producer grants, recovery,
   real provider acceptance and signed G17 go/no-go. No production claim.

[Release-gate issue #344](https://github.com/baobab-platform/shared/issues/344)
is closed for **published package integrity and baseline exact-version estate
adoption only**. These three outstanding gates are deliberately not waived.
