# ADR-SHARED-037 — ERP Purchase-Side and Vendor-Payment Recording Operation Classes

**Status:** Accepted — Normative Shared Contract Architecture (platform owner direction for EA-R03 increment ERP-A, 2026-10-15)  
**Date:** 2026-10-15  
**Repository:** `baobab-platform/shared`  
**Decision ID:** ADR-SHARED-037  
**Work item:** EA v2.2 EA-R03 / D-03 / LA-05, P0-04B ERP increment ERP-A  
**Depends On:** ADR-SHARED-034 (pattern and resolution, unchanged), ADR-SHARED-035 (money movement), ADR-BCP-027, ADR-ERP-021, ADR-ERP-022  
**Semantic Owners:** Control Plane (legal authority), `baobab-erp` (native placement, classification and accounting execution)  
**Canonical Contract:** `contracts/erp/v2/posting-operations.yaml` (catalogue `version: 2`), `contracts/erp/v2/posting-authority.schema.json`

---

## 1. Decision

The closed `erp/v2` posting catalogue is revised from `version: 1` to `version: 2`. It adds five purchase-side and vendor-payment *recording* classes. Resolution, freshness, attribution, the 30-second lease and the request and decision shapes stay exactly as ADR-SHARED-034 decides. The six version 1 classes are unchanged.

| Class | Role | Activity | Meaning |
|---|---|---|---|
| `erp.purchase-order.complete` | `CONTRACTING_PARTY` | `PURCHASE_ORDER_COMMITMENT` | The buyer commits to a supplier order |
| `erp.material-receipt.complete` | `CONTRACTING_PARTY` | `GOODS_RECEIPT` | The buyer accepts delivered goods from a supplier |
| `erp.vendor-invoice.record` | `ACCOUNTING_ENTITY` | `VENDOR_INVOICE_RECORDING` | The buyer records a supplier's invoice as a payable |
| `erp.vendor-payment.record` | `ACCOUNTING_ENTITY` | `VENDOR_PAYMENT_RECORDING` | The payer records a disbursement made outside ERP |
| `erp.payables-allocation.record` | `ACCOUNTING_ENTITY` | `PAYABLES_ALLOCATION` | Payables are matched only to recorded vendor payments |

`capability_key` stays null for every class until ADR-SHARED-033 registers finance keys. A null key matches only mandates without a capability scope (ADR-SHARED-034 §5).

## 2. Role selection

The roles follow ADR-BCP-027 §6.1 and mirror the sales side:

- A purchase order and a goods receipt are contractual acts by the buyer. They use `CONTRACTING_PARTY`, as `erp.sales-order.complete` and `erp.shipment.complete` do for the seller.
- Recording a supplier invoice, a vendor payment or a payables allocation is the buyer's own bookkeeping. It uses `ACCOUNTING_ENTITY`. The buyer never *issues* the supplier's invoice, so `INVOICE_ISSUER` never applies.
- Importer-of-record, customs and declarant roles belong to Trade Docs and customs workflows. They are not inferred from a goods receipt.

Separate activities keep each mandate scope narrow. A mandate for `PAYMENT_RECORDING` (receipts) never authorises `VENDOR_PAYMENT_RECORDING`, and `PAYMENT_ALLOCATION` (sales side) never authorises `PAYABLES_ALLOCATION`. Recording money received is never permission to record money paid out (P0-04B-05 owner decision, ADR-ERP-022 §4.1).

## 3. Recording is not money movement

`erp.vendor-payment.record` records the accounting consequence of a disbursement. It never authorises, instructs or initiates one.

- A decision for this class is never money-movement authority. A Payments decision is never accounting authority (ADR-SHARED-035 §1).
- Payouts stay non-activatable in `payments/v2`. This class does not activate them and does not stand in for them.
- ERP must keep denying every native path that would *create* a disbursement instruction. That covers payment selection, payment print or export, remittance and bank transfer file generation, and online payment-processor calls for outbound payments. None of these maps to any class. A path that both records and instructs a payment is denied in full.

ADR-ERP-022 §4.1 gave `erp.vendor-payment.disburse` as an example class name. This ADR deliberately uses `…record`, so that the class name never reads as authority to disburse.

## 4. Mixed and derived writes

- **No AP/AR netting.** An allocation that joins purchase-side and sales-side documents maps to neither allocation class. ERP must deny it, because a native document that maps to no class or to more than one is denied (ADR-SHARED-034 §1).
- **Derived writes.** A native write that iDempiere makes deterministically while completing a catalogued root document may inherit that document's decision, under ADR-ERP-022 §4.2. Examples are purchase-order or invoice matching rows, receipt costing and the ledger lines the document posts. ERP proves the same transaction, the same placement and the same attribution. Every other origin of such a write stays denied.
- **Out of scope.** Bank statements, cash journals, inventory, movement, production, landed cost and cost adjustment are not catalogued here. They remain denied until increment ERP-B revises the catalogue again. Accounting configuration stays outside the catalogue (ADR-SHARED-034 §6).

## 5. Compatibility

The revision only adds classes. Version 1 consumers keep working, because a pinned consumer only ever sees the classes in its own pin.

- CP enforces class names only by pattern (`^erp\.[a-z-]+\.[a-z-]+$`). It needs no schema migration, and it derives role and activity from the catalogue it embeds.
- ERP must not classify a native document into a version 2 class until it pins this revision, and its Gate D suite covers the class.

Every decision record keeps its own `operation_class`, so historical attribution needs no catalogue version.

`contracts/erp/v2/examples/catalogue-vectors.json` holds golden vectors for each class: one valid binding and every role and activity mismatch. CP and ERP consume them as conformance fixtures.

## 6. Consequences

- No new scope, workload or grant. `erp-posting-authority:resolve` keeps its single PROVISIONED staging holder.
- CP re-pins this revision. It also requires the registered caller to hold `context:resolve`, closing the gap that CP #400 fixed for Payments.
- ERP extends its resolver, attribution and COMMIT fences to these classes. It then proves them against real iDempiere 13, PostgreSQL 17, the real CP binary and real signed workload tokens. This is **engine-local evidence on synthetic data. It is not EA Gate D and not L4** (EA v2.2 §§3, 7). L4 runs only on the Infrastructure-owned INT-01 runner.
- Protected and production posting stay denied. Activation is never a flag.

## 7. Not decided here

- Real mandates and placements.
- Finance capability keys (ADR-SHARED-033).
- Bank, cash, inventory and cost classes (ERP-B).
- Payout activation (ADR-SHARED-035 §2).
- Provider certification and production enablement.
