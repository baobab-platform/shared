# EA v2.3 — Development Enablement and Environment Assurance Implementation Plan
## EA-DEV-01: integrated proving ground, developer experience and protected promotion

**Status:** **ACCEPTED — Authoritative EA-DEV Programme and Delivery Obligations**, approved by explicit Platform Owner direction on 23 October 2026 and published through merged Shared PR #373. Acceptance authorises the engineering programme and its dependencies; **it does not mean the individual work packages, providers, integration cases, protected staging, or production operations have passed**.  
**Date:** 23 October 2026 (Africa/Johannesburg)  
**Owner:** Shared Platform Architecture / Platform Engineering; implementation remains owned by each repository.  
**Authority:** [EA v2.3](EA-implementation-plan-v2.3-2026-10-20.md); [Accepted ADR-SHARED-043](../adr/ADR-SHARED-043-Development-Provisioning-and-Environment-Approval-Boundaries.md); Shared ADR-036/015, CP ADR-017/020/021/023/026/027, IAM ADR-0033, Infrastructure ADR-0002/0020/0021, and applicable domain ADRs.  
**Canonical case IDs:** The [v2.2 integration matrix](ea-v2.2-integration-acceptance-matrix.md) remains the sole registry for L4/INT/NAB scenarios. This document neither changes case meanings nor deletes mandatory cases.  
**Scope:** EA-DEV is an execution lane within EA-INT, EA-ENG, EA-05 and EA-09, not a second Control Plane, engine, legal authority or production admission pathway.

## 0. Accepted executive mandate — outcome, rules and accountability

**Platform Owner ruling (23 October 2026): EA-DEV is ACCEPTED.** Every first-party Baobab engine, Digital Estate, Shared library, developer-tooling component and Infrastructure integration adopter SHALL follow this programme as its **engineering delivery baseline**, subject to more specific Accepted owner ADRs and immutable canonical contract authority. The already-Accepted ADR-SHARED-043 governs the removal of unnecessary *development-only independent-human approval holds*; it **does not** remove a real enforcement check, security rule, legal obligation or protected-environment approval.

### 0.1 Required outcomes and why this programme exists

EA-DEV SHALL make the following outcomes normal rather than exceptional:

1. **Self-service synthetic enterprise development.** One named developer or CI job can prepare a disposable, correctly isolated synthetic Organisation/Tenant/Market/role/mandate scenario, issue **real** IAM test identities and use CP-governed capabilities without waiting for a human staging/production approval. The CP guarded bootstrap is development-only, private, time-bounded and incapable of authorising real operations.
2. **One reusable path for any eligible engine.** IAM and CP form the common identity/tenant/context/capability integration spine; each engine brings its *own* domain adapter, database/migrations, providers and native execution vetoes. CMS, Payments, ERP or TMS are **not universal prerequisites**. The DEV-14 profile contract and DEV-15 Pulse/Payments exemplars are the adoption reference, not a bespoke Nabhold-only integration route.
3. **Visible capability and integration progress.** No executive, maintainer or developer should reconstruct platform readiness from dozens of GitHub PRs. A current source- and evidence-linked programme register SHALL show, for each required engine/capability/scenario: owner, deployed environment, current code/CI, actual integration, blocked reason, next action and separately authorised production state.
4. **Predictable, efficient inner development loop.** Every supported Codespaces/Actions profile SHALL have deterministic tool/source locks, a diagnostic preflight, selective services/tests, actual health observations, reproducible synthetic fixtures, private logs and idempotent reset/teardown. Full-platform build or independent protected approval SHALL NOT be required to edit and locally test one unrelated engine.
5. **Proven boundaries, not mock confidence.** Synthetic facts can exercise real IAM/CP/engine implementations; mocked issuers, fabricated JWTs, static CSS prototypes and source-only tests can never PASS an L4 real-component gate. Every applicable tenant, role, audience, market, legal actor, revocation, dependency-failure and cleanup negative case SHALL retain its original required meaning.
6. **Independent production promotion.** After protected acceptance of a genuinely supportable IAM/CP common foundation, mature providers may be independently deployed and granted to **specified** Tenants, Organisations, Markets, capabilities and legal actors. Business/regulated operation permission remains separate from deployment. The [EA-REL programme](ea-v2.3-progressive-production-release-programme-2026-10-23.md) governs the delivery sequence and never supplants EA-09, Infrastructure or domain authority.

**Success is measured by the existence and reproducibility of the developer workflows and real test receipts, not by the number of ADRs, scaffolded repos, pull requests, declared capabilities, containers or green source-only workflows.**

### 0.2 Normative acceptance language and precedence

