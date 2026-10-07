# Context authority for tenant-neutral workloads: design

**Status:** APPROVED in shared#207; contracts implemented by shared#208 (control-plane/v1 1.33.0, erp/v1 1.1.0). The implementation review clarification below corrects the Control Plane contract to 1.33.1. Section 13 adds the pre-activation provisioning context purpose (control-plane/v1 1.34.0, erp/v1 1.2.0; owner ruling 2026-10-07). Runtime rollout and workload scope allocation remain separate steps.
**Date:** 2026-10-02
**Authority:** ADR-0007 sections 88-91 (workload identity: scope plus Control Plane context; "Scope is not tenant access") and its principle that independently deployable workloads have independently revocable identities, ADR-BCP-004 (context resolution and lifetime, sections 52 and 70-72), ADR-BCP-007 (signed or delegated assertions deliberately deferred), owner rulings of 2026-10-02.
**Repositories touched later:** `shared` (contracts), `baobab-cp` (redemption and validation), `baobab-erp` (consumption). `baobab-iam` issues no tenant claim; any further scope allocation follows the caller audit in section 8.

## 1. Why this is a trust-boundary change

The ERP Boundary API takes its tenant only from the access token's `tenant_id` claim. ADR-0007 sections 88-91 forbid stamping a tenant on a shared workload identity: tenant entitlement is a Control Plane decision, so a call operates in the tenant of a trusted Control Plane context. The owner has ruled that ERP therefore takes its tenant from a Control Plane context (`context_id`) and that a token `tenant_id`, when present, is only an additional binding.

Control Plane already persists such a context (`POST /v1/platform-context/resolve`, `domain.Context`). Designing ERP's consumption of it exposed that **the existing redemption of a stored context does not bind it to the caller**. That defect is fixed coherently, for every consumer, in the same design.

## 2. The existing defect (audited against `baobab-cp` main, `20235ac`)

`domain.Context` already stores `PrincipalID`, the canonical principal that resolved it (`ContextResolutionService.resolve` calls `Identity.Resolve(issuer, subject, actor_type)` and passes the result to `NewOperationContext`). Nothing reads it back when a context is consumed:

| Consumer | Route | What it checks today |
|---|---|---|
| Capability resolution | `POST /v1/capabilities/resolve`, `/resolve-batch` (`redeemContext`) | actor `workload`, scope `context:resolve`, then `resolveWorkloadTenant(token tenant, context tenant)` |
| Mapping resolution | `POST /v1/resolution/mappings` (`mapping_admin_handler.go`) | actor `workload`, scope `mapping:resolve`, then the same tenant comparison |
| Capability explanation | `POST /v1/capabilities/explain` | the handler checks actor `human` and scope `capabilities:explain`; the router additionally requires platform-administrator authority (`requireAdminRole(nil, true)`). It is deliberately platform-level diagnostics and not tenant-scoped. |

`resolveWorkloadTenant` returns `(requested, requested != "")` when the token carries no tenant. No real workload token carries one (`gate-iam-4`, baobab-iam), so for every real workload the tenant check is vacuously true. **Any workload holding `context:resolve` (or `mapping:resolve`) can redeem any stored `context_id`, whoever resolved it, and receive that tenant's capability invocation descriptors or mapping resolutions.** A `context_id` is a UUID (unguessable), but it is a bearer credential today, which it must not be.

This is not specific to ERP; the ERP design cannot be safe on top of it.

**Lifetime.** ADR-BCP-004 section 72 says a context *may* have a bounded lifetime, and nothing in the persisted-context contract requires one. The handler treats a zero TTL as unbounded. The Control Plane binary happens to bound contexts (`PLATFORM_CONTEXT_TTL` defaults to 15 minutes and rejects non-positive values), but that is configuration, not an invariant of the stored context. This paper therefore does not rely on contexts being TTL-bounded; section 4 makes boundedness a requirement for the one use that needs it.

## 3. Invariants

**I1. `context_id` is the tenant-authority carrier for tenant-neutral workload tokens.** ERP reads and the provisioning command carry a required `context_id`. A token `tenant_id` stays optional; when present it must equal the context's tenant. A request-supplied tenant is a selector, never authority.

**I2. A `context_id` is not a bearer credential.** It is usable only by the principal that owns it:

```
canonical principal of the AUTHENTICATED CALLER  ==  stored Context.PrincipalID
```

