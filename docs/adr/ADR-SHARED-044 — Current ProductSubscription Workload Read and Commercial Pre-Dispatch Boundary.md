# ADR-SHARED-044 — Current ProductSubscription Workload Read and Commercial Pre-Dispatch Boundary

| Field | Decision |
|---|---|
| Status | Accepted |
| Date | 2026-10-25 |
| Owners | Shared / Control Plane / Subscriptions |
| Extends | ADR-SHARED-011, ADR-BCP-017/018, ADR-SUB-0003/0005/0011/0015/0016 |

## Decision

Control Plane publishes an authenticated current ProductSubscription **workload read** and a distinct commercial pre-dispatch **decision**, defined in `contracts/product/v1/current-authority.schema.json`. Human classification APIs are not reused as workload authorization. Both are tenant-bound and operation/revision aware, require current IAM verification plus active registered workload scopes, and return no-store responses with short expiry.

- **Read authority:** CP is authoritative for subscription identity, owning tenant, status, revision, classification, classification provenance and current primary Organisation association. The result is a snapshot, never a command and never evidence of a payer, legal-actor mandate, pricing or Kill Bill consent.
- **Financial boundary:** CP cannot declare an `AUTHORISED` Kill Bill dispatch without independently verified current payer, account, term/catalogue version, legal actor authority, explicit billing policy, separation of duties and accepted financial contract. **v1 deliberately only returns DENIED**, explaining why. A future positive decision needs a new reviewed contract and end-to-end runtime qualification, not a configuration toggle.
- **Concurrency:** a caller-supplied authoritative revision must match a consistent CP snapshot. Never infer a monotonic revision from event timestamps. A stale revision fails closed even if the provider operation was prepared earlier.
- **Scope and identity:** two new workload-only scopes, `subscription:current-workload-read` and `subscription:commercial-authority`, audience `baobab-control-plane`; exact allowlisted baobab-subscriptions client and active current workload registry required. OIDC token membership is invocation permission only.
- **Isolation:** CP reads the tenant and subscription in a single bounded query; a mismatched or undisclosed tenant returns a generic 404, not other tenant metadata.
- **No authority transfer:** Subscriptions stores provider operation custody and may observe native state only after a current CP read; it cannot mint CP classification, payer identity, versioned prices, or a legal mandate from provider metadata.
- **Operational failure:** CP outage, expired token, missing classification, inactive subscription, missing primary Organisation, missing finance terms or unknown authorization state forbids dispatch. No retry of ambiguous monetary POST.

## Implementation and staging gate

Add read/decision routes under `/internal/subscriptions/v1` in CP. Read comes from CP's live product subscription + immutable classification record with a revision fence. Subscriptions must validate issuer/audience/scope, exact subscription and revision, response freshness and fail closed. Guard with an explicit opt-in, nonproduction deployment variable; no automatic production exposure. Verify negative cases (wrong audience, wrong client, cross-tenant, stale revision, unclassified, revoked identity, no current primary Organisation, CP outage) in connected runtime before qualification.

**Commercial dispatch remains disabled** until a separately accepted v2 positive authorization contract and payer/terms integrations exist.
