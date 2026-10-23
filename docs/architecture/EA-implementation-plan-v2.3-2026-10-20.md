# Baobab Platform Enterprise Architecture Implementation Plan v2.3
## African Enterprise Excellence, Integrated Execution and Cross-Repository Product Readiness

**Status:** **ACCEPTED — Normative EA Programme Implementation Plan**
**Approved:** 20 October 2026, by explicit Platform Owner programme direction; acceptance of this plan does not certify any capability, provider, legal case or production deployment.
**Effective execution baseline:** Upon successful merge into `baobab-platform/shared/main`, subject to mandatory CI and repository review controls.
**Authoritative location:** `baobab-platform/shared/docs/architecture/EA-implementation-plan-v2.3-2026-10-20.md`
**Owner:** Baobab Platform Architecture / Platform Owner; implementation acceptance stays with each independent owning authority.
**Basis:** [20 October 20-repository audit](ea-v2.3-cross-repository-evidence-audit-2026-10-20.md), [v2.3 acceptance/ownership delta matrix](ea-v2.3-acceptance-and-adoption-matrix.md), [live EA dashboard](ea-dashboard.md), [v2.2 real-component canonical L4 scenario matrix](ea-v2.2-integration-acceptance-matrix.md), [Nabhold Go-Live v2.0](https://github.com/baobab-platform/nabhold/blob/main/docs/go-live/NAB-GOLIVE-MP-001.md).
**Governing architecture:** Shared ADR-0001–0006; accepted ADR-SHARED-007/017/018/019/021/026/032/034/035/036/037/038/039/040/041; accepted CP ADR-BCP-026/027; IAM ADR-IAM-0033 and approved supplementary identity/assurance decisions; all relevant accepted domain/estate and Infrastructure ADRs.
**Conditional/not approved:** ADR-SHARED-033 remains Proposed; ERP ADR-ERP-023's Accepted **document in unmerged PR #110** is not an ERP-main source adoption; TMS ADR-0003–0019, TMS-TECH-01 and SCF ADRs/SCF-TECH-01 are Proposed.
**Previous plan:** [EA v2.2](EA-implementation-plan-v2.2-ADR-SHARED-036-integration-reconciliation.md), Accepted 15 October 2026, is superseded **only for active programme sequencing/evidence status** upon v2.3 merge. Its substantive accepted controls and all earlier applicable owner ADRs remain binding. v2.1/2.0 retain dated historical authority for unchanged approved substantive decisions; no silent rollback.
**Linked programme:** Nabhold Go-Live Masterplan v2.0 remains independently Accepted. No automatic version increment or altered legal/staffing/go-live status is implied.

> **Architectural status is not implementation status.** Accepted ADR ≠ accepted canonical contract ≠ merged working code ≠ verified real-component integration ≠ protected staging ≠ statutory/provider/legal certification ≠ production permission. Every row and claim must preserve its exact evidence category, owner, source revision and expiry/freshness.

---

## 1. Founding purpose and engineering charter

**Baobab Platform is being engineered to set the standard for African enterprise software, learning from proven global systems, adapting their strengths, challenging their weaknesses and building capabilities genuinely suited to African enterprises.** This is an ambitious quality/product direction, not an empirically verified market ranking or permission to appropriate third-party IP.

**Normative ADR-SHARED-041 engineering principle, verbatim:**

> **Learn from established products. Reuse what is proven. Question what is inadequate. Re-engineer what must improve. Build what Africa needs.**

Every first-party engine, corporate estate, external-facing product, infrastructure tool, Shared library and developer workflow SHALL follow proportionate **Adopt / Adapt / Re-engineer-Replace / Build Independently** evaluation when making material technical choices. A product shall be measured by user outcomes, trustworthiness, local applicability, maintainability, security, ability to integrate and actual operational quality—never by advertising phrases or number of generated ADRs.

**Africa-first does not mean one African jurisdiction.** Legal employers, local regulatory regimes, tax years, country-specific data rights, official authorities, currencies, settlement rails, languages, availability/connectivity constraints, accessibility, sector regulation and cross-border requirements must be independently evidenced. Country expansion SHALL not reuse regulatory rules or grants without effective-dated local validation. Products must remain globally interoperable.

The programme shall create original first-party African enterprise value while retaining legitimate vendor-source/licence provenance and independently governed commercial product roadmaps.

## 2. Why v2.3 is required

v2.2 introduced the necessary shared real-component L4 harness and tenant-neutral consumption contract (ADR-SHARED-036), but the 15 October source freeze is no longer an executable next-work queue. After v2.2:
1. Infrastructure INT-01 and INT-02 completed **bounded frozen-pin synthetic Actions qualifications**; the next connected integration is INT-03, not initial INT-01. Interactive Codespaces parity and protected environments remain separately unaccepted.
2. IAM human-client source, Nabhold confidential BFF, CMS source and further private-handoff preparation advanced without a complete actual IAM↔CP↔Nabhold↔CMS run.
3. Accepted ADR-SHARED-037/038/039 made native financial and Trade operation families, payment provenance and CP-approved seller bindings far more precise than a generic PEP backlog.
4. Accepted ADR-SHARED-040 introduced a cross-estate experience and frontend release/testing system; ADR-SHARED-041 introduced mandatory engineering-product philosophy for every first-party repository.
5. Thamani's **Accepted ADR-THA-0018** superseded B2C storefront assumptions with a primary **B2B integrated logistics** business. TMS remains only a foundational architecture, and the old INT-04 B2B/B2C phrase is now misleading.
6. ERP's proposed Baobab People/PG17 adoption creates a strategic human-capital/payroll/localisation lane, without making an unmerged ADR, statutory rules or a third-party payroll plugin production-ready.
7. Discovery identified **20 first-party repositories** including new/low-maturity TMS/SCF, the engine template, dev-image supplier and legacy Equator site. Previous delivery sequences did not explicitly account for their independent maturity and adoption.
8. Live EA dashboard source evidence has progressed beyond the earlier v2.2 narrative and needs one unambiguous active owner/priority baseline.

**v2.3 changes scope coverage, ownership, dependency sequencing, product-quality requirements and active register hygiene; it does NOT replace existing authority boundaries or invent a second system of record.**

## 3. Normative interpretation, precedence and method

**3.1 Document ordering**
1. Applicable law, independently verified official evidence, actual vendor/provider/financial/legal permissions and platform security restrictions; no architecture claims legal permission not granted.
2. Accepted Shared canonical contracts and architecture decisions, accepted CP/IAM/Infra/domain/estate ADRs within each authority.
3. This Accepted EA v2.3 governs cross-repository scheduling, evidence coordination and acceptance handoffs, not unilateral amendment of an owning domain protocol.
4. Nabhold Go-Live v2.0 and other Accepted local execution plans govern their own business milestones where compatible with higher authority; Shared v2.3 adds cross-engine prerequisites.
5. Proposed ADRs, illustrative samples, unmerged branches and pending PRs inform investigation only.
6. Dated evidence snapshots describe only the inspected source/runtime and can be superseded by a later dated, verified register receipt; they do not silently change an Accepted architecture.

**3.2 Requirement language**
SHALL/MUST is mandatory; SHOULD is strongly recommended, with a documented narrowly scoped exception and approval; MAY is permitted only within established rights. All work must reference accepted authority, exact source/contract versions and a testable Definition of Done. Architecture disagreements require the owning ADR and consumer compatibility review before implementation.

**3.3 Classification is non-negotiable**
- `ARCHITECTURE_ACCEPTED`: normative decision only.
- `CONTRACT_ACCEPTED`: canonical Shared semantic/schema and exact consumer pin.
- `SOURCE_MERGED`: immutable owning repository `main` commit, independently passing applicable checks.
- `LOCAL_TESTED`: bounded tests against identified build and fixtures, including negative cases.
- `REAL_COMPONENT_SYNTHETIC_DATA`: specified actual version-locked runtimes, signed issuer, CP context, database and provider API with explicitly synthetic organisations; no live credentials/merchant.
- `PROVIDER_SANDBOX`: named external vendor sandbox with scoped contractual test authorisation, not production.
- `PROTECTED_STAGING`: independently observed provisioned/authenticated deployed environment with approved identity, secret custody, legal/data controls and recovery evidence.
- `EXTERNAL_CERTIFICATION`: independent legal/official source, payroll practitioner, financial services, PSP/carrier/customs or other role-specific acceptance as applicable.
- `PRODUCTION_ACCEPTANCE`: scoped live capability, legal-actor/market/provider/instance approval, rollback, operational observability and signed go/no-go.

Gate table cells continue to use **YES / PART / NO / EXT / N/A**, with exact evidence links and freshness. `PART` is not `YES`. The L4 scenario runner continues to report **PASS / FAIL / BLOCKED / NOT_APPLICABLE** per required scenario; missing mandatory scenario ≠ skip/pass. Source-level CI is not a protected acceptance receipt.

## 4. Immutable platform invariants

1. **Organisation-first legal autonomy:** one governed PRIMARY Organisation per active Tenant; distinct canonical Organisation, Tenant, LegalEntity, DigitalEstate, Market, legal-actor mandate, PlatformAccount and CorporateRelationship. Founding-group ownership/sponsorship never supplies automatic cross-tenant authorisation; subsidiaries can operate/exit independently.
2. **External enterprise is first-class:** unrelated customers may use existing pooled/bridged/silo engines through governed APIs with **zero Baobab DigitalEstate** objects; no universally mandatory first-party frontend/CMS or copy of CP per tenant.
3. **Authority and provider neutrality:** Shared controls canonical capability/event/contract meaning, CP context/admission/grants/bindings/provider resolution, IAM identity/session/workload trust, Infrastructure physical topology, domain engines their own protected operations, Subscriptions commercial billing, Payments money execution, ERP accounting and finance, Trade commercial orders, TMS physical transport, Trade Docs authoritative document workflow, Regulations regulatory decision/evidence and Pulse advisory intelligence.
4. **Legal and financial execution vetoes:** every consequential native execution point independently enforces current CP/legal-actor/role/capability and domain financial/provider evidence. ERP journal/payables recording never authorises fund transfer; one company cannot spend/contract as another. Replays, internal/admin/native paths do not escape PEP.
5. **No invented certainty:** legal source absence, unknown market clearance, incomplete status, unqualified provider, stale grant, partial evidence or failed integration results in fail-closed/unavailable/unknown, not fabricated approval. Regulated deductions or AI advice do not become executable decisions without qualified human/statutory review.
6. **Cryptographic/version provenance:** exact pinned Shared contracts, image digests, signing keys, source commits, migration IDs, event history, receipts, source trust and immutable releases. No floating `main` or mock substitution in candidate/protected evidence.
7. **Privacy and reliability:** least privilege, lawful purpose, classification/retention, redacted observability, cryptographic custody, PII minimisation, durable event/outbox and recovery. Personal salary, identity, KYB and financing facts never leak through generic reporting or AI embeddings.
8. **Operational honesty:** no runtime support from an Accepted ADR, no capability grant from a successful login, no provider certification from a metadata declaration, no protected deployment from Compose or Codespaces, no production signoff from a PR merge.
9. **No universal frontend or new runtime engine by habit:** Shared packages are neutral, each estate retains independent brand/experience/release and legal scope. New engines require justified accepted role, technology and Shared capability contracts; proposed TMS/SCF designs cannot mint authority.
10. **No imprecise African localisation:** effective-dated country and legal-regime packs, with reviewed official sources, golden test vectors, multi-currency precision, portability and distinct jurisdictional certification.

## 5. Dated audit baseline, current and historical source

**Governing source audit:** [20-repository 20 October audit](ea-v2.3-cross-repository-evidence-audit-2026-10-20.md), including all exact `main` SHAs and candidate PR counts. It records Shared, Infrastructure, CP, IAM, ERP, Trade, Payments, Subscriptions, CMS, Pulse, Regulations, Trade Docs, TMS, SCF, baobab-dev, Nabhold, Thamani, ZuriBeans, Equator Estate and engine-template.

The **acceptance owner** SHALL update [ea-dashboard.md](ea-dashboard.md) after any merged gate-moving PR with commit/PR head, pinned Shared version, source/CI run, schema/DB migration, tested principal/market/capability/engine, provenance receipt, reviewer, external dependencies and rollback. Current dashboard statements are updated by dated new receipts; old 15/18/19 October sections remain historical even if stale. An open PR does not advance a gate.

### 5.1 Material freeze facts, as of 20 October

- **INT-01/02:** accepted bounded Actions synthetic qualification at specified commits; no evidence of new-pin/protected or complete Codespaces interactive acceptance.
- **INT-03:** connected Nabhold identity, actual approved CMS provider and full NAB-01–04 still OPEN; Infrastructure #37 and Nabhold #77 are candidates, not accepted as source.
- **IAM:** human source and C4 runner preparations merged; protected Kratos/Hydra↔CP B–E and actual approved principals/credentials remain unaccepted.
- **ERP:** #110 proposed, not merged; failed mandatory Gate-D runner executable permission, no PG17 data migration or CDSoftware 13 port proof. Existing ERP-A/B native guarded source does not certify every native operation.
- **Finance:** ADR-SHARED-033 Proposed, F1 DRAFT source exists; certified native Nabhold ledger/finance provider missing.
- **Thamani:** accepted B2B logistics ADR-0018, old B2C storefront deprecated; no native TMS runtime. A B2B2C delivery leg does not convert the seller business to B2C.
- **TMS / SCF:** Foundation-0; TMS only ADR-0001/0002 Accepted; SCF architecture Proposed. No external carrier/financing capability.
- **BXS:** Shared packages and some pinned source/adoption/release evidence, not blanket real-browser/protected consumer quality acceptance.
- **External/regulated:** no signed protected full-chain Nabhold/INT-07 acceptance, current PSP, authentic legal case, national source certification or bank transfer; Gate D/E remain blocked.
- **Tooling:** `equator-estate` still references legacy `nabhold/` paths and baobab-dev image 1.2.6; CMS Node 22 drift; engine-template still contains placeholders.

## 6. Programme topology and governance structure

### 6.1 Maintain EA-01–EA-13 without inventing EA-07/08

Existing EA workstreams retain their identifiers; **EA-INT** is an accepted cross-cutting integration workstream, not a new capability. v2.3 adds **EA-ENG** (ADR-SHARED-041 adoption and quality), **EA-BXS** (ADR-SHARED-040 experience package/consumer qualifications), **EA-PRODUCT** (scoped first-party verticals/strategic product readiness) as *execution lanes only*. They do not create new Engine types, catalogue domains, legal gates, IAM scopes or grant states.

| Workstream | Mandate | Lead authority | Non-negotiable exit |
| --- | --- | --- | --- |
| EA-01 | Canonical contracts/events, actual pinned consumer convergence | Shared + consumers | Accepted semantics, schema compatibility, no shadow domain |
| EA-02 | Capability provider census/activation and per-version support | Shared + CP + owning provider | Exact runtime support, EA-09 receipt, CP binding/denial |
| EA-03 | Engine release/instance topology and lifecycle | CP + Infrastructure | Immutable deployed digest, isolation, health vs authority, failover |
| EA-04 | IAM native/federated/workload trust | IAM + CP + estate | Actual code+PKCE/issuer/audience/revocation/assurance execution |
| EA-05 | Organisation-first admission and legal-actor mandates | CP + official reviewers | Independent legal evidence, no parent/sibling automatic grants |
| EA-06 | Durable events, inbox/outbox, temporal reconciliation | Domain owners + Infrastructure | Real persistent replay, outage and cross-tenant negatives |
| EA-09A | Pre-deployment conformance | Shared, providers, Infrastructure | Relevant frozen L4 real-component profile with mandatory positives/negatives |
| EA-09B | Protected operational certification | Security/Operations/Infrastructure/owners | Actual staging, secrets/identities, legal/vendor approvals, signed gate |
| EA-10 | Traceability/audit/observability | Platform telemetry + providers | Correlation from request to legal decision to durable consequence |
| EA-11 | Backups/recovery/rollback | Infrastructure + each provider | Actual restore/rotation/replay, tested RPO/RTO and data consistency |
| EA-12 | Headless frontend/console/corporate digital estates | CP/estates + Shared BXS | Actual IAM/CP BFF, owned domain, a11y/UX/performance/pinned packages |
| EA-13 | Regulations/official-source/policy boundaries | Regulations + Shared + expert authorities | Source provenance, independent application and no unapproved enforcement |
| **EA-INT** | INT-01..08 L4 shared harness plus protected handoff | Infrastructure orchestration + owners | Scenario-complete receipts at exact pins; separate protected run |
| **EA-ENG** | ENG-01..05 org-wide excellence and provenance | Shared Foundation + every repo owner | Verified local adoption/quality review; no vanity CI-compliance claims |
| **EA-BXS** | BXS/BGX package publishing, adoption, usable journeys | Shared Experience + owning estates | Registry-integrity, exact consumer versions, real-browser/a11y and anti-fabrication |
| **EA-PRODUCT** | TMS logistics, Baobab People, optional SCF and market-fit products | Owning engines and business sponsors | Own domain ADR/contract, proof-of-value, provider support and statutory/legal releases |

### 6.2 Legal, financial and regulatory control planes remain separate

**CP** SHALL not act as a business database, invoice transport bus or regulatory authority. **IAM** SHALL not infer organisational scope from authenticated identity. **Pulse** intelligence signals may highlight changes but cannot unilaterally change payroll, taxes, trade eligibility, transport movement or legal compliance state. **Regulations** may evaluate accepted policy with official-source evidence and governed human-reviewed change, but does not become a court, tax authority or customs official. **Payments** disburses only under legally/provider-authorised money-movement decisions; ERP financial posting is accounting recognition, not a bank instruction. **SCF** may coordinate qualified funders but never self-issues lending permission.

## 7. Preserved programme Gates A–E and separate decisions

| Gate | Scope retained | New v2.3 evidence emphasis | Signoff / restriction |
| --- | --- | --- | --- |
| **A — Architecture/contracts** | Accepted Organisation/LegalActor/market boundaries; actual Shared contract compatibility | ADR-037–041 decisions incorporated and adopted where in scope; Thamani B2B owner ADR corrected; vendor provenance for new products | Shared/CP/owners; accepted ADR ≠ capability |
| **B — Developer / experience unfreeze** | Gate A, no browser shadow authority and truthful separate estates | BXS accessibility/package version evidence and ADR-041 source decision review for significant changes | Estate + platform; no grant or live authorisation |
| **C — Controlled founding admission** | Authentic Org/Tenant/LegalEntity/mandates with scoped documentary deferral | Parent/sibling/external denials, legal source independence, current identity/actor and no-estate readiness | CP/legal/IAM reviewers; founding grace ≠ statutory waiver |
| **D — Per-capability protected qualification** | Passing relevant real-component L4 **before** actual protected staging | Native Trade/ERP financial vetoes; CMS, TMS, People, Regulations and Payments profile-specific tests where services exist | Domain, Security, Infra, CP + external review; synthetic and sandbox ≠ staging |
| **E — Production activation** | Actual issuer, identity, source/certified provider, deployed instance, recovery and signed GO | Statutory country packs, commercial licences, RPO/RTO, consent/retention, support/SLA and operation-specific live evidence | Independent release/ops/legal/provider authorities; per capability/tenant/market/legal actor |

The four independent readiness decisions remain: Organisation admission; Tenant registration/administration; permission for a specific consequential operation; production go-live. PEO-00–07, LA-00–07, one bounded 24-month founding documentary grace and all owner constraints are unchanged. v2.3 SHALL NOT introduce additional physical cluster instances solely because another legal entity is admitted.

## 8. EA-INT — critical real-component integration programme

### 8.1 Source and receipt invariant

Infrastructure owns the **common harness**. IAM, CP, CMS, Trade, ERP, Payments, Pulse, Regulations, TMS, Trade Docs, estates and other providers own **their scenario correctness**. Real-component means the claimed production-shaped component actually executes against an explicitly isolated synthetic client and database, not a mock positive authority function. Every profile must include issuer, signed token audience, CP Principal/Org/Tenant/market, current binding/provider instance, domain PEP, denied sibling/expired/revoked/missing grant, durable consequence, outage/replay and cleanup, as relevant. Frozen source SHA + digest + tests + evidence hash are immutable; a newer commit requires requalification.

### 8.2 Integration priorities and dependencies

| ID | Status at this freeze | Decisive next work | Exit/owner |
| --- | --- | --- | --- |
| INT-01 / L4-00 | Bounded Actions synthetic success; interactive Codespaces session not independently observed | Preserve exact frozen qualification; reproduce in interactive Codespaces, network/security/cleanup | Infra + Security; no staging claim |
| INT-02 / L4-01 | Frozen synthetic real IAM/CP/Pulse Actions PASS, not protected Kratos/Hydra | Requalify changed pins only when selected; keep product clients dormant; separate C4-03 real native profile | IAM/CP/Pulse/Infra; signed exact profile |
| **INT-03 / L4-02** | **NEXT P0 CONNECTED CHAIN; OPEN** | Close Infrastructure #37 and Nabhold #77 only after CI; actual private TLS browser/client/Redis, real IAM issuer, CP current context, CMS provider read/publication, revoke and denied tenant/preview | Nabhold/IAM/CP/CMS/Infra/Security; all NAB-01–04 and mandatory L4 scenario receipts, teardown |
| INT-04 / L4-03 | Blocked on native TMS and scoped Shared contracts | Treat Thamani as **B2B logistics** under ADR-THA-0018; first synthetic bounded transport flow, then qualified TMS/Docs/Regulations/Payments and live actor | Thamani/TMS/CP/IAM; actual provider, not visual prototype |
| INT-05 / L4-04 | Partial site and Commerce integration, no full B2B execution | ZuriBeans authorised buyers/suppliers, corridor compliance, Trade catalogue/quotation/order, ERP/docs/provider trace | ZuriBeans/Trade/ERP/CP/Regulations/Docs |
| INT-06 / L4-05 | Legacy Equator estate; provider scope unproven | Audit legal/property domain and site framework, migrate Foundation/ADR links, add synthetic current tenant/actor/permission fixture | Equator/CP/IAM/ERP; no invented property provider |
| **INT-07 / L4-06** | **Mandatory platform invariant OPEN** | Real unrelated EXTERNAL_CLIENT with zero DigitalEstate, CP+IAM valid product/entitlement, provider invocation and cross-tenant negative | CP/IAM/Infra/selected engine; no fake estate |
| INT-08 / L4-07 | Domain suites separate; unified business mesh incomplete | Native Finance/Trade/ERP/Payments and events; Regulations/Pulse documentary-source advisory; provider outage/retries/reconciliation | Actual APIs, durable states, reviewed negative consequences |

**Do not substitute C4-03 protected Ory/Kratos/Hydra acceptance for the earlier bounded INT-02 proof.** They are distinct. The INT-03 consumer needs a real identity/binding/provider chain in the selected synthetic integration profile; protected staging remains an additional later run.

### 8.3 Exact canonical scenario ownership

The Accepted [EA v2.2 L4 acceptance matrix](ea-v2.2-integration-acceptance-matrix.md) continues to own L4-MAN, L4-IAM, L4-CP, NAB, INT, FIN/EVT and REC scenario identifier meanings. v2.3 supplements them through the [separate admission delta](ea-v2.3-acceptance-and-adoption-matrix.md) with **product engineering receipts** for ENG, BXS, TMS, People and SCF. Do not mint parallel L4 IDs or falsify a not-applicable scenario because a component has not yet been implemented. Real protected run IDs and source receipts SHALL reference exact canonical IDs.

## 9. EA-R02 — real identity, documentary legal actor and controlled admission

Continue in parallel with INT-03:
1. Verify founding-company legal sources, beneficial ownership/control and authority within approved custody and independent reviews, rather than only displaying CIPC reference documents.
2. Establish real CP Organisation/Tenant/PRIMARY relationships, recorded current mandates, status and effective time; keep Nabhold non-trading holding-company boundaries separate from subsidiary operations. A holding company is not a trading seller or automatic employer for other subsidiaries.
3. Prove IAM human/workload registration, assurance/step-up/revocation, current CP context and independent maker/checker for sensitive approvals. Document genuine protection order/identity provenance only where lawfully necessary; do not place personal data in CI fixtures.
4. Close PEO-03K private scanner/custody and PEO-03F official-source transport independently; preserve original LA/PEO gate semantics.
5. Approve external CLIENT admission independent of a website or corporate group relationship; test cross-tenant deny and withdrawal.
6. Keep the first four Organisation cases separate: Nabhold, ZuriBeans, Thamani and Equator only where there is independently verified incorporation/trading-style/legal-role evidence. A documented example is not official verification.

Exit: named authorised officials/signatures and receipts, not a synthetic sample; no protected operation until current legal-actor permissions and provider support actually exist.

## 10. EA-R03 — native execution-point assurance and independent finance

### 10.1 Closed operation-catalogue policy

Accepted Shared ADR-034/037/038/039 and owner ERP/Trade controls govern:
- ERP native posting classification: AD_Client/AD_Org → approved CP Tenant, operating Organisation, Market, actual LegalEntity, role/activity/capability, time-bounded freshness; fail closed before native database COMMIT. A request API permission is **not** an iDempiere posting veto.
- ERP-A purchase order, goods receipt, vendor invoice and other catalogued payables recording require current actor and independent authority.
- ERP-B vendor-payment **recording** requires independently verified actual payment execution evidence; no instruction, approval or transfer originates from ERP. Bank statements, cash journals, physical inventory/costing/manufacturing stay **DENIED** until explicit versioned operation contracts and native proof.
- Trade commercial commitment/order seller operation must resolve CP-owned approved seller operating binding and role/market/legal actor **at every consequential native path**, including admin/workflow/checkout/event replays; carts alone are insufficient.
- Payments exact merchant/PSP eligibility, independent legal and settlement decisions, idempotency, refund/payout/disbursement separation and real D2 provider certification.
- Subscriptions billing/Tax/invoice responsibilities, CP routing authority and finance posting ownership must converge via versioned events and reconciled persistence. CP routes authority; it does not become the invoice bus.
- Trade Docs issuer/legal authority and Regulations requirement/evidence attestation remain separate. No official Customs result is simulated into a live certified release.

### 10.2 Finance F1

Finance F1 DRAFT schemas/source from Shared #319/#321 and ERP-convergence work are **not** accepted ADR-033 completion or live journal read/write certification. Obtain Finance/Shared semantic signoff, actual ledger/chart of accounts/journal balances, current Organisation/LegalEntity and period, secure drill-down, CPA/finance reviewer acceptance and native posting proof. Corporate Nabhold reports must not expose salaries or subsidiary records merely via group ownership. Consolidation and intercompany eliminations require accountant-approved group models and correct `internal-trade` boundaries; never register a parallel finance authority.

### 10.3 Native test and staging exit

For each protected operation, test an authorised positive with persisted effect, wrong tenant/role/legal actor/market/no current grant/refreshed denial, revoked credential, stale lease, duplicate replay, lost callback, multi-step partial rollback and financial reconciliation. Independent PSP, bank, Customs and payroll professional acceptance remain external. Gate D of a product PR can fail for tooling; a runner permission error does not prove runtime compatibility.

## 11. EA-BXS — experience system, UX excellence and browser certification

**Authority:** ADR-SHARED-040. Shared owns `experience-*` neutral packages, semantic tokens, Base UI-backed accessible primitives, optional geo/chart adapters and versioned registry artifacts. Each Digital Estate owns its branded product IA, BFF, personas and live domain workflows.

Mandatory delivery:
1. Publish exact Shared package versions after source CI and verify package integrity, exports, provenance and declared engine/UI peer constraints. A source version is not a published registry artifact.
2. Pin approved versions and lockfile hashes independently in Nabhold, CP Console, ZuriBeans and Thamani; do not infer all consumers migrated from one.
3. Prove real desktop/mobile browser keyboard/focus, screen reader/manual accessibility, loading/errors/withheld/unknown states, responsive layout, meaningful performance budgets, CSP/origin privacy and no credential egress; run visual regression, E2E and no shadow authority.
4. For maps, distinguish editorial provenance from sourced geospatial operational truth. No speculative position/route/carrier timestamp/country market eligibility displayed as live. Optional MapLibre/deck.gl remains client-safe and not a transport engine.
5. Implement role-aware console navigation, Organisation 360, guided workflows and protected sign-in/out as separately governed by CP/IAM; product login and Console login remain distinct authorised journeys.
6. Thamani B2B logistics experiences replace obsolete B2C cart as a *business frontend decision*; real quotes/booking/tracking depend on qualified TMS rather than mock scenarios.
7. Preserve external no-estate API-only service consumption; BXS does not force an application on enterprise customers.

Exit: BXS/BGX source/package/browser/real-provider/staging receipts each independently proven, not a single generic "UI complete" flag.

## 12. EA-ENG — all-repository engineering excellence

**Authority:** Accepted ADR-SHARED-041. All 20 audited first-party repositories and newly created repositories SHALL use the platform principle during material work:
- **ENG-01 inventory:** identify every repository, current Foundation version and runtime/toolchain, accepted vs proposed ADRs, dependency provenance/licence, critical risks and adoption owner; record legacy deviations.
- **ENG-02 local adoption:** each repository acknowledges ADR-041 within appropriate ADR/readme/review guidance. Review material PRs for specific users, established alternatives, adopted/adapted/re-engineered/independently built decisions, source/IP licences, current Shared contracts, comments explaining nontrivial logic and tests. Do not demand empty ADRs for trivial changes.
- **ENG-03 remediation:** prioritise high-risk gaps by production/tenant/security/customer impact; maintain testable drift register, code refactor review and rollback. Target Equator legacy paths and Codespaces image; CMS Node 22; engine-template placeholders; inconsistent PG16/PG17 in ERP.
- **ENG-04 Foundation assurance:** Shared offers nonblocking discovery/reporting, then proposes narrow machine-enforced checks only after exception/migration policy and false-positive validation. No blanket org-enforcement by slogan/string matching.
- **ENG-05 continuous evaluation:** benchmark actual African user journeys, reliability, accessibility, security, interop, legal relevance, operator experience and cost of ownership; maintain contributor/open-source obligations and vendor exit strategies.

**Software quality SHALL include:** maintainable well-commented source for nonobvious invariants/complex calculations, idiomatic standards, reproducible dependencies, current security scanning, observability, positive/negative tests, documented threat model for high-risk domains and enough operational/runbook evidence for future maintainers. Code comments do not replace explicit security contracts or automated tests.

**Developer toolchain:** pin supported `baobab-dev` images and full release digests through Foundation 4; prefer Node 24+ where the accepted frontend/runtime baseline demands; PostgreSQL 17 target where approved, Java 17 for iDempiere 13. Any upgrade requires compatibility and migrations. No silent mass CI dependency bumps to unblock an unrelated feature. Engine-template shall be refreshed before new first-party engine activation.

## 13. EA-PRODUCT — first-party African enterprise capability portfolio

The commercial capability portfolio SHALL grow **behind approved canonical contracts and independent product/tenant authority**, not via proliferation of frontend-specific business logic or premature engines.

### 13.1 Baobab People, inside ERP — BP-00..07 (parallel, conditional)

**Placement:** `baobab-erp` (not a separate engine/repository). **Stage:** ERP #110 candidate unmerged as of baseline. Subject to accepted ERP-local decision after merge, first-party People uses CDSoftware as an inspiration/selectively reusable candidate, not as eternal product definition. May port, refactor, re-engineer or replace third-party plugins within actual licence obligations; never silently fork iDempiere core.

- **BP-00:** close ERP #110 Gate-D CI invocation (Permission denied, exit 126); verify all mandatory checks and code/ADR review; confirm PG17 source defaults, safe operator upgrade guidance. No false PG17 migration claim.
- **BP-01/CD13-01:** capture exact CDSoftware source/manifests/2Pack/dependencies licences/SPDX, provenance, patches, maintainer collaboration, security compatibility and a component-level Adopt/Adapt/Replace/Build Independently register.
- **BP-02–03:** build, start, integrate and exercise *actual* iDempiere 13 + Java 17 + PG17 OSGi/AD/2Pack with native veto and report/UUID/sequence compatibility. Pin immutable upstream/container digest. No runtime pass from wiki version names.
- **BP-04:** Shared-approved workforce/attendance/payroll capability and event census, ERP provider ports, employee privacy, SoD, human approval, balances and atomic accounting; no new namespaces/keys before Shared acceptance.
- **BP-05:** expert-qualified **South Africa** effective-dated taxes/contributions/statutory returns, retroactive rules/golden fixtures, payroll practitioner signoff and parallel run against qualified external provider.
- **BP-06:** independently qualified **Uganda** pack, verified URA/PAYE/NSSF as applicable and local practitioner/authority evidence; no automatic South African portability.
- **BP-07:** multi-legal-entity privacy, tested support/billing/provider posture, exact approved CP binding, operational security, commercial launch and country-specific certification.

Nabhold G07/G08 continue blocked absent real approved provider: **provider-first fallback** protects planned March 2027 payroll, even if first-party product R&D slips. Never treat regulatory-source intelligence as a tax rule engine that can auto-promote AI changes. Actual employee PII and payslips must not appear in broad Pulse reports or generic Finance read models.

### 13.2 TMS and Thamani integrated logistics — TMS-FND / LOG-01..05

TMS ADR-0001/0002 establish Accepted engine role; 0003–0019, TECH-01 are Proposed. First accept reviewed narrow technology/domain/source/schema/authority decisions before writing a pretend logistics provider. Prefer self-hosted, genuinely testable headless runtime and stable Shared contracts, behind current CP/IAM trust.

Sequence: **TMS-FND** runnable runtime, migrations, tenant-context and authority baseline; **LOG-01** canonical shipment/consignment and sourced event lifecycle; **LOG-02** B2B carrier/quote/booking and provenance, consent and cost; **LOG-03** tracking/milestones/POD with time/source accuracy, withdrawal and replay; **LOG-04** Docs/Regulations/trade/ERP/payment composition and isolation; **LOG-05** independent provider/trust/legal/corridor certification and Thamani browser/customer acceptance.

Thamani is **B2B commercial logistics** by Accepted ADR-THA-0018. A last-mile person endpoint is not B2C commerce. Do not call synthetic map demonstration a carrier-certified real movement. Canonical document and Customs authority belongs to Trade Docs/competent officials; TMS owns physical transport execution.

### 13.3 SCF — conditional partner-led financing feasibility

SCF ADR-0001..0035 are Proposed and repo Foundation-0. SCF is not an active banker, funder, finance ledger, lender or disbursement engine. Begin with legal licensing, partner responsibilities, consent, duplicate-receivable/assignment controls, Shared case/evidence contracts and an evidence-backed **Go / Defer / Stop** architecture gate. A synthetic invoice/funder vertical slice may be implemented only after legal/authority scoping; no real financing, loan, account balance, credit recommendation or money movement without separately authorised partners/Payments and proper jurisdictional licensing. SCF is intentionally **not on the founding R0/INT-03 critical path**.

### 13.4 Pulse + Regulations + Trade Docs and African intelligence

Pulse shall scale provenance-backed intelligent research without becoming an enforcement authority. Regulations shall maintain effective-dated legal source provenance, human-reviewed rules and deterministic policy evaluation with independent requirement authority; Trade Docs shall implement real issuer/document state in its own runtime. Regulatory/commercial-market reports are potential Baobab commercial value, but data usage/licensing and local legislation must be proved before sale or downstream authoritative decisions. Integrate Pulse→Regulations knowledge signals→Trade Docs requirement evidence **only across accepted source-owned contracts**, not raw DB joins or speculative AI truth.

### 13.5 ZuriBeans, Finance, commerce and external tenants

ZuriBeans remains B2B cross-border independent legal seller/buyer estate across approved markets. Trade inventory, product, transaction, KYB, RFQ and quotations need authoritative native provider capabilities, country trade requirements, ERP accounting and approved payment/corridor controls; no fabricated market authorisation. External enterprises must consume independently qualified APIs even without any Group estate. Finance F1 and corporate revenue recognition remain ledger/GL work, not a new ungoverned payment engine.

## 14. Production physical architecture and migration controls

The existing approved AWS deployment architecture remains: **af-south-1** is current default region, not every commercial market's home; private independently deployable CP, IAM, API gateway/edge, domain engines and required managed durable stores. Default pooled instances with CP-governed bridged/silo isolation only where approved requirement/proof warrants. Native iDempiere and other stateful workloads require vendor runtime/state compatibility evidence; do not assume every service is safely hosted with Fargate ephemeral storage. No new Tenant triggers automatic CP/IAM duplication.

**PostgreSQL 17** is a platform-target database major for approved services and planned managed RDS. Existing PostgreSQL 16 database *physical volumes* require explicit operator-approved logical backup/restore or tested `pg_upgrade` with old/new binaries and compatible extensions, verified checksums, row/ledger reconciliation, original cluster preservation, runbook and controlled rollback. Do not swap Docker image and mistake it for data migration; no automated volume deletion.

**Staging inputs** (AWS account ID, trusted OIDC plan/apply roles, remote state bucket, secrets/KMS, service endpoints, legal data residency, IAM/CP governance) SHALL be provided by authorised owners and tested. The existing known region alone is insufficient. Exact digest deployment, least-privilege environment and signed run receipts are mandatory before EA-09B / Gate D/E.

## 15. Revised dependency-ordered execution roadmap

**Track P0-A — INT-03 identity/CMS integration (active critical path):**
1. Confirm current source pin/build dependencies and INT-03 negative matrix; inspect open Infrastructure #37 and Nabhold #77 and any new IAM/CP/CMS blockers.
2. Fix tests, explicit IAM→CP validator/client/Principal and private TLS Redis lifecycle; register only permitted **synthetic lab** identity; isolate and verify network; no shadow authority.
3. Prove complete Nabhold code+PKCE, CP current principal/tenancy/mandate, exact CMS PARTIAL provider behaviour, published vs preview, withdrawal, wrong audience, cross-tenant, session revocation, service restart/failure and teardown.
4. Preserve frozen INT-02 receipt and separate protected native C4-03B–E/EA-09B from synthetic INT-03. Update all owners' registers and exact evidence.

**Track P0-B — legal/finance/native safety (parallel):**
1. Continue G01 official evidence/mandates and CP real admission review.
2. Resolve Shared Finance F1 semantic contract and native iDempiere balance/journal access, keeping ADR-033 Proposed until reviewed/accepted.
3. Implement Trade native seller/operation authority and residual ERP denied-by-name families in separately governed classes; verify Payment D2 and Subscriptions billing/execution boundaries.
4. Complete source/real-provider/independent legal/PSP signoff only when available; no P0 source-only substitution.

**Track P0-C — INT-07 external platform invariant:** independent unrelated zero-estate synthetic consumer with actual current IAM↔CP↔provider identity/context/capability and negative isolation. Can reuse INT-02 harness without waiting for Thamani TMS or People.

**Track P1-D — product/experience/engineering convergence (parallel):**
1. ENG-01 repository census & ownership, ENG-02 local adoption and ENG-03 prioritised toolchain/legacy fix.
2. BXS release publication, exact consumer migrations and qualified accessible browser experiences; Thamani scope fix, ZuriBeans B2B, Nabhold executive UX.
3. Narrow TMS Foundation-1 and first sourced B2B logistics provider after accepted owner ADR/contracts; INT-04/05.
4. ERP BP-00 unmerged PR repair and BP-01 source/licence/CDSoftware feasibility; do not force payroll R&D into IAM/CMS critical path.
5. Introduce Trade Docs runtime and qualified Regulations/Pulse domain providers subject to their respective authority/consumption gates.
6. Assess SCF legal/funder feasibility, but do not activate a new finance-engine dependency.

**Track P2-E — protected staging/customer service:** AWS protected account/identity/data/custody/observability actual services, operational recovery and external legal/PSP/statutory/provider certifications for specific components.

**Track P2-F — release/market expansion:** independent Gate D/E production signoffs per legal entity/capability/provider/market, subscription support and commercial/customer agreements; no blanket platform-wide live flag.

Progress SHALL run in parallel where independent. Domain work that is not gated by INT-03 SHOULD NOT wait for it. Any missing current provider or verified actor blocks its *specific* capability, not all safe source engineering.

## 16. Critical-path blocker register

| ID | Severity | Open blocker | Owning next action |
| --- | --- | --- | --- |
| V23-B01 | P0 | Actual connected Nabhold IAM/CP/BFF/CMS INT-03 not proven | Infrastructure #37, Nabhold #77, IAM/CP/CMS real lab and negative receipts |
| V23-B02 | P0 | Protected Kratos/Hydra/C4 and real executive principals/mandates not accepted | IAM/CP/independent identity approvals |
| V23-B03 | P0 | Founding legal/entity/controller/mandate official verification incomplete | CP legal review and approved source/custody |
| V23-B04 | P0 | Payments real PSP D2, Trade native order, ERP denied operation coverage incomplete | Domain PEP owners + Shared operation catalogue |
| V23-B05 | P0 | Qualified CMS/BFF provider consumption and actual publish/preview decisions incomplete | CMS/CP/IAM/Nabhold |
| V23-B06 | P0 | External API-only zero-estate synthetic provider profile unproved | INT-07 owners |
| V23-B07 | P0 | Approved actual AWS staging roles/state/identity/KMS/services and signed Gate D/E absent | Infrastructure + account/release/security/legal owners |
| V23-B08 | P1 | Thamani needs real headless TMS; current Foundation-0 only | TMS foundation + Shared transport contracts + Thamani B2B acceptance |
| V23-B09 | P1 | Finance F1 proposed and no qualified Nabhold native ledger provider | Shared/ERP/Finance reviewer |
| V23-B10 | P1 | Baobab People/PG17 PR #110 unmerged, Gate-D script permissions fail | ERP fix execution mode/CI, vendor audit, safe migration |
| V23-B11 | P1 | BXS exact published artifacts, consumers' browser/a11y/performance tests incomplete | Shared Experience + estate owners |
| V23-B12 | P1 | ADR-041 local adoption incomplete; CMS Node 22, Equator legacy `nabhold/` and engine-template placeholders | ENG owners/Foundation/Dev tooling |
| V23-B13 | P1 | Real Trade Docs service absent; Regulations PARTIAL; Pulse only bounded provider | Trade Docs, Regulations, Pulse owners |
| V23-B14 | P2 | SCF-only proposed charter and no licensed financing partners | SCF owner and legal/commercial authority; defer |
| V23-B15 | P1 | Readiness dashboard historical assertions inconsistent across dates | Shared EA owner; immutable v2.3 source receipt, current header and history pointer |

Open blockers SHALL be maintained in the live dashboard with exact owner/date/next PR/evidence. Severity can change with demonstrated dependency and customer priority; never silently mark resolved on design intent.

## 17. Financial, statutory, operational and country-specific evidence

- Payroll ZA/UG: official-source, independent practitioner validated packs, historical rule version, EMP/other filing evidence relevant to employer, line-by-line calculation and maker/checker; payslip confidentiality; payroll approval does not authorise Payments disbursement.
- Accounting and cross-border commerce: official legal actor and independently approved seller/merchant registration, ownership/currency/market context, native accounting controls, statutory tax and Customs authority; derived estimates cannot post as certified invoices.
- Logistics: sourced physical events, actual carrier/provider credential, SLA, customer consents, document acceptance, ETA uncertainty and cross-border compliance; geographic presentation not a tracking authority.
- Finance and SCF: no funder consent/credit score/lending authority implied by data availability; partner-led financing requires signed contracts, jurisdiction-specific licensing and anti-double-financing controls.
- Statutory rule generation: Regulations/Pulse may research/flag official changes; expert approval and deterministic regression before production rule promotion.
- Data and secrets: lawful and scoped access, independent residency, privacy classification, encryption, retention, breach and audit; test with synthetic fixtures only; never commit legal documents/payslips/credentials.
- Operations: defined RPO/RTO, recoverable keys and clusters, signed images, release/rollback, metric evidence, service ownership/support/SLO and incident response.

No source-only report may certify commercial production readiness.

## 18. Assurance, maintainability and Definition of Done

Any gate-moving change SHALL provide:
1. **Authority:** links to active accepted ADR/Shared contract, identified owner, role/activity/capability/market/legal actor and intended evidence classification.
2. **Alternatives:** significant reuse/refactor choice under ADR-041, exact third-party source/attribution/SPDX/lifecycle, verified current toolchain and migration/upgrade compatibility.
3. **Quality:** well-structured tested code, explanatory comments for nonobvious business/security/statutory decisions, negative/failure tests, reliable error mapping, permission boundaries, idempotency, observability and runbook.
4. **Source:** immutable commit/PR head, contract lock, OCI artifact digest, current migration version and exact dependent engine source pins.
5. **CI:** mandatory completed green workflows, code-owner/security review where applicable, dependency and vulnerability checks; no pending/failing check masked by aggregate green. CI flakiness corrected rather than bypassed.
6. **Integration:** genuine required real-component profile with exact positive/negative scenarios, source/issuer/client/DB, provenance receipt, clean shutdown and evidence custody.
7. **Protected and external:** if a real capability, current independent source/PSP/tax/carrier/legal approvals, actual protected AWS deployed account/services, telemetry/recovery and designated signed GO.
8. **Rollout:** backward/forward compatibility, canary/progressive rollout, contract migration, consumer pin update, destructive-change review and tested rollback.
9. **Register:** update live dashboard and programme/domain owner registers with proof, remaining blockers and accountable next action.

**A passing README test, green unit suite, encrypted secret template, correct auth URL, published npm package, mock carrier, test payslip or PG17 Docker tag is not by itself operational qualification.**

## 19. Staging, production and release governance

**EA-09A** requires source/component-level mandatory L4 profiles for the exact candidate. **EA-09B** requires independently witnessed protected staging for the legally authorised provider/tenant/market operation. **Gate E** adds independent real-person/legal/PSP/provider/statutory/operational signoff and a release observation matching the tested image digest. A provider is ACTIVE only by CP-owned approved lifecycle/binding/grant at the verified current EngineInstance; no engine self-promotes from CI.

Default infrastructure AWS region **af-south-1** is not a blanket assertion about data residency in Uganda, Kenya or future markets. New regional cells, additional active CP writers, hardcoded country identity, external fund transfers or cross-border employee data require accepted owner policy and legal review.

## 20. Programme dashboard, issue routing and change control

- `docs/architecture/ea-dashboard.md` is the live operational programme register; it starts with v2.3 authority and current snapshot, then dated appendices preserve history.
- `docs/architecture/ea-v2.3-cross-repository-evidence-audit-2026-10-20.md` is the immutable source/ADR/status audit at plan inception.
- `docs/architecture/ea-v2.3-acceptance-and-adoption-matrix.md` is the new **non-L4** product/engineering adoption evidence inventory. The original v2.2 matrix remains the authoritative **L4 scenario ID registry**, subject to separately Accepted Shared revisions.
- `docs/adr/README.md` and root Shared `README.md` must link this Accepted plan, mark v2.2 historical for execution and retain substantive controls.
- PRs introducing/closing a workstream SHALL update the dashboard and any affected Nabhold/domain/engagement register. A frozen snapshot need not be rewritten for every progress update; source revisions remain addressable by Git SHA.
- Any new legal/accounting identity authority, provider semantic, capability namespace, open-banking right or production deployment design needs its *own owning Accepted ADR and contract migration*. v2.3 cannot silently confer it.
- **No unbounded cross-repo blocking upgrade:** Shared centrally publishes paved roads; each repo migrates/rebases through its own mandatory tests and gate; failures are visible.
- Owner-approved exception records identify the exact invariant, reason, scope, expiry and independent approver; privacy/finance/legal and hard security vetoes are never exceptionable merely for a deadline.

## 21. Acceptance criteria and declared next authorised actions

The **v2.3 programme plan itself** is adopted when this plan, the dated audit, companion acceptance delta, refreshed dashboard, Shared ADR register/README and CI governance checks are reviewed and merged. This action is **ENG/EA-R00 programme governance only**; it is not a pass on the downstream milestones.

First engineering closure priorities after the baseline:
1. **INT-03** real connected private lab chain and closed negative cases, with independent CMS/provider and exact source receipt; resolve Infra #37 and Nabhold #77 on their own merits.
2. **EA-R02/R03** authentic legal/mandate and native Trade/ERP/Payments/Subscriptions/Docs financial/operation guards in parallel.
3. **INT-07** unrelated EXTERNAL_CLIENT zero-estate real-component synthetic integration.
4. **ENG-01/02**, and **BXS** package/browser consumer acceptance; lift CMS/Equator/template toolchain drift according to impact.
5. **Baobab People BP-00** resolve ERP #110 mandatory Gate-D failure, then CDSoftware licence/source inspection and iDempiere 13/PG17 technical proving; no premature country payroll.
6. **TMS first execution slice** for Accepted Thamani B2B logistics; preserve SCF as conditional; progress other INT profiles as providers mature.
7. **Protected staging, real statutory/provider certification, signed production** only as every distinct authority gate genuinely passes.

The Platform Owner's strategic expectation is exacting: **learn from the best, build the software African enterprises actually need, and demonstrate that it matches or exceeds the best through reproducible evidence.** We shall not trade legal truth, enterprise privacy, technical reliability, independent authorities, maintainability or reproducible acceptance for faster status declarations.

---

**Approval record:** Accepted on 20 October 2026 by the Platform Owner's explicit direction to revise and adopt EA v2.3; the GitHub PR merge is the repository publication and CI-conformance event. The source audit is dated, not a claim of real-time current operation. No downstream capability is activated by this document.


## 23 October 2026 — accepted development provisioning amendment

[ADR-SHARED-043](../adr/ADR-SHARED-043-Development-Provisioning-and-Environment-Approval-Boundaries.md)
governs development provisioning across all engines and estates. Disposable
synthetic integration has standing authorisation and a CP-owned bootstrap;
independent human approvals apply when readying protected staging/production,
not before normal development runs. Distinct synthetic maker/checker identities
may be automated by one operator; runtime authorization mechanisms remain tested.
Development runtime PASS is separate from protected acceptance. Missing engine
implementations remain explicit blockers. This amendment supersedes earlier
INT-03C/#354/#49 development execution holds; it does not retroactively promote
historical receipts or activate production workloads.


### EA-DEV delivery companion — proposed 23 October 2026

The [EA-DEV implementation plan](ea-v2.3-development-enablement-implementation-plan-2026-10-23.md) proposes dependency-ordered implementation packages DEV-00..DEV-13 and measurable developer-experience acceptance. It operationalises already-Accepted ADR-SHARED-043 without modifying protected human/security/legal approval requirements or historic audit baselines. Its execution schedule is **proposed pending Shared review, CI and merge**; no source, runtime or stage result follows from publication.
