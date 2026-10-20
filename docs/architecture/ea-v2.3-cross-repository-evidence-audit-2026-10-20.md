# EA v2.3 — Cross-repository source, architecture, CI and open-work evidence audit
## Dated baseline: 20 October 2026 (Africa/Johannesburg)

**Evidence class:** REPOSITORY-SOURCE/ADR/PR/CHECK inspection. **Not** exhaustive line-by-line source assurance, successful connected end-to-end verification, regulatory/legal acceptance, AWS staging observation or production certification.
**Decision:** A v2.3 programme rebaseline is justified; EA v2.2 is historically retained, not silently rewritten.
**Scope:** 20 first-party repositories returned by GitHub organisation-scoped repository discovery, including templates/Developer Experience, all `baobab-*` engines, Infrastructure, Shared and Digital Estates.
**Method:** On 20 October 2026, discover organisation repositories (including non-`baobab-` names); read each accessible `main` branch SHA, open-PR listing, recursive repository path inventory, and representative owning README/ADRs/provider/architecture evidence; cross-check the live v2.2 dashboard, 15 October audit, 18 October INT-02 receipts, 19 October INT-03 dependency and Nabhold registers, Shared ADR-037–041, ERP PR #110 and actual failing Gate-D Actions log. Original snapshots are pinned below. GitHub API availability and the existence of source files do not prove a complete runtime review of all files or all CI matrix jobs.

## 1. Exact main baselines and candidate PRs

| Repository | `main` SHA at audit | Open PRs | Maturity / material consequence |
| --- | --- | ---: | --- |
| `shared` | `810128fbe59aff7b0b1d5dd76e9ce4dce71b2063` | 5 | ADR-SHARED-041 now Accepted/merged; ADR-037/038/039/040 Accepted; ADR-SHARED-033 Finance F1 still Proposed; v2.2 dashboard live but has stale historical assertions in portions |
| `infrastructure` | `84079fa6720da5e1dd5f14d9d0b0d3b0dd149f28` | 6 | INT-01/02 immutable synthetic Actions qualification; live connected INT-03 remains unproven; #37 candidate only; protected staging external inputs absent |
| `baobab-cp` | `3810b8222fa6df09b829e7c725d534af10b1155c` | 4 | Organisation-first admission, legal mandates, provider context/resolvers and guarded native authority source; no genuine founding acceptance or protected end-to-end certification |
| `baobab-iam` | `63db55c87fda13762fc438a6d32a885a63ddb353` | 1 | Human profile/subject fixes and live-runner preparation merged; Kratos/Hydra→protected CP C4-03 B–E still lacks actual protected acceptance |
| `baobab-erp` | `0bcf6d1b9d0ec262a1400eb9ce83981305e5d32d` | 9 | Native purchase/payables posting guard ERP-A/B exists; Bank/cash/inventory/costing/manufacturing families remain specifically denied; #110 Baobab People + PG17 **OPEN**, not on main |
| `baobab-trade` | `5435e7bf3e5a056920fe5d95426abfb48b3b093e` | 8 | Medusa/B2B-B2C commercial engine with guarded cart/order source; ADR-SHARED-039 seller binding and native operation-class closure not equivalent to all-trade certified execution |
| `baobab-payments` | `0eb75baa4aeabaa103a527ecaf63200c17324c69` | 2 | Real Payments/CP deterministic HyperSwitch Gate D1 source; real PSP, D2 protected staging, merchant/corridor eligibility and money transfer not certified |
| `baobab-subscriptions` | `52c69906343d7b1afee08a88b8d3afe118af0428` | 2 | Contract convergence; simulated billing and unqualified production provider; invoice-to-ERP legal-entity handoff requires operational proof |
| `baobab-cms` | `e2001e5fcc26301dd019575b49db6f782e71714e` | 6 | Content, Organisation scope and partial declared provider source; current real CP/CMS/Nabhold consumption and publication rights not qualified; Node 22 drift versus approved Node 24 |
| `baobab-pulse` | `6f4271d7b43db8d9c81e04d4f5dcc4cf50b27172` | 8 | EvidenceSet/ResearchMission and bounded Haystack/Qdrant, named INT-02 synthetic search provider; production AI/domain source and provider promotion/independent operational approval incomplete |
| `baobab-regulations` | `89a113104410121deca43e9ce48ea865bacbfbe8` | 1 | Source/evidence/BRIR→Rego deterministic evaluator implementation; PARTIAL provider, official-source authority and active CP policy certification unresolved |
| `baobab-trade-docs` | `73cd1c168be39305c2e238b1f0a5b72da7821539` | 1 | ADR and cross-repository contract convergence but **no production service runtime**; document issuer/customs workflows and real provider proof absent |
| `baobab-tms` | `9a4761f6a4c039cb000eb29503a748faa369d691` | 1 | Accepted TMS ADR-0001/0002 only; ADR-0003–0019 and TECH-01 Proposed; Foundation-0, **no runnable transport authority/provider**, critical Thamani dependency |
| `baobab-scf` | `7016dfd35773adc3bf911ae2ffa36565d5855616` | 1 | 35 Proposed SCF ADRs; Foundation-0/no financial service, no accredited funder/provider/regulated financing authority; optional future partner-led finance lane |
| `baobab-dev` | `a161d52f32974327ac35cb1519918be08547815e` | 2 | Organisation development image/toolchain supplier; pinned Codespaces and registry access must converge across consumers without floating image or unsafe PR upgrades |
| `nabhold` | `bc672d37e0e301d30090937f103710a82898df26` | 1 | Accepted Go-Live v2.0; INT-03 source prepared, no full connected identity/CMS qualification; G07/G08 blocked; #77 candidate source/report |
| `thamani` | `a5a0df2ce79325a722eb98e3f7a86cd5fa79c4d1` | 4 | **Accepted ADR-THA-0018 says B2B integrated logistics enterprise**; old B2C storefront is legacy; dedicated TMS/Docs/Regulations capabilities not production-certified |
| `zuribeans` | `8d74f5979bb6d7825637ad703a90f49b5bb2b1f2` | 9 | B2B buyer/supplier storefront and BXS package source; real approved trade, regulated UG↔ZA corridor, supply and document journeys require signed provider/legal gates |
| `equator-estate` | `5c43dcedc6f43cd2f9cafdecb446f2decca3cac5` | 9 | Legacy Django estate; README retains pre-rename `nabhold/shared` and `.nabhold/environment.yaml`, baobab-dev 1.2.6 reference; adoption/authority/modernisation audit required before INT-06 |
| `engine-template` | `61c0ccf3449543772a9e8bbd0e9887ac8e5af3e6` | 1 | Onboarding template, example manifests and placeholder instructions; adopt Shared ADR-041 and current canonical Foundation/baobab-dev baselines before creating new active engines |

