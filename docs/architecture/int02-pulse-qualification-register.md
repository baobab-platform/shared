# INT-02 Pulse provider qualification register

Date: 18 October 2026. Status: QUALIFIED_SYNTHETIC_RUN / ACTIONS SOURCE QUALIFICATION ONLY.
Authority: Accepted ADR-SHARED-036, ADR-SHARED-032, existing workload lifecycle
rules, CP ADR-BCP-025 and Pulse ADR-PULSE-018/019. The owner accepted the
[named proof-bootstrap decision](int02-pulse-proof-bootstrap-decision.md) on 18 October 2026.

## Implemented allocation

`baobab-int02-pulse-consumer` is an Infrastructure-owned, integration-only,
ACTIVE named evidence-producing client-credentials ceiling in the canonical `development`
environment (the executor profile is named INT-02 integration). Its two
audiences/scopes let the disposable actual caller resolve its own CP context and
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

## Accepted synthetic run — 18 October 2026

[Infrastructure #35](https://github.com/baobab-platform/infrastructure/pull/35)
is merged at `03ad3f488e19ad446328ba6827363730e4252409`. [Final-pin Actions run 39108198886](https://github.com/baobab-platform/infrastructure/actions/runs/39108198886)
passed L4-IAM-01/02 and L4-CP-01/02/03, including 14 actual browser/MFA,
16 Organisation-isolation, 11 Pulse HTTP, seven native and 19 provider
qualification checks. Verified TLS and successful teardown are in the receipt.
The exact executing harness is `d760256a53cb0f80d665c94c24b2cc939e4eba86`; dependency
baselines remain distinct from that executing source identity.

| Source | Qualified revision |
|---|---|
| baobab-cp | `34fc86a5bf276dfb80760710fe32a34d2431558a` |
| baobab-iam | `9b8b0b4a401139ed9055fd5947ca3b1b7e0f3f8e` |
| baobab-pulse | `6f4271d7b43db8d9c81e04d4f5dcc4cf50b27172` |
| shared | `33f1dd6aa7c0db43743dbb02cff16d5dc0802610` |

[Retained artifact 12128983186](https://github.com/baobab-platform/infrastructure/actions/runs/39108198886/artifacts/12128983186) has ZIP digest `sha256:6713419967aadc358194b3e4048746f2c7e05c83960d41d7d54963c1375ee18a`.
The receipt's self-digest is `sha256:25aa7c08ad07bee0e7cc78df72e0148409117dcc02389b5726d09a58dec032bd`. The frozen provider-proof digest
is `sha256:9c955a09bf100f0686fcf9c7b3151c96a91d213d5fd7ae963be3ca95ba3a2194` and the image-manifest digest is
`sha256:c93d1d5ce5a42d81c2de50af9d12dec5f2eef57009068c06e89459b85a17bf1b`. Downloaded artifact verification
confirmed all four digests, the running image configuration identity,
`teardown_verified: true`, `passed: true` and `QUALIFIED_SYNTHETIC_RUN`.

Actual owning APIs recorded the source-bound EngineRelease and independent
ProviderCapabilityCertification, refused recorder self-certification, approved
the release and activated the provider through reviewed changesets, and tested
certificate revocation/replacement. Current certification and all three health
levels were rechecked after actual provider outage and recovery. Missing
grant/binding, wrong contract/market/instance/isolation and expired health were
observed independently. CP #415 repaired nested canonical-scope verification;
CP #416 made isolation-restricted binding eligibility require trusted profile
evidence. Both merged after their CI and clean reviews.

Health observations were explicitly written to CP's ephemeral canonical table
from actual HTTPS readiness/search and the actual stopped-provider fault; that
CP revision has no health-ingestion HTTP endpoint. STANDARD UNKNOWN remains
eligible under Shared policy, while current HEALTHY evidence is independently
mandatory for this qualification. Reference embeddings remain deterministic.

This is acceptance of one source-pinned, synthetic-data INT-02 Actions run.
The run uses the same integration Dev Container and entrypoints as Codespaces;
an independently observed interactive Codespaces session is not asserted.
The client, credentials, sessions, databases, vector volume and private network
were destroyed. Its test certification does not survive as operational
certification. A changed pin or stale evidence requires a new complete run.
INT-03 Nabhold/IAM/CP/BFF/CMS consumption is next and remains unaccepted. No
real enterprise onboarding, legal authority, protected staging or production
permission follows. Rollback retains the named decision's suspension/revocation
procedure and reruns the refusal suite; source regressions fail qualification.
