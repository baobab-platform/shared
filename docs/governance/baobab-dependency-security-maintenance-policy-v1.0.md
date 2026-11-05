# Baobab Dependency & Security Maintenance Policy v1.0

**Policy ID:** BA-SEC-DEP-001  
**Version:** 1.0  
**Date:** 5 November 2026  
**Status:** PROPOSED — submitted through [Shared PR #429](https://github.com/baobab-platform/shared/pull/429); effective only after accepted review and merge  
**Custodian:** Baobab Platform Engineering (`@baobab-platform/platform-engineering`)  
**Security approval authority:** Baobab Security (`@baobab-platform/security`), subject to applicable CODEOWNERS and accepted governance  
**Scope:** All first-party `baobab-platform` repositories, including engines, digital estates, Shared, Infrastructure, tooling and templates  
**Review:** Quarterly and following material vulnerability, supplier compromise or technology migration

> **Authority boundary:** This policy governs maintenance and vulnerability assurance. It neither supersedes accepted EA/ADRs and owner-native decisions nor grants IAM/CP rights, staging/production approval, statutory/provider authority or financial execution rights. A security scan, Dependabot PR or source merge does not constitute protected acceptance.

## 1. Purpose and normative interpretation

Baobab is a multi-repository, polyglot enterprise platform. A defect in a direct or transitive dependency, reusable workflow or centrally published toolchain can propagate from one source repository to multiple customer and enterprise runtimes. Maintenance MUST be risk-prioritised, auditable, reproducible and coordinated without destroying independent repository ownership.

This policy establishes a common method to: identify and inventory dependencies; maintain compatible versions; triage and patch known vulnerabilities; test security and business consequences; protect CI/CD and private registries; apply independently approved exceptions; publish evidence and metrics; and prove affected consumers have received a fix.

**MUST/SHALL** means mandatory on accepted adoption, **SHOULD** means expected unless a documented justification is approved, and **MAY** is optional. During this proposal's review the language expresses intended policy, not a claim that all 20 repositories already comply.

## 2. Precedence, sources and coverage

Accepted enterprise architecture, security decisions, domain-owner authority and environment-specific release rules take precedence over this policy. It must be read with:

- [Shared SECURITY.md](../../SECURITY.md), governing private disclosure, immutable Actions, privileged workflows, secrets and incident response;
- [Foundation CI support policy](foundation-ci-support-policy.md) and [branch protection](foundation-4-branch-protection.md);
- the [Shared Dependabot template](../../templates/dependabot.yml), [configuration validator](../../.github/workflows/enforce-dependabot-config.yml) and [action-pinning validator](../../.github/workflows/enforce-action-pinning.yml);
- the existing [Foundation security workflow](../../.github/workflows/reusable-foundation-security.yml), [native dependency adapters](../../.github/workflows/reusable-foundation-dependency-adapters.yml), and [dependency review](../../.github/workflows/reusable-foundation-dependency-review.yml);
- [EA v2.3](../architecture/EA-implementation-plan-v2.3-2026-10-20.md), [EA adoption matrix](../architecture/ea-v2.3-acceptance-and-adoption-matrix.md), and accepted ADR-SHARED-041.

This policy covers GitHub Actions and reusable workflows; first- and third-party packages; direct, transitive and vendored dependencies; lockfiles, private registries and generated clients; build tools, compiler/runtime and CLI versions; Docker/OCI images, OS packages and development containers; applicable IaC providers/modules; and produced artifacts and their downstream consumers.

No repository should claim Dependabot coverage for an unsupported ecosystem. A central source of truth such as `baobab-dev`'s toolchain lock remains authoritative where appropriate, provided there is an observable, independently tested security maintenance process.

## 3. Mandatory security principles

1. **Security patch precedence:** a relevant critical advisory is not postponed until the next weekly version-update run.
2. **Immutable dependencies:** external GitHub Actions and cross-repository reusable workflows MUST use verified 40-character commit SHAs; Docker-backed Actions require verified image digests. OCI artifacts SHOULD use immutable digests wherever compatible with the approved deployment model. Never fabricate a SHA or assume an arbitrary digest is trusted.
3. **Single version authority:** manifests, lockfiles, centrally governed toolchains and image authorities must not be updated by competing systems.
4. **Fail visible, not falsely green:** absent scans, inaccessible registries, unavailable entitlements, skipped jobs and unsuccessful workflows are not passing security evidence.
5. **Least privilege:** update bots, CI tokens, publishing credentials and external downloaders have only the rights needed; secrets never flow to untrusted fork PRs.
6. **Business consequences:** package compatibility must be demonstrated for real owner-native operations where relevant; compilation is not enough for IAM, CP, Trade, ERP, Payments or TMS.
7. **Downstream custody:** Shared remediation is incomplete while known affected consumers remain unassessed or falsely reported secure.
8. **Time-bound exceptions:** no perpetual blanket ignores, silent scanner disablement, self-approved waivers or unsupported security claims.
9. **Exact evidence:** identify source, dependency version, lockfile, workflow run, published artifact and tested consumer; do not equate source CI with staging or production validation.
10. **Private disclosure:** keep exploit details, real credentials, customer data and sensitive topology out of public issues, logs and artifacts.

## 4. Roles and decision rights

| Role | Responsibility | Limit |
| --- | --- | --- |
| **Security owner** | Triage risk/exploitability, incident response, independently approve compensating controls, validate closure and coordinate advisories. | Does not replace runtime, domain or production authority. |
| **Shared/Platform Engineering** | Maintain policy, repo inventory, template, enforcement tests, reusable scanners, Action pinning and rollout reporting. | Cannot silently impose an incompatible version tool on owners. |
| **Repository/dependency owner** | Inventory packages, update manifests and locks, diagnose Dependabot failures, test final PR head and track remediation deadlines. | Cannot waive failed security controls unilaterally. |
| **Engine/estate/domain owner** | Judge semantic impact, connected compatibility, sensitive negative tests and consumer acceptance. | Cannot treat a green unit test as native execution proof. |
| **Infrastructure/release owner** | Verify runner, IaC, image and toolchain changes; rollback and environment-specific release readiness. | Cannot grant protected staging/production through a maintenance PR. |
| **Independent CODEOWNER/reviewer** | Challenge provenance, privilege changes, test evidence and exceptions. | Cannot replace required distinct approvers with self-review. |

Every security case has a named accountable owner and escalation contact. For material Shared changes, Platform and Security reviewers coordinate with impacted repo owners. Existing branch protections, stale-approval dismissal and required checks remain binding.

## 5. Repository inventory, supported ecosystems and provenance

Each active repository SHALL declare or make discoverable its package-manager capabilities (prefer `.baobab/repository.yaml`), actual manifest/lock paths, intended runtime versions, registry access, source-of-truth owner, supported Dependabot update route, scan coverage, consumer classes and approved exceptions. Verify supported manifests rather than copying ecosystem blocks uncritically. Unknown/unreadable private dependencies must be classified UNKNOWN, not absent.

The inventory distinguishes: **direct vs transitive**; **development/build vs distributed runtime**; **internal vs external**; **pinned source vs installed artifact**; **platform-controlled vs vendor-managed**; and **affected vs unaffected consumer**.

Each release SHOULD produce a suitable SBOM (SPDX or CycloneDX), package/lock provenance, immutable digest and traceable source build. SBOM, dependency graph, CI scan and runtime image inventories are complementary. Do not assume a clean package manifest means that a deployed base image has no vulnerable OS packages.

## 6. Dependabot minimum configuration and GitHub behavior

Each repository SHALL maintain a valid `.github/dependabot.yml` at its real GitHub-recognised path. Dependabot has no built-in cross-repository YAML import: Shared owns templates and conformance checks; each repo owns its file.

For every **applicable** update entry, require:

- `version: 2`, nonempty `updates`, correct `package-ecosystem`, supported `directory` or `directories` and an actual matching manifest;
- reviewed schedule and timezone where pertinent, finite routine `open-pull-requests-limit`, provisioned labels and consistent commit-message format;
- `applies-to: version-updates` for routine grouped minor/patch bumps, with separate major-upgrade review and explicit handling for tightly coupled packages;
- correct registry access using supported secret facilities, not tokens embedded in YAML or source files;
- no unrestricted security-relevant `ignore` unless a separately approved expiring exception and active advisory surveillance exist; and
- default-branch targeting unless a documented, supported exception requires a different version-update base.

**GitHub semantics matter:** `target-branch` customises version updates and should not be used as a security-update targeting policy. Dependabot security updates operate against the default branch, with their own limits/triggering behavior; a configured `open-pull-requests-limit` is not permission to delay a security fix. Scheduled version-update checks do not promise same-day CVE remediation. Confirm the dependency graph, Dependabot Alerts and automatic security updates are actually enabled and functional; a YAML file does not activate them by itself.

New or changed keys MUST be checked against GitHub's supported configuration schema before enforcement. If GitHub does not support a specific ecosystem/version authority, document an alternative update process and cover it with scanners and owner review.

## 7. Ecosystem-specific maintenance rules

| Ecosystem | Required policy implementation | Compatibility caveat |
| --- | --- | --- |
| **GitHub Actions** | Weekly routine update cadence, immutable verified 40-character SHAs, explicit permissions, action-provenance review, pinning CI. | SHA-pinned Actions may not receive the same automatic advisory coverage as semver references; independently reconcile the pinned release against advisories and all consumer uses. |
| **npm/pnpm/yarn** | Dependabot `npm` where supported, root workspace manifests and lockfile, frozen installs, native audit, type/build/tests. | Peer-pinned package families (e.g. Payload) may need coordinated updates; overrides need risk and expiry review. |
| **Go modules** | `gomod` for every actual module, locked/reproducible builds, `govulncheck`, native owner tests. | Identity/crypto and authority boundaries need targeted negative tests and actual Go runtime compatibility. |
| **Python** | `uv` or supported `pip` approach matching real lockfiles; `pip-audit` and supported runtime tests. | Suppressed packages remain subject to active vulnerability monitoring, even during migrations. |
| **Java/Maven** | `maven` at real module/BOM paths, resolved effective dependencies, Trivy, OSGi/JVM and owner-native tests. | Existing Foundation Java-native CVE adapter is not yet wired: record that gap and do not infer a passing native adapter. |
| **Rust/Cargo** | `cargo` plus `cargo-audit`, locked builds and sensitive security-negative tests. | Payment execution and other privileged paths require consequential verification. |
| **Containers/OS** | Docker/Compose entries at real directories, Trivy OS/library scanning, digest/provenance and image rebuild evidence. | Base-image and runtime migration remain separately approved; do not silently replace authoritative toolchain locking. |
| **Terraform/IaC** | Supported provider/module update process, provider lock checks, plan review and Infrastructure ownership. | No automatic protected `apply`, state migration or cloud grant from a dependency update. |
| **Central toolchains** | Named single authority, scheduled version/security review, version lock and consumer qualification. | `baobab-dev` uses `config/versions.yaml` → resolver → lock; an extra Docker Dependabot route must not compete with it. |

**Shared-specific remediation:** `shared` has a root pnpm workspace (`package.json`, `pnpm-workspace.yaml`, `pnpm-lock.yaml`), yet its examined Dependabot file monitors only `github-actions`. Add a supported `npm` entry at `/`, retain package-manager and private-registry correctness, audit security overrides and test representative BXS consumers. No unreviewed bulk upgrade is authorised by this policy.

**IAM-specific remediation:** `baobab-iam` has `go.mod` but an Actions-only update entry in the examined configuration. Add the actual `gomod` coverage and check Go/crypto compatibility.

**baobab-dev-specific remediation:** the observed unconditional `zensical` ignore suppresses security update proposals as well as routine bumps. Time-box or eliminate it after owner review; track any interim exposure outside Dependabot. Do not create an unauthorised second toolchain version authority.

## 8. Routine scheduling, major upgrades and grouping

| Class | Normal review cadence | Required treatment |
| --- | --- | --- |
| Minor/patch version updates | Weekly; prefer existing Monday SAST schedule and stagger ecosystems across the review morning. | Compatible groups reduce noise; group only routine version updates, not unrelated urgent security fixes. |
| Major framework/runtime/engine updates | Review candidates monthly; upgrade through planned compatibility windows. | Independent PR or reviewed coupled-family PR; changelog, migration risk, backward compatibility, rollback and consumer tests. |
| Failed Dependabot jobs and stale PRs | Weekly operational review. | Diagnose registry permission, lock conflict, revoked release, or unsupported manifest rather than suppressing an alert. |
| Pin, image, SBOM and inventory drift | At least monthly and when significant security advisories arrive. | Reconcile actual installed/deployed versions with source and consumer pins. |
| Security alerts | Event driven, independent of weekly schedule. | Use the response deadlines in Section 9; narrow patches have precedence. |

A routine group stuck behind unrelated CI failures SHALL be split if it delays a required fix. Critical/High fixes MUST NOT be auto-merged solely on the basis of a passing dependency bot run; appropriate security, CODEOWNER and owner-native regression review remains necessary.

## 9. Vulnerability triage and response targets

Security assesses exploitability, asset exposure, CVSS/CVE/GHSA, vendor guidance, CISA KEV/known exploitation, EPSS when available, privilege, reachable runtime path, multi-tenant effects, mitigation availability and downstream impact. Labels alone do not replace context-aware severity.

**Proposed service targets** (measured from the earliest actionable detection, not from PR creation):

| Risk | Initial triage | Verified fix or independently validated containment |
| --- | --- | --- |
| **Critical** | Within **4 elapsed hours** | Within **24 elapsed hours** |
| **High** | Within **1 business day** | Within **72 elapsed hours** |
| **Medium** | Within **3 business days** | Within **14 calendar days** |
| **Low** | Within **7 business days** | Within **30 calendar days** |

The targets require an accountable incident/on-call capability; formal acceptance MUST confirm coverage rather than assuming 24/7 staffing. Business days follow the organisation's agreed South African business calendar; hour targets are elapsed.

- **Start clock:** first actionable advisory, scan finding, disclosure or credible incident report. Do not reset aging by reopening, renaming or transferring the finding.
- **Containment:** verified isolation, revocation, disablement, safe downgrade, narrowly scoped override or other demonstrable protection can meet an emergency protection target, but **does not** close the permanent-fix obligation.
- **Closure:** independently verified fixed/contained condition in affected artifact/running environment and relevant consumers; not merely a PR, source merge, passing unrelated CI, exception, or weakened scanner.
- **Exploit in progress / secret exposure:** contain immediately, rotate or revoke compromised material, quarantine unsafe workflows/artifacts and coordinate incident response. Do not wait for a routine window.
- **No upstream fix:** track compensating controls, provider communications and permanent fix due date; reassess Critical/High at least daily and retain protected release restrictions.
- **False positives / non-reachability:** require bounded, reviewed evidence and residual-risk documentation; an `ignore` entry by itself is not evidence.

## 10. Security patch execution playbook

1. **Intake privately.** Record source/advisory ID, first-detected time, exact package version/SHA/digest and affected manifests without exposing exploitable details.
2. **Establish scope and owner.** Inspect runtime reachability, direct/transitive path, deployed images, affected services, Shared consumers, tenants and environments; appoint Security/technical decision makers.
3. **Contain when needed.** Disable unsafe action or integration, rotate credentials, block vulnerable publishing or isolate services under the existing incident authority.
4. **Choose the smallest safe remediation.** Prefer a verified upstream patch; otherwise a reviewed backport, dependency replacement or mitigated override. Record supply-chain provenance and risk tradeoffs.
5. **Update only the authoritative versions.** Commit manifest and lockfile coherently; verify runner/compiler compatibility, package signatures/checksums where available, Action SHA/release attribution and no unrelated version drift.
6. **Verify independently.** Run relevant Foundation dependency audit/Trivy, package-native scanner, workflow pinning, dependency review, SAST/secrets checks, locked build and business/negative tests. Re-run against final PR head.
7. **Obtain appropriate review.** Independent Security/CODEOWNER and owning engine/estate approval for sensitive packages. Respect required checks, stale review rules and protected branches; do not merge around failures.
8. **Propagate to consumers.** Identify every known affected repo, coordinate version/pin upgrades and representative tests, and record lagging/unreachable consumers explicitly.
9. **Release through existing authority.** Development build approval is not staging/production GO. Verify actual digest/version installed and environment-specific rollback.
10. **Close with evidence and learning.** Retest affected artifacts, dispose advisories only with defensible reason, retain permanent-fix backlog if containment-only, and update regressions/templates to prevent repetition.

If the required security fix is blocked by a routine multi-dependency PR, split or cherry-pick a focused fix onto an appropriate protected-branch PR. Never make a failing gate pass by downgrading severity or silently disabling it.

## 11. Verification and promotion gates

| Gate | Required proof | Failure semantics |
| --- | --- | --- |
| **Config conformance** | Valid Dependabot schema, observed manifests, correct update coverage, labels/owners and exception references. | A missing file, missing required ecosystem, bogus directory or unapproved ignore is nonconformant. |
| **Pin and provenance** | Full GitHub Actions SHA, verified associated upstream release, digest/integrity of critical binaries and image sources. | Floating action or unverified release attribution is not trusted. |
| **Vulnerability scanning** | Foundation Trivy and appropriate native package audit against the actual lockfile/dependency set. | Known HIGH/CRITICAL vulnerabilities fail or require approved, visible risk disposition. |
| **Dependency review** | PR-added dependency review when available, enabled and approved under GitHub entitlement/visibility rules. | Unavailable required check is a coverage blocker, not PASS. |
| **SAST, secrets, CI trust** | Applicable CodeQL/fallback, secrets checks, OIDC/permission verification; restrict fork PR privileges. | Scanner skip or missing workflow never becomes synthetic green. |
| **Build and regression** | Frozen-lockfile install, lint/type/build, applicable unit/integration/browser tests and changed runtime compatibility. | Compilation alone does not prove business compatibility. |
| **Sensitive engine tests** | Real IAM/CP or native authority, negative-path, replay, isolation and failure handling for impacted engine changes. | Synthetic fixture or mock provider must not be reported as actual consumer qualification. |
| **Publish/consumer evidence** | Exact source/CI head, SBOM/digest, consumer pin and deployment/runtime verification, independent reviewer. | Maintainer PR success does not prove another repository or live environment safe. |

Reuse the existing Foundation workflows and evidence model. Where an adapter is missing, establish a specific tracked gap and equivalent approved control; do not create a second inconsistent general scanning framework. Java-native security audit is a known unfinished adapter in the inspected Foundation implementation.

A security PR may warrant additional targeted tests beyond the baseline; changed auth, broker, payment, posting, schema or provider behavior must retain applicable refusal/rollback scenarios.

## 12. Exception, ignore, and waiver governance

Exceptions use the existing approved `.baobab/repository.yaml` / Foundation model, or a separately reviewed extension that does not create a competing waiver authority. Each exception SHALL record: ID, affected control/package/advisory and environments, exact version/scope, threat and business impact, owner, independent Security approver, compensating controls, reason, expiry, reassessment schedule, permanent-fix plan and restricted evidence reference.

- Critical actively exploited exposure cannot be indefinitely accepted or hidden by a broad ignore. Emergency containment is an incident decision, not permanent risk acceptance.
- High findings require independent Security review, frequent reassessment and explicit protected-release disposition.
- Medium/Low exceptions must be bounded and dated with accountable remediation.
- Expired, missing, unknown and self-approved exceptions SHALL block claims of conformance; extensions require fresh independent evidence.
- Dependabot ignores, audit-level changes, scanner allowlists, `--ignore-unfixed`, skipped adapters and deferred SBOM coverage are all risk-affecting decisions and must be visible to reviewers.
- Where Foundation returns **WAIVED**, reports MUST NOT re-label that status **PASSED**. Existing protected release callers may require zero active waivers.

An advisory that is not exploitable in a particular build may be dispositioned on evidence, not assumed harmless because the dependency is used only in tooling.

## 13. Supply-chain trust, registry security and action monitoring

Private package registries need read-only trusted credentials or short-lived supported auth. Do not commit token-bearing `.npmrc`, expose bot secrets to forks, or pass package publishing rights to ordinary dependency-update jobs. Pin sensitive downloads, verify checksums against trustworthy source material and apply explicit workflow permissions. Use OIDC with restricted trust claims for publishing/deployments instead of broad long-lived secrets when feasible.

Full-SHA action pinning protects against silent tag movement but does **not** guarantee that an action is free of vulnerabilities. At least weekly, reconcile action repository/release/commit/advisory signals and evaluate affected **consumer usage**, including `baobab-platform/shared` reusable workflows. A central pin upgrade is a deliberate change reviewed with the upstream release notes, new permissions, Node runner compatibility and affected callers.

Never auto-promote a new image/compiler or automatically rewrite a central tools lock through an unsupported manifest parser. All producer-to-consumer updates retain source provenance and immutable acceptance evidence.

## 14. Change safety, rollback and protected environments

Apply the existing default branch ruleset: PR review, CODEOWNER coverage, resolved conversations, latest required application and Foundation checks, stale review invalidation, and no unapproved administrative bypass. Sensitive dependency changes require domain review for cryptography, OAuth/OIDC, secrets, broker/event integrity, ERP posting, payments, Customs/regulatory decisions and external provider clients.

Development testing MAY exercise disposable engines and environments under accepted development controls. Staging/production deployment MUST still pass their independent security, IAM/CP, legal, financial/provider, artifact and runbook gates. Dependabot and this policy do not activate release authority.

A rollback plan records previous safe artifact digest, dependency lock, compatibility with persisted data/migrations, incident containment, consumer pin restoration and credentials to rotate. A rollback that knowingly reintroduces exploitable software is not a safe rollback without a verified alternative containment.

## 15. Evidence model, retention and disclosure

Every material dependency or security case must have independently reviewable evidence:

| Category | Minimum record |
| --- | --- |
| **Finding** | Advisory/CVE/GHSA or case ID; first-detected timestamp; severity basis; affected repositories, runtime or consumers. |
| **Source** | Owning repo, PR, exact tested final commit SHA; manifest and lockfile versions/diff; responsible maintainer. |
| **Execution** | CI run/job ID, scanners and versions, native checks, negative tests, failures and final dispositions. |
| **Artifact** | Package versions, Action SHA, image digest, provenance/SBOM where available, actual deployed revision. |
| **Governance** | Security/domain reviewer, exception/expiry if present, decision and deadlines, environment promotion authority. |
| **Consumers** | Names/pins of known affected repos, compatibility result, unknown or blocked consumers, propagation evidence. |
| **Closure** | Verified fix/containment, retest, timestamp and residual/permanent-fix work. |

Retain non-sensitive evidence under the existing Foundation 90-day artifact practice when configured, with durable links or appropriately stored summaries for longer governance needs. Private reports and exploits remain restricted; never add raw secrets or topology to public docs. Labels and summaries distinguish **PROPOSED, SOURCE_COMMITTED, CI_VERIFIED, CONSUMER_QUALIFIED, WAIVED, BLOCKED, STAGING_VERIFIED, PRODUCTION_VERIFIED**. These statuses are not interchangeable.

## 16. Metrics, operating rhythm and escalation

Platform Engineering produces a weekly operational review and monthly organisation-wide report, with Security validating risks. Include:

- repository and ecosystem coverage, missing/invalid Dependabot entries, feature enablement and working scanner coverage;
- open Critical/High vulnerabilities by age, exploitable path, source and runtime environment; late triage, containment and permanent fixes;
- PRs blocked by native audit, lock conflict, private registry, consumer incompatibility or reviewer availability;
- stale routine/major upgrades, vulnerable/outdated SHA-pinned Actions and container/toolchain drift;
- active/expired exceptions, scanners waived/unknown, and unscannable packages or unverified SBOMs;
- time-to-triage, time-to-containment and independently verified remediation, including percentiles and missed targets;
- Shared-derived fixes actually adopted and qualified in consumer repositories.

Never count an unknown/restricted repository as compliant. Report the checked source SHA and snapshot date. Recurrent failures enter the existing Shared assessment and improvement registers; material breaches escalate through incident management.

## 17. Findings-driven adoption programme

**Observed snapshot, 5 November 2026:** 20 accessible Baobab repositories had a `.github/dependabot.yml`. Seven examined configurations specified unnecessary `target-branch: main`; eight lacked one or more fields expected by the current Shared structural validator. Shared lacked a configured npm/pnpm update ecosystem; IAM lacked Go coverage; several repositories grouped upgrades broadly; `baobab-dev` included an unconditional `zensical` ignore. Existing Foundation dependency scans, secrets scanning, Action pinning and dependency review form a strong starting point. These are **dated configuration observations**, not current vulnerability proof or evidence that all scanners are deployed/enabled.

Adopt in controlled waves:

1. **P0 Security exposure:** inventory live alerts and exploitability, enable/verify available GitHub dependency security features, triage ignored dependencies and affected consumers; respond to actual vulnerabilities first.
2. **P1 Shared standard:** review this policy, fix the Shared Dependabot baseline and template, strengthen existing conformance checks with manifest awareness and exception validation, add positive and negative policy tests.
3. **P2 Repo-specific adoption:** coordinate companion PRs across all 20 observed repos (and newly discovered repos) with correct actual package managers, directories, grouping and scan enforcement.
4. **P3 Audit automation:** add independently sourced advisory reconciliation for SHA-pinned Actions; establish inventory, exception expiry checks and measured security response/reporting.
5. **P4 Evidence closure:** inspect final-head CI and consumer proof per repository, close only verified obligations, and track unresolved, unavailable or protected-environment evidence separately.

Illustrative owner profiles: Shared/Nabhold/ZuriBeans/Thamani/Equator (JS/Actions/containers as applicable); IAM/CP (Go plus real frontend/containers); Trade/CMS/Subscriptions (owning JS/Java modules); ERP (Maven/iDempiere); Pulse/Regulations (actual Python or other manifests); Payments (Cargo); Infrastructure/baobab-dev (Infrastructure/uv/central toolchain locks); TMS/SCF/Trade Docs and engine-template (manifest-discovered). The illustrative profile does not authorise inventing package ecosystems where manifests do not exist.

## 18. Acceptance and regression safeguards

**Required positive checks:**

- valid config and verified root or nested manifest passes the Shared structural checker;
- supported package ecosystems and authoritative locks produce testable, frozen installs and visible scanner results;
- minor/patch routine grouping and isolated majors are observable without delaying security fixes;
- full-SHA Actions have validated release provenance and consumer inventory;
- approved unexpired exceptions display as **WAIVED** with owner and expiry;
- native, negative and consumer tests prove changed sensitive paths; final artifact/digest matches tested source.

**Required negative checks:**

- missing config, malformed YAML, missing ecosystem/manifest, duplicate or unsupported paths and unapproved blanket ignore cannot pass;
- expired/self-approved exception, unavailable entitled scanner, skipped required workflow and missing registry permission are not treated as green;
- floating Action tags or incorrect SHA provenance, untrusted fork privilege, unreviewed major upgrade and failed native audit fail safely;
- an unrelated green build without actual sensitive negative tests is not declared consumer qualified;
- a fixed Shared repo with vulnerable/unknown downstream consumers remains **PARTIAL**, not closed;
- source merge, waived scanner or attempted rollback to a vulnerable image cannot be rebranded as production verification.

Use safe fixtures. Tests SHALL NOT expose live keys, attack payloads, private customer records or restricted topology. Policy-enforcement rollout MUST have false-positive and legacy-exception migration evidence before being made a mandatory organisation-wide check.

## 19. Review, amendment, acceptance and record

Changes require Platform Engineering and Security review under protected branch rules; consequential ecosystem requirements additionally involve affected owners. Review quarterly and after major compromise, release-toolchain migration, changed GitHub feature entitlement or material new advisory. Major revisions change required controls/authority; editorial revisions correct clarification without silently expanding acceptance.

**v1.0 acceptance** requires owner assignment, reviewed documentation, an implementation issue/plan for configuration and scanner gaps, and specific criteria for cross-repository evidence. This policy's merge does not itself complete the P1–P4 rollout or authorise any protected environment.

| Version | Date | Description | Decision state |
| --- | --- | --- | --- |
| **1.0** | **2026-11-05** | Risk-led maintenance standard: supported ecosystems, timely security patches, Shared controls, SHA/action provenance, exception expiry, sensitive regression tests and 20-repository rollout. | **PROPOSED — awaiting review and merge** |

---

**Engineering principle:** **Automate discovery. Verify the actual risk. Patch promptly. Preserve independent authority. Prove the consumer is safe.**
