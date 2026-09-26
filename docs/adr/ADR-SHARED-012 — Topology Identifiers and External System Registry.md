# ADR-SHARED-012 — Topology Identifiers and External System Registry

| | |
|---|---|
| **Status** | Accepted |
| **Date** | 2026-09-26 |
| **Repository** | `baobab-platform/shared` |
| **Depends on** | ADR-0004; ADR-SHARED-007; Baobab Canonical Mapping Model §§8, 13-14; baobab-cp ADR-BCP-006, ADR-BCP-022 |
| **Applies to** | `baobab-cp` and every consumer of `control-plane/v1`, `capability/v1`, `authorization/v1` and `identity/v1` |

## Context

Before the Control Plane can serve ExternalReferences in the shape `control-plane/v1` `canonical-mapping.schema.json` defines, the identifiers that shape uses must mean one thing everywhere. They did not:

| Identifier | Where | Grammar |
|---|---|---|
| Engine | `canonical-mapping` `engine_id` | snake_case slug, e.g. `baobab_trade` |
| Engine | `identity/v1` `engine`; `capability/v1` `capabilityProviderKey` (`<owning-repository>.<engine>`) | repository name, e.g. `baobab-trade` |
| Engine instance | `canonical-mapping` `engine_instance_id` | snake_case slug |
| Engine instance | `capability/v1` binding | `ei_[a-z0-9]+` |
| Engine instance | `capability/v1` resolution, `authorization/v1` context, `identity/v1` | unconstrained string |
| Engine instance | the Control Plane | a UUID |

Nothing registered which external systems may hold native objects, or which engine runs each one. An ExternalReference's `system_namespace` could only have been guessed, for example by copying the engine id. The ExternalReference contract forbids that.

## Decision

### 1. One grammar per topology identifier

`control-plane/v1` `domain.schema.json` defines both identifiers, and every contract uses them.

- **`engineId`**: a registered engine, named as its repository, for example `baobab-trade` (`^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$`). This is the form `identity/v1` and `capabilityProviderKey` already use. An engine is a service. It is not its technology family: the family is `capability/v1` `engineKey` (for example `medusa`), which an ExternalReference names as its `system_namespace`.
- **`engineInstanceId`**: a concrete engine deployment, minted by the Control Plane as `ei_[a-z0-9]+`. This is the form `capability/v1` bindings already use.

The definitions are applied as follows:
- `canonical-mapping` (`externalReference` and `mappingScope`), `capability/v1` binding and resolution, and `capability-explanation` reference them.
- `authorization/v1` and `identity/v1` use another `$id` base, so they repeat the pattern. The validator holds every copy equal to the definition.

### 2. External system registry

`control-plane/v1/external-systems.yaml` lists each `system_namespace` and the engines allowed to hold it. The Control Plane refuses an ExternalReference whose (`system_namespace`, `engine_id`) pair is not registered. A namespace is never inferred from an engine id, and an engine id is never inferred from a namespace. Registering a system is a reviewed architecture change.

The first entries are the pairs the platform owner confirmed:

| system_namespace | engine_ids |
|---|---|
| `medusa` | `baobab-trade` |
| `idempiere` | `baobab-erp` |
| `payload` | `baobab-cms` |

## Consequences

- **The Control Plane mints `ei_` identifiers.** It keeps its UUIDs only as internal surrogates. Every API that carries an engine instance emits and accepts the `ei_` identifier: capability resolution, the capability explanation, and the ExternalReference and mapping scope APIs. This is a breaking change to the runtime resolution responses for any consumer that stored or compared the UUIDs.
- **The Control Plane's engine codes must follow `engineId`.** It reports registered engines whose code does not conform, rather than renaming them.
- ExternalReference work in the Control Plane (baobab-cp admin OpenAPI phase 3c) builds on this. Legacy references whose system cannot be identified from the registry are reported, not back-filled.
- Adding an external system, or another engine for an existing one, means a change to `external-systems.yaml`.
