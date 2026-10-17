# Baobab Charts — BXS presentation foundation

This package validates **already-authorised display projections** and provides
accessible tabular view models for future charts. It does **not** calculate
financial figures, authorise an executive, cross tenant boundaries, select
providers, infer market status or supply a charting/WebGL runtime.

A server-side Digital Estate or BFF first evaluates IAM identity, CP context,
the domain capability and lawful scope, then redacts its approved view model.
Only that display-safe projection may be passed to this package.

The `available`, `stale`, `unavailable` and `restricted` statuses are
**caller-supplied classifications**, never invented from timestamps in this
package. Missing values remain `null`, not numerical zero. Rendering code
must provide a tabular equivalent and show provenance and the reporting time.

`0.0.0` denotes source under review; no registry publication or approved
consumer adoption is implied. Release only through the Shared Changesets,
foundation, artifact and version-verification gates.

Node 24 / pnpm 11.24.0:

    pnpm --filter @baobab-platform/experience-geo-core build
    pnpm --filter @baobab-platform/experience-charts lint
    pnpm --filter @baobab-platform/experience-charts test
    pnpm --filter @baobab-platform/experience-charts build

See Accepted ADR-SHARED-040 and Nabhold Go-Live Master Plan v2.0 (G12/G15).
