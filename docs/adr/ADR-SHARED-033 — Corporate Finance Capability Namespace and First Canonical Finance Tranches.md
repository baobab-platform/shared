# ADR-SHARED-033 — Corporate Finance Capability Namespace and First Canonical Finance Tranches

**Status:** Proposed — requires Shared steward and `baobab-erp` owner review  
**Date:** 2026-10-08  
**Repository:** `baobab-platform/shared`  
**Decision ID:** ADR-SHARED-033  
**Work item:** `SH-NAB-FIN-01` (Nabhold go-live masterplan NAB-GOLIVE-MP-001, gate G03)  
**Implements:** Capability census for corporate finance in the existing `finance` namespace  
**Depends On:** ADR-SHARED-007, ADR-SHARED-011, ADR-SHARED-017, ADR-SHARED-021, ADR-SHARED-029 (form of a census decision)  
**Semantic Owner:** `baobab-erp`  
**Contract Authority:** `baobab-platform/shared`  
**First Consumer:** `baobab-platform/nabhold` (corporate workspace)

---

## 1. Decision

This ADR proposes, and does not yet register, the canonical capability keys for corporate finance. It adds **no catalogue entry, no schema, no provider declaration and no domain**. Each key below becomes canonical only through its own later contract change (section 11).

Corporate finance uses the **existing `finance` domain**. It does not create a `ledger`, `accounting` or `treasury` domain. At acceptance, the `finance` description in `namespace-registry.yaml` is widened from "invoicing, receivables and settlement" to also name ledger, payables, banking, statements, budgets and reporting. The `capabilityDomain` enum is unchanged.

Keys are proposed in three tranches, ordered by what Nabhold needs first:

| Tranche | Purpose | Proposed keys |
|---|---|---|
| F1 | A ledger that can be read and posted to, and statements that tie to it | `finance.ledger.read`, `finance.journal.manage`, `finance.statement.read` |
| F2 | Payables, receivables, cash | `finance.payable.manage`, `finance.receivable.manage`, `finance.bank-reconciliation.manage`, `finance.cash-position.read`, `finance.expense.manage`, `finance.budget.manage` |
| F3 | Reporting and group | `finance.reporting-export.create`, `finance.project-cost.read`, `finance.consolidation.run` |

Existing `finance.order-consequence.process` is untouched.

## 2. Corrections to earlier proposals

The Nabhold masterplan proposed `finance.ledger.balance.read` and `finance.intercompany.reconcile`. Neither is carried forward as written.

- `capabilityKey` is exactly three segments (`<domain>.<resource>.<action>`, `domain.schema.json`). `finance.ledger.balance.read` has four and would be rejected. The ledger read is `finance.ledger.read`; balance, entries and chart of accounts are request variants, not separate keys.
- Intercompany elimination and mirrored documents already belong to the registered `internal-trade` domain (ADR-SHARED-008, ADR-BCP-012). `finance.intercompany.reconcile` is **not** proposed here, because it would duplicate that domain. Whether ERP reconciliation of intercompany balances is a finance or an `internal-trade` capability is an open decision (section 9).

## 3. Why few keys

Operation variants and report types inside one contract, not a key per screen. `finance.statement.read` serves trial balance, income statement, balance sheet and cash flow through a `statement_type` member. A key exists only where authority, classification, or approval rules differ.

## 4. Meaning and authority

