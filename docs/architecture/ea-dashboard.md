# EA Implementation Register (v2.3 — live)

**Active governing plan:** [Accepted EA Implementation Plan v2.3 (20 October 2026)](EA-implementation-plan-v2.3-2026-10-20.md), superseding v2.2 **only for active execution ordering and freshness of programme status**. Its source baseline is the [20-repository audit](ea-v2.3-cross-repository-evidence-audit-2026-10-20.md), and the new [product / engineering acceptance delta](ea-v2.3-acceptance-and-adoption-matrix.md) supplements—but does not replace—the [v2.2 canonical L4 scenario matrix](ea-v2.2-integration-acceptance-matrix.md).
**Last authoritative rebaseline:** 20 October 2026. **Status:** Accepted programme architecture; downstream code, live legal/identity, statutory/provider and production gates remain independently unaccepted as specified below.
**Active philosophy:** [Accepted ADR-SHARED-041](../adr/ADR-SHARED-041%20%E2%80%94%20Baobab%20Platform%20Engineering%20Philosophy%20and%20African%20Enterprise%20Product%20Excellence.md): **Learn from established products. Reuse what is proven. Question what is inadequate. Re-engineer what must improve. Build what Africa needs.**

This header and the current v2.3 sections **supersede older 'current' claims in the historical v2.2 material below**. Every dated prior claim remains useful as a record of what was known *then*, not as live source state. See exact 20 repository main SHAs, open PR candidates and limitations in the audit. No environment/account/PSP/carrier/legal/employee activation is created here.



**23 October 2026 — EA-DEV ACCEPTED by Platform Owner; published in merged Shared PR #373:** [EA-DEV implementation plan](ea-v2.3-development-enablement-implementation-plan-2026-10-23.md) establishes the authoritative DEV-00..DEV-15 implementation work queue to implement the Accepted ADR-SHARED-043 development route, including [headless engine onboarding](ea-dev-reusable-engine-onboarding-2026-10-23.md) for Pulse and Payments through IAM/CP, without requiring CMS. The programme is a **work queue, not runtime evidence**: CP #433 bootstrap source exists, while integrated seven-case INT-03C and fourteen-case NAB-03 runtime qualification remain unproven; Infrastructure #49 optional independent-development worksheet is not a standing development hold. Protected staging and production are independently gated. Update individual case statuses only with exact fresh evidence; the 20 October table below remains a dated baseline.

**23 October 2026 — EA-REL active release-delivery companion (NOT a protected go-live approval):** [EA-REL progressive production-release programme](ea-v2.3-progressive-production-release-programme-2026-10-23.md) defines **CP/IAM as the first candidate production foundation** with infrastructure/ops and separately witnessed staging and production evidence; other CMS/estate and headless engines may be added independently only with their exact tested provider/contract and tenant-market operation eligibility. All protected environment, statutory, provider, independent approver and live operations gates remain **NOT ACCEPTED** until actual evidence is recorded. The current dated gate table below is not silently overwritten by this planning note.

## 27 October 2026 — DEV-07 audit and corrective implementation

