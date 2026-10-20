# ADR-SHARED-041 — Baobab Platform Engineering Philosophy and African Enterprise Product Excellence

**Status:** Accepted — Normative Organisation-Wide Engineering Governance
**Decision date:** 2026-10-20
**Decision authority:** Baobab Platform Owner
**Authority home:** `baobab-platform/shared/docs/adr`
**Scope:** Every first-party repository and technical product maintained under `baobab-platform`, **including all current and future `baobab-*` repositories**, Shared itself, Infrastructure, and first-party corporate/Digital Estate repositories such as Nabhold, ZuriBeans, Thamani and Equator & Estate Co. The rule applies to platform engines, modules, APIs, user experiences, private packages, source dependencies, DevEx/CI, infrastructure-as-code and customer-facing services. Independently owned third-party or external-tenant repositories are governed only through an express contract or voluntary adoption.
**Related decisions:** ADR-0001–0005; ADR-SHARED-007/017/021/032/036/040; ADR-0020 Capability-driven Foundation CI; applicable accepted engine/estate ADRs; ADR-ERP-004 and ERP-local Baobab People ADR-ERP-023.
**Implementation state:** Normative decision adopted at platform level; individual repository adoption, implementation checks, releases and protected production evidence must be demonstrated separately.

## 1. Governing principle (verbatim)

> **Learn from established products. Reuse what is proven. Question what is inadequate. Re-engineer what must improve. Build what Africa needs.**

This statement is a **mandatory platform engineering and product-design principle**, not a Baobab People-only slogan, an optional style preference or permission to copy others' intellectual property. It expresses a standing responsibility to build outstanding enterprise products and capabilities for African organisations while maintaining globally competitive engineering quality, interoperability and integrity.

The aspiration to be the best platform for African enterprises is a **direction and measurable quality ambition**, not a current certification, ranking or marketing claim. Each product SHALL prove its fitness for actual users, employing/legal entities, operating markets and sectors by evidence.

## 2. Decision

All first-party Baobab projects and materially changed code SHALL use a disciplined **learn → assess → adopt/adapt/re-engineer/build → prove → operate → improve** lifecycle:

1. **Learn.** Research credible existing standards, open-source projects, commercial products, user workflows, local market needs and relevant platform capabilities before unnecessarily designing a new solution. Record material sources and the problem being solved; never let competitor design alone become the requirements specification.
2. **Reuse what is proven.** Prefer supported Shared packages, canonical contracts, reusable Foundation workflows, established security patterns and correctly licensed components when they meet the requirement, with evidence of maintainability, security, scale, accessibility and compatibility. Reuse SHALL NOT bypass authoritative boundaries or introduce unreviewed dependencies.
3. **Question what is inadequate.** Challenge business-model assumptions, poor user experience, unsupported jurisdictions, brittle architecture, opaque vendor lock-in, unsafe defaults, duplicated ownership, old dependencies and weak operational controls. Differentiate demonstrated issues from hypotheses.
4. **Re-engineer what must improve.** Refactor, replace, port, redesign or rebuild components when evidence demonstrates that an inherited design cannot satisfy accepted contracts, African localisation, security, performance, reliability, maintainability, licence or product requirements. Porting for compatibility does not require preserving the source application's historical product intent. Record migration, rollback, evidence and ownership.
5. **Build what Africa needs.** Develop original first-party capabilities where existing solutions are unsuitable, incomplete, too costly, legally incompatible or operationally fragile. Support legal-entity autonomy, multiple African jurisdictions and currencies, local constraints and digital inclusion without hardcoding the continent as one legal regime. Make the result interoperable and globally competitive.
6. **Prove and operate.** Require reviewed engineering quality, readable code and explanatory comments where appropriate, reproducible tests, supported versions, observability, backups, secure supply chain, user acceptance and operational accountability. Independently validate statutory, financial and safety-critical behaviour before production.
7. **Improve deliberately.** Collect product and reliability evidence, simplify what no longer serves users, contribute appropriate generic fixes upstream, and continually reassess whether each dependency should be retained, adapted or retired.

For material new features, significant rewrites, vendor/plugin adoption, localisation packages, API contracts and complex migrations, the engineering review SHALL document a decision among **Adopt, Adapt, Re-engineer/Replace, and Build Independently**, with a rationale. Low-risk maintenance and trivial bug fixes SHOULD use proportionate documentation instead of performative design paperwork.

## 3. Scope, adoption and relationship to existing architecture

