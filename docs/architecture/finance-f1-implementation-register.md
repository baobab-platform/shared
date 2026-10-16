# Finance F1 — independent engineering implementation register

**Programme:** Nabhold Go-Live v2.0 P1-01/P1-02 (G03/G06), EA v2.2.
**Contract authority:** Shared. **Accounting/native authority:** ERP.
**Status:** DRAFT contract source increment; not provider or production acceptance.

## Dependency decision — 16 October 2026

The sponsor authorised engineering that does not depend on Infrastructure #35.
Shared F1 vocabulary/schema/fixture/CI work has no dependency on that harness.
It creates no human, tenant, legal mandate, grant, binding or native posting.
The earlier global sequencing pause does not block this independent lane.

| Step | Implementation/evidence | Remaining exit |
|---|---|---|
| SH-NAB-FIN-01 census | ADR-SHARED-033 remains Proposed | Steward and ERP semantic decision; no status promotion inferred |
| Design checkpoint | Shared #319 merged after corrected journal/view schemas and mandatory CI (`49fc2ded`, merge `27eb77a`) | Historical proposal; never the runtime schema ID |
| SH-NAB-FIN-02 DRAFT wire tranche | Shared #321: three DRAFT/EXPERIMENTAL keys; common types; six request/response schemas; examples; negative tests; lock/CI/index | Final-head mandatory CI/review before source merge |
| ERP F1 provider | No provider declaration or runtime implementation in this increment | Accepted resource-server scope policy, actual routes/persistence/native tests and current CP/native veto |
| Native/operational qualification | `finance-f1-provider-acceptance.yaml` is REQUIRED_NOT_EXECUTED | Real iDempiere, Finance accounting policy, L4/protected evidence and signed acceptance |

## Engineering review record

Consulted Shared ADR-SHARED-017/033, canonical ERP scalar/baseline/idempotency/error
contracts, EA v2.2, Nabhold Go-Live v2.0 and ADR-NAB-0014. ERP review snapshot:
`0bcf6d1b9d0ec262a1400eb9ce83981305e5d32d`, accepted ADR-ERP-008 (exact money,
book currencies, accounting date/posting time, native financial processing,
immutability and SoD), ADR-ERP-018 (trial-balance reconciliation and lineage),
and ERP's current posting-authority implementation plan. This is an engineering
conformance review, not a fabricated steward/Finance approval of ADR-SHARED-033.

The draft now has operation-specific input requirements, explicit positive/zero
journal instructions, typed chart/balance/entry views, opaque ERP-owned book
selection, snapshot-bound continuation, exact signed historical correction facts,
multiple historical baseline versions and statement reconciliation metadata.
Native permission, balance arithmetic and accounting algorithms remain outside
Shared and the estate. No additional IAM scope is allocated.

Schema tests exercise actual Draft 2020-12 validation with all local references
resolved. Required format-validator dependencies are explicit: malformed as-of
and observed-at values must not silently pass because an optional library is
missing. Detailed `$comment` fields explain boundary and historical semantics.

## Next work, without bypassing #35

1. Merge this DRAFT source only after mandatory CI and review closure.
2. ERP owner determines the accepted F1 scope/route and book/baseline protocol,
   journal event contract/producer semantics and native implementation increment.
3. Implement and prove the ERP cases in `finance-f1-provider-acceptance.yaml`; do not invent
   a provider support level from catalogue registration or wire tests.
4. Independently perform CP binding and cross-engine qualification once the
   integration dependencies are satisfied; production remains gated.

Nabhold G03/G06 remains PARTIAL/BLOCKED for operational use. R0/R1/R2/R3 is not
released by this contract change. Source DRAFT vocabulary, accepted architecture,
provider support, L4 qualification and production are separate facts.
