# Changelog

All notable changes to `nabhold/shared` are documented in this file.

This changelog records changes to the shared engineering infrastructure used across the NABHOLD organisation, including:

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
  §90 anticipated but `nabhold/shared` had not yet defined.
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
- ADR-SHARED-008, confirming `com.nabhold.<context>.<...>.v<N>`
  (`contracts/events/v1/envelope.schema.json`) as the sole canonical
  event-type convention and registering the four domains above.

## Changed

- Control Plane lifecycle events and error responses now consume the canonical
  cross-engine contracts instead of defining local metadata shapes.
- Nabhold now declares confirmed `baobab-erp` consumption. Its digital estate
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
  `com.nabhold.<context>.<...>.v<N>` pattern this repository already enforces
  in `contracts/events/v1/envelope.schema.json` and ships in every real
  identity/ERP/supplier-onboarding event. ADR-SHARED-008 confirms Shared's
  shipped convention as authoritative; both `baobab-cp` documents are
  corrected by reference rather than re-drafted here.

## Security

- Restricted control-plane access tokens to asymmetric RS256 or ES256
  signatures, a 15-minute maximum lifetime, and explicit audience and scope
  checks.

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

Example:

```markdown
# Unreleased

## Added

- Added reusable Python CI workflow.

## Changed

- Standardised Python dependency installation using uv.

## Security

- Pinned all third-party GitHub Actions to immutable commit SHAs.
```

When a release is created, the relevant entries should be moved from `Unreleased` into the new release section.

---

# Release Format

Released versions should follow this structure:

```markdown
# [Unreleased]

## Added

## Changed

## Deprecated

## Removed

## Fixed

## Security


# [1.1.0] - 2026-08-15

## Added

- Added reusable documentation deployment workflow.

## Changed

- Standardised documentation builds using Zensical.

## Security

- Pinned deployment actions to immutable commit SHAs.
```

Dates should use ISO 8601 format:

```text
YYYY-MM-DD
```

---

# Release Notes

Release notes should focus on information relevant to consumers.

Avoid listing every internal commit.

A good release note answers:

* What changed?
* Why does it matter?
* Does the consumer need to do anything?
* Is the change breaking?
* Is there a security implication?

---

# Migration Notes

When a release requires consumer changes, provide a concise migration section.

Example:

```markdown
## Migration

Consumers upgrading from v1 to v2 must replace:

    old-input: value

with:

    new-input: value
```

For more complicated migrations, maintain a dedicated migration document under:

```text
docs/migrations/
```

and reference it from the changelog.

---

# Version References

Where a shared workflow or action is consumed through a version tag, the release should identify the appropriate version.

For example:

```yaml
uses: nabhold/shared/.github/workflows/python-ci.yml@v1
```

The changelog should make clear when the behaviour associated with `v1` changes and when consumers should move to `v2`.

---

# Security Releases

Security fixes may require accelerated release procedures.

A security release may:

* bypass a normal release schedule;
* require immediate consumer notification;
* require credential rotation;
* require downstream workflow updates;
* require emergency deployment;
* require temporary disabling of an affected component.

Security releases should still be recorded in this changelog after the immediate response has been completed.

---

# Dependency Updates

Routine dependency updates should generally be grouped where appropriate.

Examples:

```markdown
## Fixed

- Updated `actions/checkout` to the latest approved release.
- Updated Python documentation dependencies.
- Updated container base image.

## Security

- Updated dependency containing a known security vulnerability.
```

The changelog should distinguish ordinary maintenance from security remediation.

---

# Internal Changes

Not every internal change requires a changelog entry.

A changelog entry is generally unnecessary for:

* spelling corrections;
* minor internal refactoring with no behavioural impact;
* test-only changes;
* CI changes that affect only repository maintenance;
* formatting-only changes.

However, if a change affects consumers, security, release behaviour, or operational expectations, it should be documented.

---

# Consumer-Facing Changes

The following should normally appear in the changelog:

* workflow interface changes;
* new workflow versions;
* changed required permissions;
* changed secrets;
* changed artifacts;
* supported runtime changes;
* deployment behaviour;
* security controls;
* breaking changes;
* deprecations;
* removals;
* changes requiring consumer migration.

---

# Release Checklist

Before creating a release, maintainers should verify:

* [ ] `Unreleased` contains all relevant changes.
* [ ] Breaking changes are clearly identified.
* [ ] Security changes are documented appropriately.
* [ ] Consumer impact has been assessed.
* [ ] Migration guidance exists where necessary.
* [ ] Version number follows the applicable versioning policy.
* [ ] Release date is recorded.
* [ ] Documentation reflects the release.
* [ ] Deprecated components are identified.
* [ ] Relevant downstream repositories have been identified.

---

# Changelog Discipline

The changelog should remain useful to engineers six months after a release.

Avoid entries such as:

```text
- Fixed stuff.
- Updated things.
- Various improvements.
- More CI changes.
```

Prefer:

```text
- Fixed the documentation deployment workflow so that GitHub Pages
  artifacts are uploaded using the v4 artifact service.
```

The goal is not to produce a diary of commits.

The goal is to provide a reliable historical record of **what changed in shared NABHOLD engineering infrastructure and what those changes mean for its consumers**.

---

# Historical Releases

No releases have been published yet.

Future releases will be recorded below the `Unreleased` section in reverse chronological order.

---

# References

* Keep a Changelog
* Semantic Versioning
* NABHOLD `CONTRIBUTING.md`
* NABHOLD `SECURITY.md`
* NABHOLD `CODEOWNERS`