- **SHALL/MUST** indicates a condition for completing the relevant *work package* or qualifying a release. **SHOULD** indicates the default improvement expectation, with documented owner-specific alternatives when defensible. **MAY** indicates optional engineering choice.
- **Accepted programme** means this implementation plan and its work packages are approved for delivery. **SOURCE_MERGED** means reviewed code is on the owning repo main. **REAL_COMPONENT_SYNTHETIC_DATA** means exact observed live-component assertions with synthetic data. **PROTECTED_STAGING** requires its separately approved topology, actual test execution and human evidence custody. **PRODUCTION_DEPLOYED** means observed running production artifacts, not service eligibility. **LIVE_OPERATION_AUTHORISED** requires exact current CP grant/mandate, native PEP and applicable business/legal/provider approval. No status silently implies the next.
- EA-DEV **SHALL NOT** grant CP/IAM roles or decide certification, change legal incorporation rules, define a capability outside Shared, activate an absent provider, override an owner-native financial veto, mutate another engine's database, or erase a historical receipt. The owning Accepted ADR prevails on domain semantics.
- **One operator can drive distinct synthetic maker/checker Principals in development**, but the *same Principal* approving its own consequential change must still be rejected. Protected staging and production apply independently authorised real-person separation where required.
- Staging/production SHALL use **separate protected accounts/roles, secrets, identities, databases, release artifacts and evidence**. Infrastructure SHALL prevent the development bootstrap command, test issuer, synthetic data and optional-development approval shortcuts from appearing in protected runtimes.
- A missing engine adapter may block **its own** integration profile/capability. It SHALL NOT become a new platform-wide prohibition on continued unrelated source engineering or a substitute for the required missing-provider status.

### 0.3 Assigned responsibilities (not a new approval authority)

| Accountable source owner | Mandatory implementation contribution | What the owner cannot self-assert |
| --- | --- | --- |
| **Shared Platform Architecture / Foundation** | Closed contract semantics; accepted cross-repo programme IDs; authoritative capability catalogue; scenario/evidence registry; drift and consumer-pin visibility | A source declaration is an EA-09 certification or CP ACTIVE binding |
| **Infrastructure / Platform Engineering** | Private profile orchestration; source/image lock; lifecycle and teardown; composed L4 receipt and environment isolation; protected release manifests, operational readiness evidence | An isolated dev run approves protected staging or production |
| **baobab-dev** | Compatible Codespaces toolchains and package/registry access, deterministic installs, developer diagnostics, documented engine onboarding and rollback of upgrades | The installed runtime image makes the native engine/service operational |
| **IAM** | Genuine issuer, test clients, token audience, signature, scopes, subject mapping, revocation/deactivation and protected identity operations | IAM authentication creates a CP Tenant grant or legal actor mandate |
| **Control Plane** | Canonical Tenant/Organisation/Principal/Market/capability context, guarded disposable bootstrap, governed effective grants/bindings/legal-actor policies and fail-closed resolution | A synthetic company becomes officially registered or an absent provider certified |
| **Each engine (Pulse, Payments, CMS, Trade, ERP, TMS, etc.)** | Its domain service/API, persistence and migrations, adapter/implementation evidence, authoritative native policy enforcement and positive/negative integration cases | The engine may bypass IAM/CP or authorise its own native finance/merchant/carrier state against owner policy |
| **Digital Estate owners** | Browser and journey contract, confidential BFF/client authority as applicable, current backend capability consumption, accessibility and truthful published feature exposure | A public website grants market or PSP legitimacy |
| **Independent protected approvers** | Actual authorised staging/production plan, security, operations, legal/provider and business GO for the exact protected scope | Development source-review or synthetic PASS alone satisfies protected acceptance |

### 0.4 Delivery and executive reporting contract

Every DEV-00..DEV-15 package **SHALL** keep one current register row with: **owning repo/person or accountable team; dependencies; source branch/head/merge SHA; mandatory CI result; real-component case IDs and results; environment and evidence class; blockers and explicit next action; source and receipt freshness; target and actual completion date; and production/protected acceptance as an independent field**. The current dashboard is a **read model**, never an alternative CP authority.

Progress SHALL use truthful states: NOT_STARTED → SOURCE_IN_PROGRESS → SOURCE_MERGED → LOCAL_TESTED → REAL_COMPONENT_SYNTHETIC_DATA, with actual failures/BLOCKED tracked per mandatory scenario. Staging and production are **separate progression axes**, not steps implicitly obtained by checking the development columns. The register MUST distinguish **not yet implemented**, **implemented but not tested**, **runtime failed**, **missing external input**, **not approved**, and **accepted**. A stale status SHALL display its observation date rather than pretend to be current.

**No global release hostage:** unrelated safe work proceeds in parallel. A blocked protected account/PSP/carrier prevents only the protected or provider-dependent activity, while CP/IAM/CMS/Pulse and other supported source/test work continues on controlled synthetic profiles.

### 0.5 Mandatory work-package exit rules

