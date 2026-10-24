# DEV-02 — CP fixture qualification

DEV-02 covers CP-owned disposable fixture identity and non-authorising mandate
policy inputs. It implements the closed development/v1 profile under
ADR-SHARED-043 and preserves ADR-BCP-027's legal-actor boundary.

| Profile | Independent Tenant / PRIMARY Organisation | Legal actor model |
| --- | --- | --- |
| Nabhold | Yes | Synthetic holding actor, UNKNOWN / UNVERIFIED |
| ZuriBeans | Yes | Unincorporated; no own or DEFAULT LegalEntity |
| Thamani | Yes | Declared separately incorporated; UNKNOWN / UNVERIFIED |
| Equator Estate | Yes | Unincorporated; no own or DEFAULT LegalEntity |
| External client | Yes; estate optional | Independent UNKNOWN / UNVERIFIED actor |

The two unincorporated Organisations reference CP's generated Nabhold actor only
as a proposed synthetic parent. That reference grants no access to Nabhold,
sibling or external Tenants, and no contracting, tax, payment or provider role.
All canonical IDs are assigned by CP. Profile order cannot select the parent;
partial operating-business profiles require an explicit parent. Bootstrap version
1 runs require recreation rather than an identity rewrite on replay.

CP persists twelve immutable run-bound scenarios in its development schema,
separate from canonical operating legal actor mandates. For each unincorporated
Organisation the read-only checker evaluates these six scenarios plus six scope
boundaries (role, activity, capability, tenant, Organisation and market).

| Scenario | Required result |
| --- | --- |
| Scope-valid synthetic parent | ACTOR_NOT_VERIFIED |
| Missing, wrong-market or pending mandate | NO_APPLICABLE_MANDATE |
| Stale or revoked mandate | REVOKED_OR_EXPIRED |
| Each wrong scope boundary | NO_APPLICABLE_MANDATE |

Scope-valid is a fixture coverage term, not an approved legal mandate. There is
no fictitious VERIFIED legal evidence, synthetic maker/checker legal approval,
canonical ACTIVE mandate or engine binding. Ordinary CP legal resolution never
loads the development scenarios. Denied outcomes expose no responsible actor or
validity grant. The checker refuses expired, old-version or incomplete runs.

The CP PostgreSQL integration test injects a late insert failure and verifies
complete transaction rollback, then checks all identity projections, immutable
scenario history, expiry and ordinary resolver separation. It also exercises the
actual context HTTP handler with real PostgreSQL persistence: own-context success
and sibling/external Tenant, wrong Organisation, wrong market and anonymous
denials. Its authenticated context is explicitly synthetic; signed issuer and
revocation qualification belongs to DEV-03.

Infrastructure invokes the same CP-owned checker in the reusable development
lifecycle and checks the exact 24-case inventory and outcomes. It retains a
sanitized receipt after recovery and verified teardown. An incomplete inventory,
unexpected authority claim or failed case cannot qualify the run. Source pins,
reviewed heads, actual executed harness identity and receipts are recorded in the
[implementation register](ea-dev-implementation-register.md) and dated evidence.

These are scoped fixture and component observations supporting L4-CP-03/04;
they do not assert the complete canonical scenarios, genuine issuer authority
chain, INT-03C, NAB-03, provider acceptance, staging or production readiness.

The dated audit findings BA-AUD-006 and BA-AUD-029 concern adoption of these
specific CP fixtures and receipts into the official register. Reconciliation of
those report gaps does not close BA-AUD-002/030's real authority-chain work or
BA-AUD-033's real legal-source acceptance. The initially failed INT-02 regression
and its targeted rerun are retained separately; an unexplained MFA failure does
not become a verified root-cause repair merely because a later attempt passes.
