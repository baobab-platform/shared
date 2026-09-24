# BAOBAB-PLATFORM Shared

> **Organisation-wide shared workflows, pipelines, contracts, packages, automation, configuration, and engineering standards for the BAOBAB-PLATFORM GitHub ecosystem.**

**Repository:** `baobab-platform/shared`
**Visibility:** Private
**Scope:** BAOBAB-PLATFORM Organisation
**Status:** Foundational / Internal Infrastructure

---

## Foundation 4 repository baseline

This repository owns the reusable GitHub and contract-compatibility gates used
across all eleven Baobab-Platform repositories. Its Codespaces environment uses the
`baobab-dev` v1.4.4 `frontend` profile because Shared builds Node-based contract
packages but no deployable service.

Every consuming repository must provide a `.baobab/environment.yaml`, use an
`baobab-dev` v1.4.4 or newer development profile (the floor in
`.baobab/environment-profiles.json`), commit dependency lockfiles, pin GitHub
Actions to full commit SHAs, and call the reusable Foundation Repository Gates.
Those gates perform dependency review, source/dependency/secret scanning,
conditional container build scanning, environment-contract validation, and
reproducibility checks. Branch protection remains a GitHub repository setting;
the required check is named `foundation` and must be required on `main`.
Administrators should apply the documented [Foundation 4 branch-protection
ruleset](docs/governance/foundation-4-branch-protection.md).

---

## Overview

`baobab-platform/shared` is the central repository for **versioned organisational
contracts and reusable engineering infrastructure across the BAOBAB-PLATFORM
organisation**.

It is also the source of truth for portable API, event, identity, tenancy, and
environment schemas. It contains no deployable server or environment. Runtime
implementation belongs to the consuming application; infrastructure
implementation belongs to `baobab-platform/infrastructure`.

It exists to prevent individual repositories from independently reinventing the same CI/CD pipelines, GitHub Actions workflows, automation scripts, security controls, configuration patterns, operational conventions, API contracts, data schemas, and common libraries.

The repository provides a controlled foundation that can be consumed by BAOBAB-PLATFORM projects, products, platforms, and subsidiaries — both as **importable code** (via reusable workflows, composite actions, and versioned packages) and as **agreed interfaces** (via contracts and schemas that multiple services and repositories depend on).

The principle is simple:

> **Build common engineering capabilities once, govern them centrally, and reuse them consistently.**

This repository should therefore be treated as **organisation infrastructure**, rather than as an ordinary application repository.

---

## Why This Repository Exists

As the BAOBAB-PLATFORM technology estate grows, individual repositories will inevitably need many of the same capabilities:

- Continuous Integration
- Continuous Deployment
- Documentation deployment
- GitHub Pages deployment
- Python dependency management
- JavaScript/TypeScript builds
- Docker image builds
- Security scanning
- Dependency auditing
- Code quality checks
- Release automation
- Version management
- Artifact handling
- Infrastructure validation
- Pull-request validation
- Repository hygiene
- Dependency updates
- Supply-chain security
- Environment validation
- Scheduled maintenance
- Notifications and operational automation

They will also inevitably need to **agree on shapes**, not just processes:

- What a tenant, user, or audit event looks like as JSON
- What an API error response looks like
- What fields a log line or a metric must carry
- What a service's public interface promises to callers

Copying workflows — or re-deriving interfaces — from repository to repository creates a predictable problem:

```
Repository A ──┐
Repository B ──┤
Repository C ──┼──> Duplicated CI/CD logic AND divergent interfaces
Repository D ──┤
Repository E ──┘
```

Over time, the implementations diverge. One repository gets a security improvement. Another remains on an older action. A third uses a different Python version. A fourth has subtly different permissions. One service's error responses use `error_code`; another uses `code`. One service's audit log omits the actor's tenant ID.

That is technical debt disguised as configuration — and, in the case of contracts, technical debt disguised as an API.

The `shared` repository exists to establish a common foundation:

```
             ┌────────────────────────────────────┐
             │           BAOBAB-PLATFORM Shared            │
             │                                      │
             │ Workflows        API Contracts        │
             │ Pipelines        Data Schemas         │
             │ Actions          Event Definitions     │
             │ Scripts          Packages (TS/JS)      │
             │ Standards        Observability Specs   │
             │ Security Controls   Compliance Schemas │
             │ Templates        IaC Modules           │
             └──────────────────┬───────────────────┘
                                 │
      ┌──────────────────────────┼──────────────────────────┐
      │                          │                          │
      ▼                          ▼                          ▼
┌──────────┐              ┌──────────┐              ┌──────────┐
│ Baobab   │              │ ZuriBeans│              │ Other    │
│ Platform │              │          │              │ Projects │
└──────────┘              └──────────┘              └──────────┘
```

---

# Objectives

The repository has eight primary objectives.

## 1. Standardisation

