# DEV-07 — Independent native commitment and consequence gate (Shared)

**Date:** 5 November 2026
**Status:** SOURCE IMPLEMENTATION CANDIDATE; **NOT** actual DEV-07/INT-05 acceptance.
**Authority:** Accepted EA v2.3, EA-DEV DEV-07, ADR-SHARED-039/042/043, Trade ADR-0019/0020, and EA-XB v1.1 accepted design. This supplements (does not supersede) the original INT-05/L4 canonical case matrix.

## Scope and ownership

Shared publishes a **development-only evidence projection** under
contracts/development/v1/dev07-transaction-readback.schema.json and an executable
conformance checker, scripts/dev07_transaction_gate.py. This adds no commercial
capability, provider, seller binding, order authority, route, event type or cross-enterprise
transaction aggregate. It does not change the incompatible historical standalone
rfq/v1 and quotation/v1 CP-minted identifier semantics; Trade-owned confidential
RFQs/quotations continue to use the Trade v1 native IDs and owner lifecycle.

Trade remains the native transaction owner, IAM the identity issuer, CP the
authoritative commercial scope and legal-actor resolver, and ERP the owner of
its native consequences. Infrastructure independently reads the native database,
joins exact owner source pins, and retains evidence. The reader SHALL NOT be
the Trade producer declaring its own success.

## Gate 2: single PostgreSQL transaction

From **one genuine non-draft Medusa order** an independent reader must show:
one committed native order with item/line rows, one ENFORCED B2B seller
decision and consumed seller authority receipt, one current buyer receipt
insertion and consumption, one committed spend reservation conversion,
and exactly one immutable original Trade outbox event. All five facts must match
the **same PostgreSQL transaction ID** and native order ID. Buyer/seller receipts
must bind the same operation reference, and the spend commitment must equal
the native final **whole buyer obligation** in minor units and currency. The
registered type is the existing com.baobab-platform.trade.order.placed.v1.
A synthetic handoff with no real order remains BLOCKED.

### Exact source compatibility (Trade #189 original PostgreSQL owner)

The field-level projection has been reconciled with the original SQL in
`baobab-trade/scripts/dev11_native_business_origin.py` and its current
native Medusa transaction-owner path. It is **not** a substitute for that
reader, a claim that the current Trade #189 source has qualified, or a new
Trade schema/authority:

- `observations.order.txid` is the native Medusa `order.xmin`;
  `native_line_count` and `native_lines_same_transaction` cover the
  independent `order_item`/`order_line_item` join and each item's `xmin`.
  A draft order or an absent item/line is never an eligible positive.
- `seller.txid` is `trade_order_commitment.xmin`;
  `seller.decision_txid` is `trade_commit_fence_decision.xmin`.
  The associated decision must be `ALLOWED`/`ENFORCED`/`B2B`, its
  classification `ACTIVE`, and the associated seller authority receipt
  actually consumed. A SHADOW decision cannot satisfy this contract.
- `buyer.txid` is `trade_buyer_authority_consumption.xmin`;
  `buyer.receipt_insert_txid` is the linked
  `trade_buyer_authority_receipt.xmin`. Both are the original event XID.
  The consumption's `seller_receipt_id` and `spend_reservation_id`
  must equal the current seller and spend facts, not unrelated valid rows.
- `spend.txid` is the `b2b_spend_ledger_entry.xmin` of a real COMMIT;
  the linked reservation must be COMMITTED, for the same buyer
  organisation and entire obligation in minor units/currency.
  `outbox.txid` is `event_outbox.native_insert_xid`, verified against
  the physical `event_outbox` and same original native XID. The tenant,
  seller legal entity, immutable event UUID and idempotency key cannot be
  silently substituted. The original persisted `envelope_digest` is
  64 lowercase hex characters; its observer presentation uses
  `sha256:<hex>` only after verifying the bytes and digest algorithm.