The principal is resolved by Control Plane from a token it has verified (`Identity.Resolve(issuer, subject, actor_type)`, the same function that stamped `Context.PrincipalID`). The binding is to canonical identity, not to a JWT or `jti`, so token rotation and re-issue do not break it.

**I3. The caller never names the principal.** No request field carries a principal, subject or client id as an assertion. Where Control Plane must judge a caller it did not authenticate on this call, it is given the caller's own token as cryptographic evidence (section 5), never a claim about it.

**I4. One caller-binding rule for every consumer of a persisted context.** Direct consumers and validators share a single Control Plane function for loading and judging a context. A new consumer cannot read a context without passing it.

**I5. Resolve, redeem and validate are different privileges.**
- `context:resolve` constructs a new context through Control Plane policy.
- A workload consuming **its own** context directly (capability and mapping resolution) is judged by ownership; those routes keep their current scopes in this change.
- A new scope, **`context:validate`**, lets a resource server ask Control Plane whether a context presented by *another* authenticated workload belongs to that workload. It is named for what it does: the validator does not own the context.
Neither new nor existing scopes are granted automatically to any workload.

**I6. A resource server's own identity is not its callers' identity.** ADR-0007 requires independently deployable workloads to have independently revocable identities. A resource server (here ERP) authenticates to Control Plane as itself; it never stands in for, and no caller shares credentials with, the resource server. Control Plane must therefore judge the **actual inbound caller**, not the validator.

**I7. Context authority and plan authority stay distinct.** Provisioning still requires `control_plane_authority` (`tenant_provisioning_id`, `plan_id`, `plan_version`, `plan_digest`) and the independent `ErpAssignment` comparison. A valid context never substitutes for the plan tuple, nor the tuple for a context.

**I8. No token exchange and no signed context assertion.** ADR-BCP-007 defers that complexity. No new access token is issued. Validation is introspection-style: the resource server presents the caller's token to the authority that can judge it.

**I9. Fail closed and indistinguishably.** A context that does not exist, has expired, is unbounded where a bounded one is required, or is owned by another principal answers the same `404 CONTEXT_NOT_FOUND`, so the endpoint is not an existence oracle for other principals' contexts.

**I10. A context that crosses a service boundary as authority is bounded.** `platform-context/validate` requires the context to carry an `expires_at`. ADR-BCP-004 permits bounded lifetime; this is a stricter policy for a security-sensitive use, not a change to what a context may be elsewhere.

## 4. Proposed Control Plane operation: validate a context for an inbound caller

```
POST /v1/platform-context/validate
Authorization: Bearer <VALIDATOR token: aud baobab-control-plane, scope context:validate>

{
  "context_id": "<uuid>",
  "subject_token": "<the access token that arrived at the resource server>"
}
```

Security: `workloadOidc: [context:validate]`, actor `workload`.

Two pieces of authenticated evidence are required:
1. **The validator** (`baobab-erp-workload`, or whichever workload is the resource server), authenticated by the bearer token and holding `context:validate`.
2. **The subject** (the actual caller), proved by `subject_token`, which Control Plane verifies **independently of the validator** using the configured token-validation profile. For self-contained signed tokens it verifies issuer, signature and expiry. For opaque tokens it requires a trusted introspection result from the configured issuer/provider authority confirming the token is active and unexpired. Both profiles require `actor_type` workload and an audience equal to one explicitly registered in the validator's `validates_audiences`. Independent trustworthy validation is mandatory; local signature verification is conditional on a self-contained signed token. Control Plane does not trust the validator's description of the token.

Control Plane then:
1. verifies the subject token and resolves its `(issuer, subject, actor_type)` to a canonical principal;
2. loads the context (unknown, expired, or without an `expires_at`: 404, I10);
3. requires that principal equals `Context.PrincipalID` (otherwise the same 404);
4. applies the tenant rule to the **subject token**: if it carries a `tenant_id` it must equal the context tenant (`403 TENANT_CONTEXT_MISMATCH`);
5. re-checks that the tenant is still ACTIVE at validation time (`403 TENANT_NOT_ACTIVE`), because a context outlives the resolution that proved it.

The subject token is a bearer token in transit. It is accepted only over the authenticated validator call, never stored, never logged, and not reused for anything else.

Response `200`, only the trusted facts a resource server needs:

```
{
  "context_id": "...",
  "tenant_id": "tn_...",
  "resolved_at": "...",
  "expires_at": "...",          // always present: validation requires a bounded context
  "market_id": "...",           // omitted when absent
  "organisation_id": "..."      // omitted when absent
}
```