Each package DEV-00..DEV-15 requires (a) source/ADR/contract reconciliation, (b) reviewed merged code or authoritative documentation as specified for that package, (c) applicable positive and negative automated tests, (d) **actual** running component evidence for every L4-related acceptance, (e) redacted issuer/CP/engine/source and image provenance, (f) lease/credential/container/database cleanup where relevant, (g) owner runbook and security guidance, and (h) dashboard status/remaining blocker update. Required tests may report BLOCKED/FAIL but may never be omitted and counted PASS.

The original **seven INT-03C** and **fourteen NAB-03** case meanings remain mandatory and governed separately. The **2 January 2027** corporate websites objective is conditional on actual site/CMS/BFF/publication acceptance; live payments, trade commitments, carrier fulfilment, statutory finance or payroll remain separately scoped, regardless of website launch.

**Exit for the EA-DEV programme as a whole:** an engineer can select an eligible tenant/engine scenario, run genuine IAM + CP + the required native engine services in Codespaces/CI, exercise granted and denied capability operations, diagnose failures, preserve true receipts and tear down safely **without per-run independent staging/production appointments**; Pulse and Payments prove headless adoption without CMS; future engines follow the same contract without creating parallel IAM/CP authorities. Only *actual* execution can satisfy this exit. **EA-DEV status remains ACCEPTED while work-package completion remains independently partial/open until evidenced.**

## 1. Decision and source-grounded baseline

Retain **Accepted EA v2.3** as the authoritative architecture/portfolio plan. Its 23 October amendment already adopts ADR-SHARED-043. This companion makes that decision executable without rewriting the dated 20 October audit or reopening an architecture version.

**Verified repository sources at drafting (not proof of live runtimes):**
- Shared: Accepted ADR-SHARED-043 and closed development/v1 enterprise profiles for synthetic Nabhold, ZuriBeans, Thamani, Equator and unrelated external API-only client.
- CP: merged PR #433, standalone development-bootstrap command and development-only image; fresh marked database, dedicated role, bounded 24-hour maximum lease, synthetic IAM subjects, CP-minted IDs and PROVISIONING/UNKNOWN provider status. The production image excludes bootstrap.
- Infrastructure: the existing L4-00 Compose foundation runs PostgreSQL, Redis and RabbitMQ, **not** the full current IAM/CP/CMS/estate chain. Existing INT-03C docs expressly do not claim seven-case actual qualification. Historical Infrastructure #49 independent-human packet is optional for isolated development, not a normal DEV hold and not protected acceptance.
- baobab-dev: config/versions.lock at inspection pins Python 3.14.6, Node 24, PostgreSQL 17 client tooling and pnpm 11.24.0. Major upgrades require tested consumer compatibility, not unreviewed pin changes.
- Important modeling limitation: the current CP bootstrap uses synthetic DEV legal-entity references and UNVERIFIED profiles. These disposable fixtures are safe but insufficient on their own to demonstrate a genuinely unincorporated Organisation acting under a separately authorised legal entity.

**Operating principle:** Development proves the security and business controls using real components and synthetic facts. Protected staging proves a reviewed deployment and its operations. Production proves legally and commercially authorised scope. A passing lower gate never promotes itself into a higher gate.

## 2. Environment trust and evidence matrix

| Lane | Permitted enterprise data and identities | Provisioning approval | Proof and limitations |
| --- | --- | --- | --- |
| Local workstation / Codespaces | Fresh synthetic Organisations, Tenants, legal/evidence claims; scoped actual test issuer; no production data | Standing ADR-043 authority, normal code review, one named technical owner | L0–L4 evidence only as executed; lease and cleanup |
| Ephemeral pull-request CI | Same, with no protected credentials accessible to untrusted source | Automatic approved test profile | Pinned source/image, negative tests and sanitized receipts |
| Isolated shared development | Synthetic and bounded; owner, quota, TTL, private access | Normal dev owner, no per-run independent real-human ceremony | Real-component synthetic evidence and fresh credentials |
| Protected staging | Approved topology and credentials; synthetic/sanitized data by default; real claims subject to review | Actual independent security/operations approval for protected provisioning | Deployment, recovery, access and legally relevant scenario evidence |
| Production | Live lawful identity, data, keys, payment/provider access | Scoped independent business/security/operational GO, legal/provider approval where applicable | Current legal actor × market × operation × tenant × provider authority |

Environment selection is not a string override. Bootstrap must depend on the *conjunction* of labelled fresh database, restricted database role, permissible image/command, isolated network, issuer trust, unprivileged credentials and bounded run. Unknown or staging/production environment fails closed; no development principal, registry row, seed or token may auto-promote. Preserve engine-owned databases and release artifacts; build once and promote exact immutable digests with reviewed environment configuration.

Independent human maker/checker approval is **not required per synthetic development run**. Distinct synthetic Principals and negative same-Principal checks remain mandatory. Protected staging and production require independently authorised actual people for the consequential controls in scope.

## 3. Legal verification — at the action which depends on legal truth

