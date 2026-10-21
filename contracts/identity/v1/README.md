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

## Delegated human Principal resolution — ZuriBeans ZB-G03 step 3

`principal-resolution.openapi.yaml` and `principal-resolution.schema.json`
define how a registered workload acting for an authenticated human obtains
that human's canonical Principal from the Control Plane. This follows the
platform owner's decision of 2026-10-21.

- **Two credentials, never merged:** the caller authenticates with its own
  `baobab-control-plane` workload token. The human's IAM access token,
  audience-bound to the caller's own resource (`baobab-trade` for Trade), is
  carried in the body only as subject evidence.
- **The Control Plane verifies the evidence itself.** It checks the signature
  and issuer against its own issuer trust, then actor type, audience, scope,
  authorised party and expiry, and the token's current status by
  introspection. The caller cannot assert issuer, subject, Principal, email or
  customer identifiers.
- **`identity.principal.resolve@1`**
  (`POST /internal/identity/v1/principals/resolve`, scope
  `identity:principal:resolve`) is read-only. An unknown identity is
  `IDENTITY_NOT_RESOLVED` and creates nothing.
- **`identity.principal.register.buyer@1`**
  (`POST /internal/identity/v1/principals/register-buyer`, scope
  `identity:principal:register-buyer`) is governed just-in-time registration
  of an eligible first-time buyer. It is idempotent per (issuer, subject) and
  establishes identity only.
- **A resolution carries no authority.** No tenant, Organisation membership,
  role, market or purchasing authority comes with it. Trade still binds the
  canonical Organisation and checks an active buyer membership on every
  operation.

Both scopes are workload-only, `grants_authority: false` and allocated to no
workload. The capability keys are named here for the Control Plane
implementation. They enter the canonical catalogue only through the EA-02
candidate review. Run `python scripts/tests/test_principal_resolution.py`.
