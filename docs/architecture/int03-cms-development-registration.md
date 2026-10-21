# INT-03 CMS development identity registration

Date: 21 October 2026. Authority: the Accepted [CMS proof-bootstrap decision](int03-cms-proof-bootstrap-proposal.md), Shared #354 at `409d780d05f7825ab1228649541032d42a7b0b13`, Accepted EA v2.3 and retained v2.2 NAB/L4 matrix.

This source increment implements only that decision's two named development
registry exceptions. ACTIVE means permitted to produce disposable synthetic
proof before first qualification; it is not proof or product activation.

| Identity | Owner | Exact token ceilings |
|---|---|---|
| `baobab-int03-cms-consumer` | Infrastructure | CP/context:resolve and CMS/content:entry:resolve, independent audience-limited tokens |
| `baobab-int03-cms-validator` | CMS | CP/context:validate only; validates_audiences=[baobab-cms] |

Both entries use development/client_credentials. The complete canonical rows
are pinned by `validate-authorization-contracts.rb`, including the absence of
additional authority fields. Mutation tests exercise owner, repository, runtime,
environment, scopes, audience, credential type, rotation owner, status, context
purpose, validator relationship, extra authority and removal. The product
`nabhold-backend` stays PROVISIONED in production; the existing production CMS
validator, Pulse-only exception and all other rows are unchanged.

## Consumer order and independent lifecycle

1. Merge this exact canonical registration only after mandatory CI and exact-head
   review. It creates no credential, tenant grant, release, certification, binding
   or provider-health observation. Do not edit a copied registry snapshot locally.
2. IAM must recognise the exact two fixture-only rows and prove their absence
   from committed and ordinary live product-bootstrap clients before advancing
   its Shared pin. It must not add deterministic credentials or product client
   files for either identity. Adapt IAM-owned provisioning for a disposable
   fixture, with exact read-back, independent random secrets and fixed deadline.
3. CP and the integration harness consume the new approved Shared revision
   unmodified. No lifecycle bypass, production credential or Pulse identity may
   substitute. Explicit synthetic Organisation/Tenant/market grants remain
   independently governed. Nabhold #83 and CMS #40/#41 are merged source ports,
   not runtime acceptance of these identities.
4. Every run enforces the Accepted decision's absolute deadline, token expiry,
   early-close revocation or destruction of all issuer trust/accepting runtimes,
   and unconditional teardown. Receipt starts BOOTSTRAP/REQUIRED_NOT_EXECUTED;
   a new run never inherits a previous receipt or durable client.
5. Actual source-built CMS/PostgreSQL acceptance, independent maker/checker
   provider certification, current release/health/binding and all required
   NAB/L4 cases remain pending. Keep PARTIAL/non-production support; a current
   policy refusal is BLOCKED, not permission to change support metadata.

No private package, engine permission, executive authority, real legal fact,
protected Kratos/Hydra proof, staging, production or R0–R3 gate changes here.
Nabhold remains non-trading; corporate ownership confers no tenant access.

## Exit and rollback

Close a run by disabling/removing both ephemeral clients, revoking outstanding
credentials or destroying the entire isolated issuer/verifier trust, and
removing sessions, keys, services, volumes and networks. Canonical removal or
suspension of these named exceptions is a reviewed Shared change that updates
the complete-row pins and refusal tests together. Never alter a materialised
snapshot or replace the permanent product workload's lifecycle to roll back.

Local validation checks YAML structure, unchanged existing rows, Python test
syntax and diff hygiene. Ruby is unavailable in this executor; the mandatory
Actions contract job must execute the actual Ruby validator and Python mutation
suite before merge. No local validator or real-component pass is claimed.
