# Identity contracts (v1)

Canonical identity types shared across Baobab engines.

## Provider neutrality (Gate IAM-M1 / ADR-IAM-0019–0020)

- **Resolution key:** `issuer` + `subject` on `ExternalIdentity`. Changing identity runtime (Keycloak → Ory) MUST NOT invent a new principal solely because `provider_type` changed.
- **`provider_type`:** optional free string (`keycloak`, `ory`, `google`, `azure`, `unknown`, …). It is operational metadata only. It is **not** required and MUST NOT gate platform authorization.
- **Forbidden:** treating `keycloak_user_id` / `ory_identity_id` (or any provider-local primary key) as the Baobab canonical identity key.
- **Principal:** remains provider-independent (`principal.schema.json`).

Examples:

- `examples/external-identity-keycloak.json`
- `examples/external-identity-ory.json`


## Identity runtime profiles (MP2-A)

`provider-runtime-profile.schema.json` attaches identity facet verification to an existing CapabilityProvider and EngineInstance. `runtime-capability.schema.json` defines the closed runtime facet/status vocabulary and non-secret conformance evidence references. Runtime facets are not canonical platform capability keys.

Run `python scripts/validate-identity-runtime-contracts.py` and `python scripts/tests/test_identity_runtime_contracts.py` for schema, fixture and cross-field validation. These checks prove static publication consistency, not authoritative evidence approval or current runtime eligibility. All runtime-profile examples are synthetic and UNVERIFIED.

See [MP2-A authority, validation and remaining consumer requirements](../../../docs/architecture/iam-mp2-runtime-contracts.md).

## Federation trust and evidence (MP2-B)

`federation-trust.schema.json` and `federation-lifecycle.yaml` govern scoped canonical trust and disabled-trust semantics. `external-principal.schema.json` distinguishes unresolved adapter evidence from authoritative issuer-plus-subject mapping. `federated-assurance.schema.json` reuses existing OIDC AuthenticationAssurance and adds SAML provenance, UNKNOWN handling and explicit trust-scoped A1–A3 mapping. `federation-domain.schema.json` supplies their shared vocabulary. Existing identity/assurance schemas are unchanged.

Run `python scripts/validate-federation-contracts.py` and `python scripts/tests/test_federation_contracts.py`. Cross-field/transition checks supplement JSON Schema; current-time acceptance, authoritative reference/evidence approval and protocol verification remain runtime obligations. Both OIDC/SAML examples are synthetic, VERIFYING/UNRESOLVED/UNKNOWN and permit no federation login.

See [MP2-B semantics, compatibility and remaining consumer duties](../../../docs/architecture/iam-mp2-federation-contracts.md).

## Workload request scope syntax — Nabhold R0 convergence

`workload-token-request.schema.json` accepts the existing colon-separated
scope names from `authorization/v1/scope-registry.yaml`, including
`content:entry:resolve` and `content:entry:preview`. The earlier one-colon
pattern rejected the CMS scope already allocated to `nabhold-backend`.
This supports existing hierarchical scopes; one-colon scopes remain valid.
Workload/audience/scope lexical validation also requires absolute string end:
a final line terminator cannot exploit the usual dollar-anchor semantics.

No scope registration/allocation or workload status changes. A schema-valid
request is not a grant: the provider still requires an ACTIVE workload in the
correct environment, exact audience/scope ceilings and authenticated credential
evidence. `nabhold-backend` remains PROVISIONED until its separate qualification.
No credential, provider field, realm or grant type is accepted in this request.

Regression tests (`python scripts/tests/test_workload_token_contract.py`) validate
all declared workload scopes against the real schema and reject malformed
segments, whitespace, wildcards, duplicate/excess scopes and provider leakage.
IAM must update its pinned schema and lexical validator together before this
corrected contract is considered consumed by the issuer.

## Buyer identity handoff — ZuriBeans ZB-G03

`buyer-identity-handoff.schema.json` is the provider-neutral evidence a
confidential Digital Estate BFF presents to Trade for a B2B buyer operation
(IAM ADR-0010 section 0; ADR-IAM-0023 sections 39–45; ADR-IAM-0033). The BFF
holds the IAM tokens server-side and the browser holds only an opaque session
cookie.

- **Token:** a human (`actor_type: human`) IAM access token audience-bound to
  `baobab-trade`, with scope `trade:buy` and the BFF client as `azp`. Trade
  verifies signature and issuer against the IAM issuer metadata; the issuing
  runtime (Hydra first) is not named. Provider organisation, group, role,
  tenant or email claims are never buyer-membership evidence.
- **Request:** `requested_organisation_id` and `requested_country_code` are
  requests to be attested by the Control Plane and then checked against an
  active Trade buyer membership, never proofs. No tenant, principal,
  membership or role may be asserted.
