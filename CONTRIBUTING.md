# Contributing to BAOBAB-PLATFORM Shared

Thank you for contributing to `baobab-platform/shared`.

This repository provides shared engineering infrastructure for the BAOBAB-PLATFORM organisation, including reusable GitHub Actions workflows, composite actions, CI/CD pipelines, automation scripts, security controls, templates, and engineering standards.

Because changes made here may affect multiple repositories simultaneously, contributions must be approached as **platform changes**, not ordinary project-level changes.

> **Build once. Reuse everywhere. Change deliberately.**

---

# 1. Before You Contribute

Before adding or modifying anything, determine whether the proposed change genuinely belongs in `baobab-platform/shared`.

A good candidate is something that:

* is required by multiple BAOBAB-PLATFORM repositories;
* implements an organisation-wide engineering standard;
* eliminates meaningful duplication;
* provides reusable CI/CD functionality;
* improves organisation-wide security;
* standardises repository operations; or
* provides infrastructure that individual repositories should consume rather than recreate.

A poor candidate is something that:

* serves only one application;
* contains product-specific business logic;
* depends heavily on one repository's architecture;
* requires extensive project-specific configuration; or
* exists merely because copying it into another repository would be inconvenient.

When in doubt, favour **local implementation over unnecessary centralisation**.

Centralisation has a cost. A shared component that nobody genuinely needs is technical debt with a fancy address.

---

# 2. Contribution Principles

Contributions to this repository should follow these principles.

## 2.1 Reusability

Shared components should have clearly defined consumers and a meaningful reuse case.

---

## 2.2 Secure by Default

Security should be the default rather than an optional enhancement.

Contributions should:

* use least-privilege permissions;
* minimise secrets;
* avoid unnecessary write access;
* use OIDC where appropriate;
* pin all actions to full-length commit SHAs — third-party actions AND
  `baobab-platform/shared`'s own reusable workflows/composite actions when
  consumed from another repository;
* validate untrusted inputs;
* avoid exposing credentials to untrusted code;
* avoid unnecessary network access.

---

## 2.3 Explicit Interfaces

Reusable workflows are internal APIs.

Inputs, outputs, secrets, permissions, artifacts, and behavioural assumptions should be explicit.

---

## 2.4 Backwards Compatibility

Existing consumers must not be broken without deliberate versioning and migration planning.

Breaking changes require a new major version where the component follows semantic versioning.

---

## 2.5 Predictability

Shared infrastructure should favour predictable, boring behaviour over clever abstractions.

The person debugging a failed deployment at 02:00 will thank you.

---

## 2.6 Documentation

If a contribution changes how consumers use a shared component, the documentation must change with the implementation.

Undocumented behaviour is not a feature.

---

# 3. Repository Structure

The repository may contain:

```text
shared/
├── .github/
│   ├── workflows/
│   ├── actions/
│   ├── ISSUE_TEMPLATE/
│   └── dependabot.yml
│
├── actions/
├── scripts/
├── templates/
├── docs/
│
├── README.md
├── CONTRIBUTING.md
├── SECURITY.md
├── CHANGELOG.md
└── CODEOWNERS
```

Contributors should preserve a clear separation between:

* workflows;
* reusable actions;
* scripts;
* templates;
* documentation; and
* governance.

Do not introduce new top-level directories without a clear architectural reason.

---

# 4. Branching

Contributions should normally be made through feature branches.

Recommended naming:

```text
feature/<short-description>
fix/<short-description>
security/<short-description>
refactor/<short-description>
docs/<short-description>
maintenance/<short-description>
```

Examples:

```text
feature/python-ci
fix/pages-deployment
security/pin-actions
refactor/workflow-structure
docs/workflow-versioning
maintenance/update-uv
```

Keep branches focused on a single logical change.

---

# 5. Pull Requests

All substantive changes should be submitted through a pull request.

A pull request should clearly explain:

1. **What changed**
2. **Why it changed**
3. **Which consumers are affected**
4. **Whether the change is breaking**
5. **How it was tested**
6. **Whether documentation was updated**
7. **Whether a release/version change is required**

