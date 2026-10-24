# Audit assessments — Findings and improvement register

**Status:** Advisory tracking index, not an Accepted ADR, capability source, runtime evidence registry or production release authority.  
**Initial snapshot:** [BA-AUD-2026-10-24-EADEV-01](architecture/2026-10-24-ea-v2.3-ea-dev-strategic-technical-assessment.md), observed 24 October 2026.  
**Current implementation/evidence authority:** [EA-DEV register](../architecture/ea-dev-implementation-register.md), [canonical L4 matrix](../architecture/ea-v2.2-integration-acceptance-matrix.md), owning source/CI receipts and protected release records.

## How the register works

Audit findings use stable **BA-AUD-NNN** identifiers across re-audits. A row records observation and recommendation; **it does not grant permission to modify canonical contracts**. A suggested owner is accountable for triage, not assigned personnel or independently appointed approval. Do not mark RESOLVED because a PR opens, CI is green or a proposed ADR exists. Verify the precise closure criteria and preserve the link to the successful owning repository change, real receipt where required and reviewed decision. Proposed options must be reconciled through accepted EA/ADR/domain owners before becoming obligatory.

Allowed statuses: **OPEN** (observed with source evidence), **TRIAGE** (inference or improvement hypothesis pending validation), **ACCEPTED_FOR_WORK** (owning programme accepted a remedy), **IN_PROGRESS**, **VERIFIED_RESOLVED**, **REJECTED_WITH_REASON** and **SUPERSEDED_WITH_LINK**. An outdated evidence observation is **REVALIDATION_REQUIRED**, not automatically a failure or success. For each updated row, annotate date and immutable source, preserve previous history in a linked review or issue.

| ID | Priority | Character | Status at 2026-10-24 | Recommended owner | Problem / strategic opportunity | Proposed resolution and closure test |
| --- | --- | --- | --- | --- | --- | --- |
| **BA-AUD-001** | P0 | Observed CI blocker | OPEN | Infrastructure + IAM/CP | Infrastructure [#54](https://github.com/baobab-platform/infrastructure/pull/54) INT-02 [run](https://github.com/baobab-platform/infrastructure/actions/runs/40058049607) failed in human IAM login proof, status 500 | Identify root cause without masking the test; final-head mandatory CI passes and DEV-02 scoped fixture receipts/teardown are inspected |
| **BA-AUD-002** | P0 | Observed qualification gap | OPEN | IAM + CP + Infrastructure | DEV-03 and all seven DEV-04 INT-03C cases lack fresh qualifying current-profile evidence in inspected Shared register | Current actual IAM-issued token/Principal/grant and all original cases observed, with explicit denials and cleanup |
| **BA-AUD-003** | P0 | Observed qualification gap | OPEN | Nabhold + CMS + IAM/CP/Infra | DEV-05 fourteen NAB-03 cases and DEV-06 external zero-estate journey not qualified in inspected register | Actual case-by-case positive/negative receipts per owning programme, not lifecycle substitutions |
| **BA-AUD-004** | P1 | Architecture risk | TRIAGE | Shared EA-REL + Infrastructure | DEV-13 dependencies DEV-04..12 may be interpreted as a global production release prerequisite despite progressive EA-REL | Approve and test scope-specific release dependency projection while retaining all applicable protected approvals |
| **BA-AUD-005** | P1 | Verified tool limitation / compatibility risk | TRIAGE | Shared Foundation + engine owners | Valid but older Shared consumer pins prove neither failure nor semantic compatibility | Produce per-contract changed-consumer impact report with actual selected compatibility tests and explicit permitted lag |
| **BA-AUD-006** | P1 | Observed documentation freshness | OPEN | Shared EA-DEV register owner | CP [#434](https://github.com/baobab-platform/baobab-cp/pull/434) merged while latest Shared DEV-02 row had not yet adopted it | Reconcile exact CP and Infrastructure verified outputs; optional source-change flag does not self-accept evidence |
| **BA-AUD-007** | P2 | Manifest completeness question | TRIAGE | Shared contract catalogue | New Trade v2 schema files not enumerated in root contracts.lock.yaml; manifest exhaustiveness not established | Document manifest semantics; if intended exhaustive, generate/validate all published schemas and consumers |
| **BA-AUD-008** | P1 | Availability/revocation design opportunity | TRIAGE | CP/IAM + owner-native PEPs | Bounded authorisation attestations and CP outage consistency need explicit measured operational treatment | Owner-authorised policies and transaction-time expiry/replay/revocation/outage negative tests |
| **BA-AUD-009** | P1 | Cross-engine evidence opportunity | TRIAGE | Shared / Infrastructure / Observability owners | Receipt/trace information remains distributed across multiple owning registers and engines | Cross-link existing evidence by source/decision/environment/correlation without inventing a second authority |
| **BA-AUD-010** | P1 | Product/release measurement opportunity | TRIAGE | Platform Product / EA-ENG / Dev tooling | Architecture progress is easier to enumerate than qualified user and developer outcomes | Adopt measured integration, journey, recovery, cost and capability-specific readiness criteria |
| **BA-AUD-011** | P2 | Verified documentation mismatch | OPEN | Shared maintainers | README said repository Private; GitHub repository metadata says Public | Correct metadata wording; separately review public artifact redaction and sensitive content rules |
| **BA-AUD-012** | P3 | Verified hygiene | OPEN | Shared maintainers | Tracked Python .pyc files / missing cache exclusions | Narrow cleanup PR with ignores; confirm no tracked bytecode remains |
| **BA-AUD-013** | P1 | Developer-experience opportunity | TRIAGE | baobab-dev / Shared Foundation | Root Shared pnpm is 11.24.0 while an upstream major release exists; effects on consumers unknown | Controlled compatibility/registry/Codespaces test matrix, rollback and explicit upgrade/defer decision |
| **BA-AUD-014** | P1 | Engine onboarding opportunity | TRIAGE | Shared / Infrastructure / engine-template / Pulse / Payments | DEV-14/15 are accepted work requirements without a demonstrated reusable headless provider journey in audit evidence | Actual real IAM/CP plus Pulse and Payments sandbox test receipts, correct native vetoes and per-case limitations |

## Improvement log

An accepted and closed improvement should append a dated entry below; retain the original problem statement above. Example format (illustration only, **not a completed action**):

| Date | Finding | Change / decision | Evidence and exact qualification | Verified by | State transition |
| --- | --- | --- | --- | --- | --- |
| YYYY-MM-DD | BA-AUD-NNN | Link to accepted ADR/PR/issue | Exact reviewed merge SHA, mandatory CI run, runtime receipt or independent approval as applicable | Named owning authority | OPEN -> VERIFIED_RESOLVED |

_No improvement entries have been verified for this register at initial creation; recommendations remain unadopted until owner triage. The README metadata correction proposed in this same documentation PR is a candidate only until merged._

## Improvement reviews

At the next assessment, compare:
- count of OPEN/TRIAGE/VERIFIED_RESOLVED and genuinely newly observed findings; do not equate fewer rows with better reliability;
- time to reproduce a real IAM/CP/engine profile and perform verified teardown;
- changed Shared contracts and consumers with actual compatibility proofs;
- applicable mandatory L4/INT/NAB real-component PASS/BLOCKED/FAIL with freshness;
- production release claims strictly limited to independently approved scopes;
- developer setup and engine onboarding time, browser completion, recovery evidence and cost per qualified capability.

[Assessment index](README.md) explains status semantics, templates and retention.
