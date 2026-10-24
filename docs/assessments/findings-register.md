# Audit assessments — Findings and improvement register

**Status:** Advisory tracking index, not an Accepted ADR, capability source, runtime evidence registry or production release authority.  
**Initial snapshot:** [BA-AUD-2026-10-24-EADEV-01](architecture/2026-10-24-ea-v2.3-ea-dev-strategic-technical-assessment.md), observed 24 October 2026.  
**Current implementation/evidence authority:** [EA-DEV register](../architecture/ea-dev-implementation-register.md), [canonical L4 matrix](../architecture/ea-v2.2-integration-acceptance-matrix.md), owning source/CI receipts and protected release records.

## How the register works

Audit findings use stable **BA-AUD-NNN** identifiers across re-audits. A row records observation and recommendation; **it does not grant permission to modify canonical contracts**. A suggested owner is accountable for triage, not assigned personnel or independently appointed approval. Do not mark RESOLVED because a PR opens, CI is green or a proposed ADR exists. Verify the precise closure criteria and preserve the link to the successful owning repository change, real receipt where required and reviewed decision. Proposed options must be reconciled through accepted EA/ADR/domain owners before becoming obligatory.

Allowed statuses: **OPEN** (observed with source evidence), **TRIAGE** (inference or improvement hypothesis pending validation), **ACCEPTED_FOR_WORK** (owning programme accepted a remedy), **IN_PROGRESS**, **VERIFIED_RESOLVED**, **REJECTED_WITH_REASON** and **SUPERSEDED_WITH_LINK**. An outdated evidence observation is **REVALIDATION_REQUIRED**, not automatically a failure or success. For each updated row, annotate date and immutable source, preserve previous history in a linked review or issue.

