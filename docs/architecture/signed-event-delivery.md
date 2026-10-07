# FB-04: Signed event delivery and Control Plane event ingress

Status: contract proposed with control-plane OpenAPI 1.36.0 and ERP AsyncAPI 1.1.0. Nothing is deployed or activated by it.

## Why

`com.baobab-platform.erp.provisioning.changed.v1` has been a declared contract with no operational path: ERP never emitted it and the Control Plane has no consumer. Until it travels, the Control Plane learns an ERP operation's progress only by reading it, which the contract reserves for recovery, and nothing schedules even that. There is no message broker in the ecosystem and none is needed for a handful of lifecycle events between two engines. The owner ruled (2026-10-07): signed HTTPS delivery from ERP's transactional outbox to an idempotent Control Plane event ingress, with a recovery sweep as insurance, and no broker.

## The event stays the contract

```text
provisioning.changed   canonical, transport-neutral (events/v1 envelope, erp/v1 provisioning-state)
signed delivery        one HTTPS binding for it (this document)
```

Nothing in the event depends on HTTPS. The same envelope can travel over a broker later without changing the event, its id, its payload or its consumers' logic. The ingress operation is named for what it does, receiving an engine event, not for the transport.

## The path

```text
ERP command transaction
   |-- mutate provisioning state
   '-- INSERT canonical event into ERP outbox        (same transaction)
            |
            v
   ERP dispatcher --signed HTTPS POST--> CP event ingress (receiveEngineEvent)
                                            |-- verify key, timestamp window, signature
                                            |-- validate envelope, type, producer, payload schema
                                            |-- deduplicate by envelope id (durable inbox)
                                            |-- record receipt, answer 2xx
                                            '-- apply afterwards: Worker.OnProvisioningChanged
CP recovery sweep (second line): overdue non-terminal submissions are reconciled against ERP's authoritative state
```

## Event identity (ERP)

One event per committed revision of a provisioning command. `id` is the version 5 UUID, URL namespace, of `urn:baobab-platform:event:erp-provisioning:{operation_id}:{revision}`; `idempotencykey` is `erp-provisioning-{operation_id}-r{revision}`. A redelivery, a re-publication after a dead letter is replayed, and a rebuilt outbox all produce the same event, so deduplicating by (`source`, `id`) is sound. A validator recomputes the example's id.

## Signed delivery (HTTPS binding)

`contracts/events/v1/signed-delivery.schema.json`.

```text
POST /integration/events          Content-Type: application/cloudevents+json   body: one envelope, <= 1 MiB
Baobab-Key-Id:    erp-delivery-2026-10
Baobab-Timestamp: 2026-10-07T17:30:00Z                 signing time, UTC, whole seconds
Baobab-Signature: hmac-sha256=<64 lowercase hex>
```

The signature is HMAC-SHA256, keyed with the delivery key's secret (at least 32 random bytes), over the UTF-8 string

```text
baobab-event-delivery-v1 LF baobab-control-plane LF <key id> LF <timestamp> LF <hex SHA-256 of the body>
```

(LF is 0x0A, no trailing LF.) The recipient is in the signed text, so a signature made for one consumer is worthless at another. The body digest binds the content. The key id and timestamp bind who and when. The algorithm prefix on the signature is how a stronger scheme, asymmetric keys or workload identity, is introduced later without changing the headers: only `hmac-sha256` is defined now.

The consumer checks, in this order and before it parses or stores anything: the key id is registered for the sender and not revoked; the timestamp is within **300 seconds** of its own clock; the signature matches, compared in constant time. Each delivery attempt is signed afresh, so a retry hours later is never rejected for an old timestamp. A bearer token is neither required nor accepted: the sender is an outbox dispatcher, not a workload identity. The scheme grants no scope and is accepted by exactly one operation.

### Keys

