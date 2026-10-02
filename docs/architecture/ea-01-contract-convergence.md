# EA-01 — Canonical Contract Convergence: Implementation Record

**Governing plan:** EA Implementation Plan v2.0 §6 (EA-01) and §29 (Phase 1)
**Status:** EA-01A, EA-01C and EA-01D implemented. Every engine lock is canonical (Gate 2). The check is enforced for engine repositories (Gate 3). Engine re-pins, the rest of EA-01B, and EA-01E are open.

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
| 2 | Migrate every engine lock to the canonical shape (see below) | CP, IAM, CMS, Pulse, Trade done (Trade re-pinned to `b063f8a` after semantic compatibility, trade#114); ERP open |
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

## Open (as of 2026-10-02)

- **ERP semantic convergence (the principal blocker):** ERP stays held at `2da1a42`. Its Mapping persistence, HTTP surface, event envelope and error model differ from the Shared contracts it consumes. Sequence: semantic census, implementation reconciliation, an exact-pin compatibility suite, re-pin (the Trade pattern, trade#114). Not started.
- **IAM pin vs issued scopes:** IAM issues `administrator:read`, `administrator:write` and `administrator:approve` (iam#50, iam#51) while its lock pins `1bb1c94`, whose scope registry has none of them. Re-pin IAM and add a check that every Baobab-defined scope IAM issues exists in the exact pinned registry.
- **Identity assurance contracts:** provider-neutral `AuthenticationAssurance` and `AssuranceRequirement` no longer force `amr` (ACR-or-AMR, no Keycloak SPI).

- **EA-01B:** remove operational `nabhold/*` references from the Trade, ERP
  and Pulse configuration.
- **EA-01E:** automated update PRs from Shared, once compatibility is proven.
  Never auto-merged.
