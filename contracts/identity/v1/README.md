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
