# ADR-SHARED-033 — canonical registration and provider-declaration audit

**Audit date:** 10 November 2026. **Decision:** Accepted corporate finance capability census. **Audit scope:** Shared canonical source; ERP declaration independently inspected. **Qualification:** not granted.

## Tranche inventory

| Tranche | Key | Canonical Shared status | ERP provider status |
| --- | --- | --- | --- |
| F1 | `finance.ledger.read` | DRAFT / EXPERIMENTAL | Not declared |
| F1 | `finance.journal.manage` | DRAFT / EXPERIMENTAL | Not declared |
| F1 | `finance.statement.read` | DRAFT / EXPERIMENTAL | Not declared |
| F2 | `finance.payable.manage` | DRAFT / EXPERIMENTAL (F2/F3 canonical admission PR) | ERP planned-only |
| F2 | `finance.receivable.manage` | DRAFT / EXPERIMENTAL (F2/F3 canonical admission PR) | ERP planned-only |
| F2 | `finance.bank-reconciliation.manage` | DRAFT / EXPERIMENTAL (F2/F3 canonical admission PR) | ERP planned-only |
| F2 | `finance.cash-position.read` | DRAFT / EXPERIMENTAL (F2/F3 canonical admission PR) | ERP planned-only |
| F2 | `finance.expense.manage` | DRAFT / EXPERIMENTAL (F2/F3 canonical admission PR) | ERP planned-only |
| F2 | `finance.budget.manage` | DRAFT / EXPERIMENTAL (F2/F3 canonical admission PR) | ERP planned-only |
| F3 | `finance.reporting-export.create` | DRAFT / EXPERIMENTAL (F2/F3 canonical admission PR) | ERP planned-only |
| F3 | `finance.project-cost.read` | DRAFT / EXPERIMENTAL (F2/F3 canonical admission PR) | ERP planned-only |
| F3 | `finance.consolidation.run` | DRAFT / EXPERIMENTAL (F2/F3 canonical admission PR) | ERP planned-only |

**Separate retained capability:** `finance.order-consequence.process` — catalogued under ERP v1, ERP provider declaration **PARTIAL**. It is not F1/F2/F3 and must not be counted as a new finance-tranche implementation.

## Source and external evidence

1. `contracts/capability/v1/namespace-registry.yaml` registers the one existing `finance` namespace. There is no separate ledger, accounting or treasury domain.
2. `contracts/capability/v1/catalogue.yaml` lists the three F1 keys and the separate order-consequence key. F1 definitions in `contracts/finance/v1/capabilities.yaml` name semantic owner `baobab-erp`, RESTRICTED classification, lifecycle DRAFT and maturity EXPERIMENTAL.
3. The F1 request/response/error schema references, synthetic examples and conformance checks are present. Source conformance **is not** proof of live journal posting, ledger correctness, real finance authority or reconciled statements.
4. `contracts/capability/v1/registration-bundles.yaml` does not bootstrap an ERP finance provider. Independently inspected `baobab-erp/.baobab/capability-provider.yaml` also does not claim F1/F2/F3 support. The unmerged ERP [#153](https://github.com/baobab-platform/baobab-erp/pull/153) adds a guarded native F1 readback increment, not canonical API/binding/certification.
5. `finance-f1-provider-acceptance.yaml` retains **F1-P01…F1-P11 REQUIRED_NOT_EXECUTED**. ERP's existing native veto and connected CI are not substitutes for proof of the F1 command/query lifecycle, current IAM/CP operation-specific permits, Finance-approved books or group accounting policy.
6. F2 receivables must accept Subscriptions-originated typed source documents without inventing a Trade order; funds transfer remains `payment.*`. F3 consolidation requires an accountant-approved ownership, eliminations and FX model; internal-trade remains owner of business intercompany movement.

## Admission and drift policy

ADR-SHARED-033 §11 requires **one governed promotion per key/tranche** with actual canonical request/response/error contracts, negative fixtures, catalogue DRAFT definition and downstream owner evidence. The test `scripts/tests/test_finance_adr033_registration.py` records today's admitted/census-only split; when a future F2/F3 key is legitimately admitted, the same reviewed PR must update the test/this register and run conformance. **Do not** add F2/F3 placeholders to the catalogue, invent a Shared provider, or mark an ERP provider IMPLEMENTED merely to make this census look complete.

Further mandatory work: native F1 operation-specific CP/IAM authority, secure HTTP scope, book mapping and snapshot/pagination; journal lifecycle/SoD/reversal/native COMMIT with replay; numerical trial-balance reconciliation, historical baseline lineage and Finance policy; independent F1-P01–P11 evidence; then separate F2/F3 admission and provider qualification. Staging/production gates unchanged.


## F2/F3 canonical source-admission update — 10 November 2026

All nine accepted finance-census names now have v1 canonical draft definitions, individual request/response schemas, RFC 9457 error references, 18 synthetic fixtures, source-type constraints and denial tests. The historical census-only table above is superseded for source registration by the F2/F3 PR, subject to merge. No ERP provider support, release approval, CP binding/grant, F1-P evidence, Finance policy, actual invoice handoff, payment execution or qualified group consolidation is asserted. CP and ERP consume only an immutable merged Shared contract revision under separate PRs.
