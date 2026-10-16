# ADR-SHARED-038 — ERP Payables Recording Provenance and Native Deny-by-Name

**Status:** Accepted — Normative Shared Contract Architecture (platform owner decision for EA-R03 increment ERP-B, 2026-10-16)  
**Date:** 2026-10-16  
**Repository:** `baobab-platform/shared`  
**Decision ID:** ADR-SHARED-038  
**Work item:** EA v2.2 EA-R03 / D-03 / LA-05, P0-04B ERP increment ERP-B  
**Depends On:** ADR-SHARED-034 (pattern and resolution, unchanged), ADR-SHARED-035 (money movement), ADR-SHARED-037 (catalogue version 2, unchanged), ADR-ERP-022  
**Semantic Owners:** Control Plane (legal authority), `baobab-erp` (native classification, provenance and accounting execution)  
**Canonical Contract:** `contracts/erp/v2/payment-execution-evidence.schema.json`; `contracts/erp/v2/posting-operations.yaml` stays at catalogue `version: 2`

---

## 1. Decision

> ERP-B SHALL implement only the five purchase-side and payables operation classes introduced by ADR-SHARED-037. Native ERP classification SHALL be directional, provenance-bound and fail-closed. Vendor-payment recording SHALL NOT initiate, instruct, approve or execute a money movement; it SHALL require independently verified payment-execution provenance. All unclassified native financial operations, including bank/cash processing, treasury movements, independent costing and payment initiation, remain DENIED.

The catalogue is frozen at `version: 2`. ERP-B adds no class, role or activity. It does not expand into general bank, cash or treasury processing to make integration acceptance easier: those need their own financial and legal decisions and a later, versioned catalogue change.

ADR-SHARED-037 §4 expected ERP-B to revise the catalogue for bank statements, cash journals, inventory, movement, production, landed cost and cost adjustment. This ADR supersedes that expectation. Those families stay denied by name (§5), and each needs its own increment.

## 2. The five families and their boundaries

| Class | Native family (iDempiere) | Boundary |
|---|---|---|
| `erp.purchase-order.complete` | `C_Order`, `C_OrderLine`, `IsSOTrx='N'` | Purchase order commitments only |
| `erp.material-receipt.complete` | `M_InOut`, `M_InOutLine`, `IsSOTrx='N'` | Goods receipt, not supplier settlement |
| `erp.vendor-invoice.record` | `C_Invoice`, `C_InvoiceLine`, `IsSOTrx='N'` | Recording a recognised supplier obligation |
| `erp.vendor-payment.record` | `C_Payment`, `IsReceipt='N'` | Recording an independently verified disbursement only (§3) |
| `erp.payables-allocation.record` | `C_AllocationHdr`, `C_AllocationLine` over authorised payables | Allocating recorded payments to supplier obligations |

- **Purchase orders and material receipts.** They are completed only under the operating legal entity's `CONTRACTING_PARTY` mandate. Source-provenance-bound lines and their ordinary accounting consequences may inherit that authority within the transaction (ADR-ERP-022 §4.2). The authority never extends to procurement configuration, production or independently initiated costing.
- **Vendor invoices.** They are recorded under `ACCOUNTING_ENTITY / VENDOR_INVOICE_RECORDING`. Invoice approval, payment eligibility and disbursement authorisation are separate decisions.
- **Payables allocations.** An allocation may join only payables and eligible recorded vendor payments. It may never create a payment, change a payment's direction or bypass the authority of the payment's origin. A vendor payment may be allocated only to the obligation its execution evidence names (§3). An allocation that mixes receivables and payables stays denied, and so does an ambiguous one.
- **`Fact_Acct`** is not an operation family. A ledger line is authorised only as a proven accounting consequence of an eligible root document, with the same attribution and COMMIT-time checks.

## 3. Vendor-payment recording requires payment-execution provenance

A CP decision for `erp.vendor-payment.record` is necessary but not sufficient. ERP SHALL classify an outbound payment into this class only when the payment is bound to exactly one **payment-execution evidence** record (`payment-execution-evidence.schema.json`) that:

