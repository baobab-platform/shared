# ADR-SHARED-034 — ERP Posting Authority Resolution and Native Placement Boundary

**Status:** Accepted — Normative Shared Contract Architecture (platform owner decision, 2026-10-14)  
**Date:** 2026-10-14  
**Repository:** `baobab-platform/shared`  
**Decision ID:** ADR-SHARED-034  
**Work item:** P0-04B ERP execution-point enforcement (EA v2.1 EA-R03, CP completion plan §13)  
**Depends On:** ADR-0005, ADR-SHARED-012, ADR-SHARED-033 (Proposed), ADR-BCP-026, ADR-BCP-027, ADR-ERP-021  
**Semantic Owners:** Control Plane (authority), `baobab-erp` (native placement and accounting execution)  
**Canonical Contract:** `contracts/erp/v2/posting-authority.schema.json`, `contracts/erp/v2/posting-operations.yaml`

---

## 1. Decision

An ERP accounting operation is authorised by joining two authorities at the moment of the operation. Neither engine gains authority it does not own.

| Element | Authority |
|---|---|
| Tenant, operating Organisation, market | Control Plane RUNTIME context |
| Verified responsible legal entity, mandate, role, activity | Control Plane `OperatingLegalActorMandate` (ADR-BCP-027) |
| Engine instance bound to the tenant | Control Plane capability binding |
| Native placement (which client/organisation an operating Organisation lands in) | ERP placement registry (ADR-ERP-021) |
| Which native document is which operation class | ERP execution policy |
| Period, tax and Finance baseline readiness | ERP (ADR-ERP-008); never conferred by CP |

Three separate contracts keep the lifecycles apart:

- **`ErpAssignment`** (`control-plane/v1`): what ERP is authorised to *provision*. Unchanged. Provisioning is not posting authority.
- **Native placement**: where ERP *placed* it. ERP-owned; Shared carries only an opaque `{placement_id, placement_version}` reference. No native client, organisation or table identifier crosses the boundary (ADR-SHARED-033 §5, `erp/v1` vendor-field rule).
- **`ErpPostingAuthority`** (`erp/v2`): whether this operating Organisation may perform this catalogued accounting operation now, for which legal actor and market.

An ERP placement never creates authority. A holding company's placement cannot authorise it to post for an operating business without that business's own ACTIVE mandate for the role, activity and market. Group ownership is not a mandate.

## 2. Resolution

`PostingAuthorityRequest` names only a workload-owned RUNTIME `context_id`, the `engine_instance_id`, an `operation_class`, the opaque placement reference and an `operation_reference`. CP:

1. redeems the context for the calling workload (owner, RUNTIME purpose, expiry, active tenant);
2. requires the engine instance to be bound to the tenant's ERP capability, else `ENGINE_INSTANCE_NOT_BOUND`;
3. derives role and activity from `posting-operations.yaml`, so the caller cannot choose them;
4. resolves the mandate with the existing legal-actor semantics (exact match, `AMBIGUOUS` on more than one, revoked, expired or unverified fail closed);
5. persists an immutable decision record and returns its `decision_id`.

An `AUTHORIZED` decision expires at most 30 seconds after evaluation and never after the context or mandate. It is bound to one `operation_reference` and is not reusable, cacheable as a grant, or evidence of provider or finance readiness (`provider_permissions_granted` is always `false`).

## 3. Historical attribution

CP mandates are immutable: an amendment is a new mandate naming `supersedes_mandate_id`. The `mandate_id` therefore pins the exact version that applied. ERP stores `decision_id`, `mandate_id`, `supersedes_mandate_id`, the mandate's effective start, the responsible legal entity and the placement reference with the posting, in the same database transaction. Together with CP's retained decision this answers ADR-BCP-027 §10.2: which legal actor applied to a transaction at time T, not only today's mapping.

## 4. Freshness and atomicity

A synchronous CP call cannot join ERP's database transaction. The two guarantees are separate and both required:

- **Database atomicity.** The authority attribution and the native financial mutation commit or roll back together in ERP's transaction.
- **Bounded freshness.** ERP must deny at database COMMIT once `min(expires_at, ERP's own receipt time + 30 seconds)` has passed, so a decision that claims a longer lease can never extend a posting. Because JSON Schema cannot compare timestamps, every consumer must also check `evaluated_at < expires_at <= evaluated_at + 30 s` and that the decision echoes its request. A revocation therefore takes effect within the lease (30 seconds at most). Where that bound cannot be met, the operation is denied ([OWASP Authorization Policy and Data Distribution Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Policy_And_Data_Distribution_Cheat_Sheet.html)).

## 5. Catalogue

`posting-operations.yaml` is closed, and the decision schema binds each `operation_class` to exactly its catalogued role and activity, so a decision for one class can never carry another class's authority. Each class names one legal-actor role (ADR-BCP-027 §6.1: ledger posting is `ACCOUNTING_ENTITY`, a tax invoice `INVOICE_ISSUER`) and one activity that a mandate must scope. The activity vocabulary is new in this ADR and must match how mandates are written; the platform owner reviews it with this change. `capability_key` stays null until ADR-SHARED-033 registers finance keys; a null key matches only mandates without a capability scope.

## 6. Consequences

- The scope `erp-posting-authority:resolve` is workload-only and non-authorising. It is granted only to the PROVISIONED ERP staging assessor; no workload is activated by this ADR.
- CP implements the resolver in nonproduction environments behind an explicit flag and client allowlist. Production posting stays denied.
- ERP implements placement, document provenance, the JVM veto and a database COMMIT fence. Atomic posting is certified only by a run against a real iDempiere runtime and PostgreSQL (EA v2.1 Gate D), never by contract or synthetic tests.
- Accounting configuration tables (schema, chart, tax) are not operation classes. ERP keeps denying them in protected runtimes until a separate governed decision exists.

## 7. Not decided here

Real mandates, placements and approvers; IAM workload activation; provider certification; production enablement; the finance capability keys (ADR-SHARED-033).