| Proposed action | Development treatment | Stage/production treatment |
| --- | --- | --- |
| Create synthetic Organisation / Tenant and test admissions | Synthetic provenance, no official company verification | No fictitious incorporation represented as real |
| Start an emerging enterprise profile or non-incorporated business | Simulate claims/verification without false legal identity | Legal form and representation checked as applicable; company incorporation **not universal** |
| CMS draft, market research, product draft | IAM+CP scope and isolation, no universal incorporation test | Publication must not misstate business identity/rights; relevant claim checked |
| Live seller, invoice issuer, employer, PSP beneficiary, importer/exporter | Model valid/expired/missing/market-wrong synthetic mandate and domain PEP | Verified responsible legal person and activity-, role-, jurisdiction-, effective-time-bound mandate and provider/legal permissions |
| Market expansion, new role or regulated feature | Test requirement applicability and negative branches | Reassess the **affected** legal, tax, product, corridor or provider evidence |
| 24-month founding-group documentary deferral | Test expiry, no reset, denied nondeferrable items | Only specifically approved platform documents may be deferred; never waive law, provider KYB or a financial/legal veto |

Nabhold remains a non-trading holding business in the reference profiles; ZuriBeans is B2B trade; Thamani B2B integrated logistics. ZuriBeans and Equator are modeled as operating Organisations rather than fabricating separate incorporation. An explicit Nabhold legal-actor mandate may be tested synthetically but does not establish a live right to trade or issue invoices. Corporate affiliation is never cross-tenant entitlement.

CP evidence stores independently the assertion, evidence source, verification action/result, purpose, applicable policy/version, effective period and authority. A first-party registry digest cannot by itself mark incorporation VERIFIED.

## 4. Dependency-ordered engineering work packages

**DEV-00 — Decision/gate reconciliation (P0; Shared, CP, IAM, Infrastructure, estates).**
Inputs: Accepted ADR-043, current EA/INT/NAB cases. Deliver: single precedence table resolving development-only historical INT-03C/#354/#49 holds, current dashboard, owner map and CI gate policies; preserve former receipts. Exit: a missing optional #49 packet cannot block an authorised disposable synthetic run, nor authorise protected staging. No removal of same-Principal denials or native PEP.

**DEV-01 — One paved-road integration command (P0; Infrastructure + baobab-dev).**
Inputs: DEV-00, existing L4 Compose. Deliver: exact-source/image pinned preflight, prepare, up, test, evidence and down entrypoints; private run state; automated recovery/cleanup; equivalent GitHub Actions and dedicated Codespaces entrypoints; selected profiles. Exit: fresh create–run–destroy, retry after interrupted startup, failed health checks, and orphan recovery are proven. Missing digest, wrong image, public admin port or surviving credentials fail.

**DEV-02 — Accurate CP Organisation/tenant/mandate fixtures (P0; CP + Shared).**
Inputs: DEV-00/01; merged CP #433. Deliver: consume closed development/v1 profile and extend scenario coverage for unincorporated Organisation, synthetic parent legal actor, scope-bounded valid, missing, stale, revoked and wrong-market mandates; CP owns all canonical IDs. Exit: actual PostgreSQL transaction and API negative tests; no source-only approval, fictitious legal VERIFIED, manually written engine bindings or protected bootstrap exposure.

**DEV-03 — Real issuer and CP authority chain (P0; IAM + CP + Infrastructure).**
Inputs: DEV-01/02. Deliver: isolated genuine Hydra/Kratos and/or approved federated identity issuer profile, current issuer/subject/audience mapping, distinct maker/checker Principals, workload credentials, auth code/PKCE where used, CP context and revocation/deactivation. Exit: real signed issuer token succeeds only for own tenant/current grant. Wrong audience, sibling/external tenant, expired/revoked identity, same-Principal approval and absent capabilities deny.

**DEV-04 — Seven-case INT-03C qualification (P0; Infrastructure + IAM + CP).**
Inputs: DEV-03 and current immutable source locks. Deliver: seven original INT-03C case assertions over actual services (including issuer independent read-back, Principal lifecycle and teardown), sanitized per-case evidence, source/image/contract pins, private custody. Exit: genuinely observed results or precise BLOCKED/FAIL, never mock PASS. Independent-human optional #49 run is not a prerequisite for DEV; staging remains separate.

**DEV-05 — Nabhold IAM/CP/BFF/CMS vertical (P0; Nabhold + CMS + CP/IAM + Infra).**
Inputs: DEV-03/04 and actual CMS capability. Deliver: real confidential BFF session, CP current context, Payload scoped read/draft/publish/preview/revalidation and all applicable original fourteen NAB-03 case meanings. Exit: real positive and preview/withdrawn/cross-tenant/wrong-role/revoked/outage/recovery cases with exact service receipts; an absent provider stays BLOCKED.

