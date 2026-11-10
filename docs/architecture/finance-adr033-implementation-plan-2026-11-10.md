# ADR-SHARED-033 — implementation and qualification register

**Architecture:** ACCEPTED 2026-11-10 by explicit Platform Owner direction. **Execution status:** PARTIAL; no real F1 provider claimed. **Baseline:** Shared main at 2a2ac16a (10 November 2026). **Semantic owner:** baobab-erp. **Financial policy sign-off:** required independently.

## Delivery ledger

| Phase | Canonical Shared contracts | ERP/consumer implementation | Qualification |
|---|---|---|---|
| F1 ledger/journal/statements | Three DRAFT/EXPERIMENTAL keys, 7 schemas, 26 example fixtures, validators and catalogue; Shared #321 | ERP currently has native financial-veto infrastructure, accounting baseline and order-consequence integrations, but no claimed F1 published provider surface | F1-P01–P11: REQUIRED_NOT_EXECUTED (source validators are not native accounting tests) |
| F2 payable/receivable/bank/cash/expenses/budget | Six names approved in census; NOT REGISTERED | Not qualified; Subscriptions-to-ERP invoice provenance undecided at operational contract level | NOT_RUN |
| F3 reporting/export/project-cost/consolidation | Three names approved in census; NOT REGISTERED | Group accounting/FX/consolidation policy approval required | NOT_RUN |

## Engineering order and proof obligations

1. **ERP F1 scoped read:** establish approved finance scope, current IAM/CP resource-server permit and authoritative ERP-book mapping. Never accept caller-provided Tenant/LegalEntity, AD_Client/AD_Org or user-asserted approver. Use native iDempiere accounting rows only, exact numeric arithmetic, explicit book/currency/period/as-of and snapshot-bound pagination. Read-only endpoints cannot post or change source accounting rows.
2. **ERP F1 journal lifecycle:** CREATE_DRAFT / SUBMIT / APPROVE / POST / REVERSE through native iDempiere GL, one authoritative transaction with persistent idempotency and version fencing. Native synchronous BEFORE veto remains mandatory; refuse closed periods, unbalanced entries, wrong currency, cross-entity, stale/missing delegated SoD and unavailable CP. Lost result adoption cannot duplicate posting.
3. **ERP F1 statements:** genuine trial balance reconciliation with source row lineage, corrected historical baselines, data completeness, explicit currency and report-policy version. Test a mismatched/incomplete statement refusal.
4. **Qualified F1:** independent F1-P01–P11 owner-JVM + PG17 tests, cross-repository IAM/CP/ERP proof, signed finance policy and results. Only then register provider support level accurately and request CP binding. Keep protected environments gated.
5. **F2:** add independent versioned schemas and negative fixtures (do not reuse the Trade-only `commerce_order_id` outcome) for Subscriptions-originated receivables and payables, then banking, expenses and budgets. Require explicit source-document authority, event producer, idempotent ERP inbox, maker/checker, payment/tax vetoes, and cross-tenant negatives.
6. **F3:** accept reporting/provenance and project-capitalisation policies and an accountant-reviewed group ownership, eliminations and FX model *before* publishing consolidation as operational capability.

## Non-negotiable proofs

- All F1-P01–P11 from [the native acceptance plan](finance-f1-provider-acceptance.yaml). No synthetic example, source-only unit pass or simulated financial transaction can fill a real native case.
- ERP period/currency/book ownership, current IAM/CP legal-actor authority, no self approval and no client-side policy assertion.
- Atomic replay/idempotency and crash-after-native-commit adoption; independent readback of posted GL and trial-balance arithmetic.
- Source-typed billing/Trade invoices must be neither silently conflated nor double-recognised. CP resolves route/authority; never carries invoice bytes as its own financial fact.
- Country rules selected by effective-dated tax policy; no guessed ZA VAT status, UG compliance or unapproved multi-entity consolidation.

## Audit and change control

This register is an engineering plan, **not** evidence of execution. Any implementation PR shall update individual cases with immutable commit, test run, artifact checksum, environment/provenance, real versus synthetic inputs, and pass/fail/blocked. Accepted ADR status is normative architecture, never an automatic release or spending authority.
