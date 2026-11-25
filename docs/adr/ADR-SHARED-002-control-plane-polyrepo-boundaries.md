# ADR-0002: Control-plane polyrepo boundaries

- **Status:** Accepted
- **Date:** 2026-08-31
- **Decision owners:** Baobab-Platform platform architecture

## Context

Baobab-Platform needs a cloud-native control plane without coupling customer-facing
digital estates to environment orchestration. The earlier Baobab scaffold mixed
application, platform, and infrastructure concerns in one repository.

## Decision

The control-plane foundation is split across four repositories:

<!-- markdownlint-disable MD013 -->

| Repository | Authoritative responsibility |
| --- | --- |
| `baobab-platform/shared` | Versioned schemas, API and event contracts, state-machine definitions, compatibility policy, and reusable CI contracts |
| `baobab-platform/baobab-cp` | Go management API, control-plane metadata, reconciliation workers, audit history, and runtime database migrations |
| `baobab-platform/infrastructure` | Docker Compose, Terraform, Kubernetes/Helm, APISIX platform configuration, observability, and environment deployment |
| `baobab-platform/baobab-dev` | Versioned development and CI container images |

<!-- markdownlint-enable MD013 -->

Digital-estate and Baobab-engine repositories consume released contracts. They
must not import infrastructure implementation or call environment orchestrators
directly.

Executable Temporal workflows, JWT cryptography, and provisioning adapters are
runtime code and therefore do not belong in `shared`. Shared may define their
portable data contracts and test fixtures.

## Integration rule

Repositories integrate through versioned packages, authenticated APIs, and
versioned events. A merge in `shared` may run downstream compatibility tests,
but it must not silently deploy or mutate a consumer repository.

## Consequences

- Contracts can evolve independently through explicit versions.
- Application estates remain portable across environments.
- Infrastructure credentials are unavailable to digital estates.
- Some changes require coordinated, separately reviewed pull requests.
- Existing mixed-responsibility content in `baobab-cp` must be retired through
  an explicit migration rather than treated as the target architecture.


## Reusable Foundation container finding policy

The Shared reusable Foundation container gate is strict by default: HIGH and
CRITICAL vulnerability findings fail the gate. It also supports an explicit
consumer input to make findings non-blocking where the consumer's accepted
development policy requires image-build continuity. This setting never skips
the build or scan, never changes scanner coverage or output, and never converts
findings into a clean result. The full vulnerability report is retained as
evidence. Scanner, database, report-validation and tool failures remain fatal
regardless of the finding policy. Consumers must select the non-blocking mode
explicitly; release and protected-environment consumers retain strict
blocking behavior.
