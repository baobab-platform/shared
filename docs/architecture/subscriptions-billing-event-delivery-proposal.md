# SUB-02 billing event delivery decision proposal

Status: **Proposed for Shared #418.** The existing Subscriptions publisher remains pre-activation. This proposal changes no event, scope, workload or ingress registry.

## Receiver and event purpose

Use a dedicated, signed HTTPS Control Plane receiver for billing lifecycle observations. Four low-volume lifecycle messages can use the bounded delivery and durable receipt semantics already specified by FB-04. The receiver belongs to a CP operational read model and uses a dedicated path, signing recipient and keyring. The ERP provisioning ingress keeps its existing allowlist.

| Subscriptions event | Proposed destination and purpose |
| --- | --- |
| billing-subscription.created | CP billing observation. Reconcile the observed projection to its known ProductSubscription. |
| billing-subscription.suspended | CP billing observation. Show the current billing condition and reconcile against Subscriptions. |
| billing-subscription.resumed | CP billing observation. Refresh the condition from Subscriptions. |
| billing-subscription.terminated | CP billing observation. Preserve the terminal observation and reconcile against Subscriptions. |
| usage.recorded | Subscriptions metering custody only for this increment. External delivery awaits a named consumer and a separately reviewed purpose and minimisation policy. |

Each observation is advisory for CP billing operations. ProductSubscription state, entitlements, billing instructions, invoice posting and payment decisions follow their existing owning contracts. Subscriptions must select the four exact types before attempting delivery. An unselected usage row requires an explicit local disposition and stays available for authorised metering and audit. It cannot become acknowledged external delivery.

An event broker remains a possible later binding if fan-out or throughput calls for it. Broker publisher confirms and consumer acknowledgements cover different steps. Either binding still needs an independently verifiable durable consumer receipt.

## Publisher and receiver trust

Propose an independent development publisher workload `baobab-subscriptions-billing-events-development` with exact audience `baobab-subscriptions` and a dedicated workload-only scope `billing:events:dispatch`. The Subscriptions worker validates current IAM status and exact client, audience and scope before claiming a tenant outbox row. Tenant admission stays a separate current control. The current `events:publish` scope has the `event-broker` audience. Replace the pre-activation worker's hard-coded broker audience through a reviewed companion change before connecting this direct transport. The production payments workload keeps its separate identity and purpose. Shared and IAM must approve a credential profile and demonstrate issuance, revocation and rotation for the publisher before any lifecycle is activated.

The CP receiver authenticates the request with the signed HTTPS delivery binding. It checks an independently provisioned key assigned to the proposed recipient `baobab-control-plane-subscription-billing`, the sender and the allowed tenant. It validates the current key, the 300-second timestamp window, signature, envelope source, producer, event type, payload schema and envelope/payload tenant equality. The issuer credential authorises the worker to attempt dispatch. Only the recipient-specific signing key authenticates the HTTPS message. The protected CP ingress and signing-recipient contracts need a separate reviewed version and implementation before any endpoint can be configured.

## Receipt, ordering and recovery

Store the authenticated envelope and digest durably in a tenant-scoped inbox, using the canonical `(source, id)` event identity. Bind the receipt to that identity and digest in the same database transaction. An identical event returns 200 DUPLICATE. A first durable write returns 202 ACCEPTED. A different digest or tenant for the same identity returns 409 and is quarantined. Match the schema, identity and status in the response before acknowledging the local outbox lease. An uncertain response retries within 72 hours of the first attempt. The receiver keeps receipt identity and digest for at least seven days. ACK means durable custody. Application and business outcomes have their own evidence.

Apply the event as a signal to reconcile the current authorised Subscriptions billing projection. Match the tenant, product subscription and billing subscription against the receiver's known mapping. An older authoritative revision cannot roll back the read model. Same-revision notifications must read current source state because the revision belongs to CP's governing instruction and does not order all billing changes. Termination is final for that billing projection. A bounded recovery sweep uses the same authorised current read and reports unknown or mismatched sources without granting or regressing state.

Manual replay requires current approval scoped to one tenant and original event, immutable audit, unchanged identity and an original payload digest. If an old receipt has aged out, verify the retained application checkpoint and the current source revision before permitting replay. Uncertain checkpoints fail closed. Keep payload and receipt retention separate and avoid event IDs, tenant IDs, signatures and billing data in metric labels.

## Acceptance sequence

1. Shared and the owning CP, Subscriptions and IAM maintainers accept the receiver and workload profile. Version the relevant transport and ingress contracts without opening ERP ingress to Subscriptions events.
2. CP implements the dedicated allowlist, durable receipt and recovery read model. Subscriptions implements delivery selection and replaces the broker-bound admission check. IAM implements the dedicated profile and revocation proof.
3. In disposable development, independently verify all four routed events and the local usage disposition. Exercise revoked workload and key, cross-tenant refusal, foreign event, incorrect digest, reordered and same-revision events, lost response after durable commit, bounded retry and authorised replay. Compare sender and receiver records, reconcile the read model and witness teardown. Protected activation and monetary paths have their own approvals.

References: [ADR-SHARED-011](../adr/ADR-SHARED-011%20%E2%80%94%20Subscription%20Classification%2C%20Billing%20and%20Payment%20Contracts.md), [FB-04](signed-event-delivery.md), [billing AsyncAPI](../../contracts/subscriptions/v1/asyncapi.yaml), [Subscriptions #55](https://github.com/baobab-platform/baobab-subscriptions/pull/55), [Subscriptions #56](https://github.com/baobab-platform/baobab-subscriptions/pull/56), [RabbitMQ confirm and acknowledgement semantics](https://www.rabbitmq.com/docs/confirms).
