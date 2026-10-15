# Baobab Platform Enterprise Architecture Implementation Plan v2.2
## Accepted cross-repository integration, tenant-neutral consumption and production-readiness reconciliation

**Status:** ACCEPTED — Normative EA Programme Implementation Plan  
**Approval:** Platform owner's explicit implementation direction, 15 October 2026  
**Date:** 15 October 2026  
**Document owner:** Baobab Platform Architecture; implementation acceptance remains with the authority owning each component  
**Governing architecture:** [ADR-SHARED-036](../adr/ADR-SHARED-036%20%E2%80%94%20Cross-Repository%20Integration%20Testing%2C%20Tenant-Neutral%20Consumption%20and%20Production%20Deployment.md), ACCEPTED 15 October 2026, Shared PR #310, merge 68d841e9cc8e96b3efb9b071a9c72da87fcee194  
**Retained architecture:** ADR-BCP-026/027 (accepted), CP 002/007/009/018/025, IAM-0033, Infrastructure 0002/0006/0015/0021 and all other applicable accepted Shared/owner ADRs  
**Replaces for active programme sequencing:** [EA Implementation Plan v2.1](EA-implementation-plan-v2.1-ADR-BCP-026-027-reconciliation.md), Accepted 13 October 2026; v2.1 remains a dated, authoritative historical decision record for its approved substantive controls. No rollback of its decisions.  
**Retains:** [EA v2.0 baseline](../adr/Baobab%20Platform%20Enterprise%20Architecture%20Implementation%20Plan%20%E2%80%94%20Revised%202026-09-30.md) for unchanged workstream scope, as amended by later accepted architecture; v2.0's sequence and dashboard are historical.  
**Living state:** [EA v2.2 dashboard](ea-dashboard.md). **Audit snapshot:** [15 October 2026 evidence audit](ea-v2.2-evidence-audit-2026-10-15.md). **Test matrix:** [L4 integration and acceptance matrix](ea-v2.2-integration-acceptance-matrix.md).  
**Relevant application programme:** Nabhold Go-Live Master Plan v2.0; this EA plan extends platform-wide testing without superseding Nabhold's internal gates.  
**Scope:** Shared, Infrastructure, CP, IAM, Nabhold, Thamani, ZuriBeans, Equator & Estate Co., all participating headless engines and subsequent external platform customers.

> ARCHITECTURE APPROVED is not CODE MERGED; CODE MERGED is not INTEGRATION PROVEN; INTEGRATION PROVEN is not STAGING ACCEPTED; STAGING ACCEPTED is not LEGALLY/PROVIDER CERTIFIED; and none independently authorises PRODUCTION. Implement this plan, preserving the individual gate authorities. No implied approved identities, legal registration verification, PSP access, cloud secrets or live tenants.

---

## 1. Executive decision and why v2.2 is required

EA v2.1 accepted Organisation-first identity and operating LegalActor mandates, progressive/conditional onboarding and separate legal, IAM, subscription, service readiness and production decisions. All remain binding.

Accepted ADR-SHARED-036 added a material system requirement that the prior sequence did not operationalise: **one shared version-pinned, real-component, cross-repository integration harness** must produce reproducible security, context, capability, domain, recovery and isolation evidence in local development, GitHub Codespaces and GitHub Actions. Protected staging continues as a separate higher assurance gate.

It also clarified the **tenant-neutral production SaaS consumption architecture**: the Control Plane plus IAM and independently deployed headless engines are shared by default, provisioned/dedicated by isolation requirement, while an independently admitted customer may supply its own frontend/backend or consume API-only without a Baobab-built DigitalEstate.

Therefore EA v2.2 SHALL:
1. Create explicit Infrastructure-owned **EA-INT, INT-01–INT-08**, and embed its verifiable exit criteria into EA-09A and Gate D.
2. Preserve every v2.1 Gate A–E, PEO-00–07, LA-00–07, separate four-readiness decisions, founding-grace constraints, legal/money movement vetoes and EA workstreams.
3. Start INT-01 and INT-02 **in parallel** with source, IAM, PEP, legal-evidence and digital-estate engineering, instead of waiting for EA-R05 to begin integration testing.
4. Use **Nabhold** as L4 test pioneer (IAM → CP → Nabhold confidential BFF → CMS). Thamani, ZuriBeans, later Equator & Estate Co. and external API-only enterprises inherit generic identity/context/isolation scenarios, not Nabhold-specific entitlement or tenancy.
5. Require at least one **external synthetic customer with zero DigitalEstate records** in the platform integration matrix. A Digital Estate is a presentation option, NOT a prerequisite for independent Tenant or Subscription.
6. Restate the accepted production model and release responsibilities, without inventing deployed AWS infrastructure or changing Fargate/region policies.
7. Keep proposed/open branch work out of implementation-complete status. Assess actual main, PR head, workflow, contract pins and protected runtime separately.

