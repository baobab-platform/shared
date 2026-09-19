# Security Policy

## BAOBAB-PLATFORM Shared

`baobab-platform/shared` contains organisation-wide engineering infrastructure used by BAOBAB-PLATFORM repositories.

This may include:

* GitHub Actions workflows;
* reusable CI/CD pipelines;
* composite actions;
* deployment automation;
* security automation;
* repository automation;
* scripts;
* authentication and OIDC configuration;
* dependency and supply-chain controls.

A security defect in this repository may therefore affect **multiple BAOBAB-PLATFORM systems simultaneously**.

For that reason, security issues must be handled carefully and, where appropriate, confidentially.

---

# 1. Security Principles

Security in `baobab-platform/shared` follows these principles:

### Least Privilege

Workflows, actions, tokens, identities, and repositories should receive only the permissions they require.

### Secure by Default

Reusable components should provide safe defaults rather than requiring every consumer to implement its own security controls.

### Immutable Dependencies

Every GitHub Action reference must be pinned to a full-length commit SHA —
BAOBAB-PLATFORM policy applies this organisation-wide, with no exception for
`baobab-platform/shared`'s own reusable workflows/actions when consumed by another
repository.

### No Embedded Credentials

Secrets, credentials, tokens, private keys, and other sensitive material must never be committed to this repository.

### Explicit Trust Boundaries

Workflows must distinguish between trusted repository code and untrusted external input, particularly pull requests originating from forks.

### Short-Lived Credentials

Where supported, prefer OIDC and short-lived credentials over long-lived static credentials.

### Defence in Depth

No single security mechanism should be treated as sufficient protection for organisation-wide automation.

---

# 2. What Requires Security Attention

The following changes should be treated as security-sensitive.

## GitHub Actions

* action references;
* workflow permissions;
* reusable workflows;
* privileged jobs;
* deployment workflows;
* artifact handling;
* runner configuration.

## Authentication

* GitHub tokens;
* OIDC;
* cloud authentication;
* registry authentication;
* service identities.

## Secrets

* secret definitions;
* secret propagation;
* environment variables containing sensitive information;
* secret masking;
* external secret managers.

## Dependencies

* GitHub Actions;
* Python packages;
* Node packages;
* container images;
* operating-system packages;
* third-party CLI tools.

## Supply Chain

* action pinning;
* dependency provenance;
* artifact integrity;
* release automation;
* external downloads;
* installation scripts.

## Infrastructure

* deployment systems;
* cloud resources;
* container registries;
* infrastructure automation;
* environment promotion.

---

# 3. Reporting a Security Vulnerability

If you discover a security vulnerability, **do not disclose exploitable details in a public GitHub issue**.

This is particularly important for `baobab-platform/shared` because a vulnerability may affect multiple downstream repositories.

Where GitHub Private Vulnerability Reporting or Security Advisories are enabled for this repository, use that mechanism.

If private reporting is unavailable, contact the designated BAOBAB-PLATFORM security or platform engineering maintainers through an authorised private communication channel.

Do not use a public issue for the initial disclosure of a potentially exploitable vulnerability.

---

# 4. What to Include in a Report

A useful security report should contain as much of the following information as can safely be provided:

### Summary

A concise description of the vulnerability.

### Affected Component

Identify the affected:

* workflow;
* action;
* script;
* configuration;
* dependency; or
* infrastructure component.

### Affected Version

Provide the relevant commit, tag, or version where known.

### Impact

Explain what an attacker could potentially:

* access;
* modify;
* execute;
* impersonate;
* deploy;
* exfiltrate; or
* disrupt.

### Reproduction

Provide minimal reproduction steps where safe to do so.

### Evidence

Include relevant:

* logs;
* workflow output;
* error messages;
* configuration;
* screenshots; or
* proof-of-concept material.

Do not include live credentials or other secrets.

### Suggested Remediation

If you have a proposed fix, include it where appropriate.

---

# 5. Do Not Include Secrets

Never include the following in a vulnerability report:

* passwords;
* API keys;
* GitHub tokens;
* cloud credentials;
* private keys;
* production secrets;
* session tokens;
* personally identifiable information that is not necessary for investigation.

If sensitive information has accidentally been exposed, state that exposure has occurred without reproducing the secret itself.

The affected credential should be rotated or revoked immediately through the appropriate operational process.

---

# 6. Vulnerability Triage

Security reports should be evaluated according to:

1. exploitability;
2. affected components;
3. affected repositories;
4. privileges required;
5. confidentiality impact;
6. integrity impact;
7. availability impact;
8. likelihood of exploitation;
9. availability of mitigation;
10. downstream exposure.

Because `shared` may serve multiple repositories, impact should be assessed at the **organisation level**, not merely against the `shared` repository itself.

---

# 7. Severity

The following classification provides a practical starting point.

## Critical

A vulnerability that could provide broad unauthorised control over organisation-wide CI/CD, credentials, deployment systems, or multiple repositories.

Examples:

* arbitrary code execution with organisation-level credentials;
* compromise of a privileged reusable workflow;
* credential theft affecting multiple repositories;
* supply-chain compromise capable of affecting many consumers.

