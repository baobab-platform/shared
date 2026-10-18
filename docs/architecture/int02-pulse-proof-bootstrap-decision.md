# INT-02 Pulse proof-bootstrap decision

**Status: ACCEPTED — NAMED SYNTHETIC EVIDENCE-PRODUCER EXCEPTION; QUALIFICATION PENDING**
Date: 18 October 2026  
Scope: Infrastructure #35, L4-CP-02, disposable real-component synthetic-data laboratory only  
Governing: Accepted ADR-SHARED-036; EA v2.2 mandatory matrix; existing workload lifecycle; ADR-SHARED-032; CP ADR-BCP-025; Pulse ADR-PULSE-018/019.

Owner approval: [18 October 2026](https://github.com/baobab-platform/shared/pull/346#issuecomment-6244904207), also explicitly approved in the implementation session.

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

Before this decision, the canonical `baobab-int02-pulse-consumer` ceiling was PROVISIONED.
CP correctly refuses its tokens. The workload promotion rule requires actual
resource-server acceptance and caller-bound CP validation before ACTIVE, so
the caller cannot produce that proof under the current rule. The existing
FB-05 provisioning-evidence exception names another workload and cannot be
reused implicitly. This is a lifecycle decision, not a library-version defect.

## Latest concrete real-component result

Infrastructure [run 39090331827](https://github.com/baobab-platform/infrastructure/actions/runs/39090331827),
harness `ae6dafee1e237f75992b601f8ea75fdbd062827a`, passed all seven native
Pulse observations: actual persisted vector search, canonical hydration,
classification/tenant denial, stale projection detection, separate native
PostgreSQL/Qdrant and verified-HTTPS full semantic readiness. The four
IAM/CP groups above passed again, with all 14 browser and 16 record-isolation
checks. TLS passed and all disposable resources were destroyed.

The scrubbed receipt artifact `12122871802` is retained with digest
`sha256:83896f342f4a0a4e36d7c6c6a7721cfd1750577d049acd3383ad728370e3af90`.
L4-CP-02 remains BLOCKED and the workflow correctly fails; all other repository
checks completed (25 success, six applicable skips). This native proof provides
no HTTP caller/CP qualification or independent provider certification. The
accepted exception below permits producing the missing proof; that proof remains pending.

## Accepted owner ruling

Authorize one additional **named evidence-producing identity** before its
end-to-end proof, solely to produce INT-02 synthetic qualification evidence:

| Field | Exact accepted boundary |
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

Only that existing registry row is ACTIVE under this named exception. Shared's
contract validator pins the entire row, including the absence of additional
fields. No other PROVISIONED workload is promoted; the default lifecycle rule
remains unchanged. Registry acceptance creates no credential, grant or binding.

### Bootstrap and qualification states

The initial state is **BOOTSTRAP / REQUIRED_NOT_EXECUTED**. In each disposable
run, the named client may obtain its two audience-limited credentials and use
explicit synthetic grants to produce the first proof. Missing first proof is
not an IAM issuance or CP context denial in this state. No CP certification or
provider-health gate is bypassed: these are separate facts that the harness
must establish through owning APIs before it may report qualification.

The bootstrap window starts when the run creates its client and ends on
success, failure or the 75-minute live-job timeout. Teardown always destroys
the client, sessions, credentials, database volumes and network. A new run
starts a new bootstrap window with new credentials; it never inherits a green
receipt or an expired certification from another run.

Only after all mandatory checks on the final exact pins, current scoped
certification/health, independent maker/checker and teardown pass may that run
report **QUALIFIED_SYNTHETIC_RUN**. Missing, stale or revoked proof then
invalidates that run's qualification result. A source/pin change requires a
fresh complete run. This is an evidence acceptance rule, not an additional CP
runtime policy or a durable real-tenant activation. In both states, unexpected
scope/owner/issuer/environment or absent explicit authority fails closed.

ACTIVE means **permitted to produce synthetic proof**. It never establishes
that Pulse is qualified for a real tenant, protected staging or production.
Receipts must identify this decision, the exact Shared revision and the
per-run qualification state independently of workload ACTIVE status.

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

## Considered alternative (not selected)

Design a canonical, human-sponsored, expiring qualification-lease/context
protocol in Shared/CP/IAM that permits a PROVISIONED identity to produce proof
without giving it ordinary RUNTIME authority. This is a broader architectural
increment requiring new contracts, grant/purpose semantics, production fences,
validator behavior and acceptance. It cannot be improvised as a test flag or
an alternate registry loader. Prefer this if owner policy rejects another
named evidence-producing exception.

## Exit and rollback

The owner accepted the exact identity and boundary on 18 October 2026. Any
extra scope, changed owner, production credential, untrusted issuer or missing
cleanup fails closed. An absent first proof keeps bootstrap unqualified; after
a successful qualification, absent/current-proof failure invalidates that
qualification as described above. Infrastructure #35 remains blocked until all
mandatory real scenarios pass. Rollback suspends/revokes the canonical row,
disables the disposable client, destroys its credentials/runtime and reruns
refusal tests. This decision creates no real enterprise or production access.