### 1.1 Status and precedence

This plan is **Accepted and binding for active execution** on the platform owner's instruction. ADR-SHARED-036, CP/engine owner accepted ADRs and canonical contracts retain authority over domain/protocol/legality. An EA schedule neither activates a provider nor grants new identity. A contradictory previous plan sentence SHALL be amended or read as historical; a contradiction in a canonical runtime contract requires the owning authority's actual contract change. Unmerged source cannot supersede accepted decisions.

Proposed INT names are **work items**, not capabilities, HTTP routes, IAM scopes, provider lifecycle values or new legal gates. A new Shared schema is created ONLY where cross-repository consumers require and validate it.

## 2. Unchanged substantive controls inherited from v2.1

1. Each operational Tenant has exactly one governed **PRIMARY Organisation**. Organisation identity persists across incorporation, rebranding, sale and group exit.
2. LegalEntity and legal-actor mandate remain distinct, scoped, effective-dated and verified. An unincorporated operating Organisation can exist where lawful, but a consequential transaction must identify an independently authorised actual actor. No invented company registration or cross-border licence.
3. Founding-group grace is ONE 24-calendar-month bounded *platform documentary* deferral only for listed items; no statutory or provider waiver, no automatic extension, no reset on name or re-provisioning.
4. A Nabhold shareholding, sponsorship or PlatformRelationship never confers cross-tenant IAM access, legal authority or payment capability. Autonomy (Option B) remains.
5. CP owns Organisation/Tenant admission, current context, actor/grant/binding and approved desired state. IAM owns identity/federation and token issuance. Subscriptions owns billing/product classification. Domain engines own execution. Infrastructure owns physical provisioning, not legal admission.
6. CP never becomes an unrestricted ESB or domain database. Consumers resolve current capability and invoke approved resource servers, each enforcing its own execution policy.
7. Negative documentary/regulatory checks are vetoes, not grants. Payments money movement requires independent CP legal and Payments financial approval. ERP posting records are NOT money movement authority.
8. Durable outbox, event replay, current provider release/certification, workload audiences, drift detection, recovery and revocation remain non-negotiable.
9. The four independent readiness decisions remain: low-risk Organisation admission; Tenant registration/administration; permission for a specific consequential domain operation; and production go-live.
10. Synthetic/PostgreSQL/Compose/Codespaces CI SHALL never mark legal/provider verification, protected AWS staging or signed go-live as passed.

## 3. Source baseline and evidence classification

The authoritative snapshot for this revision is dated **15 October 2026** in [the evidence audit](ea-v2.2-evidence-audit-2026-10-15.md). It separately records main SHAs, verified PR status, reviewed non-merged branch deltas and test/operational limitations.

| Evidence class | Meaning | Can establish |
|---|---|---|
| ARCHITECTURE | Accepted ADR/EA owner decision | Design authority only |
| CONTRACT | Canonical published validated contract; exact consumer pin | Wire and semantic agreement; not a running service |
| SOURCE | Merged immutable commit and passing applicable tests | Implemented source and claimed local behaviour |
| REAL_COMPONENT_SYNTHETIC_DATA | Actual selected binary/DB/issuer/provider across real calls using synthetic identities | Cross-engine integration at recorded source pins; no authentic organisation |
| PROVIDER_SANDBOX | Named vendor sandbox under approved test contract | Limited vendor test behaviour; not live certification |
| PROTECTED_STAGING | Actually deployed and authenticated services, approved principals and real controlled environment | Operation-specific technical staging evidence, still subject to human review |
| EXTERNAL_CERTIFICATION | Independent law/regulatory/registry/PSP/provider proof | Only the externally certified fact and scope |
| PRODUCTION_ACCEPTANCE | Designated reviewers, deployment observations, tested recovery and signed release | Permission for the scoped real production activation |

Status vocabulary for every gate: **YES / PART / NO / EXT / N/A**, with exact links/receipt hashes. A workflow passing on a PR is not a merged commit; merging source does not imply a deployed EngineInstance or protected integration.

### 3.1 Current material findings, not to be conflated

