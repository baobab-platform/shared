# FIN-CAP-01: Canonical Finance Baseline reference and resolution

Status: contract proposed with erp/v1 OpenAPI 1.3.0. Nothing is deployed or activated by it.

## Why

ERP provisions a legal entity only against a Finance-approved accounting baseline (ADR-ERP-008; ADR-ERP-019 sections 36-38: "before financial activation, the LegalEntity SHALL have an approved accounting baseline", "Finance SHALL approve materially significant accounting configuration", "a template SHALL NOT be blindly applied"). The ERP provisioning request has always carried `functional_currencies` as *intent*, and ERP refuses it unless it equals its baselines. The Control Plane's provisioning worker (baobab-cp#267) therefore cannot build a request that ERP will accept: neither the approved plan nor the desired state carries a currency, and a market's registry currency is a market fact, not an entity's functional currency. The worker stops, fail closed, with `ErrFinanceBaselineUnavailable`.

The answer is not to let the Control Plane guess, and not to let it copy a value and then behave as if it owned it. It is a **reference**: Control Plane names the exact approved baseline version a provisioning relies on, ERP re-resolves it from its own authority, and a later audit can say which baseline caused which provisioning.

## Authority

| Value | Authority | Where a caller gets it |
|---|---|---|
| Intended markets and countries | Control Plane (approved plan / frozen desired state) | the plan |
| Market registry currency | Market registry | not used for provisioning |
| Legal entity functional currency and the rest of the accounting configuration | **Finance, held by ERP** | `FinanceBaselineResolution` (only `functional_currency`) |
| ERP chart of accounts, schema, tax, costing | ERP | never leaves ERP |
| Pricing and transaction currency | Trade or the pricing authority | not this contract |
| FX rates | a market-data authority | not inferred from a market or ERP |

The contract defines how engines **refer** to a baseline. It does not define the baseline: its accounting content is ERP's representation and is deliberately absent from Shared (a validator pins that no accounting field or approver identity appears in it).

## The reference

`contracts/erp/v1/finance-baseline.schema.json`.

```text
FinanceBaselineReference
  baseline_id      fb_...   ERP-minted lineage id, stable across versions
  legal_entity_id           the Control Plane legal entity
  version          >= 1     the approved version; immutable once approved
  digest           sha256   names immutable approved content
  effective_from   date
  authority        { engine_id: baobab-erp, system_of_record: FINANCE_BASELINE }
```

* **Version and digest together.** A baseline version is approved content and never changes; a change is a new version. The digest is the SHA-256 of the canonical (RFC 8785) JSON of that approved version as ERP stores it, including the facts of its approval. Provisioning consumes "this approved immutable baseline", never "whatever finance configuration ERP has now". What is hashed is ERP's representation and not part of the contract; only its stability is.
* **Authority is part of the reference.** A reference to a baseline not owned by `baobab-erp` as `FINANCE_BASELINE` is refused.
* **No accounting values.** The reference carries none. The resolution a caller reads back adds only `status`, `functional_currency` and `resolved_at`.

## Resolution

Two read-only operations, both requiring `erp:provision` (the provisioner's one ERP scope; no scope is added or granted) and a `TENANT_PROVISIONING` context, because they serve provisioning of a tenant that is not yet ACTIVE:

* `getEffectiveFinanceBaseline` (`GET /legal-entities/{legal_entity_id}/effective-finance-baseline`): the version in force on a date. ERP never creates, approves or infers one; none in force is 404 and the Control Plane must not provision that entity.
* `getFinanceBaseline` (`GET /finance-baselines/{baseline_id}?version=&digest=`): resolves exactly the version and digest named, never "the latest". Unknown, or outside the context's tenant: 404 (indistinguishable). Known baseline but another version or digest: `409 FINANCE_BASELINE_MISMATCH`. A match is returned with its current status, so a caller and an auditor can see that a version was `SUPERSEDED` or `WITHDRAWN`.

`POST /provisioning-operations` now **requires** `finance_baselines`: exactly one reference per legal entity. ERP re-resolves each one before it provisions anything and fails closed:

| Condition | Answer |
|---|---|
| unknown baseline; another version or digest; another legal entity; a legal entity of another tenant; a baseline ERP does not own; functional currency incompatible with the requested markets | `409 FINANCE_BASELINE_MISMATCH` |
| the exact version is withdrawn, superseded or not yet effective | `409 FINANCE_BASELINE_NOT_USABLE` |
| `functional_currencies` is not exactly the set of the referenced baselines' currencies | `409 PLAN_AUTHORITY_MISMATCH` |
| Finance baseline store unavailable | `503` (retryable with the same `Idempotency-Key`) |

None of the 409s is retried with the same request. Nothing is provisioned on any refusal.

### Compatibility

Requiring `finance_baselines` strengthens `erp/v1` rather than starting `v2`, on the same footing as 1.0.2 (`control_plane_authority`) and 1.1.0 (`context_id`): `POST /provisioning-operations` has no conforming caller that completes (the only caller, the Control Plane's provisioner, is unwired from any credential and stops at the missing baseline), so no valid payload exists to break. Consumers pinned earlier are unaffected until they re-pin.

## What a later increment decides, not this one

* **Freezing the reference in the plan.** The worker discovers the reference at submission time. Freezing `baseline_id/version/digest` in the Control Plane desired state or approved plan would let the approval cover the finance baseline too. That changes the plan's digest semantics (ADR-BCP-021), so it is a Control Plane decision of its own and is not made here.
* **Audit.** The Control Plane persists the exact resolved reference with each ERP submission (FB-03), so "which finance baseline caused this provisioning?" is answerable from the ledger.

## Sequence

1. **FB-01 (this change)**: the Shared contract.
2. **FB-02**: ERP serves both reads and enforces the table above; its baseline gains `baseline_id` and a stable digest.
3. **FB-03**: Control Plane replaces `ErrFinanceBaselineUnavailable` with resolution of the reference and persists it in the submission ledger.
4. **FB-04**: the `provisioning.changed` consumer triggers reconciliation; the event is a trigger to inspect authoritative state, not the state.
5. **FB-05**: end-to-end evidence runs in a dedicated evidence environment in which the provisioner is deliberately ACTIVE under bounded credentials. `PROVISIONED` workloads are **not** given runtime behaviour to obtain evidence (owner ruling 2026-10-07): approved, onboarded, provisioned, ready and active stay distinct.
6. **FB-06**: IAM proof (federated identity, audience, subject, scope and context binding, revocation and rotation), captured as deployment evidence.

## Rollout

ERP rejects unknown members, so ERP must re-pin and serve the reads (FB-02) before the Control Plane sends `finance_baselines` (FB-03). Nothing is activated by this contract: `baobab-cp-provisioning-workload` stays PROVISIONED and the validator pin that says so is unchanged.

## Negative tests the contract requires of consumers

1. A reference with another engine as authority is refused.
2. A request with a reference for a legal entity not in `legal_entity_ids`, or missing one that is, is refused.
3. A matching `baseline_id` and `version` with a different `digest` is `FINANCE_BASELINE_MISMATCH`, not a fallback to the current version.
4. A withdrawn or superseded exact version is `FINANCE_BASELINE_NOT_USABLE`.
5. `functional_currencies` that disagree with the baselines is `PLAN_AUTHORITY_MISMATCH` even when every reference is valid.
6. A `RUNTIME` context on either read is `ERP_CONTEXT_REJECTED`.
7. A legal entity of another tenant is indistinguishable from an unknown one.
