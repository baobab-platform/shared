# Changelog

All notable changes to `baobab-platform/shared` are documented in this file.

This changelog records changes to the shared engineering infrastructure used across the BAOBAB-PLATFORM organisation, including:

* reusable GitHub Actions workflows;
* composite actions;
* CI/CD pipelines;
* automation scripts;
* security controls;
* repository templates;
* engineering tooling; and
* organisation-wide development standards.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), with versioning following [Semantic Versioning](https://semver.org/) where versioned components expose a stable interface.

---

# Unreleased

Changes that have been merged but have not yet been included in a released version are recorded here.

## Changed

- **Breaking: one grammar per topology identifier, and an external system registry (ADR-SHARED-012).**
  `control-plane/v1` `domain.schema.json` now defines `engineId`, the engine named as its repository (for example `baobab-trade`), and `engineInstanceId`, the Control Plane-minted `ei_[a-z0-9]+`.
  - `canonical-mapping` (`externalReference` and `mappingScope`), `capability/v1` binding and resolution, and `capability-explanation` reference them.
  - `authorization/v1` context and `identity/v1` external references repeat the instance pattern.
  - Before this, engine ids were snake_case in one contract and repository names in two others, and engine instance ids were unconstrained, slugs or `ei_`.
  - The new `control-plane/v1/external-systems.yaml` registers each ExternalReference `system_namespace` with the engines allowed to hold it: `medusa`↔`baobab-trade`, `idempiere`↔`baobab-erp`, `payload`↔`baobab-cms`.
  - `scripts/validate-control-plane-contracts.py` checks every copy of the grammar, rejects UUID, slug and snake_case identifiers in negative fixtures, and checks the registry.

- **`tenant:read` is issued for `baobab-control-plane`.** It was registered for the audience `baobab-cp`, which the Control Plane does not use. The authorization validator now fails when an OpenAPI operation requires a scope that is not issued for its service, and it caught this.

- **Workload identities for the Control Plane -> Subscriptions -> Payments chain (assessment §22, EA-04).**
  `contracts/identity/v1/workload-registry.yaml` registers `baobab-cp-workload` (audience `baobab-subscriptions`; `billing:manage`, `billing:read`) and `baobab-subscriptions-workload` (audience `baobab-payments`; `payment:execute`, `payment:refund`, `payment:read`). Both are PROVISIONED with the new `federated_workload_token` credential type, which uses no static secret, and have no IdP client until the identity-provider migration ADR. `scripts/validate-authorization-contracts.rb` now checks every workload: each scope is registered, usable by workloads, not privileged and issued for one of its audiences, and each audience is used.

- **`tenant:write` is registered in `contracts/authorization/v1/scope-registry.yaml`.**
  The Control Plane and `control-plane/v1` (`security-policy.yaml`, `openapi.yaml`) already required it for tenant registration and management, but the registry did not define it. It is a privileged, human-only scope for the `baobab-control-plane` audience. `scripts/validate-admission-contracts.py` now checks it and `tenant:bootstrap`.

- **Breaking: tenant registration requires an AUTHORISED onboarding request (ADR-BCP-017 sections 22-24).**
  `contracts/control-plane/v1/tenant-registration.schema.json` now requires `tenant_onboarding_request_id`. The command must match the request's desired state; the request is recorded FULFILLED and produces at most one tenant. The OpenAPI `registerTenant` operation gains a 422 response. Approval still activates nothing, and there is no longer a direct registration path.

## Added

- **Administrative OpenAPI, phase 3c: external references and canonical mappings (ADR-SHARED-013).**
  `contracts/control-plane/v1/openapi.yaml` (1.6.0) adds a Mappings tag.
  - New operations: `createExternalReference`, `listExternalReferences` (by native identity), `getExternalReference`, `resolveExternalReference` (`POST /resolution/external-references`) and `validateMapping`.
  - Corrected operations:
    - `createMapping` and `updateMapping` now take `mappingCreateRequest` and `mappingUpdateRequest`, which carry no identifier, status, revision or actor.
    - `activateMapping` takes no body and enforces four-eyes approval.
    - `retireMapping` takes `mappingRetireRequest`, which carries a reason and no actor.
    - Every mapping command requires `If-Match`.
    - `getMapping` is readable by administrators through `canonical:read`.
  - `canonical-mapping.schema.json` gains the request, list and resolution definitions.
  - Its `mapping` read model now follows Canonical Mapping Model §9.2: the canonical entity is always set, with exactly one target. It previously let a canonical-to-canonical mapping omit its canonical entity.
  - `scripts/validate-control-plane-contracts.py` validates the new definitions and examples, with 20 more negative fixtures, and checks that examples name registered external systems.

- **Administrative OpenAPI, phase 3b: canonical registry and capability explanation (ADR-BCP-016, ADR-BCP-022 sections 47 and 123-131).**
  `contracts/control-plane/v1/openapi.yaml` (1.5.0) describes seven more operations. Under a new Canonical registry tag: `createCanonicalEntity`, `getCanonicalEntity` and the `validate`, `activate`, `suspend` and `retire` commands. Each command requires the entity's version in `If-Match`: a missing version is refused with 428, and a stale one with 412. Under Diagnostics: `explainCapability`. The new `canonical-entity.schema.json` defines `CanonicalEntityCreateRequest`, which cannot name an identifier, status, version or timestamp, so every entity starts DRAFT. It also defines `CanonicalEntity`. The new `capability-explanation.schema.json` defines the explanation request and response. The new `scripts/validate-control-plane-contracts.py` runs in CI and validates both schemas, their examples, negative fixtures and the OpenAPI references to them.

- **Administrative OpenAPI, phase 3a: Organisation administration (ADR-BCP-018 ORG-07, 09, 10, 13 and 15).**
  `contracts/control-plane/v1/openapi.yaml` (1.4.0) describes 19 more operations under the Organisations, Counterparties, Platform accounts, Audit and Diagnostics tags: IAM organisation links, organisation admission onboarding, legacy reconciliation, resolution candidates, counterparty roles, platform accounts and bindings, relationship drift and audit lineage. `organisation/v1/iam.schema.json` gains `IamOrganisationLinkRequest`, `IamOrganisationRetireRequest` and `IamOrganisationResolution`. `organisation/v1/counterparty.schema.json` gains `CounterpartyRoleAssignRequest`, `CounterpartyRoleEndRequest` and `CounterpartyReconciliationReport`. None of these requests can name its own Organisation, tenant or source authority.
- **`canonical:read`, `canonical:write`, `capabilities:explain` and `metrics:read` are registered.** The Control Plane already required them.

- **Administrative OpenAPI, phase 2: tenants and classification.**
  `contracts/control-plane/v1/openapi.yaml` (1.3.0) describes the tenant routes and the classification routes, 9 operations in all: tenant read, the suspend, activate and decommission commands, entitlements, classification, reclassification and the two explanations. New `control-plane/v1/tenant.schema.json` defines what the tenant routes return (`Tenant`, `Entitlement`, `TenantLifecycleResult`). `product/v1/subscription.schema.json` gains the request bodies `SubscriptionClassificationCommand` and `SubscriptionReclassificationCommand`. Provisioning is deferred to a later phase: its tenant manifest has no Shared schema yet.

- **Administrative OpenAPI, phase 1: applications, admission and onboarding (ADR-BCP-022 sections 17-20, CP Console FE-00 gap B2).**
  `contracts/control-plane/v1/openapi.yaml` (1.2.0) describes the Control Plane's 21 ADR-BCP-017 operations under the tags Applications, Admission and Onboarding. It reuses the `admission/v1` schemas for every body and response, and documents the status codes, pagination and separation-of-duties refusals the Control Plane implements. `scripts/validate-authorization-contracts.rb` now fails when an OpenAPI operation requires a scope that is unregistered or not issued for the Control Plane.

- **Bootstrap tenant registration (migration only).**
  `contracts/control-plane/v1/tenant-bootstrap-registration.schema.json` and `POST /tenants/bootstrap-registrations` register a tenant that predates the admission workflow. It needs the new privileged scope `tenant:bootstrap` and records `bootstrap_reason` and `evidence_reference`. It is never a route for a new customer.
- **CorporateGroup derivation metric (ADR-BCP-018 gate ORG-05).**
  The organisation/v1 metric catalogue gains `corporate_group_derivation_total`, which counts derivable CorporateGroups by `status` (CURRENT, PENDING, RETRYING). It uses the existing bounded label set.
- **Tenant onboarding handoff (ADR-BCP-017 sections 22-24, 39, 46).**
  `contracts/admission/v1/onboarding.schema.json` defines `TenantOnboardingRequest` (`tor_`), its desired state (subscription type, markets, products and isolation taken from the AdmissionDecision) and its commands. `onboarding-lifecycle.yaml` sets the lifecycle: REQUESTED → AUTHORISED → FULFILLED, with CANCELLED from either open state. New privileged scopes `onboarding:request` and `onboarding:authorise`. Four `tenant-onboarding.*` events. The validator gains 21 negatives, including separation of duties, one live request per decision, and desired state that departs from the decision.
- **Tenant PlatformAccount binding and account lifecycle (ADR-BCP-018 gate ORG-07).**
  `contracts/organisation/v1/platform.schema.json` adds `TenantPlatformAccountBinding` (explicit, effective-dated, at most one ACTIVE per tenant, commercial only), its bind/end commands, and the §83 PlatformAccount lifecycle (`platformAccountStatus`, `platformAccountTransitions`, `PlatformAccountStatusChangeRequest`). New events: `platform-account.status-changed`, `tenant-platform-account-binding.bound` and `.ended`. The validator gains 13 negative fixtures, including semantic ones: two ACTIVE bindings, binding on a CLOSED account, and binding without account membership.
- **Organisation drift, audit lineage and metrics (ADR-BCP-018 gate ORG-15).**
  `contracts/organisation/v1/observability.schema.json` defines
  `RelationshipDriftFinding` and `RelationshipDriftReport` (relationship
  drift in ADR-BCP-008's model; remediation is always review, never a
  cascade), `OrganisationAuditEntry` (the lineage section 131 asks for) and
  the section 130 metric catalogue with its bounded label names. New
  example, semantic checks and nine negative fixtures; the validator pins
  the metric catalogue to section 130 and rejects identifying labels.
- **Buyer/supplier reconciliation (ADR-BCP-018 gate ORG-13).**
  `contracts/organisation/v1/counterparty.schema.json` defines
  `CounterpartyRole` (tenant-scoped commercial role; migrated ADR-BCP-016
  buyer and supplier records keep their canonical ids and record their legacy
  kind), `OrganisationResolutionCandidate` (a quarantined pair of
  Organisations sharing a governed identifier; names never match) and
  `ResolutionCandidateDecision` (DISTINCT or DUPLICATE_CONFIRMED; merges
  nothing). New example, semantic checks and eighteen negative fixtures in
  `scripts/validate-organisation-contracts.py`.
- **Organisation admission onboarding (ADR-BCP-018 gate ORG-09).**
  `contracts/organisation/v1/admission.schema.json` defines
  `OrganisationAdmissionRequest` (issued by the admission reviewer after an
  approved decision; no field can set the platform relationship or mark
  anything verified) and `OrganisationAdmissionOutcome` (identity resolution
  NEW_ORGANISATION / EXISTING_ORGANISATION / QUARANTINED, plus the records
  onboarding converged on). Examples, semantic checks and ten negative
  fixtures in `scripts/validate-organisation-contracts.py`.
- **IAM organisation projection (ADR-BCP-018 gate ORG-10).**
  `contracts/organisation/v1/iam.schema.json` defines `IamOrganisationReference`,
  the explicit, issuer-scoped link from a canonical Organisation to a Keycloak
  Organization (many per Organisation, exactly one Organisation per issuer and
  provider organisation id); `IamOrganisationEvidence`, which workloads present
  instead of a canonical `organisation_id`; and the `keycloakOrganizationClaim`
  form Baobab relies on (organisation ids, never aliases). New
  `iamOrganisationReferenceId` grammar (`iamorg_*`), examples and negative
  fixtures in `scripts/validate-organisation-contracts.py`.
- **One event namespace.** `contracts/control-plane/v1` now registers every
  event `baobab-platform/baobab-cp` emits that was previously unregistered:
  `com.baobab-platform.control-plane.tenant.provisioning-ready/-active/-failed.v1`
  and `com.baobab-platform.control-plane.market-participation.created/updated.v1`,
  with payload schemas and example envelopes. `scripts/validate-event-registry.py`
  (run by the CI `governance-contracts` job) enforces the single
  `com.baobab-platform.*` namespace across every `asyncapi.yaml`: canonical and
  unique names, resolvable payloads, valid example envelopes, and no legacy
  `com.nabhold.*` types anywhere in `contracts/`.
- `contracts/organisation/v1` (ADR-BCP-018): Organisation, LegalEntityProfile,
  CorporateRelationship, CorporateGroup(Membership), PlatformRelationship,
  PlatformAccount(Membership) and explicit tenant mappings, with opaque
  resource-ID grammars and evidence-backed `VERIFIED` rules.
  `scripts/validate-organisation-contracts.py` is the first contract gate that
  performs real JSON Schema Draft 2020-12 validation with cross-schema `$ref`s
  resolved, validates the examples, and proves its rules with negative
  fixtures. The CI `governance-contracts` job now runs it.
- Foundation **security scopes** (M2). The security family now runs at `pr`
  scope on pull requests (gitleaks over the PR's own commits, dependency
  review applicable), `branch` scope on other events (the checked-out ref's
  full history) and `deep` scope under `security-deep` (every fetched ref,
  dependency review off). Each emits its own result: `Security / PR`,
  `Security / Branch` or `Security / Deep`. `security-secrets-scan.yml`
  gains a validated `log-opts` input (default `HEAD`, backward compatible).
- **`security.sast_provider`** in `.baobab/repository.yaml` (H2):
  `codeql | fallback | disabled`, with a `security.ghas` approval record
  required for CodeQL on a private repository and `disabled` requiring an
  approved `exceptions.sast`. Resolved by `scripts/foundation/sast_policy.rb`
  in the classifier; SAST reports `SAST / Fallback` instead of
  `SAST / Not available`. Private dependency review now also depends on the
  `security.ghas` record.
- **Organisation drift guard** (Phase 7):
  `.github/workflows/foundation-org-conformance.yml` runs weekly and on
  demand, evaluating every organisation repository with
  `scripts/foundation/org_conformance.py` against
  `.baobab/org-conformance.yaml`, and fails on non-deferred High findings.
  An optional `ORG_CONFORMANCE_TOKEN` secret extends it to private
  repositories.
- Fixtures: reusable-workflow nesting depth and workflow count against
  GitHub's limits, a version comment on every SHA-pinned action, SAST
  provider resolution across visibility and provider, the classifier run end
  to end, and the drift guard's rules.
- Foundation CI **Phase 4 product separation**:
  - Optional `profile` on `foundation-repository-gates.yml`
    (`full` | `contract` | `security-pr` | `security-deep` | `container`; default `full`).
  - Product entrypoints: `foundation-product-contract.yml`,
    `foundation-product-security.yml` (`mode: pr|deep`),
    `foundation-product-container.yml`.
  - Security trigger matrix and product boundaries in
    `docs/governance/foundation-ci-v2.md`.
  - Self-consumer uses `security-deep` on schedule and `full` otherwise.
- Foundation CI v2 **consumer readiness** (see
  `docs/governance/foundation-ci-promotion-v2.0.0.md` and tag `v2.0.0`):
  - Executable official caller template (`templates/caller-foundation-repository-gates.yml`)
    with required `foundation_ref`, minimum permissions, and explicit
    `advanced_security_enabled` / `legacy_metadata_enabled`.
  - Caller template validation fixture
    (`.github/foundation-tests/test_caller_template.py`).
  - Visibility-aware SAST planner: private repositories without GHAS opt-in
    emit **SAST / Not available** instead of attempting CodeQL upload.
  - Promotion record and support-policy gate for the immutable tag.
- Canonical CloudEvents 1.0 cross-engine envelope with tenant scope,
  correlation, causation, idempotency and W3C trace metadata.
- RFC 9457 problem-details schema and example for consistent API errors.
- Organisation-wide command/event idempotency policy, compatibility fixtures,
  validation gate and ADR-0004.
- ADR-0003 separating tenant, legal-entity and digital-estate identity.
- Governance validation for canonical entity, tenant and product identifiers,
  initial product-consumption intent and Control Plane examples.
- Canonical control-plane context-resolution request and response schemas.
- A machine-readable control-plane security policy covering token validation,
  scopes, transport trust, audit fields, and failure behaviour.
- OIDC-protected management and workload operations in the control-plane
  OpenAPI contract.
- Vendor-neutral Baobab ERP OpenAPI and AsyncAPI contracts for provisioning,
  mappings, Trade order/customer inputs, and ERP order, inventory, warehouse,
  invoice and payment-accounting outcomes.
- A machine-readable ERP system-of-record matrix, international value schemas,
  compatibility fixtures, validation gate and ADR-0005.
- `identity.suspended` and `identity.reactivated` events
  (`contracts/identity-events/v1/identity-suspended.schema.json`,
  `identity-reactivated.schema.json`), 2 of the 6 lifecycle events ADR-0016
  §90 anticipated but `baobab-platform/shared` had not yet defined.
- `entitlement.revoked`, `credential.compromised`, and `session.revoked`
  events (`contracts/identity-events/v1/entitlement-revoked.schema.json`,
  `credential-compromised.schema.json`, `session-revoked.schema.json`), 3
  more of the 6 lifecycle events ADR-0016 §90 anticipated.
- `workload.revoked` event (`contracts/identity-events/v1/workload-revoked.schema.json`),
  the last of the 6 lifecycle events ADR-0016 §90 anticipated -- all 9
  identity-events events it and ADR-0016 §139 call for now exist.
- `market` and `internal-trade` capability domains
  (`contracts/capability/v1/namespace-registry.yaml`,
  `domain.schema.json`'s `capabilityDomain` enum), registering
  `baobab-cp` ADR-BCP-011's market-participation/trade-lane model and
  ADR-BCP-012's internal-trade model so their capability keys (e.g.
  `market.export`, `internal-trade.mirror-document.create`) can be
  declared against a governed namespace. Added per ADR-SHARED-008.
- `customs` and `tax` capability domains (same files), registering
  `baobab-trade` ADR-0021's customs/trade-compliance model and
  ADR-0018 + its Addendum's multi-jurisdiction tax model. Added per
  ADR-SHARED-008.
- ADR-SHARED-008, confirming `com.baobab-platform.<context>.<...>.v<N>`
  (`contracts/events/v1/envelope.schema.json`) as the sole canonical
  event-type convention and registering the four domains above.
- A new `contracts/product/v1` package: `Product`, `ProductVersion`
  (`product.schema.json`), `ProductSubscription`, `EntitlementProjection`
  (`subscription.schema.json`), lifecycle events and AsyncAPI contract,
  closing 5 of Programme Gate P1's previously-absent items.
- `TenantProvisioning` (`contracts/control-plane/v1/provisioning-plan.schema.json`),
  the onboarding process aggregate Technical Specification §21 requires,
  additive to (not replacing) the already-shipped coarse
  provisioning-state-machine.yaml lifecycle.
- `ReadinessSnapshot` (`contracts/control-plane/v1/readiness.schema.json`)
  and `Drift` (`drift.schema.json`), the last 2 of Programme Gate P1's
  previously-absent items, both reusing the existing
  `capability_resolution_denial` reason-code vocabulary rather than
  introducing a new one.
- ADR-SHARED-009, closing Programme Gate P1 — Shared Contract Foundation.

## Changed

- Foundation CI **`v2.3.0` is promoted** at `31de2bc` (see
  `docs/governance/foundation-ci-promotion-v2.3.0.md`): security scopes,
  `security.sast_provider`, the organisation drift guard, and removal of
  `legacy_metadata_enabled`.
- Every SHA-pinned action carries a version comment; the five runtime setup
  pins that tracked a default branch now name the release they follow.
- Foundation environment gate: every `baobab-dev` profile now requires
  **1.4.4** or newer (was 1.2.6, and 1.4.0-rc.0 for `infra`). Callers that
  declare an older image fail the environment gate once they pin a Foundation
  revision carrying this floor. `shared` itself moves to `1.4.4-frontend`.
  Released as Foundation CI **`v2.2.0`** at `ddd2c56` (see
  `docs/governance/foundation-ci-promotion-v2.2.0.md`).
- Foundation CI **`v2.1.0` is promoted** at `53ed9cd` (see
  `docs/governance/foundation-ci-promotion-v2.1.0.md`). `v2.0.0` was tagged
  before its promotion criteria were met and is superseded; do not pin it.
- Foundation aggregator accepts a skipped gate only when the selected profile
  excludes it; gates inside the profile must succeed, so unexplained skips
  still fail `Foundation / Result`. The policy fixture now executes the real
  aggregator script.
- Python dependency adapter audits exact pins derived from `uv.lock` /
  `poetry.lock` (or `requirements.lock` / `requirements.txt`) instead of the
  runner environment, and fails when the manifest is missing.
- Rust dependency adapter uses checksum-verified `cargo-audit` 0.22.2 (0.21.2
  cannot parse the current RustSec advisory database).
- Control Plane lifecycle events and error responses now consume the canonical
  cross-engine contracts instead of defining local metadata shapes.
- Baobab-Platform now declares confirmed `baobab-erp` consumption. Its digital estate
  remains independent from its separately provisioned tenant boundary.
- Tenant identifiers are opaque `tn_` resource IDs, legal entities retain the
  uppercase registry grammar, and canonical product IDs prefer kebab case.
- The tenancy contract now records the legal entity as the default boundary
  without treating legal entity and tenant as synonyms.
- Access-token claims now require an explicit actor type and may identify an
  authorised party through `azp`.
- `Session` (`contracts/identity/v1/session.schema.json`) now carries
  authentication strength via a required `authentication_assurance`
  (`AuthenticationAssurance`) object instead of its own `assurance_level`/
  `authentication_methods` enums, so session strength and step-up decisions
  (`AssuranceRequirement`) share one OIDC `acr`/`amr` vocabulary instead of
  two. **Breaking**, though nothing in this repository or in `baobab-cp`/
  `baobab-iam` consumed the removed fields yet.
- `identity.disabled` (`contracts/identity-events/v1/identity-disabled.schema.json`)
  no longer accepts `new_status: SUSPENDED`; that transition is now the
  separate `identity.suspended` event, so a single transition can no longer
  be reported under two different event types. **Breaking**, though nothing
  in this repository consumed that value yet.

## Deprecated

- `advanced_security_enabled` (Foundation input) is **deprecated** and kept
  for one minor version: it only selects CodeQL for a repository that
  declares no `security.sast_provider`, warns when it disagrees with a
  declaration, and can no longer enable CodeQL on a private repository
  without `security.ghas`.
- Lowercase snake-case aliases for legal entities and underscore-form product
  identifiers remain accepted by Control Plane v1 only for compatibility. New
  records must use registry entity IDs and kebab-case product IDs.

## Removed

- **`legacy_metadata_enabled`** and the `.nabhold/environment.yaml` bridge
  (from the orchestrator, classifier, environment gate and product
  wrappers). Callers must drop the input when they repin; passing it to
  v2.3.0 or later fails workflow validation.

## Fixed

- Control Plane registration commands no longer accept caller-selected tenant
  identifiers; the Control Plane returns its minted opaque identifier in the
  provisioning operation.
- The shared `tenantId` schema now enforces the same opaque `tn_` grammar as
  tenancy governance.
- Legal-entity compatibility aliases are accepted only at documented input
  boundaries; responses and persisted contracts require registry identifiers.
- Control Plane product-entitlement examples now reference products declared
  by the canonical legal-entity registry.
- `baobab-cp` ADR-BCP-015 and its own Technical Specification (CR-003) had
  independently declared `baobab.<bounded-context>.<aggregate>.<event>.v<major>`
  as the canonical event-type format, contradicting the
  `com.baobab-platform.<context>.<...>.v<N>` pattern this repository already enforces
  in `contracts/events/v1/envelope.schema.json` and ships in every real
  identity/ERP/supplier-onboarding event. ADR-SHARED-008 confirms Shared's
  shipped convention as authoritative; both `baobab-cp` documents are
  corrected by reference rather than re-drafted here.
- Foundation caller template is executable as published (required inputs and
  permissions); private SAST no longer depends on a silent skip when CodeQL is
  unavailable.

## Security

- Restricted control-plane access tokens to asymmetric RS256 or ES256
  signatures, a 15-minute maximum lifetime, and explicit audience and scope
  checks.
- Foundation SAST path refuses CodeQL upload for private repositories without
  an explicit `advanced_security_enabled` opt-in, reducing accidental GHAS
  upload failures.

---

# Release Categories

Changes should be placed under one or more of the following categories.

## Added

New functionality.

Examples:

* new reusable workflows;
* new composite actions;
* new automation;
* new supported runtimes;
* new optional workflow inputs.

---

## Changed

Changes to existing functionality that are not breaking.

Examples:

* improved CI behaviour;
* performance improvements;
* updated defaults;
* additional validation;
* improved logging.

---

## Deprecated

Functionality that remains available but should no longer be used.

A deprecation entry should identify:

* the deprecated component;
* the replacement;
* migration guidance;
* expected removal version or date where known.

---

## Removed

Functionality that has been removed.

Removal should normally occur only after an appropriate deprecation period unless an urgent security issue requires immediate removal.

---

## Fixed

Bug fixes and corrections.

Examples:

* corrected workflow logic;
* fixed deployment failures;
* corrected artifact handling;
* repaired scripts;
* fixed documentation errors.

---

## Security

Security-related changes.

Examples:

* vulnerability remediation;
* action pinning;
* permission hardening;
* credential-handling improvements;
* OIDC improvements;
* dependency security updates;
* supply-chain controls.

Security entries should be sufficiently descriptive to explain the security significance without unnecessarily disclosing exploitable information.

---

# Versioning Policy

Where a shared component has a defined public interface, changes should follow semantic versioning:

```text
MAJOR.MINOR.PATCH
```

## MAJOR

Increment the major version for incompatible changes.

Examples:

* removing a workflow input;
* renaming an input;
* removing an output;
* changing an artifact contract;
* changing required secrets;
* requiring additional privileges;
* removing supported environments;
* changing behaviour in a way that requires consumer changes.

Example:

```text
v1.x.x → v2.0.0
```

---

## MINOR

Increment the minor version for backward-compatible functionality.

Examples:

* adding an optional input;
* adding a supported runtime;
* adding an optional output;
* adding additional validation that does not break valid consumers.

Example:

```text
v1.2.0 → v1.3.0
```

---

## PATCH

Increment the patch version for backward-compatible fixes.

Examples:

* correcting shell logic;
* fixing a workflow condition;
* correcting documentation;
* updating a non-breaking dependency;
* improving error handling.

Example:

```text
v1.2.1 → v1.2.2
```

---

# Shared Workflows as APIs

Reusable workflows and composite actions should be treated as **internal APIs**.

Their contracts include:

* inputs;
* outputs;
* secrets;
* permissions;
* artifacts;
* supported runners;
* supported runtimes;
* external dependencies;
* expected behaviour.

A change to any of these may affect downstream repositories and must therefore be considered when preparing a changelog entry.

---

# Breaking Changes

Breaking changes must be explicitly identified.

Example:

```markdown
### Changed

- **BREAKING:** Renamed the `python-version` input to `runtime-version`.
  Consumers using v1 must migrate to the new input before adopting v2.
```

A breaking change entry should explain:

1. what changed;
2. who is affected;
3. what consumers must do;
4. which version contains the change.

---

# Security Changes

Security changes deserve particular attention because a vulnerability in a shared workflow may affect multiple repositories.

Security entries should identify the general nature of the change without publishing sensitive exploitation details.

Example:

```markdown
### Security

- Hardened GitHub Actions permissions for deployment workflows.
- Pinned third-party Actions to immutable commit SHAs.
- Updated dependency used by the container security workflow.
```

For vulnerabilities requiring coordinated disclosure, detailed technical information should remain in the appropriate security record rather than being placed in the public changelog.

---

# Downstream Impact

When a change affects consuming repositories, the changelog should say so.

For example:

```markdown
### Changed

- Updated the deployment workflow to require the `pages: write`
  permission.
- Consumers using the affected workflow must update their workflow
  permissions before adopting the new release.
```

For significant changes, include migration instructions.

---

# Unreleased Changes

The `Unreleased` section is the staging area for changes that have entered the repository but have not yet been released.

Contributors should update it when appropriate.

When a release is created, the relevant entries should be moved from `Unreleased` into the new release section.

---

# Release Format

Released versions should follow this structure with ISO 8601 dates (`YYYY-MM-DD`).

---

# Historical Releases

Tagged infrastructure releases `v1.0.0`–`v1.4.0` exist on the repository; detailed notes for those tags predate this expanded changelog. Future releases (including Foundation `v2.0.0` once promoted) will be recorded below the `Unreleased` section in reverse chronological order.

---

# References

* Keep a Changelog
* Semantic Versioning
* BAOBAB-PLATFORM `CONTRIBUTING.md`
* BAOBAB-PLATFORM `SECURITY.md`
* BAOBAB-PLATFORM `CODEOWNERS`
* `docs/governance/foundation-ci-promotion-v2.0.0.md`
