# Context authority for tenant-neutral workloads: design

**Status:** PROPOSED for owner review. **Nothing is implemented and no contract changes in this PR.** Contract amendments, Control Plane code and ERP code follow only after this is approved.
**Date:** 2026-10-02
**Authority:** ADR-0007 sections 88-91 (workload identity: scope plus Control Plane context; "Scope is not tenant access"), ADR-BCP-004 (context resolution and lifetime, sections 52 and 70-72), ADR-BCP-007 (signed or delegated assertions deliberately deferred), owner ruling of 2026-10-02 on ERP tenant authority.
**Repositories touched later:** `shared` (contracts), `baobab-cp` (redemption), `baobab-erp` (consumption). `baobab-iam` issues no tenant claim and changes only to grant the new scope, as a separate decision.

## 1. Why this is a trust-boundary change

The ERP Boundary API takes its tenant only from the access token's `tenant_id` claim. The only ERP caller, `baobab-erp-workload`, is a shared identity that serves many tenants, and ADR-0007 sections 88-91 forbid stamping a tenant on it: tenant entitlement is a Control Plane decision, so a call operates in the tenant of a trusted Control Plane context. The owner has ruled that ERP therefore takes its tenant from a Control Plane context (`context_id`) and that a token `tenant_id`, when present, is only an additional binding.

Control Plane already persists such a context (`POST /v1/platform-context/resolve`, `domain.Context`). Designing ERP's consumption of it exposed that **the existing redemption of a stored context does not bind it to the caller**. That defect is fixed coherently, for every consumer, in the same design.

## 2. The existing defect (audited against `baobab-cp` main, `20235ac`)

`domain.Context` already stores `PrincipalID`, the canonical principal that resolved it (`ContextResolutionService.resolve` calls `Identity.Resolve(issuer, subject, actor_type)` and passes the result to `NewOperationContext`). Nothing reads it back when a context is consumed:

| Consumer | Route | What it checks today |
|---|---|---|
| Capability resolution | `POST /v1/capabilities/resolve`, `/resolve-batch` (`redeemContext`) | actor `workload`, scope `context:resolve`, then `resolveWorkloadTenant(token tenant, context tenant)` |
| Mapping resolution | `POST /v1/resolution/mappings` (`mapping_admin_handler.go`) | actor `workload`, scope `mapping:resolve`, then the same tenant comparison |
| Capability explanation | `POST /v1/capabilities/explain` | actor `human`, scope `capabilities:explain`; **no tenant or ownership check at all** |

`resolveWorkloadTenant` returns `(requested, requested != "")` when the token carries no tenant. No real workload token carries one (`gate-iam-4`, baobab-iam), so for every real workload the tenant check is vacuously true. **Any workload holding `context:resolve` (or `mapping:resolve`) can redeem any stored `context_id`, whoever resolved it, and receive that tenant's capability invocation descriptors or mapping resolutions.** A `context_id` is a UUID (unguessable), but it is a bearer credential today, which it must not be.

This is not specific to ERP; the ERP design cannot be safe on top of it.

## 3. Invariants

**I1. `context_id` is the tenant-authority carrier for tenant-neutral workload tokens.** ERP reads and the provisioning command carry a required `context_id`. A token `tenant_id` stays optional; when present it must equal the context's tenant. A request-supplied tenant is a selector, never authority.

**I2. A `context_id` is not a bearer credential.** Redeeming it requires

```
canonical principal of the authenticated workload  ==  stored Context.PrincipalID
```

The principal is resolved by Control Plane from the verified token (`Identity.Resolve(issuer, subject, actor_type)`, the same function that stamped `Context.PrincipalID`). It is never supplied by the caller. The binding is to canonical identity, not to a JWT or `jti`, so token rotation and re-issue do not break it.

**I3. The caller never names the principal being validated.** Request bodies carry the `context_id` only.

**I4. One caller-binding rule for every consumer of a persisted context.** The rule is a single function in Control Plane, used by capability resolution, mapping resolution, ERP context validation and any future redemption. A new consumer cannot read a context without passing it.

**I5. Resolve and redeem are different privileges.** `context:resolve` constructs a new context through Control Plane policy. A new scope, `context:redeem`, validates or redeems a context this principal already owns. The new scope is defined in Shared and granted to nobody automatically; granting it is a separate, per-workload decision.

**I6. Context authority and plan authority stay distinct.** Provisioning still requires `control_plane_authority` (`tenant_provisioning_id`, `plan_id`, `plan_version`, `plan_digest`) and the independent `ErpAssignment` comparison. A valid context never substitutes for the plan tuple, and the plan tuple never substitutes for a context.