| ID | Priority | Character | Status at 2026-10-24 | Recommended owner | Problem / strategic opportunity | Proposed resolution and closure test |
| --- | --- | --- | --- | --- | --- | --- |
| **BA-AUD-001** | P0 | Observed CI blocker | OPEN | Infrastructure + IAM/CP | Infrastructure [#54](https://github.com/baobab-platform/infrastructure/pull/54) INT-02 [run](https://github.com/baobab-platform/infrastructure/actions/runs/40058049607) failed in human IAM login proof, status 500 | Identify root cause without masking the test; final-head mandatory CI passes and DEV-02 scoped fixture receipts/teardown are inspected |
| **BA-AUD-002** | P0 | Observed qualification gap | IN_PROGRESS | IAM + CP + Infrastructure | DEV-03 and all seven DEV-04 INT-03C cases lack fresh qualifying current-profile evidence in inspected Shared register | Current actual IAM-issued token/Principal/grant and all original cases observed, with explicit denials and cleanup |
| **BA-AUD-003** | P0 | Observed qualification gap | OPEN | Nabhold + CMS + IAM/CP/Infra | DEV-05 fourteen NAB-03 cases and DEV-06 external zero-estate journey not qualified in inspected register | Actual case-by-case positive/negative receipts per owning programme, not lifecycle substitutions |
| **BA-AUD-004** | P1 | Architecture risk | TRIAGE | Shared EA-REL + Infrastructure | DEV-13 dependencies DEV-04..12 may be interpreted as a global production release prerequisite despite progressive EA-REL | Approve and test scope-specific release dependency projection while retaining all applicable protected approvals |
| **BA-AUD-005** | P1 | Verified tool limitation / compatibility risk | TRIAGE | Shared Foundation + engine owners | Valid but older Shared consumer pins prove neither failure nor semantic compatibility | Produce per-contract changed-consumer impact report with actual selected compatibility tests and explicit permitted lag |
| **BA-AUD-006** | P1 | Observed documentation freshness | VERIFIED_RESOLVED | Shared EA-DEV register owner | CP [#434](https://github.com/baobab-platform/baobab-cp/pull/434) merged while latest Shared DEV-02 row had not yet adopted it | Reconcile exact CP and Infrastructure verified outputs; optional source-change flag does not self-accept evidence |
| **BA-AUD-007** | P2 | Manifest completeness question | TRIAGE | Shared contract catalogue | New Trade v2 schema files not enumerated in root contracts.lock.yaml; manifest exhaustiveness not established | Document manifest semantics; if intended exhaustive, generate/validate all published schemas and consumers |
| **BA-AUD-008** | P1 | Availability/revocation design opportunity | TRIAGE | CP/IAM + owner-native PEPs | Bounded authorisation attestations and CP outage consistency need explicit measured operational treatment | Owner-authorised policies and transaction-time expiry/replay/revocation/outage negative tests |
| **BA-AUD-009** | P1 | Cross-engine evidence opportunity | TRIAGE | Shared / Infrastructure / Observability owners | Receipt/trace information remains distributed across multiple owning registers and engines | Cross-link existing evidence by source/decision/environment/correlation without inventing a second authority |
| **BA-AUD-010** | P1 | Product/release measurement opportunity | TRIAGE | Platform Product / EA-ENG / Dev tooling | Architecture progress is easier to enumerate than qualified user and developer outcomes | Adopt measured integration, journey, recovery, cost and capability-specific readiness criteria |
| **BA-AUD-011** | P2 | Verified documentation mismatch | OPEN | Shared maintainers | README said repository Private; GitHub repository metadata says Public | Correct metadata wording; separately review public artifact redaction and sensitive content rules |
| **BA-AUD-012** | P3 | Verified hygiene | OPEN | Shared maintainers | Tracked Python .pyc files / missing cache exclusions | Narrow cleanup PR with ignores; confirm no tracked bytecode remains |
| **BA-AUD-013** | P1 | Developer-experience opportunity | TRIAGE | baobab-dev / Shared Foundation | Root Shared pnpm is 11.24.0 while an upstream major release exists; effects on consumers unknown | Controlled compatibility/registry/Codespaces test matrix, rollback and explicit upgrade/defer decision |
| **BA-AUD-014** | P1 | Engine onboarding opportunity | TRIAGE | Shared / Infrastructure / engine-template / Pulse / Payments | DEV-14/15 are accepted work requirements without a demonstrated reusable headless provider journey in audit evidence | Actual real IAM/CP plus Pulse and Payments sandbox test receipts, correct native vetoes and per-case limitations |

## IAM ADR-to-capability audit — 24 October 2026

**Origin:** [24 October 2026 IAM ADR-to-capability assessment](iam/2026-10-24-iam-adr-capabilities-implementation-assessment.md), **BA-AUD-2026-10-24-IAM-01**. All rows below are **advisory**: the owning authority has not necessarily accepted their proposed remedies. Owner names identify responsible functions, not appointed reviewers. Statuses are anchored to IAM main [`0ad10360`](https://github.com/baobab-platform/baobab-iam/commit/0ad103606b9705fcb33c468ea01b54d8ce76f9ae) and the named external run/PR heads.

**No duplicate finding IDs:** IAM-specific details are related to existing BA-AUD-001 (Infrastructure #54 INT-02), BA-AUD-002 (real IAM↔CP DEV-03/04), BA-AUD-003 (NAB-03/DEV-05), BA-AUD-008 (CP revocation/outage) and BA-AUD-009 (linked evidence). Those baseline items remain independently tracked. Closing an IAM-specific row does not automatically close its related programme finding.

| ID | Priority | Character | Status at 2026-10-24 | Recommended owner | Problem / strategic opportunity | Proposed resolution and closure test |
| --- | --- | --- | --- | --- | --- | --- |
| **BA-AUD-015** | P0 | Observed canonical support gap | OPEN | IAM + Shared catalogue + CP | IAM [provider declaration](https://github.com/baobab-platform/baobab-iam/blob/0ad103606b9705fcb33c468ea01b54d8ce76f9ae/.baobab/capability-provider.yaml) declares **PARTIAL** for all three providers; no IMPLEMENTED support published/registered | Complete exact canonical conformance, positive and negative live registered consumption and CP owner-governed registration, then review support change; do not promote by a passing unit test |
| **BA-AUD-016** | P0 | Observed end-to-end qualification gap | OPEN | IAM / CP / Infrastructure | IAM [C4-03B–E](https://github.com/baobab-platform/baobab-iam/blob/0ad103606b9705fcb33c468ea01b54d8ce76f9ae/docs/operations/c4-03-live-qualification.md) and C4-04B/C real consumer/canonical readiness are not accepted | Current IAM source/provider/CP head, actual issuer/subject/audience/grant + protected resource, unexpired revocation, cross-tenant denials, private closed-schema receipts and teardown; cross-link BA-AUD-002 |
| **BA-AUD-017** | P0 | Observed native journey gap | OPEN | IAM native / CP / estate BFF owners | Kratos session, Hydra login/consent and assurance have source/fixture tests, but no accepted registered BFF/CP native complete login and step-up path | Real canonical human session, exact PKCE/state/nonce, current Principal/assurance, deny-on-revoke and estate BFF session acceptance per ADR-IAM-0023/24 |
| **BA-AUD-018** | P0 | Observed workload admission gap | OPEN | IAM Hydra / CP / first protected consumer | Hydra issued/workload mechanics exist, but current registered resource/audience/withdrawal acceptance is outstanding (MP6/C4) | Approved workload registry/client and current CP profile, signed actual token, exact one-resource audience/scope, protected consumption, expired and **unexpired-revoked** denial |
| **BA-AUD-019** | P0 | Observed enterprise-estate adoption gap | OPEN | IAM / Nabhold / ZuriBeans / Thamani / CMS/Trade | MP17 has no final multi-provider estate acceptance; designs/partial client flows do not prove all three customer journeys | Scope-specific actual Nabhold workforce, ZuriBeans B2B and Thamani current B2B logistics native/federated login/BFF/CP/domain negative and positive tests; cross-link BA-AUD-003 |
| **BA-AUD-020** | P1 | Observed federated UX/composition gap | OPEN | IAM federation / CP / estate BFF owners | MP10 login discovery remains partial and MP8 bounded enterprise OIDC/SAML broker CI is not a complete CP/estate session | Provider-neutral discovery, signed OIDC/SAML assurance provenance, approved trust, exact issuer+subject CP Principal and zero group-to-business-grant shortcuts in real enterprise journey |
| **BA-AUD-021** | P1 | Observed independent decision gap | OPEN | Platform Architecture / IAM lifecycle owner | MP13 SCIM/directory provider intentionally undecided/unactivated under ADR-IAM-0026/33 | Document concrete external provisioning need, select portable SCIM/directory provider under appropriate decision, qualify lifecycle without CP/domain business grants; no speculative activation |
| **BA-AUD-022** | P1 | Observed restore/revocation risk | OPEN | IAM Security / CP / Infrastructure / Operations | [IAM DR runbook](https://github.com/baobab-platform/baobab-iam/blob/0ad103606b9705fcb33c468ea01b54d8ce76f9ae/docs/operations/disaster-recovery-runbook.md) acknowledges no automated post-backup security journal, requiring manual post-restore revoked-state reconciliation | Durable replay-protected recovery journal and non-prod restore drill with revoked identity/session/workload/trust/grant cases remaining denied after recovery |
| **BA-AUD-023** | P1 | Observed protected operational acceptance gap | OPEN | IAM Security / Infra / Operations | MP15/16/19/20 lack qualified deployed key/cert overlap-rotation, HA/DR/residency, incident response and SLO/signed production acceptance | Approved scope-specific RPO/RTO and SLO, executed failover/restore/rotation/containment, measured evidence and protected-authority approval; no inferred GO |
| **BA-AUD-024** | P1 | Observed migration/cutover gap | OPEN | IAM Migration / CP / Operations | MP18 migration ledger exists but per-capability dual-issuer cutover and rollback have not been qualified; Keycloak enterprise federation must remain | Exact provider/binding-scoped migration and reverse drill, issuer/subject continuity, no email linking, credentials/sessions/rights not resurrected and retained Keycloak enterprise SSO |
| **BA-AUD-025** | P2 | Observed documentation/precedence drift | OPEN | IAM Docs / EA Architecture | ADR-0001–0018 still self-label Proposed, legacy [consolidated Keycloak spec](https://github.com/baobab-platform/baobab-iam/blob/0ad103606b9705fcb33c468ea01b54d8ce76f9ae/docs/adr/Consolidated-Technical-Specification.md) and Thamani B2C language conflict with newer provider/business direction; MP-status baseline says 5 Oct | Reviewed non-destructive supersession/precedence index and current source/evidence summary; **no** automatic ADR status upgrade, historical erasure or fiction of qualified Thamani B2B |
| **BA-AUD-026** | P1 | Observed inactive workload safeguard | OPEN | IAM / Shared scopes / CP / Trade | [Proposed ADR-IAM-0034](https://github.com/baobab-platform/baobab-iam/blob/0ad103606b9705fcb33c468ea01b54d8ce76f9ae/docs/adr/ADR-IAM-0034%20%E2%80%94%20Native%20Commitment%20Server%20Workload%20Identity.md) has a tested narrow server-workload rule, but explicitly **no allocated client or CP assignment** | Only after Shared workload-registry allocation, real IAM client, CP assignment and native Trade commitment provenance/negative proof; no automatic Trade activation |
| **BA-AUD-027** | P1 | Broader assurance gap requiring scoping | TRIAGE | IAM Security / Privacy / Admin / estate owners | Full high-risk recovery/proofing, delegated administration, A4 privileged sessions, privacy retention/erasure and incident containment not comprehensively demonstrated in inspected evidence | Per-domain evidence census against Accepted ADR-IAM-0024/25/29/30/31; convert verified deficits to bounded work, prove real high-risk cases and avoid unsupported absence claims |
| **BA-AUD-028** | P1 | Evidence discoverability opportunity | TRIAGE | Shared EA-DEV / IAM / CP / Infrastructure | Per-capability proof scattered across ADRs, CI, runtime support, CP, estates and ops | Build read-only joined scoreboard with current SHA, identity provider, catalogue key, registration/activation, real case outcome/expiry, scoped estate and protected readiness; no second authority or auto-promotion |

## Control Plane ADR-to-capability audit — 24 October 2026

**Origin:** [BA-AUD-2026-10-24-CP-01](cp/2026-10-24-cp-adr-capabilities-implementation-assessment.md), observed at CP main [`a21f48a8`](https://github.com/baobab-platform/baobab-cp/commit/a21f48a80cd5b2387c85aea7f6d97ff3811f2dbb). These are **diagnostic findings within Accepted EA-DEV**, **not** a new CP–IAM roadmap, new acceptance hierarchy or mandatory package ordering. Their proposed remedies require the owning programme's normal review; evidence classes and original baseline statuses remain distinct.

To prevent duplicate reporting: BA-AUD-001 already tracks Infrastructure INT-02; BA-AUD-002 tracks the current IAM/CP issuer and seven DEV-04 cases; BA-AUD-003 tracks Nabhold/external integration; BA-AUD-006 tracks DEV-02 register freshness; BA-AUD-008/009 track general authority/evidence risk; IAM BA-AUD-015–020 track provider and estate-specific details. Closing this CP-specific finding does **not** automatically close a cross-platform or IAM finding.

| ID | Priority | Character | Status at 2026-10-24 | Recommended owner | Problem / opportunity | Proposed remedy and **closure test** under existing EA-DEV |
| --- | --- | --- | --- | --- | --- | --- |
| **BA-AUD-029** | P0 | Observed report/source discrepancy | VERIFIED_RESOLVED | CP / Shared DEV-02 register owner | CP [#434](https://github.com/baobab-platform/baobab-cp/pull/434) merged five-profile Organisation/Tenant/mandate fixture code, current main Go CI green, but [official DEV-02 row](../architecture/ea-dev-implementation-register.md) remains NOT_ASSESSED / PARTIAL_SOURCE_RUNTIME_UNPROVEN | Reconcile actual independently reviewable Postgres/API fixture receipts, source/test/provenance and exact positive/negative cases in official EA-DEV JSON and generated view; don't infer runtime PASS solely from source |
| **BA-AUD-030** | P0 | Observed real integration gap | IN_PROGRESS | CP / IAM / Infrastructure | CP identity, federation, current runtime authority and INT-03C Principal disable source exist, but inspected DEV-03/04 lacks current signed issuer→CP protected-consumer seven-case evidence; Infrastructure [INT-02](https://github.com/baobab-platform/infrastructure/actions/runs/40058049607) failed | Qualify DEV-03 actual signed provider, CP canonical Principal/context/grant, revocation before expiry, wrong audience/tenant, separate Principals, then the **original** seven DEV-04 cases with private exact receipts/teardown; cross-link BA-AUD-001/002 |
| **BA-AUD-031** | P0 | Observed estate native-consumer gap | OPEN | CP / IAM / Trade / estate owners | CP #424/426/430/432 introduce source Principal, BFF binding, commerce profile and resource assignment; complete registered Trade estate/native commitment acceptance unproved | Under applicable DEV-05/07/08, prove current IAM workload/CP estate attestation, buyer/seller native operation and cross-tenant/wrong estate negatives, with domain veto intact; no Proposal-to-Accepted status assumption |
| **BA-AUD-032** | P1 | Current provider-support qualification gap | OPEN | CP provider/Shared/IAM/engine owner | CP support certification, runtime profile and observation handlers present; no checked evidence that all concerned providers are currently REGISTERED, ACTIVE, eligible and correctly consumed | Under DEV-03/14/15, verify actual owner provider-support declaration, current instance/artifact/health, exact capability binding, expiry/grant and real consumer receipts; never invent CP provider declaration or promote PARTIAL |
| **BA-AUD-033** | P1 | Observed legal-verification acceptance gap | OPEN | CP / legal/source / onboarding domain | Organisation admission, legal actor mandates, official-source capture and documentary controls substantially coded; synthetic/development cases do not provide real verified legal/market approval | Under applicable DEV-02/05/06/09, prove owner-authorised real legal-source provenance and specific permitted legal responsibility/mandate; retain nonproduction synthetic as synthetic and production approval separate |
| **BA-AUD-034** | P1 | Engine-native enforcement qualification gap | OPEN | Trade / ERP / Payments with CP / Shared | CP contains Trade order, ERP posting and Payments movement per-operation legal authority handlers; these are not native database/accounting/financial commit vetoes | Under DEV-07/09/15, demonstrate exact current CP attestation and engine's own actual permitted/denied execution; include unsupported/expired/wrong-actor/duplicate cases; don't call CP reply money/GL settlement approval |
| **BA-AUD-035** | P1 | User experience / runtime gap | OPEN | CP Console / IAM / Infrastructure | Organisation 360, searchable directory and guarded datasets have API/Next code and CI; nonproduction dataset mutations disabled by default; protected user journey and high-volume evidence not established | Under DEV-05/11, qualify actual authenticated BFF→CP, permission-filtered read/change, user-role denial, observable 401/403/outage states, accessibility and independently measured search/export/bulk performance |
| **BA-AUD-036** | P1 | Operational resilience qualification gap | OPEN | CP / Infrastructure / Security / Operations | Deployment health/reconcile/events, current issuer context and authority-read source exists; protected recovery of revoked state, HA/DR/SLO/rotation not proven by a source-green commit | Under DEV-11/12 and protected DEV-13 when appropriate, execute scope-specific fail-closed outage, withdrawal, restore, observed issuer changes, protected custody/rotation and documented RPO/RTO; no dev-wide approval hold |
| **BA-AUD-037** | P2 | ADR/document freshness discrepancy | OPEN | CP ADR owner / Shared DEV-00 report owner | [CP index](https://github.com/baobab-platform/baobab-cp/blob/a21f48a80cd5b2387c85aea7f6d97ff3811f2dbb/docs/adr/index.md) labels Accepted BCP-026/027 implementation pending despite subsequent source; BCP-028–031 Proposed with source; README dated 12 Oct | Annotate scope-specific source status, accepted/proposed precedence and actual receipts; do not amend or backdate ADR statuses without normal decision |
| **BA-AUD-038** | P1 | Authority taxonomy risk | TRIAGE | Shared capability catalogue / CP Architecture | CP has 25 sampled operation families but is itself canonical authority, not an engine whose admin APIs automatically become catalogued provider capabilities | Under DEV-00/03/14 document distinction between CP-owned commands/read models and Shared provider keys; validate consumer use without creating new canonical keys or alternative CP authority |
| **BA-AUD-039** | P1 | External tenancy acceptance gap | OPEN | Infrastructure / CP / IAM / selected domain provider | CP has Organisation-first, Tenant and estate-less source semantics but unrelated external API-only client acceptance not demonstrated in DEV-06 | Execute the accepted DEV-06 current IAM/CP → eligible engine positive/negative cases for unrelated client with **zero** DigitalEstate; deny sibling/cross-tenant access |
| **BA-AUD-040** | P1 | Reporting/readiness improvement opportunity | TRIAGE | Shared EA-DEV / CP / Infrastructure | Capability/identity/estate evidence scattered; a broad API handler inventory can be mistaken for runtime acceptance | Under DEV-00/11/14 implement optional **read-only** source-joined evidence view showing provider/contract/current binding, exact case receipt, freshness and protected status; no second register, auto-PASS or new gate |
| **BA-AUD-041** | P1 | Historical-regression verification risk | TRIAGE | CP test / Shared consumer / DB owners | Historical [Shared-CP reconciliation](https://github.com/baobab-platform/baobab-cp/blob/a21f48a80cd5b2387c85aea7f6d97ff3811f2dbb/docs/reconciliation/shared-control-plane-audit.md) includes old issues, repairs and untested assumptions; not safe to copy historic defects as current bugs | Under DEV-00/10/12 rerun current pinned contract/migrations with actual PostgreSQL and current route/negative tests, preserving prior snapshots and documenting any new verified defect |

## Improvement log

An accepted and closed improvement should append a dated entry below; retain the original problem statement above. Example format (illustration only, **not a completed action**):

| Date | Finding | Change / decision | Evidence and exact qualification | Verified by | State transition |
| --- | --- | --- | --- | --- | --- |
| YYYY-MM-DD | BA-AUD-NNN | Link to accepted ADR/PR/issue | Exact reviewed merge SHA, mandatory CI run, runtime receipt or independent approval as applicable | Named owning authority | OPEN -> VERIFIED_RESOLVED |

_No improvement entries have been verified for this register at initial creation; recommendations remain unadopted until owner triage. The README metadata correction proposed in this same documentation PR is a candidate only until merged._

## Improvement reviews

At the next assessment, compare:
- count of OPEN/TRIAGE/VERIFIED_RESOLVED and genuinely newly observed findings; do not equate fewer rows with better reliability;
- time to reproduce a real IAM/CP/engine profile and perform verified teardown;
- changed Shared contracts and consumers with actual compatibility proofs;
- applicable mandatory L4/INT/NAB real-component PASS/BLOCKED/FAIL with freshness;
- production release claims strictly limited to independently approved scopes;
- developer setup and engine onboarding time, browser completion, recovery evidence and cost per qualified capability.

[Assessment index](README.md) explains status semantics, templates and retention.

## DEV-02 adoption observation — 24 October 2026

BA-AUD-006/029 closure is scoped to fixture evidence and official reporting.
CP #434 merged at `a21f48a80cd5b2387c85aea7f6d97ff3811f2dbb`; Infrastructure #54
merged at `631e59dc0787f81bec0fed3516a97572e825d949`, after final-head review and
all applicable mandatory CI passed. Actual 24-case fixture receipts, verified
teardown and PostgreSQL/API observations are retained in the
[DEV-02 evidence record](../architecture/evidence/dev02-2026-10-24/README.md).
[Shared #382](https://github.com/baobab-platform/shared/pull/382) adopts those
observations into the official JSON/generated view; this closure takes effect
when that reviewed adoption merges, rather than merely when its PR opens.

| Date | Finding | Change / decision | Evidence and exact qualification | Verified by | State transition |
| --- | --- | --- | --- | --- | --- |
| 2026-10-24 | BA-AUD-006, BA-AUD-029 | CP #434 + Infrastructure #54; Shared #382 adoption | Exact merges above; 24 non-authorising fixture cases and native PG/API checks with complete teardown; hash-verified original receipts | CP/Infrastructure owner CI; Shared EA-DEV adoption review | OPEN -> IN_PROGRESS -> VERIFIED_RESOLVED upon adoption merge |

BA-AUD-001 remains OPEN: the original MFA failure and successful targeted rerun
are both retained. Its root cause is unestablished; a retry is not a repair.
BA-AUD-002/030 and BA-AUD-033 remain open for real authority-chain and legal-source
qualification beyond these synthetic fixtures. Historical assessment snapshots
are preserved unchanged. No provider, canonical scenario or protected acceptance
is inferred from this scoped closure.

## DEV-03 engineering observation — 24 October 2026

The IAM and CP assessments were consulted for the next Accepted gate. CP #435
adds current issuer status after local JWT validation and is merged at
`718caedca3b9203931b399464e21b0f64ffbe879` with final-head CI/review. Infrastructure
#55 composes actual native Hydra/Kratos and CP APIs, with explicit non-authorising
fixture metadata and closed case receipts. The final native run observed all sixteen cases and verified cleanup; original
receipts and archive hashes are retained in the
[DEV-03 evidence record](../architecture/evidence/dev03-2026-10-24/README.md).
Infrastructure mandatory CI/merge and final adoption remain pending.

BA-AUD-002/030 are IN_PROGRESS, not closed: they include the original DEV-04
seven-case obligations as well as this authority chain. IAM provider, C4,
estate-native, legal-source and protected findings retain their prior status.
Keycloak's federation allocation and the dated assessment snapshots are preserved.