This ADR is binding on:
- `shared`, `infrastructure`, `baobab-cp`, `baobab-iam`, `baobab-erp`, `baobab-trade`, `baobab-cms`, `baobab-pulse`, `baobab-regulations`, `baobab-trade-docs`, `baobab-payments`, `baobab-subscriptions`, and **every other existing or future first-party `baobab-*` repository**, insofar as those repositories exist and are operated by the group;
- first-party non-prefixed product repositories such as Nabhold, ZuriBeans, Thamani, and additional Group Digital Estates;
- platform engineering tools, automation, shared packages, APIs, schemas, SDKs, migrations, data pipelines, reporting and future first-party commercial offerings.

The named repository examples are **illustrative, not an assertion that each is currently accessible, active or compliant**. Globally applicable decisions SHALL be published in Shared; repository-local ADRs SHALL describe domain-specific implementations and shall link to this decision during adoption. The absence of a local acknowledgement does not cancel the normative scope.

This decision **does not supersede** accepted authority, tenancy, contracts, IAM, segregation-of-duties, legal-actor, localisation, finance, evidence, privacy, accessibility, release, or production-certification controls. In particular:
- Shared owns canonical contract meaning, capability registration and common engineering standards.
- Control Plane owns tenant/organisation context, governed bindings, grants and release/activation authority.
- IAM owns identity and credential/session/token trust; engine providers own implementation within their approved boundaries.
- Individual legal entities and independent tenants remain isolated. African market applicability never implies shared payroll, finance, customer or personal-data access.
- Regulations may curate authoritative regulatory-source evidence, and Pulse may provide advisory intelligence; neither may silently publish operational rules or determine legal/financial facts without explicit authority and review.
- Foundation, security, CI and production/staging readiness gates continue to apply. **Accepted ADR != merged code != passing CI != live integration != production approval.**

Where an accepted ADR appears to conflict with implementation of this philosophy, teams SHALL raise a scoped architecture clarification rather than weakening the existing control in code.

## 4. Operational decision framework

Every nontrivial adoption/re-engineering decision SHOULD include the following durable evidence, placed in the owning repository's issue, ADR, PR description or component register rather than a new universal database:

| Dimension | Question / required consideration |
| --- | --- |
| Problem and users | Which African enterprise user, legal employer, digital estate or platform capability needs this? What outcome is measured? |
| Existing options | What open-source, commercial, Baobab Shared and native engine solutions were evaluated? With what sources/revisions? |
| Decision | Adopt, Adapt, Re-engineer/Replace, Build Independently — or a justified mixture per component |
| Authority and contracts | Which accepted ADRs, Shared capabilities, tenant/legal-entity controls and event semantics govern it? |
| Localisation | Which specific jurisdictions, effective dates, currencies, laws, languages, accessibility and network constraints apply? |
| Licence and IP | SPDX/provenance, contributor notices, distribution/source obligations, trademarks, attribution, vendor collaboration and independent-code boundaries |
| Compatibility | Pinned platform/tool versions, supported interfaces, dependency/OSGi/package constraints, upgrade path and security advisories |
| Quality | Tests, business-rule fixtures, performance and failure budgets, privacy/security negatives, source comments, maintainability and review |
| Deployment | Backward compatibility, staged migration, backup/rollback, observability, support model and actual acceptance receipts |
| Exit criteria | Conditions for retaining, upstreaming, replacing or retiring a dependency and the accountable reviewer |

**Not all work requires a large ADR:** use proportionality. Record deeper evidence when changes touch money, identity, personal data, statutory compliance, tenant isolation, external dependency modification, data migrations or high-impact business operations. An unverified assumption SHALL be marked unknown, not promoted to implemented or compliant.

### 4.1 Product and experience bar

- Design **for African enterprises first**, but do not assume one continent-wide business law, one currency, constant connectivity, one official language or one type of employer/customer.
- Use explicit current jurisdiction and local expert validation for payroll, tax, privacy, import/export, payments, statutory filings and regulated industries. No unreviewed AI-generated regulatory configuration may be activated.
- Aim to meet or exceed relevant high-quality global enterprise offerings in measurable task success, accessibility, perceived responsiveness, actual performance, operational reliability, coherent information architecture and supportability. Benchmark representative workflows; do not invent rankings.
- Build headless, provider-neutral, composable contracts and product-appropriate digital experiences without pushing ownership into a frontend or duplicating a platform engine's authority.
- Treat enterprise requirements such as delegated access, approval auditability, data export, localisation, records custody, reconciliation and system interoperability as design foundations rather than late additions.
- Preserve domain autonomy and provider optionality; avoid unnecessary new engines, repos or platform-level abstractions unless justified by ownership and operational proof.