- **Shared ADR-SHARED-036** is accepted and merged in PR #310; the L4 orchestrator and profile implementations are **not** merged. EA-INT Architecture=YES, Code=NO.
- **Nabhold PR #55** merged on main SHA 09425a818b8a7f032c146088c2f58d64a8e86147, implementing confidential OIDC/CP check source, disabled by default.
- **IAM PR #116** (G04B-04 human CP-audience client) remains **OPEN** at 4ee06ef2a8d9912eca87c3d050a94e26b2f584f8, final-head CI green; it does not create a current real human Principal, activate a client or complete protected admission. It must be reviewed/merged independently.
- **Payments PR #38** merged as 0eb75baa4aeabaa103a527ecaf63200c17324c69. Gate D1 real Payments/CP/PostgreSQL/HyperSwitch deterministic-PSP integration is evidence for native HTTP money-movement enforcement; **D2 protected provider staging is NOT complete**. CP #400 owns independent CP money-movement authority code.
- **ERP** main 67bdcede1e52a31a9dce09276a148f8fff130eea contains approved catalogue Gate D tests for six operations; other vendor-disbursement, purchase-side, bank/cash, inventory and cost adjustment classes need individually governed native coverage; no live posting certification inferred.
- **Trade** main 5e1cc718354e02c92658cf8779fa00068dbe6af1 contains checkout consumption/commit-lease safeguards, but complete business execution/merchant actor proof is not inferred.
- **CMS** main b72ff38dc5aefb2e6b859b06044f592b86c8fd24 includes Organisation-first content/registered scope corrections; live CP-bound Nabhold CMS publication acceptance remains unproven.
- **Infrastructure** main a7e5b842b87060695fa7ac47b0d2106e0a0a2331 hosts L3 Compose/CI and Terraform assets, but not ADR-036 compliant L4. Older ahead/unmerged branches exist, including feat/integrated-testing-strategy, which calls staging L4 and must be reconciled with the now accepted L4 real-component/nonproduction classification.
- 55 organisation-wide open PRs were discovered: 54 dependency/CI/toolchain candidates and IAM #116. Other ahead/unmerged non-PR branches are catalogued separately, not counted as merged.

**Do not assign blanket "provider production-permitted" on the strength of any of the above.** The live dashboard is the controlled status register and shall be updated per accepted evidence.

## 4. EA-INT: mandatory integration verification programme

EA-INT is an **execution workstream** spanning EA-01/02/03/04/05/06/09A/10/11/12/13. It has one orchestration owner and independent provider owners. It adds engineering proofs; it neither invents capabilities nor replaces EA-R02 legal evidence or EA-R03 money-movement work.

| Task | Authoritative delivery | Owner and consumers | Dependencies | Exit evidence and status at baseline |
|---|---|---|---|---|
| **INT-01 / L4-00** | Infrastructure-owned multi-repo Compose/devcontainer profile, immutable SHA/image lock, schema, same CLI, preflight, network/secret isolation, evidence, cleanup, reusable Actions workflow | Infrastructure; Shared contract review | Accepted ADR-SHARED-036; no AWS credentials | Codespaces AND Actions execute same pinned real dependency stack, clean success/failure teardown; **NO** |
| **INT-02 / L4-01** | IAM↔CP real-component profile and canonical generic fixtures | IAM, CP, Infrastructure, Shared | INT-01; actually executable identity providers; current contracts | Human/workload token issuance, audience, CP Principal mapping, grant/mandate, wrong-audience/revoked/cross-tenant denies on actual processes; **NO** |
| **INT-03 / L4-02** | Nabhold pilot with OIDC BFF, TLS session store and CMS provider/contents | Nabhold, IAM, CP, CMS, Infrastructure | INT-01/02, accepted provider bindings, qualified fixtures; branch IAM #116 must be merged before treating as baseline | Real callback/PKCE, CP current authority, CMS published vs preview, session revocation and no shadow frontend auth; **NO** |
| **INT-04 / L4-03** | Thamani B2B/B2C logistics consumer suite with provider-authorised flows | Thamani, CP, IAM, owning logistics/finance engines | INT-02; formally reconciled Thamani B2B/B2C ADR, contract and support | B2B Organisation and B2C person scope, quotes/bookings/tracking, failure and cross-tenant isolation; **NO** |
| **INT-05 / L4-04** | ZuriBeans B2B buyer/supplier/market consumer suite | ZuriBeans, CP, IAM, Trade, ERP and enabled providers | INT-02, certified consumer contracts | Buyer/supplier isolation, scoped market/corridor, product and document/quote flow where provider qualifies; **NO** |
| **INT-06 / L4-05** | Equator & Estate Co. independent consumer profile | Equator, CP, IAM, ERP and future property engines | INT-02; owner-approved domain capabilities | Truthful operating Organisation/legal actor, distinct tenant, property/construction work only where supported; **NO** |
| **INT-07 / L4-06** | Mandatory external API-only customer with **zero** DigitalEstate fixtures | CP, IAM, Shared, Infrastructure and selected provider | INT-01/02; canonical nullable estate where permitted | EXTERNAL_CLIENT Organisation/Tenant, subscription, workloads, context, provider API, audit, revoke and cross-tenant deny; **NO** |
| **INT-08 / L4-07** | Selective financial/event/regulatory mesh and uncertainty/recovery | Payments, Subscriptions, ERP, Trade, Regulations, Pulse, Trade Docs and owning engines | Relevant INT baseline, actual provider implementations | Real domain persistence/outbox and PEP, idempotency, delayed/replayed event, crashed actor and provider reconciliation; each external PSP/legal source explicitly classified; **NO** |

