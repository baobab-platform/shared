# Baobab Platform — engineering philosophy and adoption review

**Normative source:** [ADR-SHARED-041](../adr/ADR-SHARED-041%20%E2%80%94%20Baobab%20Platform%20Engineering%20Philosophy%20and%20African%20Enterprise%20Product%20Excellence.md) (Accepted, 2026-10-20).
**Audience:** maintainers, authors and reviewers of every first-party `baobab-*` repository and every other first-party Baobab Platform or Nabhold Group estate.
**Scope:** Material new features, design choices, third-party imports/ports, major refactors, country localisation, sensitive data, contract changes and migrations. For routine small maintenance, answer only applicable items; do not generate an ADR for every code edit.

> Learn from established products. Reuse what is proven. Question what is inadequate. Re-engineer what must improve. Build what Africa needs.

## Material-change review checklist

A reviewer can link this page from a GitHub PR, issue or local ADR. Check applicable items, and explain any deliberately not-applicable items. Do not check a gate as complete without evidence.

- [ ] **Problem and user:** Identify the specific enterprise workflow or platform gap, affected African jurisdiction(s) where relevant, measurable desired improvement and constraints. Name unknowns rather than guessing.
- [ ] **Learn:** Compare at least the credible native Baobab/Shared option and relevant available external solutions; cite exact documentation, versions or source revision for nontrivial choices.
- [ ] **Reuse decision:** Declare `Adopt`, `Adapt`, `Re-engineer/Replace`, `Build Independently`, or a component-level combination. Explain why, cost/risk and expected improvement.
- [ ] **Authority:** Identify applicable accepted Shared/engine ADRs and confirm no change to tenant/legal entity, IAM, CP, regulatory, payment, ERP, event or contract ownership without approved decisions.
- [ ] **Compatibility:** Pin/review major dependency versions and source/image digests as appropriate; capture upstream API, database, operational and security compatibility. Assess a viable provider exit/rollback.
- [ ] **Licence/IP:** Review actual source and transitive licences, attribution, copyright, modification/distribution obligations and ownership of original work. Do not assert a modified upstream file has become proprietary merely through refactoring.
- [ ] **African fit:** Validate specific tax/legal/regulatory/jurisdiction, market, currency, language, accessibility, infrastructure and employer/customer constraints **when applicable**, with qualified evidence. Do not assume one African law or tax regime.
- [ ] **Security/privacy:** Identify sensitive data flows, least privilege, tenancy boundaries, denial/cross-tenant tests, security scans and relevant records/residency controls.
- [ ] **Implementation quality:** Clean architecture, maintainable structure, explanatory source comments for nonobvious behaviour, tests and representative failure/retry/rollback paths; performance/availability/user outcomes where relevant.
- [ ] **Verification:** Distinguish reviewed design, committed code, CI results, integrated services, independent regulatory/security certification and protected staging/production acceptance.
- [ ] **Decision and ownership:** Record owner, alternatives, open limitations, accepted risks, upgrade path, retirement criteria and follow-up tasks.

## Decision record: minimal example

```text
Work item / repository / owner:
User or enterprise problem:
Applicable accepted ADRs:
Country/jurisdiction and legal-employer scope (or N/A):
Existing alternatives reviewed (with source/version):
Decision for each component: Adopt | Adapt | Re-engineer/Replace | Build Independently
Reason, trade-offs, IP/licence/provenance:
Canonical contract / CP / IAM / engine ownership:
Definition of done (tests, security, user and statutory evidence):
Migration/rollback and support:
Open gaps / follow-up issues / independent certification:
```

## Practical interpretation

- An existing component does **not** earn permanent adoption merely because it currently compiles; judge its ongoing security, maintainability, quality and local business fit.
- A major rewrite does **not** automatically become an independent original work if it was derived from upstream licensed code.
- A product does **not** require the same user experience or internal object model as the software that inspired it.
- Where Baobab already provides a proven Shared capability, do not fork its semantics or maintain competing contracts in consumer repositories.
- A prototype, synthetic payroll run, green CI or merged PR does **not** establish statutory legality, tenant-safe live integration or production approval.

## Rollout status and follow-up

**Decision accepted in Shared is distinct from local adoption.** The objective is for every first-party repository to reference the Shared decision within its existing engineering governance and to apply it during material changes. Existing repo owners should inventory adoption status and record review evidence incrementally; do not rewrite every historical file or introduce a brittle org-wide CI block merely to add a sentence.

The Shared team owns the canonical text and governance changes. Each repo owner owns its local decision records, code reviews, testing, releases and independent sign-offs. If future machine enforcement is needed, it must follow the staged Foundation rollout and include coverage of private repositories, false-positive testing, exception handling and an Accepted governance amendment.
