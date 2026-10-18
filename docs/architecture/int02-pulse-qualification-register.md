# INT-02 Pulse provider qualification register

Date: 18 October 2026. Status: BOOTSTRAP APPROVED / QUALIFICATION REQUIRED_NOT_EXECUTED.
Authority: Accepted ADR-SHARED-036, ADR-SHARED-032, existing workload lifecycle
rules, CP ADR-BCP-025 and Pulse ADR-PULSE-018/019. The owner accepted the
[named proof-bootstrap decision](int02-pulse-proof-bootstrap-decision.md) on 18 October 2026.

## Implemented allocation

`baobab-int02-pulse-consumer` is an Infrastructure-owned, integration-only,
ACTIVE named evidence-producing client-credentials ceiling in the canonical `development`
environment (the executor profile is named INT-02 integration). Its two
audiences/scopes let a future actual caller resolve its own CP context and
request evidence search at Pulse. The base search scope has the existing
CONFIDENTIAL classification ceiling; it is not PUBLIC-only. Restrict fixtures
to synthetic data, test that RESTRICTED results remain denied, and never infer
a real tenant grant from that ceiling. No additional RESTRICTED clearance,
validator authority, mutation,
provider administration, deployment observation or certification scope is
allocated. Credentials must be generated per disposable run and never supplied
for production, protected staging or a real enterprise. No Tenant, grant,
DigitalEstate, binding or provider support is created by this registry row.

## Required ordered closure

1. Apply the accepted named proof-bootstrap boundary. Each disposable run
   starts BOOTSTRAP / REQUIRED_NOT_EXECUTED, may produce its first proof, and
   ends on success/failure or the 75-minute job timeout with mandatory teardown.
   Absent first proof keeps the run unqualified; it does not prevent producing
   that proof. Only a complete final-pin run may report QUALIFIED_SYNTHETIC_RUN.
   Missing/stale proof subsequently invalidates that qualification. Do not edit
   a pinned snapshot or extend this exception to another identity or environment.
2. IAM implements the accepted disposable issuance profile. The resulting
   real token must carry exactly the registered client, issuer, audience and
   operation scopes; unrelated audience, nonactive client and stale credential
   negatives must be independent. No product client receives extra scopes.
3. Infrastructure runs exact source/image-pinned Pulse, PostgreSQL and Qdrant
   processes with actual IAM/JWKS and caller-bound CP context adapters. State
   which embedding implementation is used; deterministic reference embeddings
   are not a model quality or production intelligence claim.
4. Exercise a real authorised search over seeded synthetic canonical evidence,
   verify persisted identity/context/tenant lineage and exact historical result
   hydration, then exercise wrong tenant/context owner, missing grant/binding,
   contract/market/instance/isolation mismatches and actual provider outage.
   Liveness, readiness, CP resolution and domain success are distinct facts.
5. Record the exact built-image and contract/provider-declaration digests and
   immutable scrubbed conformance evidence through the real EngineRelease and
   ProviderCapabilityCertification APIs with independent fixture maker/checker
   identities. No direct SQL certification or provider self-certification.
6. Recheck current scoped qualification, current instance/provider health and
   all mandatory negatives on the final pin set. Source qualification and
   disposable certification tests cannot authorise protected staging or
   production. Shared stewards evaluate qualification only against the accepted proof
   ceremony and actual evidence, independently of the ACTIVE producer status.

## Current disposition

The executable Pulse provider declares IMPLEMENTED evidence search, but the
existing INT-02 fixture is only a synthetic resolution row. L4-CP-02 remains
BLOCKED. This allocation removes an absent vocabulary ceiling; it supplies
no credential or qualification. The accepted proof-bootstrap decision permits
producing the required evidence. Infrastructure
#35 must stay open until this and every other mandatory real scenario passes.
