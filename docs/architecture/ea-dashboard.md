# EA Implementation Dashboard

**Governing plan:** [EA Implementation Plan v2.0](../adr/Baobab%20Platform%20Enterprise%20Architecture%20Implementation%20Plan%20%E2%80%94%20Revised%202026-09-30.md) (30 September 2026)
**Last updated:** 2026-10-04 (fleet consumed-contract reconciliation; historical stream assessments retain their evidence dates)
**Maintained:** every EA gate PR updates this page (plan §48).

This page is the single live status for each EA stream, gate and PR. The plan
holds the reasoning; this page holds where things stand now. The plan's §44
dashboard is the audit snapshot this page started from.

Status words mean what they mean in the plan: *implemented* is not *proven*,
*proven* is not *certified*, and nothing here is *production-permitted*
unless it says so.

## Current resumption checkpoint — 2026-10-04

[EA v2 resumption checkpoint](ea-v2-resumption-2026-10-04.md) records the current
Shared/IAM/CP baselines, all eight observed consumer pins and the next bounded
execution sequence. IAM #56–#60 are merged and their isolated live evidence is
sufficient to resume eligible source/integration tasks. **EA-04 remains partial**:
federated resource audiences, real signer lifecycle, deployed consumer routes
and activation evidence remain open. Provider declarations remain planned-only.