[The DEV-07 conformance audit](../assessments/trade/2026-10-27-dev07-workstream-conformance-audit.md)
records six actionable findings, exact inspected sources, retained failed runtime
receipts and the remaining owner-specific gaps. Corrections are in
[Trade #177](https://github.com/baobab-platform/baobab-trade/pull/177) and
[Infrastructure #66](https://github.com/baobab-platform/infrastructure/pull/66).
The first issuer-only repair did not qualify native buyer context. The corrected candidate now has all eight native buyer cases PASS in
Infrastructure run 40492142720, with independently hash-verified report bytes,
CP binding revocation, issuer cleanup and complete host teardown. Trade #177 and Infrastructure #66 subsequently merged after full final-head
CI/review; the corrective merge gate is closed. DEV-07/INT-05
remains PARTIAL/BLOCKED; the historical 16 PASS / 9 BLOCKED inventory remains
unchanged. Incomplete RFQ/quotation, BFF, buyer commit composition, ERP and
positive documentary providers are engineering dependencies, not a general
independent-human development approval hold.

## 24 October 2026 — DEV-00 decision and gate reconciliation

[DEV-00 precedence and CI policy](ea-dev-00-gate-reconciliation.md) is the single
reconciliation of isolated development, optional Infrastructure #49 and protected
staging/production gates. [The EA-DEV register](ea-dev-implementation-register.md)
tracks DEV-00..DEV-15 from a validated [JSON read model](ea-dev-implementation-register.json),
including owners, dependencies, exact inspected source/CI, observation dates,
blockers and next actions. DEV-00 source was subsequently merged through
[Shared #376](https://github.com/baobab-platform/shared/pull/376) at `e2acbed1` after
final-head CI and review. The current register now records that actual merge;
it does not promote runtime or protected acceptance.

Shared's named CMS development rows are ACTIVE; CP #433 is merged. Infrastructure
still has historical locks and a CMS gate that fails when OPEN. That is actionable
DEV-01/05 adapter adoption, not an independent-human development hold. No current
seven-case INT-03C or fourteen-case NAB-03 qualification was established by this
scoped source review. Other owners are explicitly NOT_ASSESSED where not checked.
Protected acceptance remains separate; earlier dated snapshots below are retained.

## 24 October 2026 — DEV-01 lifecycle accepted for its scoped Actions profile

[Infrastructure #53](https://github.com/baobab-platform/infrastructure/pull/53)
merged at `1445195e5304accaf38b29617dc223d12680cd03` after 33 successful checks
and 6 applicable skips. The final-head [actual lifecycle run](https://github.com/baobab-platform/infrastructure/actions/runs/40052631759)
proved native IAM setup, CP-owned five-profile bootstrap and replay, interrupted
start recovery, failed health/restoration, missing Compose state and expired
orphan cleanup. [Verified retained originals](evidence/dev01-2026-10-24/README.md)
keep the interrupted run incomplete and retain both verified teardown receipts.
The [EA-DEV register](ea-dev-implementation-register.md) now closes DEV-00 source
and DEV-01 lifecycle independently, with exact source/CI and bounded evidence.

This is an ordinary-development lifecycle slice, not the seven INT-03C or fourteen
NAB-03 qualification. It does not qualify Ory/federation, a domain provider,
protected staging, production or an independently observed interactive Codespace.
DEV-02 CP mandate/context variants are next, followed by DEV-03 authorisation.
The optional #49 packet remains separate; other safe engine work may proceed.

## v2.3 current gate decisions (20 October 2026)

| Item | Current verified assessment | Next exit and authority |
| --- | --- | --- |
| EA v2.3 programme | **ACCEPTED architecture**, active schedule only after Shared PR merge and mandatory checks | Shared Platform Owner; source/publication CI not runtime certification |
| EA-INT INT-01 | Frozen real-component synthetic Actions source qualification **PASS**; interactive Codespaces real run not independently observed | Infrastructure — same exact profile observed in Codespaces; new pins requalify |
| EA-INT INT-02 | Frozen real IAM/CP/Pulse synthetic Actions profile **PASS**, Infra #35 merged | IAM/CP/Pulse/Infrastructure — C4 protected native Ory and later source pins separate |
| **EA-INT INT-03** | **OPEN / P0 critical path**; real connected Nabhold BFF ↔ IAM ↔ CP ↔ CMS not accepted | Infrastructure #37, Nabhold #77 candidates; owner-positive AND negative L4/NAB receipts |
| EA-INT INT-04 | **OPEN**: Thamani is **Accepted B2B logistics** (ADR-THA-0018); TMS Foundation-0 | Thamani/TMS/Docs/Regulations — real sourced provider before commercial logistics claims |
| EA-INT INT-05/06 | **OPEN**: ZuriBeans B2B and Equator legacy estate have separately unproven source/legal/domain readiness | ZuriBeans/Trade/ERP/CP; Equator Foundation/identity/role migration |
| **EA-INT INT-07** | **OPEN mandatory** unrelated external API-only client with zero DigitalEstate | CP/IAM/Infra/provider current real-component synthetic profile |
| EA-INT INT-08 | **PARTIAL** domain-local financial and regulatory reference suites; platform L4 mesh unproven | Trade/ERP/Payments/Subscriptions/Docs/Regulations/Pulse owners |
| EA-R02 | **BLOCKED** on independently accepted founding legal cases, actual mandates, protected source/custody and current identity | CP/legal/IAM/Infrastructure |
| EA-R03 | **PARTIAL** native Trade/ERP/Payments source; deferred ERP bank/cash/other protected families still denied; PSP D2 missing | Domain PEP owners and independent financial/provider reviewers |
| FIN F1 | **PROPOSED** ADR-SHARED-033; DRAFT wire/source code is not accepted certified provider | Shared/ERP/Finance actual contract/GL and native acceptance |
| EA-BXS | **PARTIAL** Shared source/packages and first consumers; not blanket real browser/a11y/production acceptance | Shared Experience and each estate; published package and pinned consumer release |
| EA-ENG | **ADR-SHARED-041 Accepted globally**; repo-local ENG-01–05 rollout still open | All first-party repo owners / Shared Foundation; audit and proportionate evidence |
| EA-PRODUCT / People | ERP ADR-023 and PG17 defaults **PR #110 UNMERGED**; mandatory Gate D failed (permission denied / exit 126), no CDSoftware iDempiere13 runtime or statutory pack proof | ERP BP-00/01 then separate Shared People contracts and ZA/UG experts |
| EA-PRODUCT / TMS | Foundation-0, ADR-0001/0002 Accepted, ADR-0003..0019 Proposed; no running provider | TMS engineering; accepted tech, Shared contracts and source-backed tracking |
| EA-PRODUCT / SCF | Foundation-0, 35 Proposed ADRs, no operating licensed funder/bank | Conditional legal/funder viability; **not** R0/INT-03 prerequisite |
| EA-R05/06 and Gates D/E | **NOT ACCEPTED / PRODUCTION NOT AUTHORISED** | Actual protected AWS identity/secrets/data, official legal/PSP/vendor review, provider-specific certification, recovery and signed GO |

**At this source freeze:** 20 repositories discovered through organisation search; exact main baselines and a PR-state count of **81 open candidate PRs** are recorded in the v2.3 audit. Most are dependency/toolchain candidates. Open PR heads, even CI-green, are NOT merged code. No individual CI status is inferred here except where exact evidence is cited.

## v2.3 critical dependency order (current)

1. **INT-03**, with private real issued issuer/CP current Principal/tenant and qualified CMS/BFF, complete negative/revoke/failure/teardown; qualify in an actual selected synthetic lab before protected staging.
2. **Parallel EA-R02/R03** legal/mandate/official evidence and native Trade/ERP/payments authorisation; finance and Subscriptions/Docs provider/legal responsibility remain separate.
3. **INT-07** unrelated external API-only user with **zero** Baobab DigitalEstate.
4. **ENG-01/02/03 and BXS** exact published Shared package, consumer/browsers, CMS Node 24, Equator legacy links, engine-template and toolchain/data-upgrade risk.
5. **ERP BP-00/01** fix #110 runner failure then select CDSoftware source reuse/re-engineering path; **TMS Foundation** for Thamani B2B, other qualified customer profiles.
6. **EA-R05/R06** protected actually observed AWS source/provider/legal/certification and independently signed releases, once eligible.

No 'Africa compliant' or global production flag; admission remains tenant/legal actor/market/capability/provider/version scoped. Continue nondependent engineering while waiting for external protected credentials.

## Historical v2.2 live register — retained below as dated evidence, not active authority

**Governing plan:** [EA Implementation Plan v2.2](EA-implementation-plan-v2.2-ADR-SHARED-036-integration-reconciliation.md), **ACCEPTED 2026-10-15** under [ADR-SHARED-036](../adr/ADR-SHARED-036%20%E2%80%94%20Cross-Repository%20Integration%20Testing%2C%20Tenant-Neutral%20Consumption%20and%20Production%20Deployment.md) (**ACCEPTED**, Shared [#310](https://github.com/baobab-platform/shared/pull/310)). [EA v2.1](EA-implementation-plan-v2.1-ADR-BCP-026-027-reconciliation.md), Accepted 2026-10-13, remains the prior execution baseline with its substantive 026/027 decisions retained; [EA v2.0](../adr/Baobab%20Platform%20Enterprise%20Architecture%20Implementation%20Plan%20%E2%80%94%20Revised%202026-09-30.md) retains earlier unchanged workstream scope only.  
**Last updated:** **2026-10-18** — INT-02 Actions synthetic qualification accepted with verified final-pin evidence and teardown. INT-03 and an independently observed interactive Codespaces session remain open. Earlier dated checkpoints retain their historical scope.
**Source audit:** [EA v2.2 audit, 15 October 2026](ea-v2.2-evidence-audit-2026-10-15.md); [v2.1 audit](ea-v2.1-audit-2026-10-13.md) is a dated historical snapshot.  
**History:** [v2.0 dashboard, 4 October 2026](ea-dashboard-v2.0-historical-2026-10-04.md); v2.1 approval [Shared #301](https://github.com/baobab-platform/shared/pull/301); new v2.2 [integration matrix](ea-v2.2-integration-acceptance-matrix.md). Historical dashboards are not live status.

This page is the live register for every EA gate. The plan holds the reasoning.
Any PR that moves a gate updates its row here and records (v2.2 §§3, 9–11):
- commit
- contract pin
- migration ID
- test run
- approver
- unmet external dependencies
- rollback plan

## How to read this register

Each row retains v2.1's eight independent acceptance dimensions. **L4 real-component evidence is tracked independently in the EA-INT matrix below**; do not collapse L4 into Synth or Stag:

| Column | Meaning |
|---|---|
| **Arch** | Architecture accepted |
| **Contr** | Contracts converged |
| **Code** | Code merged |
| **DB** | Database migrated |
| **Synth** | Synthetic test passed |
| **Stag** | Protected staging passed |
| **Legal** | Independent legal/provider evidence accepted |
| **Ops** | Operational certification |

Values:

| Value | Meaning |
|---|---|
| **YES** | Done, with linked evidence |
| **PART** | Partial |
| **NO** | Not done |
| **EXT** | Blocked on an external dependency that cannot be produced in code |
| **N/A** | Not applicable to this row |

Rules:
- A YES or PART in any column except Arch needs evidence linked in its row; a column with no linked evidence is scored NO.
- Arch = YES for original v2.1 rows remains grounded in [S#301](https://github.com/baobab-platform/shared/pull/301) and CP accepted ADR-BCP-026/027. The **additional** EA-INT/production SaaS architecture is grounded in ADR-SHARED-036 Accepted via [Shared #310](https://github.com/baobab-platform/shared/pull/310) and the accepted v2.2 plan. This does NOT change Code/Synth/Stag/Legal/Ops scores.
- Synthetic CI or real-component L4 never sets Stag, Legal or Ops. A mandatory L4 BLOCKED is not a passed capability-specific pre-staging gate.
- *Merged* is not *proven*, *proven* is not *certified*, and nothing here is *production-permitted*.

**Important newer evidence:** [Payments #38](https://github.com/baobab-platform/baobab-payments/pull/38) and [CP #400](https://github.com/baobab-platform/baobab-cp/pull/400) were independently checked merged on main on 2026-10-15; [IAM #116](https://github.com/baobab-platform/baobab-iam/pull/116) checked OPEN, latest PR checks green. [Full 16-repo main and open PR/branch audit](ea-v2.2-evidence-audit-2026-10-15.md).

**Evidence provenance:**
- `S#NNN` links a PR in Shared, checked against Shared `main`.
- `CP #`, `Trade #`, `Trade Docs #`, `ERP #`, `Payments #` and `Subscriptions #` link PRs in the owning repository. Each one cited here was **verified merged on that repository's `main` on 2026-10-13**; citations added for P0-04B-04/05 (ERP #96, ERP #98, ERP #99, CP #393) were verified on 2026-10-14. A merged PR proves code and its CI, not the claims an owning record makes about live behaviour; those stay in the Stag, Legal and Ops columns.
- The CP [ADR-BCP-026/027 completion plan](https://github.com/baobab-platform/baobab-cp/blob/main/docs/reconciliation/adr026-027-completion-plan-2026-10-12.md) is the owning execution record for P0-01 to P0-05; this register summarises it and does not override it.

## Readiness summary

INT-02 was reconciled on 18 October 2026. Other rows retain their cited evidence dates.

```text
BAOBAB EA v2.2 READINESS                                   2026-10-18
──────────────────────────────────────────────────────────────────────
EA v2.2 plan                       ACCEPTED (2026-10-15; ADR-SHARED-036 accepted)
Backend development                SUBSTANTIAL (code merged; not proven live)
Public site ↔ Console code         INTEGRATED IN CODE (not live end-to-end certified)
Console production login           BLOCKED BY DESIGN (readAuthSettings rejects production)
Protected live E2E                 NOT DEMONSTRATED
Founding-group legal acceptance    OUTSTANDING (no independently accepted verification case)
P0-04A contract convergence        COMPLETE for current consumers (Trade, ERP, Payments, Subscriptions, Trade Docs)
P0-04B native execution PEPs       PART: Trade cart, ERP six classes, ERP-A purchase side (five classes) and ERP-B payables provenance/deny-by-name (engine-local real-CP harness) merged; Payments Gate D1 merged (#38; protected D2 open); remaining Trade/Subscriptions/Trade Docs, plus the deferred ERP families (bank/cash, inventory, costing; manufacturing in ERP-C), which stay denied by name and certified issuer/PSP acceptance
EA-INT/L4 reproducible integration  INT-01/02 REAL ACTIONS PROVEN; CODESPACES INTERACTIVE RUN NOT OBSERVED; INT-03–08 OPEN
DIGITAL ESTATE DEVELOPMENT         GATE B NOT PASSED
PRODUCTION ACTIVATION              NOT AUTHORISED
──────────────────────────────────────────────────────────────────────
```

## Programme gates A–E (retained from v2.1 §8; L4 prerequisite added by v2.2 §7)

| Gate | Arch | Contr | Code | DB | Synth | Stag | Legal | Ops | State and evidence |
|---|---|---|---|---|---|---|---|---|---|
| **A** Architecture/contract readiness | YES | YES | PART | PART | PART | NO | N/A | N/A | **Not passed.** v2.1 Accepted ([S#301](https://github.com/baobab-platform/shared/pull/301)). LA-01 contracts `5930dcf` and PEO-01 [S#274](https://github.com/baobab-platform/shared/pull/274), consumed by every owning engine through P0-04A: [Trade #145](https://github.com/baobab-platform/baobab-trade/pull/145), [ERP #95](https://github.com/baobab-platform/baobab-erp/pull/95), [Payments #36](https://github.com/baobab-platform/baobab-payments/pull/36), [Subscriptions #40](https://github.com/baobab-platform/baobab-subscriptions/pull/40), [Trade Docs #13](https://github.com/baobab-platform/baobab-trade-docs/pull/13). Organisation-first migration: [CP `c606b20`](https://github.com/baobab-platform/baobab-cp/commit/c606b20) (000102). Remaining: acceptance-owner compatibility sign-off of the final consumer inventory (LA-00/01) |
| **B** Platform developer unfreeze | YES | PART | PART | N/A | PART | NO | N/A | N/A | **Not passed.** Contracts, code and validators so far: LA-01 `5930dcf`, PEO-01 [S#274](https://github.com/baobab-platform/shared/pull/274). The unfreeze list covers Nabhold, ZuriBeans, Thamani and Equator & Estate Co. (v2.1 §8). It needs Gate A, plus proof that no estate frontend implements shadow authority (Thamani drift D-09) |
| **C** Controlled founding-group onboarding (non-production) | YES | PART | PART | PART | PART | NO | NO | N/A | **Not passed.** Truthful examples: [S#268](https://github.com/baobab-platform/shared/pull/268), [S#269](https://github.com/baobab-platform/shared/pull/269), [S#270](https://github.com/baobab-platform/shared/pull/270). CP machinery and synthetic four-tenant PostgreSQL qualification: [CP #339](https://github.com/baobab-platform/baobab-cp/pull/339) (migration 000120), [CP #340](https://github.com/baobab-platform/baobab-cp/pull/340), [CP #341](https://github.com/baobab-platform/baobab-cp/pull/341). No authentic, accepted business records exist (D-02) |
| **D** Capability-specific staging qualification (requires relevant L4 pass first) | YES | PART | PART | PART | PART | NO | EXT | NO | **Not passed** for any capability. Contracts: [S#264](https://github.com/baobab-platform/shared/pull/264), [S#300](https://github.com/baobab-platform/shared/pull/300). Code, migration and synthetic tests: [CP #382](https://github.com/baobab-platform/baobab-cp/pull/382), [CP #389](https://github.com/baobab-platform/baobab-cp/pull/389), [CP #390](https://github.com/baobab-platform/baobab-cp/pull/390), [Trade #146](https://github.com/baobab-platform/baobab-trade/pull/146), [Trade #147](https://github.com/baobab-platform/baobab-trade/pull/147), [Trade #148](https://github.com/baobab-platform/baobab-trade/pull/148), [ERP #95](https://github.com/baobab-platform/baobab-erp/pull/95), [Payments #36](https://github.com/baobab-platform/baobab-payments/pull/36), [Subscriptions #40](https://github.com/baobab-platform/baobab-subscriptions/pull/40). Protected staging qualification code: [CP #345](https://github.com/baobab-platform/baobab-cp/pull/345). Needs protected staging and certified providers (D-03, D-05) |
| **E** Production activation (EA-09B; unchanged signed approval) | YES | NO | NO | NO | NO | NO | EXT | NO | **Not authorised.** Needs real registry/PSP/KMS arrangements and a signed go/no-go (D-04, D-05) |

## EA workstreams

EA v2.0–v2.2 do not define EA-07 or EA-08 as workstreams like the others, so this register gives them no status. **EA-INT is newly established by Accepted v2.2 as a cross-cutting implementation workstream, not a capability or a substitute for EA-09B.**

| Stream | Arch | Contr | Code | DB | Synth | Stag | Legal | Ops | Assessment, evidence and gap |
|---|---|---|---|---|---|---|---|---|---|
| EA-01 Canonical contracts | YES | YES | YES | N/A | YES | NO | N/A | NO | **Implemented and converged for current consumers.** Shared CI validators on each contract PR (e.g. `5930dcf`, [S#283](https://github.com/baobab-platform/shared/pull/283)–[S#289](https://github.com/baobab-platform/shared/pull/289), [S#300](https://github.com/baobab-platform/shared/pull/300)). P0-04A owning-engine convergence: [Trade #145](https://github.com/baobab-platform/baobab-trade/pull/145), [ERP #95](https://github.com/baobab-platform/baobab-erp/pull/95), [Payments #36](https://github.com/baobab-platform/baobab-payments/pull/36), [Subscriptions #40](https://github.com/baobab-platform/baobab-subscriptions/pull/40), [Trade Docs #13](https://github.com/baobab-platform/baobab-trade-docs/pull/13). Gap: live semantic acceptance |
| EA-02 Capability catalogue and providers | YES | PART | PART | NO | PART | NO | EXT | NO | **Partial.** Payments merchant-readiness contract [S#264](https://github.com/baobab-platform/shared/pull/264). Gaps: real provider admission, active bindings, legal restrictions at runtime, certification per capability. Provider support stays simulated and `production_permitted: false` |
| EA-03 EngineRelease and topology | YES | YES | YES | PART | PART | NO | N/A | NO | **Substantial foundation.** ER-01 to ER-05 (see the [historical dashboard](ea-dashboard-v2.0-historical-2026-10-04.md)). Gaps: genuine release and deployment observations, reconciliation, protected failover |
| EA-04 IAM / workload identity | YES | YES | PART | N/A | PART | NO | N/A | NO | **Partial.** [IAM #116](https://github.com/baobab-platform/baobab-iam/pull/116) G04B-04 human-client/CP-audience changes remain OPEN (head 4ee06ef, five PR workflows green); **not in IAM main, not an active protected client**. [Nabhold #55](https://github.com/baobab-platform/nabhold/pull/55) confidential BFF source IS merged.  Scopes and staging identities defined: [S#251](https://github.com/baobab-platform/shared/pull/251), [S#265](https://github.com/baobab-platform/shared/pull/265), [S#278](https://github.com/baobab-platform/shared/pull/278), [S#279](https://github.com/baobab-platform/shared/pull/279), [S#281](https://github.com/baobab-platform/shared/pull/281). A scope definition creates no ACTIVE client or issued credential. Gaps: active scoped credentials, live revocation, acceptance of the issuer and federation |
| EA-05 CP governance | YES | YES | YES | PART | YES | NO | NO | NO | **Substantial.** Mandates LA-04C/D ([S#257](https://github.com/baobab-platform/shared/pull/257)–[S#260](https://github.com/baobab-platform/shared/pull/260)); sponsorship/deferral ([S#263](https://github.com/baobab-platform/shared/pull/263), [S#272](https://github.com/baobab-platform/shared/pull/272), [S#275](https://github.com/baobab-platform/shared/pull/275)); [CP #379](https://github.com/baobab-platform/baobab-cp/pull/379). Administrative grants stay `enforced: []`. Gaps: real founding-group decisions, external evidence, complete workbenches |
| EA-06 Event fabric | YES | YES | PART | NO | PART | NO | N/A | NO | **Partial.** Event registrations [S#259](https://github.com/baobab-platform/shared/pull/259), [S#272](https://github.com/baobab-platform/shared/pull/272). Gaps: proof of cross-engine replay, redaction, durable delivery and recovery |
| EA-09A Pre-deployment conformance | YES | PART | PART | N/A | PART | NO | EXT | N/A | **Partial.** Mandatory relevant L4 cross-engine profile acceptance is **not yet demonstrated**; [ADR-SHARED-036](../adr/ADR-SHARED-036%20%E2%80%94%20Cross-Repository%20Integration%20Testing%2C%20Tenant-Neutral%20Consumption%20and%20Production%20Deployment.md) Accepted establishes the architecture but not the runner. Contracts: [ADR-SHARED-026](../adr/ADR-SHARED-026%20%E2%80%94%20Cross-Repository%20Regulations%2C%20Trade%20Docs%20and%20Pulse%20Conformance%20Architecture.md) (cross-repository conformance) and [ADR-SHARED-032](../adr/ADR-SHARED-032%20%E2%80%94%20EA-09%20Provider%20Capability%20Certification%20and%20Pulse%20Activation%20Admission.md) (EA-09 certification and activation admission). Code and synthetic: Foundation G-FCI-1 enforcing on all 8 consumers and the rtd-conformance suite (`scripts/rtd_conformance.py`); see the [historical dashboard](ea-dashboard-v2.0-historical-2026-10-04.md). Gap: independent acceptance of security and providers across engines |
| EA-09B Operational certification | YES | NO | NO | NO | NO | NO | EXT | NO | **Not demonstrated.** Gaps: protected staging, external certification, signed go/no-go |
| EA-10 Observability | YES | PART | NO | N/A | NO | NO | N/A | NO | **Partial (contracts only).** Canonical correlation metadata: [ADR-0004](../adr/ADR-0004-canonical-cross-engine-metadata.md). No merged trace-correlation code or test is cited, so Code and Synth stay NO until one is linked. Gap: deployed trace correlation from admission through native transaction and recovery |
| EA-11 Recovery engineering | YES | PART | PART | PART | PART | NO | N/A | NO | **Partial.** Custody contracts [S#281](https://github.com/baobab-platform/shared/pull/281), [S#298](https://github.com/baobab-platform/shared/pull/298). Key rewrap, orphan recovery and migration 000124 in [CP #382](https://github.com/baobab-platform/baobab-cp/pull/382). Gap: live drills for backup/restore, key rotation, replay and rollback |
| EA-12 Console and Digital Estates | YES | YES | PART | N/A | PART | NO | N/A | NO | **Console substantial; estates uneven.** First-party Nabhold BFF is merged, but live IAM↔CP↔CMS is not accepted. **External API-only tenants MUST NOT require a Baobab-owned DigitalEstate**; test INT-07 before claiming external SaaS readiness. [CP #360](https://github.com/baobab-platform/baobab-cp/pull/360), [CP #377](https://github.com/baobab-platform/baobab-cp/pull/377), [CP #378](https://github.com/baobab-platform/baobab-cp/pull/378); CX-04/05 contracts [S#287](https://github.com/baobab-platform/shared/pull/287), [S#288](https://github.com/baobab-platform/shared/pull/288), [S#289](https://github.com/baobab-platform/shared/pull/289), [S#295](https://github.com/baobab-platform/shared/pull/295), [S#296](https://github.com/baobab-platform/shared/pull/296). Gaps: F-01 to F-07, Thamani drift (D-09) |
| EA-13 Regulatory architecture | YES | PART | PART | N/A | PART | NO | EXT | NO | **Substantial reference implementation.** Contracts: [ADR-SHARED-028](../adr/ADR-SHARED-028%20%E2%80%94%20Canonical%20Regulatory%20Decision%20Evaluation%20Contract.md), [S#276](https://github.com/baobab-platform/shared/pull/276), [S#277](https://github.com/baobab-platform/shared/pull/277). Code and synthetic: the cross-repository rtd-conformance suite ([ADR-SHARED-026](../adr/ADR-SHARED-026%20%E2%80%94%20Cross-Repository%20Regulations%2C%20Trade%20Docs%20and%20Pulse%20Conformance%20Architecture.md)). Gaps: accepted real requirement sources, trust, integration of runtime applicability |

## EA-INT — New v2.2 real-component integration workstream

**Architecture:** ADR-SHARED-036 Accepted and merged via [Shared #310](https://github.com/baobab-platform/shared/pull/310). **Programme plan:** v2.2 Accepted, this register. **Implementation:** INT-01 Foundation merged via [Infrastructure #34](https://github.com/baobab-platform/infrastructure/pull/34), main commit `09d3774fbcbcf08b190330429915a6f9393839e6`; [real L4-00 Actions suite](https://github.com/baobab-platform/infrastructure/actions/runs/38719421668) passed with pinned PostgreSQL/RabbitMQ/Redis images, mandatory L4-MAN-01–04, scrubbed receipt and cleanup. That INT-01 proof is distinct from the INT-02 IAM↔CP qualification recorded below; interactive Codespaces, protected staging and production acceptance remain open. L3 remains separate. [Audit source/branch assessment](ea-v2.2-evidence-audit-2026-10-15.md); [normative matrix](ea-v2.2-integration-acceptance-matrix.md).

| Workstream/gate | Arch | Contr | Code | DB | Synth | Stag | Legal | Ops | Evidence and remaining |
|---|---|---|---|---|---|---|---|---|---|
| **EA-INT / INT-01** Codespaces/Actions L4 runner | YES | PART | YES | N/A | YES | N/A | N/A | NO | [Infrastructure #34](https://github.com/baobab-platform/infrastructure/pull/34) merged (`09d3774`), [final-head Actions L4 real-process run](https://github.com/baobab-platform/infrastructure/actions/runs/38719421668) **PASS**; PostgreSQL, RabbitMQ and Redis image digests pinned, L4-MAN-01–04 and negative source checks green. **Codespaces interactive run not separately demonstrated**; INT-02 source/Actions qualification is recorded below, while INT-03 and remaining engine profiles stay open. No protected staging claimed. |
| **INT-02** IAM↔CP real-process tests | YES | YES | YES | N/A | YES | NO | N/A | NO | [Infrastructure #35](https://github.com/baobab-platform/infrastructure/pull/35) merged (`03ad3f488e19`); [final-pin run 39108198886](https://github.com/baobab-platform/infrastructure/actions/runs/39108198886) passes all five mandatory groups, actual governed Pulse qualification and teardown. [Verified receipt/pins](int02-pulse-qualification-register.md). Synthetic Actions source qualification only; protected staging and operational certification remain unaccepted. |
| **INT-03** Nabhold IAM/CP/BFF/CMS | YES | PART | NO | N/A | NO | NO | NO | NO | Existing Nabhold OIDC/TLS Redis/current-identity + smoke/receipt source is merged; IAM #116 dormant source merged. [19 October audit](nabhold-int03-dependency-audit-2026-10-19.md): IAM #126 repaired/reviewed/merged for C4-03E integrity-only verification and C4-04A observation; #127 subject-mapper/persistent-client repair and Infrastructure #36 private handoff source are reviewed/merged; #128 closes the two late #126 file-input findings after mandatory CI/review. No connected pinned BFF/CMS proof, protected native C4 acceptance or staging acceptance. |
| **INT-04** Thamani B2B/B2C logistics | YES | PART | NO | N/A | NO | NO | N/A | NO | Owner ADR B2B/B2C reconciliation and qualified services required before profile source acceptance. |
| **INT-05** ZuriBeans B2B | YES | PART | NO | N/A | NO | NO | N/A | NO | Buyer/supplier, corridor, quotations and relevant Trade/ERP providers need real integrated test. |
| **INT-06** Equator & Estate Co. | YES | PART | NO | N/A | NO | NO | EXT | NO | Domain capabilities and responsible actor to be qualified; no fabricated property/finance success. |
| **INT-07** EXTERNAL_CLIENT API-only, zero estate | YES | PART | NO | N/A | NO | NO | N/A | NO | Mandatory platform invariant. Real context/capability consumption by synthetic unrelated tenant with **zero DigitalEstate objects** unproven. |
| **INT-08** Finance/events/regulations mesh | YES | PART | NO | N/A | NO | NO | EXT | NO | Payments D1 merged; provider-specific L4 integration suite and authentic PSP/source qualification outstanding. |

### L4 evidence is a separate engineering gate, not protected staging

| Profile | Real selected components/fixture | L4 (actual multi-repo runner) | Protected staging | Relevant source proof |
|---|---|---|---|---|
| Core IAM↔CP | Real process/DB, synthetic scoped Principal/Tenant | NO | NO | CP/IAM own tests, no orchestrated E2E |
| Institutional Nabhold | Real IAM/CP/Nabhold BFF/CMS/TLS Redis | NO | NO | Nabhold #55 merged; IAM #116 OPEN |
| Thamani logistics | Identity/context, B2B/B2C provider and estate | NO | NO | Owner ADR/consumer work outstanding |
| ZuriBeans B2B | Buyer/supplier and actual provider instances | NO | NO | UI and providers individually tested |
| Equator property | Owner-approved real property capability and consumer | NO | NO | Source/role maturity pending |
| External API-only | EXTERNAL_CLIENT; zero estates; real approved provider | NO | NO | Accepted invariant, not implemented |
| Payments/ERP/event | Real CP/Payments/ERP, durable state and bus | NO | NO | Gate D1/D ERP local suites and the ERP-A/ERP-B real-CP harness (engine-local), no platform L4 |

## ADR-BCP-026 gates (progressive enterprise onboarding)

| Gate | Arch | Contr | Code | DB | Synth | Stag | Legal | Ops | Assessment, evidence and remaining |
|---|---|---|---|---|---|---|---|---|---|
| PEO-00/01 | YES | YES | PART | N/A | YES | NO | N/A | N/A | Architecture and contracts established ([S#274](https://github.com/baobab-platform/shared/pull/274), `596a0da`, `dd3777f`). Remaining: reconcile the programme and its evidence |
| PEO-02 | YES | YES | PART | NO | PART | NO | NO | NO | Sponsorship and the 24-month deferral ([S#263](https://github.com/baobab-platform/shared/pull/263), [S#272](https://github.com/baobab-platform/shared/pull/272), [S#273](https://github.com/baobab-platform/shared/pull/273), [S#275](https://github.com/baobab-platform/shared/pull/275)). Remaining: live approval, handling of expiry, acceptance of restriction release |
| PEO-03 (A–K) | YES | YES | PART | PART | PART | NO | EXT | NO | Scanner, custody and admission machinery: [S#276](https://github.com/baobab-platform/shared/pull/276)–[S#279](https://github.com/baobab-platform/shared/pull/279), [S#281](https://github.com/baobab-platform/shared/pull/281), [S#298](https://github.com/baobab-platform/shared/pull/298); [CP #380](https://github.com/baobab-platform/baobab-cp/pull/380), [CP #381](https://github.com/baobab-platform/baobab-cp/pull/381), [CP #382](https://github.com/baobab-platform/baobab-cp/pull/382). See PEO-03F and PEO-03K below |
| ↳ PEO-03F (incl. v2.1 proposed M criteria) | YES | YES | PART | N/A | PART | NO | EXT | NO | Certified official-source transport. Contracts and scopes: [S#276](https://github.com/baobab-platform/shared/pull/276) (CIPC/SARS observations), [S#278](https://github.com/baobab-platform/shared/pull/278) (non-authorising CIPC verifier scope and staging identity). Under decision 4 it also carries **independently certified government/PSP source and policy proof, with no synthetic approval or proxy CIPC verification**. Remaining: a genuinely certified external source |
| ↳ PEO-03K (incl. CP PEO-03L/L2) | YES | YES | PART | PART | PART | NO | EXT | NO | Custody and the candidate ledger. Contracts: [S#281](https://github.com/baobab-platform/shared/pull/281), [S#298](https://github.com/baobab-platform/shared/pull/298). CP's PEO-03L (independent scanner runtime, [CP #338](https://github.com/baobab-platform/baobab-cp/pull/338)) and PEO-03L2 (scanned-custody admission, [CP #380](https://github.com/baobab-platform/baobab-cp/pull/380)) belong to this family. Code, migration 000124 and S3 Object Lock/KMS integration: [CP #382](https://github.com/baobab-platform/baobab-cp/pull/382). Under decision 4 its staging criterion is **protected staging composition of scanner/token, custody/KMS, retention, destruction, redaction and operational negative tests**. Remaining: approved bucket/KMS deployed, scanner signer, operating retention policy |
| PEO-04 | YES | YES | PART | PART | PART | NO | NO | N/A | Contracts and truthful founding records: [S#252](https://github.com/baobab-platform/shared/pull/252), [S#266](https://github.com/baobab-platform/shared/pull/266), [S#269](https://github.com/baobab-platform/shared/pull/269), [S#270](https://github.com/baobab-platform/shared/pull/270). CP independent registration/control reconciliation and founding qualification: [CP #339](https://github.com/baobab-platform/baobab-cp/pull/339) (migration 000120), [CP #340](https://github.com/baobab-platform/baobab-cp/pull/340), [CP #341](https://github.com/baobab-platform/baobab-cp/pull/341). Remaining: four authentic, accepted business records (D-02) |
| PEO-05 | YES | PART | PART | N/A | PART | NO | EXT | NO | Contracts: [S#262](https://github.com/baobab-platform/shared/pull/262) (staging assessor registrations), [S#273](https://github.com/baobab-platform/shared/pull/273) (INTERNAL subscription authority). CP qualification gate, authority reader, IAM/provider readiness and protected-staging qualification code: [CP #342](https://github.com/baobab-platform/baobab-cp/pull/342), [CP #343](https://github.com/baobab-platform/baobab-cp/pull/343), [CP #344](https://github.com/baobab-platform/baobab-cp/pull/344), [CP #345](https://github.com/baobab-platform/baobab-cp/pull/345). Remaining: protected acceptance of IAM, subscription, provider and tenant |
| PEO-06 | YES | YES | PART | N/A | PART | NO | N/A | NO | Contracts: [S#283](https://github.com/baobab-platform/shared/pull/283)–[S#289](https://github.com/baobab-platform/shared/pull/289), [S#295](https://github.com/baobab-platform/shared/pull/295). Applicant, reviewer and Console: [CP #360](https://github.com/baobab-platform/baobab-cp/pull/360), [CP #377](https://github.com/baobab-platform/baobab-cp/pull/377), [CP #378](https://github.com/baobab-platform/baobab-cp/pull/378). Remaining: guided evidence UX (F-04), browser security and accessibility (F-05) |
| PEO-07 | YES | N/A | NO | NO | NO | NO | EXT | NO | Criteria defined. Remaining: signed production-readiness decisions |

## ADR-BCP-027 gates (Organisation-first tenancy and legal actor)

| Gate | Arch | Contr | Code | DB | Synth | Stag | Legal | Ops | Assessment, evidence and remaining |
|---|---|---|---|---|---|---|---|---|---|
| LA-00/01 | YES | YES | YES | N/A | YES | NO | N/A | N/A | Canonical model and contracts (`5930dcf`), consumed by every owning engine through P0-04A: [Trade #145](https://github.com/baobab-platform/baobab-trade/pull/145), [ERP #95](https://github.com/baobab-platform/baobab-erp/pull/95), [Payments #36](https://github.com/baobab-platform/baobab-payments/pull/36), [Subscriptions #40](https://github.com/baobab-platform/baobab-subscriptions/pull/40), [Trade Docs #13](https://github.com/baobab-platform/baobab-trade-docs/pull/13). Remaining: acceptance-owner compatibility sign-off |
| LA-02 | YES | YES | PART | PART | PART | NO | N/A | NO | Nullable legal entity and PRIMARY mapping: contracts and validators `5930dcf`; CP database and Go compatibility [CP `c606b20`](https://github.com/baobab-platform/baobab-cp/commit/c606b20) (migration 000102). Remaining: migration of real data, proof for legacy consumers, rollback |
| LA-03 | YES | YES | PART | PART | PART | NO | NO | N/A | Contract: `5930dcf` (`tenant-registration.schema.json`, `pre-tenant-admission.schema.json`). CP governed registration: [CP #294](https://github.com/baobab-platform/baobab-cp/pull/294) (migration 000103, API and service tests). Remaining: execution accepted for the four founding businesses |
| LA-04 | YES | YES | PART | PART | PART | NO | NO | NO | Mandates, independent decisions, lifecycle and readback: [S#257](https://github.com/baobab-platform/shared/pull/257)–[S#260](https://github.com/baobab-platform/shared/pull/260), [S#287](https://github.com/baobab-platform/shared/pull/287), [S#297](https://github.com/baobab-platform/shared/pull/297); [CP #379](https://github.com/baobab-platform/baobab-cp/pull/379). Remaining: authentic mandates, human authority decisions |
| LA-05 | YES | YES | PART | PART | PART | NO | EXT | NO | Engine policy and contract guards: [S#261](https://github.com/baobab-platform/shared/pull/261), [S#262](https://github.com/baobab-platform/shared/pull/262), [S#264](https://github.com/baobab-platform/shared/pull/264), [S#282](https://github.com/baobab-platform/shared/pull/282), [S#300](https://github.com/baobab-platform/shared/pull/300). P0-04B-01/02 Trade binding lifecycle, authenticated intake and CP-owned activation with native PostgreSQL 17/Medusa proof: [Trade #146](https://github.com/baobab-platform/baobab-trade/pull/146), [Trade #147](https://github.com/baobab-platform/baobab-trade/pull/147), [Trade #148](https://github.com/baobab-platform/baobab-trade/pull/148), [CP #389](https://github.com/baobab-platform/baobab-cp/pull/389), [CP #390](https://github.com/baobab-platform/baobab-cp/pull/390). P0-04B-03 cart-completion COMMIT fence for activated bindings (single consumption, revocation, lease expiry, replay, compensation; real completeCartWorkflow acceptance on PostgreSQL 17): [Trade #149](https://github.com/baobab-platform/baobab-trade/pull/149), receipt [CP #392](https://github.com/baobab-platform/baobab-cp/pull/392). P0-04B-04 ERP posting authority (ADR-SHARED-034, ADR-ERP-022): `erp/v2` contract [S#304](https://github.com/baobab-platform/shared/pull/304), [S#306](https://github.com/baobab-platform/shared/pull/306); CP resolver with immutable decision history [CP #393](https://github.com/baobab-platform/baobab-cp/pull/393) (migration 000125); ERP native placement, provenance, attribution and COMMIT fences [ERP #96](https://github.com/baobab-platform/baobab-erp/pull/96) (Gate B); real iDempiere 13/PostgreSQL Gate D [ERP #98](https://github.com/baobab-platform/baobab-erp/pull/98), [CI run 38560332080](https://github.com/baobab-platform/baobab-erp/actions/runs/38560332080) (19/19 against a synthetic CP: valid, eight denial modes, unplaced org, injected failure, concurrency, retry, background repost, direct-SQL bypass), which also fixed a JVM veto that never fired for a real `AD_Client`; receipt CP completion plan §14. P0-04B-05 [ERP #99](https://github.com/baobab-platform/baobab-erp/pull/99): receipts-only payments and sales-only allocations (closing an outbound-payment authorisation gap), shipment costing derived from the shipment's own authority, N0005 COMMIT fences; Gate D [CI run 38603012390](https://github.com/baobab-platform/baobab-erp/actions/runs/38603012390) 60/60 across order, shipment, invoice, receipt and allocation; receipt CP completion plan §15. P0-04B-06 Payments money-movement authority (ADR-SHARED-035): `payments/v2` contract [S#309](https://github.com/baobab-platform/shared/pull/309); CP resolver [CP #400](https://github.com/baobab-platform/baobab-cp/pull/400) (migration 000126); one Payments PEP for authorisation, capture, void and refund with payout fail-closed [Payments #37](https://github.com/baobab-platform/baobab-payments/pull/37); Payments-local D1 (real-component, synthetic data, deterministic PSP behind real HyperSwitch; **not EA Gate D, not L4**) [Payments #38](https://github.com/baobab-platform/baobab-payments/pull/38), [CI run 38688158345](https://github.com/baobab-platform/baobab-payments/actions/runs/38688158345) 16/16; receipt CP completion plan §16 ([CP #401](https://github.com/baobab-platform/baobab-cp/pull/401)). EA-R03 ERP-A (ADR-SHARED-037): five purchase-side and vendor-payment *recording* classes in `erp/v2` catalogue version 2 [S#314](https://github.com/baobab-platform/shared/pull/314); CP resolver [CP #402](https://github.com/baobab-platform/baobab-cp/pull/402); ERP N0006 classification, matching fences, allocation side and client binding, with payment selection, online payment, vendor return and AP credit memo denied by name [ERP #100](https://github.com/baobab-platform/baobab-erp/pull/100); N0007 purchase costing as derived writes plus an engine-local harness (real iDempiere 13, the real CP binary at `0337632`, RS256 workload tokens, PostgreSQL 17; synthetic data; **not EA Gate D, not L4**) [ERP #101](https://github.com/baobab-platform/baobab-erp/pull/101), [CI run 38764952997](https://github.com/baobab-platform/baobab-erp/actions/runs/38764952997) 28/28 (recording flow and costing, deny-by-name routes, direct-SQL bypass, SIGKILL before COMMIT, lease expiry, revocation, narrower mandate, CP unavailable, every attribution cross-checked against CP decision history); receipt CP completion plan §17. **ERP-A register receipt (v2.2 §10):** *Commits:* Shared `756edb410fdfb29c8b90bcc388a69412b4b5b7b1` (#314); CP `0337632756dea1bd99db098d02e71d8a170027f2` (#402); ERP `eea712e49ba218fd1779c379fb6bde3c2e12c228` (#100) and `6775294a7560e7a67b37a28e951f0c24ab3bb0ab` (#101, tested head `abf7094`). *Contract pin:* `erp/v2` catalogue version 2 at Shared `756edb4`, pinned in CP `contracts.lock.yaml` and ERP `contracts.lock.yaml`. *Migrations:* ERP native `N0006_purchase_side_recording` and `N0007_purchase_costing`; CP reuses 000125, with no new migration. *CI:* ERP #101 [run 38764952997](https://github.com/baobab-platform/baobab-erp/actions/runs/38764952997) (Gate B 33/33, synthetic Gate D, real-CP harness 28/28, artifact `11989645446`). *Approver:* merged under the owner's standing authorisation to merge when CI passes and the implementation is satisfactory, after Codex and bot review threads were resolved. There was no separate per-PR human approval. *Unmet live dependencies:* real placements (named maker and checker), real mandates, real IAM (not the test issuer), INT-01 L4 (deferred), protected staging, and Gate E. *Rollback:* Immediate fail-closed stop: unset `ERP_POSTING_AUTHORITY_ENABLED` in CP. The ERP PEP refuses any non-200 CP answer, so every governed native write is then refused (fail-closed; harness S24 covers CP being unreachable). Code: revert ERP #101/#100, then add a forward native migration that restores the N0005 `cost_detail_commit_fence`, `derived_write_insert_guard` and `root_table` CHECK. N0006/N0007 are forward-only, so no down migration is run. Contract: revert CP's pin to catalogue version 1 (`92541c9`); the version-2 classes are then uncatalogued and denied. EA-R03 ERP-B (ADR-SHARED-038, owner decision 2026-10-16): catalogue frozen at version 2; `erp/v2` payment-execution evidence [S#316](https://github.com/baobab-platform/shared/pull/316); ERP N0008 binds every recorded vendor payment to exactly one independently verified execution-evidence record (client, org, payee, currency, amount, vendor-invoice obligation; re-checked at COMMIT; ingest role only, never a superuser or iDempiere; append-only; authority `SYNTHETIC_ENGINE_LOCAL` only, so non-activatable for real placements), allocates it only to its obligation, and refuses bank statements, cash journals, inventory, movement, production and landed cost by name in the JVM and PostgreSQL [ERP #102](https://github.com/baobab-platform/baobab-erp/pull/102); harness [CI run 38871808398](https://github.com/baobab-platform/baobab-erp/actions/runs/38871808398) 38/38 (S01–S26, B01–B11; **not EA Gate D, not L4**); no CP change; receipt CP completion plan §18. **ERP-B register receipt (v2.2 §10):** *Commits:* Shared `e1da44e90903ab7f6fe9a9060604f9bff2f13666` (#316); ERP `0bcf6d1b9d0ec262a1400eb9ce83981305e5d32d` (#102, tested head `04a2f4a`); CP unchanged at `0337632`. *Contract pin:* ERP `contracts.lock.yaml` at Shared `e1da44e`; CP stays at `756edb4` (consumes nothing that changed). *Migrations:* ERP native `N0008_payables_provenance_and_deny_by_name`; no CP migration. *CI:* ERP #102 run 38871808398 (Gate B 37/37, synthetic Gate D, real-CP harness 38/38, artifact `12033549406`). *Approver:* the owner's standing merge authorisation after review threads were resolved; no separate per-PR human approval. *Unmet live dependencies:* a real execution authority (Payments payout, ADR-SHARED-035), real placements, mandates and IAM, INT-01 L4 (deferred), protected staging, Gate E. *Rollback:* unset `ERP_POSTING_AUTHORITY_ENABLED` (fail-closed); revert ERP #102 with a forward migration restoring the N0006 functions; ERP re-pins `756edb4`. Remaining: **P0-04B** Trade full order/payment execution; bank reconciliation, cash management, inventory and costing increments and manufacturing (ERP-C) stay denied by name; vendor disbursement stays denied; Payments D2 protected PSP qualification and payout; Subscriptions/Trade Docs execution points; issuer/PSP identity (D-03) Trade-A TA-05 central PEP/receipts: [17 October independent source receipt](ea-r03-trade-a-ta05-source-2026-10-17.md); TA-06 entry-point wiring, TA-07 native COMMIT/bypass closure and TA-08 acceptance remain. |
| LA-06 | YES | YES | PART | NO | PART | NO | NO | N/A | Contract examples separating synthetic and real businesses: [S#270](https://github.com/baobab-platform/shared/pull/270). CP synthetic founding qualification and correlation: [CP #340](https://github.com/baobab-platform/baobab-cp/pull/340), [CP #341](https://github.com/baobab-platform/baobab-cp/pull/341). Remaining: real records, evidence, independent approval |
| LA-07 | YES | PART | PART | NO | PART | NO | NO | NO | Read-only mandate scope and readback, with validators: [S#287](https://github.com/baobab-platform/shared/pull/287), [S#297](https://github.com/baobab-platform/shared/pull/297); [CP #379](https://github.com/baobab-platform/baobab-cp/pull/379). Historical financial attribution, ERP GL journals and the sales flow ([ERP #99](https://github.com/baobab-platform/baobab-erp/pull/99), with derived costing rows bound to the root decision): every governed posting stores the CP `decision_id`, mandate lineage, placement and Finance baseline in the same transaction, and CP keeps the decision immutably ([CP #393](https://github.com/baobab-platform/baobab-cp/pull/393), [ERP #96](https://github.com/baobab-platform/baobab-erp/pull/96)); Gate D asserts the rows on real iDempiere ([ERP #98](https://github.com/baobab-platform/baobab-erp/pull/98)). No cutover migration is cited, so DB stays NO. Remaining: operational cutover, attribution for the other engines, recovery |

## Founding-group truth table

These are declared business positions, not verified registry facts (v2.1 §3).

| Business | Canonical operating treatment | Independently accepted? | Still required |
|---|---|---|---|
| Nabhold Group Africa | Its own Organisation and Tenant; a potential scoped legal actor | **NO.** [S#252](https://github.com/baobab-platform/shared/pull/252) is a documentary CIPC reference, and examples stay `UNVERIFIED` ([S#269](https://github.com/baobab-platform/shared/pull/269)) | A verification case accepted in CP; any authority to act for another business |
| Thamani Global | An independent incorporated business and Tenant | **NO.** [S#266](https://github.com/baobab-platform/shared/pull/266) is a documentary CIPC reference | Its own official registration; separate proof of group control |
| ZuriBeans | An independent Organisation and Tenant, with no fictional incorporation ([S#270](https://github.com/baobab-platform/shared/pull/270)) | N/A (unincorporated) | A scope-specific authorised legal actor for each activity that needs one |
| Equator & Estate Co. | An independent Organisation and Tenant, with no fictional incorporation | N/A (unincorporated) | Real legal responsibility for property, construction and other relevant activities |

Ownership alone never lets Nabhold act as issuer, seller, importer or contracting actor for ZuriBeans or Equator. Each role needs its own accepted mandate.

## Preserved v2.1 §11 decisions (historical approval, still binding)

All five v2.1 decisions were approved on **2026-10-13** by the **platform owner** (the repository owner). The approval is recorded in [S#301](https://github.com/baobab-platform/shared/pull/301), the EA-R01 change that accepted v2.1.

| # | Decision | Outcome |
|---:|---|---|
| 1 | ADR-BCP-026/027 amend and extend EA v2.0; unchanged v2.0 workstreams and the no-premature-production premise are retained | **Approved** |
| 2 | Separate gate sequence and four distinct readiness decisions (§6); no global verified legal status | **Approved** |
| 3 | Founding-group 24-month deferral, truthful legal-entity posture, Option B autonomy, scope-bound Nabhold mandates, independent external verification | **Approved** |
| 4 | PEO-03L/M labels | **Remapped:** v2.1's proposed L criteria become the staging-acceptance criterion of PEO-03K; its proposed M criteria become the certification criterion of PEO-03F. No ADR, registry key or contract is created. **Naming (2026-10-13):** the label PEO-03L follows CP, where it names the scanner runtime ({CP(338)}) and PEO-03L2 the scanned-custody admission, both in the PEO-03K family |
| 5 | Cross-repository acceptance owners | **Approved:** see below |

## Acceptance owners (decision 5)

Only the owning authority may publish a production-support claim for its repository.

| Repository | Acceptance owner |
|---|---|
| baobab-cp, baobab-iam, shared, baobab-subscriptions, baobab-erp, baobab-trade, baobab-payments, Infrastructure | Platform owner, until delegated in writing in this register |

## Drift and gap register

| ID | Finding | Severity | Owner repo | State |
|---|---|---|---|---|
| D-01 | EA v2.1 proposed; dashboard on v2.0 | P0 Governance | shared | **Closed (2026-10-13):** v2.1 Accepted and this register published; cross-repository evidence verified merged on each owning `main` |
| D-02 | Genuine founding-company and group-control evidence not accepted | P0 Authority | baobab-cp | Open |
| D-03 | P0-04B native bypass closure incomplete | P0 Financial/legal | Trade, ERP, Payments, Subscriptions, Trade Docs | PART; **Payments D1 now merged via [Payments #38](https://github.com/baobab-platform/baobab-payments/pull/38), CP resolver [CP #400](https://github.com/baobab-platform/baobab-cp/pull/400); D2 protected/real PSP NOT passed**. P0-04B-01/02/03 merged ([S#300](https://github.com/baobab-platform/shared/pull/300), [Trade #146](https://github.com/baobab-platform/baobab-trade/pull/146), [Trade #147](https://github.com/baobab-platform/baobab-trade/pull/147), [Trade #148](https://github.com/baobab-platform/baobab-trade/pull/148), [CP #389](https://github.com/baobab-platform/baobab-cp/pull/389), [CP #390](https://github.com/baobab-platform/baobab-cp/pull/390)), [Trade #149](https://github.com/baobab-platform/baobab-trade/pull/149)); P0-04B-04 ERP posting authority merged ([S#304](https://github.com/baobab-platform/shared/pull/304), [CP #393](https://github.com/baobab-platform/baobab-cp/pull/393), [ERP #96](https://github.com/baobab-platform/baobab-erp/pull/96), [ERP #98](https://github.com/baobab-platform/baobab-erp/pull/98)), ERP's local native Gate D proof passed for GL journals (NOT EA protected Gate D); P0-04B-05 [ERP #99](https://github.com/baobab-platform/baobab-erp/pull/99) local native Gate D passed for six currently catalogued ERP classes (**NOT protected EA Gate D**); EA-R03 ERP-A purchase side and vendor-payment recording merged ([S#314](https://github.com/baobab-platform/shared/pull/314), [CP #402](https://github.com/baobab-platform/baobab-cp/pull/402), [ERP #100](https://github.com/baobab-platform/baobab-erp/pull/100), [ERP #101](https://github.com/baobab-platform/baobab-erp/pull/101)), with an engine-local real-CP harness passing 28/28 (**NOT EA Gate D, NOT L4**); EA-R03 ERP-B payables provenance and deny-by-name merged ([S#316](https://github.com/baobab-platform/shared/pull/316), [ERP #102](https://github.com/baobab-platform/baobab-erp/pull/102); harness 38/38, **NOT EA Gate D, NOT L4**); still open: Trade full order/payment execution, bank/cash, inventory and costing increments (denied by name), vendor disbursement (denied), **Payments D2 protected PSP qualification**, Subscriptions and Trade Docs execution paths |
| D-04 | Console production authentication deliberately disabled | P0 Go-live | baobab-cp | Open (by design until security-approved) |
| D-05 | No certification of scanner/custody as deployed | P0 Evidence | baobab-cp, Infrastructure | Open |
| D-06 | Public registration and login deep-link journey incomplete | P1 UX | baobab-cp, baobab-iam | Open (F-01, F-02) |
| D-07 | Independent Console workbenches incomplete | P1 Workflow | baobab-cp | Open (F-03, F-04; CX-06–10) |
| D-08 | No acceptance for protected browser, dataset lifecycle or performance | P1 Assurance | baobab-cp | Open (F-05) |
| D-09 | EA-12 estates uneven; Thamani legacy storefront routes | P1 Product | thamani and estates | Open |
| D-10 | Public website publication and documentation governance incomplete | P1 Publication | baobab-cp | Open (F-06, F-07) |
| **D-11** | Remaining L4 orchestration and consumption profiles | P0 Integration | Infrastructure, Shared, engines | PARTIAL. INT-01 and INT-02 Actions proof are merged; [INT-02 receipt/pins](int02-pulse-qualification-register.md) establish actual IAM/CP/Pulse source qualification. Interactive Codespaces invocation, INT-03 and the remaining engine/consumer profiles stay open. |
| **D-12** | IAM Nabhold CP human profile awaiting PR merge and protected identity proof | P0 IAM | baobab-iam, baobab-cp, Nabhold | PARTIAL. [IAM #116](https://github.com/baobab-platform/baobab-iam/pull/116) **merged** (`49aa42c`) after five workflows passed; dormant client and protected observer in source. No real Principal/client activation, approved secrets or protected login. |
| **D-13** | External tenant with zero Digital Estate not demonstrated | P0 SaaS | CP, IAM, Infrastructure, Shared | OPEN. Mandatory INT-07; no placeholder estate |
| **D-14** | Thamani B2B/B2C clarified requirement inconsistent with earlier B2B-only owner ADR | P1 Consumer | thamani | OPEN; reconcile owner ADR, then business integration profile |
| **D-15** | Legacy Infrastructure integrated-testing branch has L4=staging nomenclature and diverges from accepted ADR | P1 Consistency | Infrastructure | OPEN; selectively reuse against current main and ADR-SHARED-036 |
| **D-16** | Major open Node/TypeScript/GraphQL/Playwright dependency branches may not match approved runtime matrix | P1 Toolchain | Affected repos | OPEN; never treat bot candidate version as certified runtime, pin exact tested candidates |

### Frontend gaps (baobab-cp)

All open. Details are in [audit §6](ea-v2.1-audit-2026-10-13.md#6-landing-page-and-console).

| ID | Gap |
|---|---|
| F-01 | Safe post-login deep-link return. The callback always redirects to `/workspace` |
| F-02 | IAM-owned enrolment or invitation for new applicants |
| F-03 | Role-aware navigation for every independent authority persona |
| F-04 | Guided, business-language transitions in place of hand-typed identifiers |
| F-05 | Real frontend acceptance: provider login, sessions, revocation, accessibility, CSRF, cross-tenant |
| F-06 | Public website publication: ownership, domain, legal notices, indexing |
| F-07 | Stale CP documentation (`cx05e-governed-datasets.md`, README snapshot) |

## Execution order (Accepted EA v2.2)

The 13 October execution order remains a **historical sequence**. The accepted v2.2 adds an Infrastructure-owned engineering lane that runs **in parallel** with legal/evidence and source-PEP work.

| Position | Item | Current status |
|---|---|---|
| EA-R00 | Accept v2.2 plan, L4 test matrix and dashboard | Source changes in this Shared PR; Accepted plan, no deployment |
| **INT-01** | Infrastructure Codespaces + Actions reproducible harness | **MERGED, real Actions L4-00 PASS** ([Infra #34](https://github.com/baobab-platform/infrastructure/pull/34)); actual Codespaces proof not demonstrated |
| EA-R02 | Genuine founding/legal evidence, custody, source and mandates | In progress; real external approvals/infra dependencies |
| EA-R03 | Complete current native PEP operation families | PART; **Payments D1 merged**; **ERP-A and ERP-B merged** (engine-local real-CP harness, not EA Gate D, not L4); Payments D2, Trade, Subscriptions and Trade Docs remaining, plus the deferred ERP families (bank/cash, inventory, costing; manufacturing in ERP-C), which stay denied by name Trade-A TA-05 central PEP/receipts: [17 October independent source receipt](ea-r03-trade-a-ta05-source-2026-10-17.md); TA-06 entry-point wiring, TA-07 native COMMIT/bypass closure and TA-08 acceptance remain. |
| **INT-02** | IAM↔CP real-component issued token/context/denial | Demonstrated for the [final-pin synthetic Actions run](https://github.com/baobab-platform/infrastructure/actions/runs/39108198886); all five mandatory groups, provider qualification and teardown PASS. INT-03 and protected acceptance remain separate. |
| **INT-03** | Nabhold↔IAM↔CP↔CMS full browser/content pilot | Not demonstrated; IAM #116 merged as dormant source, real connected profile missing |
| EA-R04 | Console and estate UX/no-shadow-authority completion | Partial; real end-to-end acceptance missing |
| **INT-04/05/07** | Thamani, ZuriBeans, EXTERNAL_CLIENT with no DigitalEstate | Not demonstrated; owner business ADR and provider readiness |
| **INT-06/08** | Equator and selective finance/event/Regulations mesh | Not demonstrated; domain readiness gates |
| EA-R05 | Protected staging, legal/source/PSP/provider E2E | EXTERNAL DEPENDENCY; no protected GO |
| EA-R06 | Public/operational certification and production authorisation | NOT AUTHORISED |

**Separation:** L4 pass on actual processes with synthetic humans/legal actors is a prerequisite to later protected capability qualification. It does not convert a founding identity to VERIFIED or authorise a real financial instruction. Gate A–E are retained (v2.2 §7).

### Retained previous v2.1 execution order (historical, not the active queue)

### Execution order (audit §9)

| # | Item | State |
|---:|---|---|
| EA-R01 | Reconcile architecture and governance | **Done (2026-10-13)**, including cross-repository evidence verification |
| EA-R02 | Founding legal/evidence acceptance foundation | In progress. CP machinery merged ([CP #339](https://github.com/baobab-platform/baobab-cp/pull/339)–[CP #345](https://github.com/baobab-platform/baobab-cp/pull/345)). Open and actionable: integrate the scanner and custody with approved infrastructure (bucket/KMS deployment, scanner signer, operating retention policy; see PEO-03K). Externally blocked: authentic Nabhold/Thamani records, corporate-control decisions and mandates (EXT) |
| EA-R03 | Complete P0-04A and P0-04B native PEPs | P0-04A complete; P0-04B-01/02/03 merged (Trade, [Trade #149](https://github.com/baobab-platform/baobab-trade/pull/149)); P0-04B-04/05 ERP posting authority merged with Gate D passed for all six catalogued classes ([ERP #98](https://github.com/baobab-platform/baobab-erp/pull/98), [ERP #99](https://github.com/baobab-platform/baobab-erp/pull/99)); as of the historical audit the next tasks were Payments, Subscriptions and Trade Docs; **Payments Gate D1 was subsequently merged on 15 October via #38; D2 remains open**. ERP-A purchase-side and vendor-payment recording classes were subsequently merged on 15 October ([S#314](https://github.com/baobab-platform/shared/pull/314), [CP #402](https://github.com/baobab-platform/baobab-cp/pull/402), [ERP #100](https://github.com/baobab-platform/baobab-erp/pull/100), [ERP #101](https://github.com/baobab-platform/baobab-erp/pull/101); engine-local, not EA Gate D, not L4); ERP-B and Trade full order/payment execution remain open Trade-A TA-05 central PEP/receipts: [17 October independent source receipt](ea-r03-trade-a-ta05-source-2026-10-17.md); TA-06 entry-point wiring, TA-07 native COMMIT/bypass closure and TA-08 acceptance remain. |
| EA-R04 | Close frontend and Console integration | Not started |
| EA-R05 | Protected staging and E2E acceptance (audit §10 matrix) | Not started; needs EXT infrastructure |
| EA-R06 | Publication and operational certification | Not started |

Code increments may run in parallel. Production activation stays gated on its dependencies.


## 16 October 2026 — verified cross-repository implementation delta

This section supersedes stale PR-status claims in the historical 15 October audit **only where the following live PR metadata was checked**. It does not turn merged source into L4 qualification or protected admission.

| Work | Current evidence | Readiness consequence |
|---|---|---|
| INT-01 L4-00 | [Infrastructure #34](https://github.com/baobab-platform/infrastructure/pull/34) MERGED | Infrastructure foundation source and Actions proof; a Codespaces live execution remains separately required |
| Human CP-audience profile | [IAM #116](https://github.com/baobab-platform/baobab-iam/pull/116) MERGED | Dormant, no approved user, secret or protected executive admission |
| Nabhold G04B-04 | [Nabhold #57](https://github.com/baobab-platform/nabhold/pull/57) MERGED | Fail-closed source guard; concrete accepted CP adapter and INT-03 not complete |
| INT-02 L4-01 | [Infrastructure #35](https://github.com/baobab-platform/infrastructure/pull/35) OPEN — mandatory acceptance blocked | Real IAM↔CP tests still lack complete required passing receipts; cannot merge on static CI |
| Trade-0 | [Shared #318](https://github.com/baobab-platform/shared/pull/318), [CP #405](https://github.com/baobab-platform/baobab-cp/pull/405) MERGED | Versioned CP Seller Operating Binding/resolver source; Trade-A through D and real L4 remain |
| Finance F1 | [ADR-SHARED-033](../adr/ADR-SHARED-033%20%E2%80%94%20Corporate%20Finance%20Capability%20Namespace%20and%20First%20Canonical%20Finance%20Tranches.md) PROPOSED | Keys not registered, no provider certification; F1 contract design may proceed behind steward/ERP approval |

**Gate delta:** EA-INT INT-01 source progressed, INT-02 remains BLOCKED for acceptance, INT-03 NOT PROVEN. EA Gate D/E and production remain NOT AUTHORISED. EA-R03 continues in parallel: Trade-A/D, ERP remaining native coverage, Payments D2, Subscriptions and Trade Docs native execution paths. Do not infer actual legal-actor mandates, issuer grants, merchant PSP credentials or CMS bindings from the above.


**16 October engineering checkpoint:** Finance F1 schema work is independent
of Infrastructure #35. Its review-only PR #319 and canonical DRAFT PR #321
are separate from provider implementation, live iDempiere, protected L4 and
activation. Infrastructure #35 at `0f6cbac` has real L4-IAM-02 PASS, while
L4-IAM-01 and L4-CP-01/02/03 remain BLOCKED; the overall profile still fails.
No EA Gate D/E or Nabhold release is promoted by the isolated workload proof.


## 16 October 2026 — independent Finance F1 source checkpoint

Finance F1 source work proceeds independently of Infrastructure #35 under the
sponsor's clarified execution instruction. Design checkpoint Shared #319 is
merged (`27eb77a`). Shared #321 publishes the separately reviewed DRAFT wire
tranche: three DRAFT/EXPERIMENTAL vocabulary entries, six schemas/common types,
synthetic examples, offline reference validation and negative CI coverage.
See the [F1 implementation register](finance-f1-implementation-register.md).

This is not acceptance of Proposed ADR-SHARED-033 or ERP provider support.
G03/G06 F1 wire source advances; real baseline/book/approval/native posting,
reconciliation, journal events, CP qualification and Finance signoff remain.
Infrastructure #35 is not changed or merged by this independent increment.
No EA Gate D/E or Nabhold release advances from DRAFT source registration.

## INT-02 provider allocation checkpoint — 16 October 2026

The [Pulse qualification register](int02-pulse-qualification-register.md) records
`baobab-int02-pulse-consumer` as PROVISIONED for a disposable integration-only
read. No workload promotion or evidence-producer exception is added. Actual
issuer/resource/CP proof, independently recorded scoped provider qualification
and current health remain required; L4-CP-02 and Infrastructure #35 remain
blocked. Existing capability lifecycle and production gates are unchanged.


## 17 October — independent Trade-A TA-05 source lane

[The TA-05 evidence record](ea-r03-trade-a-ta05-source-2026-10-17.md) tracks
Trade #153's central PEP/receipt implementation and corrections for persistence
error denial and exact native record-class binding. It is independent of
Infrastructure #35. This is source and engine-local synthetic-authority work;
TA-06/07/08 remain. EA-R03 / LA-05 remain PARTIAL and no L4, protected staging,
legal/provider acceptance, Gate B/D/E or production activation is promoted.

## 18 October 2026 — INT-02 synthetic qualification accepted

The [verified qualification register](int02-pulse-qualification-register.md) supersedes earlier INT-02 allocation/BLOCKED checkpoints for the qualified source set only. Infrastructure #35 and CP #415/#416 are merged after required checks/reviews. All five mandatory groups and all required provider checks pass in the final-pin Actions run, with verified artifacts and teardown. Shared #346 records the owner-approved named bootstrap exception; ACTIVE producer status remains independent of acceptance. INT-03 Nabhold/IAM/CP/BFF/CMS is now the next integration dependency. EA Gate D/E, protected staging, legal/operational certification and production remain unaccepted.


## 19 October 2026 — Nabhold INT-03 dependency reconciliation

[Fresh dependency audit](nabhold-int03-dependency-audit-2026-10-19.md) preserves
INT-02's exact frozen source qualification and separates it from current native
C4-03/C4-04 protected acceptance. IAM #126 is merged after the gofmt repair and
46 final-head checks (success/applicable skips), as bounded evidence/readiness
source only. Nabhold #71–74 are reviewed/merged after final-head checks; recent
Codespaces/registry controls remain intact. IAM #127 and Infrastructure #36
are reviewed/merged subject-profile and private-handoff source preparation. CMS #38 merged after paired Vitest/coverage repair and mandatory checks; #37
is superseded. Ready-triggered #126 review arrived after merge; corrective IAM
#128 hardens CA inode ownership and checksum/JSON snapshot identity, with local
focused/broader/race tests and all 45 final-head checks passing plus zero-finding
automated review, and is merged at `63db55c87fda13762fc438a6d32a885a63ddb353`. Source candidates confer
no provider certification, Principal, grant, binding or real release authority.
INT-03, EA Gates D/E, protected staging and production remain unaccepted.

**27 October final corrective merge:** Trade #177 (`b8164f6c`) and Infrastructure
#66 (`0538e504`) are merged after full final-head CI/review; Shared #406
(`c1d66ee2`) retains the audit and original passing/failed evidence. The
eight-case live identity component proof is qualified, with independent
revocation and host teardown. The next action is estate BFF/supplier joins,
canonical RFQ/quotation and atomic buyer/seller/spend composition, followed by
available ERP/documentary providers. DEV-07/INT-05 remains partial; no provider,
protected or production acceptance follows.