`legal_entity_id` is deliberately **not** in the response. `Context.LegalEntityID` is the tenant's single registered legal entity (`ContextResolutionService`: "there is no multi-legal-entity-per-tenant registry yet, so 'resolve legal entity' degenerates to 'the tenant's own legal entity'"). That is a degenerate derivation, not an authoritative selection, and it is not added for ERP's convenience.

Status codes: `200`, `400 INVALID_REQUEST` (malformed `context_id`, missing or malformed `subject_token`, unknown fields), `401 AUTH_TOKEN_REQUIRED` (validator or subject token not verifiable, or the subject token's audience is not the validator's), `403 TENANT_CONTEXT_MISMATCH`, `403 TENANT_NOT_ACTIVE`, `404 CONTEXT_NOT_FOUND` (unknown, expired, unbounded or not owned: indistinguishable), `503 CONTEXT_STORE_UNAVAILABLE` (retryable).

Scope `context:validate`: audience `baobab-control-plane`, workload actors only, non-privileged, `grants_authority: false`, defined in `scope-registry.yaml`, allowed to no workload in `workload-registry.yaml` until a per-workload decision.

## 5. The global rule, by consumer

| Consumer | Authenticated caller judged | Rule |
|---|---|---|
| Capability resolution and batch | the caller itself | caller principal == `Context.PrincipalID`; keeps `context:resolve` |
| Mapping resolution | the caller itself | caller principal == `Context.PrincipalID`; keeps `mapping:resolve` |
| `platform-context/validate` (new) | the **subject token's** principal, presented by a validator | subject principal == `Context.PrincipalID`; validator needs `context:validate`; context must be bounded |
| `capabilities/explain` | a human platform administrator | **ownership does not apply**; the existing platform-administrator authority is kept unchanged. Not broadened to tenant administrators here. |

All four go through the one function of I4. Direct consumers need no subject-token forwarding because Control Plane already authenticates the actual caller.

**`capabilities/explain` stays platform-administrator only.** It is deliberately platform-level diagnostics. Broadening it to tenant administrators while fixing an unrelated redemption vulnerability would be an authorisation expansion. A tenant-scoped diagnostic belongs to a separate contract and an AdministrativeGrant decision.

**Enforcement is immediate. There is no shadow release.** The defect is concrete, the known caller (`baobab-trade`) resolves and consumes through the same Control Plane client, so it is same-principal by construction, and there is no reason to leave cross-principal redemption open to observe it. A cross-principal flow, if one exists elsewhere, fails closed and would need the governed delegation model.

## 6. The ERP flow

```
ACTUAL CALLER (CP / Trade / other workload)            baobab-erp                        Control Plane
   | 1. POST /platform-context/resolve (own CP token, context:resolve)  ------------------>  context_id, owned by the caller
   |
   | 2. ERP request: token aud=baobab-erp, scope erp:read | erp:provision,
   |                 tenant_id optional, context_id required  ------------>  |
                                                                             | 3. verify the caller's ERP token locally
                                                                             | 4. POST /platform-context/validate
                                                                             |    (ERP's own CP token, context:validate)
                                                                             |    { context_id, subject_token = the caller's token }  --->
                                                                             |                                   verify subject token, resolve its
                                                                             |                                   canonical principal, == Context.PrincipalID,
                                                                             |                                   bounded, unexpired, tenant ACTIVE,
                                                                             |                                   subject tenant_id (if any) == context tenant
                                                                             | <---------------------------------  trusted tenant_id
                                                                             | 5. reads or provisioning proceed in that tenant
```

ERP additionally compares the inbound token's `tenant_id`, when present, with the validated tenant (mismatch is 403). For provisioning, the plan tuple and `ErpAssignment` comparison then run unchanged (I7).

Properties:
- The validator is `baobab-erp-workload`; the subject is whoever called ERP. They are different identities and stay independently revocable (I6). No caller uses ERP's credential.
- Right ERP scope plus a stolen `context_id` fails: the thief's token resolves to a different principal.
- A caller holding the right ERP scope but no context of its own has nothing to present.

## 7. Negative tests pinned before implementation

