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


## L4-OPS-01 independent browser evidence custody increment — 2026-11-02

Infrastructure [#72](https://github.com/baobab-platform/infrastructure/pull/72) now includes a **separate independent GitHub Actions join** (`.github/workflows/dev11-evidence-join.yml`), verifier (`tests/platform-integration/development/dev11_evidence_join.py`), security/negative regression tests and an operator runbook (`docs/runbooks/dev11-l4-ops-01-independent-evidence-join.md`). This is the first independently executable evidence-custody join, **not** a successful L4-OPS-01 run.

The join requires five exact current-source GitHub Actions runs: two Infrastructure connected component proofs and one quality run each for Nabhold, ZuriBeans and Thamani. GitHub's current PR/main branch, workflow path, run SHA, run conclusion, actual named quality-test job and named test-step conclusions are checked **independently**. The corresponding run-owned artifact ZIP is downloaded privately; the SHA-256 is compared to GitHub's immutable Actions artifact digest. Incomplete or skipped owner tests, mismatched source SHAs, expired artifacts, unverified teardown and false protected-environment claims are denied. Raw screenshots, logs, request spans, cookies and credentials never enter the shared join receipt.

Native HTTP receipts must also prove real IAM/CP denial cases, current CP/Trade/BFF source pins and independent disposable teardown. Joined HTTP/estate evidence may set `join_http_and_estates_verified=true`; the **L4-OPS-01 result stays BLOCKED** until a real exported OTel graph and actual async broker/outbox/consumer business-effect/replay traces are independently qualified. Owner CI, browser test failures, and a successful GitHub job alone cannot satisfy S8 or change the Shared DEV-11 register to ACCEPTED. The join is manual `workflow_dispatch` on this development-only candidate, not falsely described as a fully deployed nightly or per-PR dispatcher.

At observation, Nabhold #99 CI run `41390782054` failed and uploaded an artifact notwithstanding unsuccessful Playwright and skipped Lighthouse/axe/visual steps. This must remain **BLOCKED** in the cross-estate join. Current-head connected Infrastructure native workflows were queued, and no unproven result has been accepted.


### Estate-owned measured-results receipts

Since the initial source audit, [Nabhold #99](https://github.com/baobab-platform/nabhold/pull/99) and [ZuriBeans #156](https://github.com/baobab-platform/zuribeans/pull/156) have been extended, and [Thamani #50](https://github.com/baobab-platform/thamani/pull/50) opened as the dedicated evidence-custody PR. The owner workflows now retain individually scoped JSON and HTML Playwright reports for functional journeys, accessibility, visual regression, Lighthouse, and Thamani logistics keyboard/browser flows. They retain real Lighthouse raw JSON and machine-readable emitted-asset budget measurements without changing thresholds.

Infrastructure #72's independent verifier *opens the source-owner artifact*, verifies its GitHub run SHA/current branch, required test job and steps, downloadable ZIP digest, non-empty passing Playwright stats, actual Lighthouse category scores/CLS/script bytes and identical fixed 800/250/64/250 KiB static budgets. The scrubbed output joins those numeric measurements with run-owned real IAM/CP and BFF/Trade authority-negative/teardown receipts; it excludes original screenshots, raw traces, credentials and payloads. A deliberately failing broker negative is not a successful consumer test. This **improves independently repeatable evidence custody**, but it is still not a completed L4-OPS-01 pass, nightly full-matrix execution, field CWV acceptance or stage/production approval.

As of this source revision the latest final-head owner and Infrastructure CI runs have not all completed successfully. This amendment does not promote the official DEV-11 implementation register beyond partial in-progress.