A good pull request should allow a reviewer to understand the change without reconstructing the author's thought process from the commits.

---

# 6. Pull Request Scope

Keep pull requests small and focused.

Prefer:

```text
PR #1
Add reusable Python CI workflow
```

over:

```text
PR #1
Add Python CI, redesign Docker builds, update security,
change release process, reorganise documentation and
upgrade every dependency
```

The latter may contain good ideas. It is still a terrible pull request.

Separate unrelated changes.

---

# 7. Reusable Workflow Requirements

Every reusable workflow should define its contract.

At minimum, document:

* purpose;
* trigger;
* inputs;
* secrets;
* permissions;
* outputs;
* artifacts;
* runner requirements;
* external dependencies;
* expected failure conditions;
* supported versions;
* compatibility considerations.

For example:

```yaml
on:
  workflow_call:
    inputs:
      python-version:
        description: Python version
        required: false
        type: string
        default: "3.13"
```

Avoid hard-coding values that consumers reasonably need to configure.

---

# 8. GitHub Actions Security

Every GitHub Action reference must comply with BAOBAB-PLATFORM's action-pinning
policy — this is organisation-wide and has no third-party carve-out. It
applies equally to third-party actions and to `uses: baobab-platform/shared/...`
references from consuming repositories.

Use a complete 40-character commit SHA for every `uses:` reference.

Prefer:

```yaml
uses: actions/checkout@<full-commit-sha> # v4.x.x
```

and

```yaml
uses: baobab-platform/shared/.github/workflows/python-ci.yml@<full-commit-sha> # v1.x.x
```

over:

```yaml
uses: actions/checkout@v4
```

```yaml
uses: baobab-platform/shared/.github/workflows/python-ci.yml@v1
```

and never use floating references such as:

```yaml
uses: actions/checkout@main
```

The release/version should be retained in a comment so maintainers can
identify the human-readable release corresponding to the immutable SHA.

This is enforced automatically, not just by review — see
`.github/workflows/enforce-action-pinning.yml` and
`templates/caller-enforce-action-pinning.yml` for the reusable CI check
consuming repositories can adopt.

---

# 9. Permissions

Reusable workflows must explicitly define the permissions they require.

Prefer:

```yaml
permissions:
  contents: read
```

over broad permissions.

Do not grant:

```yaml
permissions: write-all
```

unless there is an exceptional, documented reason.

If a workflow requires elevated privileges, explain why in the workflow and in the pull request.

---

# 10. Secrets

Never commit:

* passwords;
* API keys;
* private keys;
* access tokens;
* cloud credentials;
* certificates containing private material;
* `.env` files containing secrets;
* production credentials.

If a workflow requires a secret, define it explicitly through the appropriate GitHub mechanism.

A reusable workflow should request only the secrets it actually needs.

---

# 11. OIDC and Cloud Authentication

Where supported, prefer short-lived identity through GitHub OIDC over long-lived cloud credentials.

Contributors introducing cloud authentication should document:

* identity provider;
* required permissions;
* trust relationship;
* expected repository/environment;
* required GitHub permissions;
* required cloud-side configuration.

Do not introduce static cloud credentials merely because they are easier to configure.

---

# 12. Dependency Management

Dependencies used by shared workflows and automation should be maintained deliberately.

This includes:

* GitHub Actions;
* Python packages;
* Node packages;
* container images;
* command-line tools;
* base images;
* external services.

Dependency updates should be reviewed for:

* security implications;
* compatibility;
* breaking changes;
* licensing;
* reproducibility;
* downstream consumer impact.

---

# 13. Testing

A contribution is not complete merely because the YAML parses.

Testing should be appropriate to the change.

## Workflow changes

Validate:

* YAML syntax;
* action references;
* permissions;
* workflow inputs;
* workflow outputs;
* artifact behaviour;
* expected failure paths.

## Scripts

Validate:

* successful execution;
* invalid input;
* missing dependencies;
* failure handling;
* exit codes.

## Security changes

Validate:

