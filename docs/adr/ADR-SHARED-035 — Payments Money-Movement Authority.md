# ADR-SHARED-035 — Payments Money-Movement Authority

**Status:** Accepted — Normative Shared Contract Architecture (platform owner decision, 2026-10-14)  
**Date:** 2026-10-14  
**Repository:** `baobab-platform/shared`  
**Decision ID:** ADR-SHARED-035  
**Work item:** P0-04B Payments execution-point enforcement (EA v2.1 EA-R03, D-03; CP completion plan §8, L457)  
**Depends On:** ADR-SHARED-011, ADR-SHARED-034 (pattern), ADR-BCP-026, ADR-BCP-027, ADR-PAY-0002, ADR-PAY-0010, ADR-PAY-0013, ADR-PAY-0016, ADR-PAY-0018, ADR-PAY-0022  
**Semantic Owners:** Control Plane (legal authority), `baobab-payments` (financial instruction, approval, readiness and execution)  
**Canonical Contract:** `contracts/payments/v2/money-movement-authority.schema.json`, `contracts/payments/v2/money-movement-operations.yaml`

---

## 1. Decision

Every consequential money movement needs two independent permissions at the moment it is executed:

| Layer | Decides | Owner |
|---|---|---|
| Legal authority | Whether the responsible legal entity, operating Organisation, principal and applicable mandates may undertake this financial activity, in this market, through this engine instance | Control Plane |
| Financial execution approval | Whether this particular movement is financially valid, approved, compliant, executable, provider-ready and safe to submit | Payments |

Both must permit. Neither can override a denial by the other. CP never executes a payment and never decides the underlying commercial obligation (ADR-PAY-0002 §4).

The governing rule:

> Every independently initiated, consequential money movement must have current, operation-specific legal authority from CP and independent financial execution approval from Payments. Accounting authorization, group ownership, historical approvals and absence of restrictions never imply permission to move funds.

Consequences of the rule:

- **Collection is not disbursement.** Permission to collect money never authorises paying it out (ADR-PAY-0016).
- **Accounting is not money movement.** An `erp/v2` `erp.payment.record` decision (`PAYMENT_RECORDING`) authorises an accounting record only. It is never authority to capture, refund or pay out, and a money-movement decision is never accounting authority.
- **A negative-only documentary check is a veto, not a grant.** An unblocked response never means approved to transfer.
- **Group ownership is not a mandate.** One company cannot move funds through another group company's merchant or funding account.

## 2. Operation classes

`money-movement-operations.yaml` is a closed catalogue:

| Class | Activity | Role | Capability | Status |
|---|---|---|---|---|
| `payments.authorization.create` | `PAYMENT_COLLECTION` | `PAYMENT_BENEFICIARY` | `payment.payment.authorize` | Activatable |
| `payments.capture.execute` | `PAYMENT_COLLECTION` | `PAYMENT_BENEFICIARY` | `payment.payment.capture` | Activatable |
| `payments.refund.execute` | `PAYMENT_REFUND` | `PAYMENT_BENEFICIARY` | `payment.refund.create` | Activatable |
| `payments.authorization.void` | `PAYMENT_VOID` | `PAYMENT_BENEFICIARY` | `payment.intent.cancel` | Activatable |
| `payments.payout.execute` | `BENEFICIARY_DISBURSEMENT` | (decided at activation) | (none) | **Not activatable** |

The merchant of record that receives funds is the `PAYMENT_BENEFICIARY`; it also returns them on refund or void. The decision schema binds each class to exactly its role, activity and capability.

A payout is catalogued only so every route to it is denied by name. CP answers `OPERATION_NOT_ACTIVATED` before any mandate lookup, and an `AUTHORIZED` payout decision fails the schema. Activating payouts needs its own revision. That revision must settle:
- the payer role;
- beneficiary and destination verification;
- the approved obligation;
- maker-checker approvals;
- the funding source;
- an eligible payout provider (ADR-PAY-0016).

Creating a payment intent, reading status, receiving a webhook and recording an accounting consequence are not money movements and need no decision here. They keep their own authentication, permission and provenance checks, and must never become an indirect route to a transfer. Treasury transfers are out of scope and need a separate authority architecture. Chargebacks and provider-initiated reversals are P1.

## 3. Instruction binding

