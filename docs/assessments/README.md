# Baobab Platform — Audit assessments

This directory contains **dated, evidence-linked technical, strategic, security, developer-experience, product and operational assessments** across the Baobab Platform ecosystem. It enables comparison over time, makes recommendations discoverable and retains the rationale for improvements.

**An audit assessment is NOT a governing ADR, an Accepted implementation plan, a Control Plane source of truth, a runtime acceptance receipt or protected release authorisation.** Findings are advisory until the appropriate domain/Platform Owner approves a remedy through existing channels. Do not silently restate old audits as current facts.

## Browse

| Resource | Purpose |
| --- | --- |
| [EA v2.3 / EA-DEV assessment — 24 October 2026](architecture/2026-10-24-ea-v2.3-ea-dev-strategic-technical-assessment.md) | Evidence-based implementation drift, critical-path risk, strategic opportunities and engineering recommendations |
| [IAM ADR-to-capability assessment — 24 October 2026](iam/2026-10-24-iam-adr-capabilities-implementation-assessment.md) | 15-operation inventory; MP0–MP20 implementation/acceptance assessment; Kratos/Hydra/Keycloak capability limitations; IAM-specific BA-AUD-015–028 findings and critical path |
| [Control Plane ADR-to-capability assessment — 24 October 2026](cp/2026-10-24-cp-adr-capabilities-implementation-assessment.md) | Twenty-five CP authority/operation families; source versus qualification evidence; ADR precedence; BA-AUD-029–041 mapped into **existing EA-DEV** only |
| [Findings and improvements register](findings-register.md) | Stable IDs, owner proposals, triage state, precise closure criteria and dated improvement log |
| [Assessment template](templates/assessment-template.md) | Reusable structure for future architecture, security, UX, operations, provider or engineering reviews |

Future directories may include architecture/, security/, developer-experience/, product/, operations/ and compliance/ **only when a real assessment exists**. Do not create empty structures for appearances.

## How to conduct and retain an assessment

1. **Snapshot, do not overwrite.** Date the observation and link source SHA, audited PR head, CI run, canonical scenarios, owning evidence and any environmental restrictions. Name files YYYY-MM-DD-short-scope-assessment.md (or similarly clear).
2. **State limits.** Separate directly observed facts from prior dated evidence, interpretation, risks and proposed improvements; NOT_ASSESSED never means NOT_IMPLEMENTED.
3. **Preserve independent assurance axes.** ADR Accepted, SOURCE_MERGED, source CI PASS, actual real-component synthetic tests, independently authorised protected staging, external/provider/legal acceptance and production GO remain distinct.
4. **Respect architectural precedence.** The current [Accepted EA v2.3](../architecture/EA-implementation-plan-v2.3-2026-10-20.md), [EA-DEV](../architecture/ea-v2.3-development-enablement-implementation-plan-2026-10-23.md), [EA-REL](../architecture/ea-v2.3-progressive-production-release-programme-2026-10-23.md), [canonical L4/INT/NAB matrix](../architecture/ea-v2.2-integration-acceptance-matrix.md) and owning ADRs govern work; this directory does not replace them.
5. **Track each substantive finding.** Assign a stable BA-AUD-NNN identifier in [the findings register](findings-register.md), proposed owner, severity, evidence, verification requirement and a reviewable next action. Don't prematurely label a recommendation Accepted or a PR as successful.
6. **Reassess instead of rewriting history.** Publish a newer dated assessment; link old and new in both directions if helpful. Link to the actual fixing PR/merge and current runtime receipt, then update the tracked finding with a dated verified outcome.
7. **Use measured outcomes.** Compare security-negative coverage, enterprise journey completion, contract compatibility, developer setup/integration time, recovery, accessibility, availability and operating cost—not just number of ADRs or PRs.

## Status terminology

- **ADVISORY ASSESSMENT:** a signed/dated observation and recommendations only.
- **OPEN:** observed with actionable supporting evidence, not closed.
- **TRIAGE:** hypothesis, strategic proposal or concern requiring further verification.
- **ACCEPTED_FOR_WORK / IN_PROGRESS:** accepted work via existing owning programme and currently implemented effort.
- **VERIFIED_RESOLVED:** actual applicable closure evidence reviewed; source-only is not enough for runtime findings.
- **REJECTED_WITH_REASON / SUPERSEDED_WITH_LINK:** reviewed disposition retained.
- **REVALIDATION_REQUIRED:** stale or changed source dependency; no automated pass/fail or production approval.

## Confidentiality, source retention and audit independence

This repository may be publicly accessible. Never commit raw OAuth tokens, private issuer credentials, personal data, customer documents, session cookies, unredacted logs, private topology secrets or restricted legal/provider evidence. Link to approved private custody where appropriate, showing only redacted IDs and digests. Assessments may reference independent approvals but **must never manufacture or grant them**.

Reports may use emerging standards (e.g., OpenTelemetry, SLSA, OWASP, DORA) as explicitly labelled external research; the applicable accepted Baobab ADR/domain decisions remain authoritative. Reference links are not proof of Baobab implementation.

## Review policy

A new assessment should receive source/evidence review and ordinary documentation CI. Findings accepted for engineering require owner scope, implementation PRs and actual qualifying tests. Future automation may refresh read-only snapshots or flag dependencies, but must not invent evidence, modify canonical state or conflate protected authority with developer acceptance.