Provide common implementation patterns for recurring engineering tasks.

Repositories should not need to invent their own CI/CD architecture, error format, or logging shape unless there is a legitimate project-specific requirement.

---

## 2. Reuse

Enable repositories throughout BAOBAB-PLATFORM to consume common workflows, automation, contracts, and packages without copying implementation code or re-deriving interfaces from scratch.

Where GitHub supports reusable workflows, those should generally be preferred over duplication. Where a data shape or API interface is consumed by more than one repository, it should be defined once here.

---

## 3. Security

Centralise security-conscious implementation patterns, particularly around:

- GitHub Actions permissions
- Immutable action pinning
- Dependency management
- Secret handling
- OIDC authentication
- Artifact management
- Supply-chain security
- Container security
- Dependency vulnerability scanning

Security improvements made here should be capable of benefiting multiple repositories.

---

## 4. Maintainability

Reduce the number of independently maintained workflow implementations and independently maintained copies of the same interface.

A change to a common process, error shape, or event schema should ideally require changing one centrally maintained implementation rather than dozens of repositories.

---

## 5. Governance

Establish organisation-wide conventions for how BAOBAB-PLATFORM repositories:

- build;
- test;
- package;
- release;
- deploy;
- document;
- scan;
- version;
- classify and handle data; and
- maintain software.

---

## 6. Engineering Enablement

Make the correct engineering approach the easiest approach.

The repository should provide **paved roads**, not bureaucratic obstacles. Project teams should be able to adopt established engineering practices — and established interfaces — with minimal configuration.

---

## 7. Interface Consistency

Ensure that services and repositories which need to talk to one another, or to be operated the same way, agree on the same shapes: API contracts, event payloads, error responses, and identifiers.

A consumer of a BAOBAB-PLATFORM service should be able to rely on the same conventions regardless of which service, repository, or team produced it.

---

## 8. Data & Compliance Governance

Provide a common vocabulary for data classification, audit logging, and regulatory obligations (including South African requirements such as POPIA) so that compliance posture does not depend on each repository independently reinventing it.

---

# Scope

The repository may contain organisation-wide resources in the following categories.

## Shared GitHub Actions Workflows

Reusable workflows for common repository operations, such as:

- Python CI
- Node.js / TypeScript CI
- Flutter CI
- Django CI
- FastAPI CI
- Docker builds
- Container publishing
- Documentation builds
- GitHub Pages deployment
- Release workflows
- Pull-request validation
- Scheduled maintenance
- Security scanning
- Dependency auditing

Example:

```
jobs:
  ci:
    uses: baobab-platform/shared/.github/workflows/python-ci.yml@<sha-for-v1.x.x> # v1.x.x
```

---

## Shared Composite Actions

Where a reusable workflow is not appropriate, common task-level operations may be implemented as composite actions.

Examples include:

- installing `uv`;
- configuring Python;
- configuring Node;
- authenticating to registries;
- validating repository structure;
- generating release metadata;
- running security checks.

---

## Shared Scripts

Organisation-wide shell, Python, or other automation scripts may be maintained here where they have legitimate reuse across multiple repositories.

Scripts should remain:

- deterministic;
- documented;
- testable;
- portable where practical;
- dependency-conscious; and
- safe to execute in CI.

---

## API & Interface Contracts

`contracts/` holds the agreed shapes that more than one repository or service depends on. This is what keeps independently developed services interoperable without runtime coordination.

Current cross-engine contracts include:

- **OpenAPI specifications** for Control Plane operations consumed by other engines.
- **AsyncAPI specifications** for Control Plane lifecycle messages.
- **The canonical CloudEvents 1.0 envelope** in `contracts/events/v1`, including tenant scope, correlation, causation, idempotency and W3C trace context.
- **RFC 9457 problem details** in `contracts/errors/v1` for cross-engine HTTP errors.
- **Command and event idempotency rules** in `contracts/idempotency/v1`.
- **Vendor-neutral ERP boundary contracts** in `contracts/erp/v1`, including
  OpenAPI queries/provisioning, AsyncAPI consequences, explicit temporal
  mappings, international value types and the system-of-record matrix.
- **JSON Schema definitions** for shared data shapes — e.g. tenant object, user object, audit event.
- **GraphQL schema fragments and shared types**, where applicable.
- **gRPC / Protocol Buffer definitions**, for service-to-service calls that require them.
- **Identifier and claim contracts** — JWT claim shapes, OIDC scope definitions, tenant/session object shape.

