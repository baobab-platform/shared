# ADR-SHARED-032 — EA-09 Provider Capability Certification and Pulse Activation Admission

**Status:** Accepted — Normative Certification and Activation Governance  
**Date:** 2026-10-07  
**Repository:** `baobab-platform/shared`  
**Decision ID:** ADR-SHARED-032  
**Depends On:** ADR-SHARED-017, ADR-SHARED-029, ADR-SHARED-030, ADR-SHARED-031, ADR-BCP-025  
**Applies To:** P-CAP-08 and future provider certification

## Decision

EA-09 introduces `ProviderCapabilityCertification` as a Control Plane-owned
qualification record.

A certification is bound to exactly:

```text
CapabilityProvider
      +
canonical capability
      +
contract major
      +
immutable EngineRelease
      =
ProviderCapabilityCertification
```

Certification is deliberately release-bound. A new engine release does not
inherit the certification of an older release.

## Separation of states

```text
engine repository IMPLEMENTED
        |
        | EA-09 qualification
        v
provider-capability-release CERTIFIED
        |
        | provider registration
        v
CapabilityProvider DRAFT
        |
        | PROVIDER_ACTIVATION changeset
        v
CapabilityProvider ACTIVE
        |
        | instance + binding + grant + health
        v
resolvable for an entitled context
```

None of these states implies another.

## Certification record

The canonical contract is
`contracts/capability/v1/certification.schema.json`.

The Control Plane mints the certification id and records the authenticated
certifier. The request names only:

- provider id;
- canonical capability key;
- contract major;
- engine release id;
- qualification profile;
- immutable evidence references;
- optional validity bound;
- audit reason.

Evidence is content-addressed. Credentials and raw test artifacts are never
stored in the certification record.

## Admission rules

A certification can be recorded only when:

1. the provider exists and is owned by the release's engine;
2. the capability exists in the canonical catalogue;
3. the provider declares support for that contract major;
4. the named EngineRelease belongs to the same engine;
5. that release records the exact provider/capability/contract-major support;
6. the release is not REVOKED;
7. the certifier is not the principal that recorded the release;
8. all evidence references are immutable by digest.

The release may still be CANDIDATE when certification is recorded. This is
necessary because production release approval itself may require certification;
requiring APPROVED first would create a circular dependency.

## Revocation

Certification is revocable. Revocation changes only the certification state and
records who revoked it, when and why. A revoked or expired certification never
satisfies release approval or provider activation.

Revoking certification does not silently mutate an already ACTIVE provider or
binding. Operational response to a newly invalid certification is a separate
governed remediation/change process; the Control Plane must surface the failed
readiness condition.

## Production policy

With EA-09 available, production release approval and provider activation now
require certification. Local, development and staging remain permissive unless
policy is tightened separately.

`topology/v1/release-policy.yaml` therefore sets:

```text
certification_required.production = true
```

This applies to all providers, not only Pulse.

## Pulse P-CAP-08

The first two canonical Intelligence capabilities move from lifecycle DRAFT to
ACTIVE while retaining EXPERIMENTAL maturity:

- `intelligence.evidence.search@1`
- `intelligence.research-mission.manage@1`

The lifecycle promotion means the canonical capability may participate in
resolution. It does not certify or entitle any provider.

The transitional Shared registration bundle for `baobab-pulse.core` is added
to `registration-bundles.yaml`. Registration always creates/converges the
provider as DRAFT. Only the existing PROVIDER_ACTIVATION changeset may move it
to ACTIVE.

## Pulse certification profile

Pulse P-CAP-08 uses qualification profile:

`ea-09/pulse-intelligence-v1`

Each of the two capability contract majors is certified independently against
the exact Pulse EngineRelease being activated.

Certification evidence should include at least:

- contract conformance;
- live integration evidence;
- security review;
- operability/readiness evidence.

The canonical schema intentionally permits additional evidence types.

## No automatic binding or grant

P-CAP-08 does not create tenant bindings, CapabilityGrants or consumer IAM
scope allocations.

An ACTIVE Pulse provider with no eligible binding/grant remains non-resolvable
for tenants. That is intentional.

## Invariants

**CERT-001** — Certification is provider + capability + contract-major +
EngineRelease specific.

**CERT-002** — IMPLEMENTED is not CERTIFIED.

**CERT-003** — Release APPROVED is not CERTIFIED.

**CERT-004** — Provider ACTIVE is not CERTIFIED.

**CERT-005** — Certification may be recorded against a CANDIDATE release but
never a REVOKED release.

**CERT-006** — The certifier is not the release recorder.

**CERT-007** — A revoked or expired certification cannot satisfy policy.

**CERT-008** — Production release approval requires certification.

**CERT-009** — Production provider activation requires certification of every
supported capability/major on the covering approved release.

**CERT-010** — Certification grants no tenant entitlement or binding.

**CERT-011** — Pulse registration is DRAFT; activation is changeset-governed.

**CERT-012** — The two first-census Intelligence capabilities are ACTIVE
canonical capabilities after P-CAP-08, while maturity remains EXPERIMENTAL.

## Final decision

> EA-09 is the platform qualification boundary between an engine repository's
> IMPLEMENTED claim and runtime provider activation. P-CAP-08 uses that
> boundary for baobab-pulse.core, promotes the canonical Intelligence
> capabilities to ACTIVE, registers Pulse through the existing transitional
> registration path, and permits provider activation only after release-bound
> certification and the existing topology/health checks succeed.