1. came from an approved **execution authority** through a path the ERP runtime cannot write;
2. names the same responsible legal entity, through the same native placement;
3. names the same payee, amount and currency;
4. names the originating obligation, a vendor invoice of class `erp.vendor-invoice.record` in the same placement; and
5. is not already bound to another payment.

Positive provenance is required. The absence of a bank-statement or payment-selection reference is not enough, and neither is a payment whose fields merely look plausible. With no evidence, ambiguous evidence or evidence that no longer matches, the payment has no class. ERP denies it, at the JVM execution boundary and at the PostgreSQL COMMIT fence.

**The execution authority vocabulary is closed.** In this revision its only value is `SYNTHETIC_ENGINE_LOCAL`, for engine-local harnesses on synthetic data. A real authority, such as a Payments payout execution under ADR-SHARED-035, needs its own revision. That revision must settle the authority's money-movement decision binding, its execution observation and how ERP verifies both. Until then, **runtime activation of `erp.vendor-payment.record` stays DENIED for any protected or production placement**, even though the class is catalogued. Activation is never a flag. It needs that revision, an approved authority and the ERP evidence-ingest grant.

Recording never moves money (ADR-SHARED-037 §3). An evidence record grants nothing: it is the fact that a disbursement already happened elsewhere, never an instruction.

## 4. Bank statements never mint payment authority

A bank statement is evidence of financial activity. It is not, by itself, authority to create a payment or to start a disbursement.

| Bank-statement behaviour | ERP-B decision |
|---|---|
| Importing statement lines as externally sourced evidence | Outside ERP posting scope. Only a separately governed import workflow may do this, never iDempiere for a placed client. |
| Matching a statement line to an existing authorised `C_Payment` | A future, separately governed reconciliation capability |
| Creating a new `C_Payment` from a statement line | DENY |
| Creating an outbound `C_Payment` (`IsReceipt='N'`) from a statement | DENY, even though `erp.vendor-payment.record` exists |
| Posting bank fees, interest, adjustments or unmatched receipts | DENY until explicitly classified |
| Triggering a payment-provider or bank instruction | DENY unconditionally |

> ERP-B SHALL NOT authorise creation of `C_Payment` as a consequence of processing, completing, reconciling or posting `C_BankStatement` or `C_BankStatementLine`. `erp.vendor-payment.record` SHALL be available exclusively to a provenance-verified recording workflow for an independently authorised and executed vendor disbursement. No bank-statement-generated payment SHALL inherit this authority. The JVM execution policy and PostgreSQL COMMIT fence SHALL enforce this exclusion. All unclassified bank-statement, cash-journal and payment-creation paths SHALL fail closed.

Denying the statement header is not enough, because an iDempiere process can create `C_Payment` as a side effect. Both layers must refuse every write to the statement tables for a placed client, whichever API or background process makes it. A process that would create a payment from a statement therefore rolls back whole, including any allocation or ledger effect. The external bank evidence itself may be kept in an independently governed evidence store; denying the ERP posting does not lose it.

## 5. Denied by name

Every family below has no class. ERP SHALL refuse it for a placed client at the JVM execution boundary and, independently, in PostgreSQL. A direct SQL write by the runtime role, or a write from a background process, is refused as well.

| Native family | Reason | Future home |
|---|---|---|
| `C_BankStatement`, `C_BankStatementLine` | §4 | Bank reconciliation increment |
| `C_Cash`, `C_CashLine` | §6 | Cash-management increment |
| `M_Inventory`, `M_InventoryLine`, `M_Movement`, `M_MovementLine` | Inventory adjustment and movement | Inventory increment |
| `M_Production`, `M_ProductionLine`, `M_ProductionPlan`, BOM execution | §7 | ERP-C |
| `C_LandedCost`, `C_LandedCostAllocation`, independent `M_CostDetail`/`M_Cost`, revaluation | Independent costing (ADR-ERP-022 §4.2) | A costing increment |
| `C_PaySelection*`, online outbound payments, remittance and bank-file export | Disbursement instruction (ADR-SHARED-037 §3) | Never an ERP class |
| Treasury transfers, bank-account administration, FX transfers, payment initiation | Money movement | Payments, under ADR-SHARED-035 |
| `M_MatchPO`, `M_MatchInv` with no deterministic root | No derived-authority rule | n/a |