## High

A serious vulnerability capable of compromising a repository, deployment environment, workflow, or sensitive credential with meaningful privileges.

## Medium

A vulnerability with meaningful security impact but requiring additional conditions, limited privileges, or a narrower attack surface.

## Low

A security weakness with limited practical exploitability or impact.

Severity may be revised as investigation progresses.

---

# 8. Response Process

The expected response process is:

```text
Security Report
       │
       ▼
Private Triage
       │
       ▼
Validate Vulnerability
       │
       ▼
Determine Scope
       │
       ▼
Assess Severity
       │
       ▼
Develop Mitigation
       │
       ▼
Test Fix
       │
       ▼
Release Fix
       │
       ▼
Assess Downstream Consumers
       │
       ▼
Coordinate Disclosure
```

The response process should prioritise containment where active exploitation is suspected.

---

# 9. Organisation-Wide Impact

When a vulnerability affects a shared workflow or action, maintainers should identify all known consumers.

For example:

```text
baobab-platform/shared
       │
       ├── Repository A
       ├── Repository B
       ├── Repository C
       ├── Repository D
       └── Repository E
```

A fix is not complete merely because the `shared` repository is secure.

Affected consumers may require:

* workflow upgrades;
* version changes;
* credential rotation;
* deployment review;
* artifact invalidation;
* dependency updates;
* emergency configuration changes.

---

# 10. GitHub Actions Security

Reusable workflows must follow strict security practices.

## Explicit Permissions

Declare permissions explicitly.

Prefer:

```yaml
permissions:
  contents: read
```

over broad or implicit permissions.

---

## Avoid `write-all`

Do not use:

```yaml
permissions: write-all
```

unless there is a documented and unavoidable requirement.

---

## Pin Actions

All actions — third-party and `baobab-platform/shared`'s own reusable
workflows/composite actions alike — must be referenced using immutable
full-length commit SHAs. This is an organisation-wide requirement, not a
per-repository option.

Prefer:

```yaml
uses: actions/checkout@<40-character-sha> # v4.x.x
```

over:

```yaml
uses: actions/checkout@v4
```

Never use:

```yaml
uses: actions/checkout@main
```

for production organisation-wide workflows.

---

# 11. Untrusted Pull Requests

Workflows must treat pull requests from forks and other untrusted sources carefully.

Avoid exposing secrets to workflows that execute untrusted code.

In particular, use extreme caution with:

```yaml
pull_request_target
```

Do not check out and execute untrusted pull-request code within a privileged context unless the security implications are fully understood and the workflow has been deliberately designed for that purpose.

---

# 12. Secrets

Secrets must be supplied through appropriate secure mechanisms.

Never hard-code:

```yaml
TOKEN: abc123
```

or:

```yaml
password: "production-password"
```

Do not place credentials in:

* workflow files;
* scripts;
* documentation;
* examples;
* test fixtures;
* comments;
* commit messages.

Use GitHub Secrets, environment protection, OIDC, or an approved external secret-management system.

---

# 13. OIDC

Where cloud providers support GitHub OIDC, prefer it over long-lived cloud credentials.

OIDC configurations should use restrictive trust conditions based on appropriate attributes such as:

* organisation;
* repository;
* branch;
* environment;
* workflow;
* deployment context.

Do not create broad trust relationships when a narrower one is possible.

---

# 14. Dependency and Action Supply Chain

Every external dependency represents a potential supply-chain risk.

Before introducing a dependency, consider:

* source;
* maintainer;
* release history;
* security history;
* licence;
* update frequency;
* transitive dependencies;
* required privileges;
* whether the dependency is genuinely necessary.

Avoid introducing dependencies simply because they make a small task marginally easier.

---

# 15. Action Pinning

Action pinning is especially important for this repository because shared
workflows can propagate a compromised dependency to multiple consumers —
and because this repository's own `baobab-platform/shared/...@<ref>` references,
consumed by every repo in the org, are themselves subject to the same
requirement. There is no third-party-only carve-out: a floating `@v1` on
a `baobab-platform/shared` reference is exactly as unpinned as a floating `@v4` on
a third-party action.

A mutable reference such as:

```yaml
uses: some/action@v4
```

can change without a corresponding change to the consuming workflow.

A full commit SHA provides an immutable reference:

```yaml
uses: some/action@0123456789abcdef0123456789abcdef01234567
```

The associated version should be recorded in a comment:

```yaml
uses: some/action@0123456789abcdef0123456789abcdef01234567 # v4.2.1
```

The SHA must be verified against the intended upstream release. **Never invent or approximate a SHA.**

---

# 16. Dependency Updates

Security updates should not automatically be treated as harmless maintenance.

Before upgrading a shared dependency, consider:

* breaking changes;
* changed permissions;
* changed transitive dependencies;
* altered authentication behaviour;
* changed artifact semantics;
* changed runner requirements;
* changed defaults.

Security fixes should be tested before promotion to stable shared workflow versions whenever practical.

---

