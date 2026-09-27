# Administrative authority contracts v1

**Authority:** ADR-BCP-020 (Administrative Authority, Delegated Administration, Privileged Access and Separation-of-Duties Model), gate ADA-01.
**Runtime owner:** `baobab-platform/baobab-cp` persists grants and evaluates every administrative request (sections 130-131). This package defines their shape only.

Administrative authority answers one question: may this principal perform this Control Plane administrative action on this resource, now? It is not product entitlement: a capability says what a tenant may consume, an administrative permission says what an administrator may do (section 9).

## Files

- `domain.schema.json`: identifier grammars and closed enumerations: grant and decision ids, principal ids, permission and profile keys, permission domains, risk classes, scope levels and modes, grant status, type and source, decision outcomes.
- `permission-registry.yaml`: the canonical `AdministrativePermission` vocabulary. Each permission has a domain, a risk class, the scope levels it may be granted at, and whether it may be delegated.
- `profile-registry.yaml`: administrative profiles (for example `tenant-administrator`). A profile is a template that expands into one scoped grant per permission. It is never a grant itself.
- `scope.schema.json`: `AdministrativeScope`. It names exactly one anchor level and that level's identifiers.
- `grant.schema.json`: three definitions.
  - `AdministrativeGrant`: one principal, one permission, one scope, a lifecycle and provenance.
  - `AdministrativeDecision`: the result of one evaluation.
  - `EffectiveAuthority`: the caller's current grants, served at `GET /admin/effective-authority`.
- `lifecycle.yaml`: the grant state machine, PENDING → ACTIVE → SUSPENDED / EXPIRED / REVOKED.
- `examples/administrative-grants.json`: grants from a profile, a bootstrap, a delegation, just-in-time access and a static group membership; allow, deny and step-up decisions; and one effective-authority response.

## Rules the Control Plane enforces

- **Deny by default (section 14).** No grant means no authority. An unknown scope is never global scope, and an ambiguous one is never guessed.
- **One grant, one decision (sections 13, 111).** A single ACTIVE, currently valid grant must cover both the permission and the scope. Grants are never combined across scope to manufacture authority nobody granted.
- **No implicit inheritance (sections 15-20).** A corporate group grant covers its organisations only when its mode says so. `STATIC_MEMBERSHIP` lists them at grant time; `DYNAMIC_GROUP_DESCENDANTS` must be stated explicitly. The default is `EXACT`.
- **Delegation never widens (sections 43-48).** A delegated grant has the same permission and scope as its source, never outlives it, stays within its source's `delegable_depth`, and is granted by the source's holder. Non-delegable permissions are never delegated.
- **Nobody grants to themselves (section 39).** `granted_by` is never the grantee.
- **Bootstrap is exceptional (sections 128-129).** A `BOOTSTRAP` grant is platform-scoped and `TIME_BOUND`, never standing.
- **Safe explanations (section 98).** A denial carries codes from the `administrative_denial` category of `authorization/v1/reason-code-registry.yaml`, never internal policy detail.
- **Effective authority is a read model, not a permission (section 99).** The Console uses it for navigation and scope display. The backend evaluates every request again.

## Versioning

Adding a permission, profile, reason code or optional field is additive. Removing or renaming any of them, or narrowing a grammar, is breaking and needs a v2.