**DEV-06 — External client without estate (P0; Infrastructure + CP/IAM + eligible provider).**
Inputs: DEV-03. Deliver: INT-07 unrelated synthetic API-only client, zero DigitalEstate records, current OAuth/CP entitlements and real engine resource call. Exit: valid self-scope permitted, parent/sibling/unentitled access denied, no invented Baobab site.

**DEV-07 — ZuriBeans B2B capability slice (P1; ZuriBeans + Trade/ERP/Docs/Regulations).**
Inputs: DEV-03 and available adapters. Deliver: real-component buyer/supplier Organisation and buyer Principal, market catalogue, RFQ/quotation, native guarded order/ERP/documentary steps **only where implemented**. Exit: per-operation actual results, no side-door native commitments, wrong legal actor/market, duplicate/replay, absent grant, separate market tests; unavailable provider reports BLOCKED.

**DEV-08 — Thamani B2B logistics capability slice (P1; Thamani + TMS + Docs/Regulations + Infra).**
Inputs: DEV-03 and TMS provider readiness. Deliver: B2B customer/partner quote, booking, tracking and proof-of-event when *real TMS* exists. Until then a site prototype demonstrates UX only, never transport provider support. Deny invented carrier, ETA/custody, unapproved transport legal actor and unrelated tracking access.

**DEV-09 — ERP, finance and Subscriptions references (P1; ERP + Finance/Payments + Subscriptions + Infra).**
Inputs: DEV-02/03 and accepted operation catalogue. Deliver: disposable iDempiere database/JVM integration and supported native posting/recording tests, accounting responsible legal actor, actual GL provenance where supported; no fake bank/PSP settlement. Exit: atomic native proof in real JVM+DB when runnable, isolated company/org mapping, deny unknown classes, wrong actor, duplicate posting, stale authorisation or unsupported provider.

**DEV-10 — Developer tooling and contracts (P1; baobab-dev + Shared Foundation + each consumer).**
Inputs: DEV-01 baseline. Deliver: checked per-repo environment manifest, GHCR auth/noninteractive install, exact Node/pnpm project pins, Python/Go/Java/Postgres compatibility, versioned image/toolchain matrix and rollback procedure. Exit: a clean Codespace launches and can fetch private packages without credential leaks or interactive Corepack prompts; toolchain upgrade branch tests all affected projects and physical PG migration separately.

**DEV-11 — Observability, browser experience and CI test routing (P1; Infrastructure + Shared + estates).**
Inputs: DEV-01. Deliver: correlation from BFF → issuer/CP → engine/outbox, redacted logs, clear BLOCKED cause, per-PR affected profiles and full nightly/release qualification; browser Playwright/accessibility, performance and private preview where permitted. Exit: failure diagnosis shows exact source/profile/scenario and non-sensitive cause, never a fake-green skip or token leaked to tracing.

**DEV-12 — Database, migration and resilience drills (P1; each persistent engine + Infrastructure).**
Inputs: DEV-01/02. Deliver: migrate from fresh and supported previous engine schemas; real start-up data, crash and lease fencing, event replay/idempotency, snapshot restore and clean reset. Exit: each engine owns its database and migration, an old PostgreSQL physical volume cannot silently become PG17, and wrong-tenant/stale write/native side door cannot bypass the PEP.

**DEV-13 — Independent staging/production entry (protected; Infrastructure + Security/Ops + legal/domain owners).**
Inputs: applicable qualifying DEV-04..12 and actual approved account/roles. Deliver: protected source/image manifests, authorised distinct people, secret/issuer/network controls, independently reviewed legal/provider evidence where relevant, recovery/rollback, release signoff. Exit: actual observed protected acceptance for a scoped capability/tenant/market/legal actor; development CLI/keys are unusable there; production requires separate GO.

**DEV-14 — Reusable engine onboarding framework (P0-enabling; Shared + Infrastructure + baobab-dev + engine-template).**
Inputs: DEV-01/02/03 and existing Shared environment, capability-provider and synthetic-enterprise contracts. Deliver a **fourth, separate integration-run descriptor** with a closed schema, minimal dependency graph, IAM/CP setup reuse, isolated native stores, selected test cases and truthful evidence. The descriptor composes, but never replaces, the three existing owner contracts; it cannot grant access or certify providers. Initial reference implementations are Pulse and Payments. Exit: a new engine can integrate with actual IAM/CP without copying Nabhold-specific BFF/CMS workflow or building a new identity bootstrap. CMS is **optional** for headless engines. See the [detailed engine-onboarding specification](ea-dev-reusable-engine-onboarding-2026-10-23.md).

