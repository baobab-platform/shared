# EA-01 — Canonical Contract Convergence: Implementation Record

**Governing plan:** EA Implementation Plan v2.0 §6 (EA-01) and §29 (Phase 1)
**Status (2026-10-02):** EA-01A, EA-01C and EA-01D implemented. Every engine lock is canonical and passes the enforced check (Gates 2 and 3). **ERP semantic convergence is closed**: its pin is current and proven by an exact-pin conformance suite (see [ERP closure evidence](#erp-closure-evidence)). Not closed: EA-01B (operational `nabhold/*` references), EA-01E (automated update PRs), and the ERP operational gaps listed under [Open](#open-as-of-2026-10-02), none of which is a contract-pin problem.

## EA-01A — The lock standard

Every consumer's `contracts.lock.yaml` follows
[`.baobab/contract-consumer-lock.schema.json`](../../.baobab/contract-consumer-lock.schema.json):

```yaml
schema: baobab-contract-consumer-lock
version: "1.0"
source:
  repository: baobab-platform/shared
  commit: <full 40-character SHA on Shared main>
contracts:
  - contracts/<domain>/v<N>/<file>
policy:
  updates: explicit_pull_request
  compatibility: validate_before_merge
```

A repository may add its own top-level metadata. The Control Plane's
`contract_bundle` is one example. It may not replace or loosen these keys.
`source.repository` accepts only `baobab-platform/shared`, so a `nabhold/*`
source fails (EA-01B). `source.commit` accepts a full SHA only: a branch, a
tag or an abbreviated SHA is not a pin.

The Payments and Subscriptions locks were already in this shape and are the
reference.

## EA-01C — Foundation lock check

`scripts/contract_lock.py check` runs in the reusable Foundation environment
job against a full-history checkout of Shared `main`:

1. An `active` repository with the `engine` or `control-plane` trait must have a lock.
   Experimental engines and non-engine repositories may omit one. Any lock
   that exists is checked.
2. The lock matches the schema.
3. The pinned commit exists and is reachable from Shared `main`. A commit on
   an unmerged branch is not a pin.
4. Every listed contract exists at the pin, and JSON and YAML files parse.
5. No listed contract has been removed from Shared `main`. A removal is
   incompatible drift by definition.

The remaining links in the EA-01C chain belong to each engine's own CI
because they depend on that engine's code: vendored copies must match the
pin, and implementation fixtures must conform. The Payments, Subscriptions
and Control Plane pinned-contract tests already do this.

## EA-01D — Drift report

`scripts/contract_lock.py drift` writes the Foundation job summary: the pin,
the approved baseline (Shared `main`), how many revisions behind the pin is,
and which consumed contracts are changed or removed since the pin. The
classification:

| Class | Meaning | Consequence |
|---|---|---|
| `CURRENT` | Pin is Shared `main` | None |
| `BEHIND_UNCHANGED` | Behind, but no consumed contract changed | Re-pin at convenience |
| `BEHIND_CHANGED` | A consumed contract changed | Re-pin with the engine's compatibility tests (explicit PR) |
| `INCOMPATIBLE` | A consumed contract was removed | Check finding (fails once enforced) |
| `UNKNOWN` | No lock, a non-canonical lock, or a pin not on `main` | Fix the lock |

The drift report never fails the build: being behind is not a release
failure (plan §6). A text diff cannot decide whether a *changed* schema is
compatible. That verdict comes from the consumer's compatibility tests on the
re-pin PR, not from Foundation.

## Migration gates

| Gate | Action | State |
|---|---|---|
| 1 | Schema, check and drift report in Foundation, `warn` mode | This change |
| 2 | Migrate every engine lock to the canonical shape (see below) | **Done for all eight consumers.** Trade re-pinned to `b063f8a` after semantic compatibility (trade#114); ERP re-pinned to `739f0ca` after semantic compatibility (erp#43–erp#46) |
| 3 | Enforce: `--mode auto` fails engine repositories on any finding and warns for others, so frozen Digital Estates such as zuribeans (legacy lock) are not failed before the EA Unfreeze Gate | This change |

## Engine status at Shared `7b9212f` (2026-09-30, before migration)

| Engine | Lock | Check | Drift |
|---|---|---|---|
| baobab-cp | `schema: nabhold-contract-consumer-lock`, otherwise canonical | 1 finding (schema name) | `BEHIND_UNCHANGED` (2 behind; 104 of 104 unchanged) once renamed |
| baobab-iam | `version: 1` list of `{source, sha}` | Non-canonical | `UNKNOWN` |
| baobab-cms | None | Missing (active engine) | `UNKNOWN` |
| baobab-pulse | Legacy `nabhold/shared` | Non-canonical | `UNKNOWN` |
| baobab-trade | Legacy `nabhold/shared` (plan §3) | Non-canonical | `UNKNOWN` |
| baobab-erp | Legacy `nabhold/shared` (plan §3) | Non-canonical | `UNKNOWN` |
| baobab-subscriptions | Canonical, `ac2f0c2` | Passes | `BEHIND_CHANGED` (160 behind) |
| baobab-payments | Canonical, `f20069d` | Passes | `BEHIND_CHANGED` (166 behind) |

Each engine's migration PR carries only that engine's compatibility fixes.

Migrated since: CP (cp#229, schema name), IAM (iam#47, canonical shape and
five consumed contracts), CMS (cms#19, new lock on `content/v1`) and Pulse
(pulse#28, legacy lock replaced; events moved to `com.baobab-platform.pulse.*`
and fixtures refreshed). All four pass the check.

## Engine status at Shared `739f0ca` (2026-10-02)

Measured with `scripts/contract_lock.py check --mode auto` and `drift` against each engine's `main` lock and Shared
`main`. Every lock passes the enforced check. A pin that is behind is not a failure (plan §6): `BEHIND_CHANGED`
means the next re-pin needs that engine's compatibility tests.

| Engine | Pin | Check | Drift | Notes |
|---|---|---|---|---|
| baobab-erp | `739f0ca` | Passes | `CURRENT` | Semantic convergence proven (below) |
| baobab-cp | `a503649` | Passes | `BEHIND_UNCHANGED` (1 behind) | cp#252 |
| baobab-iam | `a503649` | Passes | `BEHIND_UNCHANGED` (1 behind) | iam#52: lock covers the scopes IAM issues; `check-issued-scopes.sh` asserts every Baobab-defined scope IAM issues exists in the exact pinned registry |
| baobab-cms | `b63ce52` | Passes | `BEHIND_UNCHANGED` (85 behind) | 3 consumed contracts, none changed |
| baobab-trade | `b063f8a` | Passes | `BEHIND_CHANGED` (34 behind) | `control-plane/v1/openapi.yaml`, `identity/v1/workload-registry.yaml` changed since the pin |
| baobab-pulse | `b63ce52` | Passes | `BEHIND_CHANGED` (85 behind) | `control-plane/v1/domain.schema.json` changed |
| baobab-subscriptions | `3a8230e` | Passes | `BEHIND_CHANGED` (66 behind) | `control-plane/v1/domain.schema.json`, `subscriptions/v1/capabilities.json` changed |
| baobab-payments | `3a8230e` | Passes | `BEHIND_CHANGED` (66 behind) | `control-plane/v1/domain.schema.json`, `payments/v1/capabilities.json` changed |

## ERP closure evidence

The EA-01 rule: ERP closes only when the resulting pin is *proven*, not merely newer. The sequence (the Trade
pattern, trade#114) and where each step landed:

| Step | Result | Evidence |
|---|---|---|
| 01 Semantic delta census (`2da1a42` to `739f0ca`) | 19 locked contracts classified: 16 cosmetic (`$id` host or name), 2 breaking (event type namespace `com.nabhold` to `com.baobab-platform`, AsyncAPI names), 1 behavioural (`system-of-record` 1.1: Control Plane is the runtime owner of Legal Entity); 9 contracts added since the pin | erp#43, `docs/migration/erp-compat-01-semantic-delta.md` |
| 02 Identity and mapping | `entity_mapping` brought to `mapping.schema.json`: boundary-minted `map_`/`erp_` ids, five-value status, `canonical_owner`, `tn_` and legal-entity grammars; legacy rows with no legal entity quarantined, never defaulted from the tenant; a Control Plane context seam with no tenant-to-legal-entity lookup (a tenant may hold several legal entities, ADR-BCP-018) | erp#43 (migration 0012) |
| 03 Boundary API | `GET /mappings/{mapping_id}` and `GET /mappings` served per the OpenAPI (tenant from the token claim only, no vendor bindings); the other four operations answer 501 | erp#43 |
| 04 Error semantics | RFC 9457 `application/problem+json` on every route, correlation id echoed, no internal text echoed, negative cases proven | erp#44 |
| 05 Event envelope | CloudEvents 1.0 profile, registry guard (ERP produces only the 8 types Shared registers to `baobab-erp`; consumes only the 2 registered Trade types), `(source, id)` dedup, legacy shape rejected | erp#45 (migration 0013) |
| 06 Exact-pin conformance | `tests/conformance/` (28 tests, CI job `shared-conformance`) validates ERP's mapping and problem documents, events and live HTTP responses against the real Shared schemas at exactly the locked commit; asserts the checkout `HEAD` equals the pin and never skips | erp#46 |
| 07 Re-pin | `2da1a42` to `739f0ca`; lock grows from 19 to 36 contracts so every contract the code depends on is covered by the drift report | erp#46 |

Why the suite is evidence and not decoration: with the old lock it refuses a `739f0ca` checkout; against the old pin
the current code fails 18 tests; at the new pin all 28 pass; mutating the code (dropping a required mapping member,
renaming `correlation_id`, pointing `invoice.changed` at the wrong payload schema) fails exactly the expected tests.
Identifier and envelope grammars are asserted equal to Shared's patterns, and the lock is asserted to name every
contract the code depends on.

Method note: 06 and 07 landed together because the new code cannot conform to the old pin.

## Open (as of 2026-10-02)

Closed since the previous record:

- **ERP semantic convergence** (the principal blocker): closed by erp#43 to erp#46, above.
- **IAM pin vs issued scopes**: closed by iam#52 (pin `a503649` and the scope-in-registry check).
- **Identity assurance contracts**: closed by shared#196 (ACR-or-AMR, no `amr` forced).

Still open. None is a contract-pin defect; each needs its own work or a decision:

- **EA-01B:** remove operational `nabhold/*` references from the Trade, ERP and Pulse configuration. Measured on
  `main`: ERP has 43 non-documentation files that mention `nabhold` (the bulk are the `org.nabhold.baobab.erp.*`
  OSGi bundle names and Java packages, which cannot be renamed casually), Trade 18, Pulse 4. ERP's lock `source` is
  already `baobab-platform/shared`.
- **EA-01E:** automated update PRs from Shared, once compatibility is proven. Never auto-merged.
- **ERP boundary operations not implemented** (answer 501 problem documents, never fabricated): `POST` and
  `GET /provisioning-operations` (needs a Control Plane assignment source, a governed finance baseline and a
  boundary-minted `op_` id), `GET /order-consequences/{commerce_order_id}` (needs a consequence read model),
  `GET /inventory-availability` (needs an iDempiere stock query).
- **ERP delivers no events yet:** its domain recorders still produce legacy-shaped events carrying iDempiere native
  ids, for which Shared registers no equivalent. They are stored as `held`, never delivered. Producing the
  registered `erp.*` events needs an outcome projection (`order_version`, revisions, totals, `erp_` ids).
- **Shared contract gaps found by the conformance suite (closed):** the ERP OpenAPI declared no 400 on `GET /mappings/{mapping_id}`
  and `GET /mappings`, and no 501 for operations whose backing capability is unavailable. OpenAPI 1.0.1 (shared#198, `92accac`)
  declares both; ERP pinned it (erp#47, `a672a64`), deleted `KNOWN_UNDECLARED`, and its exact-pin conformance now fails on any
  undeclared status. A 501 means the capability is absent from the engine release; it is not readiness.
- **Grants outside this repository:** Baobab IAM grants ERP workloads only `erp:integrate`. The Boundary API needs
  `erp:read` and `erp:provision` and a `tenant_id` claim on ERP-bound tokens; the routes fail closed until the owner
  grants them.
- **ERP image boot:** the unused Hazelcast bundle was removed from the iDempiere image to clear CVE-2026-89425
  (ADR-ERP-004 section 5, erp#43); no CI job boots iDempiere, so start-up without it is unverified.
