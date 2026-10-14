# EA Implementation Register (v2.1)

**Governing plan:** [EA Implementation Plan v2.1](EA-implementation-plan-v2.1-ADR-BCP-026-027-reconciliation.md), Accepted 2026-10-13. [EA Plan v2.0](../adr/Baobab%20Platform%20Enterprise%20Architecture%20Implementation%20Plan%20%E2%80%94%20Revised%202026-09-30.md) remains the baseline for workstreams that v2.1 does not change.  
**Last updated:** 2026-10-14 (P0-04B-04 ERP posting authority merged, Gate D passed for GL journals; previous: P0-04B-03 Trade checkout COMMIT fence)  
**Source audit:** [EA v2.1 audit, 13 October 2026](ea-v2.1-audit-2026-10-13.md)  
**History:** [v2.0 dashboard, last updated 2026-10-04](ea-dashboard-v2.0-historical-2026-10-04.md). It is historical and is not carried forward as live status (v2.1 §10).

This page is the live register for every EA gate. The plan holds the reasoning.
Any PR that moves a gate updates its row here and records (v2.1 §9):
- commit
- contract pin
- migration ID
- test run
- approver
- unmet external dependencies
- rollback plan

## How to read this register

Each row is scored separately at eight evidence levels (v2.1 §10):

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
- Arch = YES in every row rests on one record, not repeated per row: the v2.1 acceptance ([S#301](https://github.com/baobab-platform/shared/pull/301)) and ADR-BCP-026/027, Accepted in baobab-cp on 2026-10-09.
- Synthetic CI never sets Stag, Legal or Ops.
- *Merged* is not *proven*, *proven* is not *certified*, and nothing here is *production-permitted*.

**Evidence provenance:**
- `S#NNN` links a PR in Shared, checked against Shared `main`.
- `CP #`, `Trade #`, `Trade Docs #`, `ERP #`, `Payments #` and `Subscriptions #` link PRs in the owning repository. Each one cited here was **verified merged on that repository's `main` on 2026-10-13**; citations added for P0-04B-04 (ERP #96, ERP #98, CP #393) were verified on 2026-10-14. A merged PR proves code and its CI, not the claims an owning record makes about live behaviour; those stay in the Stag, Legal and Ops columns.
- The CP [ADR-BCP-026/027 completion plan](https://github.com/baobab-platform/baobab-cp/blob/main/docs/reconciliation/adr026-027-completion-plan-2026-10-12.md) is the owning execution record for P0-01 to P0-05; this register summarises it and does not override it.

## Readiness summary

```text
BAOBAB EA v2.1 READINESS                                   2026-10-14
──────────────────────────────────────────────────────────────────────
EA v2.1 plan                       ACCEPTED (2026-10-13; §11 decisions recorded below)
Backend development                SUBSTANTIAL (code merged; not proven live)
Public site ↔ Console code         INTEGRATED IN CODE (not live end-to-end certified)
Console production login           BLOCKED BY DESIGN (readAuthSettings rejects production)
Protected live E2E                 NOT DEMONSTRATED
Founding-group legal acceptance    OUTSTANDING (no independently accepted verification case)
P0-04A contract convergence        COMPLETE for current consumers (Trade, ERP, Payments, Subscriptions, Trade Docs)
P0-04B native execution PEPs       OPEN: P0-04B-01/02/03 merged (Trade); P0-04B-04 ERP posting authority merged, Gate D passed (GL journals, synthetic); next: other ERP classes, Payments, Subscriptions, Trade Docs
DIGITAL ESTATE DEVELOPMENT         GATE B NOT PASSED
PRODUCTION ACTIVATION              NOT AUTHORISED
──────────────────────────────────────────────────────────────────────
```

## Programme gates (v2.1 §8)

| Gate | Arch | Contr | Code | DB | Synth | Stag | Legal | Ops | State and evidence |
|---|---|---|---|---|---|---|---|---|---|
| **A** Architecture/contract readiness | YES | YES | PART | PART | PART | NO | N/A | N/A | **Not passed.** v2.1 Accepted ([S#301](https://github.com/baobab-platform/shared/pull/301)). LA-01 contracts `5930dcf` and PEO-01 [S#274](https://github.com/baobab-platform/shared/pull/274), consumed by every owning engine through P0-04A: [Trade #145](https://github.com/baobab-platform/baobab-trade/pull/145), [ERP #95](https://github.com/baobab-platform/baobab-erp/pull/95), [Payments #36](https://github.com/baobab-platform/baobab-payments/pull/36), [Subscriptions #40](https://github.com/baobab-platform/baobab-subscriptions/pull/40), [Trade Docs #13](https://github.com/baobab-platform/baobab-trade-docs/pull/13). Organisation-first migration: [CP `c606b20`](https://github.com/baobab-platform/baobab-cp/commit/c606b20) (000102). Remaining: acceptance-owner compatibility sign-off of the final consumer inventory (LA-00/01) |
| **B** Platform developer unfreeze | YES | PART | PART | N/A | PART | NO | N/A | N/A | **Not passed.** Contracts, code and validators so far: LA-01 `5930dcf`, PEO-01 [S#274](https://github.com/baobab-platform/shared/pull/274). The unfreeze list covers Nabhold, ZuriBeans, Thamani and Equator & Estate Co. (v2.1 §8). It needs Gate A, plus proof that no estate frontend implements shadow authority (Thamani drift D-09) |
| **C** Controlled founding-group onboarding (non-production) | YES | PART | PART | PART | PART | NO | NO | N/A | **Not passed.** Truthful examples: [S#268](https://github.com/baobab-platform/shared/pull/268), [S#269](https://github.com/baobab-platform/shared/pull/269), [S#270](https://github.com/baobab-platform/shared/pull/270). CP machinery and synthetic four-tenant PostgreSQL qualification: [CP #339](https://github.com/baobab-platform/baobab-cp/pull/339) (migration 000120), [CP #340](https://github.com/baobab-platform/baobab-cp/pull/340), [CP #341](https://github.com/baobab-platform/baobab-cp/pull/341). No authentic, accepted business records exist (D-02) |
| **D** Capability-specific staging qualification | YES | PART | PART | PART | PART | NO | EXT | NO | **Not passed** for any capability. Contracts: [S#264](https://github.com/baobab-platform/shared/pull/264), [S#300](https://github.com/baobab-platform/shared/pull/300). Code, migration and synthetic tests: [CP #382](https://github.com/baobab-platform/baobab-cp/pull/382), [CP #389](https://github.com/baobab-platform/baobab-cp/pull/389), [CP #390](https://github.com/baobab-platform/baobab-cp/pull/390), [Trade #146](https://github.com/baobab-platform/baobab-trade/pull/146), [Trade #147](https://github.com/baobab-platform/baobab-trade/pull/147), [Trade #148](https://github.com/baobab-platform/baobab-trade/pull/148), [ERP #95](https://github.com/baobab-platform/baobab-erp/pull/95), [Payments #36](https://github.com/baobab-platform/baobab-payments/pull/36), [Subscriptions #40](https://github.com/baobab-platform/baobab-subscriptions/pull/40). Protected staging qualification code: [CP #345](https://github.com/baobab-platform/baobab-cp/pull/345). Needs protected staging and certified providers (D-03, D-05) |
| **E** Production activation (EA-09B) | YES | NO | NO | NO | NO | NO | EXT | NO | **Not authorised.** Needs real registry/PSP/KMS arrangements and a signed go/no-go (D-04, D-05) |

## EA workstreams

EA v2.0 and v2.1 do not define EA-07 or EA-08 as workstreams like the others, so this register gives them no status.

| Stream | Arch | Contr | Code | DB | Synth | Stag | Legal | Ops | Assessment, evidence and gap |
|---|---|---|---|---|---|---|---|---|---|
| EA-01 Canonical contracts | YES | YES | YES | N/A | YES | NO | N/A | NO | **Implemented and converged for current consumers.** Shared CI validators on each contract PR (e.g. `5930dcf`, [S#283](https://github.com/baobab-platform/shared/pull/283)–[S#289](https://github.com/baobab-platform/shared/pull/289), [S#300](https://github.com/baobab-platform/shared/pull/300)). P0-04A owning-engine convergence: [Trade #145](https://github.com/baobab-platform/baobab-trade/pull/145), [ERP #95](https://github.com/baobab-platform/baobab-erp/pull/95), [Payments #36](https://github.com/baobab-platform/baobab-payments/pull/36), [Subscriptions #40](https://github.com/baobab-platform/baobab-subscriptions/pull/40), [Trade Docs #13](https://github.com/baobab-platform/baobab-trade-docs/pull/13). Gap: live semantic acceptance |
| EA-02 Capability catalogue and providers | YES | PART | PART | NO | PART | NO | EXT | NO | **Partial.** Payments merchant-readiness contract [S#264](https://github.com/baobab-platform/shared/pull/264). Gaps: real provider admission, active bindings, legal restrictions at runtime, certification per capability. Provider support stays simulated and `production_permitted: false` |
| EA-03 EngineRelease and topology | YES | YES | YES | PART | PART | NO | N/A | NO | **Substantial foundation.** ER-01 to ER-05 (see the [historical dashboard](ea-dashboard-v2.0-historical-2026-10-04.md)). Gaps: genuine release and deployment observations, reconciliation, protected failover |
| EA-04 IAM / workload identity | YES | YES | PART | N/A | PART | NO | N/A | NO | **Partial.** Scopes and staging identities defined: [S#251](https://github.com/baobab-platform/shared/pull/251), [S#265](https://github.com/baobab-platform/shared/pull/265), [S#278](https://github.com/baobab-platform/shared/pull/278), [S#279](https://github.com/baobab-platform/shared/pull/279), [S#281](https://github.com/baobab-platform/shared/pull/281). A scope definition creates no ACTIVE client or issued credential. Gaps: active scoped credentials, live revocation, acceptance of the issuer and federation |
| EA-05 CP governance | YES | YES | YES | PART | YES | NO | NO | NO | **Substantial.** Mandates LA-04C/D ([S#257](https://github.com/baobab-platform/shared/pull/257)–[S#260](https://github.com/baobab-platform/shared/pull/260)); sponsorship/deferral ([S#263](https://github.com/baobab-platform/shared/pull/263), [S#272](https://github.com/baobab-platform/shared/pull/272), [S#275](https://github.com/baobab-platform/shared/pull/275)); [CP #379](https://github.com/baobab-platform/baobab-cp/pull/379). Administrative grants stay `enforced: []`. Gaps: real founding-group decisions, external evidence, complete workbenches |
| EA-06 Event fabric | YES | YES | PART | NO | PART | NO | N/A | NO | **Partial.** Event registrations [S#259](https://github.com/baobab-platform/shared/pull/259), [S#272](https://github.com/baobab-platform/shared/pull/272). Gaps: proof of cross-engine replay, redaction, durable delivery and recovery |
| EA-09A Pre-deployment conformance | YES | PART | PART | N/A | PART | NO | EXT | N/A | **Partial.** Contracts: [ADR-SHARED-026](../adr/ADR-SHARED-026%20%E2%80%94%20Cross-Repository%20Regulations%2C%20Trade%20Docs%20and%20Pulse%20Conformance%20Architecture.md) (cross-repository conformance) and [ADR-SHARED-032](../adr/ADR-SHARED-032%20%E2%80%94%20EA-09%20Provider%20Capability%20Certification%20and%20Pulse%20Activation%20Admission.md) (EA-09 certification and activation admission). Code and synthetic: Foundation G-FCI-1 enforcing on all 8 consumers and the rtd-conformance suite (`scripts/rtd_conformance.py`); see the [historical dashboard](ea-dashboard-v2.0-historical-2026-10-04.md). Gap: independent acceptance of security and providers across engines |
| EA-09B Operational certification | YES | NO | NO | NO | NO | NO | EXT | NO | **Not demonstrated.** Gaps: protected staging, external certification, signed go/no-go |
| EA-10 Observability | YES | PART | NO | N/A | NO | NO | N/A | NO | **Partial (contracts only).** Canonical correlation metadata: [ADR-0004](../adr/ADR-0004-canonical-cross-engine-metadata.md). No merged trace-correlation code or test is cited, so Code and Synth stay NO until one is linked. Gap: deployed trace correlation from admission through native transaction and recovery |
| EA-11 Recovery engineering | YES | PART | PART | PART | PART | NO | N/A | NO | **Partial.** Custody contracts [S#281](https://github.com/baobab-platform/shared/pull/281), [S#298](https://github.com/baobab-platform/shared/pull/298). Key rewrap, orphan recovery and migration 000124 in [CP #382](https://github.com/baobab-platform/baobab-cp/pull/382). Gap: live drills for backup/restore, key rotation, replay and rollback |
| EA-12 Console and Digital Estates | YES | YES | PART | N/A | PART | NO | N/A | NO | **Console substantial; estates uneven.** [CP #360](https://github.com/baobab-platform/baobab-cp/pull/360), [CP #377](https://github.com/baobab-platform/baobab-cp/pull/377), [CP #378](https://github.com/baobab-platform/baobab-cp/pull/378); CX-04/05 contracts [S#287](https://github.com/baobab-platform/shared/pull/287), [S#288](https://github.com/baobab-platform/shared/pull/288), [S#289](https://github.com/baobab-platform/shared/pull/289), [S#295](https://github.com/baobab-platform/shared/pull/295), [S#296](https://github.com/baobab-platform/shared/pull/296). Gaps: F-01 to F-07, Thamani drift (D-09) |
| EA-13 Regulatory architecture | YES | PART | PART | N/A | PART | NO | EXT | NO | **Substantial reference implementation.** Contracts: [ADR-SHARED-028](../adr/ADR-SHARED-028%20%E2%80%94%20Canonical%20Regulatory%20Decision%20Evaluation%20Contract.md), [S#276](https://github.com/baobab-platform/shared/pull/276), [S#277](https://github.com/baobab-platform/shared/pull/277). Code and synthetic: the cross-repository rtd-conformance suite ([ADR-SHARED-026](../adr/ADR-SHARED-026%20%E2%80%94%20Cross-Repository%20Regulations%2C%20Trade%20Docs%20and%20Pulse%20Conformance%20Architecture.md)). Gaps: accepted real requirement sources, trust, integration of runtime applicability |

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
| LA-05 | YES | YES | PART | PART | PART | NO | EXT | NO | Engine policy and contract guards: [S#261](https://github.com/baobab-platform/shared/pull/261), [S#262](https://github.com/baobab-platform/shared/pull/262), [S#264](https://github.com/baobab-platform/shared/pull/264), [S#282](https://github.com/baobab-platform/shared/pull/282), [S#300](https://github.com/baobab-platform/shared/pull/300). P0-04B-01/02 Trade binding lifecycle, authenticated intake and CP-owned activation with native PostgreSQL 17/Medusa proof: [Trade #146](https://github.com/baobab-platform/baobab-trade/pull/146), [Trade #147](https://github.com/baobab-platform/baobab-trade/pull/147), [Trade #148](https://github.com/baobab-platform/baobab-trade/pull/148), [CP #389](https://github.com/baobab-platform/baobab-cp/pull/389), [CP #390](https://github.com/baobab-platform/baobab-cp/pull/390). P0-04B-03 cart-completion COMMIT fence for activated bindings (single consumption, revocation, lease expiry, replay, compensation; real completeCartWorkflow acceptance on PostgreSQL 17): [Trade #149](https://github.com/baobab-platform/baobab-trade/pull/149), receipt [CP #392](https://github.com/baobab-platform/baobab-cp/pull/392). P0-04B-04 ERP posting authority (ADR-SHARED-034, ADR-ERP-022): `erp/v2` contract [S#304](https://github.com/baobab-platform/shared/pull/304), [S#306](https://github.com/baobab-platform/shared/pull/306); CP resolver with immutable decision history [CP #393](https://github.com/baobab-platform/baobab-cp/pull/393) (migration 000125); ERP native placement, provenance, attribution and COMMIT fences [ERP #96](https://github.com/baobab-platform/baobab-erp/pull/96) (Gate B); real iDempiere 13/PostgreSQL Gate D [ERP #98](https://github.com/baobab-platform/baobab-erp/pull/98), [CI run 38560332080](https://github.com/baobab-platform/baobab-erp/actions/runs/38560332080) (19/19 against a synthetic CP: valid, eight denial modes, unplaced org, injected failure, concurrency, retry, background repost, direct-SQL bypass), which also fixed a JVM veto that never fired for a real `AD_Client`; receipt CP completion plan §14. Remaining: **P0-04B** Trade full order/payment execution; ERP invoice/payment/allocation/shipment/order Gate D scenarios, purchase-side and configuration classes; Payments/Subscriptions/Trade Docs execution points; issuer/PSP identity (D-03) |
| LA-06 | YES | YES | PART | NO | PART | NO | NO | N/A | Contract examples separating synthetic and real businesses: [S#270](https://github.com/baobab-platform/shared/pull/270). CP synthetic founding qualification and correlation: [CP #340](https://github.com/baobab-platform/baobab-cp/pull/340), [CP #341](https://github.com/baobab-platform/baobab-cp/pull/341). Remaining: real records, evidence, independent approval |
| LA-07 | YES | PART | PART | NO | PART | NO | NO | NO | Read-only mandate scope and readback, with validators: [S#287](https://github.com/baobab-platform/shared/pull/287), [S#297](https://github.com/baobab-platform/shared/pull/297); [CP #379](https://github.com/baobab-platform/baobab-cp/pull/379). Historical financial attribution, ERP GL journals: every governed posting stores the CP `decision_id`, mandate lineage, placement and Finance baseline in the same transaction, and CP keeps the decision immutably ([CP #393](https://github.com/baobab-platform/baobab-cp/pull/393), [ERP #96](https://github.com/baobab-platform/baobab-erp/pull/96)); Gate D asserts the rows on real iDempiere ([ERP #98](https://github.com/baobab-platform/baobab-erp/pull/98)). No cutover migration is cited, so DB stays NO. Remaining: operational cutover, attribution for the other ERP classes and engines, recovery |

## Founding-group truth table

These are declared business positions, not verified registry facts (v2.1 §3).

| Business | Canonical operating treatment | Independently accepted? | Still required |
|---|---|---|---|
| Nabhold Group Africa | Its own Organisation and Tenant; a potential scoped legal actor | **NO.** [S#252](https://github.com/baobab-platform/shared/pull/252) is a documentary CIPC reference, and examples stay `UNVERIFIED` ([S#269](https://github.com/baobab-platform/shared/pull/269)) | A verification case accepted in CP; any authority to act for another business |
| Thamani Global | An independent incorporated business and Tenant | **NO.** [S#266](https://github.com/baobab-platform/shared/pull/266) is a documentary CIPC reference | Its own official registration; separate proof of group control |
| ZuriBeans | An independent Organisation and Tenant, with no fictional incorporation ([S#270](https://github.com/baobab-platform/shared/pull/270)) | N/A (unincorporated) | A scope-specific authorised legal actor for each activity that needs one |
| Equator & Estate Co. | An independent Organisation and Tenant, with no fictional incorporation | N/A (unincorporated) | Real legal responsibility for property, construction and other relevant activities |

Ownership alone never lets Nabhold act as issuer, seller, importer or contracting actor for ZuriBeans or Equator. Each role needs its own accepted mandate.

## v2.1 §11 decisions

All five were approved on **2026-10-13** by the **platform owner** (the repository owner). The approval is recorded in [S#301](https://github.com/baobab-platform/shared/pull/301), the EA-R01 change that accepted v2.1.

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
| D-03 | P0-04B native bypass closure incomplete | P0 Financial/legal | Trade, ERP, Payments, Subscriptions, Trade Docs | Open. P0-04B-01/02/03 merged ([S#300](https://github.com/baobab-platform/shared/pull/300), [Trade #146](https://github.com/baobab-platform/baobab-trade/pull/146), [Trade #147](https://github.com/baobab-platform/baobab-trade/pull/147), [Trade #148](https://github.com/baobab-platform/baobab-trade/pull/148), [CP #389](https://github.com/baobab-platform/baobab-cp/pull/389), [CP #390](https://github.com/baobab-platform/baobab-cp/pull/390)), [Trade #149](https://github.com/baobab-platform/baobab-trade/pull/149)); P0-04B-04 ERP posting authority merged ([S#304](https://github.com/baobab-platform/shared/pull/304), [CP #393](https://github.com/baobab-platform/baobab-cp/pull/393), [ERP #96](https://github.com/baobab-platform/baobab-erp/pull/96), [ERP #98](https://github.com/baobab-platform/baobab-erp/pull/98)), Gate D passed for GL journals; next: ERP invoice/payment/allocation/shipment classes, Payments, Subscriptions, Trade Docs |
| D-04 | Console production authentication deliberately disabled | P0 Go-live | baobab-cp | Open (by design until security-approved) |
| D-05 | No certification of scanner/custody as deployed | P0 Evidence | baobab-cp, Infrastructure | Open |
| D-06 | Public registration and login deep-link journey incomplete | P1 UX | baobab-cp, baobab-iam | Open (F-01, F-02) |
| D-07 | Independent Console workbenches incomplete | P1 Workflow | baobab-cp | Open (F-03, F-04; CX-06–10) |
| D-08 | No acceptance for protected browser, dataset lifecycle or performance | P1 Assurance | baobab-cp | Open (F-05) |
| D-09 | EA-12 estates uneven; Thamani legacy storefront routes | P1 Product | thamani and estates | Open |
| D-10 | Public website publication and documentation governance incomplete | P1 Publication | baobab-cp | Open (F-06, F-07) |

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

## Execution order (audit §9)

| # | Item | State |
|---:|---|---|
| EA-R01 | Reconcile architecture and governance | **Done (2026-10-13)**, including cross-repository evidence verification |
| EA-R02 | Founding legal/evidence acceptance foundation | In progress. CP machinery merged ([CP #339](https://github.com/baobab-platform/baobab-cp/pull/339)–[CP #345](https://github.com/baobab-platform/baobab-cp/pull/345)). Open and actionable: integrate the scanner and custody with approved infrastructure (bucket/KMS deployment, scanner signer, operating retention policy; see PEO-03K). Externally blocked: authentic Nabhold/Thamani records, corporate-control decisions and mandates (EXT) |
| EA-R03 | Complete P0-04A and P0-04B native PEPs | P0-04A complete; P0-04B-01/02/03 merged (Trade, [Trade #149](https://github.com/baobab-platform/baobab-trade/pull/149)); P0-04B-04 ERP posting authority merged with Gate D passed for GL journals ([ERP #98](https://github.com/baobab-platform/baobab-erp/pull/98)); next: remaining ERP operation classes, then Payments, Subscriptions and Trade Docs execution points; Trade full order/payment execution also remains open |
| EA-R04 | Close frontend and Console integration | Not started |
| EA-R05 | Protected staging and E2E acceptance (audit §10 matrix) | Not started; needs EXT infrastructure |
| EA-R06 | Publication and operational certification | Not started |

Code increments may run in parallel. Production activation stays gated on its dependencies.
