# Baobab Payments money-movement authority v2

[ADR-SHARED-035](../../../docs/adr/ADR-SHARED-035%20%E2%80%94%20Payments%20Money-Movement%20Authority.md)
gives each consequential money movement two independent permissions: current,
operation-specific legal authority from the Control Plane, and Payments' own
financial execution approval. Both must permit. Neither overrides a denial by the
other. `payments/v1` stays wire-compatible and unchanged.

- `money-movement-authority.schema.json` — `MoneyMovementAuthorityRequest`
  (Payments to CP at `/internal/payments/v1/money-movement-authority/resolve`,
  scope `payments-money-movement-authority:resolve`) and
  `MoneyMovementAuthorityDecision`.
- `money-movement-operations.yaml` — the closed catalogue. CP derives role,
  activity and capability from it; the caller never supplies them.
- `examples/` — synthetic fixtures for contract shape, and
  `fingerprint-vectors.json`, which CP and Payments must both reproduce.

## Canonical instruction fingerprint

Payments builds the instruction from server-verified values only: the CP
RUNTIME context (tenant, operating Organisation, market), its own durable
payment records (amount, currency, payment and parent references) and its
merchant profile. Client-supplied fields are never copied into it.

The fingerprint is the lowercase hex SHA-256 of this byte string:

1. a JSON object with exactly these keys: `amount_minor`, `currency`,
   `destination_reference`, `market`, `merchant_profile_reference`,
   `operating_organisation_id`, `operation_class`, `operation_reference`,
   `parent_reference`, `payment_reference`, `tenant_id`;
2. keys in ascending code-point order, no whitespace between tokens
   (separators `,` and `:`);
3. strings as JSON strings with no escaping beyond what JSON requires
   (non-ASCII characters are written as UTF-8, not `\u` escapes);
4. `amount_minor` as a plain integer; an absent reference as `null`;
5. encoded as UTF-8.

The request also carries the instruction itself so CP can recompute the
fingerprint and check the echoed tenant, Organisation and market against the
context. A mismatch is `INSTRUCTION_MISMATCH`.

Per class: authorisation has no parent or destination; capture and void name the
parent payment; a refund names the parent payment and the destination
`ORIGINAL_PAYMENT_METHOD` only; a payout names a destination.

## Decision rules

`AUTHORIZED` is bound to one operation reference, one attempt and one
fingerprint. It lasts at most 30 seconds and grants nothing
(`provider_permissions_granted: false`). The schema binds role, activity and
capability to the class. Consumers must also check
`evaluated_at < expires_at <= evaluated_at + 30 s` and an exact echo of the
request, and must not dispatch to a provider once
`min(expires_at, own receipt time + 30 s)` has passed.

`payments.payout.execute` is catalogued with `activatable: false`. Every
decision for it is `OPERATION_NOT_ACTIVATED`, and an `AUTHORIZED` payout
decision fails the schema.

This contract activates no workload, certifies no provider and moves no money.
Production stays denied.
