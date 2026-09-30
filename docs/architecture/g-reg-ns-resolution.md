# G-REG-NS — Regulations Namespace: Decision

**Status:** **Decided — Option B** (platform architecture owner, 2026-09-30)
**Supersedes:** the "resolved, no Regulations engine" record merged in shared#150, and the open-decision record in shared#151
**Related:** `g-reg-ns-regulations-namespace-proposal.md`, ADR-SHARED-007, ADR-SHARED-008, ADR-SHARED-017 §43, ADR-0018, ADR-0021, `baobab-regulations` ADR-REG-0001 to ADR-REG-0030 (all still *Proposed*)

## Decision

`baobab-regulations` becomes a first-class, headless Baobab capability
provider. It is responsible for regulatory meaning, applicability, regulatory
evaluation and evidence-backed regulatory decisions. Trade remains
authoritative for trade execution and operational enforcement.

The existing `tax.*` and `customs.*` capability domains are **retained** for
operational tax and customs functions. A separate `regulations.*` namespace is
introduced for genuinely cross-domain regulatory capabilities. It goes through
the normal ADR-SHARED-007 review and the ADR-SHARED-017 census and contract
process. No key is accepted from examples.

Trade's ADR-0021 already anticipates this: specialised providers own
regulatory determinations where appropriate.

## Authority boundary

| Concern | Authority |
|---|---|
| Regulatory sources | Regulations |
| Source provenance and legal basis | Regulations |
| Regulatory interpretation | Regulations |
| Applicability evaluation | Regulations |
| Obligations, permissions, prohibitions | Regulations |
| Regulatory assessment and decision | Regulations |
| Regulatory change impact | Regulations |
| Jurisdiction and regime semantics | Regulations |
| Trade transaction | Trade |
| Shipment and commercial workflow | Trade |
| Customs execution workflow | Trade |
| Transaction tax commitment | Trade (ADR-0018) |
| Financial and statutory accounting | ERP |
| Capability and provider resolution | Control Plane |
| Authentication | IAM |
| Operational enforcement | The owning domain engine |

Regulations determines regulatory **meaning**. It does not own other engines'
business processes and is not a middleware layer through which they route.
For example:

- **Regulations:** "A phytosanitary certificate is required under these effective rules for this context."
- **Trade:** "The shipment cannot proceed until that requirement is satisfied."
- **ERP:** "The resulting duty, tax or accounting consequence is posted in this manner."

## Sequence

The decision is recorded; the following steps are still to be done, in order.

1. **Review and reconcile ADR-REG-0001 to ADR-REG-0030** against current
   Baobab architecture (ADR-SHARED-016/017, the CP governance model, IAM
   provider neutrality). Accept each ADR individually where it is still
   correct, and amend it where later decisions changed its assumptions.
   **Do not mass-accept the family.**
2. **Amend ADR-0018 and ADR-0021** in `baobab-trade` wherever their authority
   wording conflicts with the boundary above.
3. **Register the `regulations` domain** in `namespace-registry.yaml` and the
   `capabilityDomain` enum, after the ADR-SHARED-007 review.
4. **Run the Regulations capability census** (EA-02A method).
5. **Land canonical contracts** for accepted candidates (EA-02C method).
6. **Add Regulations' provider declaration** (`.baobab/capability-provider.yaml`).

Until step 3, Regulations may list `proposed_key: regulations.*` candidates in
a planned-only declaration. That is allowed because an unregistered domain is
permitted in a proposal. It declares no support.

## What this is not

- It does not move `tax.*` or `customs.*` into `regulations.*`.
- It does not accept any ADR-REG record by itself.
- It does not register a namespace or catalogue any key yet.
