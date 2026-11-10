# ADR-SHARED-033 — Corporate Finance Capability Namespace and First Canonical Finance Tranches

**Status:** **Accepted — Normative Corporate Finance Capability Census (10 November 2026)**; operational/provider qualification remains independently gated  
**Date:** 2026-10-08; **Acceptance:** 2026-11-10, Baobab Platform Owner  
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

This accepted decision establishes the finance-domain **capability census, authority boundaries and staged promotion process**. Acceptance is not an API implementation or provider grant. F1's three keys subsequently received DRAFT/EXPERIMENTAL canonical definitions and wire schemas in Shared #321 (16 October 2026); F2/F3 remain an approved planning inventory, **not canonical registered capabilities** until individually admitted through section 11. No provider, CP binding, operational certification, posting mandate or deployment is conferred by acceptance.

Corporate finance uses the **existing `finance` domain**. It does not create a `ledger`, `accounting` or `treasury` domain. The `finance` description in `namespace-registry.yaml` has been widened from "invoicing, receivables and settlement" to also name ledger, payables, banking, statements, budgets and reporting. The `capabilityDomain` enum is unchanged.

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
| 2 | Hand-off of Subscriptions invoices to ERP. Direction from the programme sponsor (8 October 2026): `baobab-cp` owns the hand-off and ADR-BCP-007 is followed. Reading adopted here: Control Plane owns authority and routing (payer and issuer legal entity, ERP assignment, entitlement and classification, binding health, completeness and drift) and does not carry the invoice; Subscriptions emits it as a canonical event and ERP consumes it idempotently. Still open: the event contract (section 8) and how Control Plane learns an invoice was received | `baobab-cp`, `baobab-subscriptions`, `baobab-erp` |
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

**Accepted 10 November 2026:** retain the existing `finance` domain and approve the 12-key three-tranche **census** in section 1, the authority separation in sections 4–6, and the independent promotion gates in section 11. F1 is already registered at DRAFT/EXPERIMENTAL in Shared; F2/F3 are future design and implementation work, not catalogue or provider entries. Existing `finance.order-consequence.process` and the `internal-trade` domain remain authoritative. No acceptance action silently grants IAM scopes, selects a CP provider, opens a route, qualifies accounting accuracy or authorises money movement.


## 15. Engineering checkpoint — 16 October 2026

At this **16 October historical checkpoint**, the ADR was **Proposed**; the later acceptance ruling in §16 supersedes only that status, not the unexecuted provider evidence.
Shared #319 preserves the reviewed design checkpoint. The separately reviewed
Shared #321 contract change implements the section 11 **DRAFT/EXPERIMENTAL**
vocabulary and wire tranche under ADR-SHARED-017, with examples/negative tests.
Its [implementation register](../architecture/finance-f1-implementation-register.md)
tracks the distinction between source registration, semantic acceptance and
provider/native qualification. Event production and operational acceptance remain
explicit follow-ups; this checkpoint does not change an ADR's acceptance status.


## 16. Acceptance and present-day reconciliation — 10 November 2026

**Decision:** Accepted by explicit Platform Owner direction on 10 November 2026. Shared remains contract steward; `baobab-erp` remains semantic owner; Finance/accountant approval is still independently required for actual accounting policy, chart/baseline, reports, intercompany treatment and consolidation. This ruling accepts the **architecture**, not an execution permission or a claim that the unexecuted provider plan passed.

**Current source inventory:** Shared #321 merged F1 `finance.ledger.read`, `finance.journal.manage`, `finance.statement.read` with `DRAFT/EXPERIMENTAL` status, seven schemas, request/response examples and negative source conformance. The namespace description is already broadened. `finance.order-consequence.process` is a separate existing ERP capability. F2's six and F3's three names remain **census-only**, with no catalogue registration or provider claim. The 8 October census in §7 and the 16 October checkpoint in §15 are historical observations; do not interpret them as current repository state. `workforce` and `payroll` were separately admitted under accepted ADR-SHARED-045 and remain distinct from `finance`.

**Authority interpretation (resolving section 9 at architecture level, preserving domain vetoes):**

1. `internal-trade` owns the **business transaction** for intercompany/branch movement, mirrored orders and source-document identities. ERP/`finance` owns posting, balance reconciliation, ledger attribution, monetary FX treatment and financial-statement consolidation **of those transactions**. A future separately versioned finance operation may expose reconciliation, but MUST NOT duplicate or silently register `finance.intercompany.reconcile` before Shared/ERP approval of exact semantics and `internal-trade` owner review.
2. CP owns tenant/legal-actor, binding, entitlement, current payer/issuer authority **resolution and routing**. Subscriptions remains authoritative for billed subscription facts and emits a future **approved** canonical invoice event or read model; ERP ingests idempotently under CP and native posting veto. CP SHALL NOT become an invoice payload relay or originate a commercial price. The F2 receivable contract MUST accept a typed `source_document` independent of Trade `commerce_order_id`; existing Trade invoice-outcome meaning is not mutated by default.
3. Native versus reporting-layer statements, accountant-approved consolidation rules and vendor-neutral provider assignment remain **open design selections**, not provisional authorisations. Country-effective VAT/tax profiles remain owned by their actual tax authority; no default ZA/UG status is inferred from domicile or Market.

**Mandatory execution sequence and evidence boundary:**

- **F1 native first:** approve IAM resource-server scopes, CP operation grant and legal-actor/book selection, finance baseline/period policy; implement native iDempiere GL ledger, governed journal transitions and reports without bypassing the existing synchronous native veto. Prove every `F1-P01…F1-P11` case from `docs/architecture/finance-f1-provider-acceptance.yaml` on real iDempiere/PostgreSQL, including reversal/COMMIT loss/replay/SoD/closed-period negatives, independent accounting tie-out and finance sign-off.
- **F2 next:** independently version six contracts in coherent increments, starting with source-typed receivables and Subscriptions→ERP handoff, payables and banks; preserve Payment/Settlement/Tax independent authority. Complete adapter and reconciliation tests before provider promotion.
- **F3 after policy approval:** reporting snapshots require immutable provenance and restrictions; project cost requires an approved capitalisation policy; group consolidation requires an accountant-approved ownership, eliminations and FX model. Never claim native support from a schema.

**Acceptance is not activation.** Under ADR-SHARED-017, a catalogue key can be DRAFT without a provider, a provider can be implemented without certification, and certification can exist without a live CP binding or permitted production use. Protected staging/production approvals remain distinct under ADR-SHARED-036/043. See `docs/architecture/finance-f1-provider-acceptance.yaml` (status `REQUIRED_NOT_EXECUTED`) and `docs/architecture/finance-adr033-implementation-plan-2026-11-10.md` for deliverables and exit proofs.