| Key | Meaning | Kind | Authority |
|---|---|---|---|
| `finance.ledger.read` | Chart of accounts, account balances and ledger entries for one legal entity, by period, currency, as-of date and posting state | Query | ERP is the system of record (`Accounting Entry`, `system-of-record.yaml`) |
| `finance.journal.manage` | Create a draft journal; submit; approve; post; reverse. Balanced debits and credits; refuses closed periods | Command, idempotent | ERP; approval authority comes from the approving principal's delegated authority, not a role string |
| `finance.statement.read` | Trial balance, income statement, balance sheet, cash flow for a period, reconciled to the trial balance (ADR-ERP-018 §54) | Query | ERP |
| `finance.payable.manage` | Supplier bills, credit notes, due dates, approval, payment preparation | Command | ERP; payment execution stays with `payment.*` |
| `finance.receivable.manage` | Customer invoices as receivables, allocation of receipts, credits, write-offs | Command | ERP; invoice **calculation** stays with `billing.*` |
| `finance.bank-reconciliation.manage` | Statement import, matching, exceptions, fees | Command | ERP; settlement facts come from `settlement.*` / `payment.*` |
| `finance.cash-position.read` | Bank and cash balance with reconciled status | Query | ERP; never derived from payment-intent totals |
| `finance.expense.manage` | Employee claims, receipts, approval, liability | Command | ERP; reimbursement execution via `payment.*` |
| `finance.budget.manage` | Cost centres, approved budgets, revisions, commitments | Command | ERP |
| `finance.reporting-export.create` | Immutable, reconciled financial snapshot with lineage, for reporting and intelligence | Command | ERP; consumers read the snapshot, never scrape ERP views |
| `finance.project-cost.read` | Cost by project or cost centre, including development cost | Query | ERP; capitalisation is an accounting policy decision, not part of the contract |
| `finance.consolidation.run` | Group consolidation with ownership, eliminations, FX and as-of | Command | A consolidation provider approved by finance; blocked until an accountant-approved group model exists |

## 5. Boundaries with neighbouring namespaces

| Concern | Owner | Rule |
|---|---|---|
| Invoice charge calculation, plans, proration | `billing` (Subscriptions) | Finance consumes the authoritative invoice; it never recomputes price |
| Payment execution, refunds | `payment` | Finance records the accounting outcome |
| Settlement batches and fees | `settlement` | Finance reconciles; it does not originate settlement facts |
| Tax determination, VAT, registration status | `tax` | Finance records tax lines as supplied. Registration is an **effective-dated tax profile**, never a constant in a key, schema or ERP code |
| Intercompany elimination and mirrored documents | `internal-trade` | See section 2 |
| Procurement documents | `procurement` | Separate decision (`SH-NAB-PROC-01`) |
| Documents and evidence | `documents` | Finance attaches by reference |
| Fixed assets, workforce, payroll, governance | not yet registered domains | Out of scope; each needs its own architecture review and ADR (ADR-SHARED-007 §11) |
| Legal-entity identity | Control Plane context | Never supplied by the caller |
| ERP engine selection of Client/Org | ERP | Native placement is not a contract field |

## 6. Common contract requirements

Every finance contract in section 4 SHALL:

1. Take the legal entity from the trusted Control Plane context. A request body SHALL NOT carry `tenant_id` or `legal_entity_id` as authority.
2. State period, as-of and currency semantics explicitly. No implicit "current" period and no unlabeled summed currencies.
3. Use the canonical decimal-string money representation; JSON floating point is forbidden (ADR-ERP-008 §28; `contracts/erp/v1/domain.schema.json` `money`).
4. Be idempotent for every command (`contracts/idempotency/v1`), return RFC 9457 problem details, and support concurrency control on mutable documents.
5. Classify its data. Financial data is restricted. Payroll detail SHALL NOT appear in any `finance.*` contract; payroll posts aggregate liabilities and expense only.
6. Separate maker from checker by canonical principal identity, not by role name.
7. Distinguish `complete`, `partial`, `stale` and `withheld` data in responses, so a caller cannot present a partial figure as a total.
8. Never expose engine, Client, Organisation or table identifiers (`contracts/erp/v1/README.md`).

## 7. Evidence at census date

Verified by reading Shared at `8487552` and `baobab-erp` at `2ef19b8`:

- `namespace-registry.yaml` registers `finance`, `billing`, `payment`, `settlement`, `tax`, `procurement`, `documents`, `internal-trade`. It does not register `asset`, `workforce`, `payroll` or `governance`.
- The catalogue carries one finance key: `finance.order-consequence.process`.
- `contracts/erp/v1/finance-baseline.schema.json` defines how other engines **refer** to an approved finance baseline; the accounting configuration itself stays in ERP.
- `system-of-record.yaml` names ERP the owner of `Accounting Entry`, `Invoice`, `Purchase Order` and `Asset`.
- `invoice-outcome.schema.json` requires `commerce_order_id`, so it describes Trade order-to-cash only (section 8).
- ERP's code covers finance baseline storage, order-to-cash and invoice/payment outcome events. It contains no ledger read, journal, statement, payable or bank-reconciliation code, and no engine-backed route has run against a live iDempiere (`architecture/conformance.yaml`).