**Counts:** 20 discovered repositories; open PR counts at this API snapshot total 82, including many Dependabot/toolchain updates and explicitly unmerged implementation candidates. This count is a **listing**, not a verification that every PR's CI passed. Never infer progress from PR count, branch existence, or directory presence.

## 2. Material findings requiring v2.3 corrections

### F-01 — Accepted architecture and active execution schedule diverged

EA v2.2 §3.1/§9 still described Infrastructure #35 unmerged, IAM #116 unmerged, INT-01 next authorised source increment and INT-02 unproved at the 15 October freeze. The dashboard and 18 October qualification now prove INT-01/02 at **specific frozen synthetic Actions pins** and classify INT-03 as next connected consumer execution. Preserve unobserved interactive Codespaces acceptance, source-pin rotation and protected staging as open.

### F-02 — Native domain execution has finer-grained mandatory authority

Accepted Shared ADR-037/038/039 refines P0-04B/EA-R03. ERP-B payment **recording** requires actual provenance and is not payment execution; deferred bank/cash/production/costing operations remain DENIED. Trade requires native order classifications, CP-owned seller-operating bindings and execution-point vetoes. The v2.3 test matrix must include source-level, native-operation/commit-level *negative* evidence; an HTTP 403 alone is insufficient.

### F-03 — Thamani's governing B2B decision is more specific than v2.2