### 4.2 Maintainability and software excellence

- Production implementations SHALL be readable, modular, appropriately commented (especially nonobvious invariants, authority gates, failure handling, mathematical/statutory rules and migration decisions), type-checked where available and meaningfully tested. Comments SHALL explain **why** rather than restate trivial **what**; no cargo-cult boilerplate.
- Follow current approved technology baselines and reproducible lockfile/image/toolchain policies, with explicit version compatibility and dependency licences. Do not set a universal version number here: approved runtime standards and engine-specific compatibility matrices govern actual pins.
- Include error semantics, idempotency, audit traces, resilience under provider failure, principle of least privilege, security and privacy threat modeling proportionate to risk.
- Test positive paths, denial/negative paths, cross-tenant isolation, retries, migration/rollback and failure/recovery paths when applicable. Passing unit tests alone SHALL NOT be described as real-service production acceptance.
- Refactor while preserving canonical contracts unless a properly governed Shared contract/version migration has been accepted.
- Do not hide technical debt behind optimistic status words. Track known gaps with owner, consequence and acceptance criterion.

## 5. Third-party software, modification and intellectual property

Using outside implementations as inspiration and selectively refactoring their code are different legal and engineering acts. This ADR SHALL NOT be construed as a right to copy or relicense somebody else's original work.

1. Before shipping reused/modified source, inspect the actual repository licence and dependency tree, not merely a wiki or marketplace label; record the source revision, source author, contribution notices, SPDX identifiers, build artifact/digest, patches, distribution model and required attributions.
2. Comply with all relevant copyleft/proprietary obligations. A modified GPL component remains subject to its applicable licence; neither a large refactor nor a rename automatically makes it independently owned or proprietary. Where the business needs distinct licensing, seek qualified counsel and a legitimate licence or a defensible independently authored replacement.
3. Avoid long-lived forks of upstream cores where accepted extension ADRs prohibit them (e.g. iDempiere under ERP ADR-004). A governed third-party **plugin port** is different from a forbidden **core fork**, but it still needs provenance and release maintenance.
4. Vendor outreach, sponsorship, collaboration, upstream PRs, support subscriptions and respectful public attribution are encouraged when useful. Vendor permission beyond an existing licence must be documented, not inferred from an email or an expression of goodwill.
5. Independently developed Baobab product domain models, approved localisations, original source, experience design and services form Baobab's own product/IP strategy, to the extent permitted by source licences and applicable law. No claim is made over upstream code, trademarks, design rights or unrelated external intellectual property.
6. Monitor security, compatibility, maintenance, economics and support risk. Refactor or replace unsuitable dependencies based on recorded engineering evidence, not obligation to mirror a competitor indefinitely.

**Example — Baobab People:** CDSoftware HR/Payroll may inspire the design or supply legally reusable components, but `baobab-erp` owns its People domain implementation, may re-engineer or independently develop substantially different features, and must separately prove iDempiere 13 compatibility and South African/Ugandan localisation. That ERP-local decision does not change Shared's control of canonical contracts or separate payroll certification.

## 6. Engineering review and assurance

Every material design/PR review SHALL explicitly consider:
- **Fitness:** who benefits, what is demonstrably improved for the relevant African market or enterprise user, and whether a simpler proven solution exists;
- **Reuse decision:** what is adopted, adapted, fundamentally re-engineered or built independently and why; alternatives evaluated;
- **Architecture:** authority/tenancy/canonical-contract compliance, provider neutrality and full lifecycle constraints;
- **Trust:** licence/source provenance, security, privacy, supply chain, audit and statutory approval obligations;
- **Evidence:** code quality, tests, meaningful source commentary, measured functional/nonfunctional outcomes, compatibility and operational acceptance;
- **Reversibility:** deployment, migration, rollback, upstream upgrade and vendor exit plan.

A linkable, minimal review checklist is maintained in `docs/governance/engineering-philosophy-review.md`. Repositories MAY reference it in PR templates; platform governance SHOULD introduce nonblocking conformance discovery before considering mandatory central automated checks. **Do not fail existing repositories merely for lack of this new reference until a reviewed migration and Foundation rollout plan has been completed.** Existing code is not retroactively claimed noncompliant because it predates this ADR; substantively changed areas SHALL adopt it now, and important historical gaps SHALL be inventoried and prioritised.

