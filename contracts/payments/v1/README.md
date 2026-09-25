# Payment Contracts (`payments/v1`)

**Governing ADRs:** ADR-SHARED-011 (this repository); ADR-PAY-0001 (`baobab-platform/baobab-payments`)
**Contract authority:** `baobab-platform/shared`
**Runtime authority:** `baobab-platform/baobab-payments`

The Baobab Payment API. HyperSwitch is an implementation detail behind it: a Baobab payment is not a HyperSwitch payment, and no HyperSwitch object is part of this contract.

## Files

| File | Contents |
|---|---|
| `domain.schema.json` | Identifiers (`payint_`, `pay_`, `refund_`), currency, the intent, payment and refund status vocabularies, capture method, provider kinds |
| `payment.schema.json` | `PaymentContext`, `Money`, `CreatePaymentIntentRequest`, `PaymentIntent`, `ConfirmPaymentIntentRequest`, `Payment`, `CapturePaymentRequest`, `CancelPaymentRequest`, `CreateRefundRequest`, `Refund`, `ProviderResult` |
| `events.schema.json` and `asyncapi.yaml` | `payment.created`, `.authorized`, `.captured`, `.failed`, `.cancelled` and `.refunded` |
| `capabilities.json` | The engine's capability registration: `payment.intent.create`, `payment.payment.authorize`, `payment.payment.capture` and `payment.refund.create`, provided by the simulated `baobab-payments.sandbox` |

## Rules the schemas enforce

- **The payment context is resolved.** Tenant, legal entity, market, currency, source engine and reference, and correlation come from a workload acting on Control Plane-resolved context. The payment engine never decides them.
- **No card or credential data.** Payment methods are opaque, already-tokenised references.
- **Sandbox results are always `simulated: true`**, and real-provider results are `simulated: false`. Every payment event requires `simulated`, so a sandbox outcome is never mistaken for settlement.
- **Events are emitted only for state that occurred.** They carry identifiers and state, never reasons, descriptions or payment-method references.

Money-moving requests (create intent, confirm, capture, refund) take an `Idempotency-Key`. A retry never duplicates an intent, payment or refund. The amount's currency must equal the context currency; `baobab-payments` enforces this.