**DEV-15 — Pulse/Payments first-adopter runtime profiles (P0 parallel after DEV-03; Infrastructure + baobab-pulse + baobab-payments + IAM/CP).**
Inputs: DEV-14 descriptor adoption and genuine IAM-issued workload/CP context. Deliver (a) the Pulse intelligence evidence search/research-mission flow against actual Pulse PostgreSQL/Qdrant, with classification, projection and tenant-denial tests; and (b) Payments sandbox intent/cancel/authorise/capture/refund against a real Rust Payments service and genuine caller authority. Payments must always mark **simulated** outcomes; no actual funds, HyperSwitch or PSP certification is implied. Exit: current issuer→CP→engine requests, capability + negative-case receipts, cross-tenant denial, safe cleanup and exact BLOCKED codes for unimplemented native/financial paths, independently of Nabhold CMS DEV-05.

### Cross-repository precedence

DEV-00→01/02→03→04→05 is the initial connected Nabhold path. **DEV-14 composes reusable engine profiles once DEV-01/02/03 are available; DEV-15 (Pulse and Payments) proceeds in parallel with DEV-04/05 and does not wait for CMS.** DEV-06 can proceed once 03 exists. DEV-07/08/09 proceed in parallel as providers mature. DEV-10/11/12 are parallel enablers, not general freezes. Protected DEV-13 is a **later promotion gate**, never a gate on doing ordinary source development. Do not create one infrastructure stack per legal entity where secure pooled engine instances suffice.

### DEV-00 publication and ongoing reporting

The [DEV-00 reconciliation](ea-dev-00-gate-reconciliation.md) holds the single
precedence table and source/CI policies. Maintain the [implementation register](ea-dev-implementation-register.md)
through its checked JSON source; report exact source observations and unresolved
owner adoption without substituting them for real component or protected proof.
The register is a read model, not a new contract, permission or scenario authority.

## 5. Golden reference profiles and acceptance

| Profile | Required reference behavior | Explicitly separate |
| --- | --- | --- |
| IAM/CP | Native provider, signed issuer, CP actual principal/current tenant, all seven INT-03C cases | protected credentials and live legal facts |
| Nabhold corporate | Non-trading group executive BFF → CP → real CMS content/publish; 14 NAB-03 original cases | CMS site UX vs provider certification |
| ZuriBeans B2B | B2B buyer/supplier, authorisation and market/legal-actor native Trade/ERP/documents | missing provider/real export rights |
| Thamani logistics | B2B enterprise, scoped quote/book/track when TMS actually runs | nice prototype vs real carrier/transport |
| Equator | Independent operating Organisation, separate tenant, legal actor scope | property rights, title and building licences |
| External API-only | unrelated headless client, **zero estate rows**, current binding and denial | not a first-party IAM tenant |
| Finance | scoped ledger/accounting and native class veto | not a disbursement, credit or tax certification |
| Pulse headless intelligence | real IAM/CP workload → baobab-pulse PostgreSQL canonical evidence + Qdrant projections → classification-scoped search/mission | not a CMS dependency or LLM/regulatory certification |
| Payments simulated sandbox | real IAM/CP authorised workload → Rust baobab-payments payment lifecycle with all outcomes simulated | not HyperSwitch/PSP, live money transfer, payment readiness or production entitlement |

Every supported profile tests own-tenant success; sibling/external denial; missing grant; issuer/audience mismatch; expiry/revocation; wrong activity/market/legal actor; dependency failure/recovery; idempotency/replay; bounded clean teardown; claim truth. A missing mandatory scenario is FAIL/BLOCKED, not NOT_APPLICABLE. Preserve evidence categories: SOURCE, LOCAL_TESTED, REAL_COMPONENT_SYNTHETIC_DATA, PROTECTED_STAGING, EXTERNAL_CERTIFICATION and PRODUCTION_ACCEPTANCE independently.

## 6. Developer experience requirements beyond onboarding

1. **One developer journey.** One clearly documented integration CLI and a diagnostic doctor command. It checks GHCR auth, certificate trust, private ports, Docker, database markers, issuer callbacks, secrets, Corepack and lockfiles; failures explain actionable remedies.
2. **Paved road, not universal heavy image.** Keep baobab-dev as tooling; engines run their appropriate containers. Use light per-repo Codespaces by default, opt-in 16 GB+ integration lab and dedicated browser/Java tools only as required. Local hot reload changes only affected services.
3. **Measure speed before setting release promises.** Establish clean/cached startup and first useful test p50/p95; track feedback-to-PR, CI minutes, flaky checks, cost per real profile and dependency download failures. After baseline, propose scoped targets and investigate regressions, rather than inventing metrics.
4. **Realistic synthetic data by design.** Deterministic generators with fresh nonce, proper ZA/UG currency/market/locale values, buyer/supplier roles, missing incorporation, changed mandates and denied cases; never copy production PII or official/legal documents.
5. **Clear capability discovery.** Publish per-engine actual adapter support, current provider/binding readiness and reasons for BLOCKED/NOT_IMPLEMENTED. A test image or mock must never self-declare IMPLEMENTED or approved.
6. **Private ephemeral preview.** Deploy reviewed, private per-PR site previews if permitted; never route write paths to production. Browser UX and static demo receipts are distinct from connected IAM/CP/CMS proof.
7. **Operational diagnosis.** Trace request and event correlation, sanitized structured logs, recoverable startup failures and explicit health; developer sees what blocked a capability, not just a red CI workflow.
8. **Safe parallel engineering.** A source/code PR checks directly affected profiles; main/nightly test larger integration matrix; a release candidate must pass all required cases. Unavailable TMS/payments/payroll must not block safe unrelated CMS or frontend development.
9. **Toolchain change control.** baobab-dev pinned pnpm 11.24.0 is the observed baseline, not a claim that pnpm 12 is supported. Upgrade in a separate compatibility PR: exact published release/security advisory, packageManager/Corepack, lockfile, TS/Next/Vitest/Medusa compatibility, CI, image digest, roll-forward/back.
10. **Supportability, security and cost.** CODEOWNERS/runbooks/example adapters, least-privilege private registries, short-lived secrets, image/SBOM pinning, automatic orphan sweep, scoped CPU/RAM profiles, a11y/keyboard and low-bandwidth/mobile test pathways.


