# Roles to AdministrativeGrants: decision paper

**Status:** **Migration path ACCEPTED (owner, 2026-10-01). The enforcement flip is NOT authorised.** Nothing here changes enforcement. The flip is the owner's decision and is not made on a green build (`ada-00-administrative-authority-inventory.md`, baobab-cp).
**Date:** 2026-10-01
**Authority:** ADR-BCP-020 §143–144 (migration from broad roles, shadow evaluation), gates ADA-00 to ADA-12.
**Dashboard row:** EA-05 "AdministrativeGrant enforcement: BLOCKED (roles→grants decision)".

## The question

Today the Control Plane authorises administration with two Keycloak realm roles (`cp:platform-admin`, `cp:tenant-admin` plus an ACTIVE workforce membership) behind coarse OAuth scopes. ADR-BCP-020 replaces those with per-principal, scoped, time-bound AdministrativeGrants. Grants already exist, are evaluated in shadow beside every role-guarded route, and are counted in `administrative_authority_shadow_total`. **When, and under what conditions, do grants become the enforcing decision, and when are the realm roles retired?**

## Ruling already made (owner, 2026-10-01)

> AdministrativeGrant enforcement MUST NOT replace role-based administrative enforcement until a governed operational path exists to create, inspect, amend/revoke and expire AdministrativeGrants. The bootstrap CLI cannot be the normal authority distribution mechanism.

This paper takes that as a hard prerequisite and checks it against the code.

## What existed when this paper was written (HISTORICAL SNAPSHOT, 2026-10-01)

> **Historical.** This table and the "Why the flip is unsafe today" section describe the Control Plane **before** ADA-05. They are kept because the reasoning behind the migration path rests on them, not because they describe today. Grant administration routes, `authority:self`, maker-checker, atomic replacement, scope containment, step-up evaluation, persistent shadow evidence, readiness, the reviewed-population check and the per-permission enforcement gate have since been implemented; see *Rulings*, *Evidence-phase rulings* and `ea-dashboard.md` for current state. Nothing is enforced: `enforced: []`.

## Table as of 2026-10-01 (superseded)

| Capability | State |
|---|---|
| Grant model, deny-by-default evaluation, no union across scope | Done (`internal/administration`, migration 000067) |
| Every role-guarded route mapped to a permission | Done: 117 routes, none unmapped, held in step by `TestEveryGuardedRouteIsMapped` |
| Shadow comparison and metric | Done, 250 ms budget, never changes the response |
| Read the caller's own usable authority | Done: `GET /v1/admin/effective-authority`, but the `authority:self` scope is **not yet issued by Keycloak**, so the route answers 403 |
| Create grants | **Only** `cmd/admin-bootstrap` (a command-line procedure) |
| Grant administration routes (issue, inspect, revoke, delegate) | **None** (ADA-05) |
| Separation of duties and approval for grants | Not built (ADA-06) |
| Time-bound/JIT, support access, break-glass | Not built (ADA-07 to ADA-09) |
| Access review and recertification | Not built (ADA-11) |
| Expiry sweeper | Not built (evaluation already treats an elapsed window as expired) |
| Operations routes | Authorise inside the handler with the platform-admin role, **not shadowed** |
| Step-up | The verified token carries no assurance claim the Control Plane reads, so a grant requiring step-up counts as `step_up`, never allow |
| Bootstrap grants | Platform-scoped, TIME_BOUND, **at most 30 days**, never CRITICAL or EMERGENCY |

## Why the flip was unsafe on 2026-10-01 (HISTORICAL; reasons 1, 2 and 4 are now addressed by machinery, reason 3 by evidence still to be gathered)

1. **Lockout by design.** The only way to hold a grant is the bootstrap CLI, whose grants expire within 30 days and exclude CRITICAL/EMERGENCY permissions. Flipping would leave every administrator without a bootstrap grant with no authority, and would remove all authority from the rest in 30 days. There is no governed path to renew or issue.
2. **Self-service is unproven.** Nobody can yet see their own authority through the public API (`authority:self` unissued), so there is no way to verify a population before cutting it over.
3. **Evidence is thin.** The shadow metric has no production period yet; the criteria need `grants_broader` at zero over a representative period and every `grants_narrower` explained. Routes left `not_evaluated` (a grant anchored at a level the route does not name) and the unshadowed operations routes are blind spots.
4. **Separation of duties does not exist for grants.** Without ADA-05/06, whoever can issue grants can issue themselves broad authority, which is exactly the privilege escalation the model exists to prevent.

