# Cross-engine metadata contract

Cross-engine interoperability is defined by schemas, not by a shared language
runtime. The canonical files are:

| Concern | Canonical contract |
|---|---|
| Event metadata | `contracts/events/v1/envelope.schema.json` |
| HTTP errors | `contracts/errors/v1/problem-details.schema.json` |
| Command and event idempotency | `contracts/idempotency/v1/policy.yaml` |
| Contract evolution | `docs/architecture/contract-versioning.md` |

## Event identity and context

| Attribute | Meaning | Rule |
|---|---|---|
| `source` + `id` | Delivery identity | Preserved across retries; consumer inbox key |
| `type` | Event semantics | Reverse-DNS name ending in major `vN` |
| `dataschema` | Payload shape | Immutable versioned schema URI |
| `subject` | Canonical business subject | Never a vendor database identifier |
| `baobabscope` | Platform or tenant scope | Tenant scope requires `tenantid` |
| `tenantid` | Isolation and entitlement context | Minted and resolved by Control Plane |
| `correlationid` | Distributed business interaction | Preserved across the workflow |
| `causationid` | Immediate cause | Omitted for a root occurrence; never `null` |
| `traceparent` / `tracestate` | Technical distributed trace | Propagated according to W3C Trace Context |
| `idempotencykey` | Originating command identity | Required for command consequences; not a delivery key |

The domain payload stays under `data` and is validated against `dataschema`.
Tenant, correlation and tracing metadata must not be buried only inside the
payload because gateways, brokers and generic telemetry need to inspect it.

## Delivery behaviour

1. A producer commits its business state and outbox record transactionally.
2. Publishing retries keep the original `source` and `id`.
3. A consumer validates envelope version, type, scope and payload schema before
   applying a consequence.
4. The consumer records `(source, id)` with the domain effect atomically where
   possible.
5. A duplicate is acknowledged without repeating the effect.
6. Transient failures use bounded retry with backoff and jitter. Poison or
   incompatible messages go to quarantine or a dead-letter path.
7. Replay is authorised and audited; it preserves event identity.

Unknown major event types and invalid payloads are not retried forever. They are
quarantined with safe diagnostics and the canonical correlation information.

## Legacy Control Plane mapping

| Legacy field | Canonical field | Migration rule |
|---|---|---|
| `correlation_id` | `correlationid` | Rename without changing the value |
| `causation_id` | `causationid` | Omit when legacy value is `null` |
| `tenant_id` | `tenantid` | Rename; value must pass canonical tenant grammar |
| relative `source` | absolute `source` | Use the registered logical producer URI |
| absent `dataschema` | `dataschema` | Supply the immutable payload-schema URI |
| absent scope | `baobabscope` | Derive explicitly; never default an unresolved tenant |

The legacy fixture exists to prove that old metadata is rejected by the
canonical schema. It is migration evidence, not another supported envelope.

## Legacy Trade and ERP mapping

Trade and ERP currently share another local compatibility shape. PRs A3 and A5
must remove it using the following mechanical metadata mapping; domain payload
semantics still require their own reviewed contracts.

`contracts/events/v1/compatibility/legacy-trade-erp-event.json` records the
current evidenced shape and is required to fail canonical validation.

| Legacy field | Canonical field | Migration rule |
|---|---|---|
| `event_id` | `id` | Mint a UUID for each occurrence and preserve it on retry |
| `event_type` | `type` | Adopt the `com.baobab-platform.<domain>.<event>.vN` namespace |
| `schema_version` | `type` + `dataschema` | Version semantics and payload shape explicitly |
| `occurred_at` | `time` | Preserve the UTC business-occurrence time |
| service enum `source` | absolute `source` | Use the registered logical producer URI |
| `correlation_id` | `correlationid` | Preserve the value where it is a UUID; otherwise migrate it |
| nullable `causation_id` | optional `causationid` | Omit a missing root cause; never send `null` |
| `tenant_id` | `tenantid` | Require the Control Plane-minted canonical value |
| `entity_id` | domain payload or mapping | Do not treat legal entity as envelope tenancy |
| `payload` | `data` | Validate against the immutable `dataschema` URI |

## HTTP problem details

APIs return RFC 9457 problem details with media type
`application/problem+json`. `status` agrees with the HTTP response status,
`code` drives machine behaviour, and `detail` remains safe for the caller.
Callers may retry only when `retryable` is true and the operation's documented
retry and idempotency policy permits it.