### 4.1 INT-01 must implement the accepted runtime contract, not an ad-hoc staging cluster

Infrastructure SHALL implement the exact requirements in ADR-SHARED-036 §§6.1–6.12: dedicated selectable .devcontainer integration profile; deterministic multi-repo materialisation from full Git SHAs; image digest provenance; Docker Compose profiles with isolate-by-run project name; unique disposable IAM test identities; verified TLS callback/issuer; health/readiness checks; mandatory positive and negative scenarios; documented executor resource requirements; timeouts; structured redacted evidence; reliable cleanup in success AND failure cases; least-privilege GitHub App/reusable workflow integration.

Local/Codespaces/Actions SHALL invoke one stable preflight/up/test/evidence/down CLI. No need for AWS account bootstrap. An untrusted PR runner never receives protected principals, real merchant secrets or AWS roles.

Existing Infrastructure L3 remains useful; preserve it, refactor/reuse working components. However **its older term L4="staging/design partner" SHALL NOT override** ADR-SHARED-036: name the **new L4** real-component, nonproduction integration, and classify actual staging as PROTECTED_STAGING/EA-09B by environment and evidence, not by ambiguous test-level naming. Do not promote unmerged feat/integrated-testing-strategy wholesale; reconcile against current main/ADR/contract pins.

### 4.2 INT-02 and INT-03 trust boundaries

A test SHALL use the real IAM protocol and current CP API rather than mocking the positive authorisation decision. Positive and negative proofs must include exact issuer, signing key, resource audience, code+PKCE/nonce, non-replayable callback, token introspection, CP Principal ID and grant, bound tenant/market/Organisation, authorised EngineInstance, resource server's independent security enforcement and same-run revocation.

The current Nabhold BFF remains disabled by default pending approved protected configuration. In local L4, **synthetic** issuer/client/principal fixtures are permitted if transparently labelled and no production material is used. Live protected staging requires separately approved real principals and signing ceremonies. Do not infer executive access from Keycloak login or a generic authority:self scope.

### 4.3 INT-07 is a platform invariant, not a later marketing enhancement

A synthetic unrelated EXTERNAL_CLIENT must be admitted and call at least one real domain API with NO DigitalEstate row, NO fake estate ID and NO Baobab-hosted website. It must have explicit subscriptions and actual capability/EngineInstance binding. A null estate is valid ONLY when the canonical operation supports it; a contract incorrectly requiring an estate must be amended by its owner, not bypassed in test code. Reuse same CP security, legal and audit checks as a first-party client. Its authentication can be service-to-service; identity assurance and permission are independent.

### 4.4 Source and release pin rules

Each L4 receipt SHALL name (i) candidate repository and full SHA, (ii) dependency approved SHA, (iii) Shared canonical schema/contract pins, (iv) OCI image digest/build provenance, (v) executing profile and resource limits, (vi) actual vs simulated provider, (vii) positive and negative scenario IDs, (viii) PASS/FAIL/BLOCKED/NOT_APPLICABLE (only for approved profile exclusions), (ix) scrubbed evidence digest/location and (x) reviewer authority if applicable. Floating main references and hidden mock substitutions are not sufficient in release candidates.

## 5. Integration and protected acceptance matrix

The full enforceable [acceptance matrix](ea-v2.2-integration-acceptance-matrix.md) is the **single canonical scenario identifier registry** for every profile. This plan references identifiers or scenario groups in that matrix; it MUST NOT define new overlapping IDs. The required common tests and additional named profile assertions are:

