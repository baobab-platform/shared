# G-REG-NS — Regulations Namespace Architecture Review

**Decision Required:** ADR-SHARED-007 architecture review for a canonical `regulations` namespace

**Gate:** Precedes Regulations engine survey and catalogue entries for tax/regulatory capabilities

---

## Proposal

Register a `regulations` domain in `namespace-registry.yaml` and `capabilityDomain` enum to govern cross-border regulatory capabilities: tax registration, tax calculation, import/duty registration, compliance declarations and audit evidence.

### Background

- **Current:** `tax` domain is registered under baobab-trade authority (ADR-0018, ADR-SHARED-008). Tax registration and calculation are Trade-owned with ERP projection of outcomes.
- **Issue:** Tax is one aspect of cross-border regulatory compliance. Customs, anti-fraud, sanctions and other regulatory concerns are separate lifecycles with different stakeholders (regulatory bodies, authorities, audit operators).
- **ADR-REG family:** Proposed ADRs for Regulations engine (baobab-regulations) design are under review. They define the boundary, authority and lifecycle model for regulatory domain capabilities.

### Proposed Namespace

| Domain | Description | Authority | Governed Capabilities |
|--------|-------------|-----------|----------------------|
| `tax` | Tax registration, calculation, reconciliation, filings | baobab-trade (current) | tax registration, tax calculation, tax filing, tax audit trail |
| `regulations` | Cross-border regulatory compliance (customs, import duty, sanctions, anti-fraud, audit evidence) | baobab-regulations (proposed) | customs declaration, duty calculation, sanctions screening, compliance proof-of-delivery, audit evidence collection |

### Decision Points

1. **Should regulations be a canonical domain?** Yes/No. If No, tax and regulatory concerns remain with baobab-trade; if Yes, proceed to point 2.

2. **If Yes: What is the scope of regulations?** Does it cover:
   - Customs and import-duty only?
   - All cross-border regulatory (customs + sanctions + anti-fraud + audit)?
   - Or multi-jurisdiction tax + regulatory?

3. **Authority split:** Does `tax` stay with baobab-trade or move to baobab-regulations?
   - Keep separate: `tax.*` stays under Trade, `regulations.*` under Regulations.
   - Consolidate: Move `tax.*` under Regulations, update Trade references.

4. **Regulations engine survey:** Once the namespace is decided, survey baobab-regulations for:
   - Implemented regulatory domain capabilities
   - Candidate capabilities (ADR-REG alignment check)
   - Declaration readiness (provider-neutral contract, provider declaration schema match)

### Dependency on Regulations ADRs

This review assumes ADR-REG family ADRs exist and are accepted. If they are still proposed, this G-REG-NS review may be deferred until their acceptance, or run in parallel with expectation of ADR acceptance as a gate.

### Impact on EA-02B Candidates

The candidate review deferred `tax-registrations` (Trade, ADR-0018) pending G-REG-NS:

| Candidate | Current Status | Post-G-REG-NS Path |
|-----------|---|---|
| Tax registrations | Deferred | If `tax` stays Trade-owned: domain exists, evaluate for capability candidacy. If `tax` moves to Regulations: surveyed in Regulations engine census |

### Next Steps (if approved)

1. Update `namespace-registry.yaml` with `regulations` domain entry.
2. Update `capabilityDomain` enum in capability schema.
3. Run catalogue validator to confirm consistency.
4. Proceed to Regulations engine census (EA-02A equivalent for baobab-regulations).
5. Revisit deferred tax-registration candidate once Regulations capabilities are catalogued.

---

**Stakeholders:** Architecture Review Board, baobab-trade, baobab-regulations, baobab-cp (for capability binding impact)

**Timeline:** Parallel with ADR-REG family acceptance or serial gate thereafter
