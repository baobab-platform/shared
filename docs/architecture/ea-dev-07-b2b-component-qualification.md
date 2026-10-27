# DEV-07 — ZuriBeans B2B development qualification

The Accepted EA-DEV plan permits DEV-07 after DEV-03 and available adapters.
DEV-06/INT-07 is explicitly partial and will be revisited after Subscriptions
onboarding. That sequencing does not suspend unrelated development or imply
that Subscriptions alone supplies CP binding, provider qualification or current
resource-server enforcement. No accepted scenario meaning changes.

The current Trade assessment (BA-AUD-057–065) distinguishes substantial native
Medusa commerce from the three still-planned canonical provider contracts.
This increment uses those real native components and corrects an exposed
assortment safety gap; it does not promote the provider declaration or activate
the SHADOW native buyer commitment fence.

Trade #172 adds a disposable PostgreSQL 17 owner-suite using actual migrated
Medusa services, persisted buyer Organisations/membership/role/Market-grant rows,
separate UG and ZA ten-product catalogue projections including vanilla, and
the maintained public assortment handler. The endpoint cannot accept a caller's
relaxed regulatory setting. It excludes expired/future, malformed, withdrawn
and ambiguous eligibility records under the server clock and returns no-store.
The ZuriBeans consumer already requests strict clearance; its Figma/UI work is
independent and is not included in this development change.

The report deliberately distinguishes local native Principal references from
real IAM-issued/CP-resolved buyer identity. Native Market grants cannot supply
the missing canonical Market authority. No fake CP answer is injected to obtain
an ALLOW. The suite observes the current UNAVAILABLE refusal and preserves the
joined journey as BLOCKED. Native public assortment is neither private buyer
pricing nor permission to commit an order or ship goods.

The original INT-05 obligations remain the acceptance authority. Nine explicit
blocked engineering outcomes cover joined buyer identity, independent supplier
and ERP onboarding, entitled private catalogue/prices, canonical RFQ and controlled
approval, quotation lifecycle, composed native order and replay fencing, actual
ERP steps, shipment/document access and cross-jurisdiction seller authority.
The native report's finite labels are component observations, not replacement
canonical scenario IDs. There is no completion date or protected/provider/
production acceptance.

## Operations and custody

Trade's `docs/development/DEV-07.md` documents the exact command, disposable
configuration guard, original case inventory, maintenance triggers, cleanup and
rollback. Source/unit tests do not themselves prove PostgreSQL execution. Actual
CI reports must be downloaded, hash-checked and reconciled to the exact reviewed
source. The sanitized original report/hash bytes are also retained unchanged under
`evidence/dev07-2026-10-25/` for durable source custody.

Cleanup revokes append-only grants and verifies their terminal state, soft-deletes
their referenced buyer relationship records and removes the owned product and
eligibility. All cleanup actions are attempted on failure. Completed reports
require independent active-absence readback. This is native fixture cleanup;
physical database row erasure and Infrastructure host/network/image teardown
are not certified by the owner report. The disposable CI service lifecycle owns
its PostgreSQL/Redis disposal. Full joined acceptance must subsequently use the
existing Infrastructure guarded lifecycle and independently verified teardown.

## Remaining engineering order

Compose actual IAM/CP buyer Principal/Organisation/Market authority and supplier
onboarding, implement and qualify exact RFQ/quotation provider lifecycles, and
finish composed buyer receipt/spend consumption at the native commitment point.
Then connect available ERP/Regulations/documentary adapters, preserving per-operation
BLOCKED where missing. Verify wrong legal actor/Market, absent grant, private
price/document isolation and duplicate/replay through actual execution paths.
A native module test, local policy ALLOW, Medusa customer token or public catalogue
result cannot substitute for these obligations.

## Initial verified native observation — 25 October 2026

