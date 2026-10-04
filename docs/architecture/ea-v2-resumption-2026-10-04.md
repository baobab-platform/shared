# EA v2 — Resumption checkpoint, 4 October 2026

**Governing plan:** EA Implementation Plan v2.0, sections 6, 10, 38, 48 and 51.  
**Shared baseline:** `6899a2d8f143bf23d36c4f4ac904e0a1e10c3cea`  
**IAM baseline:** `035fae168053fe91fdaa2c4218da12f36f75cb52`  
**CP baseline:** `c84063cb07dce76e1ffac4b12fa29c5e4e5ec855`  
**Scope:** Current source and consumed locks; focused IAM evidence and next-task sequencing.

## Resumption decision

Continue bounded source/integration work in EA v2. IAM's merged foundation is
sufficient for that continuation, while EA-04 remains partial. This checkpoint
is not certification, workload activation, Digital Estate unfreeze, a governance
enforcement flip or infrastructure deployment authorisation.

IAM PRs [#56](https://github.com/baobab-platform/baobab-iam/pull/56),
[#57](https://github.com/baobab-platform/baobab-iam/pull/57),
[#58](https://github.com/baobab-platform/baobab-iam/pull/58),
[#59](https://github.com/baobab-platform/baobab-iam/pull/59) and
[#60](https://github.com/baobab-platform/baobab-iam/pull/60) merged on
2026-10-04. The earlier dashboard's open-branch assumptions are historical.

| IAM outcome | Evidence boundary |
|---|---|
| Provider-neutral migration invariants | #56 corrections are merged |
| Kratos/Hydra live foundation | #57 isolated, pinned-provider evidence |
| Workload credential/trust mechanics | #58 live issuance, rotation, rejection and issuance disablement |
| Governed M4-C token profile | #59 logical audience, workload actor, stable client, bounded lifetime and scope |
| CP verifier compatibility | #60 compiles CP's unchanged verifier at `20235ac2c4e1c0285e747a5a4b41c1eefb3a4dd7`; all six live scenarios pass |
| Canonical workload activation | Not established; CP and Subscriptions federated identities and deployment reporter remain PROVISIONED |
| Full provider declaration support | Still planned-only; these partial mechanics do not prove either complete canonical identity capability |

The [final #60 live run](https://github.com/baobab-platform/baobab-iam/actions/runs/37173250549)
and [repository CI](https://github.com/baobab-platform/baobab-iam/actions/runs/37173250584)
passed. The evidence is tied to that recorded source/provider/Shared revision,
not automatically to a later pin or a deployed resource route.

Pinned Hydra v26.2.0 propagates the RFC 7523 assertion's endpoint audience into
the access token. #59's governed policy denies that mismatch for both federated
fixtures. Consumer trust must not be weakened to accept the endpoint audience,
and a federated workload must not acquire a static-secret fallback.

## Current lock census

Read from each repository's main lock on 2026-10-04. These are immutable
consumption pins, not a claim that all engines are compatible with the newest
Shared contracts. A behind pin needs semantic comparison and its own tests;
commit distance alone does not establish incompatibility.

| Consumer | Observed Shared pin | Audit scope |
|---|---|---|
| CP | `6899a2d8f143bf23d36c4f4ac904e0a1e10c3cea` | Current reviewed Shared baseline |
| IAM | `10810e20473709d4626da310fc9a84680f8efddd` | Three commits behind; five consumed paths compared |
| Trade | `b063f8a8df3f012baadf068aa9ba312d83929e69` | Lock read; new compatibility verdict not asserted |
| ERP | `0233eb30bcf4070344039e83b70d16248963dd64` | Lock read; the old dashboard's legacy-pin/501 assumptions need a fresh runtime audit |
| CMS | `b63ce52a20d1b6f8acc41d085913c6025d6c859c` | Canonical lock exists; runtime capability not re-audited |
| Pulse | `b63ce52a20d1b6f8acc41d085913c6025d6c859c` | Canonical lock exists; runtime capability not re-audited |
| Subscriptions | `3a8230ebbfe05ede65976363770f0867fa5eac45` | Lock read; federated resource acceptance remains outstanding |
| Payments | `3a8230ebbfe05ede65976363770f0867fa5eac45` | Lock read; federated resource acceptance remains outstanding |

The IAM comparison found three byte-identical contracts, a semantically
identical workload registry, and one additive scope (`context:validate`). No
existing scope entry changed. The registry's new `validates_audiences`
documentation establishes an explicit relationship; no workload has that scope
or relationship registered yet.

[IAM #62](https://github.com/baobab-platform/baobab-iam/pull/62) reconciles the
pin to this reviewed Shared baseline and records the semantic delta. Its
compatibility status is owned by that PR's final-head CI. An open re-pin PR is
not a new main baseline, and scope catalogue membership never grants a scope.

## Execution queue

| Order | Bounded outcome | Prerequisite / disposition |
|---|---|---|
| 1 | IAM EA-01 pin reconciliation and current EA evidence record | In #62 and this checkpoint; exact-pin suites required before merge |
| 2 | Remaining engine contract drift census, then per-engine semantic adaptation/re-pin | Inspect each current implementation and open PR; do not mechanically update all pins |
| 3 | EA-03D capability-based CP billing invocation | Current CP billing client still uses its BaseURL; replace production direct-address authority using existing canonical resolution and eligible instance semantics in a separate CP change |
| 4 | Resolve federated resource audience mechanics and prove CP → Subscriptions / Subscriptions → Payments | Compatible, reviewed provider mechanics and actual protected resource requests; keep PROVISIONED until complete evidence |
| 5 | Governance evidence and remaining engine hardening | Preserve approved shadow/evidence gates; do not flip enforcement merely because IAM tests pass |

Items 2 and 3 may proceed as source/integration work while item 4 is blocked.
Neither is evidence that the federated chain is production-ready. Before each
implementation, re-read governing Accepted ADRs and superseding amendments,
inspect current affected repositories, and preserve the plan's authority split.

## Holds retained

- Real infrastructure assertion issuer, public keys, rotation and expiry evidence.
- Deployed CP route/context/grant/tenant-isolation acceptance; the pinned verifier
  alone does not prove those decisions.
- Federated protected requests against Subscriptions and Payments.
- Governed rollout/rollback and canonical lifecycle activation.
- EA Foundation Unfreeze Gate section 38 and integrated qualification.
- Permanent infrastructure deployment remains execution-last.

This record supersedes older dashboard statements only within the audit scope
above. Other workstreams require a fresh evidence review; their historic labels
are not new readiness findings.