| ID | Boundary / positive and negative proof | Implementation authority | First profile |
|---|---|---|---|
| L4-IAM-01 | Real issued human token, exact JWT issuer/aud/signature/nonce/PKCE; bad issuer/expired/nonce denies | IAM, Nabhold | INT-02/03 |
| L4-IAM-02 | Workload registered target audience and scope; wrong audience/revoked client denies | IAM/Shared/CP/provider | INT-02 |
| L4-CP-01 | Actual Principal/Organisation/Tenant/context/grant; forged tenant/unmapped person fails | CP | INT-02 |
| L4-CP-02 | Provider, capability contract major, market and binding; wrong or stale instance fails | CP/provider | INT-02 |
| L4-CP-03 | Parent/sibling/external tenants denied without current mandate | CP/domain engines | INT-02 |
| NAB-01/NAB-02/NAB-03 | Nabhold encrypted BFF, session revocation and published CMS; restricted preview denied | Nabhold/CMS/IAM | INT-03 |
| INT-07 external API-only scenario | EXTERNAL_CLIENT with exactly zero Digital Estates can invoke allowed provider, but not another tenant | CP/IAM/provider | INT-07 |
| FIN-01/FIN-02/FIN-04/FIN-05 | Native Trade/ERP/Payments legal and financial veto, no bypass at COMMIT/dispatch | CP/owning engine | INT-08 |
| EVT-01 | Durable outbox/inbox idempotency, crash/replay/reconciliation | Event owners | INT-08 |
| L4-OPS-01 (failure/recovery) + REC-01 (backup/restore) | Accurate deployed image/capability observation, failover/rollback/secret and backup boundaries | Infrastructure/CP/engines | L4 and staging as appropriate |

A true positive must execute the intended authorised operation, not only parse its request. A true negative must prove the protected consequence was not committed/dispatched. A resource unavailable for a mandatory case causes BLOCKED/FAIL; no green with required skips.

## 6. Impact on EA-01–EA-13 and acceptance ownership

| Workstream | v2.2 required implementation/refinement | Owning repositories |
|---|---|---|
| EA-01 | Consumer-pinned canonical compatibility plus versioned manifest/evidence interface once cross-provider; no arbitrary new capability domain | Shared + consumers |
| EA-02 | Provider lifecycle, source/certified support, actual binding/grant and tested instance resolution | CP + engines |
| EA-03 | Immutable EngineRelease/EngineInstance, real deployed observation, change safety, pooled/bridged/dedicated placement and recovery | CP + Infrastructure |
| EA-04 | Actual human/workload issuer, principal mapping, federation, resource audience, revocation and policy negatives | IAM + CP + estates |
| EA-05 | Organisation-first progressive admission, external customer, responsible actor/mandate, group autonomy and no-estate context | CP + Shared |
| EA-06 | Delivery across real broker/outbox and controlled replay, retries, causality and data redaction | CP/engines/Infrastructure |
| EA-09A | **Required real-component synthetic L4 evidence** attached to component/contract release qualification | Infrastructure orchestrates; each provider owns result |
| EA-09B | Protected actual staging, external approvals, validated deployed binary, recovery and independent signed go/no-go | Infrastructure, Security, CP, providers, authorised reviewers |
| EA-10 | End-to-end trace from admitted principal to provider and auditable decision, no PII leakage | Engines/Infrastructure |
| EA-11 | Safe migrations, broker fault, revoked session, storage outage, reconciled unknown provider and actual restore drill | Engines/Infrastructure |
| EA-12 | First-party frontends as consumers only; external API-only path does not require DigitalEstate or CMS site | Estate owners + CP/IAM |
| EA-13 | Requirement-source provenance, real policy/resource authority and consumer tests; no synthetic legal source promoted | Regulations/Shared/CP |

EA v2.0/v2.1 have NO separately authorised EA-07/EA-08 workstream. This revision does not create either. EA-INT is a new cross-cutting delivery workstream, not a renamed unrelated programme.

**Responsible acceptance owner** for each capability/engine remains its repository's designated platform owner (unless formally delegated) as in v2.1 §11 decision 5. Infrastructure cannot certify CP grants or PSP eligibility; CP cannot sign its own AWS runtime deployment receipt; a first-party estate cannot certify its own legal identity.

## 7. Retained programme Gates A–E with new real-component evidence condition

