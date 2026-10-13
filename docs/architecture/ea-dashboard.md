# EA Implementation Register (v2.1)

**Governing plan:** [EA Implementation Plan v2.1](EA-implementation-plan-v2.1-ADR-BCP-026-027-reconciliation.md), Accepted 2026-10-13. [EA Plan v2.0](../adr/Baobab%20Platform%20Enterprise%20Architecture%20Implementation%20Plan%20%E2%80%94%20Revised%202026-09-30.md) remains the baseline for workstreams that v2.1 does not change.  
**Last updated:** 2026-10-13 (EA-R01; Shared `main` at `5dcff30`)  
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
- A YES or PART in a column needs evidence linked in its row.
- Synthetic CI never sets Stag, Legal or Ops.
- *Merged* is not *proven*, *proven* is not *certified*, and nothing here is *production-permitted*.

**Evidence provenance:**
- `S#NNN` links a PR in Shared, checked against Shared `main`.
- `CP #`, `Trade #`, `ERP #`, `Payments #` and `Subscriptions #` are as reported by the [2026-10-13 audit](ea-v2.1-audit-2026-10-13.md). They have not been re-verified from Shared. A row that depends on them stays at PART until the owning repository's register or record confirms it.

## Readiness summary

```text
BAOBAB EA v2.1 READINESS                                   2026-10-13
──────────────────────────────────────────────────────────────────────
EA v2.1 plan                       ACCEPTED (2026-10-13; §11 decisions recorded below)
Backend development                SUBSTANTIAL (code merged; not proven live)
Public site ↔ Console code         INTEGRATED IN CODE (not live end-to-end certified)
Console production login           BLOCKED BY DESIGN (readAuthSettings rejects production)
Protected live E2E                 NOT DEMONSTRATED
Founding-group legal acceptance    OUTSTANDING (no independently accepted verification case)
P0-04A contract convergence        ADVANCED (Trade, ERP, Payments, Subscriptions); Trade Docs open
P0-04B native execution PEPs       OPEN (next priority)
DIGITAL ESTATE DEVELOPMENT         GATE B NOT PASSED
PRODUCTION ACTIVATION              NOT AUTHORISED
──────────────────────────────────────────────────────────────────────
```

## Programme gates (v2.1 §8)