A contract is a promise to consumers. Changing one is equivalent to changing a public API and must follow the same versioning and backwards-compatibility discipline as a reusable workflow (see [Design Principles](#design-principles) and [Versioning Strategy](#versioning-strategy)).

---

## Shared Packages

`packages/` is a pnpm/Turborepo-managed workspace of versioned, publishable TypeScript/JavaScript packages consumed by BAOBAB-PLATFORM repositories. Candidates include:

- `@baobab-platform/eslint-config`, `@baobab-platform/tsconfig`, `@baobab-platform/prettier-config` — organisation-wide lint, type-checking, and formatting baselines.
- `@baobab-platform/types` — shared TypeScript types generated from, or hand-aligned with, the contracts in `contracts/`.
- `@baobab-platform/api-client` — a typed client for calling BAOBAB-PLATFORM services, generated from their OpenAPI contracts where practical.
- `@baobab-platform/ui-tokens` — shared design tokens (colour, spacing, typography) for future frontend and mobile work.
- Small, dependency-conscious utility packages (date/time helpers, validators, tenant-context helpers) that would otherwise be copy-pasted between repositories.

A package belongs here only once a second consumer genuinely needs it — see [Relationship With Product-Level Shared Directories](#relationship-with-product-level-shared-directories).

---

## Observability Contracts

Shared specifications so that logs, metrics, and traces are interpretable the same way regardless of which service produced them:

- Structured logging schema — required fields (timestamp, service, tenant, correlation ID, severity) and their names.
- Metric-naming conventions.
- Trace-context propagation standards.
- OpenTelemetry semantic-convention extensions specific to BAOBAB-PLATFORM, where the standard conventions are insufficient.

---

## Compliance & Data Contracts

Shared vocabulary and schemas that support regulatory and governance obligations across the organisation:

- A data-classification taxonomy (e.g. public / internal / confidential / restricted, with explicit PII handling tiers).
- A standardised audit-log event schema, so that "who did what, to what, when" is captured the same way in every service — this is both an engineering convenience and part of the organisation's POPIA compliance posture.
- Common validation rules and enums relevant to the jurisdictions BAOBAB-PLATFORM operates in (e.g. South African ID number and phone number formats, currency and locale codes).

---

## Infrastructure-as-Code Modules

Reusable Terraform modules and related infrastructure definitions, so that infrastructure patterns are not re-derived per repository once more than one deployable service exists:

- Common modules (VPC, RDS, S3, ECS/EKS patterns).
- Base Kubernetes manifests / Helm chart templates.
- Environment-promotion patterns (distinct from environment-specific *values*, which must never live here — see [What Does *Not* Belong Here](#what-does-not-belong-here)).

---

## Testing Contracts

Assets that let repositories verify they still honour the contracts above without full end-to-end integration:

- Consumer-driven contract tests (e.g. Pact-style) between services, once more than one service calls another.
- Shared test fixtures and mock-data generators aligned with the schemas in `contracts/`.
- Shared load-testing scripts, where genuinely reusable.

---

## Configuration

Common configuration may include:

- Dependabot configuration patterns;
- CodeQL configuration;
- security scanning configuration;
- linting configuration;
- repository metadata;
- release configuration;
- workflow configuration;
- automation configuration.

Project-specific configuration should remain in the consuming repository.

---

## Templates

The repository may provide templates for:

- workflows;
- issue forms;
- pull requests;
- release processes;
- security reporting;
- repository bootstrapping;
- documentation;
- development environments;
- new-service scaffolding (e.g. a generalised equivalent of a per-project `scaffold_*.py` script).

Templates should be used where central reuse is not technically appropriate.

---

# What Does *Not* Belong Here

Centralisation is useful, but not everything belongs in `shared`.

The repository should **not become a dumping ground**.

The following generally belong in their respective project repositories:

### Application code

Business logic and application-specific implementation belong in the consuming project.

### Product documentation

Product-specific documentation belongs in the product repository.

### Project-specific workflows

A workflow that genuinely depends on unique project architecture should remain with that project.

### Single-consumer contracts or types

An API shape, schema, or type used by exactly one repository is not yet a shared contract — it should stay local until a second consumer needs it (see below).

### Secrets

Secrets must **never** be committed to this repository.

### Credentials

API keys, passwords, private certificates, tokens, and other credentials must never be stored here.

### Environment-specific configuration

Configuration containing environment-specific operational values should normally remain outside this repository and be supplied through appropriate GitHub, cloud, or infrastructure mechanisms. This includes IaC *values* (account IDs, environment-specific sizing) as distinct from the reusable *modules* themselves.

---

# Relationship With Product-Level Shared Directories

Individual product repositories (for example `baobab/shared/`) may maintain their own internal `shared/` directory for APIs, contracts, schemas, and utilities used *within that repository's own services*.

That is expected and correct — not everything needs to be an organisation-wide concern on day one.

A contract, schema, or package should graduate from a product-level `shared/` into `baobab-platform/shared` when, and only when:

1. **A second repository** — not merely a second service inside the same repository — genuinely needs it; and
2. The interface is stable enough to accept the versioning and backwards-compatibility discipline described in this document.

Until both conditions are met, the asset should remain local. Promoting something too early creates coordination overhead without a second real consumer to justify it; promoting it too late causes silent, divergent copies to accumulate. When in doubt, leave it local and revisit once a second consumer appears.

---

# Design Principles

## DRY — Don't Repeat Yourself

Common behaviour — and common interfaces — should have one authoritative implementation wherever practical.

---

## Secure by Default

Reusable workflows must assume that repositories should operate under the principle of least privilege.

For example:

```
permissions:
  contents: read
```

should be preferred over broad permissions unless additional access is demonstrably required.

---

## Immutable Dependencies

GitHub Actions must be pinned to full-length commit SHAs. This is an
organisation-wide requirement and applies to every `uses:` reference without
exception — third-party actions (`actions/checkout`), and **baobab-platform/shared's
own reusable workflows and composite actions**, wherever they're consumed
from another repository (`uses: baobab-platform/shared/...@<sha>`). A floating tag,
a branch name, or `@main` are all disallowed as the checked-in reference,
regardless of source.

Avoid:

```
uses: actions/checkout@v4
```

```
uses: baobab-platform/shared/.github/workflows/python-ci.yml@v1
```

Prefer:

```
uses: actions/checkout@<40-character-commit-sha> # v4.x.x
```

```
uses: baobab-platform/shared/.github/workflows/python-ci.yml@<40-character-commit-sha> # v1.x.x
```

with the release version (or, if no tag exists yet for `baobab-platform/shared`,
"main HEAD" and the verification date) documented in a comment. Verify the
SHA live against the upstream tag rather than trusting a marketplace
listing or a previous PR — see `templates/caller-*.yml` for examples of
this comment style in practice.

A repository can enforce this automatically in CI rather than relying on
review alone — see [`enforce-action-pinning.yml`](https://github.com/baobab-platform/shared/blob/main/.github/workflows/enforce-action-pinning.yml) and `templates/caller-enforce-action-pinning.yml`. This repository dogfoods
its own check via [`ci.yml`](https://github.com/baobab-platform/shared/blob/main/.github/workflows/ci.yml), which calls `enforce-action-pinning.yml` locally on every push/PR touching `.github/workflows/` or `.github/actions/` — nothing here is exempt just
because it's the source of the policy rather than a consumer of it.

Published packages under `packages/` follow the analogous discipline for
consumers: pin to an exact published version, not a floating range, for
anything security- or interface-sensitive.

This provides both:

1. immutable execution; and
2. human-readable release traceability.

## Dependency Updates (Dependabot)

Pinning to a SHA stops an action from changing under you silently — it
doesn't, by itself, get you the update. `.github/dependabot.yml` is how a
pinned reference actually moves forward: Dependabot opens a PR bumping
the SHA (and the version comment) whenever the upstream tag/branch it was
pinned against advances, so a human still reviews and merges each change
rather than it happening invisibly.

Dependabot configuration cannot be centralized the way reusable
workflows/actions can. `.github/dependabot.yml` is read directly by
GitHub's Dependabot service at that literal path in each repository —
there's no `workflow_call`-equivalent import mechanism, and no `uses:` syntax a repo's config can reference to pull in another repo's config.
Given that constraint, this repository provides the closest practical
equivalent:

- [`templates/dependabot.yml`](https://github.com/baobab-platform/shared/blob/main/templates/dependabot.yml) — the canonical
config, copied into a consuming repo's `.github/dependabot.yml` and
adjusted for TODOs (timezone, default branch).
- [`enforce-dependabot-config.yml`](https://github.com/baobab-platform/shared/blob/main/.github/workflows/enforce-dependabot-config.yml) — a reusable **workflow** (this part *can* use `workflow_call`, since
it's an Actions check, not a Dependabot config) that validates a
consuming repo's actual `.github/dependabot.yml` still satisfies the
org's structural requirements — `version: 2`, a `github-actions` ecosystem entry present, and every declared entry having a schedule,
an open-PR limit, labels, and a commit-message prefix. It deliberately
does not enforce exact values (schedule cadence, label wording,
timezone) since those legitimately vary by team; only structural
completeness is checked. Adopt it via
`templates/caller-enforce-dependabot-config.yml`.

This repository dogfoods that check too, via the `dependabot-config` job
in [`ci.yml`](https://github.com/baobab-platform/shared/blob/main/.github/workflows/ci.yml).

---

## Explicit Over Clever

Shared infrastructure is consumed by people who did not necessarily write it.

Prefer straightforward workflows, contracts, and packages over clever abstractions.

A few extra lines of YAML — or a slightly more verbose schema — are cheaper than several hours of debugging an opaque abstraction.

---

## Backwards Compatibility

Reusable workflows are APIs. So are contracts, and so are published packages.

Changing their inputs, outputs, behaviour, permissions, fields, or assumptions can break downstream repositories.

Changes must therefore be treated with the same care as changes to a public software interface.

---

## Version Everything

Reusable workflows, actions, contracts, and packages should be versioned.

Consumers should preferably reference a stable major release line — but,
per the [Immutable Dependencies](#immutable-dependencies) policy, pinned to
that release's commit SHA (for workflows/actions) or exact version (for
packages) rather than the floating tag or range:

```
uses: baobab-platform/shared/.github/workflows/python-ci.yml@<sha-for-v1.x.x> # v1.x.x
```

while major-version branches/tags are maintained deliberately as the
human-readable label for that SHA.

Breaking changes should result in a new major version.

---

# Versioning Strategy

Shared workflows, contracts, and packages should follow semantic-versioning principles where practical.

```
MAJOR.MINOR.PATCH
```

### MAJOR

Breaking interface or behavioural changes.

Examples:

- removed input;
- renamed input;
- changed required secret;
- changed expected artifact;
- incompatible runner;
- changed output contract;
- removed or renamed a contract field;
- changed a field's type or meaning;
- removed a package export.

### MINOR

Backward-compatible functionality.

Examples:

- new optional input;
- additional validation;
- additional supported runtime;
- new optional contract field;
- new package export.

### PATCH

Backward-compatible fixes.

Examples:

- corrected shell logic;
- dependency update;
- documentation correction;
- security fix that does not change the interface;
- contract description/documentation correction that does not change the schema.

For reusable workflows, major-version tags (`v1`, `v2`, ...) are still cut
and maintained, and remain the human-readable way to talk about a release
line — but per the [Immutable Dependencies](#immutable-dependencies) policy,
the reference actually checked into a caller's workflow file must resolve
that tag to its full-length commit SHA at the time of pinning:

```
uses: baobab-platform/shared/.github/workflows/python-ci.yml@<sha-for-v1.x.x> # v1.x.x
```

not the floating tag itself. Consumers re-pin (bump the SHA and comment)
to pick up new patch/minor releases within the same major line; Dependabot
(configured in this repository, see `.github/dependabot.yml`) opens these
bump PRs automatically once a tag exists to track.

Contracts and packages follow the same major/minor/patch discipline, with
`changeset-config.json` driving versioning and changelog generation for
the `packages/` workspace.

---

# Security Model

Because this repository contains infrastructure capable of affecting multiple repositories — including the interfaces they depend on to interoperate — it should be considered **high-value internal infrastructure**.

Changes must therefore receive appropriate review.

## Minimum Security Expectations

Shared workflows should:

- use least-privilege permissions;
- avoid unnecessary secrets;
- prefer OIDC over long-lived cloud credentials where supported;
- pin third-party actions;
- validate external inputs;
- avoid executing untrusted pull-request content with privileged credentials;
- avoid exposing secrets to forked pull requests;
- minimise write permissions;
- avoid unnecessary network access;
- document security-sensitive behaviour.

Shared contracts and packages should additionally:

- avoid encoding secrets, credentials, or environment-specific values as example data;
- treat any PII-bearing field in a schema as requiring the classification tier defined in the compliance contracts, and document it as such.

---

# Secrets

Secrets must never be committed to the repository.

Use the appropriate GitHub mechanism:

- organisation secrets;
- repository secrets;
- environment secrets;
- GitHub OIDC;
- external secret managers.

Reusable workflows must explicitly document any secrets they expect.

Example:

```
on:
  workflow_call:
    secrets:
      DEPLOY_TOKEN:
        required: true
```

A workflow should request only the secrets it actually needs.

---

# Permissions

Permissions should be explicitly declared.

For example:

```
permissions:
  contents: read
```

If a workflow needs additional privileges, they should be declared deliberately and documented.

Avoid relying on implicit repository-level defaults.

---

# Repository Structure

The exact structure may evolve, but the repository should generally follow a predictable layout:

```
shared/
├── .github/
│   ├── workflows/
│   │   ├── ci/
│   │   ├── cd/
│   │   ├── security/
│   │   ├── documentation/
│   │   └── maintenance/
│   │
│   ├── actions/
│   │   └── <composite-actions>/
│   │
│   ├── ISSUE_TEMPLATE/
│   └── dependabot.yml
│
├── contracts/
│   ├── control-plane/v1/
│   ├── development-environment/
│   ├── errors/v1/
│   ├── events/v1/
│   ├── idempotency/v1/
│   ├── infrastructure/v1/
│   ├── legal-entity/
│   └── tenancy/
│
├── packages/
│   ├── eslint-config/
│   ├── tsconfig/
│   ├── types/
│   ├── api-client/
│   └── ui-tokens/
│
├── observability/
│   ├── logging/
│   ├── metrics/
│   └── tracing/
│
├── compliance/
│   ├── classification/
│   └── audit-schema/
│
├── infrastructure/
│   └── terraform-modules/
│
├── scripts/
│   ├── ci/
│   ├── release/
│   ├── security/
│   └── maintenance/
│
├── templates/
│   ├── workflows/
│   ├── repositories/
│   └── documentation/
│
├── docs/
│   ├── architecture/
│   ├── workflows/
│   ├── contracts/
│   ├── security/
│   └── operations/
│
├── README.md
├── CONTRIBUTING.md
├── SECURITY.md
├── CHANGELOG.md
├── CODEOWNERS
├── package.json
├── pnpm-workspace.yaml
├── turbo.json
└── changeset-config.json
```

The structure should remain **purpose-driven**. Directories should not be created merely because the structure looks impressive.

---

# Consuming Shared Workflows

A consuming repository should use a reusable workflow rather than copying it whenever the workflow is sufficiently generic.

Example:

```
name: CI

on:
  pull_request:
  push:
    branches:
      - main

jobs:
  ci:
    uses: baobab-platform/shared/.github/workflows/python-ci.yml@<sha-for-v1.x.x> # v1.x.x
```

If inputs are required:

```
jobs:
  ci:
    uses: baobab-platform/shared/.github/workflows/python-ci.yml@<sha-for-v1.x.x> # v1.x.x
    with:
      python-version: "3.13"
      test-command: "pytest"
```

Project-specific behaviour should be supplied through documented inputs rather than hard-coded into the shared workflow.

---

# Consuming Shared Contracts & Packages

Contracts under `contracts/` are consumed by reference, not by copy-paste: a service implementing an interface, or generating a client from an OpenAPI/AsyncAPI spec, should point at a tagged version of this repository rather than duplicating the schema inline.

Packages under `packages/` are consumed as ordinary versioned npm/pnpm dependencies, published from this repository's `packages/` workspace:

```
"dependencies": {
  "@baobab-platform/types": "^1.x.x",
  "@baobab-platform/api-client": "^1.x.x"
}
```

As with workflows, security- or interface-sensitive packages should be pinned to an exact version rather than a floating range, with intentional upgrades reviewed like any other dependency bump.

---

# Workflow Contract

Every reusable workflow should document its contract.

At minimum:

| Property           | Description                   |
| ------------------ | ------------------------------ |
| Purpose            | What the workflow does        |
| Trigger            | How the workflow is invoked   |
| Inputs             | Accepted configuration        |
| Secrets            | Required secrets              |
| Permissions        | Required GitHub permissions   |
| Outputs            | Values exposed to callers     |
| Artifacts          | Artifacts produced            |
| Runners            | Required runner environment   |
| Dependencies       | External dependencies         |
| Failure conditions | Conditions that cause failure |
| Version            | Current workflow version      |
| Breaking changes   | Compatibility considerations  |

This documentation is particularly important because reusable workflows behave like internal APIs — and every schema in `contracts/` should document the equivalent: purpose, fields, required vs. optional, version, and breaking-change history.

---

# Testing Shared Workflows

Changes to shared workflows must be tested before they are promoted to a stable release.

Testing should include, where applicable:

1. YAML syntax validation.
2. Action reference validation.
3. Permission validation.
4. Reusable workflow invocation.
5. Representative consumer repositories.
6. Security checks.
7. Artifact creation.
8. Failure-path behaviour.

Changes to contracts and packages should additionally include:

9. Schema/contract validation against representative payloads.
10. Consumer-driven contract tests against known consumers, where they exist.
11. A documented compatibility assessment (does this change require a MAJOR bump?).

A workflow — or contract — that is syntactically valid but unusable by consumers is not considered successfully tested.

---

# Release Process

Changes should normally follow:

```
Change
  │
  ▼
Pull Request
  │
  ▼
Review
  │
  ▼
Validation
  │
  ▼
Merge
  │
  ▼
Release
  │
  ▼
Version
  │
  ▼
Consumer Adoption
```

Breaking changes should receive particular attention and must not be silently introduced into an existing major release.

---

# Deprecation

Shared workflows, contracts, and packages should not be removed abruptly when downstream repositories depend on them.

A normal deprecation process should be:

```
Introduce replacement
        │
        ▼
Mark old workflow/contract/package deprecated
        │
        ▼
Notify consumers
        │
        ▼
Provide migration guidance
        │
        ▼
Monitor adoption
        │
        ▼
Remove after agreed sunset period
```

Deprecation notices should identify:

- affected workflow, contract, or package;
- replacement;
- migration instructions;
- deadline;
- breaking changes;
- responsible maintainers.

---

# Ownership

The `shared` repository should have explicit ownership.

Critical files and directories should be covered by `CODEOWNERS`.

Example:

```
/.github/              @baobab-platform/platform-engineering
/actions/              @baobab-platform/platform-engineering
/scripts/              @baobab-platform/platform-engineering
/contracts/            @baobab-platform/platform-engineering @baobab-platform/architecture
/packages/             @baobab-platform/platform-engineering
/observability/        @baobab-platform/platform-engineering
/compliance/           @baobab-platform/security @baobab-platform/legal
/infrastructure/       @baobab-platform/platform-engineering
/security/             @baobab-platform/security
```

The actual teams should be substituted for the organisation's real GitHub teams.

---

# Contribution Guidelines

Contributors should ask one question before adding anything:

> **Is this genuinely reusable across multiple BAOBAB-PLATFORM repositories?**

If the answer is no, the code — or contract — probably belongs in the consuming project (see [Relationship With Product-Level Shared Directories](#relationship-with-product-level-shared-directories)).

Before contributing a shared workflow, contract, or package:

- identify its intended consumers;
- define its interface;
- minimise required inputs;
- minimise required permissions;
- document secrets;
- pin external actions;
- test the workflow or validate the contract;
- document compatibility;
- consider versioning;
- consider failure behaviour;
- consider whether the change requires notifying existing consumers.

---

# Change Management

Shared infrastructure changes require greater discipline than ordinary application changes because a single defect — or a single breaking contract change — can affect multiple repositories.

Changes should be categorised as:

- **Breaking**
- **Feature**
- **Fix**
- **Security**
- **Maintenance**
- **Documentation**

Security fixes should be prioritised appropriately and may require expedited release procedures.

---

# Recommended Repository Labels

The following labels are recommended for issues and pull requests in `baobab-platform/shared`.

## Type

| Label                | Purpose                                                  |
| -------------------- | ---------------------------------------------------------|
| `type:feature`       | New capability                                           |
| `type:fix`           | Bug or defect correction                                 |
| `type:security`      | Security-related change                                  |
| `type:maintenance`   | Routine maintenance                                      |
| `type:refactor`      | Internal restructuring without intended behaviour change |
| `type:documentation` | Documentation-only change                                |
| `type:breaking`      | Breaking change                                          |
| `type:deprecation`   | Deprecation or removal                                   |
| `type:automation`    | Automation-related change                                |

## Area

| Label                 | Purpose                       |
| ---------------------- | ------------------------------|
| `area:actions`        | GitHub Actions                |
| `area:workflows`      | Reusable workflows            |
| `area:ci`             | Continuous Integration        |
| `area:cd`             | Continuous Deployment         |
| `area:security`       | Security infrastructure       |
| `area:dependencies`   | Dependency management         |
| `area:release`        | Release automation            |
| `area:documentation`  | Documentation infrastructure  |
| `area:containers`     | Docker/container workflows    |
| `area:python`         | Python tooling                |
| `area:node`           | Node.js/TypeScript tooling    |
| `area:flutter`        | Flutter tooling                |
| `area:infrastructure` | Infrastructure automation     |
| `area:scripts`        | Shared scripts                |
| `area:templates`      | Repository/workflow templates |
| `area:github`         | GitHub platform configuration |
| `area:contracts`      | API/event/data contracts      |
| `area:packages`       | Published TS/JS packages      |
| `area:observability`  | Logging/metrics/tracing specs |
| `area:compliance`     | Data classification/audit     |

## Priority

| Label               | Purpose                                    |
| -------------------- | -------------------------------------------|
| `priority:critical` | Immediate attention required               |
| `priority:high`     | Significant operational or security impact |
| `priority:medium`   | Normal priority                            |
| `priority:low`      | Can be scheduled later                     |

## Status

| Label                  | Purpose                                      |
| ------------------------| ----------------------------------------------|
| `status:blocked`       | Cannot proceed due to an external dependency |
| `status:in-progress`   | Currently being implemented                  |
| `status:needs-review`  | Awaiting review                              |
| `status:needs-testing` | Implementation requires validation           |
| `status:ready`         | Ready for implementation                     |
| `status:stale`         | No recent activity                           |

## Security

| Label                    | Purpose                                 |
| --------------------------| ------------------------------------------|
| `security:vulnerability` | Confirmed vulnerability                 |
| `security:hardening`     | Security improvement                    |
| `security:supply-chain`  | Dependency/action supply-chain security |
| `security:permissions`   | GitHub permissions/security boundary    |
| `security:secrets`       | Secret-handling concern                 |
| `security:oidc`          | OIDC/authentication security            |

## Dependencies

| Label                        | Purpose                         |
| ------------------------------| ----------------------------------|
| `dependencies:github-action` | GitHub Action dependency        |
| `dependencies:python`        | Python dependency                |
| `dependencies:node`          | Node/npm dependency             |
| `dependencies:container`     | Container/base-image dependency |
| `dependencies:tooling`       | Development/CI tooling          |

## Compatibility

| Label                               | Purpose                               |
| --------------------------------------| ----------------------------------------|
| `compatibility:breaking`            | Breaking compatibility change         |
| `compatibility:backward-compatible` | Backward-compatible change            |
| `compatibility:consumer-impact`     | Requires downstream repository action |

---

# Label Naming Convention

Labels use a namespace format:

```
namespace:value
```

For example:

```
type:security
area:workflows
area:contracts
priority:high
security:supply-chain
```

This makes labels easier to search, filter, automate, and interpret consistently.

Avoid creating arbitrary labels such as:

```
urgent
important
workflow issue
security thing
```

Prefer the structured namespace.

---

# Governance

The `shared` repository should be governed as an internal platform.

That means:

- changes should be reviewed;
- security-sensitive changes should receive appropriate scrutiny;
- breaking changes should be explicitly identified;
- reusable workflows and contracts should have documented interfaces;
- dependencies should be kept current;
- deprecated interfaces should be managed deliberately;
- consumers should not be surprised by changes.

The repository should favour **predictability over novelty**.

---

# Relationship With BAOBAB-PLATFORM Projects

`baobab-platform/shared` is intended to sit beneath the organisation's application and product repositories as a common engineering and interface layer.

Conceptually:

```
           BAOBAB-PLATFORM ORGANISATION
                     │
                     ▼
         ┌───────────────────────┐
         │     baobab-platform/shared     │
         │                        │
         │ CI/CD                  │
         │ Security               │
         │ Automation             │
         │ Standards              │
         │ Tooling                │
         │ Contracts & Schemas    │
         │ Packages               │
         │ Observability Specs    │
         │ Compliance Schemas     │
         └────────────┬───────────┘
                       │
      ┌────────────────┼────────────────┐
      │                │                │
      ▼                ▼                ▼
┌────────┐        ┌────────┐        ┌────────┐
│ Baobab │        │ Zuri   │        │ Future │
│        │        │ Beans  │        │ Repos  │
└────────┘        └────────┘        └────────┘
```

The shared repository should provide the **common engineering and interface foundation**, while individual repositories retain responsibility for their own business logic and product-specific behaviour.

---

# Repository Classification

`baobab-platform/shared` should be considered:

**Category:** Internal Platform / Engineering Infrastructure
**Visibility:** Private
**Criticality:** High
**Consumers:** BAOBAB-PLATFORM repositories and approved organisation projects
**Primary Function:** Reusable engineering automation, contracts, and governance

---

# Roadmap

The repository may progressively evolve toward the following capabilities.

### Foundation

- [ ] Reusable CI workflows
- [ ] Reusable CD workflows
- [ ] Security workflows
- [ ] Documentation workflows
- [ ] Release workflows
- [ ] Standard action pinning
- [ ] Standard permissions model
- [ ] Repository templates

### Interfaces & Data

- [ ] Core API contracts (OpenAPI) for existing services
- [ ] Standard error-response contract
- [ ] Audit-log event schema
- [ ] Data-classification taxonomy
- [ ] AsyncAPI contracts once multi-service events exist
- [ ] `@baobab-platform/types` package generated from contracts

### Developer Experience

- [ ] Standard development environment checks
- [ ] Language-specific CI templates
- [ ] Container build templates
- [ ] Release automation
- [ ] Dependency update automation
- [ ] `@baobab-platform/eslint-config`, `@baobab-platform/tsconfig` packages

### Security

- [ ] CodeQL integration
- [ ] Dependency vulnerability scanning
- [ ] Secret scanning guidance
- [ ] Supply-chain controls
- [ ] OIDC patterns
- [ ] SBOM generation
- [ ] Container scanning

### Platform Engineering

- [ ] Standard deployment workflows
- [ ] Cloud authentication patterns
- [ ] Infrastructure validation
- [ ] Reusable Terraform modules
- [ ] Environment promotion workflows
- [ ] Organisation-wide operational automation
- [ ] Consumer-driven contract testing across services

---

# Guiding Principle

The purpose of `shared` is not to centralise everything.

It is to **centralise what should be common**.

A good shared component — whether a workflow, a contract, or a package — should provide:

> **One implementation, many consumers, clear ownership, explicit contracts, secure defaults, and predictable versioning.**

If a component cannot satisfy those characteristics, it should probably remain local to the project that needs it.

---

## Maintainers

**BAOBAB-PLATFORM Engineering / Platform Team**

For changes affecting organisation-wide workflows, security controls, deployment infrastructure, contracts, or reusable workflow interfaces, obtain appropriate maintainer review before merging.

---

## License

This repository is private and proprietary to **BAOBAB-PLATFORM**.

No content in this repository should be copied, redistributed, or reused outside authorised BAOBAB-PLATFORM projects without explicit permission.

---

## Internal Use

This repository is intended for authorised BAOBAB-PLATFORM personnel, systems, and repositories.

Because workflows, contracts, and packages contained here may execute with elevated privileges — or be relied upon as interfaces — across other repositories, treat changes to this repository as changes to **shared organisational infrastructure**.
