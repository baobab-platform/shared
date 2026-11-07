# DEV-11 — composed Trade and native ERP integration, 5 November 2026

This dated engineering assessment follows the [engine-local checkpoint](2026-11-04-dev11-engine-local-qualification.md). It is evidence review under EA v2.3 / EA-DEV DEV-07/09/11/12/14, not an ADR, release approval or an L4-OPS-01 acceptance receipt. It builds on the existing Trade publisher and ERP consumer; no parallel messaging framework is introduced.

## Exact execution composition

| Owner | Exact execution source | Purpose |
| --- | --- | --- |
| Trade #189 | `f2c88d4a70486abe0e44c642f22feaaf8bc18c6c` | Actual merged native-owner and confirmed-publisher implementation |
| Trade #189 parent | `2b4c7c929801d47d1215771f6071c2704ddd38ec` | Buyer valuation, native Order Module and atomic composition foundation |
| Trade #188 parent | `55659409a7e4787c0d70a69d4c1301f13d7fc219` | Durable broker dispatch, crash/replay and actual OTLP instrumentation |
| ERP #125 | `115e9a0d22ed6516a649bc6d36bdfc0b658880c2` | Native UUID recovery mapping and real same-event JVM qualification root |
| Infrastructure #72 | `65931ab9892b829b0e0b1ca23c53199ba1216e8b` | Independent exported-span observer and collector configuration |
| CP accepted main | `6fee9fe9537409df428a2e3dd7b8f78ff8d1d456` | Actual runtime context, legal-actor and native posting authority |
| IAM #153 | `fae32b20187b2201e6070c382f563e170773e692` | Real disposable Hydra workload identity configuration |

The execution root is ERP's real-stack job. It checks out the exact composed Trade source, verifies both parents as ancestors, invokes that source's original Medusa outbox producer and RabbitMQ dispatcher, and runs its own current consumer and JVM. It does not invoke Trade's separate broker-component workflow or import that workflow's separately pinned ERP. This is an acyclic executable source tuple, not an assertion of reciprocal repository-SHA equality or a waiver of the eight-owner verifier.

The distinct successful broker-component run `41905489004` executes Trade `f2c88d4`, ERP `1db56a20d049ac772afc40c0223f2d897cdcf7e7` and Infrastructure `65931ab9`. Its original ZIP artifact `13359778340`, SHA-256 `feb51ef16add0087dac96fde7573e041f1d0c052652de9ee646271b1abbfd091`, was independently downloaded and accepted by the original Infrastructure broker receipt validator for THAT tuple. It proves confirmed dispatch, both crash windows, fenced reclaim/replay, DLX/unroutable negatives and seven exported spans/six parent edges. It retains `NATIVE_ORDER_ABSENT` and is not evidence for the final ERP JVM source.

Trade's separate native transaction run `41905488909`, original artifact `13360850358`, SHA-256 `d661896ee60d78c877b362034425ad333f24c9179cdfd605ef0ed5b8cd139022`, was independently downloaded. It proves native DRAFT order/line transaction and rollback negatives; it does not prove a genuine non-draft governed buyer commitment. All required Trade workflows at the composed head pass; the optional formatter helper was skipped and is not counted as a pass.

## Native identity and same-event ownership

ERP's migration `0026_order_native_reference.sql` retains the full opaque Trade order ID, tenant/legal entity, engine/client/Organisation, version, payload digest and original source event. It allocates a distinct random native `C_Order_UU` and commits the recovery intent before a remote native call. This private recovery coordinate is neither a CP Mapping nor an authority grant. POReference is not widened or used as a truncated/hash alias.

The intent is immutable; creation-attempt and native-ID settlement are once-set. Native UUID type/capacity and a valid live exact unique native key are checked before creation. Existing CP legal-actor, documentary, company/placement, REST request and JVM vetoes remain mandatory. Initial creation and uncertain-result adoption both require complete native business-fact readback. Older versions remain `STALE_VERSION`; unsupported amendments remain refused.

The actual Trade source returns only IDs of already persisted envelopes. A separate Trade publisher process claims those original outbox rows. RabbitMQ delivers to the separate ERP consumer and durable inbox; ERP does not manufacture a new event or directly call the consumer. Local settlement binds the exact original event and full order to the verified native ID together with execution, consequence, consequence outbox and fenced inbox outcome. Read-only observers join both databases, native UUID and actual CP/JVM attribution; a separately sourced observer queries the real exported graph.

## Runtime review

The repaired ERP source above passes all nine PR workflows. The full CI (`41946627447`) includes real native Gate D and full ERP-A; Foundation (`41946629114`) includes the container vulnerability scan and full-history secret scan; Security (`41946628507`) also passes. The real-stack runtime (`41946627517`, job `126980351291`) passes independently of those source/security checks.

