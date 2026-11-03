# IAM-N02/N04/N07 — reconciled closed development authority

**Status: DRAFT / PROVISIONED ONLY. Not accepted, issued, ACTIVE or released.**
Governing: EA v2.3, EA-DEV DEV-08/14, ADR-SHARED-042/043 and ADR-IAM-0033.

This single Shared candidate supersedes the conflicting canonical inventory edits
in Shared PRs #420 (N04), #421 (N02) and #422 (N07). The original PRs are
retained for audit history until owner decisions, not independently merged.

| Proposed principal | Owner | Narrow resource authority ceiling |
| --- | --- | --- |
| baobab-dev-iam-runtime-reader | IAM | CP identity-runtime:read |
| baobab-dev-zuribeans-cp-principal-validator | ZuriBeans | CP identity:principal:resolve for separately verified Trade human subject |
| baobab-dev-tms-subject | TMS | CP context:resolve, legal-actor:assess; TMS transport-only tms:booking:submit |
| baobab-dev-tms-validator | TMS | CP context:validate for TMS audience only |
| baobab-dev-zuribeans-native-browser-bff | ZuriBeans | Separate authorization_code/S256 browser client; no workload grants |

All are **development PROVISIONED declarations**. No credentials, ACTIVE CP
Principals, AdministrativeGrants, legal mandates, business entitlements, native
booking provider commitments or protected-environment allocations are created.

**Authority remains split:** Kratos authenticates humans, Hydra issues tokens,
CP resolves current canonical principals, context, actor grants and capability
bindings, and owner-native PEPs independently veto business operations.
Keycloak remains the permanent federation provider. Browser Trade scope does
not create buyer authority. The N04 read also requires separately current
`security.identity-runtime.view` administrative permission, not just the
issued `identity-runtime:read` scope.

## Acceptance sequence

1. Complete final-head Shared Python/Ruby/OpenAPI, registry and negative
   conformance tests without weakening any existing closed allowlist.
2. After independent ADR/owner review, merge **only one reconciled source**
   into Shared main. The prior three overlapping PRs must not be merged
   independently.
3. Re-pin CP's two consumer-lock references and the exact embedded contract
   bytes in a **separate** reviewed adoption after the merged Shared commit
   is reachable from main. CP #455 currently tests only an inert candidate;
   CP #454's independent runtime-read response still needs full current
   Postgres source and issuer/observer/grant proof.
4. Qualify IAM N02/N04/N07 and named estate/TMS consumers with real issuer,
   original bound token and current CP authority, wrong-audience, unknown,
   expired, revoked, replay, cross-tenant, absent-grant, provider failure and
   owner-native negative paths. Native TMS booking remains denied until its
   separate provider/idempotency/resource fence is qualified.
5. Independently verify source-pinned evidence custody, run-owned teardown,
   return to inactive state and original negative case preservation. Separate
   staging/production approvals and provider capability promotion remain held.

A green contract-validator check is **source acceptance evidence only**.
It is never a replacement for live CP/IAM issue-and-readback evidence.
