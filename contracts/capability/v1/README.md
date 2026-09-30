# Baobab capability-centric contracts v1

This package defines the canonical, implementation-neutral vocabulary for
Baobab's capability-centric platform architecture (ADR-BCP-002 through
ADR-BCP-009, ADR-SHARED-007). It answers four distinct questions without
conflating them:

- **What** can Baobab do? -> `capability.schema.json`
- **What package** needs it? -> `composition.schema.json`
- **May this tenant** consume it? -> `grant.schema.json` (scoped by `scope.schema.json`)
- **How and where** is it implemented? -> `provider.schema.json` + `binding.schema.json`, resolved into `resolution.schema.json`

It also holds the **Canonical Capability Catalogue** and the portable
**provider declaration** contract. ADR-SHARED-017 is the governing EA-02
decision for both (*Accepted*; see "EA-02 status" below):

- **Which capabilities exist?** -> `catalogue.yaml` (`catalogue.schema.json`)
- **Who claims to implement them?** -> each engine's
  `.baobab/capability-provider.yaml` (`provider-declaration.schema.json`)

## Vocabulary (ADR-SHARED-017)

| Concept | Meaning | Authority | Contract |
|---|---|---|---|
| Capability | What Baobab can do, e.g. `payment.payment.capture`. Never names a provider, vendor, tenant or region | Shared | `capability.schema.json`, indexed by `catalogue.yaml` |
| CapabilityProvider | A specific implementation able to provide capabilities, e.g. `baobab-payments.sandbox` (`<engine-id>.<provider-name>`) | Engine repository declares it; Control Plane registers it | `provider-declaration.schema.json`, `provider.schema.json` |
| Engine (`engine_id`) | A Baobab engine/service identity, named as its repository, e.g. `baobab-trade` (ADR-SHARED-012). Not a technology | Control Plane topology | `control-plane/v1` `engineId` |
| `implementation_key` | The underlying technology or provider family, e.g. `medusa`, `ory`, `hyperswitch` | Engine repository | `domain.schema.json` `implementationKey` |
| EngineInstance | A concrete deployed runtime of an engine | Control Plane (EA-03) | `control-plane/v1` |
| ProviderCapabilitySupport | Which capabilities and contract majors a provider can implement | Declared by the engine, registered and activated by the Control Plane | `provider.schema.json` `capabilitySupport` |
| CapabilityBinding | Contextual routing eligibility: a provider on an instance for a scope | Control Plane | `binding.schema.json` |
| CapabilityGrant | Tenant entitlement | Control Plane (product/subscription governance) | `grant.schema.json` |
| Certification | Independent evidence that an implementation conforms | EA-09 | not yet modelled |
| HealthObservation | Time-bounded operational health evidence | Runtime observation | `health.schema.json` |

`engine_key` (`domain.schema.json` `engineKey`) is the v1 provider field whose
meaning drifted between technology family and provider label. It stays
unchanged in v1 for compatibility, is marked deprecated, and the next
capability contract major removes it in favour of `engine_id`,
`provider_key` and `implementation_key`. ADR-BCP-006's older description of
"Engine" as a technology family is superseded by ADR-SHARED-012 and
ADR-SHARED-017 SS8.

## Three `.baobab` contracts, three meanings of "capability"

| File | Question it answers | Its "capabilities" are | Schema |
|---|---|---|---|
| `.baobab/repository.yaml` | What kind of repository is this, and which Foundation controls apply? | Foundation technical traits (`engine`, `node`, `container`) | `.baobab/repository.schema.json` (ADR-0020) |
| `.baobab/environment.yaml` | Which `baobab-dev` toolchain does development need? | `validation.required_capabilities`: `baobab-dev` capabilities (`languages.node`) | `contracts/development-environment/schema.yaml` |
| `.baobab/capability-provider.yaml` | Which canonical Baobab capabilities do this engine's providers implement or plan? | Canonical capability keys from `catalogue.yaml` (`payment.payment.capture`) | `provider-declaration.schema.json` |

