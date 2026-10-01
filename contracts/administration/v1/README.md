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
- **Delegation never widens (sections 43-48).** A delegated grant has the same permission as its source and a scope within the source's (see *Scope containment*), never outlives it, stays within its source's `delegable_depth`, and is granted by the source's holder. Non-delegable permissions are never delegated.
- **Nobody grants to themselves (section 39).** `granted_by` is never the grantee.
- **Bootstrap is exceptional (sections 128-129).** A `BOOTSTRAP` grant is platform-scoped and `TIME_BOUND`, never standing.
- **Safe explanations (section 98).** A denial carries codes from the `administrative_denial` category of `authorization/v1/reason-code-registry.yaml`, never internal policy detail.
- **Effective authority is a read model, not a permission (section 99).** The Console uses it for navigation and scope display. The backend evaluates every request again.

## Scope containment

A scope is *within* another when every resource the first reaches the second reaches. Evaluators decide it from the scopes themselves, as the converse of how they decide coverage, and never from identifier text:

- an environment-less scope contains any environment; a named environment contains only itself;
- `PLATFORM` contains every scope;
- otherwise the levels and anchors match (`PLATFORM_ACCOUNT`, `ORGANISATION`, `TENANT`, `LEGAL_ENTITY`, `DIGITAL_ESTATE`, `RESOURCE`), a `MARKET` scope contains the same market with a narrower set of qualifiers (`organisation_id`, `tenant_id`), and a `CORPORATE_GROUP` scope contains, by `STATIC_MEMBERSHIP`, an organisation in its list or a shorter list of the same group, and, by `DYNAMIC_GROUP_DESCENDANTS`, the same group, exact or dynamic;
- an `ORGANISATION` scope contains a `TENANT` scope only through an explicit, effective `TenantOrganisationMapping` (ADR-BCP-018: `ACTIVE` and inside its effective window) between that tenant and that organisation. Ownership, naming, common parentage and `PlatformAccount` membership are not relations. The reverse never holds: a tenant scope does not contain an organisation. The permission must be valid at both levels. Coverage follows the same mapping, so containment implies coverage; a delegation resting on a mapping stops being usable when the mapping ends;
- nothing else is assumed. In particular no group-descendant membership is followed unless the evaluator holds the canonical group graph, so a dynamic group does not contain an organisation without it, and corporate groups have no automatic expansion. Where containment cannot be proven, including when the evaluator holds no mapping data, the answer is *not within*, and a delegation is refused rather than widened.

## Versioning

Adding a permission, profile, reason code or optional field is additive. Removing or renaming any of them, or narrowing a grammar, is breaking and needs a v2.
