# DEV-07 workstream conformance audit — 27 October 2026

Authority: Accepted EA v2.3, EA-DEV DEV-07, the unchanged INT-05 inventory and ADR-SHARED-042/043. This is a source and evidence audit, not provider activation or protected/production approval.

## Assessment

DEV-07 is **partial**. The original 16 PASS / 9 BLOCKED native Medusa/PostgreSQL receipt remains historical and unchanged. A later eight-case IAM/CP/native-handler qualifier is a separate component proof; it does not cover BFF HTTP, RFQ/quotation, buyer commitment execution, ERP or document access. Missing providers must remain BLOCKED per operation. Neither a pure evaluator nor a SHADOW fence proves that purchasing is enforced at commit.

The audit began with Infrastructure #66 at `272a631fc19425c1e6fb0506258eeb5fe42bb099`. Its run [40484450678](https://github.com/baobab-platform/infrastructure/actions/runs/40484450678) passed actual issuer issuance/readback and CP Principal/Organisation/Market resolution, then failed `native-buyer-context`. Native fixture/token cleanup, independently witnessed CP binding revocation, native client deletion and complete labelled host teardown succeeded. Qualification stayed false.

The issuer-only correction was tested by [40490001220](https://github.com/baobab-platform/infrastructure/actions/runs/40490001220), Infrastructure `477774d0aec7cca89573c1d70dc0e6dfb96387e8`, Trade `8dad6b3def0fb309a5bb26f7073f0d1be61e3a7e`. The native-context assertion still failed. It must not be presented as a passing IAM/CP qualification. Both downloaded report/hash pairs were independently SHA-256 checked; the failed original bytes are retained under `docs/architecture/evidence/dev07-audit-2026-10-27/`.

## Source inventory

| Owner | Inspected main / reviewed source | Audit surface |
| --- | --- | --- |
| Shared | `21a8dac2d1d014321c8be676b80b81c5194c7e27` | EA/EA-DEV, ADR-042/043, original INT-05, buyer/context/RFQ/quotation contracts and DEV-07 register |
| Trade | `7cc08af7eeef15fb90abd04555032169bedad83f` | Merged #176, buyer token/assurance/context and operation policy, native identifier generation, spend/classification/fence migrations, ERP projections, documentary veto consumer and qualifiers |
| Infrastructure | `272a631fc19425c1e6fb0506258eeb5fe42bb099` | #66 source locks, actual issuer/CP composition, receipt parser, secret boundary, owner cleanup, host recovery and retained failure evidence |
| CP | `6b0ec5fa70b4ccc2b7ab9ff0cd8829a080d355ff` | Guarded development buyer fixture and owner readback; leased independent synthetic buyer Organisation and binding |
| IAM | `2ce99492d0af88e93524a28d3c9494a5770f71cf` | Native dual-grant BFF builder, separate validator ceilings and grant-derived human/workload claim normalisation |
| ZuriBeans | `dee98026e54bebb815e658c03cef32a8fa2742df` | Buyer server client, account-context selection and section/capability gating |
| ERP | `75e564e68ddeb3bd25824f99c7f55a6841456344` | Provider declaration and the distinction between order-consequence PARTIAL and stock-read implementation evidence |
| Trade Docs | `d622f541cbf545230ab000e3321f5870bc954fa9` | Runtime URLs/kernel boundary and source inventory: health/kernel scaffold, not an issuance/document-access provider |
| Regulations | `10516f9e4155bc771d0499227b5ccf4a20b28568` | Provider declaration and source inventory; its existence is not DEV-07 joined acceptance |

These immutable snapshots are not claims that unrelated files or later commits were exhaustively reviewed. Infrastructure's actual owner pins are recorded in each receipt; current main snapshots above must not be substituted for the source actually executed.

## Corrected implementation findings

| Finding | Severity | Defect and consequence | Correction / verification |
| --- | --- | --- | --- |
| D07-01 | High | `buyer-assurance.ts` rewrites an issuer through `URL.href`, while the token verifier preserves exact OIDC issuer spelling. A valid slashless Hydra issuer fails assurance. | Preserve exact configured issuer after HTTPS/credential/query/fragment/whitespace validation. Exact and alternate-spelling regression tests. |
| D07-02 | High | Native Medusa `generateEntityId` appends an uppercase ULID, while Shared buyer Organisation/membership IDs require lowercase. A newly persisted buyer cannot satisfy the context wire contract. Unit fixtures with manually lowercase IDs hid this mismatch. | The native B2B service mints lowercase opaque IDs before persistence for these two record types; preserves native single/batch overloads, receiver and transaction context. Explicit and existing IDs are not renamed. Test grammar against the pinned Shared schema and rerun actual persistence/handler CI. Existing incompatible records require governed migration before canonical handoff. |
| D07-03 | High | The policy loader drops malformed spend/approval amounts. Removing a threshold can remove mandatory approval; removing an invalid duplicate can conceal ambiguous spending authority. | Malformed monetary source returns UNAVAILABLE. Tests cover a lone malformed approval threshold, malformed duplicates and both spend-limit fields. |
| D07-04 | High | An invalid or reversed budget-balance period is filtered out as non-current, potentially treating consumed capacity as zero. | Validate periods and evaluation clock before selecting current balances; invalid periods make the budget source UNAVAILABLE. Preserve ordinary new-month zero consumption and valid historical periods. |
| D07-05 | Medium | The documentary veto consumer does not reject a non-finite evaluation clock, or a zero/reversed lease inside its clock-skew allowance. | Require a finite clock and expiry strictly after evaluation, alongside existing exact-scope/current/max-lease checks. This negative veto remains incapable of granting document or seller authority. |
| D07-06 | Medium | Infrastructure reduces a native positive-context failure to COMMAND_FAILED/ASSERTION_FAILED, obscuring the owning refusal. | Emit and release only a finite HTTP/reason diagnostic for the exact native command. Test malicious/unknown diagnostics; never expose the handler body or tokens. Remove the unused probe variable and resolve its review thread. |

Corrections are in [Trade #177](https://github.com/baobab-platform/baobab-trade/pull/177) and the existing [Infrastructure #66](https://github.com/baobab-platform/infrastructure/pull/66). Trade #176 had already merged during this audit, so the owning correction is a follow-up PR. No Shared identifier grammar, issuer trust, negative expectation, protected setting or production scope was weakened.

## Requirement-by-requirement gaps and closure evidence

| DEV-07 obligation | Current result | Required next engineering / actual proof |
| --- | --- | --- |
| Independent buyer Organisation and canonical human Principal | Owner fixture and real issuer/CP joins exist; eight-case native handoff is under repair. | All eight native cases PASS at reviewed final source, independent CP binding revocation, issuer cleanup and host teardown. Also qualify the real estate BFF HTTP path. |
| Supplier Organisation and ERP onboarding | Not joined by the buyer qualifier. Portal records/reference contracts are insufficient. | Actual independent supplier admission/linkage, owner readback, wrong-party denial and available ERP adapter execution; absent provider stays BLOCKED. |
| Market catalogue | Historical native UG/ZA public assortment proof exists. | Keep markets separate, require current clearance; add CP-bound buyer Market/local-key mapping and entitled private catalogue/pricing with foreign-buyer/Market denial. Public assortment grants no purchase permission. |
| RFQ and controlled approval | Canonical contracts and pure operation/spend policy exist; Trade declares `commercial.rfq.manage` planned and has no canonical RFQ route/lifecycle. | Persist versioned RFQs and lifecycle/outbox under current buyer/seller authority; governed approval and distinct approver checks, no grant, material edit, duplicate/replay and tenant/Market negatives. Keep binding and non-binding effects explicit under Decisions 5–7. |
| Quotation lifecycle | `commercial.quotation.manage` remains planned; no canonical Trade quotation route/lifecycle. | Exact versioned offer/validity/accept/reject lifecycle, seller/supplier authority, current approval/assurance and binding acceptance reservation lineage; no second budget consumption on order conversion. |
| Buyer commitment fencing | TA seller controls and classification/spend components exist. `Migration20261023120000` deliberately starts SHADOW and unconditionally refuses B2B authority when ENFORCED because composition is missing. | Consume matched buyer receipt, seller receipt and active hold revision in the native order transaction; authoritative gross valuation/digest; cover checkout, direct order, draft finalisation, jobs/callbacks and raw SQL, concurrency/replay/revocation. Never activate incomplete composition or reinterpret it as B2C. |
| Non-BFF commitment provenance | Accepted Decision 9 requires governed resource assignment; a Medusa server key is not estate authority. | Actual scoped CP assignment/profile resolution, withdrawal/ambiguity/Market denial, followed by the complete fence TA-08 rerun and reviewed activation/rollback. Historical TA-08 does not certify buyer composition. |
| ERP consequence | Trade has durable projections; ERP declares order consequence PARTIAL. | Actual engine-owned native order/shipment/invoice/accounting operations where supported, correct company/Organisation/legal actor and atomic/replay evidence. Projection MATCHED is not an iDempiere posting receipt. |
| Documentary/shipment access | CP negative restriction consumer exists; Trade Docs runtime currently exposes health/kernel only. | Qualified document issuance/evidence/access and shipment owner/recipient controls through actual providers; private supplier document denial and current cross-jurisdiction issuer/seller authority. `blocked=false` confers no positive permission. |
| Original INT-05 negatives | The eight-case qualifier covers identity, wrong company/audience, membership suspension, token revocation and cleanup only. | Keep all original obligations; add actual absent-grant, wrong legal actor/Market, private-price/document, duplicate/replay and jurisdiction tests to the relevant operations. No replacement scenario IDs or aggregate fake-green skip. |

The inactive fence is an Accepted Decision 9 development boundary, not itself an unauthorised drift. The defect would be claiming enforcement or activating it without completing the composition and qualification. EA-DEV explicitly permits per-operation BLOCKED for unavailable providers; those labels cannot be counted as implementation completion.

## Validation and maintenance

Local validation: 120 Infrastructure development source tests; 21 targeted Trade tests across five correction suites; 111 operation-policy/source tests including the unchanged evaluator matrix. These overlap and must not be added together as independent acceptance cases. Repository-wide final-head CI, native PostgreSQL/Medusa and genuine IAM/CP execution remain separate gates.

For every native rerun retain exact harness/head and owner pins, original sanitized report/hash bytes, image/config/lock identities, every result and independent cleanup. Preserve the 25 October receipt. A passing source/unit suite, new native ID helper or CP fixture does not close the joined runtime gate.

Rollback restores reviewed source pins and disables only the failing development profile, revokes owned credentials, verifies labelled teardown and retains evidence. Do not rename persistent buyer records, delete histories, widen credentials, disable the seller fence or enable production buying as a shortcut.

## Current runtime disposition

The final corrected candidate is awaiting a fresh native run. Until a reviewed exact-source result demonstrates otherwise: `iam_cp_native_component_qualified=false`, `bff_http_qualified=false`, `int05_qualified=false`, `provider_qualified=false`, `protected_acceptance=false`, `production_authorized=false`. This audit does not declare DEV-07 complete.