They are never merged, and a key from one is never valid in another.
`baobab-platform/engine-template` ships an example of each.

## Canonical Capability Catalogue

`catalogue.yaml` lists every canonical capability, sorted by key, with its
semantic owner and the definition document holding it, for example
`../../payments/v1/capabilities.yaml`. Definition documents use one shape,
`capability.schema.json#/$defs/CapabilityDefinitionDocument`, whose
definitions are `CapabilityDefinition`s without the identifiers the
Control Plane mints. **A capability is canonical if and only if the
catalogue lists it.** Nothing discovers capabilities by directory scan,
file name or extension; serialization is not membership.

`scripts/capability_catalogue.py validate-catalogue` enforces, in CI:
unique and sorted entries; every entry resolves to exactly one definition
with the same owner; owners are Baobab engine/service repositories; domains
are registered, and `namespace-registry.yaml` agrees with the
`capabilityDomain` enum; request, response, error and event schemas
resolve; dependencies target catalogued capabilities and REQUIRED
dependencies are acyclic; no key names a vendor, tenant, country or
region; and no capability definition anywhere in `contracts/` escapes the
catalogue, whatever its file is called.

The catalogue currently indexes the nine capabilities Shared had defined
before EA-02: Payments (4), Subscriptions (2) and Trade (3). The
cross-engine census (EA-02A) adds entries only once its candidates are
accepted. Until then, engines record intent as planned capabilities.

## Provider declarations

An engine repository owns `.baobab/capability-provider.yaml`, which conforms
to `provider-declaration.schema.json`. Shared is contract authority, not a
provider, and has no declaration of its own. A declaration names the engine
(`engine_id`) and one or more providers. Several providers per engine are
normal, for example `baobab-iam.keycloak` and `baobab-iam.ory` during a
migration. For each provider it states:

- `provider_type`, `implementation_key`, `simulated` and
  `production_permitted`. A simulated provider can never be production
  permitted, and permission is not activation;
- an optional logical `invocation` (`service://<engine-id>/<service>`), never
  a host, address or credential;
- `support`: canonical `capability_key`s, the contract majors implemented,
  `implementation_status` (`PARTIAL` or `IMPLEMENTED`, never
  `ACTIVE`/`CERTIFIED`/`HEALTHY`), provenance, and repository-relative
  `implementation_evidence`, which `IMPLEMENTED` requires.

`planned_capabilities` records architecture intent (`CANDIDATE`, `PROPOSED`,
`CONTRACTING`, `CONTRACTED`). A plan that is not yet canonical uses
`proposed_key`; only `CONTRACTED` references a canonical `capability_key`.
Planned capabilities never create provider support or bindings, never
satisfy compositions and never resolve.

A declaration cannot carry certification, lifecycle, activation, bindings,
grants, tenants, engine instances, releases or health. Every object is
closed. It also cannot claim a capability that is not in the catalogue.
`scripts/capability_catalogue.py validate-declaration` checks a declaration
against this Shared checkout: known capabilities and contract majors,
provider keys that belong to the engine, no duplicate support, invocation
for the engine only, plans kept separate from support, and, with
`--repository-root`, evidence paths that exist. `--template` validates
engine-template's placeholder example. `examples/provider-declaration.yaml`
is illustrative only.

A future EA-09 `ProviderCapabilityCertification` keys on provider,
capability, contract major and engine release. Every one of those except
the release is already explicit here. The release comes from EA-03 and never
from this file.

## Transitional registration (until EA-02E)

The Control Plane still bootstraps providers from `EngineRegistration`
bundles (`registration.schema.json`), `payments/v1/capabilities.json` and
`subscriptions/v1/capabilities.json`. These are now bundles, not
authoring formats:

- `registration-bundles.yaml` lists them explicitly. It replaces the Control
  Plane's discovery of any embedded path ending in `/capabilities.json`,
  which is how `trade/v1/capabilities.yaml` was silently missed;
- CI requires each bundle's capabilities to equal their canonical
  definitions, and every bundle in `contracts/` to be listed;
