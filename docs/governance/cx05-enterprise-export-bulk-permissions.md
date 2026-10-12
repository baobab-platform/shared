# CX-05 enterprise export and bulk rights

CX-05 registers **two distinct** AdministrativePermissions:
- `organisation.export`: HIGH, ORGANISATION-exact-only, nondelegable read-only request. Requires an effective independent `organisation.view` grant for the same Organisation, a purpose string, row/byte budget, safe redacted projections, correlation/audit evidence, anti-formula-injection output encoding and synchronous re-authorization before any artifact leaves the server. Never implies evidence, identifiers, secrets, addresses or corporate registration source exports.
- `organisation.bulk.propose`: HIGH, ORGANISATION-exact-only, nondelegable and mutating. This authorises creating a governed bulk change **proposal**, not executing its targets. Every target must be within the granted scope with independently supported operation type, version, idempotency and immutable plan; decision/apply require distinct maker/checker and current authority, and deny on suspension, revocation, plan drift, cross-tenant or partial-result concealment.

No profile automatically confers these rights. Platform, corporate-group and parent/subsidiary grants must not be expanded into these exact ORGANISATION permissions. Default is deny, including pending runtime implementation. This registry addition must be pinned in CP and backed by runtime and negative integration tests before publication.

- `organisation.bulk.approve`: **CRITICAL**, exact Organisation, nondelegable, not a proposal or execution privilege. The checker must be distinct from the maker, approve the entire immutable digest and evidence, and may not override missing per-target authority. Export is read-only in the validator's explicit allowlist, not a general relaxation of the permission naming rule.