| Gate | Completion criterion inherited from v2.1 | Additional requirement from ADR-SHARED-036 | Authority |
|---|---|---|---|
| **A — Architecture and contracts** | LA-00/01, PEO-01, resolved Organisation-first mappings and pinned consumers | Publish accepted ADR-SHARED-036, explicit no-estate consumer contract review, version-pin/evidence design and compatibility inventory | Shared/CP and impacted owners |
| **B — Developer unfreeze** | Gate A plus no frontend shadow authority; four founding consumer scopes | Verify each estate implements only presentation/BFF; avoid forcing external API-only tenants into EA-12 estate path. Testable interface design required, NOT completed L4 entire stack | CP/estate owners |
| **C — Controlled founding-group admission** | Four truthful Organisations/Tenants, scoped actors/mandates, independent classification and restricted pending services | L4 generic fixture proves sibling/parent/external denial; authentic real cases still separately reviewed | CP, IAM, legal evidence authorities |
| **D — Capability-specific staging qualification** | Actual CP, IAM, Subscription entitlement, legally scoped provider, appropriate certified requirements and current evidence | **Require passing relevant REAL_COMPONENT_SYNTHETIC_DATA L4 profile BEFORE protected staging qualification, then actual protected deployed end-to-end acceptance** | Owning engine/CP/IAM/Infrastructure and independent staging reviewers |
| **E — Production activation** | Real sources/PSP/KMS and deployed operation certification, recovery, signed go/no-go | Reconcile actual tested digests with ECS task/EngineInstance observations, tenant-specific external API protections, pooled/dedicated drift and release dossier | Release/security/operational owners |

No Gate A/B/C can be marked passed by the mere existence of ADR-SHARED-036. No Gate D/E is satisfied by a Codespace, real-component test or deterministic PSP fixture. Legal/source and provider requirement statuses stay independent of Organisation admission.

### 7.1 Consistency with v2.1 PEO-03 remap

PEO-03K SHALL continue to own the protected scanner/custody composition criterion; PEO-03F SHALL own independently certified official-source transport. The labels PEO-03L/PEO-03L2 in CP retain their scanner-runtime meanings. EA-INT does not add fake "L/M" canonical gates or legal source authority.

## 8. Production topology and tenant-neutral SaaS admission

### 8.1 Platform deployment

The AWS production baseline is already accepted by Infrastructure ADRs. Default region is **af-south-1**, not one region per commercial Market. Deploy private, independently scalable CP APIs/workers, IAM Kratos/Hydra and retained Keycloak federation, private APISIX backed by ALB/ACM and appropriate WAF, and independently qualified headless engines through immutable ECS/Fargate tasks/services **where compatibility is proven**. Durable services include managed RDS PostgreSQL 17 Multi-AZ, ElastiCache Valkey or approved compatible Redis, Amazon MQ RabbitMQ and engine-specific data stores; private network zones, KMS/secrets, telemetry, recovery and governance remain mandatory.

Infrastructure SHALL prove vendor-runtime compatibility for stateful components, notably iDempiere JVM, IAM, APISIX/etcd and Qdrant. Do not assert that every stateful engine is safely run on Fargate ephemeral volumes. OCI promotion builds once, deploys verified image digest, supports rollback/migrations and observes running tasks through the infrastructure deployment controller under existing ER-04/05 policy.

### 8.2 Logical and physical tenancy

One real Organisation can be admitted as an external platform client without owning any Baobab frontend. Default **pooled** EngineInstances serve multiple independently authorised tenants. A **bridged** profile dedicates selected service/data resources; a **silo** uses a stronger cell/account/region only where approved IsolationProfile/contract/regulation demands. A new Tenant SHALL NOT automatically deploy a copy of CP, IAM and every engine. Infrastructure owns physical resources; CP governs tenant desired state and which instance is bound. No cross-engine raw database read or group-admin wildcard.

A corporate subsidiary can exit Nabhold with its same Organisation/Tenant; the effective-dated CorporateRelationship and derived grants adjust under approval. It does not gain shared authority merely because its engine runs on the same Fargate cluster.

### 8.3 New external enterprise without DigitalEstate

Minimum governed lifecycle:
1. Evidence-backed canonical Organisation and eligible platform applicant; choose EXTERNAL_CLIENT PlatformRelationship and PlatformAccount under CP, not Nabhold affiliate.
2. Approve Tenant/PRIMARY Organisation, optional legal actor for required activities, market and isolation/residency requirements.
3. Accept Subscription entitlement, current CapabilityGrant/Binding and engine support; deny unactivated capabilities.
4. Register external workload client or approved user federation under IAM, with exact resource audiences/scopes and credential assurance.
5. Resolve CP context and approved EngineInstance; reuse shared provider unless stronger placement certified.
6. External backend invokes the authorized resource API through governed ingress; domain PEP checks actor and operations. Third-party webhook/API payloads are authenticated and replay protected.
7. Bill/audit/rotate/revoke/retain/exit under the appropriate agreements. DigitalEstate remains **absent** unless the customer independently opts into an estate product.
8. In a future multi-region cell, maintain one canonical identity and a reviewed single-writer authority/replication/failover regime. Do not introduce a second independent CP writer by convenience.