- `scripts/capability_catalogue.py generate-registration` produces the
  bundle shape from canonical definitions plus one declared provider. It
  registers IMPLEMENTED support only, and the provider lifecycle defaults to
  `DRAFT` (ADR-SHARED-017 SS33). CI proves the example sandbox declaration
  regenerates the committed Payments bundle.

The follow-up gates that retire this path, all in
`docs/architecture/ea-02-capability-catalogue.md`, are: CP catalogue sync,
index-driven bootstrap, provider registration that rejects unknown
capabilities, binding integrity and Foundation CI enforcement.

## Who answers what

| Question | Authoritative source |
|---|---|
| What capabilities exist? What does each mean? Who owns its semantics? | Shared: `catalogue.yaml` and the definitions it indexes |
| Which providers claim support, for which contract majors? Which are simulated or production permitted? What is merely planned? What evidence backs each claim? | Engine repository: `.baobab/capability-provider.yaml` |
| Which implementations are certified? | EA-09 |
| Which support is ACTIVE? Which EngineInstances serve it? Which tenants are entitled? Which bindings apply? Which provider does resolution select? | Control Plane runtime state |

No single source-controlled artefact answers every question, and that is
intentional.

## What this package is not

This is a contract-authority package: JSON Schema, YAML governance files,
AsyncAPI and OpenAPI definitions only. It does **not**:

- run as a service, hold tenant state, or execute resolution -- that is
  `baobab-platform/baobab-cp`'s runtime responsibility;
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
- `health.schema.json` -- `HealthObservation`: the health of an engine
  instance, a provider, or one capability on a provider, valid only from
  `observed_at` until `expires_at`.
- `health-policy.yaml` -- how health affects eligibility. A missing or
  expired observation counts as UNKNOWN. A capability whose
  `health_criticality` is `CRITICAL` accepts only HEALTHY (ADR-BCP-006).
- `resolution.schema.json` -- the runtime resolution request/response
  shapes and the persisted `CapabilityResolution` record.
- `catalogue.schema.json` / `catalogue.yaml` -- the Canonical Capability
  Catalogue: the explicit index of every canonical capability.
- `provider-declaration.schema.json` -- the engine-owned
  `.baobab/capability-provider.yaml` declaration.
- `registration.schema.json` / `registration-bundles.yaml` -- the
  TRANSITIONAL `EngineRegistration` bundle and its explicit index.
- `namespace-registry.yaml` -- the governed set of top-level capability
  domains (the first segment of every `capability_key`).
- `scope-specificity.yaml` -- the canonical, deterministic algorithm for
  ranking competing eligible bindings. Every capability-centric ADR
  deferred this definition to Shared; this file is that definition.
- `asyncapi.yaml` -- capability lifecycle events, using the existing
  `com.baobab-platform.<context>.<...>.v<N>` convention already enforced by
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
  replaced by this package; `baobab-platform/baobab-cp`'s Phase 2+ work
  (see the Capability Platform tracking issue) extends context
  resolution into the richer `PlatformContext` model these capability
  contracts assume, as a separate, sequenced piece of work.
- Capability lifecycle events use the same envelope and the same
  `com.baobab-platform.*` reverse-DNS convention as every other event domain in
  this repository -- see the Phase-0 audit finding on the Capability
  Platform tracking issue for why an earlier draft specification's
  `baobab.*` proposal was not adopted.

## EA-02 status

ADR-SHARED-017 reframes EA-02 as *Canonical Capability Catalogue, Provider
Support, Engine Registry and Runtime Resolution Convergence*. Its status is
**Accepted — Normative Target Architecture**, so its "SHALL"s bind Shared,
engines and the Control Plane. This package implements its Phase 1
(catalogue, provider-declaration schema, validation) additively within v1.
The Control Plane converges through the follow-up gates in
`docs/architecture/ea-02-capability-catalogue.md`. The `regulations`
namespace is not registered. SS43 requires the ADR-SHARED-007 architecture
review first, so Regulations capabilities can only be *planned*
(`proposed_key: regulations.*`) until that review accepts it.
