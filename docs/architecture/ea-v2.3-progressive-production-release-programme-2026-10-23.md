# EA v2.3 — Progressive Production-Release Programme
## EA-REL — Foundational CP/IAM production, independent engine adoption, scoped business activation

**Status:** Proposed execution companion to the Accepted [Enterprise Architecture Implementation Plan v2.3](EA-implementation-plan-v2.3-2026-10-20.md). Becomes the active EA-REL delivery lane **only after** Shared source review, required checks and merge; publication does **not** approve a protected environment, real actor, provider, deployment or production operation.  
**Prepared:** 23 October 2026 (Africa/Johannesburg)  
**Owners:** Platform Architecture / Platform Owner (programme); Infrastructure (release/deploy/operations); IAM (issuer and identity federation); CP (canonical control authority and tenancy); Shared (capability/contract semantics); each engine and Digital Estate (its own implementation and capability acceptance); independent appointed reviewers for protected staging, security, legal/provider and production business activation.  
**Governing sources:** [EA v2.3](EA-implementation-plan-v2.3-2026-10-20.md), [EA-DEV](ea-v2.3-development-enablement-implementation-plan-2026-10-23.md), [ADR-SHARED-043](../adr/ADR-SHARED-043-Development-Provisioning-and-Environment-Approval-Boundaries.md), Shared ADR-015/017/036, CP ADR-BCP-026/027, IAM ADR-IAM-0033; Infrastructure [ADR-Infra-0002](https://github.com/baobab-platform/infrastructure/blob/main/docs/adr/ADR-Infra-0002-aws-account-environment-region-strategy.md), [0020](https://github.com/baobab-platform/infrastructure/blob/main/docs/adr/ADR-Infra-0020-ci-cd-infrastructure-change-governance.md), [0021](https://github.com/baobab-platform/infrastructure/blob/main/docs/adr/ADR-Infra-0021-application-deployment-promotion-release-manifests.md), [0022](https://github.com/baobab-platform/infrastructure/blob/main/docs/adr/ADR-Infra-0022-deployment-rollback-database-change-safety.md) and service-specific Accepted owner ADRs.  
**Constraint:** There is **no** globally green enterprise/engine production flag; a service may run without any organisation, market, capability or regulated operation being activated. EA-REL does **not** modify EA-09A/EA-09B or Gate D/E acceptance semantics or waive statutory/provider conditions. The platform *may* release the foundation before every engine; it has not yet proven eligible to do so.

## 1. Release strategy and trust model

**Decision:** Treat Baobab as a collection of independently released, backwards-compatible services with two initial common authorities—**IAM and CP**—and one or more separately deployable digital estates/engine providers. A complete enterprise portfolio is **not** the prerequisite for a safe production foundation. Conversely, passing development L4 with synthetic data does **not** permit a live enterprise to use an incomplete service.

Sequence the **smallest useful protected and supportable production capability**:

1. **Foundation**: independently reviewed Infrastructure, protected IAM and CP in production, private durable databases, gateway, identity, secrets, backups, monitoring and response. An empty or restricted CP tenant catalogue is legitimate. First deployment is *dark/internal-restricted* with no normal customer entitlements.
2. **Digital estate and CMS**: separately certify and deploy the qualified Payload CMS provider, the corporate BFF/site consumers and their own release manifests; approved public pages can launch while commercial backends remain disabled.
3. **Independent service providers**: release eligible Pulse, Trade, ERP, Subscriptions, TMS, Regulations, Trade Docs, other engines *one provider/capability version at a time* with existing consumer contracts and current CP instance/grant/binding checks. CMS is **not** a prerequisite for headless engines.
4. **Consequential operations**: enable live payments, payroll, accounting commitments, carrier movement or other regulated/customer-affecting operations only after **additional** exact PSP/bank/employer/legal-actor/market/operational acceptance and owner-native PEP tests.

Track four orthogonal states:

| Axis | Authority / example | What it does NOT imply |
| --- | --- | --- |
| **Source / qualification** | Committed code + SHA, contract pin, tested runtime case, security and integration receipt | deployed or live |
| **Deployment / observation** | Infrastructure: exact image digest running, configured, healthy, recovery-tested in a specified environment | certified capability or an entitled Tenant |
| **Provider / resolution** | Shared defines capability; engine declares support; EA-09 independently certifies where required; CP governs current EngineInstance, availability, binding, grant, scope | legal eligibility of a specific operation |
| **Business / market operation** | CP legal/Organisation/tenant/market/context + native domain execution veto + independently valid legal/provider approval | entitlement for other tenants, markets or functions |

Never infer higher-order state from the existence of a Docker container, green CI, dashboard colour, prior frozen source receipt, accepted ADR, earlier market evidence or a real public website.

## 2. Release units and the dependency rules

- The **release unit is a versioned service/artifact and a narrowly described capability slice**, not the entire Baobab GitHub organisation, holding company or enterprise family. When two changes cannot remain backward/forward compatible, a deliberately coordinated release is permitted with explicit cutover and rollback evidence.
- Foundations are **shared** where the Accepted tenancy/isolation profile permits it. No automatic new CP/IAM installation per subsidiary or geography; data/legal boundaries remain independently enforced. A real customer may have **zero** DigitalEstate.
- **Development**, **protected staging** and **production** use separately restricted roles, keys, network/state and preferably accounts per Infra-0002. The known deployment default \`af-south-1\` is not a blanket claim that all cross-border data/activities may legally reside there.
- **Provider-specific release** may depend on IAM+CP capability/context/API contract, and on its own actual persistence/broker/native vendor services. It does **not** depend on an unrelated engine or website, except where that concrete capability's contract actually requires it.
- **Public site go-live** depends on qualified public edge, published CMS/source content where CMS is the provider, legal/brand representations and accessible/performance-tested site navigation. Live B2B trade orders, carrier bookings, payment capture or finance posting remain separate features and may stay disabled.
- **Cohabitation of revisions** must be tested: client and provider old/new contract pair, semantic version/capability compatibility, overlapping IAM issuer keys and audience boundaries, CP API/read-model and event-schema dual support where applicable.
- No engine reads/writes another engine's native database, creates its own CP canonical Tenant/Principal, locally declares itself ACTIVE or bypasses independently approved release/signer boundaries.

## 3. Dependency-ordered programme and acceptance

| ID / stage | Delivery owner | Implementable package and observable exit | Blockers that must remain scoped |
| --- | --- | --- | --- |
| **REL-00 — readiness truth and inventory (P0)** | Shared + Platform Engineering | One authoritative per-service/release/capability/tenant/market dashboard; exact commit, Shared lock, OCI digest, current mandatory CI, real L4, staging, ops/GO evidence and accountable owner. Historical snapshots immutable; no future-looking DONE. | Missing sources, unsigned qualification and stale provider receipts never appear ready |
| **REL-01 — protected production landing zone (P0)** | Infrastructure + Security/Ops | Explicit approved AWS env/account/OIDC state+roles, private networking, gateway/TLS, KMS/secrets/rotation, managed durable store and migration policy, backup/PITR+restoration, observability/SLO, on-call + incident/break-glass, security scans/SBOM, image attestation, least-privilege deployments, actual test of isolation and rollback. Dev bootstrap denied. | Region alone or Terraform source cannot count as protected environment. No dev state/issuer/secret/credential copied in |
| **REL-02 — IAM/CP foundation qualification and dark launch (P0)** | IAM + CP + Infrastructure, independent reviewers | Prove real staging IAM human/workload issuance, signed audience, key rotation, current CP Principal/tenant/market/capability/mandate resolution, revocation/deactivation, wrong-audience/cross-tenant denial, fresh registration, failover/restart and restore; witness logs and protected topology; independently approve **exact** production artifacts. Deploy production privately with **no default real tenant entitlement** and limited operator/test access. | DEV-03/04 seven INT-03C source tests and prior INT-02 synthetic run are not protected staging or production evidence |
| **REL-03 — foundation operational acceptance (P0)** | Security/Ops + CP/IAM + Infrastructure | Observe actual release digest/issuer DNS/TLS and gateway, backups and restore, alerts/on-call, recovery/rollback, admin separation and approved access reviews; monitor controlled rollout and record production operational acceptance for the **foundation only**. | Operating IAM/CP does not certify a legal company, CMS or payment provider |
| **REL-04 — CMS and public digital estates (P0/P1)** | CMS + Nabhold/ZuriBeans/Thamani + Infrastructure | Qualify and promote CMS and site/BFF releases independently, exercise current IAM→CP→CMS private/public scopes and mandatory **14 NAB-03** case meanings; test navigation, access, cache, content publishing, a11y, performance, legal disclosures, DNS/TLS, restore and rollback. Release each public site only after its own approved GO. | An unqualified live cart/order/ship/settle endpoint is disabled, not masked behind an unsafe frontend-only flag |
| **REL-05 — headless intelligence and other low-risk providers (P1)** | Pulse + future approved engines + CP/IAM/Infrastructure | First exemplar: Pulse actual evidence-search/research-mission operations, tenant/classification denials, Postgres canonical/Qdrant projection, producer data rights, SLO and support runbook. Independently promote an approved Pulse provider/version. Apply same process to Regulations/Trade Docs or other capable engines as contracts mature. | CMS is **not** required for Pulse; unqualified AI/regulatory claims are never enforcement decisions |
| **REL-06 — trade/logistics/accounting domain releases (P1)** | Trade + ERP + Subscriptions + TMS + domain reviewers | Narrow capability slices: B2B catalogue/RFQ before native order commitment, TMS quote before real physical booking/tracking, ERP reference/reporting before native financial posting, etc. Each release exercises real IAM/CP/engine authority, market/legal actor, tenant isolation, native execution veto, delivery/read-model/event compatibility, migration and rollback. | Market access, source-only code and provider declaration never authorise activity or commercial launch |
| **REL-07 — money and regulated launch (separate, P1/P2)** | Payments + Finance/ERP + business/legal/PSP/bank/security | Real-world charge, capture, refund, settlement, accounting/posting, payroll or logistics activity activated **only** after actual independent actor, jurisdiction, PSP/bank/carrier, statutory and reconciled provider tests, fraud/dispute/refund controls, key custody and signed business GO. Sandbox is simulation only. | Never infer D2 real PSP, bank funding, certified native accounting or statutory compliance from dev money simulation |
| **REL-08 — release operations and iterative promotion (continuous)** | Infrastructure + Shared + each owner | Versioned release manifest pipeline with build-once/publish-digest, scan/provenance, protected staging, canary/progressive exposure, telemetry and rollback decision, independent scoped approval, immutable receipts and non-propagating per-engine release cadence. | Source merged != staging observed != production GO; one engine's failed release must not globally block safe unaffected development |

**Dependency graph:** DEV-01..04 prepare the real issuer/CP L4 lab; **REL-00/01 can proceed concurrently with developer experience work**. REL-02 requires REAL protected environment evidence in addition to INT-03C/CP/IAM acceptance; REL-03 follows its protected qualification. REL-04 and REL-05 can be *developed* in parallel, and qualify their own protected slices as IAM/CP services become eligible. REL-06/07 depend on their specific CP/IAM and provider/legality contracts, **not** the completion of every other engine. REL-08 accompanies each promoted slice. Unavailable approval only blocks the actual protected deployment/operation in scope.

## 4. Production foundation gate checklist (REL-01..03)

**G1 — Security, infrastructure and accountable humans:** independent authorised security/operations roles; verified separation of reviewer/operator/issuer where required; protected GitHub environment OIDC plan/apply/deploy rights; approved private DNS, WAF/gateway configuration where applicable; network segmentation; managed credentials and rotation; no development bootstrap in any production image or route; least-privilege platform administrators; break-glass logging and reconciliation.

**G2 — IAM/CP functional authority:** real provider issuance (Kratos/Hydra, approved Keycloak federation), token verifier and trust bootstrap; exact issuer/audience/client and workload scopes; Principal lifecycle and revocation; CP authority for Organisation, Tenant, Market, Principal, legal actor mandate and capability resolution; cross-tenant/group and zero-estate client denial; same-Principal maker/checker rejection for consequential actions; independent review of operator rights.

**G3 — Data and operations:** separate **production** IAM and CP databases, independently secured state; migrator identity, idempotent migrations, backup/PITR and witnessed restore, verified runbook and stated RTO/RPO after testing; encryption in transit/at rest, retention and access logging; no direct cross-engine database writes. For PostgreSQL major upgrades (including target 17), logical restore or verified upgrade migration, never an implicit physical-volume swap.

**G4 — Resilience and deployability:** build once, pin exact OCI digest and contracts; review release declaration + environment secret references; independently verify deployed running digest and migration/version; authentication and CP fallbacks deny safely during outages; measure health/SLO, exercise token signing key rollover, issuer outage, CP failure and incident escalation; dry-run actual rollback or forward-fix according to Infra-0022 (code, config, data and external effects differ).

**G5 — Scope and business:** dark/limited internal production is the first possible GO; no real customer tenant admission or consequential operation until its **separate** Organisation/legal actor/market/permission/source and provider GO. Production infrastructure presence alone does not make a regulated engine or website eligible.

**G6 — Evidence custody:** independent protected staging and production approvers sign exact gate decision with role, timestamp, artifact digest, deployment identity, restoration and scenario receipts, dependencies, expiry and explicit authorized scope. An issue, assignment, proposed person or code-only approval is not a signed production GO.

No one may change this gate by toggling an environment string. A failed G1–G6 keeps REL-02/03 HELD with specific actionable reasons while ordinary development and other approved source tasks continue.

## 5. Each later engine follows the same small release protocol

For each proposed provider capability \`engine_id / implementation_key / capability@major / version\`, repeat **only the applicable** domain steps, reusing the already-qualified IAM/CP/Infra platform foundation:

1. Identify current canonical Shared catalogue contract, engine/provider declaration, production-permitted status and implementation/source evidence. Confirm owner/native data boundaries and compatibility with current CP/IAM interface.
2. Establish engine-local actual L4 proof against current IAM/CP and fresh synthetic tenants (using DEV-14/15 reusable headless onboarding). Run both own-tenant success and all applicable unauthorized negative, expiry, duplicate/replay and dependency failure tests; keep unsupported operations BLOCKED.
3. Independently qualify exact engine provider/image/data migration in protected staging, recheck all consequential legal/finance/provider obligations relevant to this capability. A real engine may be stage-eligible while its commercial operation is not.
4. Infrastructure publishes and promotes a **single immutable source-built image** by digest, release manifest and environment references; owns the private deployment. Engine owner owns persistence migrations and native runtime proof; no unreviewed schema destructive operation.
5. Observe the exact deployed instance, health and readiness. CP, via normal governed lifecycle, registers/verifies its EngineInstance, capability bindings and explicitly granted tenant/market/role scopes; do not self-activate or inherit Nabhold-group access.
6. Canary the approved consumers/tenants with health, auth/denial, event and customer outcome telemetry; retain roll-forward/rollback and contract downgrade decision. Permit independent service release while keeping unauthorized capabilities disabled at **the server/native PEP**, not merely by UI hiding.
7. Independently sign the **business activation** for each consequential production operation; name exact legal seller/employer/merchant/transport provider, market, expiry and independent authority. Retain artifacts and revoke/deactivate immediately when eligibility expires.

**No global release hostage:** optional ERP or PSP missing? A safe public CMS and qualified Pulse evidence API may still be independently promoted. But a consumer that actually depends on that missing provider must fail closed and show a truthful BLOCKED capability; no implicit fallback to ungoverned storage, a third-party API or a synthetic provider.

## 6. Mandatory release record and management dashboard

Publish a source-controlled release decision record per actual release **separate from** runtime secrets and protected evidence, linking immutable private custody refs. Proposed minimum fields:

| Field | Value meaning |
| --- | --- |
| Release ID, environment, service/engine/provider/version | What candidate, where and who owns it |
| Immutable source SHA, Shared contract pin, OCI digest, database migration | Exactly what was reviewed, tested and deployed |
| Integration qualification | Real L4 case IDs, tests actually observed, synthetic-vs-real provider classification and blockers |
| Protected stage verdict | Approved/HELD, independent human authority, network/issuer/data boundaries, restore/rollback and private evidence pointer |
| Production deployment verdict | Actual digest/readiness/telemetry and operating owner; can be **DEPLOYED_DARK** |
| Capability readiness | Contract/declaration/EA-09 certification/current provider health, CP grants/bindings and per-tenant status |
| Business activation | \`DENIED\`, \`INTERNAL_ONLY\` or **explicitly** \`LIVE_AUTHORIZED\` for specific Tenant + Organisation + Market + activity + legal actor + provider, valid-until and revocation |
| Rollout plan and state | Canary scope, kill switch at native PEP, rollback class, consumer versions, alerts, next review |
| Owner + next action | One responsible engineering owner, independent protected approver and actual next blocker |
| Evidence class | Distinguish SOURCE, REAL_COMPONENT_SYNTHETIC_DATA, PROTECTED_STAGING, PRODUCTION_DEPLOYED and PRODUCTION_OPERATION_AUTHORIZED |

**These are candidate reporting labels for the management register, not a replacement for the canonical CP provider lifecycle/status enumeration.** The dashboard shall **read** GitHub, Infra receipts and CP-authorised read models; never become an extra authority that writes a provider ACTIVE, fabricates a legal VERIFIED status or promotes runtime approvals. Use bounded cached reads with freshness/source SHA and display UNKNOWN when evidence is missing.

Release health should be visible at a glance across the portfolio: per-repo current main, open PR/migration, tests, L4, stage, production observed, live customer capability, owner, latest evidence and next blocked dependency. Maintain historical and current status separately to avoid disorientation from stale dated audits.

## 7. First production release waves and launch focus

| Wave | Candidate | Measurable exit | Can it happen without all engines? |
| --- | --- | --- | --- |
| **W0 — engineering foundation** | Disposable IAM/CP, DEV-14/15 + reproducible headless integration | Real signed issuer/CP L4 with negative coverage and truthful receipts; no real customer data | Yes; no protected production claim |
| **W1 — production landing/foundation** | IAM + CP + required Infrastructure/observability + gateway | G1–G6 qualified staging then independently signed production *dark/internal* deployment and resilience observation | **Yes** |
| **W2 — public digital estates** | Nabhold, ZuriBeans, Thamani + qualifying CMS/BFF frontend slices | All applicable NAB-03 and estate acceptance, published content, independent site-level GO; commerce/transport/payments dark unless separately qualified | **Yes**; target 2 January 2027 remains conditional |
| **W3 — independently useful providers** | Pulse first where ready; then Trade/Regulations/Docs/ERP/TMS in scoped slices | Actual IAM/CP/engine native tests, provider-specific stage/ops and market/tenant activation proof | **Yes**, each independently |
| **W4 — consequential commercial operations** | Real payments/settlement, financial accounting/payroll, contracting/shipping/regulated features | Native veto, verified real legal actor, applicable statutory and PSP/carrier/regulator requirements, reconciliation and independently signed exact GO | Only **after** their domain approvals |

**Calendar and authority distinction:** the 2 January 2027 public website objective is not itself authorisation for trade, logistics, payroll or settlement. The order of W2 and W3 may overlap, because Pulse does not need a CMS website. W1 must be safe to operate without real tenant authorisation. The readiness of any future engine can bring it ahead of a less mature one, subject to its actual dependencies.

## 8. Implementation actions and independent PR order

| Work package / owning repo | PR deliverable (not already implemented merely because written here) | Acceptance |
| --- | --- | --- |
| **EA-REL-00 — Shared** | Add release progression/portfolio decision matrix and link EA v2.3, EA-DEV, dashboard | README/contract/source references valid, no false gate transitions, owner/status evidence |
| **EA-REL-01 — Infrastructure** | Production landing-zone plan and identity/security/backup/gateway observability attestation wiring; review current staging roles/state | Actual independent approved plan and operators before provisioning; no use of DEV credentials |
| **EA-REL-02 — IAM + CP** | Independent production deployment candidate manifests, current integration/negative tests, issuer/CP revocation, trust/key recovery, version compatibility and operator runbooks | Source CI + real current L4, protected staging and independent signoff separately observed |
| **EA-REL-03 — Infrastructure** | Build-once release manifests, deployment read-back, canary, rollback/recovery proof and per-engine release receipts/dashboard projection | Immutable digest equals deployed runtime, fail-closed error and safe previous-version compatibility |
| **EA-REL-04 — CMS + Nabhold/ZuriBeans/Thamani** | Site BFF/CMS intake, realm/context-bound content and per-estate feature activation policy and release candidate | Real CMS integration, no 404 auth/entry, no unqualified transaction paths |
| **EA-REL-05 — Pulse then domain owners** | Adopt reusable IAM/CP L4 engine onboarding; independently qualified provider release per domain | Tenant/scope negative tests, native provider truth, image and migration acceptance |
| **EA-REL-06 — Payments/finance/carrier/legal reviewers** | Standalone real-PSP/financial/regulated activation packet by operation | No simulated PSP or synthetic legal verification promoted to real payment/transport authority |
| **EA-REL-07 — Shared + Infrastructure** | Executive portfolio read view with fresh multi-axis source/CI/runtime/market evidence | Read-only from actual owners, current status refresh, no invented corporate/funding approvals |

**Definition of Done for this programme (not blanket production readiness):** an independently accepted foundation can remain safely running while real engine owners deploy, qualify and activate one supported capability at a time; failed engine releases cannot grant other tenants rights or bring down unrelated production services; each state and next action is visible with evidence. Actual W1 qualification and any W2–W4 GO remain **NOT DEMONSTRATED** until source, staging, live observations and independent approvals exist.

**Rollback/reversal:** a release candidate may be revoked/cancelled before deployment. A running deployment with defects is handled using the appropriate Infra-0022 category (stateless release rollback, config reversal, compatible DB change, PITR/restore, forward fix, external-effect reconciliation) and a human incident decision where warranted. Never blindly replace a PostgreSQL data directory or release secret to simulate rollback.

## 9. Explicit programme guardrails

- No new "EA-REL approver" replacing actual Infrastructure, EA-09, IAM, CP, company/legal or native domain approvers.
- Normal development remains approved under Shared ADR-043; this protected release lane adds **no new per-run developer-human approval**.
- No auto-promotion of sample Nabhold/ZuriBeans/Thamani legal registrations, group corporate relationship, bank accounts, carrier providers, regulatory status or operator appointment into protected IAM/CP rights.
- No customer-facing claim that a website being live means its checkout, cross-border shipping, credit, payroll or settlement is live.
- IAM and CP may be running production with zero external organisations and with no customer-facing products. A running service has operational accountability even if no customer is onboarded.
- Production audit/evidence custody and independent human signoff stay at the **protected** boundary. CI approval of a documentation PR does not grant protected deployment.
- No direct connections from dev environment to production legal/identity/financial data or native databases. No cross-tenant fallback; missing required capability denies.