Control Plane:
- `validate` with a `context_id` owned by another principal: 404, identical to unknown, expired and unbounded.
- A validator that is the context's owner but presents a subject token of a different principal: 404 (the validator's own identity is not the test).
- `validate` with a missing, malformed, expired, wrongly-signed, wrong-audience or human subject token: 400 or 401, never 200.
- A subject token whose audience is not the validator's own: 401.
- `validate` of a context without `expires_at`: 404.
- Capability resolution and mapping resolution with another principal's `context_id`: 404 (they pass today).
- A rotated token (new `jti`, same client): still resolves to the same principal and validates its own context.
- Subject token `tenant_id` equal to the context tenant: allow. Different: 403 `TENANT_CONTEXT_MISMATCH`. Absent: allow.
- Tenant suspended after resolution: 403 `TENANT_NOT_ACTIVE`.
- A caller that supplies a principal, subject or client id as a field: 400 (unknown fields are rejected).
- `context:resolve` alone cannot call `validate`; `context:validate` alone cannot call `resolve`.
- `capabilities/explain` still requires platform-administrator authority and is unaffected by ownership.

ERP:
```
missing context_id                                  -> 400
unknown, expired or unbounded context               -> reject
context owned by another principal                  -> reject
tenantless token + own context                      -> allow
token tenant_id == context tenant                   -> allow
token tenant_id != context tenant                   -> 403
right scope + stolen context_id                     -> reject
right context + wrong ERP scope                     -> 403
valid context + stale/mismatched plan tuple         -> 409 PLAN_AUTHORITY_MISMATCH, nothing provisioned
Control Plane unreachable                           -> 503 with Retry-After, nothing read or provisioned
ERP never sends its own token as the subject token  -> asserted
```

## 8. Caller matrix: audit before any further scope allocation

