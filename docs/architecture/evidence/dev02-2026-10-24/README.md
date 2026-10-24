# DEV-02 — verified fixture and lifecycle evidence

Observed 24 October 2026. Scope: actual CP-owned disposable PostgreSQL fixtures,
24 non-authorising legal-actor scope/lifecycle observations, real component
context APIs, and reusable development lifecycle recovery/teardown.

- CP engineering: https://github.com/baobab-platform/baobab-cp/pull/434
- CP merged source: `a21f48a80cd5b2387c85aea7f6d97ff3811f2dbb`
- Reviewed and runtime-pinned CP head: `6ed4c63f4e28b3370c4f83c097f22d2308f4d474`
- CP actual CI merge SHA: `7b932eac9712078fb6a1ef285c622b566df5da00`
- Lifecycle adoption: https://github.com/baobab-platform/infrastructure/pull/54
- Merged Infrastructure source: `631e59dc0787f81bec0fed3516a97572e825d949`
- Reviewed Infrastructure head: `bd181655bf8b2c64420beeeab72129f9811df3bc`
- Actual executed CI harness merge SHA: `8d0d435d4ef8228a08cd5c8fa62066fa4cc926df`
- Native run: https://github.com/baobab-platform/infrastructure/actions/runs/40058049472
- Artifact: https://github.com/baobab-platform/infrastructure/actions/runs/40058049472/artifacts/12546228663
- Downloaded archive SHA256: `708f9e4213c4d5e2070c86b3b7535dccb7081bd4587e0244beb482ff8c4a7981`

The archive digest was verified against GitHub's artifact metadata after
download. Both original per-run receipt hashes were also verified. JSON suite
and receipt bytes are retained unchanged; the fixture-suite sidecar hash was
computed locally from those unchanged downloaded bytes. The interrupted run
truthfully records lifecycle failure, and both runs record verified teardown.
Per-run receipts retain exact source, lock and runtime image identities. No
private credentials, subjects, bearer tokens, DSNs or run-state directories
are included.

`cp-ci-observation.json` is a locally recorded observation of GitHub check
metadata, not a CP-issued runtime receipt. It records all final-head successful
checks and applicable skips. CP's native PostgreSQL/race suite also tested
transaction rollback, identity projections, immutable fixture history, expiry,
canonical resolver separation, actual routed context API success/denials and
absence of protected bootstrap/default-off assessment routes. Its token verifier
is explicitly synthetic; these are component tests, not signed issuer proof.

The runtime CP pin is the reviewed source head contained in the CP merge, so it
identifies the exact code tested without guessing a future merge object. The CI
harness merge SHA identifies the actual execution, independently of the source
merge record in the implementation register. Prior DEV-01 evidence is retained
in its original dated directory; this run's evidence is separately scoped.

Scope-valid synthetic mandates still return ACTOR_NOT_VERIFIED. Missing,
wrong-market, pending and wrong-scope cases return NO_APPLICABLE_MANDATE;
stale/revoked cases return REVOKED_OR_EXPIRED. Official actor verification,
provider permissions, INT-03C, NAB-03, protected acceptance and production
authorisation remain false. These receipts do not establish complete canonical
L4-CP-03/04 or DEV-03 authority-chain acceptance.

The separate mandatory INT-02 regression failed its first MFA attempt and passed
a targeted rerun at the unchanged reviewed head. Both job references are retained
in `int02-regression-attempts.json`. All 29 applicable Infrastructure checks
succeeded before merge; 6 checks were applicable skips. The cause of the initial
MFA failure remains unestablished and BA-AUD-001 remains OPEN. This change does
not treat a retry as a root-cause fix or as DEV-03 qualification.
