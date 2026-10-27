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

Shared #405, CP #446 and IAM #139 are merged. Their reviewed heads remain
Infrastructure's exact owner pins (`2fde03e2f5f3a8a6cbc1e2081b4859fdccc1bb53`,
`695f08112898f65b17a4ec90b680720526b64dc4` and
`03d4d7c026d524a265403af9606d0b9e46f71783` respectively). Do not retain an
obsolete companion-approval hold or call those pins their merge SHAs. New
Trade #177 source remains a corrective candidate until its own review/CI.

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
| Independent buyer Organisation and canonical human Principal | Owner fixture and real issuer/CP joins exist; eight-case native handoff now has all eight cases PASS at the final corrected candidate. | Retain the exact-source eight-case proof and independent CP binding revocation/issuer/host cleanup. The real estate BFF HTTP path still requires qualification. |
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

[Infrastructure run 40492142720](https://github.com/baobab-platform/infrastructure/actions/runs/40492142720)
now proves **all eight component cases PASS** at reviewed Infrastructure head
`9ef5b5a376840041a8ea4fef868c133b9287785e`, tested merge
`e43b789b5e168c25318d3480a1f50982612b2322`, Trade owner source
`bda46ba2815f6938d8c6502f0d847e09c87c2fc6`.
Independent CP binding revocation, issuer cleanup and complete labelled host
teardown are all true. The observed run is `6fb71dc6448aef44b473e66201346e21`.

Artifact `12729580345` ZIP SHA-256:
`fa365c83860594e27b2ee8e47700febd183c07e8e57f403c4be25c9ace8d7b95`.
Original `dev07-buyer-suite.json` SHA-256:
`1fdedbd45a8080f0bc9c58b38d593f7522dc4396735850bc792f6133ea6eed73`.
Both archive and every downloaded report/hash pair were independently checked.
The original passing report/hash bytes are retained separately under
`docs/architecture/evidence/dev07-audit-2026-10-27/40492142720/`.
Earlier failed candidates and the 25 October 25-case inventory remain unchanged.

Only `iam_cp_native_component_qualified=true` is established by this new
Infrastructure observation. The nested Trade report still correctly says host
teardown NOT_OBSERVED; the Infrastructure owner supplies the independently
observed host proof. `bff_http_qualified=false`, `int05_qualified=false`,
`provider_qualified=false`, `protected_acceptance=false` and
`production_authorized=false` remain required. Final-head mandatory CI and
review remain merge prerequisites; this component proof does not declare
DEV-07 complete.

## Final source publication and merge review — 27 October 2026

All corrective source and evidence PRs are merged after final-head CI and
review, with no unresolved inline threads:

| PR | Reviewed head | Merge commit | Final checks |
| --- | --- | --- | --- |
| Trade #177 | `bda46ba2815f6938d8c6502f0d847e09c87c2fc6` | `b8164f6c3a5bd940f968194d9b74c66e05a94350` | All 34 reported checks completed with successful/applicable skipped outcomes; full core PostgreSQL regression, TA-08, build, lint/typecheck, 935 unit tests and security pass. |
| Infrastructure #66 | `9ef5b5a376840041a8ea4fef868c133b9287785e` | `0538e5040a9080a7dd9bd937bc24f2d892d6af22` | All 43 reported checks completed with successful/applicable skipped outcomes; all eight live buyer cases, existing profiles, independent cleanup and host teardown pass. |
| Shared #406 | `f714b3975ee48792bdb643ff0b6548cffaf13812` | `c1d66ee2bb63c8d0d6a9aa8757dfe8157cb0679f` | All 32 reported checks completed with successful/applicable skipped outcomes; original passing/failed evidence and audit published. |

The new Trade regression artifacts from run 40492136773 were independently
hash-checked: native B2B remains 16 PASS / 9 BLOCKED and supplemental native
buyer-context remains 11 PASS, at tested merge
`db237f9e19e273aecaf425c3689b95de1bfef1cf` of the reviewed final head.
They are separate from the original 25 October receipts and the eight-case
Infrastructure identity proof; their counts are not added to canonical INT-05.

The source/CI merge gate described earlier in this dated audit is now closed.
The next work is the actual estate BFF handoff and available supplier joins,
then canonical RFQ/quotation and atomic buyer/seller/reservation composition,
followed by qualified ERP/documentary operations. All remaining scope and
acceptance limitations in the matrix above still apply. DEV-07 remains partial.

## Implementation continuation — 27 October 2026

| Increment | Source and observed validation | Disposition |
| --- | --- | --- |
| ZuriBeans Playwright repair | [ZuriBeans #95](https://github.com/baobab-platform/zuribeans/pull/95), reviewed head `02fe651dfc4bb188317335927e5349778cf70e53`, merge `ddddd949a2dafbbe80322852e6158da75071ad7c`. Matching Playwright 1.63.0 browser revisions are explicitly installed and all three browsers must launch and render/read back a page. Zod 4.6.6 and the jsdom-scoped undici 8.12.2 patch close the high-severity dependency findings without adding suppressions. | Merged after full application/browser CI 40534946408, Foundation 40534950206, Security and remaining checks passed; the browser-image review finding is resolved. No visual baselines changed. |
| Confidential estate BFF handoff | [ZuriBeans #135](https://github.com/baobab-platform/zuribeans/pull/135), reviewed head `3f37c2a2124082afc897de1885a083fec4bae381`, merge `60750e0a1a01824ddcf380643e6419acb9232a5c`. The actual Next route uses confidential custody, origin/CSRF/body/cookie guards, independently checked human and BFF credentials and a fixed deployment-owned Trade HTTPS destination. | Merged after CI 40536013509, Foundation 40536016256, Security, compatibility and environment checks passed. The feature defaults off. Source tests and frontend CI do not establish native IAM/CP/Trade HTTP qualification. |
| Full buyer assurance policy | [Trade #178](https://github.com/baobab-platform/baobab-trade/pull/178), reviewed head `f1e9da0bbea87027c266a48410fac68e034ddd64`, merge `92762152c1efcc3b2cf58eaea9d4a59774aba9fe`. Pinned schema, exact issuer/ACR, canonical operation/profile mapping, all required methods, authentication age/step-up, policy status/effective interval and immutable revision are checked. Invalid explicit policy never falls back to the interim allowlist; contexts cannot outlive assurance freshness. | Merged after all 34 final-head checks completed successfully or with applicable skips, including 949 full-suite unit tests, formatting/lint/type-check/build, Shared conformance, the full core PG17 native regression, production infrastructure and TA-08 (CI 40535732828). No unresolved review threads. No policy, approval or operation is activated. |
| Spend/native transaction primitive | [Trade #179](https://github.com/baobab-platform/baobab-trade/pull/179), reviewed head `45917be36fe64f704440e1475d3047e523fa854b`, merge `39f5a7e0ce221f03aa60c8425600035e5bad563a`. The owner mutation can use the spend command's same connected transaction; callback/deferred-COMMIT failure rolls it all back, and replay never invokes the mutation again. A separate digest prevents capacity-only commands from pretending to have written a native resource. | Merged after all 34 final-head checks completed successfully or with applicable skips. CI 40537528782 passes the full core PG17 native regression, production infrastructure, Shared conformance and TA-08, including callback/deferred rollback, concurrent replay and MVCC transaction identity checks. No unresolved review threads. This is not receipt issuance, native order adaptation or a completed buyer fence. |

The full native buyer fence remains incomplete and inactive: it still needs
server-issued buyer receipts, the final authoritative gross valuation, both
receipt consumptions and the reservation commit bound to the same immutable
native resource/version/digest in one transaction. The transaction primitive
does not make a workflow that opens another connection atomic.

RFQ/quotation lifecycle, supplier Principal/canonical-Organisation joins and the
remaining ERP/documentary provider work stay open. In particular, the estate's
existing supplier adapter calls `POST /business-partners/project`, which is
absent from the maintained ERP server and the current Shared ERP OpenAPI. Its
ADR-ERP-021 citation describes Proposed client topology, not approval of that
route. Implement the owning supplier/vendor projection contract and adapter
before claiming this join; a non-empty `erp_*` identifier is insufficient proof.
The existing ERP customer projection is a different operation and cannot be
used as evidence for supplier-role provisioning.

All previous historical receipts and counts remain unchanged.
`bff_http_qualified`, `int05_qualified`, `provider_qualified`,
`protected_acceptance` and `production_authorized` remain false. No source/unit
or ledger-probe result is substituted for an unchanged INT-05 acceptance case.

The actual HTTP qualifier is being prepared through
[IAM #140](https://github.com/baobab-platform/baobab-iam/pull/140), which selects
only the actual estate `/api/iam/callback` in a closed development profile,
and [ZuriBeans #136](https://github.com/baobab-platform/zuribeans/pull/136),
which supplies a digest-pinned standalone source-build Dockerfile.
These preparations do not constitute an Infrastructure execution or a native
BFF HTTP receipt. The existing native-handler profile remains unchanged.
