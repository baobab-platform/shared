# DEV-14 integration profile v1

The accepted DEV-14/15 specification is implemented by
`contracts/development/v1/engine-integration-profile.schema.json` and the read-only
`scripts/engine_integration_profile.py` validator. This is the fourth development
artifact: it references the existing environment, provider and enterprise contracts.
It does not create an identity, grant, binding, health observation or certification.

Profiles select a dependency graph, existing canonical capability majors and
registered development IAM clients. Required services cannot depend on an optional
or absent node. Native stores belong to the subject engine; headless profiles do
not start CMS. Examples select the unrelated API-only enterprise plus a distinct
neighbour. CP still allocates every canonical ID and owns current authority.

Immutable source and image identities live in the Infrastructure run lock, not in
self-referential Shared examples. Runtime admission compares the actual owner
source, provider declaration, environment contract, adapter and Dockerfile to that
lock. A missing required image or adapter is blocked, never inferred ready.

The owner supplies a Python adapter at the declared relative path. Infrastructure
executes it inside an unprivileged private container, using the subject image or a
pinned Python driver image. The native service keeps its own runtime language.
The adapter receives only its engine's credentials, stores and CP-issued context;
it receives no CP database credentials, issuer administration secret or Docker
socket. Migration, seeding and domain observations are owner responsibilities.
The common controller retains issuer issuance, CP bootstrap/governance, isolation,
source checking, native identity observation, receipt publication and recovery.

Environment bindings reference generated private context fields. Literal secrets,
endpoints, protected environments, security bypass flags, host paths, undeclared
capabilities and client rights above the registry ceilings are refused. Normal
CP maker/checker and provider lifecycle remain mandatory. ADR-SHARED-043 permits
disposable synthetic development; ADR-SHARED-017/036 and protected gates retain
their existing ownership and meanings.

ENG-ONB-01 through ENG-ONB-09 are engineering criteria, not aliases for INT/NAB
cases. Receipts separately report source declaration, current authority, observed
native operations and certification for each capability. Payments sandbox outcomes
must remain simulated; `PSP_NOT_CONFIGURED`, `NATIVE_PAYMENT_NOT_CERTIFIED` and
`PRODUCTION_BLOCKED` are separate from successful development simulation. No
sandbox result grants subscription entitlements or moves external money.

Schema and examples passing CI establish source conformance only. CLI/runtime,
Codespaces and first-adopter acceptance require their own actual receipts. The
baobab-dev provider security/lock hold is not lifted by this contract.