Derived costing proven under ADR-ERP-022 §4.2 and §4.3 stays allowed: one root, the same transaction, the same placement and the same attribution.

## 6. Cash journals

Cash journals are excluded from ERP-B, in both directions. Neither direction inherits authority from customer-payment recording, vendor-payment recording, payables allocation or general-ledger posting. `erp.gl-journal.post` never becomes a route to an unapproved cash payout.

> Cash journals (`C_Cash`, `C_CashLine`) are excluded from ERP-B's approved operation catalogue. Cash receipts and cash disbursements are distinct financial activities and SHALL NOT inherit the authority of customer payment recording, vendor payment recording, payables allocation or general-ledger posting. Any future cash-journal activation SHALL require explicit operation classes, line-level classification, independent execution provenance, applicable approval controls and transaction-level enforcement. A journal containing any unclassified or unauthorised line SHALL be denied in full.

A later cash-management increment is expected to catalogue cash receipts and cash disbursements as separate classes, each with its own activity. Transfers between tills or accounts, and cash adjustments, would each need their own class. Every line would be classified on its own, and a journal with a mixed or unknown line would be denied whole. These are expectations only. **No class name is registered here.**

Depending on configuration, completing an iDempiere payment with cash tender can write a cash-journal line. When it does, that write is denied along with the cash journal, and the payment rolls back with it.

## 7. Manufacturing is deferred to ERP-C

> Manufacturing and production operations, including `M_Production`, associated lines, BOM execution, production-derived inventory mutations, costing and accounting consequences, SHALL remain outside ERP-B. No manufacturing operation may inherit authorization from a purchase order, material receipt, sales shipment or general-ledger posting. Production execution requires an explicitly catalogued operation and independent acceptance. Unclassified manufacturing writes SHALL fail closed at both the JVM execution boundary and PostgreSQL COMMIT fence.

Receiving goods from a supplier is not the same operation as manufacturing them from components. ERP-C will need its own Shared catalogue revision and ADR. Before anything is activated, it must settle:
- production ownership;
- component traceability;
- inventory availability;
- legal authority specific to manufacturing;
- costing provenance;
- atomic acceptance tests against real iDempiere and PostgreSQL.

## 8. Acceptance

ERP-B is accepted only when it demonstrates the full payables flow without ERP becoming a disbursement engine: a supplier payable is ordered, received and invoiced, then reconciled against an independently executed and verified payment.

Its tests must prove:
- wrong-direction denial;
- cross-tenant isolation, and isolation from the wrong legal entity;
- expired authority;
- revoked mandates;
- missing, mismatched and already-bound payment evidence;
- ambiguous allocation;
- denial of bank-statement-created payments;
- denial of the families in §5;
- direct SQL bypass;
- whole-transaction rollback.

The engine-local run on synthetic data is **engine-local real-component evidence. It is not EA Gate D and not L4** (EA v2.2 §§3, 7). Under the `SYNTHETIC_ENGINE_LOCAL` authority, a recorded vendor payment proves the mechanism only. It never proves that a real disbursement happened.

## 9. Consequences

- No new class, scope, workload or grant in CP. CP keeps resolving `VENDOR_PAYMENT_RECORDING` exactly as ADR-SHARED-037 decides. Provenance is ERP's native check, alongside finance readiness, and is never a CP field.
- ERP ingests evidence only through a privileged path that the iDempiere runtime role cannot write. It binds each evidence record to at most one payment, and it re-checks the match at COMMIT.
- Protected and production posting stay denied. Vendor-payment recording stays non-activatable for real placements until §3's revision.

## 10. Not decided here

- Real execution authorities, and the Payments payout binding (ADR-SHARED-035 §2).
- Bank reconciliation, cash management, inventory, costing and manufacturing (ERP-C) classes.
- Finance capability keys (ADR-SHARED-033).
- Real mandates, placements, provider certification and production enablement.