# 17. Artifact Security

Artifacts produced by shared workflows may contain:

* build output;
* packages;
* deployment bundles;
* reports;
* logs;
* generated documentation.

Workflows should:

* upload only necessary files;
* avoid including secrets;
* avoid unnecessarily long retention;
* use predictable artifact names;
* validate artifacts before deployment where appropriate.

Artifacts should not be treated as trusted merely because they were generated by GitHub Actions.

---

# 18. Container Security

Where shared workflows build or publish containers:

* use trusted base images;
* pin important image versions;
* avoid unnecessary packages;
* scan images where practical;
* do not embed secrets;
* use non-root execution where appropriate;
* minimise image size;
* publish provenance/SBOM information where supported.

---

# 19. Script Security

Shared scripts should:

* validate input;
* fail safely;
* avoid unsafe command construction;
* quote variables appropriately;
* avoid arbitrary remote execution;
* verify downloaded resources where practical;
* use strict error handling;
* avoid unnecessary privileges.

Shell scripts should generally use:

```bash
set -euo pipefail
```

unless there is a documented reason otherwise.

---

# 20. Security Reviews

Security review should be considered for changes involving:

* authentication;
* authorisation;
* GitHub permissions;
* secrets;
* OIDC;
* deployment;
* privileged runners;
* external code execution;
* dependency installation;
* action references;
* artifact handling;
* organisation-wide automation.

Security-sensitive changes should receive review from an appropriate security or platform owner as defined by `CODEOWNERS`.

---

# 21. Security Advisories

When a vulnerability has been confirmed and responsibly remediated, maintainers should consider whether a GitHub Security Advisory is appropriate.

The decision should take into account:

* severity;
* exploitability;
* downstream impact;
* whether public disclosure would increase risk;
* whether affected consumers have been notified;
* whether a remediation is available.

---

# 22. Emergency Response

For vulnerabilities with evidence of active exploitation or imminent risk, normal change-management procedures may be accelerated.

Potential emergency measures include:

* disabling an affected workflow;
* revoking credentials;
* rotating secrets;
* restricting repository access;
* pinning to a known-safe dependency;
* disabling a compromised action;
* suspending deployments;
* notifying affected repositories;
* issuing an emergency release.

Emergency remediation should be documented retrospectively once the immediate threat has been contained.

---

# 23. Credential Compromise

If a credential is believed to have been exposed:

1. Treat it as compromised.
2. Revoke or rotate it immediately.
3. Identify where it was used.
4. Review relevant logs.
5. Determine whether unauthorised access occurred.
6. Identify affected repositories or environments.
7. Replace the credential through the approved mechanism.
8. Document the incident.

Do not wait for proof of exploitation before rotating an exposed credential.

---

# 24. Security Incident Records

Security incidents should be documented according to BAOBAB-PLATFORM's applicable incident-management procedures.

Records should capture, where appropriate:

* incident date;
* affected systems;
* vulnerability;
* severity;
* impact;
* containment;
* remediation;
* affected consumers;
* credential rotation;
* lessons learned;
* preventive actions.

Sensitive incident information should remain appropriately restricted.

---

# 25. Responsible Disclosure

BAOBAB-PLATFORM encourages responsible disclosure.

Researchers and contributors who identify vulnerabilities are asked to:

* report privately;
* provide sufficient information to reproduce the issue;
* avoid accessing or modifying data beyond what is necessary;
* avoid disrupting services;
* allow reasonable time for remediation;
* avoid public disclosure before coordinated remediation where the vulnerability presents material risk.

---

# 26. Security Contacts

### Primary

**BAOBAB-PLATFORM Security Team**

`@baobab-platform/security`

### Platform

**BAOBAB-PLATFORM Platform Engineering**

`@baobab-platform/platform-engineering`

These teams are responsible for coordinating the assessment and remediation of security issues affecting shared engineering infrastructure.

---

# 27. Scope

This policy applies to:

* the `baobab-platform/shared` repository;
* reusable workflows maintained by the repository;
* composite actions;
* shared scripts;
* security automation;
* templates distributed from the repository;
* downstream BAOBAB-PLATFORM repositories consuming shared components where the issue originates in `shared`.

---

# 28. Out of Scope

The following should generally be reported through the appropriate system rather than this repository's security process:

* vulnerabilities entirely within an unrelated consumer repository;
* ordinary software bugs without security implications;
* feature requests;
* documentation errors;
* CI failures without security implications;
* account-access issues unrelated to this repository.

When uncertain, treat a potentially sensitive issue as a security issue and report it privately.

---

# 29. Security Is a Shared Responsibility

The `shared` repository is infrastructure.

Its consumers inherit both its capabilities and, potentially, its weaknesses.

Therefore:

> **A secure shared workflow is not merely a secure workflow. It is a security control for every repository that consumes it.**

Contributors and maintainers are expected to treat changes accordingly.

---

## Final Principle

The safest shared infrastructure is infrastructure that assumes it will eventually be attacked, misconfigured, depended upon incorrectly, and run in environments its original author never imagined.

Design accordingly.