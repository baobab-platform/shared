# Baobab ERP posting authority v2

[ADR-SHARED-034](../../../docs/adr/ADR-SHARED-034%20%E2%80%94%20ERP%20Posting%20Authority%20Resolution%20and%20Native%20Placement%20Boundary.md)
joins Control Plane legal-actor authority to an ERP-owned native placement for
one accounting operation. `erp/v1` stays wire-compatible and unchanged.

- `posting-authority.schema.json` — `PostingAuthorityRequest` (ERP to CP at
  `/internal/erp/v1/posting-authority/resolve`, scope
  `erp-posting-authority:resolve`) and `PostingAuthorityDecision`.
- `posting-operations.yaml` — the closed catalogue of operation classes, each
  with one legal-actor role and one activity. CP derives role and activity from
  it; the caller never supplies them.
- `examples/` — synthetic fixtures for contract shape only.

The request names a workload-owned RUNTIME context, the engine instance, an
operation class, an opaque `{placement_id, placement_version}` and the exact
operation reference. It cannot select a tenant, Organisation, legal entity,
mandate, role, market or time, and carries no native client, organisation or
table identifier.

`AUTHORIZED` lasts at most 30 seconds, is bound to one operation reference and
grants nothing (`provider_permissions_granted: false`). ERP must deny at its
database COMMIT once `expires_at` has passed, and must store `decision_id`,
`mandate_id` and the placement reference with the posting so the legal actor
that applied can be answered later. Finance readiness (period, tax, baseline)
remains ERP's own check. This contract activates no workload and certifies no
posting; production stays denied.
