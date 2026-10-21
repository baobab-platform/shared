# INT-03 CMS proof-bootstrap decision

**Status: ACCEPTED — NAMED SYNTHETIC EVIDENCE-PRODUCER EXCEPTIONS; QUALIFICATION PENDING**
Proposed: 20 October 2026; accepted: 21 October 2026
Acceptance owners: Shared architecture, IAM, CP, CMS, Infrastructure and Security
Execution lane: Accepted EA v2.3 P0-A; retained v2.2 INT-03/NAB matrix
This decision authorises the bounded engineering below. This documentation change itself creates no registry row, credential, grant, binding, provider support or release.

Owner acceptance: [explicit Platform Owner approval](https://github.com/baobab-platform/shared/pull/354#issuecomment-6307263681), reaffirmed in the 21 October implementation session. Both named development identities below are accepted within the stated limits.

## Concrete blocker

At Shared `ba5b4523ffc82cbf1b1d804b4d88ab69be04843a`, the canonical
[workload registry](../../contracts/identity/v1/workload-registry.yaml) leaves
`nabhold-backend` PROVISIONED until actual IAM issuance, CMS resource-server
acceptance, caller-bound CP context validation and owner/tenant negatives pass.
A fresh source or identity-smoke result cannot promote it.

The [accepted Pulse bootstrap decision](int02-pulse-proof-bootstrap-decision.md)
says: "Only that existing registry row is ACTIVE under this named exception."
It names `baobab-int02-pulse-consumer`, not a CMS caller. Its audience,
scope, ownership and lifecycle exception must not be reused for CMS.

The existing CMS validator `baobab-cms-workload` is ACTIVE with CP audience
and `validates_audiences: [baobab-cms]`. That production validator cannot authenticate in this development run: the
registry forbids cross-environment credential use. It is also not the Nabhold
consumer and grants no authority to read content or act for another Principal.
This decision therefore requires **two separately named development identities**;
approving the caller alone cannot enable proof production.
The CMS declaration remains PARTIAL and non-production; a registry ceiling
is neither provider qualification nor permission to broaden support.

Nabhold's canonical gateway/resolver and CMS's provider/context validator already
exist. Nabhold currently supplies a fixed runtime context and has no default
workload-token provider; automatic current-context issuance/refresh and actual
provider execution remain engineering tasks. Reimplementing these ports or
using the human identity token as a workload would evade the real blocker.

## Accepted owner decision

Authorise exactly this finite evidence-producing boundary:

| Field | Accepted limit |
|---|---|
| Caller | New separately named `baobab-int03-cms-consumer`; do not activate or change `nabhold-backend` |
| Owner / executor | Infrastructure, with Nabhold/CMS/IAM/CP scenario owners |
| Canonical environment | development; isolated INT-03 synthetic integration only |
| Audiences | `baobab-control-plane` and `baobab-cms` only, using independently audience-limited tokens |
| Scopes | `context:resolve` only at CP; `content:entry:resolve` only at CMS |
| Data ceiling | PUBLIC synthetic institutional content only; no personal, legal, payroll or business records |
| Credentials | Two distinct OS-random confidential client secrets per run, one per named development identity; no product secret, shared secret or production credential |
| Context | Current CP-issued RUNTIME context belonging to the same verified workload Principal; no supplied subject impersonation |
| Synthetic authority | Separate explicit synthetic Organisation/Tenant/estate/grants; corporate relationships confer no access |
| Provider | Actual source-built CMS, PostgreSQL and declared content/v1 route; retain current PARTIAL/non-production semantics |
| Validator | Separate `baobab-int03-cms-validator`, owner CMS, environment development; audience `baobab-control-plane`, scope `context:validate`, `validates_audiences: [baobab-cms]` only; no context:resolve, content, provisioning, migration or administration scope |
| Validation | This separate development validator presents the caller token as subject evidence; it never becomes the caller or receives content-read authority |
| Window | One disposable run, at most the existing 90-minute INT-03 job timeout; no inherited proof or durable client |
| Destruction | On success/failure/interruption, destroy clients, secrets, sessions, containers, volumes, network and per-run keys |

Explicit exclusions: preview scope, mutations/publication scope, provisioning,
validator scope on the consumer, provider/certification administration, executive
authority, real Tenant onboarding, production activation and wildcard exceptions.
A published-content fixture may be seeded by CMS-owned disposable setup; this
does not prove a human editorial publication approval or mutation journey.
Preview/draft requests must be denied to this read-only caller. Any later
positive preview/editorial flow requires its own explicitly authorised actor,
scope and CP/domain permission; it cannot silently widen this proposal.

**Both named development identities are accepted for this bounded proof.** The caller exception alone is insufficient: without the separate
development validator, caller-bound CP context redemption is BLOCKED. The
existing production `baobab-cms-workload` row and credentials remain unchanged
and cannot be used here. The development validator gets no business authority and
may validate only the CMS audience; independent wrong-audience, wrong-owner,
wrong-environment and swapped-identity negatives must pass. Do not rewrite a
materialised registry snapshot, set a production client ACTIVE, disable
lifecycle checks, mint a token outside the accepted fixture or borrow the Pulse caller.

## Bounded pre-proof lifecycle exceptions

When implemented in the canonical registry, **only**
`baobab-int03-cms-consumer` and `baobab-int03-cms-validator` may be `ACTIVE`
before first proof under this decision. ACTIVE means permitted to produce
synthetic evidence, never provider qualification or durable product activation.
This is an explicit exception to the pre-proof PROVISIONED rule for both named
identities; neither needs the proof it is being created to produce. The
production `nabhold-backend` remains PROVISIONED and the production CMS
validator remains unchanged. No wildcard/bootstrap class is introduced.

The implementation SHALL pin each complete registry row with contract validation,
including exact owner, development environment, audience, scopes and absence of
extra authority-bearing fields. IAM-owned fixture provisioning SHALL consume the
unmodified approved registry, create two independent per-run secrets, read back
the exact client ceilings and forbid ordinary production bootstrap issuance.
A reviewed registry change is required before either identity can authenticate;
this document does not alter a materialised snapshot or bypass lifecycle checks.

Each disposable run begins in **BOOTSTRAP / REQUIRED_NOT_EXECUTED** when its
clients are created. Lack of first proof does not itself deny this bounded
bootstrap. The window closes on success, failure, interruption or the existing
90-minute job timeout, whichever occurs first. Always destroy clients, sessions,
secrets, keys, volumes, containers and network. A new run uses new secrets and
cannot inherit qualification or certification from an earlier run.

Only a scenario-complete receipt at exact final pins, current independent
maker/checker certification, health/binding and successful teardown may report
**QUALIFIED_SYNTHETIC_RUN**. Missing/stale/revoked evidence invalidates that
qualification. Unexpected issuer, environment, scope, owner or missing explicit
tenant authority fails closed in both states. No EngineRelease, certification,
health or binding gate is bypassed. Receipts SHALL identify this decision, exact
Shared revision and per-run qualification state separately from ACTIVE status.

## Engineering and qualification order

1. Converge CMS's Node 22 drift with the reviewed Node 24 toolchain while
   preserving maintained Payload/Next package compatibility and Codespaces.
   Source checks are not runtime/provider acceptance.
2. Implement their registration/fixture using IAM-owned provisioning, exact
   read-back and independent ephemeral credentials. Preserve the
   canonical registry's unmodified approved snapshot and fail-closed lifecycle.
3. Adapt maintained confidential client-credentials acquisition and CP context
   issuance/refresh into the existing Nabhold ports. Independently scoped tokens
   must resolve and redeem the same Principal's current context.
4. Run the actual source-built CMS and storage. Prove exact published home/nav/
   footer content through Nabhold with fallback disabled for qualification.
   Test wrong audience/credential, disabled/expired/revoked caller, missing
   grant, wrong owner/context, neighbour Tenant, draft/preview, withdrawal,
   unavailable dependencies and restoration. Use existing normative scenario IDs.
5. Use current EngineRelease, independent maker/checker certification,
   health/binding and provider resolution APIs. No SQL-written qualification or
   self-certification. If PARTIAL support or another current policy blocks
   resolution, report BLOCKED; do not advertise fuller support to make it pass.
6. Retain exact source/image/runtime provenance, fixed outcomes and hashes;
   require all applicable canonical NAB/L4 cases, durable consequences and
   teardown. Keep identity-only smoke, local synthetic integration, protected
   staging and production as separate facts.

The normal lifecycle remains binding outside these two named exceptions. This
decision permits producing synthetic proof; it does not establish proof, provider acceptance, full INT-03, protected
native Kratos/Hydra C4, legal onboarding, protected staging or R0–R3/production GO.
Nabhold remains a non-trading holding/platform estate; subsidiaries remain
autonomous and independently isolated.

Rollback suspends/revokes both named lab identities, disables their profile and
destroys disposable credentials and runtime resources;
retain historical receipts without extending their scope.