- The current Trade original reader exports a bounded summary including
  `business_origin.event_id`, `order_id`, `transaction_id`,
  `persisted_envelope_digest`, and `traceparent`. It does **not**
  by itself export all this schema's redacted decision/consumption facts.
  An independent, source-reviewed query and custody artifact must supply
  those extra facts. Never reconstruct them from a producer assertion.

The documented ERP #125 same-event JVM/inbox/exported-component-graph
qualification is valuable **component evidence**, but its original
`NATIVE_ORDER_ABSENT` and synthetic buyer origin do not complete this
Gate 2. Likewise, until Trade #189's genuine buyer authority and whole final
pricing—including potentially non-zero governed freight, duty, handling
and insurance—are demonstrated, a zero-extra-charge cart must not be
presented as full cross-border valuation coverage.

## Gate 3: same persisted event, never a reconstructed substitute

Publisher confirms, RabbitMQ delivery, durable ERP inbox, native iDempiere
effect and independently exported trace must be observed separately. ERP
readback must join the **original** outbox event UUID and payload digest;
native ERP effect cardinality must be one. A schema-valid declaration is not
proof that these actions actually ran. The observer's external artifact and
SHA-256, exact source revisions and receipt must be independently retrieved
and checked by the owner before any acceptance statement.

## Gate 4: closed refusal and recovery cases

The 11 required cases are wrong tenant/company, invalid audience, revoked
mandate, stale buyer authority, event payload mutation, duplicate delivery,
expired lease, simultaneous reservation, publisher outage, post-commit/pre-ACK
crash, and ambiguous ERP outcome. A PASS requires **zero prohibited effects**,
bounded retry count and either zero eligible effects for denials or exactly one
eligible business effect after authorised recovery. FAIL is a hard failure;
BLOCKED is not a PASS. No check is silently omitted. An unqualified/BLOCKED case also cannot hide
a prohibited effect, unbounded retry or excess eligible effect.

The helper distinguishes INVALID, BLOCKED, TEST_VECTOR_ONLY, and
CANDIDATE_INDEPENDENT_REVIEW. It intentionally **never** emits ACCEPTED.
Even a structurally complete real-component candidate still needs
independent live source/artifact custody, authentication and authority evidence,
original canonical-case adjudication, cleanup and owner review.

## Developer usage

Install .github/foundation-tests/requirements.txt and run:

    python3 scripts/tests/test_dev07_transaction_gate.py
    python3 scripts/dev07_transaction_gate.py path/to/redacted-observer-report.json
    python3 scripts/dev07_transaction_gate.py --require-candidate path/to/report.json

The final command refuses a blocked or test-vector report. The tests use
**invented vectors only**; no test vector or schema-valid report is real runtime
evidence. Do not store tokens, private prices, personal data or native payloads
in this public Shared repository.

## DEV-07 owner work still outstanding

- Trade #189: governed final-price reader, actual current IAM/CP buyer provider,
  enforced buyer/seller/spend native commit across checkout, direct-order and
  draft conversion; remain SHADOW until complete.
- Trade and ZuriBeans: RFQ/quotation, BFF private pricing and spend-approval
  lifecycle; no CP allocation of Trade-native RFQ IDs.
- CP, Trade, ERP and Trade Docs: independent supplier admission, vendor/Business
  Partner projection, real documentary recipient authorization and scoped
  cross-market execution; absent owners/providers stay BLOCKED.
- Infrastructure/ERP: independently verify the exact event across RabbitMQ,
  ERP inbox, native iDempiere, OTel export, 11 negatives, cleanup and final
  exact-source case matrix. Synthetic commercial facts are permitted in
  development; manufactured authority or simulated native effects are not.
- EA-XB v1.1 applies profile-specific external/bilateral evidence boundaries:
  no inference of an external buyer's ERP books and no new CrossBorderTransactionCorrelation
  registration from this DEV-07 development gate.

**Not authorised:** provider activation, protected staging/production, financial
posting inference, payments, physical delivery, or a claim of INT-05/L4 acceptance.