The runtime's original artifact `13379825989` was downloaded separately from the worker execution. Its complete ZIP SHA-256 is `9a49bd788e3159ec313a8e88cfb5d28d0082ff433fc72a9bf18bd6ab2fcab90b`, matching GitHub's recorded artifact digest. Infrastructure `65931ab9`'s unmodified `verify_zip` and `native_receipt("l4_erp_native", ...)` accept it for the exact CP/IAM/ERP tuple above. Both persisted-event join receipts independently bind all five execution sources above and report unchanged payload, event ID, correlation and traceparent.

| Original source receipt | Independently reviewed result | Limit |
| --- | --- | --- |
| `dev11-native-effect.json` | Actual iDempiere order and lines, company isolation, original inbox, immutable native UUID reference and consequence/outbox verified | Sales-order placement, not invoice, shipment or GL posting |
| `dev11-cp-jvm-lineage.json` | Two independent PostgreSQL read-only observers reconcile current CP authority decisions and actual JVM attribution | Does not qualify Trade buyer permission |
| `dev11-native-unknown-adopted.json` | JVM committed, worker outcome lost, original event replay adopted the verified existing native order | No second native order and no synthetic success substitution |
| `dev11-trade-jvm-joined.json` and unknown-result counterpart | Exact persisted Trade event joins the real protected JVM effect through broker/inbox | Trade's originating business input is synthetic |
| `dev11-trade-jvm-exported.json` | Independently queried exported graph: 10 spans, 9 parent edges, Trade/publisher/ERP services | Source is not an authorised native buyer commitment |
| `dev09-cleanup.json` | COMPLETE; run-owned containers, networks and volumes all zero; temporary directory removed | Host/image teardown is outside this receipt |

The original source report retains `full_medusa_buyer_commitment_proven=false`, `native_buyer_origin_refusal=NATIVE_ORDER_ABSENT`, `protected_acceptance=false` and `l4_ops_01=BLOCKED`. Its separate legacy full-lineage flag also remains false: the now-proved exported component graph must not be relabelled as the missing genuine buyer lineage.

Earlier failed candidates remain failures. At `698a5e9`, run `41910924583` reached native UUID schema verification and an `EXECUTED` inbox outcome, then the independent effect observer refused. Original artifact `13362952605` was independently downloaded and its SHA-256 `a1b4329697c6e1ac2f2a7347a000e87bc36d7c467cad4b1e12b03500f93de071` verified. Cleanup removed all run-owned containers, networks, volumes and temporary files. The worker's success assertion did not overrule the observer. Subsequent source adds closed refusal diagnostics and suppresses private child arguments on failure; no native/authority comparison is removed.

The fresh single pip resolution of ERP plus Trade's frozen telemetry requirements passes `pip check`; the local pinned Python 3.12 suite passes 417 unit tests. Actual Actions qualification uses Python 3.14, Node 24, PostgreSQL 17, real Hydra/CP/RabbitMQ and the actual iDempiere 13 JVM. Local fixtures are not substituted for that execution.

## Unchanged acceptance and merge boundaries

The composed source deliberately uses synthetic business inputs. Its original Trade observer must retain `NATIVE_ORDER_ABSENT`. Even a successful same-event JVM component run does not prove a genuine ENFORCED non-draft buyer/seller/spend commitment or complete authenticated BFF/IAM/CP/Trade lineage. Native sales-order creation does not qualify shipment/invoice/GL posting. The current independent eight-owner custody join and remaining estate/booking requirements remain required. DEV-11/L4-OPS-01 stays **BLOCKED**, with no staging, production or provider activation authority.

The earlier native ActiveMQ 5.16.7 HIGH findings, CVE-2026-50734 and CVE-2026-53917, were repaired with checksum-pinned upstream ActiveMQ 5.19.12 artifacts while preserving the native OSGi bundle identities. The native setup profile and main runtime both install the necessary JMS 2 API; an actual native OSGi/JMS/OpenWire probe runs after native startup in Gate D. Current Foundation and native runtime passes qualify this combination. No vulnerability exception or severity reduction was introduced.

A single exact historical Gitleaks fingerprint exempts a public Maven JMS archive checksum that was falsely classified as an API key. The exception documents its public provenance; it is neither a secret-value exemption nor a directory/rule bypass. The current revision also separates that checksum from the artifact's API name, and its complete secret scan passes. Earlier candidates (`c2084bee`, `261549cc`, `b42e6b29`) remain failed runs: the final successful revision does not retroactively qualify them.

This dated increment contributes to existing BA-AUD-080, BA-AUD-087, BA-AUD-092 and Infrastructure #72 F05 without closing their broader requirements or creating a second acceptance register. The old checkpoint remains a record of its historical source. New runtime originals must be independently checked at their actual exact source; expired evidence requires requalification or approved custody.