Not verified: what iDempiere's native modules expose, because no live instance was available.

## 8. Receivables that have no commerce order

The existing `invoice-outcome` and `payment-outcome` contracts are keyed to a Trade order and a Trade-owned capture. A receivable raised from a Subscriptions invoice has neither. The F2 receivable contract SHALL therefore reference its source by a typed `source_document` (`type`, `id`, `authority`) and SHALL NOT require a commerce order. Whether `invoice-outcome` is widened or a separate receivable outcome is created is an F2 decision; it SHALL NOT silently change meaning for existing Trade consumers.

## 9. Open decisions

| # | Decision | Needed from |
|---|---|---|
| 1 | Is ERP reconciliation of intercompany balances `finance.*` or `internal-trade.*`? | Shared stewards, ERP |
| 2 | Hand-off of Subscriptions invoices to ERP: Control Plane is stated to own the hand-off. Control Plane resolves context, ERP assignment and bindings but must not carry financial payloads (ADR-BCP-007). Define exactly what "hand-off" means (routing and authority only, with the invoice itself moving Subscriptions to ERP as a canonical event) | `baobab-cp`, `baobab-subscriptions`, `baobab-erp` |
| 3 | Widen `invoice-outcome` or add a receivable outcome (section 8) | ERP, Subscriptions |
| 4 | Which statements ERP can produce natively versus through a reporting layer | ERP |
| 5 | Consolidation provider and accounting model | Finance, accountant sign-off |
| 6 | Entity registers as VAT vendor later: how the tax profile change is dated and applied | Finance, `tax` owner |

## 10. Invariants

1. Finance reports never mix currencies or periods without labelling them.
2. Posted entries are immutable; correction is by reversal or adjusting journal.
3. A closed period refuses posting unless a governed correction period exists.
4. Amount billed, cash captured, cash settled and revenue recognised remain distinct facts in distinct contracts.
5. No contract names a vendor, a tenant, a region or a country in a key. Country-specific accounting (for example South African VAT rules) is configuration behind the contract, selected through the tax profile and baseline.
6. A key is not a provider claim. Registration does not make ERP support it.

## 11. Promotion path

For each key, in its own Shared PR (`SH-NAB-FIN-02` onward, one tranche at a time):

1. Request, response, error and event schemas, examples, and negative fixtures.
2. A catalogue entry at `lifecycle = DRAFT`, `maturity = EXPERIMENTAL`, `owner = baobab-erp`, validated by `scripts/validate-capability-contracts.rb` and `capability_catalogue.py`.
3. ERP implementation and a provider-declaration entry only for operations with real routes and tests.
4. Live-provider conformance, EA-09 certification, Control Plane registration, health and binding. Each is a separate claim.

## 12. Consequences

- Positive: ERP and Nabhold can plan against stable names; the three-segment rule and the `internal-trade` overlap are caught before any code depends on the wrong names.
- Negative: nothing is consumable until F1 contracts are written, reviewed and merged, and ERP has proven a live iDempiere read and write.
- Risk: F2's receivable design touches Trade consumers of `invoice-outcome`; it needs review by every current consumer.

## 13. Next increments

1. `SH-NAB-FIN-02`: F1 contracts (`finance.ledger.read`, `finance.journal.manage`, `finance.statement.read`) with examples and negative fixtures.
2. ERP census update recording these proposed keys and the live-conformance prerequisite.
3. `SH-NAB-PROC-01`, `SH-NAB-BILL-01`, then separate namespace reviews for `asset`, `workforce` and `payroll`.

## 14. Final decision

Adopt the `finance` domain for corporate finance, accept the three-tranche key set in section 1 as the **proposed** inventory, and defer every schema, catalogue entry and provider claim to its own contract change.
