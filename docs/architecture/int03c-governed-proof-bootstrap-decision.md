# INT-03C named supervised identity bootstrap and Principal lifecycle ruling

**Status: Accepted — scoped development proof bootstrap; runtime certification pending**  
**Date:** 22 October 2026  
**Governing:** EA Implementation Plan v2.3; ADR-0007 (IAM Workload Identity);
ADR-IAM-0016/0033; ADR-BCP-020/021; Accepted Shared #354 (CMS hold remains);
INT-02 proof-bootstrap precedent.

The owner authorises implementation of governed INT-03C workload identities,
canonical CP Principal-deactivation authority, and actual seven-case real
IAM ↔ CP disposable qualification. The authorisation does **not** certify a
run, register CMS proof clients, or authorise staging/production issuance.

## 23 October 2026 — development execution amendment

Accepted [ADR-SHARED-043](../adr/ADR-SHARED-043-Development-Provisioning-and-Environment-Approval-Boundaries.md)
supersedes the human approval/certification requirements below **for isolated
synthetic development only**. CP-owned bootstrap may establish synthetic actors
and enterprise state. One operator/CI job may drive distinct maker/checker
Principals; the same Principal must still be denied self-approval. Actual IAM
issuance and the seven runtime assertions may execute without Infrastructure
#49's independent human gate. Development results may be PASS with retained
real-component synthetic evidence and no protected acceptance claim. Independent
people, external custody and protected go/no-go apply when readying staging and
production. The CMS development hold is lifted within ADR-043's scope. The text
below remains the protected workflow/mechanism reference, not a prerequisite
for normal development provisioning.

## Exact identity ceilings

Two *and only two* new canonical workspaces are allowed:

| Field | Issuer owner | Independent issuer verifier |
|---|---|---|
| Client ID | `baobab-int03c-issuer-owner` | `baobab-int03c-issuer-verifier` |
| Owning repository | baobab-platform/infrastructure | baobab-platform/infrastructure |
| Environment | development | development |
| Audience | baobab-control-plane | baobab-control-plane |
| Canonical scope | context:resolve | context:resolve |
| Credential profile | client_credentials | client_credentials |
| Registry lifecycle | ACTIVE: synthetic-proof bootstrap exception | ACTIVE: synthetic-proof bootstrap exception |
| Actual use | short-lived source-verified bearer for CP | independent issuer introspection, not CP administration |

Neither client is an administrator, validator, provider-certifier,
Principal-registration service, resource owner for another Tenant, CMS
consumer or CMS validator. The verifier needs **no** CP `context:validate`
privilege: OAuth introspection is an IAM operation with independently
governed provider-side client permissions, not permission to validate
another service's Context.

The existing Shared authorization validator pins both entire rows including
their statuses, ownership, scopes, audiences and absence of extra fields.
The `ACTIVE` exception permits a fresh **development-only** token to
produce the evidence necessary for qualification. It is not a CP grant,
permission to activate an unrelated client, production access or the
independent qualification decision.

## Per-run issuance and revocation rules

- Each named client is created only by IAM's supervised disposable native
  provider configuration, with fresh per-run OS-random credentials, a
  60–900-second token lifetime, and an issuer pinned to a local verified-CA
  service. The clients do not enter production or regular Keycloak/Hydra
  bootstrap profiles.
- The issuer owner obtains a token while a distinct registered verifier
  independently introspects its issuer, client ID, audience, scope, status
  and expiry. The verifier has no authority to approve its own results.
- Revocation proof requires a positive CP request **first**, a real IAM
  revocation with independent active-to-inactive read-back before token
  expiry, and a negative CP request using the **same** bearer. Natural
  expiry, wrong audience or an unrelated 403 are not revocation.
- Separate disposable ACTIVE CP Principals and actual governed market,
  organisation, tenant, grants, release/binding and proof records must
  be admitted through CP-owned APIs, with two distinct already authorised
  CP human makers/checkers. No test harness may insert synthetic
  `identity.principal`/external identity links through SQL and call them
  live acceptance.

## Canonical CP Principal deactivation

A canonical Principal lifecycle is **CP** authority, not an IAM provider
client operation. CP must expose a new, specifically governed, initially
nonproduction-only operation with these mandatory rules:

1. The target is an existing **ACTIVE synthetic** Principal under a verified
   exact development-only issuer/subject and CP-owned run registration.
   No global Principal toggle, no production/staging enablement.
2. The requester is a real ACTIVE, canonically resolved, scoped human maker;
   a different real ACTIVE human checker approves the immutable digest
   of exact Principal, issuer, subject, expected source revision, run nonce,
   purpose, expiry and requested terminal status.
3. The approval must be bound to the current revision and execution
   transaction, with idempotent replay detection, dual-person separation,
   expiry and fail-closed checks against current CP grants. Fail on stale
   plan, mismatched target, missing independent approval or reviewer.
4. The CP mutation and immutable security audit/outbox evidence commit
   atomically. Any existing external links for that Principal become
   non-authorising. Existing issuer credentials are **not** automatically
   revoked; real IAM and CP read-backs must both be checked after mutation.
5. A new request cannot re-enable a Principal through this proof path.
   All live request authorization, cached Context and effective grants
   must stop admitting the deactivated Principal without a stale-token
   bypass. The independent reader verifies status and current denial.

If the required CP store, schema, policy or read models cannot be
established, deactivation must remain **BLOCKED**, never replaced by
fixture SQL or a locally fabricated `PRINCIPAL_INACTIVE` result.

## Independent seven-case acceptance

The seven cases are issuer issuance, current CP Principal, wrong-audience
denial, wrong-Tenant denial, issuer revocation denial before natural expiry,
canonical CP Principal deactivation denial, and independent teardown.
Every case must be observed against real pinned IAM/CP services in the
same bounded disposable run; isolated source tests are prerequisites, not
acceptance. Original sanitized evidence with SHA-256 and run/source/image
pins must be retained in an externally immutable reviewed artifact and
re-downloaded/rehash-verified by a different checker. The accepting
runtime, both issuer clients, CP owned resources, client secrets, images,
volumes and networks must be independently read back as absent or
terminal. No result is `PASS` until the entire acceptance matrix is
independently certified.

**Shared #354:** `baobab-int03-cms-consumer` and
`baobab-int03-cms-validator` remain absent/HELD. These decisions
do not activate them, and none of the 14 NAB-03 cases can be marked PASS.
