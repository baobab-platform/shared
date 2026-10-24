# Baobab IAM — ADR-to-Capability Implementation and Strategic Assessment

**Assessment ID:** BA-AUD-2026-10-24-IAM-01  
**Observed:** 24 October 2026 (Africa/Johannesburg)  
**Status:** **ADVISORY ASSESSMENT** — a dated source/CI evidence review, **not** an Accepted ADR, new gate, certification, provider registration, activation or production release authorisation.  
**Accountable domain for remediation:** Baobab IAM engineering; CP, Shared, Infrastructure, Security and the relevant Digital Estate retain their own existing authority. Suggested owners below are not appointments.  
**Primary assessed main:** [baobab-iam `0ad103606b9705fcb33c468ea01b54d8ce76f9ae`](https://github.com/baobab-platform/baobab-iam/commit/0ad103606b9705fcb33c468ea01b54d8ce76f9ae), merged via [IAM #138](https://github.com/baobab-platform/baobab-iam/pull/138), 23 October 2026.  
**Related programme baseline:** [Shared EA v2.3](../../architecture/EA-implementation-plan-v2.3-2026-10-20.md), [Accepted EA-DEV](../../architecture/ea-v2.3-development-enablement-implementation-plan-2026-10-23.md), [EA-REL](../../architecture/ea-v2.3-progressive-production-release-programme-2026-10-23.md), [Shared ADR-043](../../adr/ADR-SHARED-043-Development-Provisioning-and-Environment-Approval-Boundaries.md).  
**Tracking:** [Shared stable findings register](../findings-register.md), new findings **BA-AUD-015–BA-AUD-028**; overlap cross-references existing **BA-AUD-001, 002, 003, 008 and 009**.  
**Reassess when:** Infrastructure INT-02/DEV-02 becomes current-head green, DEV-03/C4-03 real issuer–CP–consumer evidence arrives, an IAM support declaration is legitimately promoted, or a new protected release is qualified.

## 1. Executive assessment

**Baobab IAM has an advanced, functioning engineering foundation but has not yet demonstrated a fully qualified enterprise identity service.** It has provider-neutral Go interfaces, a native Ory Kratos identity adapter, Ory Hydra workload/OAuth implementation, substantial Keycloak OIDC/SAML enterprise federation, governed CP mapping and runtime-reader code, durable federation trust state and security-negative tests. Its latest inspected source CI is green.

**The most important unfinished capability is the complete IAM → current CP authority → protected resource → Digital Estate journey**, including authentic issued bearer tokens, canonical Principal mapping, audience/grant resolution, revocation while credentials are unexpired, isolation, exact receipts and supervised teardown. A source-merged adapter, fixture-only conformance test, positive Keycloak broker exercise and an Accepted ADR are **not** production readiness.

**Authoritative allocation under [Accepted ADR-IAM-0033](https://github.com/baobab-platform/baobab-iam/tree/0ad103606b9705fcb33c468ea01b54d8ce76f9ae/docs/adr):** Kratos provides native human authentication/credentials/sessions; Hydra provides OAuth/OIDC and workloads; Keycloak remains the permanent initial enterprise OIDC/SAML federation and SSO provider. IAM proves authentication; CP owns canonical identity/context/entitlement; domain engines authorise business operations. No provider-local organisation or role is a CP Tenant/mandate/business grant.

The source [provider declaration](https://github.com/baobab-platform/baobab-iam/blob/0ad103606b9705fcb33c468ea01b54d8ce76f9ae/.baobab/capability-provider.yaml) deliberately retains **all three declared supports as PARTIAL**, including the otherwise advanced Keycloak broker. Shared does not register PARTIAL support. Its `production_permitted: true` describes prospective eligibility, **not** acceptance or activation.

## 2. Scope, evidence and explicit limitations

Inspected: IAM's ADR index and original ADR-0001–0018 plus Accepted ADR-IAM-0019–0033 and Proposed ADR-IAM-0034; [IAM capability matrix](https://github.com/baobab-platform/baobab-iam/blob/0ad103606b9705fcb33c468ea01b54d8ce76f9ae/docs/governance/iam-capability-matrix.md), [machine-readable matrix](https://github.com/baobab-platform/baobab-iam/blob/0ad103606b9705fcb33c468ea01b54d8ce76f9ae/.baobab/iam-capability-matrix.yaml), provider declaration, [MP0–MP20 status](https://github.com/baobab-platform/baobab-iam/blob/0ad103606b9705fcb33c468ea01b54d8ce76f9ae/docs/governance/iam-mp-programme-status.md), [execution evidence](https://github.com/baobab-platform/baobab-iam/blob/0ad103606b9705fcb33c468ea01b54d8ce76f9ae/docs/governance/iam-33-execution-evidence.md), relevant Go source packages, tests, operation runbooks, recent merged PRs, main CI and selected Infrastructure interoperation.

CI inspected at immutable IAM main `0ad103606b9705fcb33c468ea01b54d8ce76f9ae`:
- [IAM CI run 39920911473](https://github.com/baobab-platform/baobab-iam/actions/runs/39920911473) — **SUCCESS**, including `enterprise-federation-live`, `federation-postgres`, Go build/tests and integration variants.
- [Ory Foundation Live run 39920911523](https://github.com/baobab-platform/baobab-iam/actions/runs/39920911523) — **SUCCESS** for released and audience-backport matrix branches; candidate success must not be confused with general vendor-release portability.
- [Foundation run 39920912944](https://github.com/baobab-platform/baobab-iam/actions/runs/39920912944), [security/secret scan 39920912150](https://github.com/baobab-platform/baobab-iam/actions/runs/39920912150) — **SUCCESS**, with standard inapplicable jobs skipped.
- [Infrastructure #54](https://github.com/baobab-platform/infrastructure/pull/54) checked at `bd181655bf8b2c64420beeeab72129f9811df3bc`: **OPEN**; [INT-02 run 40058049607](https://github.com/baobab-platform/infrastructure/actions/runs/40058049607) **FAILED** in actual human-login proof, status 500. Its independent CI/F4/DEV-01 successes cannot override the INT-02 failure. See existing **BA-AUD-001**.

**Not performed:** deployment or independent CP/provider login, penetration test, complete source-line security audit, production IAM/CP/estate case execution, independent legal/person vetting, provider certification, cloud HA/failover or backup restoration. Findings state **NOT_QUALIFIED in inspected evidence**, not that the operation is impossible. Old runbook statements are historical until a current receipt supersedes them.

## 3. Normative ADR reconciliation

| ADR set | Recorded document status | Treatment in this assessment |
| --- | --- | --- |
| Original ADR-0001–0018 | Individual files retain **Proposed** status at checked revision | Historic architectural baseline and domain requirements as expressly preserved by Accepted successors, **not** independently Accepted merely by being indexed |
| ADR-IAM-0019–0032 | **Accepted** | Provider-neutral migration, contracts, Kratos/Hydra, browser/BFF, assurance, identity proofing, federation, multi-region, keys, security, privacy, administration and production operations |
| ADR-IAM-0033 | **Accepted**, 4 Oct 2026 | Governing three-provider assignment; **partially supersedes** 0019 and 0022 and amends provider-specific interpretations of 0020/21/26–32. **Does not reinstate** superseded ADR-0002 as universal Keycloak authority |
| ADR-IAM-0034 | **Proposed**, 23 Oct 2026 | Source rule for native commitment server workload implementing Accepted Shared ADR-042 Decision 9; no client/scope allocation or connected acceptance |

The [older consolidated technical specification](https://github.com/baobab-platform/baobab-iam/blob/0ad103606b9705fcb33c468ea01b54d8ce76f9ae/docs/adr/Consolidated-Technical-Specification.md) still describes a Keycloak-centred target and Thamani B2C. It is historical where newer accepted decisions conflict. Make the precedent clear in future IAM navigation rather than silently altering original signed-off text.

## 4. Capabilities declared by IAM

The checked [matrix](https://github.com/baobab-platform/baobab-iam/blob/0ad103606b9705fcb33c468ea01b54d8ce76f9ae/.baobab/iam-capability-matrix.yaml) contains **15 operation rows**. The source matrix records fourteen as Partial, while the enterprise federation operation claims **implemented bounded OIDC/SAML integration** with production acceptance still outstanding. The three **published provider supports**, a narrower surface than these fifteen operations, all remain PARTIAL.

Classification matters: only `identity.authentication.perform` and `identity.workload-token.issue` are listed as **PLATFORM_RESOLVABLE_CAPABILITY** under the inspected Shared pin; other matrix operations are IAM management, candidate-platform or provider-internal. The matrix does **not** allocate runtime instances, create CP activation or grant a new platform key.

| Operation (exact matrix name) | Class | Source / CI evidence | Highest justified finding | Remaining exit evidence |
| --- | --- | --- | --- | --- |
| `identity.authentication.perform` | Platform-resolvable | [Kratos adapter](https://github.com/baobab-platform/baobab-iam/blob/0ad103606b9705fcb33c468ea01b54d8ce76f9ae/internal/provider/ory/kratos.go), [human handoff](https://github.com/baobab-platform/baobab-iam/blob/0ad103606b9705fcb33c468ea01b54d8ce76f9ae/internal/provider/ory/human_handoff.go), Ory foundation CI | PARTIAL: native mechanics and guarded handoff; Keycloak separate broker implementation | Current CP mapping, full native login/BFF and cross-tenant/step-up denials |
| `identity.workload-token.issue` | Platform-resolvable | [Hydra](https://github.com/baobab-platform/baobab-iam/blob/0ad103606b9705fcb33c468ea01b54d8ce76f9ae/internal/provider/ory/hydra.go), [canonical workload response](https://github.com/baobab-platform/baobab-iam/blob/0ad103606b9705fcb33c468ea01b54d8ce76f9ae/internal/provider/ory/workload_response.go), Ory CI | PARTIAL: real Hydra/candidate and fixture verifier mechanics | Current registered CP runtime, workload support, signed issuer, correct audience, live consumer and still-unexpired revoke |
| `identity.human.provision` | IAM management | Kratos create/import methods, migration bridge, provider tests | PARTIAL source | Complete approved provisioning/import and actual lifecycle readback |
| `identity.human.disable` | IAM management | Kratos activation and [kill switch](https://github.com/baobab-platform/baobab-iam/blob/0ad103606b9705fcb33c468ea01b54d8ce76f9ae/internal/provider/killswitch.go) | PARTIAL source | Provider disable + CP membership/grant removal; no orphan sessions |
| `identity.authentication.assurance` | Candidate | [human token profile](https://github.com/baobab-platform/baobab-iam/blob/0ad103606b9705fcb33c468ea01b54d8ce76f9ae/internal/tokenprofile/human.go), browser password/TOTP and disposable Chromium passkey evidence, [#119](https://github.com/baobab-platform/baobab-iam/pull/119)/[#122](https://github.com/baobab-platform/baobab-iam/pull/122) | PARTIAL; browser/security mechanisms tested | Normalized assurance and estate-authorized step-up across actual current provider chain |
| `identity.session.revoke` | IAM management | Kratos revoke and logout/kill-switch code | PARTIAL source | Current federated + native logout/revoke proof with live unexpired credentials |
| `identity.token.issuance` | Candidate | Hydra issued-token projection, request and consent controls | PARTIAL; source and isolated integration | End-to-end OAuth/OIDC lifecycle, registered audience, consumer and operational acceptance |
| `identity.workload.provision` | IAM management | Hydra client creation, RFC 7523/JWT federation, disable/rotate code | PARTIAL source | Approved real workload/admission, rotation, termination and revocation readback |
| `identity.federation.enterprise` | Candidate | [Keycloak adapter](https://github.com/baobab-platform/baobab-iam/blob/0ad103606b9705fcb33c468ea01b54d8ce76f9ae/internal/provider/keycloak/enterprise.go), [real broker tests](https://github.com/baobab-platform/baobab-iam/blob/0ad103606b9705fcb33c468ea01b54d8ce76f9ae/internal/provider/keycloak/enterprise_live_test.go), [#75](https://github.com/baobab-platform/baobab-iam/pull/75), PostgreSQL [#77](https://github.com/baobab-platform/baobab-iam/pull/77), dispatch [#80](https://github.com/baobab-platform/baobab-iam/pull/80) | **BOUNDED IMPLEMENTED** OIDC/SAML federation; declared PARTIAL platform support | Actual BFF→CP→domain consumer and enterprise estate adoption; operational/production certificate and rotation |
| `identity.recovery.perform` | IAM management | Kratos recovery mechanisms and ADR-0025 policies | PARTIAL | Real recovery, throttling, account rebinding, proofing and downstream authority safeguards |
| `identity.security.revoke` | IAM management | kill-switch, independent trust containment, durable event/replay records | PARTIAL | Cross-provider coordinated containment, audit and disaster recovery drill |
| `identity.human.anonymise` | IAM management | Provider lifecycle/data minimisation contracts and policy | PARTIAL | Retention/erasure, legal holds, cross-provider privacy and audit lineage proved |
| `identity.migration.ledger` | IAM management | [migration state machine](https://github.com/baobab-platform/baobab-iam/blob/0ad103606b9705fcb33c468ea01b54d8ce76f9ae/internal/migration/service.go), bridge and ledger tests | PARTIAL | Real issuer/subject dual-run cutover, rollback and retained-Keycloak federation invariant |
| `identity.provider.ready` | Provider-internal | [C4-04 readiness](https://github.com/baobab-platform/baobab-iam/blob/0ad103606b9705fcb33c468ea01b54d8ce76f9ae/docs/operations/c4-04-governed-runtime-readiness.md), health and current CP runtime checks | PARTIAL observational readiness | Independent CP owner activation, deployed profile/artifact certification and resumption/outage evidence |
| `provider.adapter.normalize` | Provider-internal | [provider interfaces](https://github.com/baobab-platform/baobab-iam/blob/0ad103606b9705fcb33c468ea01b54d8ce76f9ae/internal/provider/provider.go), Keycloak/Ory adapters, canonical normalization tests | PARTIAL | Complete conformance across supported functions, real callers and portability/regression |

**Do not promote these candidate/management/provider-internal rows into Shared's canonical capability catalogue based on this assessment alone.**

## 5. Accepted ADR-IAM-0033 MP0–MP20 gate assessment

This reconciles historical IAM's [programme status](https://github.com/baobab-platform/baobab-iam/blob/0ad103606b9705fcb33c468ea01b54d8ce76f9ae/docs/governance/iam-mp-programme-status.md) with recent merged source. `Advanced` here is source maturity, not a new official gate state.

| Gate | Observed implementation | Acceptance still outstanding |
| --- | --- | --- |
| MP0 baseline | Reconciled source inventory | Owner-approved operational census |
| MP1 ownership | Capability matrix and provider allocation implemented | Registered, real runtime support is distinct |
| MP2 shared/CP authority | Contracts, scoped CP reader, governed federation authority and mapping consumption built | Current deployed composition and accepted consumer |
| MP3 registry/profiles | Provider declaration, publication preflight and CP profile-read clients implemented | Three PARTIAL declarations block canonical registration; exact approved runtime profile/active support |
| MP4 resolution/dispatch | CP runtime reads, enterprise dispatch and C4-01/02 compositions implemented | Current registered native/workload provider binding, controlled activation and consumer |
| MP5 Kratos | Lifecycle, session, native challenge and guarded handoff implemented in part | Whole credential/proofing/MFA/session/BFF workflow conformance |
| MP6 Hydra | OAuth/workload, RFC 7523, audience/profile tests and supervised disposable clients | Current issuance → protected consumer M4-F, authentic revoke |
| MP7 Keycloak reduction | Permanent federation-only allocation decided | Per-capability legacy-native retirement, census and rollback |
| MP8 federation | Real Keycloak OIDC and SAML brokering CI **passes** | Accepted estate and production conformance |
| MP9 FederationTrust | Durable trust revisions, independent review rules, replay/containment tested | Actual protected provision, governance and rotation |
| MP10 login discovery | Governed broker selection/route | Tenant-neutral native/federated discovery and browser selection |
| MP11 canonical normalization | Exact upstream issuer+subject to CP consumption bounded integration | Actual estate Principal/context resolution; no email linking |
| MP12 assurance | Signed OIDC/SAML proof validation and bounded A1–A3 normalization | Real estate step-up; cannot assert A4 from federation |
| MP13 SCIM | Intent and independent-provider boundary specified | Provider decision, portable lifecycle conformance, no domain role grants |
| MP14 events | Durable event/replay ledgers exist | Cross-provider correlation, stale-state/drift reconciliation and security event coverage |
| MP15 cryptography | Private credentials, signing verification and source-side isolation | Deployed rollover/overlap/compromise, secret/certificate revocation drills |
| MP16 HA/DR | PostgreSQL recovery epoch/fencing and integration tests exist | Approved multi-replica failover, restoration, residency and measured RPO/RTO |
| MP17 estate integration | Per-estate fixture/profile construction and login controls advancing | Nabhold, ZuriBeans, Thamani complete native/federated BFF/CP journeys |
| MP18 migration | Capability-aware ledger and rollback scaffolding | Dual-run/cutover acceptance; retain Keycloak federation, no global delete |
| MP19 security certification | Protocol negatives, race, image/scanning and provider CI | Cross-provider incident, resilience, revocation and security certification |
| MP20 production acceptance | Runbooks, image workflow and evidence hooks | Protected stage/prod rollout, owner approval, monitoring/SLO/recovery and consumer acceptance |

## 6. Critical-path tests and runtime qualification gaps

**C4-03 (real provider and CP):** [IAM source runbook](https://github.com/baobab-platform/baobab-iam/blob/0ad103606b9705fcb33c468ea01b54d8ce76f9ae/docs/operations/c4-03-live-qualification.md) explicitly labels B–E acceptance outstanding:
- A: current CP context and native/workload capability/profile reads (executable);
- B: real Hydra hook, correctly scoped signed token and revoked issuance;
- C: live Kratos session + Hydra login/consent challenge + current CP context + replay fence;
- D: running CP protected resource, cross-Tenant refusal and unexpired-bearer withdrawal;
- E: complete bounded receipts, independent verification and environment-specific acceptance.

**C4-04:** [readiness runbook](https://github.com/baobab-platform/baobab-iam/blob/0ad103606b9705fcb33c468ea01b54d8ce76f9ae/docs/operations/c4-04-governed-runtime-readiness.md) distinguishes C4-04A, a source-implemented observational check, from C4-04B canonical support/CP activation and C4-04C actual consumption, revocation, outage and recovery. Do not infer availability from admin-health or bypass a failed read with another provider.

**EA-DEV:** This IAM gap overlaps existing **BA-AUD-002 (DEV-03/04)** and **BA-AUD-003 (DEV-05/06)**. [Infrastructure #54](https://github.com/baobab-platform/infrastructure/pull/54) and its [INT-02 failure](https://github.com/baobab-platform/infrastructure/actions/runs/40058049607) remain **BA-AUD-001**, not an unrelated new IAM bug. Correct DEV-02 synthetic fixtures and DEV-03/04 are permitted within [ADR-SHARED-043](../../adr/ADR-SHARED-043-Development-Provisioning-and-Environment-Approval-Boundaries.md)'s isolated-development rules; actual protected stage/prod approvals remain separately mandatory.

## 7. Specific IAM findings / opportunities — stable register IDs

The full triage, recommended owners and closure definitions live in [the Shared findings register](../findings-register.md). This assessment is the immutable originating snapshot.

| Finding | Category | Evidence / interpretation | Proposed action |
| --- | --- | --- | --- |
| **BA-AUD-015** | P0 observed readiness gap | Three provider supports PARTIAL; Shared publication excludes them | Complete per-contract real conformance before CP source registration/support promotion |
| **BA-AUD-016** | P0 observed qualification gap | C4-03B–E and C4-04B/C lack current connected receipts | Qualify issuer/session/token/CP/resource, negatives, unexpired revocation and exact cleanup |
| **BA-AUD-017** | P0 observed adoption gap | Kratos→Hydra→CP current native BFF/step-up not estate accepted | End-to-end native login/consent/session/assurance tests against real registered consumers |
| **BA-AUD-018** | P0 observed adoption gap | Hydra workload mechanics advanced; no current registered consumer acceptance | Current audience/issuer/scope proof and real resource denial/revocation |
| **BA-AUD-019** | P0 observed estate gap | MP17 not accepted | Independently qualify Nabhold, ZuriBeans and Thamani journeys; do not infer B2C authority for B2B logistics |
| **BA-AUD-020** | P1 mixed source gap | Provider-neutral login discovery and controlled enterprise handoff unfinished | Complete routing, federation evidence/assurance mapping and current CP Principal in one journey |
| **BA-AUD-021** | P1 missing provider choice | MP13 SCIM/directory remains undecided | Architect portable lifecycle provider selection only when driven by customer requirements |
| **BA-AUD-022** | P1 observed recovery risk | [DR runbook](https://github.com/baobab-platform/baobab-iam/blob/0ad103606b9705fcb33c468ea01b54d8ce76f9ae/docs/operations/disaster-recovery-runbook.md) admits post-backup revocation journal is not automated | Durable security-event replay/reconcile test, prevent revoked access resurrecting after restore |
| **BA-AUD-023** | P1 operational assurance gap | MP15/16/19/20 key rollover, HA/DR, residency, incident and release certification incomplete | Measured approved RPO/RTO, drills, secret/cert rotation, degraded-mode and restore receipts |
| **BA-AUD-024** | P1 migration gap | MP18 cutover and per-capability Keycloak reduction not accepted | Dual-run, binding-specific cutover and rollback; retain Keycloak enterprise SSO |
| **BA-AUD-025** | P2 observed documentation drift | Original Proposed ADRs, old Keycloak-centric consolidated specification, dated 5 Oct MP status, Thamani B2C references | Non-destructive precedence notes and refreshed *reviewed* source/evidence index; no unapproved status promotion |
| **BA-AUD-026** | P1 observed unactivated rule | [Proposed ADR-IAM-0034](https://github.com/baobab-platform/baobab-iam/tree/0ad103606b9705fcb33c468ea01b54d8ce76f9ae/docs/adr) has source test rules only; no trade workload allocated | Approved Shared registry + IAM client + CP assignment and connected Trade acceptance |
| **BA-AUD-027** | P1 broad coverage gap | High-assurance admin, native recovery/proofing, privacy/erasure, delegated support lifecycle lack complete deployed proof | Prioritised threat-model cases and ADR-0024/25/29/30/31 acceptance evidence |
| **BA-AUD-028** | P1 strategic opportunity | Capability source, registered support, current provider and estate readiness are difficult to compare | Build **read-only**, evidence-linked cross-provider capability scoreboard from owner records |

Other cross-cutting issues are intentionally **not duplicated**: [BA-AUD-001](../findings-register.md) (Infrastructure INT-02), BA-AUD-002 (real current IAM/CP), BA-AUD-003 (Nabhold/external), BA-AUD-008 (revocation/outage authority) and BA-AUD-009 (cross-engine evidence joins).

## 8. Strategic direction, sequencing and limits

**Strategic recommendation:** complete *Baobab IAM as a composable, evidence-verified African-enterprise identity service*, not by counting adapters or moving to more identity vendors, but by proving identity and authority continuity across an actual enterprise journey. Preserve native Kratos, Hydra's OAuth/workload remit and permanent Keycloak federation. Do not duplicate CP entitlement or let customer IdP groups become Trade/ERP/CMS permissions.

| Rank | Safe engineering sequence | Owner(s) | Verified exit / no-go boundary |
| --- | --- | --- | --- |
| P0 / first | Close [Infrastructure #54](https://github.com/baobab-platform/infrastructure/pull/54) INT-02 final-head CI and DEV-02 accurate CP fixtures | Infrastructure/CP/IAM | True current-head green integration, private sanitized receipts and teardown; stop on failed real login |
| P0 / second | DEV-03 / IAM C4-03 current issuer and Principal; DEV-04 original seven INT-03C cases | IAM/CP/Infrastructure | Actual signed provider issuance, CP resource, grant/audience negatives, unexpired revocation, tenant denial and verifier receipts |
| P0 / third | C4-04B/C scoped canonical support publication, CP owner-controlled activation and real consumer | IAM/CP/Shared/consumer | Complete specific canonical contract and current support/instance/profile, not `PARTIAL` promotion by assertion |
| P0 / parallel | DEV-05 / MP17 Nabhold, ZuriBeans and Thamani authentic BFF/CMS/Trade estate paths | IAM/CMS/Trade/estate owners | Positive/negative estate-authorized cases; historical B2C docs do not confer new B2B permissions |
| P1 / parallel | Unexpired session/workload revocation; protected restore-safe security journal, key rotation, containment | IAM/Security/Operations/Infra | Applicable recovery/incident drills and distinct protected authority |
| P1 / later | SCIM/directory, per-capability Keycloak cutover, multi-region SLO and provider portability | Architecture/IAM/Operations | Actual customer need, approved provider/region scope, migration/rollback and operational receipts |

**Do not add** a new global IAM role system, a replacement central policy store, automatic provider failover or an unverified SCIM product just to increase feature count. Any new operation promoted to Shared canonical contract requires a separate authorised contract decision and consumer compatibility tests.

**Recommended reporting improvement (not an architectural decision):** for each existing capability display one joined read-only projection: provider allocation, Shared catalogue key/major, IAM implementation support status, CP registered/current support and binding, latest concrete positive/negative evidence receipt, estate acceptance, security domain, protected environment scope, and stale/revalidation marker. Keep owner records and expiry authoritative.

## 9. What changed versus earlier audit evidence

| Topic | Earlier dated programme snapshot | 24 Oct assessment from IAM main | What cannot be inferred |
| --- | --- | --- | --- |
| MP8 federation | [5 Oct programme status](https://github.com/baobab-platform/baobab-iam/blob/0ad103606b9705fcb33c468ea01b54d8ce76f9ae/docs/governance/iam-mp-programme-status.md) already recognised real Keycloak broker, PostgreSQL and CP composition | Current main still includes these; CI enterprise and Postgres tests green | No accepted estate/certificate or production SSO |
| Native/workload composition | Older MP programme docs describe incomplete MP4 C4 | [#120–123](https://github.com/baobab-platform/baobab-iam/pull/123) and [#126](https://github.com/baobab-platform/baobab-iam/pull/126) added CP reader, supervised composition, qualification runner and readiness tests | Source-built runners do not prove C4-03B–E live success |
| Buyer/browser controls | Earlier foundation/enterprise evidence | [#119](https://github.com/baobab-platform/baobab-iam/pull/119), [#122](https://github.com/baobab-platform/baobab-iam/pull/122), [#134](https://github.com/baobab-platform/baobab-iam/pull/134), [#136](https://github.com/baobab-platform/baobab-iam/pull/136) now include browser/MFA/passkey and buyer token/consent safeguards | No final Nabhold/ZuriBeans/Thamani estate integration acceptance |
| INT-03C clients | Earlier optional approval holds applied | [#135](https://github.com/baobab-platform/baobab-iam/pull/135), [#137](https://github.com/baobab-platform/baobab-iam/pull/137) implement supervised disposable owner/verifier safeguards under current development permissions | No current seven-case acceptance receipt |
| Native commitment identity | Not in initial MP matrix | [#138](https://github.com/baobab-platform/baobab-iam/pull/138) + Proposed IAM-0034 source rule | No allocated workload scope, CP assignment, activated Trade native commitment |
| Cross-repository INT-02 | Historic partial/integration receipts | Infrastructure #54 still has failing real IAM/CP run at observed head | Cannot claim DEV-03/04 complete from IAM green CI |

A count of closed PRs is not an SLO and a decrease in outstanding checkboxes is not sufficient evidence of end-user improvement. Measure current trusted login completion, revocation delay, cross-tenant denials, provider failover/restore effects, issuer-to-consumer lead time, audit traceability, accessible BFF UX and integration/operator recovery effort.

## 10. Evidence links and next assessment

Canonical owning references: [IAM ADR index](https://github.com/baobab-platform/baobab-iam/blob/0ad103606b9705fcb33c468ea01b54d8ce76f9ae/docs/adr/README.md), [ADR-IAM-0033 implementation plan](https://github.com/baobab-platform/baobab-iam/blob/0ad103606b9705fcb33c468ea01b54d8ce76f9ae/docs/governance/iam-mp-implementation-plan.md), [MP0–20 execution dossier](https://github.com/baobab-platform/baobab-iam/blob/0ad103606b9705fcb33c468ea01b54d8ce76f9ae/docs/governance/iam-33-execution-evidence.md), [C4-03 real qualification](https://github.com/baobab-platform/baobab-iam/blob/0ad103606b9705fcb33c468ea01b54d8ce76f9ae/docs/operations/c4-03-live-qualification.md), [C4-04 readiness](https://github.com/baobab-platform/baobab-iam/blob/0ad103606b9705fcb33c468ea01b54d8ce76f9ae/docs/operations/c4-04-governed-runtime-readiness.md), [shared federation storage](https://github.com/baobab-platform/baobab-iam/blob/0ad103606b9705fcb33c468ea01b54d8ce76f9ae/docs/operations/federation-shared-storage.md), [migration rollback](https://github.com/baobab-platform/baobab-iam/blob/0ad103606b9705fcb33c468ea01b54d8ce76f9ae/docs/operations/migration-rollback-baseline.md), [IAM DR runbook](https://github.com/baobab-platform/baobab-iam/blob/0ad103606b9705fcb33c468ea01b54d8ce76f9ae/docs/operations/disaster-recovery-runbook.md), and immutable CI runs above.

A future assessment shall first revalidate the current IAM, Infrastructure and CP merge SHAs, separately inspect original case receipts and protected environment evidence, and update the stable BA-AUD findings only after exact verified closure. Do not overwrite this 24 October snapshot with later claims.

---

**Judgement:** The IAM codebase is well beyond scaffolding; its remaining competitive leverage comes from qualified provider-neutral integration, enterprise adoption, revocation-safe operations and measurable reliability. **Source-green ≠ support-registered ≠ live-consumer-qualified ≠ protected production-approved.**