IAM [#62](https://github.com/baobab-platform/baobab-iam/pull/62) reconciles its
five consumed contracts from `10810e2` to reviewed Shared `6899a2d`; final-head
compatibility CI is required before merge. No scope grant, canonical activation,
Digital Estate unfreeze or infrastructure deployment is implied.

The checkpoint takes precedence over conflicting historical IAM/pin statements
below. The remaining streams have **not** been fully re-audited in this update;
in particular the ERP lock has advanced and its old operational gaps must be
checked against current runtime code before being treated as outstanding work.

## Fleet consumed-contract reconciliation — 2026-10-04

[Current fleet reconciliation](ea-v2-contract-drift-2026-10-04.md) records the
six consumer PRs, consumed semantic deltas, exact reviewed Shared target and
head-specific CI. IAM #62 and Shared #210 were merged by the owner; CP already
pins the reviewed contract target. New consumer PRs remain draft proposals.

ERP now implements the new caller-bound CP context boundary in its reconciliation
PR, retaining independent approved-plan and Finance requirements. Production
validator registration/grant and deployed acceptance remain outstanding.
Subscriptions/Payments provider metadata is DRAFT, simulated and non-production.
CMS/Trade security failures remain merge blockers; contract compatibility alone
does not override them. This record supersedes older pin and ERP 501 statements
within its audit scope. EA-04, certification, activation and deployment remain held.

## Baselines — historical 2026-10-02 assessment

Verified against each repository's `main` on 2026-10-02. Evidence-level baselines are read from `main`, not from this table; re-verify before relying on a pin.

| Repository | `main` | Shared pin | Note |
|---|---|---|---|
| `shared` | `a503649` (shared#195) | n/a | Administration policy: criteria APPROVED, phishing-resistant evidence = trusted `acr` 3 or `webauthn`/`hwk` `amr` |
| `baobab-cp` | `f234ee5` (cp#252) | `a503649` | CURRENT. Consumes the approved shadow criteria and the ACR-or-AMR evidence form |
| `baobab-iam` | `2a5bd78` (iam#51) | `1bb1c94` | **BEHIND, and behind in substance**: IAM issues `administrator:read/write/approve` (iam#50, iam#51), which the pinned registry does not contain. Correction open (see *Open corrections*). iam#52 open |
| `baobab-payments`, `baobab-subscriptions` | `fc144da`, `0019f3a` | `3a8230e` | Re-pinned (payments#16, subscriptions#21) |
| `baobab-cms`, `baobab-pulse` | `19deac1`, `0cece91` | `b63ce52` | Canonical locks (cms#19, pulse#28) |
| `baobab-trade` | `78d16b8` (trade#114) | `b063f8a` | T-COMPAT-04…07 DONE: adapted, re-pinned, exact-pin conformance suite |
| `baobab-erp` | `b65ef74` | `2da1a42` | HELD deliberately: consumed contracts changed, so a mechanical re-pin is wrong. Semantic reconciliation not started |

## Readiness

```text
BAOBAB EA READINESS                                   2026-10-02
─────────────────────────────────────────────────────────────────

EA-01 Contract Convergence             CONVERGED for locks, pins and ERP semantic compatibility (proven); open: EA-01B nabhold references, EA-01E, ERP operational gaps (record: ea-01-contract-convergence.md)
  CP Shared pin                        a503649 (cp#252): 1 behind, no consumed contract changed (BEHIND_UNCHANGED), canonical lock
  IAM Shared pin                       a503649 (iam#52): 1 behind, no consumed contract changed; the lock covers the scopes IAM issues and check-issued-scopes.sh asserts every Baobab-defined issued scope exists in the exact pinned registry
  Subscriptions Shared pin             3a8230e (subscriptions#21): 66 behind, BEHIND_CHANGED (control-plane domain, capabilities.json)
  Payments Shared pin                  3a8230e (payments#16): 66 behind, BEHIND_CHANGED (control-plane domain, capabilities.json)
  Trade Shared pin                     b063f8a (trade#114): 34 behind, BEHIND_CHANGED (control-plane openapi, workload-registry); T-COMPAT-04…07 DONE with an exact-pin conformance suite
  ERP Shared pin                       CURRENT (739f0ca, erp#46): ERP-COMPAT-01…07 DONE; exact-pin conformance suite (28 tests, CI shared-conformance); lock 19 to 36 contracts. Not done: 4 boundary operations (501), domain events held (none delivered), see record
  Pulse Shared pin                     b63ce52 (pulse#28): 85 behind, BEHIND_CHANGED (control-plane domain), canonical lock
  CMS contract lock                    b63ce52 (cms#19): 85 behind, BEHIND_UNCHANGED, canonical lock
  Lock schema in Shared (EA-01A)       READY (shared#157)
  Foundation lock validation (EA-01C)  ENFORCING in Shared and on all 8 consumers (Foundation `06c49e8`); all 8 locks pass `check --mode auto` against Shared 739f0ca (2026-10-02)
  Drift report (EA-01D)                READY (Foundation job summary)

EA-02 Capability Governance            02A–02E IMPLEMENTED; G-FCI-1 ENFORCED FLEET-WIDE; PLATFORM CONFORMANCE GATE CLOSED (not certification)
  Canonical catalogue                  16 capabilities
  Provider declarations                PARTIAL (see table)
  Foundation enforcement (G-FCI-1)     ENFORCING on all 8 consumers, all on Foundation `06c49e8`: CP (cp#238), IAM (iam#48), CMS (cms#20), Payments (payments#17), Subscriptions (subscriptions#23), Pulse (pulse#29), Trade (trade#113), ERP (erp#42)
  Control Plane classification         DONE: control-plane trait (shared#174); CP classified control-plane, no declaration, Foundation `06c49e8` (cp#238)
  ERP container scan (erp#42)          FIXED: jackson-databind 2.15.4 CVE-2026-91776/91777 in the upstream idempiere:13-release image replaced by Jackson 2.18.11 (ADR-ERP-004 s5 emergency mitigation, in the Dockerfile with owner, removal condition and build guards). jackson-datatype-joda stays 2.15.4 (needs joda-time 2.12, image has 2.10.14). CVE-2026-89425 (jackson-core 2.15.2 shaded inside Hazelcast 5.3.7 in the Hazelcast bundle, in neither 13-release nor 13-daily fixed) cleared in erp#43 by removing the unused Hazelcast bundle (ADR-ERP-004 s5, build guard; no scan exception). Not boot-tested: no CI job starts iDempiere. Upstream issue not yet filed
  Gate closed because                  every consumer pins an enforcing Foundation and passes it in CI. It proves structure, catalogue references and contract locks only; it never certifies (EA-09) or activates (Control Plane) anything
  Provider registration DRAFT (02C)    READY (shared#167, cp#231)
  Provider activation Changeset (02D)  READY (shared#167, #168, cp#232; ENGINE_RELEASE check cp#233)
  Binding integrity (02E)              READY (cp#234: constraint validated, fails loudly on unresolved bindings)

EA-03 Runtime Topology                 PARTIAL      (ER-01…05 IMPLEMENTED; capability-based invocation and operational proof OPEN)
  EngineInstance                       READY
  HealthObservation                    READY
  ProviderMigration                    READY
  EngineRelease architecture           ACCEPTED (ADR-BCP-025, A1–A4)
  EngineRelease                        ER-01 contracts; ER-02 record/read (cp#233); release approval via ENGINE_RELEASE_APPROVAL Changeset (shared#171, cp#235); ER-03 desired release/deprecation/revocation (shared#173, cp#237) MERGED; ER-04 intake and observed release MERGED (shared#178, cp#239) but NOT OPERATIONALLY PROVEN (see ER-04 production gates); ER-05 MERGED: drift (cp#240), release/status/desired-release events and topology metrics (cp#242), readiness consequences (cp#243)
  Binding contract versions            positive integer majors (cp#236, ADR-BCP-025 §2.1.1)
  Capability exclusion on observed state ER-06: DISABLED (amendment A4)
  DeploymentObservation                CP intake MERGED (cp#239); production reporter registered PROVISIONED; no observation received
  Capability-based invocation (EA-03D) OPEN: the Control Plane still invokes Subscriptions through BILLING_ENGINE_URL rather than CapabilityResolution to an eligible instance

EA-04 Identity                         ADVANCED
  provider-neutral identity contracts  READY (shared#151)
  IAM #42                              MERGED
  activation evidence (#148)           MERGED
  IAM provider declaration             PLANNED-ONLY
  federated workload path              IMPLEMENTED / UNPROVEN
  Workload registry authority          Shared owns it; a production CP loads it and fails closed (cp#241). The six existing ACTIVE records still need reconciling before ACTIVE lifecycle enforcement is trusted (ER-04 production gate 1)
  Deployment controller workload       PROVISIONED (baobab-deployment-controller-production)
  CP workload                          PROVISIONED
  Subscriptions workload               PROVISIONED

EA-05 Governance                       ADVANCED
  Administrative authority             MIGRATION PATH ACCEPTED (roles-to-grants-decision.md); implementation in progress
    ADA-05 grant administration        IMPLEMENTED (cp#244, shared#184/#185; exact-scope delegation, then narrower-scope cp#247)
    grant replace/supersede            IMPLEMENTED (cp#246)
    narrower-scope delegation          IMPLEMENTED (cp#247, cp#248) for provable containment, incl. org->tenant via effective TenantOrganisationMapping; group-descendant needs a supplied canonical group graph
    CRITICAL grant bound               24 hours, STANDING prohibited (shared#190, cp#248)
    ADA-06 maker/checker and SoD       IMPLEMENTED (shared#187, cp#245)
    authority:self issuance            DONE (iam#49)
    administrator:read/write/approve   DONE (iam#50, iam#51): optional, privileged, human admin client only
    ADA-07 step-up / assurance         IMPLEMENTED (shared#192, cp#249, shared#195, cp#252): trusted acr 3 or webauthn/hwk amr; CRITICAL stays PROHIBITED. IAM passkey step-up (raw LoA 3) is iam#52, OPEN and blocked by a base-image CVE gate; no real passkey login has been driven
    shadow blind spots                 operations routes closed (cp); organisation ancestry via TenantOrganisationMapping
    shadow evidence / readiness        IMPLEMENTED (shared#193, cp#250); exit criteria APPROVED 2026-10-02 (shared#195, cp#252): 14 observed UTC days / 100 decisions / 0 narrower, not-evaluated, unresolved-or-error; no evidence collected yet
    grant population                   tooling only (cp#251): the reviewed list is Platform Security / CP Governance's to supply; approved_by must be a real accountable human principal
    per-permission enforcement         MECHANISM IN PLACE (cp#251), EMPTY: `enforced: []`, no permission enforced, NOT AUTHORISED YET; CRITICAL PROHIBITED
    realm-role retirement              NOT AUTHORISED

EA-06 Event Fabric                     PARTIAL      (plan §44, not re-audited)
  event context registry               READY (ADR-SHARED-018; 29 contexts)
  event-type registry                  READY (124 types: 107 ACTIVE, 17 PROPOSED)
  Trade legacy event migration         T-COMPAT-03 MERGED (trade#111); no com.nabhold in event code; legacy migrations immutable
  Broker/relay/inbox/replay            OPEN
EA-09A Pre-deployment certification    NOT COMPLETE
EA-10 Observability                    PARTIAL      (plan §44, not re-audited)
EA-11 Recovery Engineering             NOT COMPLETE
EA-12 Console                          FOUNDATION
EA-13 Regulations                      DECIDED — Option B; step 1 ADR review drafted (g-reg-ns-adr-review.md), nothing accepted; follow-through open

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
| 2 | Contract convergence audit and lock remediation | Done | Lock schema, check and drift report shared#157; canonical locks on all 8 consumers (cp#229, iam#47, cms#19, pulse#28, trade#114, erp#46, subscriptions#21, payments#16); all 8 pass the enforced check at Shared 739f0ca; ERP semantic convergence proven by an exact-pin suite (erp#43 to erp#46); remaining BEHIND_CHANGED pins re-pin by explicit PR with each engine's compatibility tests ([EA-01 record](ea-01-contract-convergence.md)) |
| 3 | `identity.workload-token.issue` provider neutrality | Done | shared#151 |
| 4 | Complete IAM #42 | Done | iam#42 |
| 5 | Shared #148 lifecycle semantics | Done | shared#148 |
| 6 | IAM provider declaration | Planned-only | iam#45; support waits on M2–M4 evidence |
| 7 | CMS provider declaration and contract lock | Done | cms#17, cms#19 |
| 8 | Foundation provider-declaration validation | Done (enforcing) | shared#152, #153, #154 |
| 9 | Finalise/accept EngineRelease architecture | Done | cp#228 (ADR-BCP-025 A1–A4) |
| 10 | Implement EngineRelease | ER-01…05 implemented; operational proof open | ER-01 contracts; ER-02 record and read (shared#169, #170, cp#233); release approval (shared#171, cp#235); ER-03 (shared#173, cp#237); ER-04 (shared#178, cp#239); ER-05 (cp#240, cp#242, cp#243); ER-06 a separate gate, disabled |
| 11 | DeploymentObservation model/interfaces | Intake merged; not operationally proven | ER-01 contracts; ER-04 (shared#178, cp#239). Production evidence waits on the gates in [er-04-production-gates.md](er-04-production-gates.md) |
| 12 | Provider activation Changeset | Done | DRAFT-only registration and PROVIDER_ACTIVATION (shared#167, #168, cp#231, cp#232); binding integrity (cp#234). Release approval (cp#235) lets a release be APPROVED and a provider be activated without direct SQL |
| 13 | AdministrativeGrant enforcement | Machinery built; evidence phase not begun; flip not authorised | Staged path in roles-to-grants-decision.md; ADA-05/06/07, readiness, population check and enforcement gate merged; `enforced: []` |
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
| Workload registry in production CP | Mandatory and fail-closed; ACTIVE lifecycle enforced for every inbound workload after the existing ACTIVE entries are reconciled | [er-04-production-gates.md](er-04-production-gates.md) |
| ADR-BCP-025 reporter | Infrastructure deployment controller and runtime observer, federated, no static secret; no admission webhook (production is ECS/Fargate, EKS deferred); PROVISIONED until proven | [er-04-production-gates.md](er-04-production-gates.md) |
| Event context governance | ADR-SHARED-018 Accepted; `erp` DEPRECATED, `payments` kept, fulfilment/logistics/trade.shipment distinct, Regulations owns classification and assessment, `thamani-*` retired in T-COMPAT-03 | shared#161 |

Still open, and not to be decided in code: the roles→grants *flip* (the migration path is accepted;
`authority:self` is issued, iam#49); tenant suspend/activate routes; OEV-02 storage and regions;
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

## Open corrections (audit of 2026-10-02)

| # | Correction | State |
|---:|---|---|
| 1 | Provider-neutral identity assurance contracts must not force `amr` (ACR-or-AMR, no SPI) | This change: `AuthenticationAssurance.amr` optional, `AssuranceRequirement.accepted_acr_values` added, `accepted_methods` optional, behaviour validated |
| 2 | CP consumes shared#195 | DONE (cp#252, pin `a503649`) |
| 3 | IAM consumer lock must cover the scopes IAM issues; every Baobab-defined scope IAM issues must exist in the exact pinned scope registry | DONE (iam#52: pin `a503649`, `check-issued-scopes.sh`, integration sections 9b, 19, 19b) |
| 4 | iam#52 (passkey step-up) is blocked by the Foundation container scan: Keycloak 26.7.4 ships jackson-core 2.21.5 (CVE-2026-89407, CVE-2026-89425, fixed in 2.21.7). Not weakened, not merged. `main` fails the same scan | DONE: upstream Keycloak 26.7.5 (iam#53) pinned by digest `sha256:37dbaf6f…475a85` (R-1 closed); the Bouncy Castle, FreeMarker and Jackson overrides were removed after CI showed the image vendors 1.86, 2.3.35 and 2.21.7 (server and admin CLI); container scan green; iam#52 then merged with no waiver |
| 5 | ERP semantic convergence (Trade-style census, reconciliation, exact-pin suite, re-pin) | DONE (erp#43 to erp#46; evidence in the EA-01 record). Residual ERP operational items are rows 7 to 10 |
| 6 | Reconcile this page and the historical sections of roles-to-grants-decision.md | DONE for the 2026-10-02 reconciliation; re-reconciled in this change for EA-01 |
| 7 | ERP Boundary API: `POST`/`GET /provisioning-operations`, `GET /order-consequences/{id}`, `GET /inventory-availability` answer 501 | OPEN: needs a Control Plane assignment source and finance baseline, a consequence read model, an iDempiere stock query |
| 8 | ERP delivers no events: domain recorders still emit legacy-shaped events with iDempiere native ids, stored `held` | OPEN: outcome projection to the registered `erp.*` events |
| 9 | ERP OpenAPI declared no 400 on the two mapping reads and no 501; ERP tracked them in `KNOWN_UNDECLARED` | CLOSED: OpenAPI 1.0.1 (shared#198, `92accac`) declares them; ERP pinned it (erp#47, `a672a64`), deleted `KNOWN_UNDECLARED`, and its exact-pin conformance fails on any undeclared status. The 501s remain a capability-absent signal, not readiness (row 7) |
| 10 | Baobab IAM grants ERP workloads only `erp:integrate`; the Boundary API needs `erp:read`/`erp:provision` and a `tenant_id` claim | OPEN: owner grant (not made here) |