## Recommended path

Each step ends with evidence; none is skipped.

1. **Grant administration API (ADA-05).** Issue, inspect, amend, revoke and delegate grants as Control Plane commands, attributable to a canonical principal, audited, with scope-subset, permission-subset, duration and depth validation and revocation propagation. Grants that are CRITICAL, or broaden authority beyond the issuer's, go through the ADR-BCP-021 changeset with an independent approver (ADA-06). The bootstrap CLI stays as bootstrap and break-glass machinery, not the normal plane.
2. **Make authority visible.** Issue `authority:self` in IAM (a Keycloak configuration change, which stays untouched pending its ADR and is therefore an owner action) so each administrator can verify their effective authority.
3. **Close the blind spots.** Shadow the operations routes; resolve the organisation, account and group ancestry for routes that return `not_evaluated`; read an assurance claim so step-up is evaluable.
4. **Populate.** Issue grants for the real administrator population from a reviewed list; verify each person's `effective-authority` equals or narrows what their role allowed (ADR-BCP-020 §144: "equal or narrower justified authority, not accidental expansion").
5. **Observe.** Run shadow evaluation for a representative period. Exit criteria: `grants_broader` zero; every `grants_narrower` explained as a missing grant or an over-broad role; `unresolved` and `error` explained.
6. **Flip gradually, not in a day.** Enforce grants per permission, starting with low-risk read permissions, then by tenant or environment, with a fail-closed rule and a documented rollback (re-enable the role decision for that permission). ADR-BCP-020 §143 warns against a flag-day migration.
7. **Retire the realm roles** only after a full period with enforcement on and no role-only decisions needed; then remove the roles and the transitional `scopeEntitlements` binding.

Gates ADA-07 to ADA-09 (time-bound/JIT, support access, break-glass), ADA-11 (access review) and ADA-12 (hardening tests) are required before the model is declared production ready; I would not retire roles before ADA-11, since recertification is how standing grants are kept honest.

## Decisions requested

