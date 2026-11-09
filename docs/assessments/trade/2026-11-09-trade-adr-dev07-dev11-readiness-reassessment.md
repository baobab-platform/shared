# Baobab Trade — current ADR, capability and DEV-07/DEV-11 readiness reassessment

**Assessment ID:** BA-AUD-2026-11-09-TRADE-02  
**Observed:** 9 November 2026, Africa/Johannesburg; GitHub source and workflow metadata sampled on this date.  
**Disposition:** **ADVISORY — SOURCE IMPLEMENTATION PROGRESS, INTEGRATED ACCEPTANCE HELD.** This assessment does not accept a provider, close INT-05/L4-OPS-01, activate a commitment fence, grant buyer authority or approve staging/production.  
**Verified source baselines:** [Trade main 4c18597300d2daa44af16258046f697f3369a5fb](https://github.com/baobab-platform/baobab-trade/commit/4c18597300d2daa44af16258046f697f3369a5fb); [Shared main 4ce963d2adba4e1d441f9524d4c420be688e6120](https://github.com/baobab-platform/shared/commit/4ce963d2adba4e1d441f9524d4c420be688e6120). Candidate heads appear in §3; they are **not on Trade main**.  
**Governing decisions:** Accepted EA v2.3, EA-DEV, EA-XB v1.1, ADR-SHARED-039/042/043, actual owner ADRs and [Shared's DEV-07 independent native transaction gate](../../architecture/ea-dev-07-transaction-gate-2026-11-05.md).  
**Historical chain:** [24 October Trade ADR/capability assessment](2026-10-24-trade-adr-capabilities-readiness-assessment.md) → [27 October DEV-07 audit](2026-10-27-dev07-workstream-conformance-audit.md) → [29 October EA-XB companion](2026-10-29-ea-xb-companion-reconciliation.md) → **this snapshot**. The earlier source and runtime observations are historical, not silently refreshed.  
**Tracking:** Existing [BA-AUD-057–074](../findings-register.md), plus cross-engine IDs in the same register. No new duplicate finding ID or independent delivery programme is created.

## 1. Executive judgment

Trade has advanced from the October native-commerce/SHADOW-fence baseline to a much stronger **implementation candidate**: real Medusa/PostgreSQL transaction ownership and source-level controls, durable original-event outbox publishing and instrumentation, development buyer-context component qualification, and individual ADR correctness/remediation branches. This is materially better engineering coverage, **not** a completed governed purchase or cross-engine financial transaction.

The critical evidence boundary is still missing: **one real, authorised ZuriBeans confidential BFF checkout** with a provisioned IAM human/workload, current CP buyer/seller/Market/approval authority, actual governed cart and full final price; then one **non-draft** Medusa order, enforced seller and buyer consumptions, committed whole-obligation spend, and original immutable outbox event **independently read from the same PostgreSQL transaction ID**. The original event must subsequently be proved in RabbitMQ, ERP durable inbox, native iDempiere and independently exported distributed trace, with denial/recovery cases. Trade #189 explicitly keeps that end-to-end claim **HELD**.

**Architectural status is not runtime readiness.** The Platform Owner's 9 November directive approves previously Proposed, non-superseded Trade ADR-0023–0027 and ADR-0033–0036 as **Accepted normative architecture**, subordinate to applicable Shared decisions. The edits are recorded on the corresponding **open draft PR branches**, not yet consolidated on Trade main. They do not authorise ENFORCED mode or provider activation.

### Assurance separation at this observation

| Axis | Assessment | Evidence / limitation |
| --- | --- | --- |
| Existing native Medusa, PostgreSQL, Trade-A | **Qualified at historical bounded component scope** | [24 October snapshot](2026-10-24-trade-adr-capabilities-readiness-assessment.md) cites real Medusa/PG17 TA-08 and nonproduction synthetic receipts. No fresh rerun of those historical cases in this assessment. |
| ZuriBeans BFF→IAM/CP→Trade buyer context | **Scoped component PASS, not purchasing PASS** | [Infrastructure #67's 29 October eight-case BFF HTTP receipt](2026-10-29-ea-xb-companion-reconciliation.md) includes independent revocation and teardown; exact then-tested owner heads only. |
| DEV-11 original event transport and OpenTelemetry source | **Source merged; scoped component evidence** | Trade [#188](https://github.com/baobab-platform/baobab-trade/pull/188) is in main; the [EA-DEV register](../../architecture/ea-dev-implementation-register.md) records ERP #125's merged same-event JVM component proof. Synthetic buyer-origin evidence is not a real native buyer order or full eight-owner L4 trace. |
| DEV-07 final buyer native checkout | **Candidate; acceptance HELD** | Trade [#189](https://github.com/baobab-platform/baobab-trade/pull/189) still open/unmerged at head 4ba239eb3ac7658a72cad7b4ecb5760646cd427b. Real native non-draft test order is not the governed buyer-positive transaction. |
| Trade ADR-0007–0036 remediation | **30 draft PRs open; no merges** | [#200–#225](https://github.com/baobab-platform/baobab-trade/pull/200) and [#227–#230](https://github.com/baobab-platform/baobab-trade/pull/230), itemised in §3. #226 is the closed, unmerged duplicate of ADR-0031. PR creation is neither code merged nor requirement accepted. |
| Canonical Shared capability provider support | **Still PLANNED only** | Current [Trade provider declaration](https://github.com/baobab-platform/baobab-trade/blob/4c18597300d2daa44af16258046f697f3369a5fb/.baobab/capability-provider.yaml) has commerce.cart.manage, commercial.rfq.manage and commercial.quotation.manage under planned_capabilities, with **no providers[].support**. |
| Universal native B2B commitment fence | **SHADOW; ENFORCED not authorised** | ADR-SHARED-042 / Trade ADR-0036. A disposable test that briefly uses ENFORCED is not an operational mode change. |
| Full INT-05, DEV-07, L4-OPS-01, cross-border/provider, protected, production | **BLOCKED / NOT ACCEPTED** | No same-source, independently held complete evidence was reviewed here. Existing canonical case counts and previously blocked cases are preserved. |

## 2. Material progress since the preceding assessments

**Merged and historically qualified:** Native buyer-context components and the real estate BFF HTTP qualifier (Infrastructure #67) improved identity handoff and denial coverage, without giving the BFF permission to purchase. Trade #188 merged native HTTP/outbox telemetry and a confirmed RabbitMQ publisher with retry/reclaim, event identity and failure handling. ERP #125 is recorded in Shared's 8 November register as merged after final-head checks and independently verified earlier same-event JVM component receipts. The event and ERP receipt can be meaningful **even when their buyer-origin premise is synthetic**; that distinction must survive every assessment and dashboard.

**Trade #189 at 8–9 November:** Its PR records final valuation in integer minor units, native Medusa Order Module transaction ownership, an immutable buyer receipt/reservation/outbox composition path, source checks for original persisted event provenance, native order module PG17 regression, and a **committed non-draft PENDING test order** with independent line-item/readback and cleanup. Its 8 November head 4ba239eb3ac7658a72cad7b4ecb5760646cd427b has reported successful [native transaction workflow](https://github.com/baobab-platform/baobab-trade/actions/runs/42489784009), [Foundation](https://github.com/baobab-platform/baobab-trade/actions/runs/42489784701), [Security](https://github.com/baobab-platform/baobab-trade/actions/runs/42489784359) and [Release Readiness](https://github.com/baobab-platform/baobab-trade/actions/runs/42489783930) jobs. These checks do **not** verify live IAM/CP-bounded checkout or independently close the whole native buyer XID/ERP/trace gate.

The actual Trade main contains [tests/native-buyer-commit-route.test.ts](https://github.com/baobab-platform/baobab-trade/blob/4c18597300d2daa44af16258046f697f3369a5fb/tests/native-buyer-commit-route.test.ts), which imports a native buyer-commit route absent at the corresponding main revision. A [5 November main Foundation run](https://github.com/baobab-platform/baobab-trade/actions/runs/41999007548) was unsuccessful; this assessment does not infer a causal job diagnosis solely from the file mismatch. The absent route and current candidate composition must be reconciled, not hidden by deleting the regression. **A green individual job or PR does not confer a global baseline pass.**

**Current ADR review:** Dedicated candidate branches strengthen fail-closed market and buyer scope; native pricing/inventory/order/payment/fulfilment replay; ERP cost, tax and procurement evidence; regulatory, documentary, logistics and finance checks; ZB-04 buyer commercial activation, KYB/invitation evidence; post-CP lineage and workload provenance; and test gate cleanup. Much of the added functionality is **pure guard/kernel/source and tests**, not activated endpoints, independent provider receipts or operational qualifications.

## 3. One-PR-per-ADR implementation inventory, read 9 November

Each row is a distinct **open draft**, based on the recorded head. The text is **the change proposed by the PR**, not a statement that main now implements or that CI/real runtime accepts it. ADR numbers are the owning Trade identifiers; duplicate-number governance is addressed below.

| ADR | Trade PR | Audited change / scope | Branch state and observed head prefix |
| --- | --- | --- | --- |
| ADR-0007 | [#200](https://github.com/baobab-platform/baobab-trade/pull/200) | PostgreSQL-backed readiness fail-closed | Draft; unmerged; 2a96cc471344 |
| ADR-0008 | [#201](https://github.com/baobab-platform/baobab-trade/pull/201) | Startup/contract drift and isolation guards | Draft; unmerged; 829ddd367a5b |
| ADR-0009 | [#202](https://github.com/baobab-platform/baobab-trade/pull/202) | Legacy B2B tenancy / applicant isolation | Draft; unmerged; 7f0d2d72149b |
| ADR-0010 | [#203](https://github.com/baobab-platform/baobab-trade/pull/203) | CP Market, currency, seller execution scope | Draft; unmerged; faef4efd0082 |
| ADR-0011 | [#204](https://github.com/baobab-platform/baobab-trade/pull/204) | Confidential buyer catalogue/eligibility | Draft; unmerged; 41d2e3ab679c |
| ADR-0012 | [#205](https://github.com/baobab-platform/baobab-trade/pull/205) | Exact price variant/Market/buyer precedence | Draft; unmerged; 520b0969c977 |
| ADR-0013 | [#206](https://github.com/baobab-platform/baobab-trade/pull/206) | Native inventory scope, stock/reservation evidence | Draft; unmerged; 17165d56993f |
| ADR-0014 | [#207](https://github.com/baobab-platform/baobab-trade/pull/207) | Order idempotency and immutable facts | Draft; unmerged; af49c6073e8b |
| ADR-0015 | [#208](https://github.com/baobab-platform/baobab-trade/pull/208) | Payment replay, merchant/buyer/amount scope | Draft; unmerged; a847ba7de8e7 |
| ADR-0016 | [#209](https://github.com/baobab-platform/baobab-trade/pull/209) | Shipment replay and native fulfilment transition | Draft; unmerged; cd2e5ed759ac |
| ADR-0017 | [#210](https://github.com/baobab-platform/baobab-trade/pull/210) | Selected CP-attested buyer Organisation | Draft; unmerged; bbfcd28c1c23 |
| ADR-0018 | [#211](https://github.com/baobab-platform/baobab-trade/pull/211) | Exact tax minor units and provenance | Draft; unmerged; 148ac85880e8 |
| ADR-0019 | [#212](https://github.com/baobab-platform/baobab-trade/pull/212) | ERP purchase-order adoption with commitment proof | Draft; unmerged; 754fbd166d2d |
| ADR-0020 | [#213](https://github.com/baobab-platform/baobab-trade/pull/213) | Cost basis, ERP evidence and margin floor | Draft; unmerged; 0180cf12ff55 |
| ADR-0021 | [#214](https://github.com/baobab-platform/baobab-trade/pull/214) | Regulatory-provider evidence; no projected approval | Draft; unmerged; 2f412e797ed0 |
| ADR-0022 | [#215](https://github.com/baobab-platform/baobab-trade/pull/215) | Multi-leg transport/provider booking boundaries | Draft; unmerged; 90f9fb007599 |
| ADR-0023 | [#216](https://github.com/baobab-platform/baobab-trade/pull/216) | Supplier federation and ERP/compliance readiness | Draft; unmerged; 92ec8ee24355 |
| ADR-0024 | [#217](https://github.com/baobab-platform/baobab-trade/pull/217) | Conditional market tradeability veto | Draft; unmerged; 9f97c8081ce5 |
| ADR-0025 | [#218](https://github.com/baobab-platform/baobab-trade/pull/218) | Document provenance and qualified evidence | Draft; unmerged; 82c43c531c34 |
| ADR-0026 | [#219](https://github.com/baobab-platform/baobab-trade/pull/219) | Incoterms 2020/named-place versioning | Draft; unmerged; aa63bc5e1ca6 |
| ADR-0027 | [#220](https://github.com/baobab-platform/baobab-trade/pull/220) | Independent ERP/finance clearance receipts | Draft; unmerged; 1a9ef7081dc0 |
| ADR-0028 | [#221](https://github.com/baobab-platform/baobab-trade/pull/221) | Fresh CP workload/tenant attestation | Draft; unmerged; 96fbdb982595 |
| ADR-0029 | [#222](https://github.com/baobab-platform/baobab-trade/pull/222) | ERP profile event chronology / future-date denial | Draft; unmerged; 8973dcda2fe0 |
| ADR-0030 | [#223](https://github.com/baobab-platform/baobab-trade/pull/223) | KYB evidence integrity and duplicate-ADR crosswalk | Draft; unmerged; 0c70e2e2c76c |
| ADR-0031 | [#224](https://github.com/baobab-platform/baobab-trade/pull/224) | Finite buyer invitation expiry | Draft; unmerged; 96f4a942c324 |
| ADR-0032 | [#225](https://github.com/baobab-platform/baobab-trade/pull/225) | ZB-04 certification test/evidence separation | Draft; unmerged; 3e08ec80c9a6 |
| ADR-0033 | [#227](https://github.com/baobab-platform/baobab-trade/pull/227) | Post-CP buyer authority lineage recheck | Draft; unmerged; 9a467b22c6c8 |
| ADR-0034 | [#228](https://github.com/baobab-platform/baobab-trade/pull/228) | Exact buyer/seller Market classification scope | Draft; unmerged; c260aff85a61 |
| ADR-0035 | [#229](https://github.com/baobab-platform/baobab-trade/pull/229) | Assignment endpoint and credential fail-closed | Draft; unmerged; 1e9179c8fdc6 |
| ADR-0036 | [#230](https://github.com/baobab-platform/baobab-trade/pull/230) | Disposable regression SHADOW restoration | Draft; unmerged; 6625d7077c9c |

**CI is not uniformly green.** For example, at inspected heads: [#200](https://github.com/baobab-platform/baobab-trade/pull/200) reports failed CI/Foundation/Release Readiness (Security succeeded); [#205](https://github.com/baobab-platform/baobab-trade/pull/205) passed its dedicated pricing conformance while broader CI/Foundation/Release Readiness failed; [#213](https://github.com/baobab-platform/baobab-trade/pull/213) reported failed broad CI/Foundation/Release Readiness; [#223](https://github.com/baobab-platform/baobab-trade/pull/223) had its latest CI running and Foundation queued with Release Readiness failed; [#228](https://github.com/baobab-platform/baobab-trade/pull/228) reported CI/Release Readiness failed with Foundation queued; and [#230](https://github.com/baobab-platform/baobab-trade/pull/230) had CI running and Foundation/Security queued with Release Readiness failed. These are **time-scoped observations**, not timeless claims; recheck each final head before any merge. Do not assume shared baseline defects excuse unrelated changes.

### ADR status, precedence and duplicate identifiers

- **ADR-0023–0027:** Source previously labelled Proposed; Platform Owner accepted normative decisions on 9 November. Accepted status edits and honest engineering ceilings are on draft [#216–#220](https://github.com/baobab-platform/baobab-trade/pull/216), not Trade main.
- **ADR-0033–0036:** Platform Owner accepted their Trade implementation records on 9 November, governed by already Accepted **ADR-SHARED-042**. Status edits remain on draft [#227–#230](https://github.com/baobab-platform/baobab-trade/pull/227). **ADR-0036 acceptance is NOT a vote to flip SHADOW to ENFORCED.**
- **ADR-0008:** Historical document has its own Normative wording; do not silently convert that wording into a verified implementation status.
- **Two ADR-0029s:** ZB-03.7 real-token integration verification **and** ZB-04 ERP commercial-profile consumption. **Two ADR-0030s:** ZB-06 product/Market assortment **and** ZB-04 buyer KYB. Each is a separate already Accepted decision. The four-way gate-qualified identifier crosswalk is **proposed on #223** at docs/development/ADR-0029-0030-numbering-crosswalk-2026-11-09.md. Do not claim it is already merged into main or renumber historical references without a formal index migration.
- **PR #226:** accidental duplicate ADR-0031 candidate, closed **unmerged**. The active ADR-0031 candidate is **#224**. This is 30 distinct active PRs for ADR-0007–0036, not 31.
- **ADR-0001–0006 and the ADR-0018 tax addendum:** Remain historical/owning material in the [24 October census](2026-10-24-trade-adr-capabilities-readiness-assessment.md); this focused 30-PR pass is **not** their fresh conformance certification.

## 4. DEV-07/DEV-09/DEV-11/DEV-12/DEV-14 connected gate disposition

| Gate / owner | What was demonstrably achieved | Still required to claim completion |
| --- | --- | --- |
| **Identity and buyer context** — IAM, CP, ZuriBeans, Trade | 29 October BFF HTTP eight-case synthetic real-component qualifier; Trade buyer lineage and Market guards proposed #227/#228. | Current final-head run-private real IAM issuer and CP human/workload/Organisation/Site/Market/mandate; approved signer/budget; fresh revocation and cross-tenant negatives; independently witnessed current BFF checkout, not context only. |
| **Gate 1: original event to ERP native JVM** — ERP #125, Trade #188/#189, Infrastructure | ERP #125 merged source plus earlier independently checked **same-event JVM component** evidence; durable inbox, native effect, duplicate/lost-result adoption are bounded in that source scope. | Join the **genuine current governed buyer-origin** event to this exact original outbox UUID, publisher, RabbitMQ, inbox, JVM effect and exported trace with current source pins. Synthetic origin must remain denied by the buyer-origin verifier. |
| **Gate 2: native Trade buyer commitment** — Trade #189 | Non-draft **test** Medusa Order Module PG17 commit/readback plus stronger buyer receipt/valuation and transaction primitive. Source/CI work is substantial. | Independent same-XID readback of actual governed Medusa **buyer** order + ENFORCED seller consumption + buyer receipt insertion/consumption + committed spend ledger + original outbox, including idempotent replay, crash/recovery, currency and non-zero freight/duty/handling/insurance policy, not just zero-charge test fixtures. |
| **Gate 3: end-to-end observability and transport** — Trade #188, Infrastructure #72, ERP #125 | Native events/OTLP and confirmed publisher with durable evidence and component test workflows; Infrastructure #72 and full connection remain separate work. | Run one original event through all owner boundaries and independently export/reconcile the W3C parent/causal graph, source/event IDs, original payload digest, retry/DLX diagnostics, and native ERP effects. |
| **Gate 4: adversarial and recovery** — Trade/ERP/Infrastructure | Existing source and negative test suites, including branch-level improvements. | Qualify eleven [Shared Gate 4 denial/recovery cases](../../architecture/ea-dev-07-transaction-gate-2026-11-05.md) with zero prohibited effects and exact-at-most-once eligible effect; independently retained immutable evidence and teardown. |
| **RFQ, quotation, supplier, document and compliance** — Trade/ERP/Docs/Regulations | Separate native/customer/supplier and document/compliance policy scaffolds; drafts #216–#220 add source guards. | Trade-owned Trade v1 confidential RFQ and versioned quotation lifecycle; supplier's genuine CP/IAM identity and ERP vendor record, real documentary custody/version/recipient grant, qualified regulatory provider and current provider negatives. The older standalone RFQ identifier contract is distinct. |
| **Shared canonical and CP capability support** — Shared/Trade/CP | Three exact catalogue intentions recorded, not support. | Exact canonical operation conformance, qualified consumer and owner/CP provider registration and rights. No auto-promotion from native operation families. |
| **Protected acceptance** — Infra/Security/Platform Owner | No new protected approval. | Independent staging-authorised issuer/keys, separation of migration/runtime DB roles, source/image custody, durable negative/recovery and rollback approvals. **Production is a separate future gate.** |

**EA-XB:** Accepted design and TMS's earlier native source components do not imply an executed AGR, MFG, NET, LOG or CORE cross-border business case. Keep the existing 30-case design executions NOT_RUN until each owning proof exists. **Thamani B2B logistics** remains distinct from Trade's historical Thamani B2C retail module.

## 5. BA-AUD-057–074 review and priority corrections

The [findings register](../findings-register.md) retains every original ID, owner, closure test, severity and **24 October status**. No finding is marked VERIFIED_RESOLVED merely because a draft PR exists. This snapshot adds **dated progress annotations**:

| Finding IDs | 9 November interpretation / next independent action |
| --- | --- |
| **057, 063, 074** — canonical capabilities / transparency | Still OPEN/TRIAGE: three planned-only catalogue keys; PRs do not implement registered exact Shared quick-order/RFQ/quotation lifecycle. Publish only evidenced per-capability status. |
| **058, 059, 060, 064, 071** — buyer/Market/workload/native transaction | **P0 active engineering; acceptance OPEN**. Prior BFF component receipt and draft #203/#210/#227–#230 plus #189 reduce source gaps but no final same-XID governed buyer proof. Keep SHADOW. |
| **061, 067, 068, 073** — CI, protected environment, privileged roles and recovery | **Unclosed**. Old TA-08 scope remains historical, varied current CI failures and queued jobs prohibit blanket merge readiness, and protected role/failover/effect-denial proof is still owed. |
| **062, 072** — ZB-04 and duplicate ADR governance | **In progress, not closed**. Draft #222–#225 adds dated ERP/KYB/invitation and verification guards; #223 crosswalk gives safe aliases but is not merged or a renumbering authority. ZB-04 real provider certification still unexecuted. |
| **065, 070** — native providers / cross-engine consequences | Source-level and same-event JVM **component** progress (#188, ERP #125), but provider-neutral ERP/document/finance/PSP/carrier proof and actual original buyer event remain OPEN. |
| **066** — Thamani business scope | Still TRIAGE: historical retail implementation must not be counted as current B2B logistics/TMS qualification. |
| **069** — Shared pin/compatibility | OPEN. Reconcile updated Trade #189, 30 ADR branch heads, and Shared/CP/IAM/ERP ownership **before** relying on one merged integration source. No invisible pin update. |

### Required engineering sequence, without weakening historical gates

1. **Reconcile CI and branch composition.** Diagnose main's orphan native buyer-commit test, then rebase/order 30 isolated ADR candidates against their actual shared touchpoints, eliminate PR-specific failures, preserve security negatives and obtain **final-head** CI and review. PR count is not merge count.
2. **Finish one genuine buyer transaction on #189.** Run-private buyer/cart/budget/current-CP signer; independently witnessed same-XID seller/buyer/spend/order/outbox; test whole invoice with governed non-zero charges and refusal/recovery before enabling buyer checkout.
3. **Attach the already-owned event transport and ERP effects.** Reuse #188's RabbitMQ/OTLP architecture and ERP #125, complete Infrastructure #72 independent original-event proof and eleven closed negatives. Do not reimplement a parallel event path.
4. **Complete actual operations in sequence.** Trade native RFQ/quotation, supplier-to-ERP Business Partner, document/compliance provider custody, finance and logistics; then canonical Shared support qualification and external customer/cross-border profiles.
5. **Keep protected controls independent.** Any proposal to change the universal fence from SHADOW requires its own Platform Owner approval, independent CP/IAM conformance, privileged role and rollback drills. No assessment, CI result or accepted ADR automatically flips the switch.

## 6. Evidence integrity, observation limits and next reassessment

This snapshot read repository files, pull request metadata and selected GitHub workflow conclusions; **it did not independently execute** a current combined Medusa/CP/IAM/ERP/Infrastructure runtime, download/rehash the latest broker/ERP/trace artifacts or witness protected deployment. Older successfully retained and verified artifacts are cited **as dated prior audits**. CI state can change after this observation; an open PR can change head without changing its number. Exact heads and artifacts must be reacquired at review.

**Next review triggers:** #189's independently signed native positive and original-event custody; final-head CI+merge for the relevant ADR candidates; updated Shared consumer/CP provider binding; ZB-04 real provider environment suite; current DEV-07/11 canonical case adjudication; or separately authorised protected readiness.

**Exit conclusion:** Trade is **engineering-progressing, component-qualified in bounded places, and not yet end-to-end business-execution accepted**. All independent buyer purchase, external provider, release and production barriers remain explicit.