## 9. Critical path and execution order (parallel lanes)

### 9.1 Immediate gate-aware execution

| Position | Increment | Authority | Notes / dependencies |
|---|---|---|---|
| **EA-R00** | Adopt v2.2 baseline and refresh dashboard, audit, index and source-priority register | Shared | **This document**. ADR-SHARED-036 already Accepted |
| **INT-01** | L4 harness: Codespace + GitHub Actions parity | Infrastructure | Start now without staging AWS account, independent of CP real admission |
| **EA-R02** | Authentic legal/evidence/custody and independent founding mandates | CP/IAM/Infrastructure and sources | Continue in parallel. Real source and AWS protected evidence remain dependencies |
| **EA-R03** | Remaining P0-04B/LA-05 native execution-point safeguards (especially Payments D2, Subscriptions, Trade Docs and unmapped ERP/Trade classes) | CP/owning engines | Payments D1 already merged; distinguish native code from PSP certification |
| **INT-02** | IAM/CP real issuer, context and revocation | Infrastructure/IAM/CP | Requires INT-01 and approved source/contract pins; integrate but don't activate protected client |
| **INT-03** | Nabhold OIDC/CMS pilot | Infrastructure/Nabhold/IAM/CP/CMS | INT-02 plus IAM #116 merged and compatible client, not real executive access |
| **EA-R04** | Console/estate F-01…F-07, CX-06…10 and no shadow authority | CP/estates | Can proceed in parallel subject to Gate B |
| **INT-04/05/07** | Thamani, ZuriBeans, external **no-estate** profiles | Appropriate consumers/engine owners | Reuse L4; Thamani B2B/B2C ADR reconciliation first |
| **INT-06/08** | Equator upon domain maturity; finance/events mesh in selective profiles | Domain owners | Real actors/providers required for staging, synthetic fixtures permitted for L4 |
| **EA-R05** | Protected tenant/capability E2E, scanner/custody, provider and rollout acceptance | Infrastructure/Security/owners | Actual AWS config, approved credentials, independent legal/source/PSP evidence; no synthetic substitute |
| **EA-R06** | Operational publication, final provider/go-live certificates and signed activation | Independent release owners | All relevant Gate D/E requirements |

EA-R02/R03 source work SHALL NOT stop while INT-01 is built. Conversely absence of AWS staging access SHALL NOT block implementing the L4 source harness. Source work SHALL only be marked DONE when independently validated and merged; protected acceptance remains separate.

### 9.2 Critical-path blockers

| ID | Blocker | Owner / next source move | Source-programme effect |
|---|---|---|---|
| BL-01 | No merged ADR-036 L4 runner and cross-engine manifest | Infrastructure: INT-01 | Real-component integration gates cannot pass |
| BL-02 | IAM Nabhold human profile only in open PR #116, no real protected human principals | IAM + CP + approved reviewers | INT-03 profile needs source convergence; G04 real acceptance blocked |
| BL-03 | Genuine Nabhold/Thamani incorporation/control/mandate cases unaccepted | CP + independent authorities | Gate C/real financial operations blocked, despite synthetic tests |
| BL-04 | No confirmed protected AWS account/roles/bucket/identity/service endpoints (except af-south-1) | Infrastructure and authorised account owner | Gate D/E cannot be claimed |
| BL-05 | Incomplete native PEP catalogue and provider certifications | Trade/ERP/Subscriptions/Trade Docs/Payments/CP | Consequential operations cannot release |
| BL-06 | No first-party pilot complete CMS/IAM/CP issuer/binding acceptance | Nabhold/CMS/IAM/CP/Infrastructure | R0 acceptance and downstream baseline pending |
| BL-07 | External no-DigitalEstate path not demonstrated end-to-end | CP/IAM/Shared/selected engine | External SaaS admission acceptance pending |
| BL-08 | Thamani owner ADR still reflects B2B-only versus clarified B2B/B2C logistics requirement | Thamani owner | Profile INT-04 cannot imply unapproved business scope |
| BL-09 | Legacy Infrastructure integrated testing branch defines L4 as staging rather than newly accepted nonproduction level | Infrastructure | Must reconcile before reuse; no branch merge by assumption |
| BL-10 | Multiple open major toolchain dependency PRs (Node 26, TS 7, other major) | Per-repo maintainers | Review provenance, compatibility and vulnerability risk before accepting source pins |

