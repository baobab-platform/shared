# EA v2.1 — Comprehensive implementation audit, 13 October 2026

**Scope:** EA Implementation Plan v2.1, ADR-BCP-026/027, Control Plane frontend, public landing page, IAM and dependent engines.  
**Shared baseline:** `5dcff30` (shared#300).  
**Nature:** A code-and-repository audit, not an inspection of every deployed runtime. Each status reflects the strongest evidence found for it.  
**Cross-repository evidence:** The audit reports the PR numbers cited for baobab-cp, Trade, ERP, Payments and Subscriptions. They were **not re-verified from Shared** when this record was written.  
**Live status:** [EA v2.1 register](ea-dashboard.md). This page is the dated audit, and the register records how each finding has been acted on since.

## 1. Executive assessment

Implementation has advanced materially since the 4 October checkpoint, but Baobab is **not ready for unrestricted production onboarding**.

These areas have substantial implementations:
- Organisation-first tenancy
- progressive admission
- legal-actor governance
- frontend integration

The audit separates two things: functionality **merged** into repositories, and functionality **proven** across a live, authorised operating environment.

**Governance finding (D-01).** The v2.1 reconciliation plan was still labelled a proposed revision, while `ea-dashboard.md` named v2.0 as the governing plan and was last updated on 4 October. That dashboard was not a reliable current register. *Acted on 2026-10-13:* v2.1 is Accepted and the dashboard has been replaced (see the register).

**Landing page and Console.** CP #360 fixed the missing navigation and the `/start` 404. The public routes are now:

| Route | Purpose |
|---|---|
| `/` | Get started, Console login and Sign up |
| `/start` | Onboarding guide |
| `/login` | IAM sign-in entry |
| `/signup` | Access-request guidance |

The authenticated Console is at `/workspace`, with Applications, Governance, Organisations, Tenants and Provisioning.

**Verdict on the landing page and Console:** *code-integrated, not live end-to-end certified.* Component tests show the links render. They do not show that a deployed browser completes sign-in, returns to the right workspace and carries out an authorised workflow.

## 2. Progress since the previous audit (as reported)

| Area | Reported merge | Remaining qualification |
|---|---|---|
| Organisation 360° mandate restrictions | CP #379; Shared [#297](https://github.com/baobab-platform/shared/pull/297) | Recorded scope is descriptive. Every operation still needs fresh legal-actor authorisation |
| Applicant and Tenant Console | CP #377, #378 | Real sign-in, human approval, multi-browser acceptance |
| Scanner admission | CP #380, #381; Shared [#281](https://github.com/baobab-platform/shared/pull/281), [#298](https://github.com/baobab-platform/shared/pull/298) | A scanner that runs independently, and an issued workload identity |
| Durable document custody (P0-02C) | CP #382 (migration 000124, S3 Object Lock/KMS, retention, key rewrap, orphan recovery) | An approved bucket and KMS key deployed, a retention policy in operation, the scanner activated, custody accepted live |
| Trade contracts | Trade #145; Shared [#300](https://github.com/baobab-platform/shared/pull/300) | Native protected checkout, provider certification |
| ERP contracts | ERP #95 | Native finance execution live, a trusted workload/provider, proof of historical attribution |
| Payments contracts | Payments #36 | A real merchant, PSP, settlement and protected runtime acceptance |
| Subscriptions contracts | Subscriptions #40 | Protected billing/usage executed for real, provider integration |

**P0-04A** (contract convergence) has advanced through Trade, ERP, Payments and Subscriptions. **Trade Docs** is the last consumer still to converge.

These merges **do not certify** transactions in the owning engines. The next work is **P0-04B**: enforcement at the native execution point.

## 3. Workstream assessment

| Workstream | Assessment | Gap |
|---|---|---|
| EA-01 Canonical contracts | Substantially implemented | Trade Docs convergence, consistent pins in the remaining consumers, live semantic acceptance |
| EA-02 Capability catalogue and providers | Partial | Real provider admission, active bindings, legal restrictions at runtime, certification per capability |
| EA-03 EngineRelease and topology | Substantial foundation | Genuine release observations, deployment reconciliation, protected failover |
| EA-04 IAM/workload identity | Partial | Active scoped workload credentials, live revocation, acceptance of the issuer and federation |
| EA-05 CP governance | Substantial | Real founding-group decisions, external evidence, complete operator workbenches |
| EA-06 Event fabric | Partial | Proof of cross-engine replay, redaction, durable delivery and recovery |
| EA-09A Pre-deployment conformance | Partial | Independent acceptance of security and providers across engines |
| EA-09B Operational certification | Not demonstrated | Protected staging, external certification, signed operational go/no-go |
| EA-10 Observability | Partial | Deployed trace correlation from admission through native transaction and recovery |
| EA-11 Recovery engineering | Partial | Live drills for backup/restore, key rotation, event replay and rollback |
| EA-12 Console and Digital Estates | Console substantial; estates uneven | Browser acceptance, advanced workbenches, readiness of the founding estates |
| EA-13 Regulatory architecture | Substantial reference implementation | Accepted real requirement sources, trust, and integration of runtime applicability |

EA v2.0 and v2.1 do not define EA-07 and EA-08 as workstreams like the others, so the audit gives them no status.

**Architectural conformance:**

| Property | Status |
|---|---|
| Organisation-first tenant identity | Conforms |
| Subsidiary operational autonomy | Conforms |
| Scope-bound operating legal actor (mechanisms) | Conforms |
| Independently verified real legal authority | Outstanding |
| Protected multi-engine acceptance | Outstanding |

## 4. ADR-BCP-026 gates

| Gate | Assessment | Remaining |
|---|---|---|
| PEO-00/01 | Architecture and contracts established | Reconcile the programme and its evidence |
| PEO-02 | Durable sponsorship/deferral implemented | Live approval, handling of expiry, acceptance of restriction release |
| PEO-03 | Scanner, custody and admission machinery substantially implemented | Independently certified external sources, scanner/KMS deployed, proof of source trust |
| PEO-04 | Controlled founding-group machinery exists | Four authentic, accepted business records |
| PEO-05 | Qualification orchestration and staging runbooks exist | Protected acceptance of IAM, subscription, provider and tenant |
| PEO-06 | Applicant, reviewer and Console functionally implemented | Guided evidence UX, live tests of browser security and accessibility |
| PEO-07 | Criteria defined | Signed production-readiness decisions |

**P0-02C closes a significant gap at the code level.** It covers durable custody intents, encrypted object storage, version-specific reads, retention, holds, key rotation and orphan reconciliation. It does **not** prove that approved AWS KMS/S3 resources, malware-scanner signers or independently trusted verification sources are operating. The CP P0-02C runbook keeps those restrictions in place.

## 5. ADR-BCP-027 gates

| Gate | Assessment | Remaining |
|---|---|---|
| LA-00/01 | Canonical model and contracts substantially converged | Final consumer inventory, compatibility sign-off |
| LA-02 | Nullable legal-entity and PRIMARY mapping foundations | Migration of real data, proof for legacy consumers, rollback |
| LA-03 | Governed Organisation-first registration implemented | Execution accepted for the four founding businesses |
| LA-04 | Mandates, independent decisions, lifecycle and Console readback implemented | Authentic mandates, human authority decisions |
| LA-05 | Policy and contract guards implemented in several engines | Native execution certified, issuer/PSP identity, bypasses closed |
| LA-06 | Synthetic founding-business qualification implemented | Real business/tenant records, evidence, independent approval |
| LA-07 | Cutover/test infrastructure and Console increments | Full operational cutover, historical financial attribution, recovery |

### Founding-group truth table

| Business | Canonical operating treatment | Legal/evidence acceptance still required |
|---|---|---|
| Nabhold Group Africa | Its own Organisation and Tenant; a potential scoped legal actor | Independently accepted registration, and any authority to act for another business |
| Thamani Global | An independent incorporated business and Tenant | Its own official registration, and separate proof of group control |
| ZuriBeans | An independent operating Organisation and Tenant, with no fictional incorporation | A scope-specific authorised legal actor for activities that need one |
| Equator & Estate Co. | An independent operating Organisation and Tenant, with no fictional incorporation | Appropriate real legal responsibility for property, construction and other relevant activities |

The Nabhold and Thamani CIPC records ([#252](https://github.com/baobab-platform/shared/pull/252), [#266](https://github.com/baobab-platform/shared/pull/266)) are documentary references. They are **not** independently accepted verification cases in CP.

The ownership structure alone does not let Nabhold act as issuer, seller, importer or contracting actor for ZuriBeans or Equator. Each role needs a separately accepted mandate.

## 6. Landing page and Console

| Area | Status |
|---|---|
| Public navigation and CTAs | Implemented in code |
| OIDC/BFF (server sessions, Redis, PKCE, introspection, CSRF, server-only CP calls) | Implemented in code |
| Real production login | Blocked by design: `readAuthSettings()` rejects production |
| Public registration | Guidance only: `/signup` creates no IAM identity |
| Cross-browser E2E | Not demonstrated |

### Frontend gaps (baobab-cp)

| ID | Gap |
|---|---|
| F-01 | **Deep-link return.** After sign-in the OIDC callback always redirects to `/workspace`. A user who starts at `/signup` and chooses the protected application cannot return to `/workspace/apply`. This is an integration gap, not an authorisation bypass. |
| F-02 | **New-user entry.** There is no approved IAM-owned enrolment or invitation that leads a new applicant into the governed application. |
| F-03 | **Role-aware navigation.** The reviewer workspace link is gated only on `application.review`/`application.decide`. It is not gated for the independently authorised requester and authoriser personas at every stage. |
| F-04 | **Guided transitions.** The independent review screen asks for application, review, organisation and policy/evidence identifiers to be typed in by hand. That falls short of the business-language-first experience PEO-06 and CX-07 require. |
| F-05 | **Real frontend acceptance.** No evidence yet for: provider login, callbacks, multi-replica sessions, token revocation, sign-out, accessibility, small screens, CSRF, cross-tenant access, or real application-to-provisioning transitions. |
| F-06 | **Public website publication.** The website is transitional and co-located. Legal notices are placeholders, indexing is disabled, and ownership, domain, deployment and launch approvals have not been given. |
| F-07 | **Stale documentation.** `docs/frontend/cx05e-governed-datasets.md` still describes export/bulk as ports that cannot be deployed. The README's 12 October snapshot needs rebaselining. |

## 7. Cross-engine and Digital Estate observations

| Component | Conclusion |
|---|---|
| IAM | Provider-neutral federation and workload architecture implemented. Defining a scope does not create an ACTIVE client or an issued credential |
| Trade | Native Medusa checks and exact-contract validation improved. Real checkout and legal/merchant acceptance still gated |
| ERP | Native iDempiere financial safeguards and generated contract validation exist. Live issuer/finance policy and proof of the JVM runtime are outstanding |
| Payments | Durable reservations, signed webhooks, PSP transport and authority checks exist as guarded components. No unrestricted real-money permission |
| Subscriptions | Stronger handling of current-INTERNAL and protected commands. Live invoicing and commercial provider integration unproven |
| Trade Docs | Reference logic for issuer assessment exists. No deployable native issuance/signature/outbox runtime |
| Regulations | Requirements/policy implementation progressing. Promotion of official sources and protected applicability are separate steps |
| Infrastructure | Protected staging workflows and deployment definitions exist. Authentic account/role configuration and cross-engine proof required |
| ZuriBeans | B2B digital-estate foundation exists. Readiness per capability unproven |
| Thamani | **EA-12 drift.** The accepted B2B integrated-logistics model replaced the legacy storefront, but shop, product, cart and checkout routes remain |
| Nabhold | Corporate website foundation exists. Real onboarding and publication acceptance are separate steps |
| Equator & Estate | An early independent estate foundation |

## 8. Drift and gap register

| ID | Finding | Severity | Required correction |
|---|---|---|---|
| D-01 | EA v2.1 still proposed; dashboard still on v2.0 | P0 Governance | Decide acceptance; publish an evidence-backed v2.1 register |
| D-02 | Genuine founding-company and group-control evidence not accepted | P0 Authority | Independent verification and maker/checker acceptance |
| D-03 | P0-04B native bypass closure incomplete | P0 Financial/legal | Real PEP testing in Trade, ERP, Payments, Subscriptions and Trade Docs |
| D-04 | Console production authentication deliberately disabled | P0 Go-live | Security-approved deployment design and protected acceptance |
| D-05 | No certification of scanner/custody as deployed | P0 Evidence | Certified workloads, S3/KMS/retention, acceptance of official sources |
| D-06 | Public registration and login deep-link journey incomplete | P1 UX | IAM enrolment/invitation, safe post-login destination |
| D-07 | Independent Console workbenches incomplete | P1 Workflow | CX-06–10, authority checks per persona |
| D-08 | No acceptance for protected browser, dataset lifecycle or performance | P1 Assurance | Real authenticated browser and dataset maker/checker tests |
| D-09 | EA-12 estates uneven; Thamani has a legacy experience | P1 Product | Align estate routes and journeys to the accepted ADRs |
| D-10 | Public website publication and documentation governance incomplete | P1 Publication | Ownership, domain, legal content, indexing, CI, release evidence |

These are separate items. Fixing D-01 does not fix runtime shortcomings. Passing more code-level CI does not close D-02, D-04 or D-05.

## 9. Recommended order

1. **EA-R01: Reconcile architecture and governance.** Approve the v2.1 decisions, replace the v2.0 dashboard, and record each gate's status per evidence level.
2. **EA-R02: Lay the founding legal/evidence foundation.** Onboard Nabhold and Thamani from real sources, take separate control decisions, run mandate approval workflows, and integrate scanner and custody with approved infrastructure.
3. **EA-R03: Complete P0-04A and P0-04B.** Converge Trade Docs, then deny execution live, revoke, and attribute the correct legal party in Trade, ERP, Payments and Subscriptions.
4. **EA-R04: Close frontend and Console integration.** Covers F-01 to F-04, CX-06 to CX-10, and source-backed eligibility explanations.
5. **EA-R05: Run protected staging and E2E acceptance.** Take four businesses through the lifecycle with positive and negative cases, real browsers, revocation, search at volume, rollback and restoration.
6. **EA-R06: Publish and certify operations.** Correct the documentation, align the founding estates, approve the public site, certify providers, and sign off PEO-07, LA-07 and EA-09B.

Code increments can proceed in parallel. Production activation stays gated on its dependencies.

## 10. Minimum end-to-end acceptance matrix

| Test | Expected evidence |
|---|---|
| Public entry | CTAs resolve to real destinations; no 404 or dead end |
| Sign-up/identity | An approved applicant can get an IAM identity or invitation |
| Login/deep-link | A valid login returns the user to the authorised Console task they intended |
| Applicant | Unincorporated and incorporated claims stay distinct; drafts survive edits |
| Admission | Reviewer and decider are different people; all current evidence and scope checks enforced |
| Organisation-first registration | Correct PRIMARY Organisation, an optional DEFAULT legal entity, a separate Tenant |
| Mandate | Exact actor, role, activity, market and effective interval; revoked or expired mandates fail closed |
| Subscriptions/provider | Only explicit current entitlements and certified bindings permit operations |
| Native Trade/ERP/Payments | The correct legal actor is enforced at irreversible execution |
| Console readiness | Planned, observed, permitted, blocked, stale and active states told apart |
| Security | CSRF, revocation, replay, sibling access and unauthorised approval all denied |
| Operations | Traceable events, recovery, key rotation, backup/restore, signed acceptance |

A positive test must show a legitimate operation actually happening, not just successful validation. A negative test must confirm that the intended business action did not happen.

## 11. Final judgement

| Dimension | Readiness |
|---|---|
| EA architecture | Established. Plan approval was pending at audit time; **Accepted 2026-10-13** |
| Backend development | Substantial |
| Public–Console code integration | Implemented |
| Protected live E2E | Not demonstrated |
| Founding-group operational acceptance | Outstanding |
| Production activation | **Not authorised** |
