# EA-R03 Trade-A TA-05 — independent source closure

Date: 17 October 2026. Governing authority: Accepted ADR-SHARED-039
§§2/4/6/7 and EA v2.2 EA-R03 / LA-05 / P0-04B.

## Evidence and disposition

Trade [#153](https://github.com/baobab-platform/baobab-trade/pull/153)
implements the central order-authority enforcement point and append-only
receipt store. Final reviewed head:
`e4ac79b3bb75ba31dcdddd8d5d24bcf4ec15088f`.
Merge: `5435e7bf3e5a056920fe5d95426abfb48b3b093e` (MERGED).
All 32 final-head check runs completed: 24 success and 8 applicable skips;
no failures or unresolved review threads remained before merge. Native
Medusa/PostgreSQL17 migration and regression job `117325627123` passed,
including the class/type matrix and existing checkout COMMIT fence.

Contract pin: Shared `2f5a330fd09f1e62608ae7728897e35c053bf738`, unchanged.
Migration: Trade `Migration20261016140000` (new in this PR).
Local checks: formatting, lint, typecheck, build/postbuild, 600 unit tests
(including 18 PEP tests) and 99 exact-pinned Shared conformance tests pass.
CI run: [39008448291](https://github.com/baobab-platform/baobab-trade/actions/runs/39008448291).

## Engineering corrections

A valid CP decision now fails closed if durable receipt persistence rejects.
The PEP awaits the insert inside its error boundary and returns a safe 503
UNAVAILABLE authority denial; it exposes no SQL/connection details, preserves
no original error cause and performs no automatic retry of the old decision.

The database independently binds commit to cart, create to order and
finalize to draft_order attribution, in addition to existing binding/version,
digest/currency/context/scope checks. The real Medusa/PostgreSQL17 regression
covers three matching positives and all six wrong pairs through both the
store and direct SQL. Fresh IDs/references/leases and SQLSTATE P0001 prevent
uniqueness or expiry from masquerading as class/type enforcement. Rejected
raw SQL must leave no receipt row. Both original review findings are fixed.

## Authority, rollback and remaining work

This increment consumes no Infrastructure #35 output, protected credential
or L4 acceptance. CP authority ports in its native regression are explicitly
synthetic. Engine-local real Medusa/PostgreSQL evidence is not L4, EA Gate D,
protected staging, legal acceptance or operational certification. No workload,
mandate, grant, binding or production capability is activated.

TA-06 entry-point wiring, TA-07 native COMMIT consumption/bypass closure and
TA-08 acceptance remain. Trade-B/C/D, Subscriptions/Trade Docs native execution,
ERP remaining classes and Payments protected-provider work stay separate.
LA-05 and EA-R03 remain PARTIAL; Gate B/D/E and production are not promoted.

Rollback/containment: retain protected operation denial and withhold later
activation. The new migration is corrected before merge; a persistent user
of an unreleased candidate needs a reviewed forward repair. Never erase
receipt history or run an implicit down migration.

Approver: standing user authorisation to own related PRs, repair reviews and
merge after mandatory checks. Engineering/automated review is source review;
no independent business, Finance, legal or production sign-off is asserted.