* intended permissions;
* secret handling;
* authentication;
* access boundaries;
* failure behaviour.

## Documentation

Check:

* links;
* examples;
* commands;
* filenames;
* workflow references;
* version references.

---

# 14. Testing With Consumer Repositories

Because shared workflows are consumed externally, testing should include at least one realistic consumer where practical.

A successful local test does not necessarily demonstrate that:

```text
Consumer Repository
        │
        ▼
Reusable Workflow
        │
        ▼
GitHub Runner
        │
        ▼
External Services
```

will work correctly.

Where a change affects a widely used workflow, test against representative consumers before release.

---

# 15. Workflow Versioning

Shared workflows should be treated as versioned interfaces.

Where semantic versioning is used:

```text
MAJOR.MINOR.PATCH
```

### Major

Breaking interface or behaviour.

### Minor

Backward-compatible functionality.

### Patch

Backward-compatible fixes.

Breaking changes should not silently replace the behaviour of an existing major release.

---

# 16. Breaking Changes

Examples of breaking changes include:

* removing an input;
* renaming an input;
* changing an input's meaning;
* removing an output;
* changing artifact names;
* changing required secrets;
* requiring additional permissions;
* changing the expected runner;
* removing supported runtimes;
* changing deployment semantics.

Breaking changes must:

1. be clearly identified;
2. be reviewed;
3. be documented;
4. have migration guidance;
5. receive an appropriate version increment.

---

# 17. Deprecation

Do not remove a shared workflow immediately when a replacement exists.

A normal deprecation process should be:

```text
Replacement introduced
        ↓
Old interface marked deprecated
        ↓
Consumers notified
        ↓
Migration guidance published
        ↓
Consumers migrate
        ↓
Old interface removed
```

Deprecation should include an expected sunset date where practical.

---

# 18. Commit Messages

Use clear, concise commit messages.

Recommended format:

```text
type(scope): description
```

Examples:

```text
feat(workflows): add reusable Python CI
fix(pages): correct deployment artifact
security(actions): pin third-party actions
refactor(ci): simplify workflow inputs
docs(workflows): document release process
chore(deps): update setup-uv
```

Use imperative language where practical:

```text
Add Python CI workflow
```

rather than:

```text
Added Python CI workflow
```

---

# 19. Labels

Pull requests and issues should use the repository's standard labels.

Examples:

```text
type:feature
type:fix
type:security
type:breaking

area:workflows
area:security
area:ci
area:cd

priority:high
priority:medium

security:supply-chain
security:permissions
```

Labels should describe the nature, area, priority, and impact of a change.

---

# 20. Review Requirements

At least one appropriate CODEOWNER should review changes affecting shared infrastructure.

Additional review may be required for:

* security controls;
* privileged workflows;
* deployment automation;
* organisation-wide authentication;
* secrets;
* breaking changes;
* release mechanisms.

The objective is not to create bureaucracy.

The objective is to prevent one bad line of YAML from becoming an organisation-wide incident.

---

# 21. Security-Sensitive Changes

Security-sensitive changes should be identified explicitly in the pull request.

Examples:

* GitHub permissions;
* OIDC configuration;
* authentication;
* secrets;
* deployment credentials;
* action pinning;
* dependency vulnerabilities;
* container security;
* supply-chain controls.

When a vulnerability is suspected, do **not** disclose sensitive details in a public issue or ordinary pull request.

Follow the process described in `SECURITY.md`.

---

# 22. Documentation Requirements

Update documentation when a change affects:

* consumer configuration;
* workflow inputs;
* workflow outputs;
* secrets;
* permissions;
* supported runtimes;
* deployment behaviour;
* versioning;
* migration procedures.

The README should explain the repository at a high level.

Individual workflows should explain their own interfaces and operational assumptions.

---

# 23. Adding a New Shared Workflow

Before creating a new reusable workflow, answer:

### Why is it shared?

Identify at least one realistic consumer and preferably multiple potential consumers.

### What problem does it solve?

State the problem in terms of consumer repositories rather than implementation details.

### What is the interface?

Define:

