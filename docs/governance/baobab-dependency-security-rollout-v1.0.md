# BA-SEC-DEP-001 — Dependency and Security Maintenance rollout register

**Baseline:** [Approved Dependency & Security Maintenance Policy v1.0](baobab-dependency-security-maintenance-policy-v1.0.md), 5 November 2026.  
**Implementation branch:** [Shared PR #429](https://github.com/baobab-platform/shared/pull/429).  
**Evidence class:** Engineering adoption register, not a replacement for repository-specific source, CI, security, integration or production evidence.  
**Custodians:** Platform Engineering and Security, with each source repository's owner responsible for its own verification.

## A. What is implemented on Shared PR #429

| Control | Owned implementation | State on source branch | Required independent qualification |
| --- | --- | --- | --- |
| Approved policy text and response windows | `docs/governance/baobab-dependency-security-maintenance-policy-v1.0.md` | SOURCE_COMMITTED | Branch review and adoption; confirm staffing for 4h/24h Critical targets |
| Correct Shared Dependabot coverage | `.github/dependabot.yml` | SOURCE_COMMITTED | GitHub Dependabot npm/pnpm 11 update job actually starts, accesses manifests/registry, and produces a reviewable PR |
| Org adoption template | `templates/dependabot.yml` | SOURCE_COMMITTED | Real consumer pilot, retained package-specific adaptations |
| Strict conformance with legacy baseline mode | `.github/workflows/enforce-dependabot-config.yml` | SOURCE_COMMITTED | End-to-end workflow invocation and 23 offline positive/negative fixture cases; no false green |
| Strict Shared gate | `.github/workflows/ci.yml` | SOURCE_COMMITTED | Final-head CI and Foundation; routine consumers retain baseline mode pending pilot |
| Advisory watch for SHA-pinned Actions | `scripts/action_advisory_watch.py` and `.github/workflows/action-advisory-watch.yml` | SOURCE_COMMITTED | Scheduled public API response, safe UNKNOWN failure, artifact review, reviewer disposition of actual pinned SHA |
| Advisory watch offline test coverage | `scripts/tests/test_action_advisory_watch.py` | SOURCE_COMMITTED | Test execution plus live advisory API smoke check |
| Independent security ownership | `.github/CODEOWNERS` | SOURCE_COMMITTED | Actual protected-branch CODEOWNER enforcement, not merely filename membership |

**Not done merely by source commit:** verified CI status, GitHub feature enablement, Dependabot-generated security PR, actual live vulnerability triage, downstream conformance, private advisories, protected deployment, and any enterprise-wide policy enforcement. Do not label SOURCE_COMMITTED as CI_VERIFIED.

### Development checks to execute

`python scripts/tests/test_dependabot_policy.py` and `python scripts/tests/test_action_advisory_watch.py` require the already governed PyYAML fixture runtime. The Shared CI governance-contracts job invokes both; the reusable self-check runs with `policy-level: strict` and `required-ecosystems: github-actions,npm`.

The SHA advisory watcher runs on a UTC daily schedule **only after merge into the repository's default branch** (or when explicitly dispatched). It has read-only permissions, produces review/triage evidence, and never auto-upgrades dependencies, grants security clearance or promotes releases. A package-name match is NOT proof its pinned SHA is within a vulnerable range; zero matches are NOT a safety assertion. A network/API failure is UNKNOWN.

## B. Open priority risks and next implementation waves

| Gate | Priority | Owned follow-up | Evidence required to close |
| --- | --- | --- | --- |
| P0-A | Critical when actionable alerts exist | Security + each repository owner: inventory Dependabot Alerts, available automation and current GHSA/CVE findings; triage exploitability and environment exposure | Restricted advisory inventory with first-seen timestamps, owners, deadlines and verified fixes/containment. The GitHub source-file audit alone cannot establish no CVEs. |
| P0-B | High | All repos with redundant `target-branch: main`, beginning with Shared plus named consumer PRs | Per-repo confirmed default branch and reviewed config change; security updates target intended default branch |
| P0-C | High | IAM adds `gomod` for real Go modules; audit other actual nested modules | Immutable source, supported Dependabot job, successful Go-native build, `govulncheck` and IAM authority negative tests |
| P0-D | High | `baobab-dev` owner resolves `zensical` blanket ignore | Fixed or bounded version-only ignore; security finding and permanent-fix review preserved; no second toolchain authority |
| P1-A | High | Shared Platform/Security: promote template/strict validator after a real pilot | Actual consumer CI starts, locked build succeeds, negative policies refuse invalid config, existing Foundation unaffected |
| P1-B | High | Native Java adapter owner: reconcile Maven/OSGi audit coverage | Effective dependency tree, independently reviewed CVE result and iDempiere JVM compatibility; do not claim Trivy is a full Java-native adapter |
| P2-A | Medium | All 20 source owners: implement manifest-correct Dependabot config and strict opt-in | Each repo's final-head CI, classifier match, owners, native scans and reviewed exemptions. Do not enable all gates simultaneously without migration receipts |
| P3-A | Medium | Security: advisory review process for pinned Actions and containers | Real documented reviewer triage of package match, upstream SHA, resolved release, affected consumer and action permissions |
| P3-B | Medium | Security & Platform: posture/aging report | Exact inventory date/SHA; coverage, UNKNOWN, ACTIVE, WAIVED and overdue counts; no invented data |
| P4-A | Medium | Owners/release managers: consumer verification and protected deployment | Actual downstream version/digest adoption, negative tests and separate environment acceptance |

### Initial inventory snapshot

The following reflects only the **5 November 2026 Dependabot configuration survey**, not a live dependency alert or current vulnerability assessment. Re-inventory the organisation before each rollout because the codebase and repo counts change.

| Repository | Observed update characteristics | Next owner action |
| --- | --- | --- |
| `shared` | Actions only; root pnpm workspace omitted | Shared config corrected in this PR; verify npm update flow |
| `nabhold` | Actions + npm; `target-branch` present; Node type major deliberately constrained | Remove redundant target branch, confirm runtime major and BXS/estate tests |
| `zuribeans` | Actions + npm + Docker; `target-branch` present | Remove target branch, adopt routine grouping, run Playwright/Lighthouse/performance and buyer/supplier paths |
| `thamani` | Actions + npm + Docker; unscoped groups | Separate routine groups from security, validate B2B logistics UX and build |
| `equator-estate` | Actions + pip + Docker; minimal fields | Verify real Python/container manifests and supply missing governance fields |
| `baobab-cp` | Actions, Go, Docker, npm and frontend Docker; broad Go grouping | Restrict routine grouping and run CP authority/tenancy negatives |
| `baobab-iam` | Actions only though Go modules exist | Add `gomod` and native Go security/authority verification |
| `baobab-trade` | Actions + npm + Docker; `target-branch` present | Remove target branch and qualify native buyer/commitment operations |
| `baobab-erp` | Actions + Docker + Maven; `target-branch` present | Remove target branch; JVM/iDempiere and transactional replay verification |
| `baobab-cms` | Actions + npm; grouped Payload family; `target-branch` present | Preserve peer-pinned Payload family; remove redundant target branch |
| `baobab-pulse` | Actions + uv + Docker; `target-branch` present | Remove redundant target branch, validate lock/AI ingestion evidence |
| `baobab-dev` | Actions + uv; central toolchain lock; `zensical` ignored | Remove/time-box blanket ignore; preserve deliberate versions lock |
| `infrastructure` | Actions + Docker minimal | Add required fields, inspect actual Terraform and Compose directory coverage |
| `baobab-subscriptions` | Actions + Maven + Docker; broad Actions grouping | Scope routine grouping, add native JVM verification |
| `baobab-payments` | Actions + Cargo + Docker; broad Actions grouping | Scope routine grouping and preserve mandate/transaction negatives |
| `baobab-regulations` | Actions only | Discover actual Python/other manifests and qualify deterministic decision boundary |
| `baobab-trade-docs` | Actions only | Discover actual manifests; add documentary custody/advisory coverage |
| `baobab-tms` | Actions only | Discover provider SDK/runtime dependencies; test booking/replay negatives |
| `baobab-scf` | Actions only | Discover actual manifests and ensure finance partner/legal restrictions |
| `engine-template` | Actions only | Produce secure profile template and require governance fields |

**Important:** No row authorises a package-manager guess. `uv`, `pip`, `gomod`, `maven`, `cargo`, `terraform` and Docker configurations must match confirmed manifests and the actual repo owner-approved version authority.

## C. Consumer adoption procedure

1. Inspect the consumer's current default branch, `.baobab/repository.yaml`, manifests, package manager, private registry permissions, true Docker/IaC directories and required Foundation/Security jobs.
2. Start from the Shared template; keep only real ecosystems, supported paths and labels. Do not introduce `target-branch: main` merely to repeat the default branch. Scope routine groups to `applies-to: version-updates`, with major/sensitive families independently reviewable.
3. Remove blanket ignores or obtain approved, expiring remediation decisions under the existing Foundation exception model. Do not invent a parallel waiver format. A blanket ignore is a strict conformance failure by default.
4. Adopt the existing reusable configuration workflow pinned to the **approved released Shared commit**, initially with `policy-level: baseline` while discovering legacy conformance gaps. Change the consumer to `strict` only after tests, approvals and migration evidence; never reference an unmerged PR SHA as a promoted security control.
5. Demonstrate the actual Dependabot job, required scans and final-head native/build/integration checks; verify both positive updates and negatives: malformed config, outdated Action pin, blocked registry access, unapproved ignore and relevant authority/refusal behavior.
6. Confirm the consumer's new dependency lock/image/pin is published and adopted where applicable. Do not confuse synthetic source tests with protected release or independent legal/provider approval.
7. Record `SOURCE_COMMITTED`, `CI_VERIFIED`, `CONSUMER_QUALIFIED` and `STAGING/PRODUCTION_VERIFIED` separately, including unknown and blocked evidence. Require independent Security/Platform/owner review per scope.

## D. Exception and reporting rules

The new strict validator intentionally **fails closed** on unconditional Dependabot ignores, broad security catch-all groups, undefined registries, duplicate or unsafe paths, missing required ecosystems, and redundant default-branch `target-branch`. It does not implement a live CVE/EPSS/CISA KEV severity classifier or private advisory reader; those require authorised data access and separate runtime evidence.

The action advisory watcher MUST be treated as intelligence for a human decision. Reviewers must independently establish the **specific pinned SHA** and upstream release mapping, whether the GHSA affects the used version, the call path and consumer scope. Record false matches with explanation. Failure to contact the advisory API reports **UNKNOWN** and must not be interpreted as clearance.

All maintenance evidence is subordinate to the accepted EA and release-gate authorities. **Shared #429 retains its DEV-11 blocked connected acceptance**; adding security policy files must not convert that separate blocker into acceptance.

## E. Completion criteria

- Shared policy decision is **Approved**, with exact source changes reviewed and CI verified.
- The Shared pinned Actions / npm updates and strict local conformance run with actual supported package managers.
- At least one carefully selected consumer passes and fails the deliberate positive/negative pilot before strict adoption is advertised as reusable.
- All 20 initial repo owners produce qualifying migration/exception receipts; newly discovered repos join the inventory.
- A current, restricted security-alert inventory validates Critical/High exposures and records disposition within the approved severity targets.
- At least one real advisory review demonstrates exact pinned Action SHA assessment rather than broad package-name matching.
- No inherited release authority, self-certified evidence, secret leakage or hidden skipped mandatory checks.

**Status note (5 November 2026):** Only Shared source changes are committed to PR #429; no claim of cross-repository completion is made by this register.
