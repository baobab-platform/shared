# EA Implementation Dashboard

**Governing plan:** [EA Implementation Plan v2.0](../adr/Baobab%20Platform%20Enterprise%20Architecture%20Implementation%20Plan%20%E2%80%94%20Revised%202026-09-30.md) (30 September 2026)
**Last updated:** 2026-10-01 (reconciled against `main`)
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
| `shared` | main (`7705c0f`, after shared#176) | Evidence-level baselines are read from `main`, not from this table; re-verify before relying on a pin |
| `baobab-cp` | main (`a241607`, after cp#237) | Lock pinned to Shared `e151243`; Foundation caller `06c49e8` (cp#238) |
| `baobab-iam` | main | Lock pinned to Shared `1bb1c94` (BEHIND_UNCHANGED) |
| `baobab-payments`, `baobab-subscriptions` | main | Re-pinned to Shared `3a8230e` (payments#16, subscriptions#21) |
| `baobab-trade`, `baobab-erp` | main | Contract pin deliberately held at `2da1a42`: consumed contracts changed, so a mechanical re-pin is wrong (EA-01). Foundation `06c49e8` since trade#113 and erp#42 |

## Readiness

```text
BAOBAB EA READINESS                                   2026-10-01
─────────────────────────────────────────────────────────────────

EA-01 Contract Convergence             IN PROGRESS
  CP Shared pin                        CURRENT at merge (e151243), canonical lock (cp#229, cp#233, cp#237)
  IAM Shared pin                       BEHIND_UNCHANGED (1bb1c94), canonical lock (iam#47)
  Subscriptions Shared pin             RE-PINNED (3a8230e, subscriptions#21)
  Payments Shared pin                  RE-PINNED (3a8230e, payments#16)
  Trade Shared pin                     HELD at 2da1a42, canonical lock (trade#110); semantic compatibility T-COMPAT-04…07 open
  ERP Shared pin                       HELD at 2da1a42, canonical lock; semantic reconciliation not started
  Pulse Shared pin                     CURRENT at merge, canonical lock (pulse#28)
  CMS contract lock                    CURRENT at merge, canonical lock (cms#19)
  Lock schema in Shared (EA-01A)       READY (shared#157)
  Foundation lock validation (EA-01C)  ENFORCING in Shared and on all 8 consumers (Foundation `06c49e8`)
  Drift report (EA-01D)                READY (Foundation job summary)

EA-02 Capability Governance            02A–02E IMPLEMENTED; G-FCI-1 ENFORCED FLEET-WIDE; PLATFORM CONFORMANCE GATE CLOSED (not certification)
  Canonical catalogue                  16 capabilities
  Provider declarations                PARTIAL (see table)
  Foundation enforcement (G-FCI-1)     ENFORCING on all 8 consumers, all on Foundation `06c49e8`: CP (cp#238), IAM (iam#48), CMS (cms#20), Payments (payments#17), Subscriptions (subscriptions#23), Pulse (pulse#29), Trade (trade#113), ERP (erp#42)
  Control Plane classification         DONE: control-plane trait (shared#174); CP classified control-plane, no declaration, Foundation `06c49e8` (cp#238)
  ERP container scan (erp#42)          FIXED: jackson-databind 2.15.4 CVE-2026-91776/91777 in the upstream idempiere:13-release image replaced by Jackson 2.18.11 (ADR-ERP-004 s5 emergency mitigation, in the Dockerfile with owner, removal condition and build guards). jackson-datatype-joda stays 2.15.4 (needs joda-time 2.12, image has 2.10.14). Not boot-tested: no CI job starts iDempiere. Upstream issue not yet filed
  Gate closed because                  every consumer pins an enforcing Foundation and passes it in CI. It proves structure, catalogue references and contract locks only; it never certifies (EA-09) or activates (Control Plane) anything
  Provider registration DRAFT (02C)    READY (shared#167, cp#231)
  Provider activation Changeset (02D)  READY (shared#167, #168, cp#232; ENGINE_RELEASE check cp#233)
  Binding integrity (02E)              READY (cp#234: constraint validated, fails loudly on unresolved bindings)

EA-03 Runtime Topology                 PARTIAL
  EngineInstance                       READY
  HealthObservation                    READY
  ProviderMigration                    READY
  EngineRelease architecture           ACCEPTED (ADR-BCP-025, A1–A4)
  EngineRelease                        ER-01 contracts; ER-02 record/read (cp#233); release approval via ENGINE_RELEASE_APPROVAL Changeset (shared#171, cp#235); ER-03 desired release/deprecation/revocation (shared#173, cp#237) MERGED; ER-04, ER-05 MISSING
  Binding contract versions            positive integer majors (cp#236, ADR-BCP-025 §2.1.1)
  Capability exclusion on observed state ER-06: DISABLED (amendment A4)
  DeploymentObservation                CONTRACTS (ER-01, topology/v1); CP ER-04 MISSING

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
  event context registry               READY (ADR-SHARED-018; 29 contexts)
  event-type registry                  READY (124 types: 107 ACTIVE, 17 PROPOSED)
  Trade legacy event migration         T-COMPAT-03 MERGED (trade#111); no com.nabhold in event code; legacy migrations immutable
  Broker/relay/inbox/replay            OPEN
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

The Control Plane is not an engine. It carries the `control-plane` trait,
provides no resolvable capability, and may not carry a declaration
(ADR-0020 amendment, 2026-10-01).

| Engine | `repository.lifecycle` | Declaration | Support declared |
|---|---|---|---|
| baobab-iam | active | Yes | Planned only: `identity.authentication.perform`, `identity.workload-token.issue` |
| baobab-payments | active | Yes | IMPLEMENTED, sandbox/temporary, simulated, `production_permitted: false` |
| baobab-subscriptions | active | Yes | IMPLEMENTED, sandbox/temporary, simulated, `production_permitted: false` |
| baobab-cms | active | Yes | Planned only: `content.entry.resolve` |
| baobab-pulse | experimental | None | None; intelligence/v1 not yet in scope |
| baobab-trade | active | Yes | Declared; contents not re-reviewed here |
| baobab-erp | active | Yes | Declared; contents not re-reviewed here |
| baobab-cp | active, `control-plane` (cp#238) | None, by design | None: platform authority, not a provider |

## Immediate execution queue (plan §51)

| # | Gate | State | Evidence |
|---:|---|---|---|
| 1 | EA plan v2 committed; prior sequence superseded | Done | Plan in `docs/adr`; this dashboard (#155); v1 assessment marked Historical and plan registered Accepted (#156) |
| 2 | Contract convergence audit and lock remediation | In progress | CP #227, IAM #46 re-pinned; lock schema, check and drift report shared#157; CP, IAM, CMS and Pulse canonical locks merged (cp#229, iam#47, cms#19, pulse#28); Trade and ERP locks canonical but pinned to `2da1a42` pending semantic compatibility; Subscriptions, Payments re-pinned ([EA-01 record](ea-01-contract-convergence.md)) |
| 3 | `identity.workload-token.issue` provider neutrality | Done | shared#151 |
| 4 | Complete IAM #42 | Done | iam#42 |
| 5 | Shared #148 lifecycle semantics | Done | shared#148 |
| 6 | IAM provider declaration | Planned-only | iam#45; support waits on M2–M4 evidence |
| 7 | CMS provider declaration and contract lock | Done | cms#17, cms#19 |
| 8 | Foundation provider-declaration validation | Done (enforcing) | shared#152, #153, #154 |
| 9 | Finalise/accept EngineRelease architecture | Done | cp#228 (ADR-BCP-025 A1–A4) |
| 10 | Implement EngineRelease | In progress | ER-01 contracts; ER-02 record and read (shared#169, #170, cp#233); release approval (shared#171, cp#235); ER-03 (shared#173, cp#237); ER-04, ER-05 next; ER-06 a separate gate, disabled |
| 11 | DeploymentObservation model/interfaces | Contracts done | ER-01 (`deployment-observation.schema.json`, `deployment:observe`); intake is ER-04 |
| 12 | Provider activation Changeset | Done | DRAFT-only registration and PROVIDER_ACTIVATION (shared#167, #168, cp#231, cp#232); binding integrity (cp#234). Release approval (cp#235) lets a release be APPROVED and a provider be activated without direct SQL |
| 13 | AdministrativeGrant enforcement | Blocked | Awaiting the roles→grants decision |
| 14–30 | Engine hardening onward | Not started | Plan §51 |

## Decisions

| Decision | Outcome | Record |
|---|---|---|
| G-REG-NS | Option B: Regulations is a first-class capability provider; Trade keeps operational enforcement | [g-reg-ns-resolution.md](g-reg-ns-resolution.md) |
| G-FCI-1 | Declaration mandatory for `active` engines; enforcing on all 8 consumers (closed 2026-10-01) | [ea-02-capability-catalogue.md](ea-02-capability-catalogue.md) |
| Control Plane classification | CP is `control-plane`, not `engine`; no provider declaration | [ea-02-capability-catalogue.md](ea-02-capability-catalogue.md), ADR-0020 amendment |
| Payments/Subscriptions lifecycle | Promoted to `active`; simulated support stays non-production | payments#14, subscriptions#19 |
| Pulse lifecycle | `experimental` | pulse#26 |
| ADR-BCP-025 | Accepted with amendments A1–A4 | cp#228 |
| Event context governance | ADR-SHARED-018 Accepted; `erp` DEPRECATED, `payments` kept, fulfilment/logistics/trade.shipment distinct, Regulations owns classification and assessment, `thamani-*` retired in T-COMPAT-03 | shared#161 |

Still open, and not to be decided in code: roles→grants flip; Keycloak
`authority: self`; tenant suspend/activate routes; OEV-02 storage and regions;
CIPC/URSB access; capability resolution record retention.

## ADR status

Normative status lives in each register, not here:
[Shared](../adr/README.md) and `baobab-cp` `docs/adr/index.md`. In summary:

| Class | Shared | CP |
|---|---|---|
| Accepted | ADR-0001…0006, ADR-SHARED-007…017, ADR-0020, Canonical Mapping Model, EA Plan v2.0 | ADR-0001, 0004, 0006, ADR-BCP-001…025, Tenant Onboarding spec |
| Superseded (in part) | ADR-0001 tenancy portions (by ADR-0003) | ADR-0003 (by ADR-BCP-001…010, 018) |
| Historical | Production-Readiness Assessment v1 (findings kept; sequencing superseded by EA Plan v2.0, which is registered Accepted) | — |
| Proposed | — | — |
| Rejected | — | — |

Outside these registers: `baobab-regulations` ADR-REG-0001…0030 are all
Proposed, pending individual review (G-REG-NS step 1). Trade ADR-0018 and
ADR-0021 are Accepted and due amendments under G-REG-NS step 2.