* inputs;
* secrets;
* outputs;
* permissions;
* artifacts.

### What is configurable?

Expose only values consumers genuinely need to control.

### What should remain standardised?

Do not expose configuration merely because it is technically possible.

### What happens when it changes?

Define compatibility and versioning expectations.

---

# 24. Adding a New Composite Action

A composite action should be used when a reusable sequence of steps is more appropriate than an entire workflow.

The action should have:

* `action.yml`;
* clear inputs;
* documented outputs;
* explicit dependencies;
* failure behaviour;
* usage documentation;
* tests where practical.

Keep composite actions narrowly focused.

A composite action that does twenty unrelated things is probably several actions wearing a trench coat.

---

# 25. Adding Shared Scripts

Shared scripts should:

* fail safely;
* use explicit error handling;
* validate inputs;
* return meaningful exit codes;
* avoid unnecessary global state;
* document dependencies;
* work consistently in CI;
* avoid machine-specific assumptions where practical.

Shell scripts should generally use:

```bash
set -euo pipefail
```

unless there is a documented reason not to.

---

# 26. Pull Request Checklist

Before submitting a pull request, confirm:

* [ ] The change genuinely belongs in `baobab-platform/shared`.
* [ ] The implementation is reusable.
* [ ] Inputs and outputs are documented.
* [ ] Required permissions are explicit.
* [ ] Third-party actions are pinned appropriately.
* [ ] No secrets or credentials are committed.
* [ ] Security implications have been considered.
* [ ] Tests have been performed.
* [ ] Consumer impact has been considered.
* [ ] Documentation has been updated.
* [ ] Breaking changes are identified.
* [ ] Versioning implications are understood.
* [ ] Relevant labels have been applied.
* [ ] The pull request has a clear description.

---

# 27. Maintainer Checklist

Maintainers reviewing a contribution should consider:

### Architecture

* Does this belong in the shared repository?
* Is the abstraction genuinely reusable?
* Is the interface appropriately narrow?

### Security

* Are permissions minimal?
* Are actions pinned?
* Are secrets handled correctly?
* Is untrusted input isolated?

### Compatibility

* Could existing consumers break?
* Is a new major version required?
* Is migration guidance necessary?

### Operations

* What happens when the workflow fails?
* What happens when an external dependency changes?
* Is rollback possible?

### Maintenance

* Who owns the component?
* Is the documentation sufficient?
* Are dependencies maintainable?

---

# 28. Release Checklist

Before releasing a shared workflow:

* [ ] Tests pass.
* [ ] Consumer compatibility has been considered.
* [ ] Documentation is current.
* [ ] Changelog is updated.
* [ ] Version impact is identified.
* [ ] Security implications are reviewed.
* [ ] Required CODEOWNER approvals are obtained.
* [ ] Release/tag is created correctly.
* [ ] Migration guidance exists for breaking changes.

---

# 29. Questions and Discussions

For normal engineering questions, use the appropriate GitHub issue or discussion mechanism configured for the repository.

Before opening a new issue:

1. Search existing issues.
2. Check the documentation.
3. Determine whether the problem is specific to one consumer or genuinely shared.
4. Provide reproducible information.

Include:

* repository/consumer;
* workflow/action name;
* version;
* runner;
* relevant error;
* expected behaviour;
* actual behaviour;
* reproduction steps.

---

# 30. Code of Conduct

Contributors are expected to behave professionally and respectfully.

Technical disagreement is healthy.

Personal attacks, harassment, deliberate disruption, or attempts to circumvent security controls are not acceptable.

The objective is to build reliable infrastructure, not to win arguments.

---

# 31. Final Principle

`baobab-platform/shared` exists to make BAOBAB-PLATFORM engineering **more consistent, secure, maintainable, and efficient**.

Every contribution should therefore pass a simple test:

> **Does this make the organisation's engineering foundation better for the repositories that consume it?**

If yes, contribute it.

If it only makes one repository more convenient, put it in that repository.

That distinction is what keeps a shared platform useful rather than turning it into a warehouse of miscellaneous YAML.