# Baobab IAM native development completion — Shared contract proposal

**Status: PROPOSED, NOT APPROVED OR QUALIFIED (6 November 2026).**

This proposal follows the revised Library *Baobab IAM Native Provider Capability Audit and Development-Completion Plan* and accepted ADR-IAM-0033 / ADR-SHARED-017. **Goal:** fully implement and independently qualify IAM **in development**; CP and consumer enablement are subsequent independent gates. Neither source declaration nor target matrix is evidence of implementation, certification or deployment.

## Canonical platform-resolvable operations

The existing `identity.authentication.perform` (Kratos/Hydra code/S256 native path) and `identity.workload-token.issue` (Hydra) stay unchanged. Two proposed new entries are catalogued in this PR:
- `identity.authentication.assurance`: only a server-owned decision about current authentication, with no browser-selected assurance level, business grant or static provider qualification.
- `identity.federation.enterprise`: Keycloak-owned OIDC/SAML trust-bound browser initiation, without native credential, platform workload, canonical Principal or membership authority.

`identity.token.issuance` is **subsumed** by the two existing token-producing capabilities: it is not introduced as a separately grantable minting capability. Current Hydra JWKS, expiry, audience, scope and signing rotation remain concrete provider qualification obligations.

## Management and provider facets

`native-provider-targets.yaml` is a **target inventory**, not a runtime support report. It lists the exact Kratos, Hydra and Keycloak facet allocations and separately inventories eleven **IAM management/security/status operations**. Those management operations use the closed `iam-management-operation.schema.json` request/outcome envelopes with original `PROVIDER_VERIFIED` evidence, owner controls and deterministic denial; they are **not** automatically grantable capabilities merely because their names are declared here. `native-provider-targets.schema.json` validates the architecture-only inventory against existing runtime facet vocabulary.

Existing `provider-runtime-profile.schema.json`, `runtime-capability.schema.json`, `federation-trust.schema.json`, `federated-assurance.schema.json` and `authentication-assurance.schema.json` remain authoritative. Do not introduce a parallel CP registry, invent provider IDs or grant Business/Tenant/LegalEntity claims.

## Development qualification exit

1. Each Kratos/Hydra/Keycloak target facet has a real provider positive, corresponding failure/replay/revocation negatives, exact source SHA and provider image/build digest, private original receipt and teardown. A3 requires a real origin/user-verification proof; A4 requires independent privileged/security witness. AAL2 or method labels alone never qualify them.
2. Prove real recovery, rebinding, old-session invalidation, governed high-risk holds, issuer/JWKS overlap and retirement, incident containment, clean rebuild and *whole-runtime* restore without resurrected revocations.
3. Exercise the provider-neutral contracts through a disposable IAM-controlled development consumer, where a representative CP/context boundary is necessary. This is a **portable compatibility probe**, not a prerequisite for readiness of Nabhold/ZuriBeans/Thamani or production engines.
4. Only then mark the specific IAM implementation `IMPLEMENTED` in its declaration and publish independently verified **development qualification evidence**. A new Shared catalogue entry by itself never implies IMPLEMENTED, CP ACTIVE, EA-09 protected certification, or consumer permission.
5. Leave CP provider registrations/bindings/approvals, engine PEP acceptance and staging/production deployment for later explicitly authorised work.

Run `python scripts/capability_catalogue.py validate-catalogue` and `python -m unittest scripts.tests.test_iam_native_target_contracts`. Neither converts TARGET_NOT_QUALIFIED into a support receipt.

## Provider-first development evidence (distinct from CP)

`native-development-qualification.schema.json` defines the exact-source,
provider-artifact and facet-specific **IAM-owned development qualification
receipt**. Its `DEVELOPMENT_QUALIFIED` representation requires independently
reviewed original test/artifact digests, same-run positive and negative
observations, authentic runtime origin and teardown. The *schema alone* cannot
verify witness authority or original runtime semantics; the reviewer must
compare it with the authenticated GitHub-run provenance and actual provider
readback. The synthetic `native-development-unqualified.json` example is
explicitly `UNQUALIFIED` and never constitutes an operational receipt.

Crucially this receipt has **no CP provider ID or engine instance ID** and
cannot grant a Client, Tenant, Organisation, Market or business operation.
Following IAM development completion, CP may independently register the
reviewed provider facet against its own instance/release and current grant
policy. Protected staging and production remain independent.
