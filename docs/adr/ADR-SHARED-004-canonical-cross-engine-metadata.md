# ADR-0004: Canonical Cross-Engine Event, Error, and Idempotency Metadata

| | |
|---|---|
| **Status** | Accepted |
| **Date** | 2026-09-01 |
| **Owner** | Chief Software Engineer, Baobab-Platform Group Africa |
| **Repository** | `baobab-platform/shared` |
| **Depends on** | ADR-0002; ADR-0003; Shared contract-versioning policy |
| **Applies to** | `baobab-cp`, Baobab engines, infrastructure adapters, and authorised digital-estate backends |

## 1. Context

Control Plane already defined a CloudEvents-like JSON envelope, while ERP and
Trade carried local compatibility shapes. The definitions disagreed on naming,
tenant identity, tracing, idempotency, error responses, and whether a payload
schema was discoverable. Allowing each engine to settle those concerns locally
would make implementation language or vendor details part of the platform API.

The Control Plane runtime does not yet publish its documented lifecycle events,
and Trade-to-ERP publishing is not operational. The platform can therefore
converge the contract before an incompatible production event history exists.

## 2. Decision

### 2.1 Event envelope

`contracts/events/v1/envelope.schema.json` is the sole organisation-wide event
envelope. It is a constrained CloudEvents 1.0 structured-JSON profile.

- CloudEvents core attributes keep their standard meanings.
- The pair `(source, id)` is the delivery deduplication identity.
- `type` and `dataschema` independently version event semantics and payload
  shape. A breaking payload change requires a new `vN` type and schema URI.
- Baobab extension attributes use lowercase alphanumeric CloudEvents-compatible
  names: `baobabscope`, `correlationid`, `causationid`, `tenantid`,
  `idempotencykey`, `traceparent`, and `tracestate`.
- Tenant-scoped events require a Control Plane-minted `tenantid`. Platform
  events must not invent or default tenant context.
- `traceparent` and `tracestate` follow W3C Trace Context. Correlation and
  causation remain business-interaction identifiers and do not replace traces.
- Context attributes must not contain credentials, personal data, accounting
  data, or vendor-internal identifiers.

The former Control Plane envelope path remains as a reference to the canonical
schema so existing consumers have one migration location, not a competing
definition. Its snake_case envelope is retained only as a negative
compatibility fixture.

### 2.2 Idempotency

`contracts/idempotency/v1/policy.yaml` governs commands and events.

- Side-effecting synchronous commands use `Idempotency-Key`, scoped by service,
  operation, tenant and key, and bound to canonical request semantics.
- Reusing a key for an incompatible request returns the canonical 409 problem.
- Event delivery retries preserve `source` and `id`.
- Consumers atomically record the inbox identity with the business effect where
  storage permits; duplicates are acknowledged without repeating the effect.
- An event caused by an idempotent command carries `idempotencykey`, but that
  value does not replace `(source, id)` as the delivery identity.
- Exactly-once delivery is not claimed. Financial correctness comes from
  transactional effects, idempotency and reconciliation.

### 2.3 HTTP errors

`contracts/errors/v1/problem-details.schema.json` is the canonical
`application/problem+json` shape and follows RFC 9457. Baobab extensions add a
stable `code`, `correlation_id`, optional `trace_id`, explicit `retryable`
decision and bounded field errors.

Error details must not leak another tenant's existence, credentials, personal
information, raw accounting records or internal stack traces.

## 3. Consequences

### Positive

- Go, Java, TypeScript and Python services share semantic metadata without a
  common implementation library.
- Brokers, gateways and observability tooling can inspect routing and tracing
  metadata without decoding domain payloads.
- Duplicate delivery and partial failure have explicit, testable behaviour.
- ERP-specific contracts can now focus on business payloads rather than
  reinventing transport metadata.

### Costs

- Existing local snake_case event adapters must translate once and then be
  retired.
- Every domain event requires an immutable payload schema URI.
- Consumers need durable inbox/idempotency storage before they can claim a
  financial consequence is safe to replay.

## 4. Rejected alternatives

- **Keep the Control Plane envelope as the general contract unchanged.**
  Rejected because its snake_case extensions are not CloudEvents-compatible and
  it omits payload-schema and explicit scope requirements.
- **Publish a second ERP envelope.** Rejected because it would hard-code the
  current migration into every consumer.
- **Use trace IDs as idempotency or business-correlation IDs.** Rejected because
  tracing samples and span topology have different lifecycle semantics.
- **Promise exactly-once broker delivery.** Rejected because retries, crashes
  and partial failures make that promise misleading.
- **Continue custom JSON error bodies.** Rejected because RFC 9457 already
  provides the interoperable base semantics.

## 5. Follow-up

1. Generate or publish language bindings only after the schemas stabilise.
2. Update Control Plane and Trade consumers in PRs A4 and A5.
3. Define ERP domain payloads and the system-of-record ADR in A3 without
   changing this envelope.
4. Add registered downstream compatibility jobs as consumers adopt a released
   Shared revision.

## 6. Standards references

- [CloudEvents 1.0.2 specification](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md)
- [W3C Trace Context Recommendation](https://www.w3.org/TR/trace-context/)
- [RFC 9457 — Problem Details for HTTP APIs](https://www.rfc-editor.org/rfc/rfc9457.html)
