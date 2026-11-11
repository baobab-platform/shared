# DEV-11 cross-owner reconciliation

**Observed 11 November 2026.** EA v2.3 EA-06 and EA-10 require correlation from the initiating request and authority decision to a durable business consequence. EA-DEV DEV-11 adds closed failure diagnostics, browser accessibility and performance, affected-profile PR routing and full nightly or release qualification.

## Authority and acceptance

| Owner | Applicable decision | Required observation |
| --- | --- | --- |
| IAM | ADR-IAM-0017, ADR-IAM-0033/0034 | The real issuer and its credentialed native HTTP transport preserve diagnostic lineage. IAM supplies authentication and assurance. Native workload registration and grants retain their own evidence. |
| Control Plane | ADR-BCP-008, ADR-BCP-018 and ADR-SHARED-042 | CP records the real resolution and issuer calls. Current buyer and seller authority and the distinct price signer mandate are independently verifiable. |
| Trade | ADR-0014, ADR-0017 and ADR-0033–0036 | The native Medusa owner commits the non-draft order, enforced seller and buyer decisions, spend and original outbox event in one PostgreSQL transaction. |
| ZuriBeans | Estate BFF and Shared DEV-11 observability contracts | The confidential buyer entry point propagates W3C ancestry through actual credentialed calls. Estate owners retain the original browser, accessibility, visual and performance evidence. |
| ERP and Infrastructure | EA-06 and L4-OPS-01 | Follow the original Trade event across publisher confirmation, durable inbox and JVM effects. Independently query the Collector backend and verify replay, failed paths and teardown. |

Trace context has no authority role. OTLP/HTTP JSON uses hexadecimal trace and span identifiers. W3C sampling is a bit within a byte. The Collector and Jaeger readback is the acceptance witness for export delivery. See the [OTLP protocol](https://opentelemetry.io/docs/specs/otlp/#json-protobuf-encoding) and [W3C Trace Context](https://www.w3.org/TR/trace-context/#trace-flags).

## Owner changes and evidence

| Owner source | Change and evidence |
| --- | --- |
| [Trade #189](https://github.com/baobab-platform/baobab-trade/pull/189) | The development price issuer indexes validated charge lines and preserves canonical order without an unchecked assertion. The native-owner inventory now explicitly accounts for the leased fixture's price readbacks and checks that it does not invoke the order writer. Local lint, type checking and focused tests passed. The native Order Module and broker component workflows passed at the initial lint-fix head. Two expired Foundation waivers were removed to restore dependency and container scanning. A local production dependency audit still reported 23 high findings. Medusa remediation needs its own compatibility qualification for the pinned transaction owner. |
| [CP #463](https://github.com/baobab-platform/baobab-cp/pull/463) | The failed checksum-verifiable scanner downloads returned HTTP 504. The same Foundation run passed on retry. The JSON exporter branch is an independent component candidate. |
| [CP #465](https://github.com/baobab-platform/baobab-cp/pull/465) | Reconciled with CP main, preserving the price issuer lifecycle and current Go dependencies. The candidate already uses the OpenTelemetry SDK. It is the CP pin in the new composed candidate. Its Go CI and Foundation gates passed. The two CP exporter candidates overlap and require owner review before integration. |
| [IAM #153](https://github.com/baobab-platform/baobab-iam/pull/153) | Updated the Hydra audience candidate's separate security patch and verified the exact runtime module graph selects `golang.org/x/net v0.62.0`. JWT, assertion-audience and driver configuration tests passed locally. IAM exports wire-correct IDs, applies the sampled bit, records bounded HTTP status classes and sends asynchronously with a finite in-flight limit. Race-enabled native BFF tests passed. The SAML dependency finding is independently tracked in [IAM #180](https://github.com/baobab-platform/baobab-iam/pull/180) and remains a Foundation blocker until remediated. |
| [ZuriBeans #159](https://github.com/baobab-platform/zuribeans/pull/159) | Follow-up to merged #156. Fixed OTLP wire IDs and sampled ancestry, capped in-flight requests and removed Collector waits from the buyer HTTP response path. Six focused source tests passed. Estate browser and production-build quality remain subject to their owner workflows. |
| [Infrastructure #72](https://github.com/baobab-platform/infrastructure/pull/72) | Previous connected run [42168676260](https://github.com/baobab-platform/infrastructure/actions/runs/42168676260) stopped during the Trade image build. The harness now writes an immutable, redacted failure receipt after independent teardown, avoids native cleanup before fixture preparation starts, and still attempts CP/IAM cleanup after a failed control probe. The scrubbed receipt remains a failure. The new locks identify the exact owner candidates. The local development suite passed 250 tests. |
| [ERP #125](https://github.com/baobab-platform/baobab-erp/pull/125) | Merged native same-event JVM implementation. Historical [run 41946627517](https://github.com/baobab-platform/baobab-erp/actions/runs/41946627517) used a different source tuple and retained `NATIVE_ORDER_ABSENT`. The ten-span component graph and loss/replay evidence remain valid for that run. |

## Reviewed source tuple

| Owner | Source |
| --- | --- |
| Infrastructure | `794420887aafd23bdf81584577b8d73aad808f41` |
| ZuriBeans | `2ca5d85c663a725c698df4fe66452f113a8a3a23` |
| IAM | `399a505f08ad34922845bfd8a08bab385e2de80f` |
| Control Plane | `ba337b5700ff344e9ca3762a5ded53042a0c07fe` |
| Trade | `b9ad5fa42745f79bc94f43abaec28771a4996ce2` |
| ERP | `f8558b616e81f37ef0246a0e7fc58bc81b2a1e3a` |

This tuple records the candidate sources. Runtime evidence requires the same
sources in the owning workflow receipts and the independent readback.

## Remaining gate

L4-OPS-01 remains **BLOCKED**. The connected HTTP profile and source preflight cannot qualify a genuine buyer purchase. The run needs an actual IAM buyer session and approved workloads, a current CP price signer and mandate, a bound Medusa cart, active budget and an approved signer for the purchase. Independently read the resulting non-draft order, seller/buyer decisions, spend commit and original outbox event under one XID. Dispatch exactly that event to the real ERP inbox and JVM, verify the exported ancestry and repeat replay and refusal cases with independent teardown. Obtain all eight required original receipts and the unchanged estate quality evidence.

The current Trade ERP consequence mapping still refuses unsupported non-zero cross-border charge kinds. Those need a governed mapping and a qualified charged purchase. The protected release and finance-posting gates are independent.
