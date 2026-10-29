# TMS native-execution authority v1 — accepted development design

**Decision status: ACCEPTED — architecture and development contract design only.**
Authority: the platform owner's instruction in the DEV-07 implementation review
to audit Shared #409 against ADRs and accept it once correct. Acceptance applies
to the corrected revision, following schema and semantic conformance checks.
The files remain under `proposals/` until additive active-contract adoption.
No CP endpoint, IAM credential, registry allocation, native execution permission,
provider certification or protected/production activation is created here.

## Governing sources and audit

Reviewed Shared base `ab7a473a1f69784f115ad353e36383faf9b95965`, CP
`6b0ec5fa70b4ccc2b7ab9ff0cd8829a080d355ff`, and TMS
`6fab69a36d6ea0fbc5520a2b09640bdc0d661ed1`. The governing decisions are
Shared ADR-017 (catalogue/provider/runtime separation), ADR-021 (owner-domain
references), ADR-036 (connected integration evidence), ADR-043 (development
authorisation), IAM ADR-0033 (Kratos/Hydra/federation responsibilities), and
accepted TMS ADR-0001/0004/0010/0011/0013/0015 as amended by ADR-0020/0021.
TMS's dated governance reconciliation ratifies the subsidiary ADRs; older
"Proposed" sentences inside them do not overturn that later ratification.

| Original finding                                                                     | Correction required for acceptance                                                                                                       |
| ------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------- |
| Decision did not identify issuer, subject audience, context or independent validator | Bind exact verified subject identity and registered client, CP context, actor Principal and a separate validator identity.               |
| Missing native binding, deployment, isolation and resource revision                  | Pin the independently read CP/native binding revisions, deployment, isolation profile, resource version, policy and release digest.      |
| Any operation could name any resource; approvals were optional                       | Closed operation/resource/authority-plane mapping and conditional plan/approval requirements.                                            |
| Nonempty identifiers and string revisions allowed malformed authority                | Reuse Shared canonical types; UUID identities, bounded fields and positive safe integer revisions/generations.                           |
| ALLOW had no claim protocol, temporal limit or independent expectation               | Authenticated online claim/readback, five-second maximum decision lifetime, earliest-evidence expiry and exact-current-state comparison. |
| DENY could omit a reason or assert a usable lease                                    | Closed refusal vocabulary; DENY contains no positive scope, claim, binding or approval fields.                                           |
| Tests checked schema text, rather than decisions                                     | Draft 2020-12 validation plus temporal/current-state negative fixtures; schema validity grants no authority.                             |

## Ownership and six resolved design decisions

1. **Identity allocation.** `baobab-tms` is the intended resource-server audience,
   not a new OAuth client or a credential. A separately registered future
   `baobab-dev-tms-validator` authenticates to CP with its own CP-audience
   workload token. Its context-validation profile is development-only,
   `PROVISIONED`, `context:validate`, `validates_audiences: [baobab-tms]`.
   That ceiling permits no native decision/claim API. A later Shared/IAM/CP
   allocation must register separate least-privilege decision, claim, renew,
   release and readback permissions before those APIs accept it. No wildcard,
   caller-supplied audience, default grant or production credential is allowed.
   TMS independently verifies the original caller's issuer, exact audience,
   client, subject, actor type, signature/current introspection and revocation.
   CP independently verifies the subject evidence through a registered
   relationship; the TMS-audience token is never the CP caller credential.

2. **Online CP authority.** Select a dedicated versioned authority/claim API,
   planned as `POST /v1/tms-native-authority/decisions`, `/claims`, and
   `/claims/{claim_id}/validate`, `/renew`, `/release`. These are design names,
   absent from active OpenAPI and unimplemented. CP owns the current canonical
   Principal, Tenant, Organisation, legal mandate, Market participation,
   entitlement, first-party provider/engine binding, release eligibility,
   registered isolation policy, desired-state/plan approvals and claim generation.
   TMS owns carrier/resource eligibility, domain relationships, native adapter
   selection, native health/credential observations and regulatory/documentary
   preconditions from their respective owners. CP does not duplicate TMS domain
   tables or certify native health from an assertion in this JSON.
   Generic context validation and capability resolution are necessary inputs;
   neither is this operation authority. A signed/offline decision is insufficient.

