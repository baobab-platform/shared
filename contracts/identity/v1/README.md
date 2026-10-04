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