**I7. No token exchange and no signed context assertion in this change.** ADR-BCP-007 defers that complexity. Synchronous Control Plane validation is sufficient.

**I8. Fail closed and indistinguishably.** A context that does not exist, has expired, or is owned by another principal answers the same `404 CONTEXT_NOT_FOUND`, so the endpoint is not an existence oracle for other principals' contexts.

## 4. Proposed Control Plane operation

```
POST /v1/platform-context/validate
Authorization: Bearer <workload token, aud baobab-control-plane, scope context:redeem>

{ "context_id": "<uuid>" }
```

Security: `workloadOidc: [context:redeem]`, actor `workload`.

Control Plane then:
1. resolves the authenticated workload to its canonical principal;
2. loads the context (unknown or expired: 404);
3. requires `Context.PrincipalID` equals that principal (otherwise the same 404);
4. applies the existing tenant rule: if the token carries a `tenant_id` it must equal the context tenant (`403 TENANT_CONTEXT_MISMATCH`);
5. re-checks that the tenant is still ACTIVE at validation time (`403 TENANT_NOT_ACTIVE`), because a context outlives the resolution that proved it.

Response `200`, only the trusted facts a resource server needs:

```
{
  "context_id": "...",
  "tenant_id": "tn_...",
  "resolved_at": "...",
  "expires_at": "...",          // omitted when the context is unbounded
  "market_id": "...",           // omitted when absent
  "organisation_id": "..."      // omitted when absent
}
```

`legal_entity_id` is deliberately **not** in the response. `Context.LegalEntityID` is the tenant's single registered legal entity (`ContextResolutionService`: "there is no multi-legal-entity-per-tenant registry yet, so 'resolve legal entity' degenerates to 'the tenant's own legal entity'"). That is a degenerate derivation, not an authoritative selection, and it is not added for ERP's convenience. It can be added when a real selection exists.

Status codes: `200`, `400 INVALID_REQUEST` (malformed `context_id`), `401 AUTH_TOKEN_REQUIRED`, `403 TENANT_CONTEXT_MISMATCH`, `403 TENANT_NOT_ACTIVE`, `404 CONTEXT_NOT_FOUND` (unknown, expired or not owned: indistinguishable), `503 CONTEXT_STORE_UNAVAILABLE` (retryable).

Scope `context:redeem`: audience `baobab-control-plane`, workload actors only, non-privileged, `grants_authority: false`, defined in `scope-registry.yaml`, allowed to no workload in `workload-registry.yaml` until a per-workload decision.

## 5. The global redemption rule

All consumers use one function, conceptually `RedeemOwnedContext(ctx, principal, contextID)`: resolve the caller's canonical principal, load, require ownership, apply the tenant rule, return the trusted context.

| Consumer | Change |
|---|---|
| Capability resolution and batch | ownership enforced; keeps `context:resolve` for now |
| Mapping resolution | ownership enforced; keeps `mapping:resolve` for now |
| ERP context validation (new) | ownership enforced; requires `context:redeem` |
| Capability explanation (human administrator) | **not** an ownership case: an administrator explaining another principal's context is legitimate diagnosis. It is the "explicitly governed delegation" case and must instead require administrative authority over the context's tenant (platform administrator, or tenant administrator of that tenant), which it does not check today. Its exact authority check is an open question below. |

Existing workload consumers keep their current scope in this change and move to `context:redeem` one workload at a time (a later governed step), so adopting the ownership rule does not wait on, or force, a scope rollout.

**Real callers are already same-principal.** `baobab-trade` resolves a context and redeems it through the same Control Plane client (`src/baobab/control-plane/client.ts`), so enforcing ownership does not break the known flow. A cross-principal flow, if one exists elsewhere, would fail closed and need the governed delegation model, which is out of scope here.

## 6. The ERP flow

```
caller (baobab-erp-workload)
   | 1. POST /v1/platform-context/resolve      (CP-audience token, context:resolve)
   v
Control Plane  -> context_id, owned by the caller's canonical principal
   |
   | 2. ERP request: token aud=baobab-erp, scope erp:read | erp:provision,
   |                 tenant_id optional, context_id required
   v
baobab-erp
   | 3. verify the ERP token (issuer, audience, workload actor, scope)
   | 4. POST /v1/platform-context/validate     (ERP's own CP-audience token, context:redeem)
   v
Control Plane: exists, unexpired, caller principal == Context.PrincipalID,
               tenant ACTIVE, token tenant (if any) == context tenant
   v
trusted tenant_id  ->  ERP reads or provisioning proceed in that tenant
```