3. **Exact immutable binding.** An ALLOW binds every required schema field to
   authenticated, independently current source state. It names the subject and
   validator separately, exact action/resource revision and intent digest,
   primary and operating Organisations, legal actor, Market participation,
   environment, CP provider/engine/capability revision, native binding/deployment,
   provider release, isolation, policy, claim and execution attempt.
   Issuers compare exactly without URL rewriting. Resource IDs belong to TMS;
   they are not newly minted CP CanonicalEntities merely because the reusable
   identifier definition is named `canonicalEntityId`. Native vendor IDs remain
   scoped ExternalReferences. Foreign owner objects use ADR-021 typed/pinned
   references in the owner contract, not an untyped copied aggregate.

4. **Claim lifecycle and freshness.** CP atomically claims one exact operation
   scope and immutable intent for an authenticated claimant and attempt.
   Idempotency includes tenant, legal actor, subject/client, environment,
   action, aggregate and client key. Same key/digest retrieves the same outcome;
   changed digest conflicts. Claim/renew/validate must re-read current authority.
   A decision expires within **five seconds** of issue and never outlives any
   required evidence or the claim deadline. Renewal requires fresh readback;
   it grants no grace to a revoked or superseded generation. Reclaim advances
   the monotonic generation atomically. Release/complete uses compare-and-set
   on claimant, attempt, generation and intent; it never deletes history.
   The worker validates after durable claim and immediately before each native
   effect, then validates before recording completion. Stale/unknown authority
   blocks a new effect; a possible effect followed by uncertainty becomes
   `PROVIDER_UNKNOWN`, requiring native idempotency/readback without blind retry.
   Neither a five-second lease nor a post-effect check makes a remote effect
   globally atomic. If the native provider cannot enforce the required fence or
   prove non-duplication, that irreversible operation remains BLOCKED.

5. **Separate control and transport actions.** `tms.native.*` is CONTROL and
   requires a verified workload, governed CP `ExecutionOperation`, current
   execution attempt, immutable CP plan/desired-state digests and appropriate
   approval/authorisation. It follows the long-running CP lifecycle; this
   short-lived claim does not replace or silently extend `ExecutionOperation`.
   Provisioning may reconcile a governed non-ACTIVE desired binding; suspension
   and deprovision use their separate current control authority, retention/legal
   holds and safe teardown rules, not a customer's withdrawn data-plane grant.
   `tms.plan.revise`, booking, capacity and dispatch are DATA and cannot borrow
   CP provisioning fields. Booking submission and dispatch require a current
   approved transport-plan revision/digest; carrier booking submission additionally
   requires an independent purpose-bound carrier purchase authorisation.
   Development may supply synthetic authorisation under ADR-043; protected
   maker/checker, real carrier, financial, safety and legal gates remain mandatory
   where applicable. An approved plan is not a carrier purchase, Customs release,
   confirmed capacity, documentary access, payment or accounting permission.

6. **Adoption and proof.** Publish additive active Shared request/decision/claim,
   error and lifecycle contracts, exact IAM audience/scope/registry profiles and
   CP/TMS owning implementations in separately reviewed PRs. Pin their merged
   versions in consumers. Do not add an ACTIVE workload or extend a generic
   operation enum merely to make a fixture pass. ADR-043 permits separately
   scoped, leased synthetic development provisioning without per-run human
   approval; owner readback and cleanup still apply. Before marking any native
   operation qualified, execute actual IAM/CP and provider tests for independent
   Tenants A/B, wrong audience/client/subject, absent grant, revoked identity,
   wrong legal actor/Market/isolation/native deployment, expired decision,
   stale/reclaimed generation, changed plan/intent/approval, worker concurrency,
   replay/conflict, provider timeout/unknown outcome and independent cleanup.

## Contract and runtime boundary

The candidate schema defines syntactic binding and conditional obligations.
`decision-semantics.mjs` is a side-effect-free design reference for time and
independently supplied expectations, **not an authority SDK**. JSON Schema
cannot prove current IAM/CP state, compare timestamps, grant a mandate or
fence a native transaction. Consumers must enforce both kinds of check and
authenticated online source validation; copying decision fields into the
expected object is not independent verification. A DENY is an authenticated
minimal refusal, not disclosure of a foreign Tenant or a reusable claim.

All protected native TMS operations **remain HELD**. Architecture acceptance,
active contract adoption, source implementation, connected development proof,
provider certification and production authorisation are separate gates.
Fleetbase/Open TMS licence/security review, actual per-operation compatibility,
native database/cache/worker/socket isolation, real carrier qualification and
independently observed provider readiness remain required. No legacy
`trade.shipment.*` ownership, event namespace or canonical capability is changed.
This acceptance does not grant permission to merge or deploy another PR.
