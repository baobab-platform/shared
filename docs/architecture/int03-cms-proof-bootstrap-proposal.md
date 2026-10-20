# INT-03 CMS proof-bootstrap proposal

**Status: PROPOSED — NOT AUTHORISING**  
Date: 20 October 2026  
Owners for decision: Shared architecture, IAM, CP, CMS, Infrastructure and Security  
Execution lane: Accepted EA v2.3 P0-A; retained v2.2 INT-03/NAB matrix  
No registry, credential, grant, binding, provider support or release is changed by this proposal.

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
and `validates_audiences: [baobab-cms]`. That validator is not the Nabhold
consumer and grants no authority to read content or act for another Principal.
The CMS declaration remains PARTIAL and non-production; a registry ceiling
is neither provider qualification nor permission to broaden support.

Nabhold's canonical gateway/resolver and CMS's provider/context validator already
exist. Nabhold currently supplies a fixed runtime context and has no default
workload-token provider; automatic current-context issuance/refresh and actual
provider execution remain engineering tasks. Reimplementing these ports or
using the human identity token as a workload would evade the real blocker.

## Proposed owner decision, not an accepted exception

Approve or reject this finite evidence-producing boundary before any registry
promotion or runtime bootstrap implementation:

| Field | Proposed limit |
|---|---|
| Caller | New separately named `baobab-int03-cms-consumer`; do not activate or change `nabhold-backend` |
| Owner / executor | Infrastructure, with Nabhold/CMS/IAM/CP scenario owners |
| Canonical environment | development; isolated INT-03 synthetic integration only |
| Audiences | CP and CMS only, using independently audience-limited tokens |
| Scopes | `context:resolve` only at CP; `content:entry:resolve` only at CMS |
| Data ceiling | PUBLIC synthetic institutional content only; no personal, legal, payroll or business records |
| Credential | New OS-random confidential client secret per run; no product secret or static shared credential |
| Context | Current CP-issued RUNTIME context belonging to the same verified workload Principal; no supplied subject impersonation |
| Synthetic authority | Separate explicit synthetic Organisation/Tenant/estate/grants; corporate relationships confer no access |
| Provider | Actual source-built CMS, PostgreSQL and declared content/v1 route; retain current PARTIAL/non-production semantics |
| Validation | CMS's own independently authenticated validator presents the caller token as subject evidence under unchanged canonical constraints |
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

Reuse of the existing CMS validator is permitted only if its actual issued
credential satisfies its unchanged canonical owner/environment/audience/scope
constraints. A new validator environment or identity needs a separate owner
decision. Do not rewrite a materialised registry snapshot, set a production
client ACTIVE, disable lifecycle checks, mint a token or borrow the Pulse caller.

## Engineering and qualification order after an accepted decision

1. Converge CMS's Node 22 drift with the reviewed Node 24 toolchain while
   preserving maintained Payload/Next package compatibility and Codespaces.
   Source checks are not runtime/provider acceptance.
2. Implement the narrowly accepted registration/fixture using IAM-owned
   provisioning, exact read-back and ephemeral credentials. Preserve the
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

The normal lifecycle still applies unless this precise proposal is independently
accepted and implemented. A decision alone would permit producing synthetic
proof; it would not establish proof, provider acceptance, full INT-03, protected
native Kratos/Hydra C4, legal onboarding, protected staging or R0–R3/production GO.
Nabhold remains a non-trading holding/platform estate; subsidiaries remain
autonomous and independently isolated.

Rollback before acceptance is deletion of this proposal. After any future
accepted implementation, revert the named lab exception and disable its profile;
retain historical receipts without extending their scope.
