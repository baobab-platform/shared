# MP2-B: federation trust and authentication evidence

This additive identity/v1 increment implements the contract portion of ADR-IAM-0033 MP2-B, preserving ADR-IAM-0026's explicit federation trust and ADR-IAM-0024's event-scoped assurance. It does not configure an IdP, register a real trust, activate federation, resolve a principal, or implement runtime evidence approval. Keycloak remains the intended enterprise SSO/federation implementation; provider products and native realm/IdP aliases do not enter these canonical contracts.

| Contract | Meaning and authority |
| --- | --- |
| FederationTrust | IAM-administered governed trust policy over exact upstream issuer/entity ID and explicit CP organisation/estate references |
| Provider binding | Existing CapabilityProvider/EngineInstance IDs plus approved non-secret CP ExternalReferences |
| FederatedExternalPrincipal | Verified adapter evidence for one human authentication event; canonical resolution remains authoritative CP mapping |
| FederatedAuthenticationAssurance | OIDC or SAML event provenance with approved trust-scoped mapping to A1–A3, or UNKNOWN |
| Federation lifecycle | Canonical state transitions, independent of provider configuration/availability |

## Trust and scope

`organisation_ids` and `estate_ids` are explicit nonempty sets, never wildcards or inferred from an email domain. They bound where a federation relationship may be used; they do not grant estate access, tenancy, membership, roles or business permissions. Organisation IDs reuse CP canonicalEntityId and must resolve specifically to Organisation records. Estate IDs, provider IDs, instance IDs and all ExternalReferences must resolve to approved targets of the expected type, ownership and scope. The binding must resolve to the approved provider/instance association and current MP2-A profile. A valid identifier or profile is not approval or health evidence.

Trust material references identify approved public metadata/certificates/JWKS configuration. References must never resolve to private keys, static secrets or raw authentication assertions. Provider-native configuration remains in the adapter/configuration boundary. Domain discovery/verified-domain configuration remains in its governed configuration reference; it does not link identities or replace organisation verification.

Protocol and upstream issuer/entity ID are immutable for an existing trust ID; replacing either requires a new trust. Comparison is exact, including issuer path/trailing slash. OIDC issuers require HTTPS without credentials, query or fragment. SAML entity IDs may be URI/URN identifiers; they are not necessarily fetchable URLs. Protocol-specific signature, algorithm, issuer, audience, recipient, replay and time validation is an adapter obligation before normalized evidence is emitted. The approved configuration reference must bound recipient/client audiences; merely matching this contract is not protocol verification.

## Lifecycle

The lifecycle manifest governs transitions and monotonic revisions. REQUESTED → CONFIGURING → VERIFYING → ACTIVE requires organisation verification, authorised administration and successful technical proof through independently approved activation evidence. Uploaded metadata or working provider configuration alone cannot establish ACTIVE.

Only ACTIVE passes the necessary lifecycle predicate for new federation authentication. REQUESTED, CONFIGURING, VERIFYING, SUSPENDED, ROTATING and REVOKED deny it. Suspension and rotation return through VERIFYING before activation. REVOKED is terminal; a replacement uses a new ID. Existing sessions, enterprise relationships and domain grants require independent containment/revocation workflows; deleting a trust does not delete a person. Durable concurrency/revision enforcement and activation-evidence authenticity remain consumer obligations.

## External identity

Issuer plus stable subject remains the identity key; a provider label, organisation or email address is never the linking key. A SAML adapter must establish stable scoped subject semantics (including NameID qualifiers where relevant) through approved versioned mapping configuration; transient or email-derived subjects must not become canonical linking evidence. Email-shaped opaque subjects cannot be classified by syntax alone, so the contract rejects EMAIL mapping mechanisms rather than pretending to prove stability from a string.

UNRESOLVED carries no fabricated principal, external-identity ID or mapping reference. RESOLVED references the existing Principal and ExternalIdentity identifier contracts plus an authoritative mapping whose basis is ISSUER_SUBJECT. Consumers must resolve the mapping and independently confirm its exact issuer/subject, canonical principal, external-identity association and lifecycle. Schema validity does not make arbitrary UUIDs authoritative. Linking consent/review and provisioning/deprovisioning remain governed workflows; no JIT business authority is created here.

## Assurance provenance

The assurance record repeats the exact authentication event, trust, provider, instance, protocol, issuer and subject to prevent mixing evidence across sessions/identities. OIDC reuses AuthenticationAssurance unchanged. SAML retains AuthnContext and authentication/session times; it does not manufacture OIDC acr/amr. Browser assertions, upstream branding and SSO alone do not establish MFA.

UNKNOWN has no level or mapping decision reference. MAPPED requires an explicit trust policy reference and immutable approved mapping evidence. Consumer integration must independently validate rule/version, issuer, subject/event, raw evidence coverage, authenticity and current expiry before accepting A1, A2 or A3. Arbitrary raw acr/AuthnContext values are legal evidence but never automatically map to a level. Unknown or insufficient evidence remains UNKNOWN until an approved baseline policy is actually evaluated. A4 additionally requires privileged Baobab context, fresh A3 authentication, risk evaluation and restricted session policy; upstream federation evidence cannot assert it.

Static validation enforces exact cross-record provenance, event/evidence time bounds, schema closure and lifecycle consistency. It does not claim current freshness or permission to consume a historical event. Authentication and assurance records must expire under governed runtime policy; consumers enforce current-time acceptance, replay prevention and configured maximum lifetimes independently.

## Compatibility and evidence

Existing ExternalIdentity, Principal, AuthenticationAssurance and AssuranceRequirement schemas are unchanged. Four schemas and the lifecycle manifest are registered additively in identity/v1 and contracts.lock.yaml. Exact published schema IDs are resolved offline through repository schemas; unknown URLs and duplicate IDs fail. Cross-field and transition checks are normative alongside JSON Schema and must be implemented by consumers.

Both fixtures are synthetic: VERIFYING trust, UNRESOLVED principal and UNKNOWN assurance. They prove format/consistency only and authorize no login or real organisation registration. Tests also exercise synthetic ACTIVE/RESOLVED/MAPPED publication records; these are not activation evidence.

MP2-C must implement authoritative target/evidence consumption, protocol verification boundaries and current eligibility checks against a pinned merged Shared revision. MP3/MP4 registry/resolver, MP9 provider-binding reconciliation and MP12 assurance/step-up runtime integration remain outstanding. This PR does not close those gates or EA-04.