Accepted [ADR-THA-0018](https://github.com/baobab-platform/thamani/blob/main/docs/adr/ADR-THA-0018%20%E2%80%94%20B2B%20Commercial%20Model%2C%20Legacy%20Supersession%20and%20Platform%20Engine%20Responsibility%20Reallocation.md) defines **B2B integrated logistics** and supersedes legacy B2C ecommerce. The original EA v2.2 INT-04 phrasing 'Thamani B2B/B2C logistics' and its D-14 assertion that business model reconciliation remained undone are stale. Last-mile delivery to a natural person or B2B2C execution does not establish B2C as Thamani's selling model. Tests must follow Accepted owner scope. A future B2C commercial offering requires a new Accepted owner ADR and contracts.

### F-04 — TMS is an unready critical dependency; SCF is not a production engine

TMS is Foundation-0: two Accepted foundation ADRs, remaining Proposed. No actual tracking, quotation/booking, carrier, trust, consent, SLA or source-authenticated logistics provider exists. The Thamani digital experience cannot promote synthetic maps/shipments into real customer execution. SCF is also Foundation-0 and proposed: do not assume a funder, licence, underwriting, lending or disbursement right. TMS is a consequential logistics-provider critical path; SCF is **not a mandatory Nabhold R0/INT-03 critical-path dependency**.

### F-05 — ERP People and PG17 have distinct authority/implementation states

[ERP PR #110](https://github.com/baobab-platform/baobab-erp/pull/110) adds ADR-ERP-023 with Accepted *document status* on its feature branch and PostgreSQL 17 source defaults; neither is merged on ERP `main` or licensed-source-qualified. At the checked PR head `d432d2f...`, 41 check runs completed, with **Gate D FAILED**: invoking `idempiere/acceptance/run-gate-d.sh` produced **Permission denied / exit 126**, followed by missing evidence artifacts. This is an executable-bit/invocation/runner issue, **not** a PostgreSQL 17 compatibility result. Do not upgrade ERP People source, statutory compliance, database migration, CDSoftware v13 compatibility or native finance acceptance to complete. iDempiere 13 and Java 17 remain pinned; PG17 is already the Shared target for RDS architecture and separate CP tests. Migration of any persistent PG16 volume demands operator-approved data-copy/pg_upgrade runbook and restore proof.

### F-06 — Accepted Shared ADR-040/041 introduce platform-wide quality adoption

Shared ADR-040 governs BXS frontend primitives and published packages, while Shared ADR-041, [merged 20 October](https://github.com/baobab-platform/shared/pull/352), governs **ALL** first-party `baobab-*` repositories and Group estates. The exact principle is: **Learn from established products. Reuse what is proven. Question what is inadequate. Re-engineer what must improve. Build what Africa needs.** Adopt/adapt/re-engineer/build decisions now require proportionate review evidence and lawful IP/licence provenance. The approved quality standard applies to application software, engines, APIs, infra, developer tooling, experiences and future enterprise products; green CI, code comments and published packages do not alone prove user/business acceptance.

### F-07 — Foundation and toolchain convergence is not uniform

CMS still reports a Node 22 runtime path; target Node 24 requires verified dependency/CI/prod compatibility. Equator's README still references legacy `nabhold/` locations and an outdated development image. Engine-template placeholder defaults need governance rebaselining. Avoid a cross-repository untested mass upgrade and do not assume no drift from image publication or Codespaces success in one repo.

### F-08 — Cross-engine maturity is asymmetrical and external acceptance open

Nabhold G01 legal verification/mandates, G05 CMS, G06 finance, G07 HR, G08 payroll, G10 billing, G11 payments, G16 infrastructure and G17 protected acceptance are still separately gated. Shared Finance F1 ADR-033 is **Proposed** despite DRAFT contract/source merges. Pulse and Regulations have meaningful implementation but only bounded provider readiness; Trade Docs and TMS do not have production runtimes. External API-only INT-07 remains unproven. No independent regulatory source, actual PSP, bank mandate, RDS production instance, protected AWS role/bucket, live human login, funded transaction, payroll or statutory filing may be inferred.

### F-09 — Historical registers need a single fresh source-of-truth pointer

`ea-dashboard.md` currently calls itself v2.2 and last-updated 18 October but contains 19 October appendices; its frozen 15 October baseline lines still say L4 and IAM #116 are unmerged. v2.3 shall preserve dated evidence history without deleting contradictory past observations, add a new 20 October accepted source snapshot, update current headers/queue, and link the v2.2 file through immutable Git history/historical pointer. Nabhold Go-Live v2.0 remains independently Accepted; do not silently version or re-scope it.

## 3. Cross-ADR integration map

| Decision | Status at audit | Required programme consequence |
| --- | --- | --- |
| ADR-SHARED-036 | Accepted and active | L4 versioned real-component matrix, INT-01..08, external zero-estate and protected staging separation |
| ADR-SHARED-037/038 | Accepted | Closed ERP operation classes, payables execution provenance, bank/cash/manufacturing still denied |
| ADR-SHARED-039 | Accepted | Native Trade order PEP and CP-approved seller operating bindings |
| ADR-SHARED-040 | Accepted | Shared BXS packages, published/pinned exact consumer versions, accessible visual/geospatial evidence |
| ADR-SHARED-041 | Accepted in `shared/main` | Organisation-wide African enterprise engineering excellence and ENG-01..05 rollout |
| ADR-SHARED-033 | **Proposed** | Finance F1 contract/provider business review still needed; do not assert accepted canonical programme |
| ERP ADR-ERP-023 | **Accepted wording in unmerged ERP PR #110** | Evaluate first-party Baobab People architecture as pending ERP merge, with independent Shared contract and statutory decisions |
| ADR-THA-0018 | Accepted | Treat Thamani as B2B logistics, mark legacy B2C source as deprecated; TMS/Docs runtime is independent |
| TMS ADR-0001/0002 | Accepted | Engine mission and domain only; no runtime/provider claim |
| TMS ADR-0003..0019; TMS-TECH-01 | Proposed | Build/accept scoped technological and execution architecture before certified logistics claims |
| SCF ADR-0001..0035; SCF-TECH-01 | Proposed | No activated financing engine; evaluate optional partner-led risk/control programme and legal permissions |
| Nabhold Go-Live v2.0 | Accepted independently | G00–G17 and R0–R3 retain their existing owner gates; People/finance not made implied current services |

## 4. Candidate PRs and concrete blockers at this freeze

- [Infrastructure #37](https://github.com/baobab-platform/infrastructure/pull/37): connected INT-03 source **OPEN**; exact network/issuer/client/CP/BFF/CMS real run and teardown must be accepted, not inferred from handoff generation.
- [Nabhold #77](https://github.com/baobab-platform/nabhold/pull/77): INT-03 evidence reconciliation **OPEN**; not protected acceptance.
- [ERP #110](https://github.com/baobab-platform/baobab-erp/pull/110): Baobab People/PG17 **OPEN** with failed Gate-D execution due to Permission denied. Repair and rerun all mandatory checks before merge.
- [Shared #352](https://github.com/baobab-platform/shared/pull/352): **MERGED** to `810128f` after green checks, ADR-SHARED-041 active.
- [Infrastructure #35](https://github.com/baobab-platform/infrastructure/pull/35): **MERGED** to `03ad3f488e19...`, bounded synthetic INT-02 qualification only.
- [Shared ADR-SHARED-033](https://github.com/baobab-platform/shared/blob/main/docs/adr/ADR-SHARED-033%20%E2%80%94%20Corporate%20Finance%20Capability%20Namespace%20and%20First%20Canonical%20Finance%20Tranches.md): Proposed; DRAFT F1 source/consumer code is not a certified ERP F1 provider.
- Five open Shared PRs at audit were dependency/toolchain candidates. Across the estate many open PRs are Dependabot candidates; no blanket merge or open-head readiness inferred.

## 5. Programme remediation decisions

1. Publish EA v2.3 as **new active plan**, retain v2.2 as historical, and update the dashboard with a dated merged-source audit.
2. Preserve all EA/LA/PEO/INT Gate A–E and current Shared/CP/domain authority. Reprioritise INT-03 and current Finance/Trade/ERP, authentic legal/identity work; keep INT-07 mandatory.
3. Add **TMS/Thamani B2B first-class dependency**, distinguish proposed SCF; add ERP-local **Baobab People** and ZA/UG country localisation **conditionally** without minting Shared keys.
4. Adopt ENG-01–05 and BXS quality/release work as cross-cutting standards, not a single blocking 'rewrite all' work item.
5. Add package/image/PG17/toolchain compatibility and explicit data-migration gates, plus real protected AWS/account/PSP/legal acceptance still unproven.
6. Amend the L4 acceptance matrix only through the owning Shared scenario register; a companion v2.3 delta matrix may enumerate BXS/ENG/TMS/People/SCF evidence without inventing L4 scenario identifiers.
7. Each implementation PR supplies exact main/PR-head/source pins, CI and evidence, approver, remaining blocker and rollback; failures and pending reviews cannot be declared successful.

## 6. Audit limitations and next evidence requirement

This is broad **repository-level cross-architecture and PR-state reconnaissance**, not a substitute for 20 exhaustive source-quality/security line audits or active cloud/service verification. Some README statements are dated and may lag more recent code. Where conflicts exist, this audit prefers exact merged code, accepted ADRs and dated run receipts over stale prose, while identifying unresolved conflicts for the owning repo. The next source work must deepen inspection at each named incremental implementation gate. Do not treat this survey as legal, payroll, customs, funder, logistics carrier, tax, PSP, privacy or security certification.

A future census of additions/removals SHALL use organisation API/approved connector access and record discovered repositories; the 20 are the discoverable snapshot **as of this date**, not a permanently exhaustive catalogue of all subsidiaries or future engines.
