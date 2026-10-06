# G-REG-NS — Regulations Namespace Architecture Review

**Decision:** APPROVED / RESOLVED by ADR-SHARED-024 (RTD-08), 2026-10-06  
**Result:** Canonical `regulations` capability domain registered; `tax` and `customs` namespaces remain unchanged  
**Remaining Gate:** Regulations engine capability census and catalogue promotion remain separate work

---

## Original Proposal — Historical Context

The original review proposed registering a `regulations` domain broadly enough
to cover several cross-border regulatory concerns, including some tax and
Customs-adjacent capabilities.

That broad scope is **not** the final RTD-08 decision. ADR-SHARED-024 resolves
the namespace more narrowly around regulatory context, applicability,
obligations/requirements, evidence sufficiency, regulatory assessment and
RegulatoryDecision-related capabilities. Existing `tax` and `customs`
namespaces remain unchanged.

### Background

- **Current:** `tax` domain is registered under baobab-trade authority (ADR-0018, ADR-SHARED-008). Tax registration and calculation are Trade-owned with ERP projection of outcomes.
- **Issue:** Tax is one aspect of cross-border regulatory compliance. Customs, anti-fraud, sanctions and other regulatory concerns are separate lifecycles with different stakeholders (regulatory bodies, authorities, audit operators).
- **ADR-REG family:** Proposed ADRs for Regulations engine (baobab-regulations) design are under review. They define the boundary, authority and lifecycle model for regulatory domain capabilities.

### Proposed Namespace

| Domain | Description | Authority | Governed Capabilities |
|--------|-------------|-----------|----------------------|
| `tax` | Tax registration, calculation, reconciliation, filings | baobab-trade (current) | tax registration, tax calculation, tax filing, tax audit trail |
| `regulations` | Original candidate scope before RTD-08 resolution | baobab-regulations | Historical candidate included Customs/tax-adjacent concerns; final scope is narrowed by ADR-SHARED-024 |

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

### Original Next Steps (superseded by ADR-SHARED-024)

1. Update `namespace-registry.yaml` with `regulations` domain entry.
2. Update `capabilityDomain` enum in capability schema.
3. Run catalogue validator to confirm consistency.
4. Proceed to Regulations engine census (EA-02A equivalent for baobab-regulations).
5. Revisit deferred tax-registration candidate once Regulations capabilities are catalogued.

---

**Stakeholders:** Architecture Review Board, baobab-trade, baobab-regulations, baobab-cp (for capability binding impact)

**Timeline:** Resolved on 2026-10-06 by ADR-SHARED-024; remaining capability census/catalogue work continues separately


---

## Resolution — ADR-SHARED-024 / RTD-08

The architecture review is resolved as follows.

### 1. Canonical domain

```text
regulations
```

is approved as a canonical Shared capability domain.

Its semantic scope is:

```text
regulatory context
applicability
obligations / requirements
evidence sufficiency
regulatory assessment
RegulatoryDecision-related capabilities
```

### 2. Tax namespace

The existing:

```text
tax
```

domain is **not migrated by this decision**.

RTD-08 does not redefine existing tax registration/calculation/reconciliation
contracts. Regulations may determine regulatory tax meaning under its own
domain boundary, but migration or decomposition of established `tax.*`
capabilities requires a separate architecture decision.

### 3. Customs namespace

The existing:

```text
customs
```

domain is **not migrated by this decision**.

RTD-08 does not decide ownership of Customs declaration, submission, clearance
or authority-response workflow capabilities. The Regulations/Trade Docs
decomposition established by ADR-SHARED-019 remains authoritative.

### 4. Namespace registration is not capability promotion

Registering `regulations` permits canonical capability keys such as:

```text
regulations.context.resolve
regulations.decision.evaluate
regulations.change.subscribe
```

to be considered by the normal capability-governance process.

It does not make those keys catalogued, ACTIVE, supported or bound.

The baobab-regulations provider declaration may continue to use
`proposed_key` until Shared catalogue contracts and implementation evidence
justify promotion.

### 5. Event-context consequence

Because the namespace gate is now resolved, ADR-SHARED-024 also activates the
Shared `regulations` event context with `baobab-regulations` as steward and
producer for the two RTD-06 documentary-assessment facts.

