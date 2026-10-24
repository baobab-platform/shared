# DEV-04 — original seven-case native IAM and CP qualification

The Accepted EA-DEV plan requires the original seven INT-03C cases over actual
services. DEV-03's sixteen assertions and historical #49 evidence cannot be
translated into this gate's PASS. Each destructive proof uses a fresh isolated
run under ADR-SHARED-043. One operator may drive distinct synthetic Principals;
independent people and protected-environment custody remain separate.

The maintained implementation and operational reference is Infrastructure's
[`development/INT03C.md`](https://github.com/baobab-platform/infrastructure/blob/feat/dev-04-qualification/tests/platform-integration/development/INT03C.md)
with engineering in [Infrastructure #56](https://github.com/baobab-platform/infrastructure/pull/56).
It documents exact commands, assertion meanings, verifier permission boundaries,
FAIL/BLOCKED semantics, artifact adoption, rollback and cleanup recovery. Use its
reviewed immutable source once merged; the register records actual observations.

| Original case | Required evidence |
| --- | --- |
| issuer-issuance-and-readback | Real owner token; separately authenticated named verifier binds current issuer/subject/client/audience/scope/expiry/status; positive CP control |
| current-cp-principal-and-link | Checker reads exact ACTIVE canonical Principal, approves exact issuer/subject/run/source provenance after same-Principal denial, and own context succeeds |
| wrong-audience-denial | Genuine same-subject wrong-audience token stays issuer-active and unexpired but CP returns 401; valid control succeeds |
| wrong-tenant-denial | Same unexpired bearer receives sibling/external tenant 403 while own context succeeds |
| issuer-revocation-before-expiry | Positive control, native revoke, independent active-to-inactive readback, same-token CP 401 while expiry remains future, fresh-token control |
| cp-principal-deactivation | Digest-bound maker/checker mutation, same-Principal/wrong-digest denial, terminal CP readback, same-token CP 403 while unexpired and issuer-active |
| complete-teardown | Native proof client and human deletion/readback, issuance denial and token inactivity, terminal CP state; independent host accepting-runtime/resource inventory and private-state removal |

Qualification remains pending until original current-run receipts are downloaded
and hash-verified and all final source/CI checks pass. Closed per-case reports
must retain failed and unexecuted outcomes; missing evidence is not success.
Only host teardown may complete the last case. Dependency source pins, actual
executed harness, runtime image IDs/digests, lock/config/Shared contract hashes
must be recorded separately from reviewed and merged source identities.

This gate does not qualify CMS/NAB-03, estate BFF sessions or ID-token consumption,
IAM's registered canonical provider hook/conformance, full canonical L4 or C4
protected readiness, external legal sources, staging or production. Provider
support stays PARTIAL. The private fixture hook normalizes identity only;
canonical Principal, link, context and grants remain CP authority. The exact
seven-case acceptance does not automatically close these broader findings.
