# EA Implementation Dashboard

**Governing plan:** [EA Implementation Plan v2.0](../adr/Baobab%20Platform%20Enterprise%20Architecture%20Implementation%20Plan%20%E2%80%94%20Revised%202026-09-30.md) (30 September 2026)
**Last updated:** 2026-09-30
**Maintained:** every EA gate PR updates this page (plan §48).

This page is the single live status for each EA stream, gate and PR. The plan
holds the reasoning; this page holds where things stand now. The plan's §44
dashboard is the audit snapshot this page started from.

Status words mean what they mean in the plan: *implemented* is not *proven*,
*proven* is not *certified*, and nothing here is *production-permitted*
unless it says so.

## Baselines

| Repository | Baseline | Note |
|---|---|---|
| `shared` | `7b9212f` (main) | EA-01 approved baseline for consumer pins: `1bb1c94` (the only later change, #154, is a Foundation workflow) |
| `baobab-cp` | main | Pinned to Shared `1bb1c94` |
| `baobab-iam` | main | Pinned to Shared `1bb1c94` |

## Readiness

```text
BAOBAB EA READINESS                                   2026-09-30
─────────────────────────────────────────────────────────────────

EA-01 Contract Convergence             IN PROGRESS
  CP Shared pin                        CURRENT (1bb1c94), legacy lock schema name
  IAM Shared pin                       CURRENT (1bb1c94), non-canonical lock shape
  Subscriptions Shared pin             STALE (canonical lock shape)
  Payments Shared pin                  STALE (canonical lock shape)
  Trade Shared pin                     STALE (legacy nabhold/* lock)
  ERP Shared pin                       STALE (legacy nabhold/* lock)
  Pulse Shared pin                     STALE (legacy nabhold/* lock)
  CMS contract lock                    MISSING
  Lock schema in Shared (EA-01A)       MISSING
  Foundation lock validation (EA-01C)  MISSING
  Drift report (EA-01D)                MISSING

EA-02 Capability Governance            ADVANCED
  Canonical catalogue                  16 capabilities
  Provider declarations                PARTIAL (see table)
  Foundation enforcement (G-FCI-1)     ENFORCING
  Provider registration DRAFT (02C)    MISSING
  Provider activation Changeset (02D)  MISSING
  Binding integrity (02E)              MISSING

EA-03 Runtime Topology                 PARTIAL
  EngineInstance                       READY
  HealthObservation                    READY
  ProviderMigration                    READY
  EngineRelease architecture           ACCEPTED (ADR-BCP-025, A1–A4)
  EngineRelease                        MISSING
  DeploymentObservation                MISSING

EA-04 Identity                         ADVANCED
  provider-neutral identity contracts  READY (shared#151)
  IAM #42                              MERGED
  activation evidence (#148)           MERGED
  IAM provider declaration             PLANNED-ONLY
  federated workload path              IMPLEMENTED / UNPROVEN
  CP workload                          PROVISIONED
  Subscriptions workload               PROVISIONED

EA-05 Governance                       ADVANCED
  AdministrativeGrant enforcement      BLOCKED (roles→grants decision)

EA-06 Event Fabric                     PARTIAL      (plan §44, not re-audited)
EA-09A Pre-deployment certification    NOT COMPLETE
EA-10 Observability                    PARTIAL      (plan §44, not re-audited)
EA-11 Recovery Engineering             NOT COMPLETE
EA-12 Console                          FOUNDATION
EA-13 Regulations                      DECIDED — Option B; follow-through open

Infrastructure Deployment              DEFERRED BY PLAN
─────────────────────────────────────────────────────────────────
DIGITAL ESTATE DEVELOPMENT              HOLD
PRODUCTION ACTIVATION                   BLOCKED
```

## Engine lifecycle and provider declarations

G-FCI-1 applies: an `active` engine must carry `.baobab/capability-provider.yaml`;
an `experimental` one may omit it or declare planned support only. Foundation
validates a declaration. It never certifies or activates a provider.

| Engine | `repository.lifecycle` | Declaration | Support declared |
|---|---|---|---|
| baobab-iam | active | Yes | Planned only: `identity.authentication.perform`, `identity.workload-token.issue` |
| baobab-payments | active (payments#14) | Yes | IMPLEMENTED, sandbox/temporary, simulated, `production_permitted: false` |
| baobab-subscriptions | active | Yes | IMPLEMENTED, sandbox/temporary, simulated, `production_permitted: false` |
| baobab-cms | active | cms#17 | Planned only: `content.entry.resolve` |
| baobab-pulse | experimental | None | None; intelligence/v1 not yet in scope |
| baobab-trade | — | Not yet reviewed | — |
| baobab-erp | — | Not yet reviewed | — |

## Immediate execution queue (plan §51)

| # | Gate | State | Evidence |
|---:|---|---|---|
| 1 | EA plan v2 committed; prior sequence superseded | Dashboard done; supersession awaiting approval | Plan in `docs/adr`; this dashboard; the supersession marker and register classification are an ADR-status PR that needs owner approval |
| 2 | Contract convergence audit and lock remediation | In progress | CP #227, IAM #46 re-pinned; engines and EA-01A–D open |
| 3 | `identity.workload-token.issue` provider neutrality | Done | shared#151 |
| 4 | Complete IAM #42 | Done | iam#42 |
| 5 | Shared #148 lifecycle semantics | Done | shared#148 |
| 6 | IAM provider declaration | Planned-only | iam#45; support waits on M2–M4 evidence |
| 7 | CMS provider declaration and contract lock | Declaration in review; lock open | cms#17 |
| 8 | Foundation provider-declaration validation | Done (enforcing) | shared#152, #153, #154 |
| 9 | Finalise/accept EngineRelease architecture | Done | cp#228 (ADR-BCP-025 A1–A4) |
| 10 | Implement EngineRelease | Open | ER-01…ER-05 authorised; ER-06 a separate gate |
| 11 | DeploymentObservation model/interfaces | Open | |
| 12 | Provider activation Changeset | Open | EA-02C/D |
| 13 | AdministrativeGrant enforcement | Blocked | Awaiting the roles→grants decision |
| 14–30 | Engine hardening onward | Not started | Plan §51 |

## Decisions

| Decision | Outcome | Record |
|---|---|---|
| G-REG-NS | Option B: Regulations is a first-class capability provider; Trade keeps operational enforcement | [g-reg-ns-resolution.md](g-reg-ns-resolution.md) |
| G-FCI-1 | Declaration mandatory for `active` engines; enforcing | [ea-02-capability-catalogue.md](ea-02-capability-catalogue.md) |
| Payments/Subscriptions lifecycle | Promoted to `active`; simulated support stays non-production | payments#14, subscriptions#19 |
| Pulse lifecycle | `experimental` | pulse#26 |
| ADR-BCP-025 | Accepted with amendments A1–A4 | cp#228 |

Still open, and not to be decided in code: roles→grants flip; Keycloak
`authority: self`; tenant suspend/activate routes; OEV-02 storage and regions;
CIPC/URSB access; capability resolution record retention.

## ADR status

Normative status lives in each register, not here:
[Shared](../adr/README.md) and `baobab-cp` `docs/adr/index.md`. In summary:

| Class | Shared | CP |
|---|---|---|
| Accepted | ADR-0001…0006, ADR-SHARED-007…017, ADR-0020, Canonical Mapping Model | ADR-0001, 0004, 0006, ADR-BCP-001…025, Tenant Onboarding spec |
| Superseded (in part) | ADR-0001 tenancy portions (by ADR-0003) | ADR-0003 (by ADR-BCP-001…010, 018) |
| Historical | Proposed for the Production-Readiness Assessment v1 (findings kept, sequencing superseded by v2.0), with EA Plan v2.0 registered as Accepted; awaiting owner approval | — |
| Proposed | — | — |
| Rejected | — | — |

Outside these registers: `baobab-regulations` ADR-REG-0001…0030 are all
Proposed, pending individual review (G-REG-NS step 1). Trade ADR-0018 and
ADR-0021 are Accepted and due amendments under G-REG-NS step 2.
