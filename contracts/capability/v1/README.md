# Baobab capability-centric contracts v1

This package defines the canonical, implementation-neutral vocabulary for
Baobab's capability-centric platform architecture (ADR-BCP-002 through
ADR-BCP-009, ADR-SHARED-007). It answers four distinct questions without
conflating them:

- **What** can Baobab do? -> `capability.schema.json`
- **What package** needs it? -> `composition.schema.json`
- **May this tenant** consume it? -> `grant.schema.json` (scoped by `scope.schema.json`)
- **How and where** is it implemented? -> `provider.schema.json` + `binding.schema.json`, resolved into `resolution.schema.json`

## What this package is not

This is a contract-authority package: JSON Schema, YAML governance files,
AsyncAPI and OpenAPI definitions only. It does **not**:

- run as a service, hold tenant state, or execute resolution -- that is
  `nabhold/baobab-cp`'s runtime responsibility;
- implement business workflows (approval logic, workflow engines, state
  machines with side effects) -- see the retired
  `packages/supplier-domain/src/lifecycle.ts` for a worked example of
  exactly the pattern this package must not repeat;
- pick a winning provider or engine instance for any given request;
- define domain-specific business authorization (that remains with each
  domain engine: `baobab-trade`, `baobab-erp`, `baobab-cms`, `baobab-pulse`).

## Contract surfaces

- `domain.schema.json` -- every identifier grammar and closed enumeration
  used across the other files in this package.
- `capability.schema.json` -- `CapabilityDefinition` and
  `CapabilityDependency`.
- `composition.schema.json` -- `CapabilityComposition` and
  `CapabilityCompositionMember`.
- `scope.schema.json` -- `CapabilityScope`, the applicability dimensions
  shared by grants and bindings.
- `grant.schema.json` -- `CapabilityGrant` (entitlement).
- `provider.schema.json` -- `CapabilityProvider` and
  `ProviderCapabilitySupport` (implementation declaration).
- `binding.schema.json` -- `CapabilityBinding` (routing).
- `resolution.schema.json` -- the runtime resolution request/response
  shapes and the persisted `CapabilityResolution` record.
- `namespace-registry.yaml` -- the governed set of top-level capability
  domains (the first segment of every `capability_key`).
- `scope-specificity.yaml` -- the canonical, deterministic algorithm for
  ranking competing eligible bindings. Every capability-centric ADR
  deferred this definition to Shared; this file is that definition.
- `asyncapi.yaml` -- capability lifecycle events, using the existing
  `com.nabhold.<context>.<...>.v<N>` convention already enforced by
  `contracts/events/v1/envelope.schema.json` (confirmed during the
  Phase-0 audit as the real, shipped convention across identity, ERP and
  supplier-onboarding events -- this package does not introduce a
  different one).
- `openapi.yaml` -- the capability registry and resolution HTTP surface.

All asynchronous messages use `contracts/events/v1/envelope.schema.json`.
All HTTP errors use `contracts/errors/v1/problem-details.schema.json`.
Capability-resolution denial reason codes live in the `capability_resolution_denial`
category of `contracts/authorization/v1/reason-code-registry.yaml`, alongside
(not duplicating) the pre-existing `authorization_denial` category.

## Relationship to existing contracts

- `CapabilityScope` (this package) and `mappingScope`
  (`contracts/control-plane/v1/canonical-mapping.schema.json`) share
  dimension vocabulary but are evaluated by different resolvers for
  different purposes and are never treated as interchangeable.
- `contracts/control-plane/v1/context-resolution.schema.json` is the
  pre-capability-centric context/entitlement check
  (`product_id` in, coarse `entitled: true/false` out). It is not
  replaced by this package; `nabhold/baobab-cp`'s Phase 2+ work
  (see the Capability Platform tracking issue) extends context
  resolution into the richer `PlatformContext` model these capability
  contracts assume, as a separate, sequenced piece of work.
- Capability lifecycle events use the same envelope and the same
  `com.nabhold.*` reverse-DNS convention as every other event domain in
  this repository -- see the Phase-0 audit finding on the Capability
  Platform tracking issue for why an earlier draft specification's
  `baobab.*` proposal was not adopted.