## 10. Workstream/accountability and no-bypass review

| Authority | Accountable evidence | Cannot authorise |
|---|---|---|
| Shared | Accepted ADRs, canonical schemas/registries, consumer compatibility and this plan | Runtime business truth, cloud resources, provider certification |
| Infrastructure | Codespaces/L4 runner, Compose profiles, artifact lock/provenance, ECS/Fargate deploy/observations and backups | IAM grant, legal/tenant actor decision, actual PSP funds |
| IAM | Human/federated/workload token profiles, issuer, scopes, client activation and revocation | CP tenant membership or role-to-domain grant |
| CP | Real Organisations, Tenants, legal mandates, active context, bindings and capability resolution | Provider domain financial execution or fake infra deploy receipt |
| Nabhold | First-party BFF, confidential session and R0 experience | Group-wide tenant grant or cross-company legal actor |
| Thamani/ZuriBeans/Equator | Independently governed digital consumer experiences and applicable business rules | Other company or external tenant authority |
| Trade/ERP/CMS/Pulse/Regulations/Documents/Subscriptions/Payments | Own resource-server operation/records/events, contract and provider-conformance evidence | Self-issued global platform admission or false external certification |
| Legal/PSP/release/security reviewers | Specific independent source/provider/go-live acceptance | Replace required tests or invent protected stage evidence |
| External enterprise | Own BFF/workload and business operations permitted by agreement | CP authority or infrastructure configuration |

Every merged implementation affecting gates must add a register receipt with **commit SHA, contract pin, migration, CI run, owner approval, remaining live dependencies and rollback**. A draft branch, unmerged PR or CI-green isolated test is not a production support claim.

## 11. Gates for completion of v2.2 implementation

### 11.1 Engineering completion is profile-scoped

The L4 programme is source-complete ONLY when:
- INT-01 supports identical tested runner/manifest and cleanup from Codespaces and Actions with pinned real components, and no publicly exposed admin ports;
- INT-02 proves current real IAM issuer and CP policy with independent negative/revocation cases;
- INT-03 proves Nabhold BFF+CMS through actual complete callback, data and denied operations;
- INT-07 proves an unrelated EXTERNAL_CLIENT with **zero** DigitalEstate objects; and
- each subsequent profile meets its domain-required positive/negative and failure tests without silently skipped mandatory assertions.

Consumer profiles INT-04/05/06/08 are independently qualified as their accepted scope matures. The platform may develop or test incrementally, but **an affected capability cannot claim EA-09A cross-engine qualification until its mandatory profile passes**.

### 11.2 Production completion remains externally gated

Unrestricted customer onboarding or production use is NOT authorised until real workload registry lifecycle, actual approved provider instance/release, independent legal/PSP source where needed, protected IAM, S3/KMS scanner/custody, operational telemetry and DR restore, data retention, proper isolation/regional placement and signed Gate D/E activation evidence are present. Go-live is per capability and operating legal role, not a blanket global switch.

### 11.3 Plans and documents updated together

This v2.2 change SHALL:
- replace the live EA dashboard authority and status;
- register EA-INT and make real-component evidence distinguishable;
- preserve v2.1/earlier plans as historical and date-stamped, with references to v2.2;
- keep ADR-SHARED-036 Accepted, unchanged;
- register open candidate PRs and divergent branch gaps, without upgrading their readiness;
- add a reusable L4 acceptance matrix and new audit snapshot;
- annotate stale legacy production readiness percentages as **not a live GA determination**.

## 12. Change control, owner approval and next action

All the above provisions are **Accepted programme decisions** dated 15 October 2026 per the platform owner's explicit instruction to implement v2.2 and merge following green CI. Changes to authority, identity, tenant law, provider semantics or production compute require their respective owning ADR and review. Routine evidence refreshes may update the dashboard without a new plan version; substantive gate/sequence decisions require a documented Accepted revision.

**Next authorised implementation increment: INT-01** in baobab-platform/infrastructure. It builds a reproducible, isolated L4 harness; it does NOT create production tenant identities or deliver AWS staging. INT-02/03 follow its measured acceptance.

Reference: ADR-SHARED-036 Accepted (Shared PR #310); EA v2.1 Accepted (Shared PR #301); CP ADR-BCP-026/027; Infrastructure ADR-Infra-0002/0006/0015/0021; Nabhold Go-Live v2.0.