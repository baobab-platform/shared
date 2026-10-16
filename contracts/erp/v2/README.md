# Baobab ERP posting authority v2

[ADR-SHARED-034](../../../docs/adr/ADR-SHARED-034%20%E2%80%94%20ERP%20Posting%20Authority%20Resolution%20and%20Native%20Placement%20Boundary.md)
joins Control Plane legal-actor authority to an ERP-owned native placement for
one accounting operation. `erp/v1` stays wire-compatible and unchanged.

- `posting-authority.schema.json` — `PostingAuthorityRequest` (ERP to CP at
  `/internal/erp/v1/posting-authority/resolve`, scope
  `erp-posting-authority:resolve`) and `PostingAuthorityDecision`.
- `posting-operations.yaml` — the closed catalogue of operation classes, each
  with one legal-actor role and one activity. CP derives role and activity from
  it; the caller never supplies them. Catalogue `version: 2`
  ([ADR-SHARED-037](../../../docs/adr/ADR-SHARED-037%20%E2%80%94%20ERP%20Purchase-Side%20and%20Vendor-Payment%20Recording%20Operation%20Classes.md))
  appends purchase-order, material-receipt, vendor-invoice, vendor-payment and
  payables-allocation *recording* classes; the six version 1 classes are
  unchanged. `erp.vendor-payment.record` is never money-movement authority.
- `payment-execution-evidence.schema.json` — `PaymentExecutionEvidence`
  ([ADR-SHARED-038](../../../docs/adr/ADR-SHARED-038%20%E2%80%94%20ERP%20Payables%20Recording%20Provenance%20and%20Native%20Deny-by-Name.md)):
  the independently verified fact that a vendor disbursement already happened
  outside ERP. ERP classifies an outbound payment as `erp.vendor-payment.record`
  only when it is bound to exactly one such record naming the same placement,
  payee, amount, currency and vendor-invoice obligation. The only execution
  authority is `SYNTHETIC_ENGINE_LOCAL`, so vendor-payment recording stays
  non-activatable for real placements until a revision admits a real one.
- `examples/` — synthetic fixtures for contract shape only.
  `catalogue-vectors.json` holds golden VALID/INVALID class-to-role/activity
  vectors for every catalogued class, for CP and ERP conformance tests.

The request names a workload-owned RUNTIME context, the engine instance, an
operation class, an opaque `{placement_id, placement_version}` and the exact
operation reference. It cannot select a tenant, Organisation, legal entity,
mandate, role, market or time, and carries no native client, organisation or
table identifier.

`AUTHORIZED` lasts at most 30 seconds, is bound to one operation reference and
grants nothing (`provider_permissions_granted: false`). The schema binds the
decision's role and activity to its operation class. Consumers must also apply
the semantic rules in the schema: `evaluated_at < expires_at <= evaluated_at + 30 s`
and an exact echo of the request. ERP must deny at its database COMMIT once
`min(expires_at, its own receipt time + 30 s)` has passed, and must store `decision_id`,
`mandate_id` and the placement reference with the posting so the legal actor
that applied can be answered later. Finance readiness (period, tax, baseline)
remains ERP's own check. This contract activates no workload and certifies no
posting; production stays denied.
