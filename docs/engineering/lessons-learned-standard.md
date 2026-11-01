# Cross-repository engineering lessons learned standard

Status: **Proposed for architectural acceptance**  
Scope: Baobab Platform engineering repositories, including Shared, Control Plane, IAM, Infrastructure, Digital Estates (Nabhold, ZuriBeans, Thamani), and future consumers.  
Origin: ZuriBeans [#131](https://github.com/baobab-platform/zuribeans/pull/131), [#142](https://github.com/baobab-platform/zuribeans/pull/142), and [#144](https://github.com/baobab-platform/zuribeans/pull/144).

## Principle

A resolved engineering failure becomes reusable institutional knowledge only when its cause, verified resolution, and executable regression guard are retained. Before addressing a failure, look for the same signature in prior incidents; compare actual root causes rather than blindly repeating a patch.

This standard proposes process controls. It does not replace Accepted EA v2.3, EA-DEV, ADRs, provider authority, environment controls, or production/staging approvals.

## Required learning record

Assign a stable ID in the owning repository's engineering lessons register and record:

1. **Symptom**: exact error, failing gate, affected routes/components, runtime and environment.
2. **Evidence**: commit SHA, CI run/job, minimal reproduction, observed measurements and artifacts.
3. **Root cause**: distinguish verified causality from hypotheses and environmental noise.
4. **Correction**: minimal durable change, alternatives rejected, and any compatibility consequences.
5. **Regression prevention**: test name, script, workflow, budget, static rule, negative test, or review checklist.
6. **Verification**: passing final-head run, before/after values, independent review and status.
7. **Reuse scope**: ownership, related incidents, affected engines/estates, and candidate shared guard.

Avoid unsupported “fixed” or “qualified” claims. Failed or missing evidence remains visible.

## Required workflow

- At PR intake, search the owning repository's register and the Shared register for the same signature and adjacent failures.
- Diagnose from the current exact commit and failed CI step, not an earlier passing ancestor.
- Preserve specified contracts, accessibility, approved UX, security boundaries, and fail-closed authority. Never fix CI by disabling a test, globally hiding overflow, blindly changing screenshots or inflating performance thresholds.
- Add a focused automated regression guard when feasible; document any justified gap explicitly.
- Re-run scoped checks and required full qualification at the final head. Stacked PRs each need independent evidence.
- Record the incident in the owning register and cross-link the PR, root cause, correction and test.
- Promote cross-repository patterns through reviewed Shared documentation or shared tooling changes. Never mutate consumer budgets or estate-specific design policies without the owning acceptance decision.

## Initial cross-estate lessons proposed for adoption

- **Responsive overflow**: absolutely positioned visually hidden elements can inflate page width; prefer semantic native structure over global `overflow-x: hidden`. Verify 320, 390, 768, 1024 and 1440 px where applicable.
- **Visual regression**: compare screenshots against approved design, not merely a stale prior baseline. Review changed pixels and do not auto-accept updates.
- **Performance bundles**: measure actual emitted assets and preserve meaningful CSS, JavaScript and image budgets; optimize modules before considering budget revisions.
- **Lighthouse**: run throttled performance checks without competing Playwright workers; preserve thresholds and measurement receipts.
- **Prototype authority**: Figma parity, synthetic data and development visuals are not evidence of commercial facts, certification, mandate, provider acceptance or live commitments.
- **Final-head gates**: a passing parent or historical SHA does not qualify a modified child branch.
- **Documentation quality**: new engineering guidance itself must satisfy formatting and repository quality gates.

The authoritative incident details remain in the owning repository: [ZuriBeans lessons register](https://github.com/baobab-platform/zuribeans/blob/feat/zb-dev-data-v1-synthetic-experience/docs/engineering/lessons-learned.md). This Shared standard is not proof that all consumers have adopted these controls. Consumers should implement enforcement under their respective change reviews.

## Acceptance and lifecycle

The Shared maintainers and affected consumer owners review this proposal. Upon acceptance, maintain a versioned shared index of lessons, distinguish platform-wide standards from repository-specific remedies, and include a register lookup in PR templates or review checklists. Any new generic check must be tested against representative consumers before broad enforcement.

**Do not merge solely because this document exists.** Check final-head CI and architectural review requirements.