Payments builds an immutable instruction from server-verified values only:
- the CP RUNTIME context (tenant, operating Organisation, market);
- its own durable records (amount, currency, payment and parent references, destination);
- its merchant profile.

The **instruction fingerprint** is the SHA-256 of a canonical encoding of those values plus the operation class and reference (README). CP recomputes it, checks the echoed context fields, and records it with the decision. Changing the amount, currency, merchant, payer, beneficiary, destination or parent payment changes the fingerprint and invalidates the decision. A refund may only return funds to the original payment method.

## 4. Resolution

`MoneyMovementAuthorityRequest` names a workload-owned RUNTIME `context_id`, the `engine_instance_id`, an `operation_class`, the `operation_reference`, an `attempt`, the instruction and its fingerprint. CP:

1. refuses a non-activatable class (`OPERATION_NOT_ACTIVATED`);
2. redeems the context for the calling workload (owner, RUNTIME purpose, expiry, active tenant);
3. checks the instruction echoes the context and the fingerprint recomputes, else `INSTRUCTION_MISMATCH`;
4. requires the engine instance to be bound to the tenant's Payments capability, else `ENGINE_INSTANCE_NOT_BOUND`;
5. derives role, activity and capability from the catalogue and resolves the mandate with the existing legal-actor semantics (an exact match is required; more than one match is `AMBIGUOUS`; revoked, expired or unverified fail closed);
6. persists an immutable decision record and returns its `decision_id`.

`AUTHORIZED` expires at most 30 seconds after evaluation and never after the context or mandate. It is bound to one operation reference, one attempt and one fingerprint, and it grants nothing (`provider_permissions_granted` is always `false`).

## 5. Execution protocol

Payments and an external provider cannot share one database transaction, so Payments does not claim distributed atomicity. It must prove this protocol instead:

1. Authenticate the workload and resolve current CP authority (attempt 1).
2. Validate the instruction and the independent provider readiness (ADR-PAY-0022).
3. Durably reserve the operation and its idempotency identity in PostgreSQL, with the decision.
4. Re-validate CP authority, documentary restriction and readiness at the execution point (a fresh decision for attempt 2).
5. Durably record the dispatch attempt, then dispatch the uniquely identified provider operation once.
6. Record the provider observation and its immutable evidence.
7. Reconcile an unknown outcome with the provider before any retry. A dispatch with no recorded outcome is treated as possibly executed, never re-sent blindly.
8. Publish canonical results through the transactional outbox.

Payments must refuse to dispatch once `min(expires_at, own receipt time + 30 s)` has passed. A revocation before the final dispatch therefore prevents it. A request that has already crossed the execution boundary is reconciled, not presumed undone. Payments stores `decision_id`, `mandate_id`, the responsible legal entity and the fingerprint with the reservation and the dispatch, so the legal actor for each movement can be answered later (ADR-BCP-027 §10.2).

## 6. Proof gates

| Gate | Proves |
|---|---|
| A–C | Contract, unit, PostgreSQL fence and integration tests on every PR |
| **D1** | The real Payments service through its HTTP handlers, the real CP resolver, real signed workload tokens, PostgreSQL 17 with the restricted role, and a deployed HyperSwitch with a controlled test connector run the protocol end to end. This includes revocation, readiness withdrawal, replay, payout denial and a crash between provider acceptance and persistence. |
| **D2** | The same flow in protected staging with independently approved PSP sandbox credentials, real IAM, webhook and reconciliation evidence |
| **E** | Provider certification, production operations, recovery and formal activation approval |

Neither D1 nor D2 activates production. Public money routes stay fail-closed in protected environments until a separate, explicitly approved activation change. That change is never a feature flag.

## 7. Consequences

- The scope `payments-money-movement-authority:resolve` is workload-only and non-authorising. It is granted only to the PROVISIONED Payments staging assessor; no workload is activated by this ADR.
- CP implements the resolver in nonproduction environments behind an explicit flag and client allowlist.
- Payments implements the protocol, its own financial checks and PostgreSQL fences. Execution correctness is certified only by Gate D1 or later, never by contract or synthetic tests.

## 8. Not decided here

- Payout activation and its payer role.
- Real mandates and merchant certification; IAM workload activation.
- Provider certification; production enablement.