[Trade run 40156275115](https://github.com/baobab-platform/baobab-trade/actions/runs/40156275115)
retains `dev07-native-b2b-components`, artifact `12584404889`. The downloaded ZIP
SHA-256 is `6ae6a96f77299100b375db26bbe63797a8c3cf32d59e625c9413a54562897491`;
the original `report.json` SHA-256 is
`1b34b4631bb93c8340aa7b8efe4cf370ad2018e148fac7523aa1b898dddbc11f`.
Both independently match their artifact/receipt metadata. The report's source
SHA `2aaf478d5363bf94f082591691f025f8882d3db4` matches the tested PR merge for
reviewed head `beee8c6ccdb205c71fd483011628ba00f87e74bb`.

The exact observed result is **16 PASS, 9 BLOCKED, no failures**. All sixteen
native component observations and active-fixture cleanup completed. Joined
IAM/CP buyer, canonical INT-05, provider, protected and production qualification
flags remain false. The local Principal-reference-only flag remains true.
The requested workflow retention is 30 days, but the returned artifact metadata
is authoritative: its expiry is 9 November 2026. The original sanitized [report](evidence/dev07-2026-10-25/report.json) and
[hash pair](evidence/dev07-2026-10-25/report.sha256.json) are retained unchanged
in this repository, so receipt custody survives archive expiry.

## Final reviewed source and native observation — 25 October 2026

Trade #172 merged at `afea037ba8e32154ac920667609ac1016a9fb02a` after review of
head `0b99f4aed188361bfaafd198ed5ae577585a3322`. All 35 reported checks completed:
27 successful checks and eight applicable skips. This includes the full core
Medusa/PostgreSQL regression job, Trade-A TA-08, production-infrastructure,
conformance and security checks, with no unresolved review threads.

The final candidate reads the missing-role policy from an actual persisted
membership and removes stale report output before running observations. Fresh
[run 40157210941](https://github.com/baobab-platform/baobab-trade/actions/runs/40157210941)
retains artifact `12584737149`, `dev07-native-b2b-components`. Its downloaded ZIP
SHA-256 is `0a8c284f20d8962b5911b89be810581d52e5c6a3e87960f380e5d5c42429b2db`.
The unchanged original [final report](evidence/dev07-2026-10-25/final-report-40157210941.json)
and [hash pair](evidence/dev07-2026-10-25/final-report-40157210941.sha256.json)
are retained alongside the initial historical pair. The final report SHA-256 is
`fdaa834ac57dc4ac473dc34724709d6c2a5353a3cfe6fc40953bb66fbb2222fb`.
Both archive and report hashes were independently checked after download.

The receipt source `6e48045b78759f36b7703073f684490281c733ac` matches the final
head's tested PR merge. Its exact result is **16 PASS, 9 BLOCKED, no failures**.
All 25 engineering observations remain visible. Local Principal references stay
explicitly synthetic; joined IAM/CP buyer, INT-05, provider, protected and
production qualification flags remain false. Native active-fixture cleanup was
read back; this does not certify Infrastructure host teardown. The final artifact
metadata expires on 9 November 2026, while the retained original report/hash
bytes remain available in this repository.

## 27 October 2026 — workstream conformance audit and corrective candidates

The [DEV-07 conformance audit](../assessments/trade/2026-10-27-dev07-workstream-conformance-audit.md)
traces all delivery obligations across their owners. Infrastructure #66's
actual eight-case buyer handoff failed after successful issuer and CP joins;
failed original reports/hashes are retained separately from the 25 October
baseline. Trade #177 corrects issuer equality, native buyer ID minting,
malformed spending/budget facts and documentary lease validation. Infrastructure
#66 pins reviewed owner source and adds closed, credential-free native refusal
diagnostics. The corrected exact-source run 40492142720 now records all eight live
component cases PASS with independent issuer/CP revocation and host teardown;
full final-head CI/review remains required. This is bounded component
qualification only. Canonical RFQ/quotation, BFF HTTP, atomic buyer/seller/spend
composition and joined ERP/documentary operations remain incomplete or
unqualified. The universal fence stays SHADOW under Accepted Decision 9.
No historical receipt, INT-05 case or provider/protected/production status is
promoted by these source corrections.

**27 October final corrective merge:** Trade #177 (`b8164f6c`) and Infrastructure
#66 (`0538e504`) are merged after full final-head CI/review; Shared #406
(`c1d66ee2`) retains the audit and original passing/failed evidence. The
eight-case live identity component proof is qualified, with independent
revocation and host teardown. The next action is estate BFF/supplier joins,
canonical RFQ/quotation and atomic buyer/seller/spend composition, followed by
available ERP/documentary providers. DEV-07/INT-05 remains partial; no provider,
protected or production acceptance follows.