### 6A. Developer throughput and correctness improvements — prioritised proposals

These improve daily engineering beyond provisioning. They create **no additional independent approval gate** and must not become mandatory work on unrelated engines. They are testable follow-up tasks under DEV-10/11/12/14, sequenced by observed friction:

| Priority | Experience improvement | First implementation owner | Concrete exit |
| --- | --- | --- | --- |
| **P0** | **Cross-repository dependency/contract impact planning** | Shared + Infrastructure | A PR change planner identifies affected engine contracts and minimal profile tests from actual imports, contract-lock SHAs and execution paths; when unsure, conservatively tests more |
| **P0** | **Stable error vocabulary and runnable policy explanations** | CP/IAM + Shared + consumer owners | Denied capability reports a redacted reason category such as missing grant, invalid audience, wrong tenant/market, stale mandate or provider unavailable; never disclose other-tenant existence |
| **P0** | **Reusable scenario data factories and deterministic time** | Shared + CP + engine owners | Seed/clock/run IDs vary by disposable run; controlled time tests expiring grants, evidence, tokens, retries and dates; replay produces same expected outputs with new isolated identifiers |
| **P0** | **Contract compatibility and consumer-driven cross-version tests** | Shared + engines | Producer/consumer pinned-current contract pairs pass bidirectional old/new compatibility where specified, with deprecation windows and clear migration evidence; no silent release break |
| **P1** | **Domain-local mocks separated from real L4 providers** | Each engine + Infrastructure | Fast component test uses explicit fakes, but isolated L4 profile cannot pass unless genuine required component/issuer/CP request was observed; simulated PSP marked separately |
| **P1** | **Replayable event flows and outbox/inbox inspector** | Infrastructure + event owners | A developer can trace a synthetic event across producer, broker and consumer, replay it safely and observe idempotency, duplicate, wrong-context, stale-schema and dead-letter behavior |
| **P1** | **Local observability bundle and cross-engine trace search** | Infrastructure + Shared | One private correlation ID links issuer → CP → engine → event consumer; token/PII redaction and retention tests demonstrably pass |
| **P1** | **Recovery + migration rehearsal and chaos scenarios** | Infrastructure + engine owners | Kill/restart provider/broker/DB under a run profile; verify bounded retries, canonical idempotency, stable recoverability and no lingering disposable resources |
| **P1** | **Developer onboarding guide and per-engine self-service template** | engine-template + baobab-dev | An unfamiliar engineer can follow one documented path to generate a profile, start an engine, run first real own-tenant/denial tests, diagnose and destroy it |
| **P2** | **Lightweight engineering status portal** | Shared + Infrastructure | Read-only status page groups required checks, provider readiness, exact source pins, current failed run and links to GitHub artifacts; **no duplicate registry or CP authority** |
| **P2** | **Cost- and connectivity-aware profiles** | baobab-dev + Infrastructure | Baseline low-resource/offline-friendly contract tests, selective large L4 suites, warm caches, private GHCR package mirror policy and South Africa/UG realistic high-latency tests; log runner cost |
| **P2** | **Automated dependency/toolchain upgrade rehearsals** | baobab-dev + affected repos | Tool upgrades (including pnpm major versions) use trial branch, exact image/lock pins, clean Codespaces startup, contract/runtime suites, rollback, and observed compatibility—not an automatic fleet-wide bump |

**Observability must not become a privacy leak**: logs/explain messages are authenticated, tenant-filtered, private, redacted, bounded and cannot reveal another tenant's grants, documents or identities. **Component mocks remain valuable for speed**; only evidence-class claims are restricted. Synthetic data may model ZA/UG market needs, local-language formatting, multi-currency, interruptions and low-bandwidth connectivity without falsely claiming any legal compliance certification.

