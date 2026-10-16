# SH-NAB-FIN-02 — Finance F1 contract semantics

**Lifecycle:** DRAFT / EXPERIMENTAL. Canonical vocabulary only once indexed in the Shared catalogue. This file is not ERP implementation certification.

## Authority and isolation

1. Resolve an authenticated Principal, PRIMARY Organisation, Tenant, market, effective-dated legal actor, mandate, entitlement, capability major and active EngineInstance through CP before invoking ERP. Never accept caller-supplied tenant or legal-entity identity, and never derive authority from a corporate parent relationship.
2. ERP's approved FinanceBaseline binds accounting policy, currency and company/organisation placement. Native AD_Client/AD_Org is ERP-private. Reject absent, stale, withdrawn, or wrong-entity baseline and native posting authority.
3. Financial queries are restricted. Each request explicitly names period_start, period_end (inclusive), as_of timestamp, and currency. Reject reversed periods, future/inconsistent as_of, unapproved currency, and cross-legal-entity aggregation. Amounts are decimal strings.
4. Ledger query variants are chart_of_accounts, balances, entries. POSTED is the default *operational policy*, not inferred by schema; DRAFT requires additional privilege. Pagination must preserve an immutable snapshot to avoid duplicating journal rows.
5. Statements carry statement_type, observed_at, data_version and completeness. Treat partial, stale or withheld as non-final, and refuse certified statement rendering. Trial balance must reconcile to the same posted ledger snapshot; other statements require ERP-approved reporting policy.
6. Journal CREATE_DRAFT requires lines with exactly one strictly positive debit or credit per line, zero on the opposite side, balanced sums at currency precision and an open period. SUBMIT/APPROVE/POST/REVERSE require journal_ref, expected_version, exact current authorisation and idempotency_key. Maker and checker must be different canonical Principals; no self-approval. Posted journals are immutable: correction by separately authorised reversal. No POST occurs directly as a side effect of CREATE_DRAFT.
7. All mutating actions are atomic, idempotent (including payload-digest conflict detection), optimistic-concurrency guarded and fail closed on CP/ERP or policy uncertainty. Return RFC 9457 problems without leaking restricted financial data.
8. No finance operation creates, captures, settles, refunds or disburses money. Payment and settlement authorisation remains in owning engines, and Trade order accounting remains finance.order-consequence.process.

## Review and qualification

This increment registers three DRAFT catalogue entries and v1 request/response schemas: finance.ledger.read, finance.journal.manage and finance.statement.read. ERP provider declarations, HTTP handlers, migrations, JVM evidence, L4, protected staging, CP registration/binding and activation are separate deliverables. ADR-SHARED-033 remains Proposed until authorised Shared and ERP reviewer decision. No estate may consume a non-certified provider.