Evidence classes (explicit):
1. Normative acceptance (this ADR);
2. Repo-level acknowledgement / engineering decision;
3. Implementation in source and tests;
4. CI/static conformance;
5. Real-component integration and qualification;
6. Protected staging, external regulatory or security signoff where required;
7. Independently authorised production operation.

No promotion to a higher class is inferred from a lower class.

## 7. Adoption sequence and accountable owners

| Phase | Owner | Deliverable | Acceptance |
| --- | --- | --- | --- |
| ENG-00 — Normative | Shared / Platform Owner | Accepted ADR-041, Shared ADR index, root README, reusable checklist and automated docs integrity test | Reviewed PR, mandatory CI green, merged to Shared main |
| ENG-01 — Inventory | Platform Engineering | Discover first-party engine, `baobab-*`, Corporate/Digital Estate and tooling repos; baseline existing decisions and gaps | Dated inventory distinguishing readable, unreadable, in-progress and adopted |
| ENG-02 — Local adoption | Each repo's owner | Link ADR-041 in appropriate engineering governance; update review templates/decision logs where useful | PR merged with required CI; no existing authority bypass |
| ENG-03 — Focused improvements | Domain/product owners | Prioritised refactor/re-engineering plans based on user impact and risk, not blanket rewrites | Measurable acceptance targets and secure incremental changes |
| ENG-04 — Org assurance | Shared Foundation owners | Evaluate optional automated metadata/reporting and a staged upgrade to policy checks | No false negatives, evidenced coverage, approved migration and separate rollout |
| ENG-05 — Continuous | All engineering owners | Regular product/dependency/localisation/quality review | Published source/CI/real-component evidence and tracked exceptions |

All rows beyond ENG-00 are execution work, not effects automatically completed by accepting an ADR. Each repo remains responsible for local testing, adoption and delivery. This ADR sets the minimum philosophy and review intent, not a new provider, capability domain, subscription, licence, deployment authority or production certification.

## 8. Alternatives and consequences

**Only Baobab People adopts the motto — rejected.** That would leave inconsistent platform engineering philosophy and separate operating cultures for every engine.

**Copy commercial or open-source systems wholesale — rejected.** This creates licence, security, product differentiation, maintenance and African localisation risk.

**Always reuse an existing library — rejected.** Unsupported or mismatched dependencies can cost more than a principled replacement.

**Always rebuild from scratch — rejected.** Duplicates proven innovation and increases risk, cost and time to market.

**Mandate all legacy repos rewrite immediately — rejected.** Disruptive, untestable and indifferent to risk. New/changed work adopts now; legacy cleanup is governed by evidence and priority.

**Turn the motto into an unreviewed central CI block — rejected.** A phrase cannot substitute for correct architecture or evidence; any future machine-enforced policy must be narrow, reproducible, proportionate, separately approved and safely rolled out.

Expected benefits: first-party African enterprise product leadership, responsible reuse, interoperability, maintainability, legally defensible IP provenance and a consistent engineering standard across Baobab.

Expected costs: explicit product discovery, ongoing dependency/standards reviews, independent statutory expertise, better test and evidence investment, migration plans and cultural adoption. These costs are part of enterprise-grade engineering, not a reason to relax quality gates.

## 9. References and amendments

- Shared ADR register: `docs/adr/README.md`
- Shared platform engineering governance: `docs/governance/engineering-philosophy-review.md`
- Existing Foundation contract: `docs/architecture/decisions/ADR-0020-capability-driven-foundation-ci.md`
- Existing experience contract: `docs/adr/ADR-SHARED-040 — Baobab Experience System, Frontend Engineering and Geospatial Presentation.md`
- ERP extension/core-fork prohibition: `baobab-platform/baobab-erp/docs/adr/ADR-ERP-004 — Baobab iDempiere Extension Architecture.md`
- ERP People interpretation: `baobab-platform/baobab-erp/docs/adr/ADR-ERP-023 — Baobab People African Workforce, Payroll, CDSoftware Re-engineering and PostgreSQL 17.md`

**Amendment rule:** Future exceptions or scope changes require an Accepted Shared-level amendment. An engine-level ADR may refine how this philosophy is implemented but SHALL NOT silently override its scope or loosen existing platform security, contractual and production controls.
