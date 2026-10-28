# PROPOSAL — TMS native-execution authority v1 (EA v2.3 / EA-DEV)

**Decision status: PROPOSED / NOT ACCEPTED.** No executable CP API, IAM token scope, workload registration, capability binding, or trust key is issued by this document or accompanying schema. Explicit user direction: **do not merge any PR without authorisation**.

## Scope and ownership

- **Shared** owns canonical resource, event and identity/scope contracts and the reviewed registered TMS workload profile. The separate reviewed draft schema `proposals/tms-native-execution/v1/decision.schema.json` is NOT an active `contracts/` schema.
- **IAM** issues and independently revokes workload identities, registering the exact TMS resource-server audience. It does **not** issue legal actor or tenant/market mandates. The TMS resource server must verify its incoming subject token; the CP validator authenticates to CP with its own independent workload token.
- **CP** owns current Tenant, operating Organisation, legal actor/mandate, Market, capability entitlement, binding/release, approved plan, revocation/suspension and a monotonic fencing generation / operation lease. CP must independently evaluate caller and intended operation against the current objects; the proposed ALLOW is not a bearer credential and cannot be accepted when stale or from user input.
- **TMS** owns operation-specific eligibility and native booking/capacity/transport execution, plus durable first-party domain ledger, attempts/outbox/inbox and provider-neutral readback. Neither Fleetbase Company nor Open TMS orgId is a CP Principal or Tenant.

## Confirmed source gaps

Shared `contracts/identity/v1/workload-registry.yaml` currently registers **no TMS validator**. Shared `contracts/control-plane/v1/execution-operation.schema.json` has no TMS-native operation type. CP `POST /v1/platform-context/validate` only establishes that a context belongs to the actual verified subject, not an operating legal mandate or an action grant; `POST /v1/capabilities/resolve` only redeems the caller's **own** context. These surfaces must not be treated as a TMS-native execution ALLOW. The proposed decision JSON deliberately names Tenant, Organisation, legal entity, Market, IAM Principal/client, provider/binding/release, intent hash, absolute expiry and fencing generation.

## Proposed owner decisions before acceptance

1. Register `baobab-tms` as a resource-server audience and a **development-only** independent TMS validator workload with `aud=baobab-control-plane`, `context:validate`, `validates_audiences: [baobab-tms]`; use a status that does **not** provision credentials or grant authority until IAM/CP integration tests and owner approval. Define the calling workload and subject audience separately. No default scope gives native dispatch authority.
2. CP/API owner must select a versioned, authenticated TMS-native execution decision API and explain which current mandate, binding, release, provider health/entitlement and action-specific eligibility checks it owns; decide signed or online readback semantics. Avoid extending a generic `ExecutionOperation` enum with misleading success meaning if a separate operation lease contract is more appropriate.
3. Bind decision to verified issuer/subject and canonical Principal ID, exact action + aggregate/resource, intent digest, legal actor, market, Tenant, isolation profile, current CP capability binding revision and native release, expiry, current lease generation and revocation.
4. Define lease-claim/release/readback and permitted staleness. **An ALLOW must be rechecked immediately before irreversible native booking or capacity effect.** Unknown outcomes require provider-native idempotency and observation; approval cannot be created locally.
5. Classify `native.provision` and `tms.booking.submit` separately. Confirm whether CP mandates/approvals authorize the external carrier purchase independently of canonical first-party plan/booking. The accepted TMS ADRs imply separate booking authority; do not infer it from a plan draft.
6. Publish additive Shared contracts, owner-approved tests, CP provider and IAM profile/registry PRs; separately execute real issuer+CP synthetic A/B positive, wrong-audience, revocation, wrong-tenant/market/legal actor, stale fencing and independent cleanup.

## Qualification exit

This PR is **a contract review proposal only**. All protected native TMS operations remain HELD. Accepted Shared/CP/IAM contract, completed source adoption and runtime readback are separate verifiable gates. No Fleetbase commercial licence, native provider activation, carrier qualification or production readiness follows from proposal review.