**Suggested adoption order:** first deliver DEV-14/15 plus P0 dependency impact, scenario factories and diagnostic codes, then measure Codespaces/CI friction; select P1/P2 from observed operational bottlenecks. Avoid a platform-wide process freeze or adding a new authority service as the implementation shortcut.

## 7. Target windows (not a promise of completion)

| Proposed target | Actual exit expected |
| --- | --- |
| **26 October–1 November 2026** | DEV-00/01/02 core composition, guarded profiles, DB/lease negatives and cleanup |
| **2–8 November** | DEV-03/04 real issuer/current CP seven-case qualification, or exact actionable blockers |
| **9–15 November** | DEV-05/06 Nabhold CMS BFF connected acceptance and no-estate external consumer evidence |
| **16–29 November** | DEV-07/08/09 engine-specific real slices in parallel; no pretend TMS/PSP completion |
| **30 November–13 December** | DEV-10/11/12 hardening, browser/a11y and recovery, reviewed release candidate |
| **14–31 December** | Independent protected-staging qualification and selective approved site promotion |
| **2 January 2027 target** | Public Nabhold, ZuriBeans and Thamani sites only for approved public capabilities; payments/transport/accounting operations remain independently gated |

Source and runtime readiness, not calendar pressure, determine actual gate transitions. A public CMS site can launch without suggesting that unrelated regulated payment or logistics capabilities are operational.

## 8. Evidence, scorecard and stop conditions

Per work item/PR record: owner, governing ADR, exact Shared/engine source SHA, artifact digest, migrations, current stage, positive and denied case IDs, actual running services/issuer/current CP context, CI evidence link, redacted logs/hash, cleanup receipt, dependency BLOCKED reasons, next action and rollback. **Do not publish passwords, tokens, DSNs, legal documents, employee data or real identity records** in a public PR. The live dashboard records latest status without rewriting older snapshots.

Measured scorecard: verified clean profile starts; zero unneeded dev-human approval waits; source→real integration elapsed time; cold/warm Codespace boot and first-test distribution; Codespaces GHCR/pnpm installation success; CI flake and false-green rate; mandatory scenario completeness; cleanup/orphan rate; cost per passing L4; source contract drift; negative tenant/actor tests; restoration and migration recovery; browser accessibility and private preview quality; independently accepted staging and production scope.

**Immediate stop conditions:** dev-bootstrap reachable in stage/prod; live secret or data injected into CI; forged bearer/evidence/corporate verification; access to another tenant without grant; same Principal checks own consequential mutation; incorrect legal seller/issuer; money/posting side door; missing cleanup; a mandatory L4 case wrongly marked PASS; unsafe database migration. Stop that operation and retain evidence; do not stop unrelated safe engineering.

## 8A. Progressive production-release handoff (EA-REL)

The [Progressive Production-Release Programme](ea-v2.3-progressive-production-release-programme-2026-10-23.md) is the **separate protected promotion and operations** programme for DEV-13 and independently qualifying engines. It makes CP/IAM the **first candidate shared production foundation** and permits subsequently mature providers such as CMS, Pulse, Trade, ERP, TMS and Payments to be released individually with actual EA-09 evidence, protected operators and precisely scoped CP/market/legal-actor approvals. It does **not** turn any current source or L4 milestone into staging or production acceptance. A production-deployed engine may remain **dark** with no authorised live tenant operation. CMS and the public estates are their own release units and need not be a prerequisite for Pulse or other headless capabilities.

The EA-REL dashboard reports independent **source, runtime, stage, deployed-health and business-activation** states rather than one global green label. Normal synthetic development remains free of per-run independently appointed-human approval under ADR-SHARED-043; signed independent approval remains mandatory at applicable protected transitions. Full plan status and acceptance belong to the owning release records, not this documentation link.

## 9. Publication, adoption and rollback

- Publication rule: when this document is present on `shared/main` after reviewed required CI, EA-DEV is the active **execution lane**. On an unmerged PR branch it remains a candidate. Neither publication nor programme activation changes any Accepted ADR, stage-human approval, production gate, scenario ID or historical receipt.
- Repository owners deliver separate narrow implementation PRs with current Shared pins; reconcile merged status and mandatory CI before dependent changes.
- Rollback disables the failing disposable profile, revokes generated credentials, removes owned volumes/containers and restores prior version pins. Never roll back by enabling unguarded bootstrap, inventing provider support or reopening obsolete general human approval holds.
- Any change of *legal authority semantics* or *domain permission* needs its own owning ADR/Shared contract review, not a convenient plan edit.

**Done also requires the first two headless engine adopter profiles (Pulse and Payments) to publish truthfully scoped runtime outcomes without CMS, and an accessible onboarding template for subsequent engines.**

**Done means:** Every supported enterprise journey starts, executes positive and negative real-component tests and tears down repeatably under a single developer's control with truthful evidence; unavailable capabilities remain visibly BLOCKED; production and staging remain independently and appropriately governed.
