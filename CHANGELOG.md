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

## Added

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

- Lowercase snake-case aliases for legal entities and underscore-form product
  identifiers remain accepted by Control Plane v1 only for compatibility. New
  records must use registry entity IDs and kebab-case product IDs.

## Removed

Nothing yet.

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
