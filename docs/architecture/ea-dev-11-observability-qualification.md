# DEV-11 — observability and cross-estate qualification handoff

**Date:** 2026-11-02  
**Authority:** Accepted EA v2.3 / EA-DEV DEV-11; Infrastructure ADR-Infra-0016; Shared event and authority contracts.  
**Status:** SOURCE IN PROGRESS / CONNECTED QUALIFICATION BLOCKED. **Not a completion certificate.**

## Source reconciliation

- [Infrastructure #72](https://github.com/baobab-platform/infrastructure/pull/72) initially provided a closed linear five-hop diagnostic verifier, source-only CI routing and a daily *plan*; it is a draft, not a deployed trace pipeline. The companion graph extension validates branching and explicit cross-trace asynchronous links, while retaining a false `runtime_qualified` output.
- [Control Plane #458](https://github.com/baobab-platform/baobab-cp/pull/458) proposes generic request-log privacy correction (server-owned route templates and bounded fields); it is a draft and must be reviewed against current CP source.
- [Infrastructure #71](https://github.com/baobab-platform/infrastructure/pull/71) is DEV-12 PostgreSQL physical-volume start protection, **not** DEV-11 observability. It cannot be counted as trace or browser evidence.
- This Shared change defines `contracts/observability/v1/dev11-trace-evidence.schema.json` and negative schema tests. Its intentionally minimal input is **not** an OTLP, W3C, event envelope or CP authority replacement.

## Evidence boundary

The schema is an **input allowlist** for synthetic or real-component trace *projections*, not an evidence-admission policy. Every graph node is limited to controlled role, trace context, causal references, canonical correlation, event identity, boundary, and closed status/cause. This excludes paths, headers, tokens, SQL, payloads, emails and free-text diagnostics before any artifact export.

The owning verifier must additionally check: nonzero W3C IDs, unique span identities, valid same-trace parentage, unbroken graph reachability, no cycles, exact event publish/consume link and event ID, closed cause/result semantics, and source SHA. JSON Schema alone cannot prove all these cross-record invariants.

`runtime_observed` and `teardown_verified` in an input are **untrusted recorder assertions**. No `runtime_qualified`, `production_authorized` or `protected_acceptance` field is admitted in inputs. A structurally valid, all-PASS graph does **not** prove native execution or present-day CP/IAM authority.

Correlations are not privileges. Trace ID ≠ business correlation ID ≠ canonical event ID. A tenant attribute or baggage value cannot grant access. Logs and metrics must follow ADR-Infra-0016 minimisation/cardinality rules. The system must continue working if the telemetry collector fails.

## DEV-11 outstanding engineering gates

| Gate | Current finding | Owner / required proof |
| --- | --- | --- |
| S1 Closed source projection + graph negatives | Proposed in Infra #72 and this Shared contract | Infrastructure and Shared: passing final-head CI, reviewed privacy/graph negatives |
| S2 Native multi-hop tracing | Not demonstrated | BFF, IAM issuer, CP, Trade/ERP/provider, outbox: real W3C propagation including asynchronous consumer links |
| S3 Authoritative negative cases | Not demonstrated | Missing/revoked/wrong-tenant authority, invalid/missing traces, event redelivery, unknown provider, replay and expiry must remain denied |
| S4 Redaction and correlation | CP #458 proposed; cross-engine not proven | Each owner: structured bounded logging, no secrets/PII leakage, tenant-free low-cardinality metrics |
| S5 Per-PR affected-profile execution | Routing plan only | Infrastructure: dispatch actual owner workflows, record CI/run IDs and explicit BLOCKED instead of skipped-as-PASS |
| S6 Nightly/release full matrix | Scheduled plan only | Independent disposable runtime and owner workflow execution with source pins, hashes, teardown, repeatable results |
| S7 Browser and performance | Source-audited per estate, but runtime evidence not independently reconciled: Nabhold #99 is OPEN; ZuriBeans and Thamani each have Playwright/visual/axe/Lighthouse CI definitions | Nabhold, ZuriBeans, Thamani: current-head browser execution, axe/keyboard, visual regression, Lighthouse/CWV budgets and private-preview receipts |
| S8 Evidence custody and DEV-11 acceptance | Not demonstrated | Independent owner review of immutable receipts, source/config pins, privacy, negative cases and teardown; Shared register update only after actual observations |

**Canonical acceptance:** `L4-OPS-01` requires a live multi-service operation, explicit request/async lineage, safe redacted logs, failure diagnosis, reproducible source/CI context, and independently verified cleanup. Neither source graph nor successful GitHub Actions alone passes this case.

## Estate owner-source review (2026-11-02)

- **Nabhold:** [PR #99](https://github.com/baobab-platform/nabhold/pull/99) proposes additional cross-browser Chromium/Firefox/WebKit profiles, WCAG 2.2 accessibility checks, layout/visual screenshot qualification and isolated Lighthouse budgets. The PR remains **OPEN / not main**. Existing main includes Playwright public-estate, Africa footprint and security-header tests; do not mistake proposed gates for merged execution.
- **ZuriBeans:** current main contains Playwright functional, accessibility, responsive and landing-page visual tests, a performance-budget checker, and separate CI stages for Lighthouse, axe and visual regression. Current observed source is not independent L4-OPS-01 evidence.
- **Thamani:** current main includes logistics browser tests, landing-page accessibility and visual tests, a Lighthouse suite and performance-budget checker; CI names the relevant owner tasks. The source presence does not attest a current real-provider booking, CI evidence custody or independent teardown.

Each estate owns its tests and visual identity. DEV-11 Infrastructure should collect per-owner immutable run URLs, exact commit/config/browser-source pins and receipts rather than copy estate tests or invent cross-tenant authority. No budget thresholds are changed to achieve green CI.

## Next implementation sequence

1. Finish and review Infra #72 graph and CI checks; keep #71 DEV-12 separate.
2. Implement native W3C context in the appropriate runtime owners without substituting inbound headers for IAM/CP authority. Start with an IAM-issued request through CP to a real engine/outbox and consumer.
3. Capture actual positive and denied/replayed receipts with complete source pins, no raw telemetry artifacts and independent custody/teardown.
4. Connect affected-profile routing to genuine owner CI/Playwright/axe/Lighthouse execution. Refuse to mark absent external estate evidence PASS.
5. Only then reconcile the machine-readable EA-DEV DEV-11 register with observed results. Do not change protected staging/production flags.

**Rollback:** revert unmerged source branches. Never delete independently held receipts or treat a rollback as approval.
