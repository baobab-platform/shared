# INT-02 Pulse proof-bootstrap decision request

**Status: PROPOSED — OWNER DECISION REQUIRED; NOT AN ACTIVATION**  
Date: 18 October 2026  
Scope: Infrastructure #35, L4-CP-02, disposable real-component synthetic-data laboratory only  
Governing: Accepted ADR-SHARED-036; EA v2.2 mandatory matrix; existing workload lifecycle; ADR-SHARED-032; CP ADR-BCP-025; Pulse ADR-PULSE-018/019.

## Problem and actual evidence

Infrastructure run `39006461245`, harness `272697ca96bf7aa08dbbb1b805e2b8acd4f8cc4a`,
passed L4-IAM-01, L4-IAM-02, L4-CP-01 and L4-CP-03. L4-CP-02 remains BLOCKED:
its provider binding is synthetic and no current real-provider qualification
has been recorded. IAM #119 has now merged after all 44 final-head checks and
its review correction, at `9b8b0b4a401139ed9055fd5947ca3b1b7e0f3f8e`.

Infrastructure #35 now prepares actual source/image-pinned Pulse with isolated
PostgreSQL and a separate Qdrant server. Native conformance independently
checks canonical persistence, actual vector retrieval and canonical hydration,
classification/tenant isolation, stale projection and dependency readiness.
These are necessary observations, not caller authentication, CP authority,
resource-server acceptance or certification. Reference embeddings are
deterministic; no production model-quality claim follows.

The canonical `baobab-int02-pulse-consumer` ceiling exists but is PROVISIONED.
CP correctly refuses its tokens. The workload promotion rule requires actual
resource-server acceptance and caller-bound CP validation before ACTIVE, so
the caller cannot produce that proof under the current rule. The existing
FB-05 provisioning-evidence exception names another workload and cannot be
reused implicitly. This is a lifecycle decision, not a library-version defect.

## Proposed owner ruling

Authorize one additional **named evidence-producing identity** before its
end-to-end proof, solely to produce INT-02 synthetic qualification evidence:

| Field | Exact requested boundary |
|---|---|
| Client | Existing `baobab-int02-pulse-consumer`; no wildcard or general qualification class |
| Owner | baobab-platform/infrastructure |
| Canonical environment | development; executor profile INT-02 integration |
| Audiences | baobab-control-plane and baobab-pulse only; independent audience-limited tokens |
| Scopes | context:resolve and intelligence:evidence:search only |
| Classification | Existing CONFIDENTIAL ceiling; RESTRICTED remains denied |
| Credential | New OS-random client secret for each disposable run; exact ephemeral issuer |
| Issuance | Infrastructure fixture only; no client file in IAM's ordinary production bootstrap |
| Data/authority | Synthetic Principals/Organisations/Tenants and explicit tenant grants only |
| Network | Internal per-run network, verified per-run CA, no published ports |
| Duration | Client, sessions, keys, volumes and network destroyed on success/failure |
| Exclusions | No mutation, validator, provisioning, deployment observation, provider administration or certification scope |

After explicit owner acceptance, a separate implementation change would make
**only that existing registry row ACTIVE under this named exception**, with
Shared validators pinning every field above. No other PROVISIONED workload is
promoted, and the default lifecycle rule remains unchanged. This proposal
itself changes no registry status and creates no credential, grant or binding.

ACTIVE under this exception would mean **permitted to produce the synthetic
proof**, not that the proof has passed or that Pulse is qualified for any
real tenant, protected staging or production. The receipt must state that
distinction and identify the owner decision and exact Shared revision.

## Engineering required after acceptance

1. Pin the accepted Shared change and merged IAM/CP/Pulse sources; load the
   unmodified canonical registry. Never edit its materialised snapshot or
   disable lifecycle checks to get a token accepted.
2. Create the one disposable IAM client with exact scope/audience mappers,
   per-run secret, short token lifetime and no human/password/admin grants.
   Prove wrong audience, nonactive client and wrong credential independently;
   do not broaden any existing platform or product client.
3. Resolve the caller's actual CP context, invoke Pulse's normal HTTP API and
   require Pulse's independent ACTIVE validator to redeem that context with
   the caller's token. Prove another owner/context/tenant is denied.
4. Tie actual PostgreSQL hydration and Qdrant observations to the qualified
   source/image/contract declaration. Native-only conformance must not stand
   in for this resource-server positive.
5. Use actual EngineRelease and ProviderCapabilityCertification APIs with
   separate browser-authenticated synthetic maker/checker Principals. Record
   immutable scrubbed evidence digests. No SQL-written certification or
   provider self-certification; approval, certification, health and activation
   remain distinct facts.
6. Require current qualification plus actual provider/instance health. Observe
   missing grant/binding, wrong contract/market/instance/isolation, stale health
   and actual provider outage without fallback. Every negative needs its
   corresponding live positive and an exact policy result.
7. Re-run every mandatory IAM/CP scenario on the final exact pins; retain
   sanitized evidence and fail the workflow for any FAIL/BLOCKED/missing case.
   Demonstrate teardown. Only then consider Infrastructure #35 merge.

## Alternative without a named exception

Design a canonical, human-sponsored, expiring qualification-lease/context
protocol in Shared/CP/IAM that permits a PROVISIONED identity to produce proof
without giving it ordinary RUNTIME authority. This is a broader architectural
increment requiring new contracts, grant/purpose semantics, production fences,
validator behavior and acceptance. It cannot be improvised as a test flag or
an alternate registry loader. Prefer this if owner policy rejects another
named evidence-producing exception.

## Exit and rollback

Owner acceptance must identify this exact identity/boundary and its decision
date before the registry/issuance change is activated. If rejected, the row
stays PROVISIONED and #35 stays BLOCKED while the alternative is designed.
After acceptance, any extra scope, changed owner, production credential,
untrusted issuer, missing cleanup or absent current proof fails closed.
Rollback suspends/revokes the named canonical row, disables the disposable
client, destroys its credentials/runtime and reruns the refusal tests. No
real enterprise or production access is created by this decision.