- A commerce-engine (Medusa) customer token alone authorises no commerce
  operation.

`trade:buy` is registered human-only for `baobab-trade` with
`grants_authority: false`, and is granted to no client. Trade `v1`'s
`humanOidc` scheme now names the issuer's discovery document instead of
Keycloak realm URLs. Run `python scripts/tests/test_buyer_identity_handoff.py`.
These are static checks; signature, expiry, client allowlisting, canonical
Principal resolution and membership remain runtime obligations.

## Delegated human Principal resolution — ADR-SHARED-042 (CAA-01)

`principal-resolution.openapi.yaml` (v1.1) and `principal-resolution.schema.json`
define how a registered workload acting for an authenticated human obtains
that human's canonical Principal from the Control Plane. They implement
ADR-SHARED-042 sections 3 and 4.

- **Two credentials, never merged:** the caller authenticates with its own
  `baobab-control-plane` workload token. The human's IAM access token is
  carried in the body only as subject evidence.
- **A registered validator relationship.** The subject audience CP accepts
  from a caller is the caller's `subject_principal_audiences` entry in
  `workload-registry.yaml` (`baobab-trade` for Trade). CP never infers it from
  `allowed_audiences`, and a request cannot choose it.
- **The Control Plane verifies the evidence itself.** It checks the signature
  and issuer against its own issuer trust, then actor type, audience, scope,
  authorised party and expiry, and the token's current status by
  introspection. The caller cannot assert issuer, subject, Principal, email or
  customer identifiers.
- **`resolveDelegatedHumanPrincipal`**
  (`POST /internal/identity/v1/principals/resolve`, scope
  `identity:principal:resolve`) is read-only. An unknown identity is
  `IDENTITY_NOT_RESOLVED` and creates nothing.
- **`registerBuyerPrincipal`**
  (`POST /internal/identity/v1/principals/register-buyer`, scope
  `identity:principal:register-buyer`) is governed just-in-time registration
  of an eligible first-time buyer. The request declares `purpose:
  BUYER_ONBOARDING`, which must be approved for the BFF client. CP refuses an
  identity-link conflict (`IDENTITY_LINK_CONFLICT`; never resolved by email)
  and enforces abuse limits (`REGISTRATION_RATE_LIMITED`). It writes the
  Principal, ExternalIdentity, audit record and a
  `com.baobab-platform.identity.created.v1` outbox event in one transaction.
  It is idempotent per (issuer, subject) and establishes identity only.
- **A resolution carries no authority.** No tenant, Organisation membership,
  role, market or purchasing authority comes with it. Trade binds those in
  `trade/v2` `buyer-execution-context.schema.json`.

These are operations, not catalogued capabilities: no capability key is
registered for them. Both scopes are workload-only, `grants_authority: false`
and allocated to no workload. Run
`python scripts/tests/test_principal_resolution.py`.

## Buyer handoff v1.1 and buyer assurance policy (ADR-SHARED-042 CAA-03/CAA-04)

These follow the Platform Owner ruling of 22 October 2026 (ADR-SHARED-042 §14).

- **The BFF authenticates as itself.** In `buyer-identity-handoff.schema.json`
  v1.1, the estate BFF presents its own IAM workload token to Trade as the
  caller credential (`BffCallerTokenClaims`: actor `workload`, audience
  `baobab-trade`, scope `trade:buyer-handoff`). It carries the human access
  token in the body as subject evidence (`BuyerOperationHandoffRequest`).
  The BFF client must equal the human token's `azp`. Trade forwards the BFF
  token to the Control Plane as client evidence for the estate binding
  (`control-plane/v1/estate-client-binding`). The v1.0 shape authorises no
  operation that needs the Digital Estate.
- **`assurance-policy.schema.json`** is the versioned buyer assurance policy.
  - It is scoped to one trusted issuer and the Trade audience.
  - It has three canonical profiles: `BUYER_SESSION`, `BUYER_COMMITMENT` and
    `BUYER_ADMINISTRATION`. The operation-to-profile mapping is fixed by the
    contract, so no policy can downgrade an operation.
  - `acr` values match exactly, with no ordering. Required methods and
    authentication freshness apply where a profile sets them; a future
    `auth_time` is not fresh.
  - Only an `APPROVED` policy within its effective interval is enforced.
    Anything else denies with `OPERATION_NOT_ACTIVATED`. Evidence that fails a
    profile is `ASSURANCE_INSUFFICIENT`.
  - IAM owns the values and their evidence. The example is synthetic and a
    `DRAFT`.

  This policy is distinct from `administration/v1/assurance-policy.yaml`, which
  ranks the workforce realm for administrative authority.

Neither scope is allocated to any workload, and nothing is activated. Run
`python scripts/tests/test_buyer_identity_handoff.py` and
`python scripts/tests/test_assurance_policy.py`.