ERP additionally compares the inbound ERP token's `tenant_id`, when present, with the validated tenant (mismatch is 403). For provisioning, the plan tuple and `ErpAssignment` comparison then run unchanged (I6).

### Decision needed: whose principal does CP authenticate?

In step 4 Control Plane authenticates **ERP's** workload token, so the ownership check compares the context to ERP's principal, not to the inbound caller's. In v1 the only holder of `erp:read` and `erp:provision` is `baobab-erp-workload`, which is also the principal ERP validates as, so the inbound caller, the context owner and the validating principal are the same canonical identity and the binding holds.

If a different workload were later allowed `erp:read`, it could present a `context_id` owned by `baobab-erp-workload` and ERP's own validation would succeed, because the check authenticates ERP and not that caller. **So this design requires ERP to reject any inbound token whose client is not the principal it validates as**, and treats allowing another caller as a governed delegation design (a Control Plane operation that validates on behalf of a named caller, with its own authorisation), explicitly out of scope. This closes the gap between "ERP calls CP as its registered workload" and "right scope plus stolen `context_id` is rejected". Owner review is requested on this point.

## 7. Negative tests pinned before implementation

Control Plane:
- `validate` with a `context_id` owned by another principal: 404, identical to unknown and expired.
- Capability resolution and mapping resolution with another principal's `context_id`: 404 (they pass today).
- A rotated token (new `jti`, same client): still validates its own context.
- Token `tenant_id` equal to the context tenant: allow. Different: 403 `TENANT_CONTEXT_MISMATCH`. Absent: allow.
- Tenant suspended after resolution: 403 `TENANT_NOT_ACTIVE`.
- A caller that supplies a principal or subject in the body: 400 (unknown fields are rejected).
- `context:resolve` alone cannot call `validate`; `context:redeem` alone cannot call `resolve`.

ERP:
```
missing context_id                          -> 400
unknown or expired context                  -> reject
context owned by another principal          -> reject
tenantless token + own context              -> allow
token tenant_id == context tenant           -> allow
token tenant_id != context tenant           -> 403
right scope + stolen context_id             -> reject
right context + wrong ERP scope             -> 403
token from a client ERP does not validate as -> 403 even with a valid context
valid context + stale/mismatched plan tuple -> 409 PLAN_AUTHORITY_MISMATCH, nothing provisioned
Control Plane unreachable                   -> 503 with Retry-After, nothing read or provisioned
```

## 8. Contract changes this design implies (made in later PRs, not here)

- `control-plane/v1/openapi.yaml`: `POST /platform-context/validate` and its request and response schemas (`platform-context.schema.json`); the consumed-context operations document the ownership rule and the 404.
- `authorization/v1/scope-registry.yaml`: `context:redeem`; `workload-registry.yaml` unchanged (granted to nobody).
- `erp/v1/openapi.yaml`: required `context_id` on the reads (query) and on the provisioning request; the access-token description changes from "the resolved tenant claim is authoritative" to "tenant authority is a trusted Control Plane context; a token tenant_id, when present, must equal it". `access-token-claims.schema.json` already has `tenant_id` optional.
- Validators pin: the ownership wording on every consumer, `context:redeem` registered and granted to no workload, `legal_entity_id` absent from the validate response.

## 9. Implementation sequence after approval

1. Shared: the contract amendments above.
2. Control Plane: one caller-bound redemption function; adopt it in capability resolution, mapping resolution and the new `validate`; the administrator authority check on `explain`; tests from section 7.
3. ERP: re-pin; `context_id` on reads and provisioning; validate through Control Plane; reject non-owner callers; tests from section 7.
4. IAM and registry: grant `context:redeem` to `baobab-erp-workload` (a separate, explicit decision), then move other workloads to it one at a time.

## 10. Open questions for the reviewer

1. **Section 6:** confirm that v1 restricts the ERP Boundary API to `baobab-erp-workload` (ERP rejects any other inbound client) and that cross-caller validation is deferred to a governed delegation design.
2. **`explain`:** confirm the check should be administrative authority over the context's tenant (platform administrator, or tenant administrator of that tenant), not ownership. It is a behaviour change for an existing route.
3. **Rollout of the ownership rule on existing consumers:** the recommendation is to enforce immediately, because contexts are TTL-bounded and the known caller (`baobab-trade`) is same-principal by construction. The alternative is one release in shadow mode with an `owner_mismatch` outcome counter before enforcing. This leaves the defect open for that release.
4. **Error shape:** the not-owned case answers 404, where capability and mapping resolution answered 403 `TENANT_CONTEXT_MISMATCH` for a tenant mismatch. Confirm the 403 stays only for a token-tenant mismatch.
