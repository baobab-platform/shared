# SH-NAB-FIN-02 — Finance F1 contract design checkpoint (16 October 2026)

**State:** HISTORICAL DESIGN CHECKPOINT, not a runtime contract. **Authority:** Proposed ADR-SHARED-033; accepted ADR-SHARED-017, ADR-SHARED-034/037/038 and EA v2.2. **Stewards:** Shared capability-contract steward and baobab-erp semantic owner.

## Deliverables and limits
- [Candidate JSON Schema](finance-f1-candidate.schema.json) specifies scoped ledger-read, journal draft/transition and statement-read envelope types.
- Names proposed in ADR-SHARED-033: `finance.ledger.read`, `finance.journal.manage`, `finance.statement.read`. These names are **not** added to the canonical catalogue in this increment, and no provider registration, CP binding, rollout activation, or implied ERP implementation occurs.
- CP resolves Tenant, PRIMARY Organisation, operating legal actor, legal entity, mandate, capability, market and EngineInstance. Never trust these values from finance JSON bodies.
- ERP owns the FinanceBaseline, chart, journals, fiscal period controls, posting, accounting truth and report generation. A draft request is not a posting permit. Maker/checker separation uses distinct canonical principals.
- The controller must enforce double-entry balance in a fixed precision decimal implementation, positive monetary semantics, closed-period denial, chronological periods, data completeness, concurrency version and idempotency on every command. JSON Schema is a necessary structural check, not sufficient enforcement.
- Statement responses must carry as-of, period, currency, version and completeness. `partial`, `stale` and `withheld` cannot be presented as complete financial results.
- Posting veto / native operation source is independently governed by ERP and CP; F1 read and journal contracts must never bypass the accepted native authority classes or generate payment/settlement permission.
- All realistic examples and negative fixtures must be synthetic. No real Nabhold journal or legal evidence is asserted.

## Required review and promotion stages
1. Obtain explicit Shared and ERP approval of ADR-SHARED-033, including whether journal changes need dedicated command envelopes and whether statement rows should be specialised by type.
2. Split candidate into canonical request, response, problem and event contracts, replace local scalar approximations with pinned Shared canonical definitions, verify finance baseline reference semantics.
3. Create synthetic positive/negative fixtures: missing scope, wrong currency, float amount, reversed dates, unbalanced lines, maker=checker, stale expected_version, repeated idempotency key with changed payload, closed period, absent/expired CP grant and cross-tenant context.
4. Add three definitions and sorted catalogue entries with DRAFT/EXPERIMENTAL status, verify with `scripts/validate-capability-contracts.rb` and `scripts/capability_catalogue.py`.
5. Separately implement ERP HTTP/native adapters, migrations, persistence and actual JVM/iDempiere tests; only then update provider declarations to their proven level.
6. Prove real-component L4 and protected staging, CP activation and finance approval independently. No release is production-permitted from this document.

## Other EA-R03 work (parallel owners)
- Trade: merged Trade-0 CP Seller Operating Binding and resolver are preconditions for Trade-A–D real consequential order writes.
- ERP: merged ERP-A and ERP-B engine-local proofs do not demonstrate final native posting, manufacturing or remaining accounting families under real deployed iDempiere.
- Payments: D1 merged, D2 PSP/certification outstanding.
- Subscriptions and Trade Docs: native execution-point guards and real L4 evidence remain independent owner tasks.
- Infrastructure #35 is still open; do not reclassify its INT-02 mandatory blocked tests as passed.

## Engineering review correction — 16 October 2026

The candidate now requires an explicit debit and credit with exactly one
strictly positive amount and one zero counterpart. “No zero posting” means no
zero-only line; a zero counterpart is required for an unambiguous wire shape.
Both-positive, both-zero, signed-negative, exponent and JSON-number amounts are
rejected structurally. ERP still owns balance/precision/closed-period/approval
and idempotency enforcement; this draft cannot prove those runtime behaviours.

Ledger responses echo `view` and use separate closed chart, balance and entry
row schemas. Chart metadata and dated journal/entry references therefore have
representable fields. The journal and ledger negative fixtures run through a
real Draft 2020-12 validator in CI, not substring assertions. This remains a
noncanonical historical design checkpoint; #321 supplies the separately
reviewed DRAFT catalogue contracts. ADR-SHARED-033 remains Proposed.


## Subsequent DRAFT wire tranche

The separate `contracts/finance/v1` package in Shared #321 is the indexed DRAFT
wire source. Do not import this historical candidate ID into a consumer. Its
local eight-place draft scalar approximation is not a currency precision policy;
the canonical draft reuses ERP decimal strings and leaves precision to ERP.
The candidate tests now protect separation of proposal IDs from catalogue sources
while permitting a separately reviewed DRAFT tranche to be registered.
