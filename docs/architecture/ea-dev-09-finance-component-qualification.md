# DEV-09 ERP, finance and Subscriptions component qualification

Observation: 2026-10-25. EA-DEV engineering read model only; no new operation
catalogue, provider contract, authorisation or financial certification.

## Source reconciliation

[ERP #111](https://github.com/baobab-platform/baobab-erp/pull/111) reuses
ADR-ERP-022's native placement, Finance baseline, per-operation CP decision and
transactional native veto, plus Shared ADR-037/038 purchase recording/provenance.
ERP's existing owner CI has a real iDempiere 13 JVM, PostgreSQL 17, persisted
Fact_Acct and native COMMIT fence, not merely Python models or JDBC table stubs.
The ERP-A/B harness uses a pinned CP binary with signed tokens from a test issuer.
GardenWorld, legal verification/mandate records and payment evidence are synthetic.

DEV-09 adds an exact 39-case native inventory (S01–S26, S04b, S22b, B01–B11),
source/dependency/image provenance and a closed sanitised receipt/hash pair.
Each invocation owns a unique Compose project; teardown failures now fail CI,
even after a scenario or log-redaction failure. The cleanup observation independently
queries surviving labelled containers/volumes/networks and temporary directory
removal. It does not certify host or built-image removal. Fixed loopback ports
still prevent simultaneous runs on the same host; collision fails safely.

The separate mandatory Gate D job exercises actual GL journals and sales-side
atomic posting/rollback with a synthetic CP. Its CI result does not by itself
prove a current joined IAM/CP/finance gate. The DEV-09 receipt deliberately keeps
joined GL provenance BLOCKED rather than relabelling another profile's result.

[Subscriptions snapshot](https://github.com/baobab-platform/baobab-subscriptions/tree/52c69906343d7b1afee08a88b8d3afe118af0428)
has a Java 21 service, PostgreSQL store, current INTERNAL CP-authority adapter,
zero-charge INTERNAL policy, usage/idempotency and durable outbox. **Kill Bill,
commercial Payments handoff and outbox relay remain unimplemented.** Its own
README reports commercial billing BLOCKED. Source is not a new onboarding receipt.

[Payments snapshot](https://github.com/baobab-platform/baobab-payments/tree/0eb75baa4aeabaa103a527ecaf63200c17324c69)
has a simulated public sandbox and bounded separate financial execution components;
public HyperSwitch is not activated. Sandbox outcomes move no money. Nothing in
DEV-09 promotes these components to real bank/PSP settlement.

## Mandatory inventory and remaining work

The register preserves 48 engineering observations: 39 original native scenarios,
run-owned teardown and eight joined obligations. These IDs map evidence to the
accepted INT-08/FIN-01–05 requirements; they do not replace canonical cases.

The eight joined obligations cover current estate IAM/CP, independent company/org
isolation, joined GL provenance, Subscriptions INTERNAL current authority,
commercial Kill Bill, Payments simulated lifecycle, external provider settlement
and Trade native COMMIT. One GardenWorld placement does not prove independent
native-company isolation. A synthetic execution-evidence record does not prove
payment disbursement. Every unavailable path remains BLOCKED.

Full DEV-09/INT-08 has no completion date, protected acceptance, provider
qualification or production authority. DEV-06/INT-07 stays deferred until after
Subscriptions onboarding; that onboarding must still be followed by current CP
binding/resource enforcement and unchanged INT-07 negative differentials.

## Initial native evidence (immutable historical receipt)

[ERP #112](https://github.com/baobab-platform/baobab-erp/pull/112) merged as
`62c5e1d6bfc438f17eb442ab26a8e218e5c2cb2b`, reviewed head
`d205edebd14a970d6c438ac2878b313b72c9aac6`. All 41 final-head checks completed
successfully or were applicable skips; native Gate D and ERP-A ran successfully.
The original receipt was observed at 2026-10-25T05:14:28.895767Z in
[owner CI run 40164469183](https://github.com/baobab-platform/baobab-erp/actions/runs/40164469183).
Its source `2a973263ec720cf3d3e035c8ea47def47b503d46` is the tested PR merge,
whose parents contain the reviewed head and whose tree equals the actual merge.
CP pin: `0337632756dea1bd99db098d02e71d8a170027f2`.

[Artifact 12588260076](https://github.com/baobab-platform/baobab-erp/actions/runs/40164469183/artifacts/12588260076)
archive SHA-256: `ebf53b62facb2f4654e9a519e09c2fdc95d653b3f5d6eaa6cbcaf1a0b2986da1`.
The archive digest was independently compared with GitHub metadata; original
report bytes match the original companion hash:
`8bb408f19c3b6b24119c949fd003fd10c18a42a908902e15328ae9912986c306`.
GitHub's actual expiry is **2026-11-09T05:08:55Z**, despite the workflow's 30-day
request. Original bytes are retained at
[evidence/dev09-2026-10-25/dev09-report.json](evidence/dev09-2026-10-25/dev09-report.json)
and [the companion hash](evidence/dev09-2026-10-25/dev09-report.sha256.json).

All 48 cases were inspected: **40 PASS / 8 BLOCKED**, no FAIL. INT-08, current
IAM, provider qualification, protected acceptance, production authority and money
movement flags are all false. Cleanup COMPLETE applies strictly to run-owned
Compose containers/volumes/networks and temporary files; host/images are excluded.

The N0009 increment verifies actual active AD_Org ownership and rejects misplaced
or reassigned native organisations, with 39 executed JDBC/PostgreSQL cases. Its
two-company database fixture does not establish native company provisioning or
independent JVM accounting. Those remain blocked in this initial receipt.

## Real Ory and second-company increment

[ERP #113](https://github.com/baobab-platform/baobab-erp/pull/113) is an unmerged
candidate. It requires actual pinned Hydra/Kratos, current CP workload contexts,
native InitialClientSetup and company-B-only balanced Fact_Acct with a matching
CP decision. Failed or pending CI is not an observed PASS; a successful run needs
its own original receipt/hash and final-head review. The initial pair above must
never be overwritten.