Granting `erp:read` and `erp:provision` only to `baobab-erp-workload` (iam#55) was safe while those scopes reached no tenant data, but **it is not the final allocation** and this design shows why: the ERP workload is the resource server's own identity (I6), not the identity of its callers. `iam#55` can stay landed; it is not treated as settled.

Before the context path is enabled, the concrete calling flows are audited and the matrix is decided, conceptually:

```
erp:provision -> the workload executing the approved Control Plane provisioning operation
erp:read      -> specifically authorised consumers of ERP reads
erp:integrate -> ERP's own internal (iDempiere) integration workload
context:validate -> the resource server doing the validating (baobab-erp-workload for ERP)
```

`baobab-erp-workload` credentials are not shared with Control Plane, Trade or any other engine. IAM and the workload registry are not changed again on a guess; they follow the audit.

## 9. Contract changes this design implies (made in later PRs, not here)

- `control-plane/v1/openapi.yaml`: `POST /platform-context/validate` and its request (`context_id`, `subject_token`) and response schemas (`platform-context.schema.json`); the direct consumers document the ownership rule and the 404.
- `authorization/v1/scope-registry.yaml`: `context:validate`; `workload-registry.yaml` unchanged in that amendment (granted to nobody); a later, audited allocation gives it to the ERP validator alone.
- `erp/v1/openapi.yaml`: required `context_id` on the reads (query) and on the provisioning request; the access-token description changes from "the resolved tenant claim is authoritative" to "tenant authority is a trusted Control Plane context; a token tenant_id, when present, must equal it". `access-token-claims.schema.json` already has `tenant_id` optional.
- Validators pin: the ownership wording on every consumer, `context:validate` registered (first granted to nobody, later to the ERP validator alone), `legal_entity_id` absent from the validate response, `expires_at` required in it, `subject_token` present in the request, `capabilities/explain` unchanged.

## 10. Implementation sequence after approval

1. Shared: the contract amendments above.
2. Control Plane: one caller-bound function; adopt it in capability resolution, mapping resolution and the new `validate` (subject-token verification, bounded-context requirement); leave `explain` as is; tests from section 7. Ownership is enforced immediately.
3. Audit the ERP caller matrix (section 8) and make the resulting scope allocations as separate, explicit decisions.
4. ERP: re-pin; `context_id` on reads and provisioning; validate through Control Plane forwarding the inbound token as subject evidence; tests from section 7.

## 11. Contract clarification after implementation review (2026-10-03)

The subject_token contract carries an OAuth access-token value, bounded to 16–8192 characters and write-only. It does not require compact JWT serialization. Missing, undersized or oversized values fail schema validation; token authenticity and validity are runtime verification decisions. Local JWT validation is the initial CP adapter capability; trusted token introspection remains permitted by ADR-IAM-0020/0021.

The validates_audiences field explicitly registers each validator-to-subject-audience relationship. Multiple independently revocable validators may register the same resource-server audience. Each validator's list remains distinct and non-empty, must exclude the Control Plane audience, and requires context:validate. No scope is allocated by this clarification.

Batch capability resolution explicitly enforces the same ownership and tenant-binding invariants as single resolution and mapping resolution.

Provisioning retries validate the fresh context before returning an idempotent replay. The context_id stays outside the request fingerprint; validated canonical principal stays in the fingerprint and validated tenant stays in the idempotency scope. An old key grants no authority.

## 12. Decisions recorded

| Question | Decision |
|---|---|
| Whose principal Control Plane judges | The **actual inbound caller's**, proved by the forwarded subject token; the validator is a separate, independently revocable identity (revised, owner 2026-10-02) |
| `capabilities/explain` | Platform-administrator only; unchanged; not broadened (revised) |
| Rollout on existing consumers | Enforce ownership immediately; no shadow release (approved) |
| Not-owned error | 404 `CONTEXT_NOT_FOUND`, indistinguishable from unknown and expired; 403 only for tenant mismatch or inactive tenant (approved) |
| Lifetime | Contexts are not universally bounded; the paper no longer claims it; contexts used as cross-service authority must be bounded (added) |

## 13. Provisioning contexts: authority before a tenant is ACTIVE (owner ruling 2026-10-07)

### 13.1 The gap

Section 4 requires the tenant to be ACTIVE at validation (`403 TENANT_NOT_ACTIVE`), and that stays the rule for every ordinary context. But the canonical lifecycle activates a tenant only after provisioning and readiness:

```
PENDING -> provisioning -> provider provisioning (including ERP) -> reconciliation -> readiness -> READY -> tenant activation -> ACTIVE
```

APPROVED, ONBOARDED, PROVISIONED, READY and ACTIVE are different facts, and the ERP provisioning that the Control Plane requests is itself part of the evidence that justifies READY and therefore activation. A context that is valid only for an ACTIVE tenant cannot carry the authority for that step, and activating the tenant first would make activation a prerequisite of its own justification. The lifecycle is therefore not reordered. Nor is the ACTIVE rule weakened into "ACTIVE or PENDING tenants may validate contexts", which would turn every ordinary context into authority over a tenant that was never approved for operation.

### 13.2 The rule: an explicit authority purpose

Every stored context has a purpose, stated and never implied (`ContextAuthorityPurpose`):

| Purpose | Created by | Acts for | Tenant must be |
|---|---|---|---|
| `RUNTIME` | `POST /v1/platform-context/resolve` (the only HTTP issuance, and it cannot ask for another purpose) | ordinary runtime operations | ACTIVE |
| `TENANT_PROVISIONING` | the Control Plane's own provisioning execution, internally; no HTTP operation creates one | exactly the operations one approved provisioning plan authorises | not suspended, decommissioning or decommissioned (a PENDING tenant is admissible) |

**P1. Narrow, not generic.** The only relaxation is for a context whose purpose is `TENANT_PROVISIONING` and that satisfies every condition below. Nothing else about validation changes: the RUNTIME rule, ownership (I2), the bounded-lifetime rule (I10) and the validator relationship (I6) all still apply.

**P2. Owned by the dedicated provisioner.** The context is owned by the canonical principal of the provisioner workload, and that workload's registry entry lists `TENANT_PROVISIONING` in `context_purposes`. Control Plane checks both: ownership by the existing caller-binding function (I4), and that the registry permits the owner's workload to hold that purpose. A workload that may provision tenants before activation holds no `context:resolve` and no `context:validate`, and uses a federated workload token, so the identity that acts before activation can never also be a runtime caller or a validator.

**P3. Short and bounded.** At most 15 minutes (`PT15M`), always with `expires_at`.

**P4. Bound to the approved plan.** The context carries `provisioning_authority` (`tenant_provisioning_id`, `plan_id`, `plan_version`, `plan_digest`), the same tuple an ERP provisioning request names in `control_plane_authority`. It means "this provisioner may perform the operations this exact approved plan authorises for this not-yet-active tenant", not merely "this workload has some context for this tenant". The resource server compares the tuple member by member; Control Plane validates that the tuple is still the current approved plan.

**P5. Admissible provisioning only.** Validation holds only while the named TenantProvisioning exists for the context's tenant, is in `PROVISIONING_PROVIDERS`, `VERIFYING_READINESS` or `REMEDIATING`, and the tuple is its approved, current plan (approval binds id, version and digest, ADR-BCP-021). A provisioning that is stale, withdrawn, cancelled, failed, blocked or in any other state, or a plan that is no longer the approved current one, is `403 PROVISIONING_AUTHORITY_NOT_CURRENT`. The authority ends when the provisioning leaves the admissible states even though the context has not expired.

**P6. Never runtime authority.** Capability resolution, batch resolution and mapping resolution accept `RUNTIME` contexts only and answer a `TENANT_PROVISIONING` context `CONTEXT_NOT_FOUND` (404), indistinguishable from an unknown one. A resource server accepts a provisioning context only for the operations the approved plan authorises: ERP accepts it for the two provisioning operations and refuses it (403 `ERP_CONTEXT_REJECTED`) for every business-data read, and refuses a `RUNTIME` context for provisioning.

**P7. Stated in every answer.** `PlatformContextValidation` always carries `authority_purpose`, and `provisioning_authority` exactly when the purpose is `TENANT_PROVISIONING`. A resource server therefore never has to infer a purpose from the tenant's lifecycle.

### 13.3 What the provisioning authority is not

It is not a grant of tenant activation, of any other capability, or of any scope: scopes remain the invocation permission (ADR-0007) and the provisioner still needs `erp:provision`, which it holds only while its registry entry and IAM client allow it. It is not a way to read a pending tenant's business data. It does not replace the ERP plan-authority comparison (I7): context authority and plan authority are independent, and both must hold.

### 13.4 Negative tests pinned before implementation

Control Plane:
```
RUNTIME context, tenant PENDING                              -> 403 TENANT_NOT_ACTIVE (unchanged)
TENANT_PROVISIONING context, tenant PENDING, admissible plan -> 200, authority_purpose and provisioning_authority present
TENANT_PROVISIONING context owned by a workload without TENANT_PROVISIONING in context_purposes -> refused, as not found
TENANT_PROVISIONING context presented with a subject token of another principal                 -> 404
TENANT_PROVISIONING context unbounded or longer than 15 minutes                                 -> 404 (never issued: creation is refused)
provisioning in VALIDATING, PLANNED, BLOCKED, FAILED, CANCELLED, READY, DEPROVISIONED            -> 403 PROVISIONING_AUTHORITY_NOT_CURRENT
plan id, version or digest differs from the approved current plan                               -> 403 PROVISIONING_AUTHORITY_NOT_CURRENT
tenant suspended, decommissioning or decommissioned                                             -> 403 TENANT_NOT_ACTIVE
capability, batch or mapping resolution with a TENANT_PROVISIONING context                      -> 404 CONTEXT_NOT_FOUND
no HTTP operation can create or request a TENANT_PROVISIONING context                           -> asserted
```

ERP:
```
provisioning POST with a RUNTIME context                                -> 403 ERP_CONTEXT_REJECTED, nothing provisioned
provisioning POST, provisioning_authority != control_plane_authority    -> 403 ERP_CONTEXT_REJECTED, nothing provisioned
provisioning GET with a context bound to another provisioning or plan   -> 403 ERP_CONTEXT_REJECTED
mapping, order-consequence or inventory read with a TENANT_PROVISIONING context -> 403 ERP_CONTEXT_REJECTED
PROVISIONING_AUTHORITY_NOT_CURRENT from Control Plane                   -> 403 ERP_CONTEXT_REJECTED (never told apart from other rejections)
```

### 13.5 Sequence

1. Shared: this amendment (control-plane/v1 1.34.0, erp/v1 1.2.0, `context_purposes` in the workload registry, validators).
2. Control Plane: persist the purpose and the tuple when the provisioning execution creates the context; apply the purpose-specific policy in `platform-context/validate`; keep every runtime path ACTIVE-only; the negative tests above.
3. Re-pin consumers (ERP validates purpose and tuple; its caller-rejection set gains the new code), then wire the provisioning worker into the provider-provisioning phase.
4. Activation of the provisioner workload remains separate and follows its own end-to-end evidence.

### 13.6 Decisions recorded

| Question | Decision |
|---|---|
| Tenant activation before ERP provisioning | Rejected: circular, since provisioning is evidence for activation (owner 2026-10-07) |
| Weaken `validate` for PENDING tenants | Rejected: would undermine the ACTIVE invariant for every context |
| Pre-activation authority | A distinct, first-class context purpose, `TENANT_PROVISIONING`, bound to the approved plan tuple, the provisioner principal and a short lifetime |

