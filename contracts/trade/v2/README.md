# Baobab Trade order authority v2

[ADR-SHARED-039](../../../docs/adr/ADR-SHARED-039%20%E2%80%94%20Trade%20Order%20Authority%20and%20CP-Owned%20Seller%20Operating%20Bindings.md)
requires every consequential Trade operation to be classified and authorised at
its execution point, whatever API, workflow, administrator, background job or
database path starts it. `trade/v1` stays wire-compatible and unchanged.

## Files

- **`order-operations.yaml`** is the closed catalogue. Every class uses role
  `SELLER_OF_RECORD` and has its own activity. Catalogue `version: 1` makes the
  Trade-A classes activatable: `trade.order.commit`, `trade.order.create` and
  `trade.draft-order.finalize`. The Trade-B and Trade-C classes are reserved
  (`activatable: false`), so CP answers `OPERATION_NOT_ACTIVATED` for them and
  Trade refuses them by name.
- **`order-authority.schema.json`** holds two shapes:
  - `OrderAuthorityRequest`, sent by Trade to CP at
    `/internal/trade/v1/order-authority/resolve` with scope
    `trade-order-authority:resolve`;
  - `OrderAuthorityDecision`, CP's answer. `AUTHORIZED` lasts at most 30
    seconds, is bound to one binding version and one operation reference, and
    grants nothing.
- **`seller-operating-binding.schema.json`** defines the CP-owned, reusable,
  versioned Seller Operating Binding: its record, Trade's native-configuration
  attestation, the human lifecycle commands, the immutable transitions and the
  `trade.seller-operating-binding.changed` event payload. A binding is never
  scoped to a cart. It also holds binding discovery (Trade-A TA-01):
  `BindingResolveRequest`, sent to
  `/internal/trade/v1/seller-operating-bindings/resolve` with scope
  `trade-seller-binding:resolve`, and CP's recorded `BindingResolution`.
  `RESOLVED` names exactly one ACTIVE, in-effect binding version; every other
  outcome denies. Discovery is never authority.
- **`examples/`** holds synthetic fixtures for contract shape only.
  `binding-resolution-vectors.json` pins discovery precedence: zero, ambiguous,
  stale-digest and inactive matches, tenant and Organisation isolation,
  currency scope, superseded versions and effective dates.

## Ownership

CP is authoritative for:
- binding identity, scope, version and lifecycle;
- the tenant, Organisation, legal entity and market;
- the legal-actor decision.

Trade is authoritative for its native seller configuration, carried to CP only
as an opaque reference and a SHA-256 digest, and for cart and order
attribution.

## Binding lifecycle

| Step | Who acts | Result |
|---|---|---|
| Attest | Trade workload (`trade-seller-binding:attest`) | Nothing is authorised |
| Propose | Human maker | `PENDING_APPROVAL` |
| Approve | A different human checker | `APPROVED` |
| Activate | A third human operator, after CP revalidates | `ACTIVE` |
| Suspend, reinstate or revoke | Operator | `SUSPENDED`, `ACTIVE` again (a fresh activation) or `REVOKED` |

Only CP's durable commit of `ACTIVE` activates a binding. Neither the lifecycle
event nor Trade's projection is authority.

## Trade's obligations

Trade must:
- deny once `min(expires_at, its own receipt time + 30 s)` has passed;
- deny when its current native-configuration digest differs from the attested one;
- store the binding id and version and the CP `decision_id` with every committed order.

A Trade decision is never money-movement authority (`payments/v2`) and never
ERP posting authority (`erp/v2`). This contract activates no workload and
certifies no commerce. Production stays denied.

## Buyer execution context — ADR-SHARED-042 (CAA-01)

`buyer-execution-context.schema.json` is the `TradeBuyerExecutionContext`
Trade derives on the server for one buyer operation, and its
`BuyerOperationDecision`. It records the verified chain behind the decision:

- the CP human Principal and its ExternalIdentity;
- the selected, CP-attested canonical Organisation, and the Trade
  BuyerOrganisation that maps to it;
- the current BuyerMembership and its revision;
- Trade's own CP context and, for order commitment, the seller of record;
- the exact operation, resource version and transaction digest;
- the policy revision, approvals and decision.

Rules:
- **Server-built only.** No client, browser, Medusa customer JWT or job may
  submit it as a source of truth.
- **Human actors only.** Machine procurement needs its own versioned
  delegation profile (ADR-SHARED-042 section 8) before activation.
- **Bounded lifetime.** At most 60 seconds, and never later than the earliest
  evidence it rests on.
- **Not executable on its own.** `APPROVAL_REQUIRED` is not purchase
  permission. Buyer `ALLOW` executes nothing without the seller decision
  (`order-authority.schema.json`) and a native fence.
- **No probing.** Reasons about an Organisation the actor cannot act for are
  never more specific than `BUYER_NOT_AUTHORISED`.

Not yet defined, and still CAA-01 work: the buyer-authority receipt consumed at
native commit (coupled to CAA-06) and the machine-mandate delegation profile.
Run `python scripts/tests/test_buyer_execution_context.py`.
