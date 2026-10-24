# DEV-03 — native issuer and current CP authority

The IAM and CP assessments under `docs/assessments/` guide this gate without
changing its Accepted scope. ADR-IAM-0033 keeps Kratos native authentication,
Hydra OAuth/workloads and Keycloak enterprise federation distinct. The selected
disposable profile uses the pinned IAM-owned Hydra/Kratos images/configurations.
The old Keycloak development lifecycle remains historical evidence.

CP #435 adds request-time issuer status after signature, issuer and audience
verification. Both admin and workload introspection are configured in this
profile. Inactive tokens deny; outages return retryable 503 without a local
signature-only fallback. Subject, client, audience, normalized authority scopes
and expiry are bound to the verified bearer. Partial or cross-origin status
configuration refuses startup. This creates no Principal, Tenant or grant.

Hydra's admin-plane introspection is exposed only through an authenticated,
POST-only exact path on the private TLS issuer edge. Other admin operations stay
inside the isolated network. Native configuration overlays and runtime image
identities are pinned and hashed. No service port is published to the host.

The private protocol driver authenticates actual Kratos native password sessions
and handles actual Hydra login/consent challenges and code/S256 PKCE exchanges.
Its callback validates origin, path, state and single-code shape before exchange.
The consumer uses Hydra access tokens verified independently by CP. It is not
an OIDC ID-token consumer or an estate BFF. The authenticated fixture hook
normalizes actor/client identity for a closed disposable client list; it grants
no Tenant, Organisation, capability or legal authority and is not IAM's
registered production hook. Canonical provider support stays PARTIAL.

CP's guarded development command owns every canonical identity, mapping,
assignment and temporary administrative grant. It binds two real Kratos subjects
to distinct canonical maker/checker Principals. The qualifier uses ordinary CP
HTTP APIs, including independent provenance and digest-bound deactivation; it
never inserts canonical CP SQL or invents ACTIVE provider/engine bindings.

The exact runtime inventory is:

| Area | Required observations |
| --- | --- |
| Current authority | Genuine signed bearer resolves its own CP context; sibling and unrelated external Tenant requests deny |
| Scope and lifetime | Same-subject wrong-audience bearer denies; missing capability/grant denies without invocation; genuinely expired short-lived bearer denies |
| Issuer revocation | Native issuer revoke and independent status readback; the original still-unexpired bearer denies at CP; fresh issuance succeeds |
| Native human protocol | Two actual Kratos/Hydra subjects; real S256 exchange; wrong verifier, mismatched state and exact code replay deny |
| CP governance | Same Principal cannot approve provenance or deactivation; distinct checker completes the operation; original still-unexpired bearer denies after canonical disable while issuer status remains active |

These sixteen case meanings qualify only the scoped development authority chain.
DEV-04 retains its original seven obligations, independent readback and recovery
requirements. Provider registration/conformance, protected C4-03/C4-04 readiness,
Nabhold/CMS, estate sessions, real legal-source verification and production remain
separate. No source-green result can substitute for a real case receipt.

The reusable lifecycle keeps credentials/session/codes/tokens in its private run
and private provider stores. It publishes only closed outcome booleans, exact
source/image/configuration identities and verified cleanup. A failed assertion,
unknown outcome, source/config drift or surviving owned resource prevents a
successful authority receipt. A qualification run is destructive only to its
own synthetic identity and must be recreated before repeating those cases.

The official implementation register and dated evidence record are updated only
from actually observed native results and final-head review/CI. Combined audit
gaps BA-AUD-002/030 and IAM provider/readiness findings must not be auto-closed by
this scoped work: seven-case and provider/estate obligations remain separate.