Key ids and secrets are deployment configuration, never contract. Rotation needs two active keys for the consumer at once: add the new key to the consumer, switch the sender, remove the old key after the window and the longest retry horizon pass. Revoking a key makes its signatures fail at once. A secret never appears in a log, an audit record, an error or a trace.

This is deliberately a bounded first scheme. The shared secret is the weakest part of it, which is why the algorithm is named in the signature and why the key lookup is by id: moving to rotating asymmetric or workload-identity credentials changes the key store and one prefix, not the event, the headers or the endpoint.

## Receipt semantics

At-least-once, deduplicated by the envelope's **(`source`, `id`)**, the delivery identity `envelope.schema.json` defines (two producers may legitimately reuse an id). A **2xx means the event is durably recorded**, never that it has been acted on.

| Answer | Meaning | Sender |
|---|---|---|
| 202 `ACCEPTED` | first receipt of this (source, id), recorded | delivered |
| 200 `DUPLICATE` | this (source, id) already accepted with identical content | delivered |
| 400 | malformed headers or envelope | dead-letter now |
| 401 | unknown or revoked key, stale or future timestamp, signature mismatch | retry with backoff (each retry re-signs), then dead-letter |
| 409 `EVENT_ID_CONFLICT` | this (source, id) already received with different content | dead-letter now, alert: the id is no longer a function of the change |
| 413 | body over 1 MiB | dead-letter now |
| 422 | type or producer not accepted, `source` not the producer's, or `data` fails its payload schema | dead-letter now |
| 503 | the consumer could not record it | retry with backoff |

Receipts are kept at least **seven days**, and a sender stops retrying and dead-letters an event at most **72 hours** after its first attempt, so a retry can never arrive after the consumer has forgotten the first acceptance. Re-publishing a dead letter later is a new delivery; applying an event is gated on its revision, so a late duplicate is harmless. The 200 and 202 answers each have their own schema, so `status` cannot contradict the HTTP status. No failure answer, audit record or log carries the signature, key material or event data.

## What the Control Plane accepts

`contracts/control-plane/v1/event-ingress.yaml` is a closed list: a type and producer not on it is refused with 422, and adding one is a reviewed contract change. It currently holds exactly `com.baobab-platform.erp.provisioning.changed.v1` from `baobab-erp`, which must be an ACTIVE registry type with that producer. Applying it is `Worker.OnProvisioningChanged`: validated against `erp/v1` `provisioning-state`, tied to the submission the Control Plane recorded (ERP's state carries no provisioning id), and applied only if newer. **The event is a trigger to inspect authoritative state, not the state**, and acting on it never replaces the Control Plane's own readiness checks.

An event can arrive before the Control Plane has recorded the submission it concerns (ERP accepts the request, then publishes, while the Control Plane is still recording its own answer). Such an event is **not dropped**: it stays accepted and pending in the inbox and is applied once the submission exists, or dead-lettered for operators after `pending_max_age_hours` (24).

## Recovery is not the primary path

A Control Plane sweep reconciles overdue non-terminal submissions against ERP's authoritative state. It repairs a delivery that never arrived, a long outage or a bug; it does not replace delivery, and `getProvisioningOperation` stays the recovery and reconciliation fallback.

## Delivery order and gates

1. Shared: this contract.
2. ERP: transactional outbox emission, the signed dispatcher, retry and dead-letter behaviour, metrics.
3. Control Plane: signed ingress, replay window, durable inbox, schema validation, apply.
4. Control Plane: the bounded recovery sweep.
5. A cross-repository test: ERP state, event, Control Plane convergence.

The ingress can be deployed before ERP emits anything; ERP can emit before the ingress exists (its outbox retries and dead-letters). Provisioning the delivery keys is an operator step, not part of any of these.

## Not in this contract

No broker. No activation: `baobab-cp-provisioning-workload` stays PROVISIONED, and the delivery key is not a workload credential and grants no scope. No change to `provisioning.changed`'s payload. No ordering guarantee: consumers apply by revision, never by arrival.
