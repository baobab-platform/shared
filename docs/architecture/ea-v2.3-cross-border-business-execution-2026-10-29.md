# EA v2.3 expansion — Cross-Border Business Execution (EA-XB)

**Decision:** ACCEPTED programme objective by explicit Platform Owner direction, 29 October 2026. **Publication:** effective as the EA v2.3 cross-repository acceptance expansion only after reviewed, CI-green merge to Shared \`main\`. **Execution evidence:** NOT EXECUTED; no provider, corridor, enterprise or production acceptance is conferred.
**Scope:** Additional enterprise-business outcome gate; not a replacement for EA v2.3, EA-DEV/EA-REL, ADR-SHARED-036, existing EA-R02/R03, EA-09, Gate A–E, or the authoritative v2.2 L4 case registry.
**Owned by:** Shared Platform Architecture (programme/semantic integration); CP/IAM (tenant and actor), Trade (commercial commitment), ERP (manufacture/finance), Regulations (jurisdictional normative decision), Trade Docs (documentary custody), TMS/logistics provider (physical movement), Payments (money execution), Infrastructure (connected runtime/custody); each retains its accepted decision authority.
**Machine-readable design inventory:** [EA-XB acceptance matrix](ea-xb-cross-border-acceptance-matrix.json). Validation is structural assurance only.

## 1. Governing objective

The defining **business-outcome acceptance objective for the next EA expansion** is an end-to-end, independently evidenced, cross-border trade lifecycle between legally distinct enterprises in different African markets, including an unrelated external customer; **passing SaaS tenant onboarding, IAM issuance, a customer portal, or isolated engine CI is insufficient** to claim this enterprise outcome.

Success SHALL prove **actual execution of controlled domain operations across independent authorities**, from supplier procurement to manufacturer production, trade contracting, customs/origin decisioning, logistics delivery, bilateral accounting and financial reconciliation, with current IAM/CP/legal actor authorization and complete negative cases. No single aggregate \`PASS\` may hide BLOCKED mandatory stages.

This gate is \`EA-XB\`, a **new programme-level overlay**, not a new L4 \`INT-\` ID, canonical capability, provider, ADR reassignment or a production licence. Existing L4/NAB/FIN/EVT/REG/REC cases remain mandatory with unchanged meanings and owners. EA-XB receipts cite their separately executed canonical L4 cases; do not fork, rename or declare an existing case NOT_APPLICABLE.

## 2. Reference-enterprise topology (synthetic only)

- \`ZA-MFG-01\`: **independent South African industrial/solar water-pumping systems manufacturer**, an \`EXTERNAL_CLIENT\` with a separately onboarded commercial ProductSubscription and its own Tenant, Organisation, verified-in-real-life LegalEntity, Market ZA and finance context. No Nabhold affiliation or internal subsidy.
- \`UG-BUY-01\`: independent Ugandan B2B equipment buyer, first as a **non-Baobab external counterparty** and separately as an optionally onboarded \`EXTERNAL_CLIENT\` tenant. Both variants mandatory. Never force the buyer into a fake DigitalEstate.
- \`EXT-COMP-01\`: unrelated non-Baobab component supplier, used for imported manufacturing inputs.
- Optional \`EXT-CARRIER-01\`, \`EXT-CUSTOMS-01\`, and \`EXT-PSP-01\` represent **non-qualified external boundaries** until their true permitted sandbox/provider evidence exists, not fictitious active registrations.
- Product and test quantities (illustrative only): 20 assembled pumping systems; imported component inputs, BOM/production order, serial/lot outputs; USD contract currency, ZA reporting in ZAR and UG reporting in UGX. No actual HS code, customs duty, origin status, delivery date, exchange rate, Incoterm, UNBS clearance, bank payout or verified organisation is asserted.

The Ugandan buyer can later become a Baobab customer **without duplicating verified canonical identity**. Its supplier/buyer commercial role is tenant-scoped and independently authorised. Ownership, commercial relationship, IAM membership, PlatformAccount, subscription and data-access grants remain different facts. No global cross-tenant database, transaction, identity or inferred authority.

## 3. Cross-repository capability and owner boundary

| Step | Owning authority | Required integration; never infer |
| --- | --- | --- |
| Enterprise admission, subscriptions and context | CP / IAM / Subscriptions | EXTERNAL_CLIENT, two distinct tenancy/legal placements, grants/bindings; zero DigitalEstate permitted. Subscription is not authorization. |
| Prospect, RFQ, quotation, contract and commitment | ERP-local **provider-neutral Baobab CRM** where applicable; Trade owns RFQ, quotation, commercial order | Sales pipeline does not authorise a Trade buyer commitment. Both seller and buyer current authority at the native commit point. |
| Component import, supplier payable and receiving | ERP (iDempiere 13 / PostgreSQL 17) and Regulations/Docs | Real accepted purchase, receipt, valuation, customs/source evidence and current native posting veto. Supplier portal cannot assume supplier is a Baobab tenant. |
| BOM, MRP, work order, consumption, WIP, output | ERP manufacturing capability after upstream audit | Actual native transaction, production genealogy and balancing; upstream iDempiere modules alone do not mean Baobab canonical provider support. No manufactured inventory without documented cost and legal placement. |
| Tariff, origin, preference, conformity, customs | Regulations normative requirement/decision; Docs evidence workflow | Current jurisdiction, date, HS/product evidence, source/version, origin rule and approval. Pulse is advisory only; absent/contested official facts yield UNKNOWN/BLOCKED, not ALLOW. |
| Freight, custody, clearance, delivery | TMS or independently qualified logistics provider; Trade Docs | Booking, carrier acceptance, documentary handoff, custody and final delivery independently witnessed; no fabricated tracking/ETA or import release. Thamani not forcibly involved. |
| Bilateral accounting and payment | ERP GL/AP/AR/FX/landed costs; Payments separately executes money | Exporter receivable and importer payable are independently governed; no shared mutable invoice/ledger, no bank authority from ERP payment recording. Unknown PSP outcome reconciled, never blindly retried. |
| Intelligence and evidence | Pulse/Regulations/Docs, Infrastructure | Separate sourced advice from regulatory decision; signed/hashed, time-pinned, redactable immutable evidence + independently verified teardown. |

**Technology direction:** \`baobab-crm\` and \`baobab-people\` belong in \`baobab-erp\` repository as product families. Their internal placement does **not** imply shared mandatory runtime, a new Engine, an automatic iDempiere dependency for external CRM, or a Salesforce monopoly. Specialist capabilities must be separately registered in Shared before provider declarations/CP binding. CRM account and opportunity authority does not subsume canonical Organisation or ERP invoice authority.

## 4. Acceptance classes and source truth

**EA-XB design acceptance:** this programme amendment, machine-readable case inventory, owner/source mapping and automated structural tests merged and green. It does **not** close a case.

**EA-XB component evidence:** relevant owner suites actually executed with version/digest pins; failures retained; statuses per case; real iDempiere PostgreSQL 17 native posting observed where ERP is implicated. No mock authorisation or synthetic provider used to claim actual external service.

**EA-XB connected synthetic execution:** real current pinned IAM/CP, Trade, native ERP and applicable Docs/Regulations/TMS/Payments components in an isolated bounded runtime. Synthetic enterprises, identity/mandates and regulatory *test fixtures* are clearly labelled; all mandatory cases evaluated. Missing provider or source must remain BLOCKED; no synthetic proxy is treated as external clearance or settlement.

**EA-XB provider sandbox execution:** external carrier/customs/PSP/regulatory data source is named, separately approved and traced by immutable receipt. Sandbox success cannot constitute live customs clearance or real money movement.

**EA-XB protected/production acceptance:** independently accepted legal actor, jurisdictional rules, qualified providers, real document custody, operational restore, signed release scope and financial/physical consequences. No aggregate business-ready flag from source merges, CI green or synthetic Actions. Explicitly record cases and evidence axes ARCH/CONTRACT/SOURCE/CI/L4/STAGING/EXTERNAL/OPS-GO.

**Enterprise-outcome exit:** all mandatory EA-XB cases \`PASS\` at **the same specified evidence class**, with actual owner run/time/commit/contract/image references and verified negative and teardown receipts. A \`PASS\` in development cannot be promoted to protected/production without re-execution at the required trust level. \`BLOCKED\`, \`FAIL\`, \`NOT_RUN\` and \`NOT_APPLICABLE\` are not acceptance. A new test *may* be nonmandatory only by a reviewed Shared decision; this first baseline makes all cases mandatory.

## 5. Mandatory profile and negative assurance

The [design case inventory](ea-xb-cross-border-acceptance-matrix.json) enumerates \`XBE-01..XBE-18\`, each with accountable owners, prerequisite, positive, negative, evidence and initial \`NOT_RUN\` status. It covers:
1. Unrelated South African enterprise onboarding with no Nabhold access, and buyer-as-unsubscribed plus buyer-as-tenant variants.
2. Current identity/mandate and bilateral role/Market constraints, RFQ/quotation/commit, imported input supplier and procurement.
3. Actual iDempiere BOM/production/costing/traceability, origin/duty and documentary evidence, goods shipment, receipt and customs.
4. Bilateral GL/AP/AR/FX/landed cost, Payment execution/reconciliation, event replay/rollback, buyer-offboarding historic evidence and disaster recovery.
5. Reject bypasses, wrong audience/tenant/legal actor, B2C fallthrough, expired mandates, ambiguous origin/HS, quarantine release, duplicate native documents, swapped invoice/currency/amount, blind PSP retry, replay, unavailable providers and unauthorised data exchange.

Every positive MUST have an independent negative/failure path and refusal evidence; missing current authority fails closed. The run must report each owner/provider separately and verify all required actual services rather than injecting fake ALLOW.

## 6. Programme execution and dependencies

| Workstream | Deliverable | Hard dependencies / status at inception |
| --- | --- | --- |
| **XB-00** | EA-XB acceptance/design inventory and governance CI | This PR; **design only** |
| **XB-01** | Upstream iDempiere 13 manufacturing BOM/MRP/production/costing adoption/census + native veto assessment | ERP ADR-015/022, Shared ADR-034/037/038; manufacturing was historically out of scope and is **not proven** |
| **XB-02** | Canonical product/BOM/work-order/lot genealogy contracts; finance/Trade mapping | Shared contract decisions; no raw AD IDs in public contracts |
| **XB-03** | External manufacturer + optional Ugandan tenant qualification and buyer/supplier continuity | CP ADR-BCP-014/017/018, IAM; INT-07 zero-estate unchanged |
| **XB-04** | Connected Trade RFQ/order/ERP work-order/stock/accounting journey | DEV-07/09 owners; native commit authority and event reconciliation |
| **XB-05** | ZA→UG corridor rules, tariff/origin/conformity and documentary evidence qualification | Regulations/Docs; actual source dates and independent legal review; no invented duty/preference |
| **XB-06** | Carrier/TMS, cross-tenant documentary delivery, bilateral invoices, FX and Payments | Real qualified providers; external sandbox claims kept distinct |
| **XB-07** | Complete XBE-01..18 connected case execution, source/receipt custody, independent negative/teardown and release review | Does not inherit an INT/L4 pass; all mandatory cases PASS at same required level |

XB does **not** renumber DEV-00..15, rewrite L4 INT-01..08, or change historical EA-DEV receipts. Its dependencies are *evidence and business-outcome* constraints, not a blanket prohibition on continuing independent safe engineering or launching a separately scoped public CMS website. Progressive IAM/CP releases under EA-REL may continue by their own approved gates; they must not be advertised as cross-border business execution-ready.

## 7. Evidence receipt and stop rules

An owner must retain: canonical case ID, scenario/failure step, preconditions, synthetic-vs-real participant classification, legal actor/Market/Tenant/Organisation per side, current CP decision/expiry, authority and contract pins, source commit and image digests, real component and third-party version, DB migrations, event/object reference and correlation, test issuer, actual run and stage, executed positive/negative assertion, regulatory source/effective date/decision, customs/transit references where applicable, verified finance/PSP disposition, redacted immutable log/hash, reviewer, independently verified teardown, remaining blockers and explicit rollback/restore outcomes.

No PII, credentials, taxpayer identifiers, production bank data or restricted documents in public/shared receipts. A disputed shipment, legal-actor mismatch, revoked entitlement, absent official rule, unknown PSP settlement or failed restore is **BLOCKED/FAIL** at the applicable gate, never silently N/A or synthetic PASS.

## 8. Change control

Shared may amend programme cases and mappings through explicit reviewed changes. A new canonical event/namespace, capability, cross-tenant grant, legal actor or native operation requires its *own* Accepted owning-domain and Shared contract decision. Domain implementations belong in their repos with owner CI. Every PR must link back to XBE scenario IDs **without changing** the v2.2 canonical L4 registry. The programme itself grants no corporate/legal authority, provider certification or protected/production activation.
