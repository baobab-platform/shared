# G-REG-NS Resolution — Regulations Namespace Decision

**Date:** 2026-09-30
**Related:** G-REG-NS proposal, ADR-0018, ADR-0021, ADR-SHARED-008
**Governance:** Architecture review completed per ADR-SHARED-007

## Decision

The `regulations` domain is **not registered as a canonical capability domain.**

**Rationale:**
- ADR-0018 establishes Trade as canonical authority for tax registrations and multi-jurisdiction tax context
- ADR-0021 establishes Trade as canonical authority for customs, trade compliance and regulatory determinations
- ADR-SHARED-008 §2 registered `tax` and `customs` domains under Trade authority
- These authorities are normative and sufficient; no separate Regulations engine is needed

**Scope stays with Trade:**
- `tax.*` capabilities (tax registration, calculation, reconciliation)
- `customs.*` capabilities (duty determination, import/export eligibility, compliance)
- Regulatory evidence and audit trails (owned by Trade's compliance workflow)

## Consequences

1. **No new `regulations` domain registration** — capabilities remain under `tax` and `customs` domains
2. **Regulations engine defers** — not added to capability census or provider declarations
3. **Tax-registrations candidate** (from EA-02B) — catalogued under Trade's `tax` domain when contract lands
4. **Trade-CMS boundary** (regulatory content, evidence templates) — remains Trade → CMS reference, no Regulations intermediary

## Next Steps

- Update EA-02 implementation record: tax-registrations candidate catalogued as Trade-owned
- Proceed with remaining contract work (buyer-org, identity, content, intelligence)
- Regulations engine census deferred indefinitely unless ADR-0018/0021 are superseded
