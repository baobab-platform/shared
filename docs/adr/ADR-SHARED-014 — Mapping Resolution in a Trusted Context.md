# ADR-SHARED-014 — Mapping Resolution in a Trusted Context

| | |
|---|---|
| **Status** | Accepted |
| **Date** | 2026-09-26 |
| **Repository** | `baobab-platform/shared` |
| **Depends on** | ADR-SHARED-012; ADR-SHARED-013; Baobab Canonical Mapping Model §§17.3, 22-24; `capability/v1` `resolution.schema.json` |
| **Applies to** | `baobab-cp` and every workload that resolves a canonical entity to its mapped representation |

## Context

`resolveMapping` (`POST /resolution/mappings`) took its context inline, as a `context-resolution` response. The calling workload therefore asserted the tenant, legal entity and other dimensions that decide which mappings apply.

The Canonical Mapping Model forbids this. A caller must not be able to select an arbitrary tenant by what it sends (§17.3). Context is resolved from trusted evidence before mappings are resolved (§22).

Capability resolution already follows this rule. Its request redeems a `context_id` the Control Plane resolved and stored, and a caller never supplies raw tenant, estate or market identity to it.

The operation had four further gaps:
- It had no tenant of its own.
- It could not return a canonical-to-canonical result.
- Its `target_system` grammar predated ADR-SHARED-012.
- Its `target_capability` had no defined meaning for mappings, which do not name capabilities.

No service implemented it.

## Decision

1. **The context is redeemed, never supplied.**
   - `resolutionRequest` requires `context_id`: a context the Control Plane resolved and stored earlier, as in capability resolution.
   - It carries no tenant, legal entity, market or other scope dimension, and no inline context.
   - An unknown or expired context is `CONTEXT_NOT_FOUND` (404).
   - A context of another tenant than the caller's is `TENANT_CONTEXT_MISMATCH` (403).
2. **Resolution follows the Mapping Model.**
   - It runs in the context's tenant, over that tenant's ACTIVE CANONICAL_TO_EXTERNAL, BIDIRECTIONAL and SOURCE_TO_TARGET Mappings in effect at `effective_timestamp` (default: now).
   - CANDIDATE and REJECTED mappings never resolve.
   - A scoped mapping is a candidate only when the context matches its scope.
   - Candidates rank by scope specificity, then resolution priority, then confidence (§9.7).
   - Equally ranked candidates are `MAPPING_AMBIGUOUS` (409) and resolve to nothing (§24). No candidate is `MAPPING_NOT_FOUND` (404).
3. **Targets are named in the registry grammar.**
   - `target_system_namespace` and `target_engine_id` (ADR-SHARED-012) restrict candidates to mappings to an external reference of that system or engine.
   - `target_capability` is removed. The engine serving a capability is what capability resolution decides, so a caller resolves the capability first and passes its engine.
4. **The response says what resolved.**
   - `resolutionResponse` adds `context_id` and `tenant_id`, and exactly one of `external_reference_id` and `target_canonical_entity_id`.
   - `mapping_version` and `resolved_at` are required.
   - `resolution_reason` is `default_mapping` for an unscoped mapping and `scope_matched` for a scoped one, or `priority_applied` when priority or confidence decided between equally specific candidates.

## Consequences

- `control-plane/v1` `openapi.yaml` is 1.7.0. The request change breaks callers of `resolveMapping`, which no service served.
- The Control Plane implements `resolveMapping` by redeeming the stored context, as its capability resolution does. It removes the operation from its list of described-but-unimplemented routes.
- A workload that needs a canonical entity's representation in an engine resolves context first, then optionally the capability, then the mapping.
