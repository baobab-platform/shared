# MP2-A: identity runtime verification contracts

This is the first contract increment of ADR-IAM-0033's multi-provider plan. It adds an identity-specific runtime profile to existing Shared models; it does not introduce a competing provider registry or implement runtime selection. Keycloak remains the intended enterprise SSO/federation provider. Synthetic examples describe facets only and make no product support claims.

| Concern | Existing authority/model reused |
| --- | --- |
| Provider identity and platform lifecycle | CapabilityProvider |
| Platform capability support and routing | ProviderCapabilitySupport, CapabilityBinding |
| Placement and deployed release | CP EngineInstance and topology release contracts |
| Scope and entitlement | Shared Scope and grants; CP resolution |
| Identity runtime facet verification | IdentityProviderRuntimeProfile, this increment |
| Non-secret configuration and security policy | CP ExternalReference to approved IAM configuration |

The 16 runtime facets are implementation mechanics, not canonical platform capability keys. This increment adds no catalogue entries, grants, workload allocations, bindings or activation evidence. A profile cannot declare lifecycle, health, tenant/business authority, provider product, or secrets.

## Static validation

Each facet occurs at most once. VERIFIED requires an opaque conformance evidence reference, exact artifact digest and observation/expiry timestamps. Evidence must cover publication time and match the profile artifact. Other statuses cannot retain evidence that could be misinterpreted as verification. Enum values are exact; padded mechanisms fail closed.

The schemas reference the existing provider, engine-instance and external-reference identifier definitions. The validator resolves cross-schema references offline using the pinned repository files, enforces timestamp and cross-field invariants, and checks the contract lock. JSON Schema alone does not enforce all cross-field rules; consumers must implement equivalent semantic checks.

All three checked-in examples are synthetic and UNVERIFIED. They are neither deployment configuration nor provider registration.

## Runtime acceptance remains required

Structural validity is not approval. Before selection, a consumer must resolve every reference through its authoritative registry, verify target type, ownership and security-domain association, enforce monotonic approved revisions, and match the artifact against the approved deployed release. It must verify evidence authenticity, exact provider/instance/facet/artifact coverage and current freshness under governed policy. An opaque reference or copied digest proves none of these facts.

Conformance evidence uses an ExternalReference to a versioned approved immutable evidence record. The existing evidence/v1 EvidenceRecord concerns organisation verification and has no provider-conformance subject type; this increment does not misuse or expand that contract. The conformance target model and approval workflow remain a consumer-integration prerequisite. References are non-secret and cannot resolve to credential values.

Historical profiles may remain valid as publication records after evidence expires; they are ineligible for current selection. Missing facets provide no affirmative support. DEPLOYMENT_DEPENDENT requires further deployment-specific proof and is not selectable as VERIFIED. Provider lifecycle, health, binding, scope and entitlement checks remain independent.

## Remaining increments

MP2-B will govern FederationTrust, external-principal and assurance extensions after review of existing identity contracts. MP2-C will implement authoritative reference/evidence consumption. MP3 will implement the registry using existing CP platform models; MP4 will implement the fail-closed resolver. Until those land, these are proposed contracts and fixtures, not an operational provider registry. Runtime adoption requires consumers to pin the merged immutable Shared revision separately.

Keycloak SSO retention does not allocate tenant authority to a realm or make Ory the platform authority. Shared owns canonical meaning, CP owns canonical context and platform resolution, IAM owns identity mechanics, and providers supply bounded implementations.