| Gate | Arch | Contr | Code | DB | Synth | Stag | Legal | Ops | State and evidence |
|---|---|---|---|---|---|---|---|---|---|
| **A** Architecture/contract readiness | YES | PART | PART | PART | PART | NO | N/A | N/A | **Not passed.** v2.1 Accepted (this change). LA-01 contracts `5930dcf`; PEO-01 [S#274](https://github.com/baobab-platform/shared/pull/274). Open: Trade Docs convergence; the consumer-pin inventory for LA-01/PEO-01 has not been re-verified |
| **B** Platform developer unfreeze | YES | PART | PART | N/A | PART | NO | N/A | N/A | **Not passed.** The unfreeze list covers Nabhold, ZuriBeans, Thamani and Equator & Estate Co. (v2.1 §8). It needs Gate A, plus proof that no estate frontend implements shadow authority (Thamani drift D-09) |
| **C** Controlled founding-group onboarding (non-production) | YES | PART | PART | PART | PART | NO | NO | N/A | **Not passed.** Truthful examples: [S#268](https://github.com/baobab-platform/shared/pull/268), [S#269](https://github.com/baobab-platform/shared/pull/269), [S#270](https://github.com/baobab-platform/shared/pull/270). Synthetic qualification is in CP (as reported). No authentic, accepted business records exist (D-02) |
| **D** Capability-specific staging qualification | YES | PART | PART | PART | PART | NO | EXT | NO | **Not passed** for any capability. Needs protected staging and certified providers (D-03, D-05) |
| **E** Production activation (EA-09B) | YES | NO | NO | NO | NO | NO | EXT | NO | **Not authorised.** Needs real registry/PSP/KMS arrangements and a signed go/no-go (D-04, D-05) |

## EA workstreams

EA v2.0 and v2.1 do not define EA-07 or EA-08 as workstreams like the others, so this register gives them no status.

| Stream | Arch | Contr | Code | DB | Synth | Stag | Legal | Ops | Assessment, evidence and gap |
|---|---|---|---|---|---|---|---|---|---|
| EA-01 Canonical contracts | YES | PART | YES | N/A | YES | NO | N/A | NO | **Substantially implemented.** Shared CI validators on each contract PR (e.g. `5930dcf`, [S#283](https://github.com/baobab-platform/shared/pull/283)–[S#289](https://github.com/baobab-platform/shared/pull/289), [S#300](https://github.com/baobab-platform/shared/pull/300)). Consumers reconciled: Trade #145, ERP #95, Payments #36, Subscriptions #40 (as reported). Gaps: Trade Docs convergence, consistent consumer pins, live semantic acceptance |
| EA-02 Capability catalogue and providers | YES | PART | PART | PART | PART | NO | EXT | NO | **Partial.** Payments merchant-readiness contract [S#264](https://github.com/baobab-platform/shared/pull/264). Gaps: real provider admission, active bindings, legal restrictions at runtime, certification per capability. Provider support stays simulated and `production_permitted: false` |
| EA-03 EngineRelease and topology | YES | YES | YES | PART | PART | NO | N/A | NO | **Substantial foundation.** ER-01 to ER-05 (see the [historical dashboard](ea-dashboard-v2.0-historical-2026-10-04.md)). Gaps: genuine release and deployment observations, reconciliation, protected failover |
| EA-04 IAM / workload identity | YES | YES | PART | N/A | PART | NO | N/A | NO | **Partial.** Scopes and staging identities defined: [S#251](https://github.com/baobab-platform/shared/pull/251), [S#265](https://github.com/baobab-platform/shared/pull/265), [S#278](https://github.com/baobab-platform/shared/pull/278), [S#279](https://github.com/baobab-platform/shared/pull/279), [S#281](https://github.com/baobab-platform/shared/pull/281). A scope definition creates no ACTIVE client or issued credential. Gaps: active scoped credentials, live revocation, acceptance of the issuer and federation |
| EA-05 CP governance | YES | YES | YES | PART | YES | NO | NO | NO | **Substantial.** Mandates LA-04C/D ([S#257](https://github.com/baobab-platform/shared/pull/257)–[S#260](https://github.com/baobab-platform/shared/pull/260)); sponsorship/deferral ([S#263](https://github.com/baobab-platform/shared/pull/263), [S#272](https://github.com/baobab-platform/shared/pull/272), [S#275](https://github.com/baobab-platform/shared/pull/275)); CP #379 (as reported). Administrative grants stay `enforced: []`. Gaps: real founding-group decisions, external evidence, complete workbenches |
| EA-06 Event fabric | YES | YES | PART | PART | PART | NO | N/A | NO | **Partial.** Event registrations [S#259](https://github.com/baobab-platform/shared/pull/259), [S#272](https://github.com/baobab-platform/shared/pull/272). Gaps: proof of cross-engine replay, redaction, durable delivery and recovery |
| EA-09A Pre-deployment conformance | YES | PART | PART | N/A | PART | NO | EXT | N/A | **Partial.** Gap: independent acceptance of security and providers across engines |
| EA-09B Operational certification | YES | NO | NO | NO | NO | NO | EXT | NO | **Not demonstrated.** Gaps: protected staging, external certification, signed go/no-go |
| EA-10 Observability | YES | PART | PART | N/A | PART | NO | N/A | NO | **Partial.** Gap: deployed trace correlation from admission through native transaction and recovery |
| EA-11 Recovery engineering | YES | PART | PART | PART | PART | NO | N/A | NO | **Partial.** Custody key rewrap and orphan recovery are in CP #382 (as reported). Gap: live drills for backup/restore, key rotation, replay and rollback |
| EA-12 Console and Digital Estates | YES | YES | PART | N/A | PART | NO | N/A | NO | **Console substantial; estates uneven.** CP #360, #377, #378 (as reported); CX-04/05 contracts [S#287](https://github.com/baobab-platform/shared/pull/287), [S#288](https://github.com/baobab-platform/shared/pull/288), [S#289](https://github.com/baobab-platform/shared/pull/289), [S#295](https://github.com/baobab-platform/shared/pull/295), [S#296](https://github.com/baobab-platform/shared/pull/296). Gaps: F-01 to F-07, Thamani drift (D-09) |
| EA-13 Regulatory architecture | YES | PART | PART | N/A | PART | NO | EXT | NO | **Substantial reference implementation.** Gaps: accepted real requirement sources, trust, integration of runtime applicability |

## ADR-BCP-026 gates (progressive enterprise onboarding)

| Gate | Arch | Contr | Code | DB | Synth | Stag | Legal | Ops | Assessment, evidence and remaining |
|---|---|---|---|---|---|---|---|---|---|
| PEO-00/01 | YES | YES | PART | N/A | YES | NO | N/A | N/A | Architecture and contracts established ([S#274](https://github.com/baobab-platform/shared/pull/274), `596a0da`, `dd3777f`). Remaining: reconcile the programme and its evidence |
| PEO-02 | YES | YES | PART | PART | PART | NO | NO | NO | Sponsorship and the 24-month deferral ([S#263](https://github.com/baobab-platform/shared/pull/263), [S#272](https://github.com/baobab-platform/shared/pull/272), [S#273](https://github.com/baobab-platform/shared/pull/273), [S#275](https://github.com/baobab-platform/shared/pull/275)). Remaining: live approval, handling of expiry, acceptance of restriction release |
| PEO-03 (A–K) | YES | YES | PART | PART | PART | NO | EXT | NO | Scanner, custody and admission machinery: [S#276](https://github.com/baobab-platform/shared/pull/276)–[S#279](https://github.com/baobab-platform/shared/pull/279), [S#281](https://github.com/baobab-platform/shared/pull/281), [S#298](https://github.com/baobab-platform/shared/pull/298); CP #380–#382 (as reported). See PEO-03F and PEO-03K below |
| ↳ PEO-03F (incl. former M) | YES | YES | PART | N/A | PART | NO | EXT | NO | Certified official-source transport. Under decision 4 it also carries **independently certified government/PSP source and policy proof, with no synthetic approval or proxy CIPC verification**. Remaining: a genuinely certified external source |
| ↳ PEO-03K (incl. former L) | YES | YES | PART | PART | PART | NO | EXT | NO | Custody and the candidate ledger (CP #382 as reported: migration 000124, S3 Object Lock/KMS). Under decision 4 its staging criterion is **protected staging composition of scanner/token, custody/KMS, retention, destruction, redaction and operational negative tests**. Remaining: approved bucket/KMS deployed, scanner signer, operating retention policy |
| PEO-04 | YES | YES | PART | PART | PART | NO | NO | N/A | Controlled founding-group machinery exists. Remaining: four authentic, accepted business records (D-02) |
| PEO-05 | YES | PART | PART | N/A | PART | NO | EXT | NO | Qualification orchestration and staging runbooks exist. Remaining: protected acceptance of IAM, subscription, provider and tenant |
| PEO-06 | YES | YES | PART | N/A | PART | NO | N/A | NO | Applicant, reviewer and Console functionally implemented (as reported). Remaining: guided evidence UX (F-04), browser security and accessibility (F-05) |
| PEO-07 | YES | N/A | NO | NO | NO | NO | EXT | NO | Criteria defined. Remaining: signed production-readiness decisions |

## ADR-BCP-027 gates (Organisation-first tenancy and legal actor)

| Gate | Arch | Contr | Code | DB | Synth | Stag | Legal | Ops | Assessment, evidence and remaining |
|---|---|---|---|---|---|---|---|---|---|
| LA-00/01 | YES | PART | YES | N/A | YES | NO | N/A | N/A | Canonical model and contracts substantially converged (`5930dcf`). Remaining: final consumer inventory, compatibility sign-off |
| LA-02 | YES | YES | PART | PART | PART | NO | N/A | NO | Nullable legal entity and PRIMARY mapping foundations. Remaining: migration of real data, proof for legacy consumers, rollback |
| LA-03 | YES | YES | PART | PART | PART | NO | NO | N/A | Governed Organisation-first registration implemented (as reported). Remaining: execution accepted for the four founding businesses |
| LA-04 | YES | YES | PART | PART | PART | NO | NO | NO | Mandates, independent decisions, lifecycle and readback: [S#257](https://github.com/baobab-platform/shared/pull/257)–[S#260](https://github.com/baobab-platform/shared/pull/260), [S#287](https://github.com/baobab-platform/shared/pull/287), [S#297](https://github.com/baobab-platform/shared/pull/297); CP #379 (as reported). Remaining: authentic mandates, human authority decisions |
| LA-05 | YES | YES | PART | PART | PART | NO | EXT | NO | Engine policy and contract guards: [S#261](https://github.com/baobab-platform/shared/pull/261), [S#262](https://github.com/baobab-platform/shared/pull/262), [S#264](https://github.com/baobab-platform/shared/pull/264), [S#282](https://github.com/baobab-platform/shared/pull/282), [S#300](https://github.com/baobab-platform/shared/pull/300). Remaining: **P0-04B** native execution certification, issuer/PSP identity, bypasses closed (D-03) |
| LA-06 | YES | YES | PART | PART | PART | NO | NO | N/A | Synthetic founding-business qualification (as reported). Remaining: real records, evidence, independent approval |
| LA-07 | YES | PART | PART | PART | PART | NO | NO | NO | Cutover/test infrastructure and Console increments. Remaining: operational cutover, historical financial attribution, recovery |

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

All five were approved on **2026-10-13** by the **platform owner** (the repository owner). The approval was recorded in the EA-R01 change that accepted v2.1.

| # | Decision | Outcome |
|---:|---|---|
| 1 | ADR-BCP-026/027 amend and extend EA v2.0; unchanged v2.0 workstreams and the no-premature-production premise are retained | **Approved** |
| 2 | Separate gate sequence and four distinct readiness decisions (§6); no global verified legal status | **Approved** |
| 3 | Founding-group 24-month deferral, truthful legal-entity posture, Option B autonomy, scope-bound Nabhold mandates, independent external verification | **Approved** |
| 4 | PEO-03L/M labels | **Remapped:** L becomes the staging-acceptance criterion of PEO-03K; M becomes the certification criterion of PEO-03F. No ADR, registry key or contract is created |
| 5 | Cross-repository acceptance owners | **Approved:** see below |

## Acceptance owners (decision 5)

Only the owning authority may publish a production-support claim for its repository.

| Repository | Acceptance owner |
|---|---|
| baobab-cp, baobab-iam, shared, baobab-subscriptions, baobab-erp, baobab-trade, baobab-payments, Infrastructure | Platform owner, until delegated in writing in this register |

## Drift and gap register

| ID | Finding | Severity | Owner repo | State |
|---|---|---|---|---|
| D-01 | EA v2.1 proposed; dashboard on v2.0 | P0 Governance | shared | **Closed (2026-10-13):** v2.1 Accepted and this register published. Follow-up: confirm cross-repo evidence marked "as reported" against each owning repository |
| D-02 | Genuine founding-company and group-control evidence not accepted | P0 Authority | baobab-cp | Open |
| D-03 | P0-04B native bypass closure incomplete | P0 Financial/legal | Trade, ERP, Payments, Subscriptions, Trade Docs | Open. Shared contract step P0-04B-02 merged ([S#300](https://github.com/baobab-platform/shared/pull/300)) |
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
| EA-R01 | Reconcile architecture and governance | **Done in Shared (2026-10-13)**; cross-repo evidence confirmation follows |
| EA-R02 | Founding legal/evidence acceptance foundation | Not started |
| EA-R03 | Complete P0-04A (Trade Docs) and P0-04B native PEPs | In progress (contracts); native enforcement open |
| EA-R04 | Close frontend and Console integration | Not started |
| EA-R05 | Protected staging and E2E acceptance (audit §10 matrix) | Not started; needs EXT infrastructure |
| EA-R06 | Publication and operational certification | Not started |

Code increments may run in parallel. Production activation stays gated on its dependencies.