1. **Accept the path** above, in particular that step 1 (the grant administration API with maker-checker) is the next Control Plane work and the flip waits on steps 1 to 5.
2. **IAM action:** approve issuing `authority:self` (a Keycloak change, outside this repository's remit).
3. **Population source:** who supplies the reviewed administrator list for step 4.
4. **Flip granularity:** confirm per-permission, then per-tenant, rather than a single switch.
5. **Bootstrap policy:** until step 1 exists, should the 30-day bootstrap grants be renewed manually by an operator procedure, or should role authority simply stay primary (the current state) and bootstrap grants be left to lapse? I recommend the latter: roles stay authoritative, so nothing is lost when they lapse.

## Rulings (owner, 2026-10-01)

| # | Decision | Ruling |
|---|---|---|
| 1 | Accept the staged path | **Accepted.** No enforcement flip before grant administration, authority visibility, shadow blind-spot closure, population/reconciliation and a representative shadow-observation period. Steps 1 to 5 are prerequisites for the first flip, not follow-up work |
| 2 | `authority:self` | **Approved.** Configure it in the current IAM provider for the human administration client only; never for workloads. The canonical scope stays provider-neutral: Keycloak may issue it today, Baobab owns its semantics, and it must remain valid after the Ory migration |
| 3 | Administrator population | **Platform Security / Control Plane Governance** owns the reviewed list. IAM supplies *evidence* of current role holders and must not become the grant source of truth. Tenant-scoped grants need tenant/organisation attestation. No script maps a role to every permission. Each reviewed record names: canonical principal, current roles, proposed permissions, scope, environment, tenant/organisation, grant type, validity, risk, reason, reviewer. Approval: Platform Architecture/Security owner |
| 4 | Enforcement granularity | **Per permission first, then per applicable tenant/environment scope.** No platform-wide switch. Each permission has an independent rollback to the role decision. Order: low-risk reads, then moderate mutations, then high-risk mutations, CRITICAL last. For platform-scoped permissions, canary by environment and administrator cohort |
| 5 | Bootstrap grants | **Let them lapse.** Do not mass-renew. Roles stay authoritative until each controlled flip. `cmd/admin-bootstrap` stays only for initial bootstrap and exceptional recovery; an exceptional grant before ADA-05 is a fresh, explicitly approved, time-bounded one, never part of the migration population |

### Requirements the rulings add

- **Grant administration API** (step 1) supports at least issue, inspect/list, amend where permitted, suspend, revoke, delegate, expiry/lifecycle visibility and audit, and enforces that a principal cannot delegate authority they do not possess. HIGH and CRITICAL authority changes go through the Changeset/maker-checker path, not direct mutation.
- **CRITICAL permissions do not move** until maker/checker, step-up evidence, an independent approver, grant lifecycle administration, audit and rollback all exist. Missing step-up does not block migrating low-risk permissions later; it blocks critical privilege enforcement.

### Status after the rulings

```text
EA-05 Administrative Authority      MIGRATION DECISION ACCEPTED, implementation in progress
  ADA-05 grant administration       IMPLEMENTED (exact-scope delegation; replace/supersede and narrower-scope delegation follow-ups)
  ADA-06 maker/checker and SoD      NEXT
  authority:self issuance           APPROVED (IAM action)
  shadow blind spots                OPEN
  grant population                  BLOCKED on the above
  shadow observation                BLOCKED on population
  per-permission enforcement        NOT AUTHORISED YET
  realm-role retirement             NOT AUTHORISED
```

### ADA-05 follow-up rulings (owner, 2026-10-01)

| Item | Decision |
|---|---|
| IAM `administrator:read` | Approved. Human workforce client `baobab-control-plane-admin` only; provider-neutral. |
| IAM `administrator:write` | Approved. Privileged, explicitly requested, human admin client only, never a workload. The scope makes the route callable; authority still comes from `administrator.view/grant/revoke/delegate` grants. HIGH/CRITICAL changes stay refused until ADA-06. |
| Exact-scope delegation | Accepted for ADA-05 as a deliberately restrictive first implementation (cannot expand authority). |
| Narrower-scope delegation | **Required follow-up**, not an ADA-05 blocker. Must be done before delegated customer/organisation administration is relied on in production, using the canonical organisation/tenant/group relationships, never string-prefix or hierarchy guessing. Target: delegated authority is a subset of the delegator's effective authority (ADR-BCP-020). |
| Amend a grant in place | **Rejected.** Authority-bearing fields (permission, scope, validity, delegation source) are never rewritten; grants stay historically truthful. |
| Atomic replace/supersede | **Required before AdministrativeGrants become the enforcing authority.** One transaction: validate the replacement, create the new immutable grant, preserve provenance, revoke the old grant, handle dependent delegations. Not an amend: both records remain. Avoids lockout (revoke first) and overlapping broader authority (issue first). |

### ADA-06 rulings (owner, 2026-10-01)

| Item | Decision |
|---|---|
| Narrower-scope containment baseline (cp#247) | Accepted in its conservative form. |
| `ORGANISATION` to `TENANT` containment | **Wanted**, only through the explicit, effective `TenantOrganisationMapping` of ADR-BCP-018. Not through corporate ownership, naming, common parentage or PlatformAccount membership; never the reverse (a tenant scope does not contain an organisation scope). The source permission must be valid at both scope levels. Coverage and containment must consume the same mapping relation. |
| Corporate groups | Keep NO AUTOMATIC EXPANSION. `STATIC_MEMBERSHIP` uses its frozen member set. `DYNAMIC_GROUP_DESCENDANTS` may traverse the canonical effective group graph only when that graph is supplied to the evaluator. |
| CRITICAL `STANDING` | Prohibited. |
| CRITICAL `TIME_BOUND` | At most 24 hours. Extension is a new approval/change. |
| CRITICAL `JUST_IN_TIME` | Target 1 hour, shorter where the operation bounds it. |
| HIGH grants | Policy-controlled separately; do not inherit the CRITICAL bound. |
| IAM `administrator:approve` | Approved: optional, privileged, human admin client only, never a workload or default scope. The scope is not approval authority: approval still needs `changeset:approve`, separation of duties and, eventually, the required assurance. |
| HIGH maker-checker | May become usable once IAM issues the scope. |
| CRITICAL | Grants may be prepared under the controlled workflow while roles remain authoritative. CRITICAL AdministrativeGrant **enforcement stays disabled** until the assurance/step-up path is implemented and proven. |

### Evidence-phase rulings (architecture owner, 2026-10-02)

| Item | Decision |
|---|---|
| Shadow exit criteria | **Approved as proposed**, status `APPROVED`: 14 observed UTC days (days on which decisions were actually observed, not calendar days since deployment), 100 decisions per permission, `grants_narrower` 0, `not_evaluated` 0, `unresolved_or_error` 0. `grants_broader` is always 0 and not tunable. |
| Low-volume waiver | **None.** A permission that cannot reach 100 decisions stays role-authoritative longer. |
| `grants_narrower` = 0 | Deliberately stricter than ADR-BCP-020's "equal or narrower justified authority": there is no contract yet for an individually reviewed, intentional narrowing. Introduce one only if real evidence shows the need. |
| First enforcement wave | LOW-risk permissions only, one at a time, each chosen for the strongest clean evidence (traffic, zero anomalies, population complete), not for looking harmless. Tenant/environment scoping may precede global enforcement. |
| Before the first flip | Rehearse `ADMINISTRATIVE_ENFORCEMENT_ROLLBACK=<permission>`: it must restore role authority immediately without a deployment. |
| CRITICAL enforcement | **Remains PROHIBITED.** Lifting it is a separate reviewed policy change after the full chain is proven (WebAuthn step-up, acr, amr, freshness, assurance evaluation, HIGH/CRITICAL grant, independent approval, authoritative decision), not an automatic consequence of IAM issuing `acr` 3. |
| Population ownership | IAM role holders are evidence only; Platform Security and Control Plane Governance jointly review. `approved_by` in the artifact is a real, accountable canonical human principal: never the architecture-owner role, an assistant, an agent name or an automation principal. |
| Canonical phishing-resistant ACR | `urn:baobab:acr:step-up`; normative raw Keycloak LoA **3** (an alias such as `platinum` is optional and nothing depends on it). |
| Phishing-resistant evidence | Issuer-authenticated, either form: trusted `acr` 3, or a trusted `amr` naming `webauthn`/`hwk`. LoA 3 must have exactly one meaning: a flow requiring WebAuthn with user verification and no OTP-only or password-only alternative, proven by IAM CI (password, TOTP, ordinary MFA and SSO reuse never yield 3; asking for 3 without WebAuthn fails rather than falling back). |
| Custom Keycloak SPI for `amr` | **No** (ADR-0002 extension hierarchy; avoid new Keycloak-specific Java debt while IAM moves toward provider neutrality). No Keycloak fork. The native `oidc-amr-mapper` is tested first but the programme does not depend on it. |
| Step-up freshness | 300 seconds. |
| Raw mapping | `0`/`1` → `urn:baobab:acr:basic`; `2`/`gold` → `urn:baobab:acr:mfa`; `3` → `urn:baobab:acr:step-up`. An enrolled but unused passkey never meets a CRITICAL requirement; the person must have performed the phishing-resistant authentication for the current fresh step-up. |

### Remaining sequence (implemented as mechanism, owner decisions open)

| Item | State |
|---|---|
| Step-up / assurance evaluation | Implemented (`assurance-policy.yaml`, shared#192, cp#249). IAM issues no phishing-resistant level, so CRITICAL stays disabled. |
| Reviewed population | Format and validation only (`ReviewedPopulation`). The list is Platform Security / Control Plane Governance's; no grant is issued from here. |
| Shadow evidence | Readiness read model (`GET /admin/authority-migration/readiness`) against `enforcement-policy.yaml`. The criteria are PROPOSED; approving them is the owner's. |
| Per-permission enforcement | Mechanism in place (per permission, fail closed, independent rollback). `enforced` is empty: **no permission is enforced and none is authorised**. |

Sequence: organisation-to-tenant containment, CRITICAL bound (this change), IAM issuance, step-up/assurance evaluation, reviewed grant population, shadow evidence, permission-by-permission enforcement. Nothing here authorises a roles-to-grants flip.

Status: ADA-05 IMPLEMENTED (shared#184/#185, baobab-cp#244). IAM issuance of the two scopes: baobab-iam#50.

Nothing in this paper issues a grant, changes a route, or alters the realm roles.
