# Control-plane foundation contract

This document is the canonical Foundation 0 architecture for the Baobab-Platform
control plane. Runtime repositories may explain their implementation, but must
reference these contracts rather than copy and alter them.

## Domain boundaries

- A **legal entity** describes an incorporated or otherwise recognised
  organisation.
- A **tenant** is a security and data-isolation boundary. A legal entity is the
  default tenant boundary, but the concepts are not synonymous.
- An **estate** is an independently deployable customer-facing application.
- A **product subscription** grants a tenant access to a Baobab capability.
- A **deployment** is one released workload in an environment.
- A **domain binding** maps a verified host name to an estate deployment.
- An **infrastructure binding** records a provisioned resource without exposing
  its credentials.

## Command and event flow

1. A caller submits `POST /v1/tenants` with an idempotency key.
2. The control plane validates the released contract and records the tenant,
   provisioning operation, and outbox event in one database transaction.
3. Idempotent workers reconcile database, broker, cache, and gateway resources
   through narrowly scoped provisioner adapters.
4. Each state transition emits a versioned event carrying correlation and
   causation identifiers.
5. Desired state remains in PostgreSQL; observed state is updated only after a
   provisioner confirms the external result.

## Initial technology decisions

| Concern | Decision |
| --- | --- |
| Runtime | Go with REST/OpenAPI |
| Metadata store | PostgreSQL 17 |
| Database tenancy default | Schema per tenant |
| Events | RabbitMQ with publisher confirms and dead-letter queues |
| Delivery reliability | Transactional outbox and idempotent consumers |
| Gateway | Apache APISIX reconciled through its Admin API |
| Cache | Redis 7 as a rebuildable projection, never the source of truth |
| Local environment | Docker Compose |
| Production provisioning | Terraform on AWS Cape Town |
| Later orchestration | Kubernetes/Helm and Temporal only when justified |
| Observability | OpenTelemetry, structured logs, and Prometheus metrics |

## Non-negotiable invariants

- APISIX and its plugins never receive control-plane PostgreSQL credentials.
- Redis cache misses do not cause the gateway to query PostgreSQL directly.
- Events are immutable facts; commands express requested work.
- Consumers ignore unknown additive fields and reject unsupported major
  contract versions.
- Provisioning operations are retryable, idempotent, and auditable.
- Secrets are referenced by opaque identifiers and never carried in contracts,
  logs, events, or Git.
