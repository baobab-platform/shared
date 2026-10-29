# EA-XB v1.1 — Enterprise Corrective Architecture: Cross-Border Operations and Business Networks

**Status:** ACCEPTED DESIGN — Platform Owner conditionally authorised acceptance after review and correction on 29 October 2026. Effective for future qualification claims upon reviewed CI-green merge. **Execution remains NOT_EXECUTED.**
**Date:** 29 October 2026. **Owner:** Shared / Platform Architecture; participating domain owners retain their authority.
**Basis:** Accepted Enterprise Architecture v2.3; merged Shared PR [#411](https://github.com/baobab-platform/shared/pull/411); [EA-XB v1.0 baseline](ea-v2.3-cross-border-business-execution-2026-10-29.md); immutable [XBE-01..18 design inventory](ea-xb-cross-border-acceptance-matrix.json). The baseline's business-execution objective is retained, but its implicit universal manufacturing gate is proposed for correction.
**Proposed companion inventory:** [EA-XB v1.1 proposed acceptance profiles](ea-xb-v1.1-proposed-acceptance-profiles.json). Both this document and the new inventory are **design artifacts only**, not evidence of executed operations, certification or release authority.
**Approval/merge rule:** The Platform Owner requested audit, correction, acceptance and merge after satisfactory implementation and passing checks (Shared #413 review discussion and implementation audit request, 29 October 2026). This records acceptance of D1–D7 and the complete legacy crosswalk as architecture design; effectiveness requires the reviewed CI-green merge. Cross-tenant disclosure, legal decisions, new capability registration, provider activation and protected/production operations retain their independent gates.

## 1. Executive decision request

**Accepted enterprise positioning:** Baobab is a capability-driven **enterprise operations platform** whose differentiating promise is **governed cross-border business execution between independently authorised enterprises**, including non-Baobab counterparties. Core enterprise systems and cross-border workflows are complementary: CRM originates/serves relationships; Trade governs commercial commitments; ERP governs procurement, manufacturing/processing, inventory and accounting; Regulations and Trade Docs govern distinct normative/documentary boundaries; TMS tracks physical execution; Payments executes money; Pulse advises; CP/IAM govern current participants and permissions.

**Seven corrective design decisions accepted (effective on merge):**

| No. | Proposed decision | Replaces no accepted authority |
| --- | --- | --- |
| D1 | Every cross-border readiness claim requires **XB-CORE**, plus independently applicable **XB-AGR**, **XB-MFG**, **XB-NET**, **XB-LOG** profiles. A sector profile must not block another sector's separately qualified corridor. | Preserves PR #411's cross-border business-outcome objective; keeps all historical XBE IDs and existing canonical L4 cases. |
| D2 | Explicitly separate **external non-tenant**, **single qualified tenant**, and **independently qualified bilateral tenant** proof; never require inaccessible foreign ERP books. | CP tenant isolation, Trade commitments, ERP ledger authority remain. |
| D3 | Introduce **opaque cross-enterprise transaction correlation and governed evidence exchange**, never a shared mutable order, transaction, buyer account, document repository or ledger. | Trade/ERP/Trade Docs retain their own aggregate and document authority. |
| D4 | Formalise **verified counterparty → independently onboarded platform customer** as *new relationships and grants*, not identity conversion or supplier-data migration. | CP ADR-BCP-014/017/018 remain controlling. |
| D5 | Establish **Baobab CRM as a provider-neutral ERP-repository product family**, separately qualified from manufacturing and People. CRM never owns canonical Organisation, native Trade commitment or finance posting. | Does not invent a baobab-crm repository/Engine or register CRM keys. |
| D6 | Reuse the **generic lot, genealogy, quality, inventory, and commercial evidence substrate** across agriculture and manufacturing without treating one industry's process as canonical for the other. | ERP/Trade/inventory role and authority boundaries remain. |
| D7 | Make acceptance **scenario × applicable profile × trust level × source version × exact actor/market/product/corridor**, not one platform-wide green label. | No production permission from source, CI, development fixtures, or sandbox receipts. |

**Review finding (P0):** the merged v1.0 design asserts XBE-15's independent buyer-ERP proof in the same aggregate suite that requires an external non-Baobab buyer (XBE-02). That buyer's ledger is not within Baobab's authority. In v1.1, bilateral **financial** evidence is required only when both accounting sources are separately authorised and qualified; all other external evidence (commercial acknowledgement, fulfilment, settlement) is still mandatory where applicable. A seller may never claim the foreign buyer's AP/GL merely by observing its own AR.

**Review finding (P1):** v1.0 demands BOM/work-order/native WIP evidence for the universal business-outcome gate. This must remain mandatory for **manufacturing** but cannot hold a separately qualified coffee-export profile hostage. The new test inventory never deletes or rewrites XBE-01..18; each receives an explicit mapping, and its historical NOT_RUN state remains honest until owners execute or formally supersede those cases.

## 2. Sources, evidence and precedence

| Baseline | Audited observation | Disposition |
| --- | --- | --- |
| [ZuriBeans Go-Live Masterplan v2.0](https://github.com/baobab-platform/zuribeans/blob/main/docs/go-live/ZB-GOLIVE-MP-001.md) | Accepted: both UG and ZA may source, buy, import, export, sell and fulfil; R0 public, R1 domestic, R2 corridor/direction/product qualified, R3 market expansion. Three transaction classes: domestic, external cross-border, internal branch/intercompany. | **Preserve** original N-market bidirectionality and independently qualified launch slices. |
| [CP ADR-BCP-011](https://github.com/baobab-platform/baobab-cp/blob/main/docs/adr/ADR-BCP-011%20%E2%80%94%20Market%20Participation%2C%20Trade%20Lanes%20and%20Cross-Market%20Trading%20Model.md) and [ADR-BCP-013](https://github.com/baobab-platform/baobab-cp/blob/main/docs/adr/ADR-BCP-013%20%E2%80%94%20Canonical%20Inventory%20Ownership%2C%20Custody%2C%20Location%20and%20In-Transit%20Model.md) | Accepted: trade lane is not a physical transport route; warehouse/custody/location/ownership are independent axes. | **Reuse** rather than introduce trade-lane or inventory-control masters. |
| [CP ADR-BCP-014](https://github.com/baobab-platform/baobab-cp/blob/main/docs/adr/ADR-BCP-014%20%E2%80%94%20Canonical%20Counterparty%20Identity%2C%20Roles%20and%20Relationships%20Model.md), [017](https://github.com/baobab-platform/baobab-cp/blob/main/docs/adr/ADR-BCP-017%20%E2%80%94%20Organisation%20Admission%2C%20Subscription%20Classification%20and%20Tenant%20Onboarding%20Lifecycle%20Model.md), [018](https://github.com/baobab-platform/baobab-cp/blob/main/docs/adr/ADR-BCP-018%20%E2%80%94%20Canonical%20Organisation%2C%20Corporate%20Group%2C%20Platform%20Account%20and%20Tenant%20Relationship%20Model.md) | Accepted: global verified Organisation identity distinct from tenant-private counterparties, PlatformAccount, legal entity, subscription and grants. | **Extend** existing-org admission and anti-claim-hijack negative tests. |
| [Trade ADR-0019](https://github.com/baobab-platform/baobab-trade/blob/main/docs/adr/ADR-0019%20%E2%80%94%20B2B%20Procurement%2C%20Supplier%20Commercial%20Workflow%20and%20Trade-to-ERP%20Boundary%20Model.md), [Trade ADR-0020](https://github.com/baobab-platform/baobab-trade/blob/main/docs/adr/ADR-0020%20%E2%80%94%20B2B%20Landed%20Cost%2C%20Margin%20and%20Commercial%20Price%20Resolution%20Model.md) | Accepted: Trade runs commercial procurement collaboration; ERP owns PR/PO/receipt/AP, inventory cost and ledger. | **Reuse** across coffee and components; candidate correlation must not bypass Trade/ERP commit fences. |
| [Trade ADR-0026](https://github.com/baobab-platform/baobab-trade/blob/main/docs/adr/ADR-0026%20%E2%80%94%20Incoterms%2C%20Delivery%20Obligations%2C%20Risk%20Transfer%20and%20Title%20Transfer%20Model.md) | **Proposed**, not Accepted; Incoterm ≠ title policy ≠ tax ≠ payment terms. | **Review** and accept independently before claiming controlled Incoterms semantics. |
| [Regulations ADR-REG-0027](https://github.com/baobab-platform/baobab-regulations/blob/main/docs/adr/ADR-REG-0027%20%E2%80%94%20Cross-Border%20Trade%20Regulatory%20Profile.md) | **Proposed** UG→ZA coffee/vanilla profile; direction, product, dates, origin, SPS, customs and evidence separate. | **Extend by addition**: ZA→UG industrial goods needs independent official-source assessment; do not reverse a rule pack. |
| [Trade Docs ADR-TDOC-0018](https://github.com/baobab-platform/baobab-trade-docs/blob/main/docs/adr/ADR-TDOC-0018%20%E2%80%94%20Cross-Organisation%20Document%20Exchange%2C%20Disclosure%20and%20Consent%20Architecture.md) | **Proposed** exact-version, recipient-purpose scoped disclosure, receipt, revocation; not a qualified service. | **Prioritise** owner acceptance, implementation and non-disclosure negatives. |
| [ERP ADR-ERP-015](https://github.com/baobab-platform/baobab-erp/blob/main/docs/adr/ADR-ERP-015%20%E2%80%94%20ERP%20Inventory%2C%20Warehouse%2C%20Procurement%20and%20Supply-Chain%20Architecture.md) and [ERP issue #116](https://github.com/baobab-platform/baobab-erp/issues/116) | Native iDempiere inventory/finance are authoritative; #116 audits manufacturing BOM/work-order/WIP/costing/posting but **does not scope CRM implementation**. | **Keep** #116 manufacturing-specific and add CRM companion programme, including an explicit dependency note. |
| [Shared canonical catalogue](https://github.com/baobab-platform/shared/blob/main/contracts/capability/v1/catalogue.yaml) and [ERP provider declaration](https://github.com/baobab-platform/baobab-erp/blob/main/.baobab/capability-provider.yaml) | No CRM or manufacturing canonical capability family currently registered; ERP declares limited finance/inventory support; source != qualification != activation. | **Propose** keys in owning Shared ADR; do not add arbitrary keys here. |

**Standards researched, NOT automatically adopted as platform contracts:** [ICC Incoterms 2020](https://iccwbo.org/business-solutions/incoterms-rules/incoterms-2020/); [SARS exporters](https://www.sars.gov.za/customs-and-excise/registration-licensing-and-accreditation/exporters/), [SARS Rules of Origin](https://www.sars.gov.za/customs-and-excise/rules-of-origin/); [Uganda UNBS PVoC product categories](https://www.unbs.go.ug/content.php?content=&src=categories-of-goods-covered-under-pvoc); [iDempiere Business Partner](https://docs.idempiere.org/docs/basic-functional/business_partner); [Salesforce API application OAuth](https://developer.salesforce.com/docs/platform/api-rest/guide/intro-oauth-and-connected-apps.html) and [CDC/PubSub durability](https://developer.salesforce.com/docs/platform/pub-sub-api/guide/event-message-durability.html). Product-specific tariff/HS, origin, customs/PVoC, Incoterms, VAT, FX and licence facts require fresh, effective-dated specialist verification for each transaction. Neither assembling imported goods in ZA nor a UG farm reference proves preferential origin.

## 3. Reference businesses and testable transaction classes

| Reference | Relationship to Nabhold | Own operations | Cross-border scenario | Required profile selection |
| --- | --- | --- | --- | --- |
| **ZuriBeans Uganda / ZA** | Corporate relationship only with verified lawful mandates | Independent buyer, seller, sourcing, warehousing and importer/exporter per qualified market | UG→ZA coffee/vanilla, and separately qualified reverse/other corridors; direct UG export may bypass ZA importer | XB-CORE + XB-AGR + XB-LOG for physical exports; XB-NET only for independently qualified inter-tenant exchange |
| **BCU-like cooperative supplier** | No group membership presumed; contemplated co-ownership is **not concluded** | Aggregation, quality, produce sale, possibly processing; may subscribe separately | Supplies ZuriBeans; separately may serve its own overseas buyers | XB-AGR; XB-NET for independent customer onboarding/tenant exchange; XB-CORE/LOG when cross-border |
| **Kyagulanyi supplier** | No assumed group ownership or subscription | Exact legal form and sourcing capacity **unknown pending verification** | B2B or individual-producer supply as lawful; potential independent Baobab customer only after admission | Producer/counterparty identity and relationship; XB-AGR where product/process applies |
| **ZA-MFG-01** | Unrelated synthetic South African EXTERNAL_CLIENT | Imports components, BOM/production/QA/serialised inventory/AR | ZA→UG industrial pumps/equipment | XB-CORE + XB-MFG + XB-LOG; XB-NET when dual-tenant actors/providers are claimed |
| **UG-BUY-01 external** | Unrelated non-Baobab commercial buyer | Outside Baobab, its ERP/AP is **unobservable** absent authorised external evidence | Accepts ZA-MFG-01 goods through documented external exchange | CORE + MFG + LOG seller-side and external recipient; no foreign-ledger claim |
| **UG-BUY-01 tenant variant** | Unrelated COMMERCIAL external Baobab customer | Own tenant, IAM/CP context, optional qualified ERP/CRM | Bilateral qualified orders and independent GL/AP | CORE + MFG + LOG + NET where dual-tenant accounting is claimed |
| **Thamani Global / external carriers** | Thamani may offer logistics but **must never be mandated** | Logistics services; independent third-party carriers may be selected | Carrier booking/custody/POD for any eligible industry | XB-LOG if physical shipment/provider performance claimed |

**Transaction classes** are: LOCAL_DOMESTIC; EXTERNAL_CROSS_BORDER; INTERNAL_CROSS_MARKET_SAME_LEGAL_ENTITY; INTERCOMPANY_CROSS_MARKET_DIFFERENT_LEGAL_ENTITIES. Class does not decide legal actor or tax treatment. Movement of inventory between warehouses is not automatically a sale; commercial transaction direction is not the same as truck/ship/air route; an Incoterm does not by itself transfer title.

## 4. Domain vocabulary and bounded identities

| Term | Identity / authority | Dangerous conflation prohibited |
| --- | --- | --- |
| Canonical Organisation | CP-admitted, verified real-world organisation identity | Not tenant, legal actor, ERP Business Partner or CRM Account |
| Human natural person / producer | Appropriate identity and legal representation evidence; personal data minimised | Not automatically a corporate Organisation or blanket cooperative member |
| LegalEntity / lawful actor | Actual registered/legal entity and market/capacity evidence; CP projects mandates | Not inferred from website, brand, parent shareholding or PlatformAccount |
| Tenant / PlatformAccount | Separate SaaS resource and commercial-customer relationships | Not seller/importer-of-record or CRM account |
| CounterpartyRole / relationship | Tenant-owned SUPPLIER, BUYER, CARRIER etc., with qualifications and terms | Commercial relationship is not IAM access or CP CapabilityGrant |
| Cooperative membership / shareholder interest | Independently sourced membership/equity record, effective dates and rights | Membership ≠ beneficial ownership ≠ procurement mandate ≠ platform grants |
| CRM relationship / opportunity / contact | CRM provider's tenant-private engagement record | Not canonical identity, Trade order, KYB authority or ERP invoice |
| Trade lane / regulatory profile | Directed market/actor/product/date/permit/contract scope | Not route, tariff preference or customs clearance |
| Commercial order / invoice / ledger / settlement | Trade commitments; ERP financial truth; Payments/bank money execution | Each is independently authoritative and may disagree until reconciled |
| Lot transformation / BOM and genealogy | ERP/qualified process providers preserve inputs, outputs, quantities, losses and custody | A new lot/finished good does not prove origin eligibility |
| Document disclosure / external receipt | Trade Docs exact-version purpose-limited recipient grants; external acknowledgement | Document sent ≠ recipient accepted ≠ customs released |

### 4.1 Architecture (logical, no new mandatory engine)

~~~mermaid
flowchart TB
 subgraph Enterprise["Independent enterprises / external counterparties"]
  Z["ZuriBeans UG / ZA"]
  B["BCU-like cooperative / Kyagulanyi"]
  M["Independent ZA manufacturer"]
  U["UG buyer: outside or on Baobab"]
 end
 subgraph Experience["Authenticated enterprise experiences"]
  BX["B2B digital estates / partner APIs / optional cross-border workspace"]
 end
 subgraph Governance["Shared contracts + CP/IAM, not a universal business ledger"]
  SH["Shared identifiers / capability / events / evidence profiles"]
  CP["CP: actors / markets / tenants / bindings"]
  IAM["IAM: authentication / delegated principals"]
 end
 subgraph Engines["Independently authoritative domain engines"]
  CRM["Baobab CRM in ERP repo: relationship authority"]
  TR["Trade: RFQ / quote / native commitment"]
  ERP["ERP: PO / stock / transform / AR-AP / GL"]
  RE["Regulations: requirements / normative evaluation"]
  TD["Trade Docs: documents / controlled exchange"]
  TM["TMS / qualified carrier: movement / POD"]
  PAY["Payments / PSP: money execution"]
  PU["Pulse: advisory intelligence"]
 end
 Z --> BX
 B --> BX
 M --> BX
 U --> BX
 BX --> IAM
 BX --> CP
 BX --> CRM
 BX --> TR
 CRM -->|qualified opportunity handoff| TR
 TR -->|authorised consequence| ERP
 TR -->|scoped documentary request| TD
 TR -->|physical service request| TM
 RE -->|pin applicable decision| TR
 RE -->|require evidence| TD
 ERP -->|financial obligation| PAY
 PU -.->|advisory, non-authorising| RE
 SH -.->|contract/version conformance| Engines
 CP -.->|current scope grants, not business data| Engines
~~~

The **cross-border workspace** is a read/propose/authorise experience composed from source-owned projections; it is not another system of record and it never mints legal, customs, credit or payment authority. Unknown/stale information displays BLOCKED/UNKNOWN with source and next action; it does not become green from optimistic UI defaults.

## 5. Cross-enterprise transaction architecture

**Proposed Shared contract concept (NOT REGISTERED): CrossBorderTransactionCorrelation.** This is a small immutable linking/permission context, not an omni-transaction aggregate. A participating enterprise owns its own Order/PO/Invoice/AR/AP/CRM/private bank/stock; no common mutable economic record, inter-tenant database connection or cross-tenant global account master.

**Minimum proposed attributes:** opaque UUID; initiating verified Organisation; participating counterparty/Organisation references with individually evidenced roles; transaction class; effective market/corridor/product profile reference; requesting actor/authority reference; version; creation time; and scoped **disclosed external references**. Store no private contract price, PII, bank account, margin, raw native AD identifiers or complete document bodies. All participants independently authorise relationship/disclosure.

~~~mermaid
sequenceDiagram
 actor Seller as ZA manufacturer / seller
 participant CRM as Tenant CRM
 participant T as Trade
 participant CP as IAM + CP current authority
 participant E as Seller ERP
 participant D as Trade Docs
 participant R as Regulations
 participant L as TMS / carrier
 participant P as Payments
 actor Buyer as UG buyer (external)
 Seller->>CRM: Qualify relationship / opportunity
 CRM->>T: Intent / references (not order authority)
 Buyer->>T: RFQ / binding quotation acknowledgement
 T->>CP: Resolve seller/buyer, Market, mandate, scope
 alt Current authority denied or ambiguous
  CP-->>T: DENY / UNKNOWN
  T-->>Seller: No native commitment
 else Authorised
  CP-->>T: Time-bound decision
  T->>T: Atomic native commitment + idempotency
  T->>E: Authorised financial/stock consequence
  T->>D: Versioned contract / invoice disclosure request
  D->>Buyer: Scoped receipt / evidence delivery
  T->>R: Check corridor/product/date/origin requirements
  R-->>T: Sourced decision / blocked reason
  opt Requirements satisfied and qualified carrier
   T->>L: Authorised shipment request
   L-->>T: Authenticated POD/custody observations
   E->>P: Authorised settlement instruction (separate authority)
   P-->>E: Verified PSP/bank outcome and reconciliation
  end
 end
 Note over Buyer,E: External buyer ledger not asserted; only authenticated external evidence
~~~

### 5.1 Bilateral evidence rules (mandatory correctness correction)

| Party configuration | Baobab-authorised financial truth | Independently required external evidence | Allowed acceptance claim |
| --- | --- | --- | --- |
| Baobab seller ↔ **non-Baobab buyer** | Seller AR/revenue/COGS/FX/inventory where qualified and relevant | Contract/order/invoice acceptance, delivery/POD, actual bank/PSP settlement or accountable unresolved state | Seller financial consequences and externally evidenced exchange; **not buyer AP/GL** |
| Baobab seller ↔ Baobab buyer **without qualified ERP** | Seller consequences; buyer Trade relationship/ack only | Scoped buyer consent/receipt and other evidence | Seller-qualified business exchange, **not bilateral ledger** |
| Baobab seller ↔ independently ERP-qualified Baobab buyer | Seller AR/GL, buyer AP/GL/inventory separately from respective lawful contexts | Scoped documentary correlation, explicit buyer-side authorisation and independently sourced settlement | Bilateral financial reconciliation when both sides independently match |
| External seller ↔ Baobab buyer | Buyer AP/receipt/FX/payment where qualified | Seller invoice/source, shipment/custody, receipt and payment observations | Buyer-side accounting + external seller evidence; **not external seller GL** |

When an actual payment provider or customs authority is unavailable, the corresponding required provider evidence is **BLOCKED**, not replaced by a fabricated success. An external buyer does not have to become a Baobab tenant for ZuriBeans or a manufacturer to sell to it.

### 5.2 Distributed execution and failure

No global two-phase database commit spans Trade, ERP, TMS, customs and PSP. Each local consequential write MUST recheck native current authority and transact atomically in its own system, with durable outbox/inbox, idempotency and scoped external reference. Failures create **explicit compensating processes** owned by the source engine (cancel/reserve/rebook, credit/reverse invoice, customs hold, refund/dispute), never delete a historical ledger/document or replay an uncertain PSP charge blindly. A disputed legal decision cannot be overruled by Pulse; a cargo hold cannot be 'cleared' by a carrier ETA.

## 6. BCU/Kyagulanyi and cooperative continuity

**Real-world fact boundary:** BCU supplying ZuriBeans and contemplated future BCU co-ownership are business assumptions to verify; no completed JV, equity percentage, membership register, beneficial ownership, farmer consent or BCU SaaS subscription is asserted. Kyagulanyi's exact legal form, authority and relationship must be independently established; a natural-person grower and an incorporated supplier cannot be forced into the same Organisation model.

~~~mermaid
flowchart TB
 B["Verified existing party identity (Organisation or lawful person path)"]
 B --> S["ZuriBeans tenant-private SUPPLIER relationship"]
 B --> V{"Independently requests Baobab subscription?"}
 V -- No --> EX["External supplier portal / API / consented evidence only"]
 V -- Yes --> KYB["Authority-to-represent + existing-identity reconciliation"]
 KYB -->|ambiguous/hostile match| STOP["Manual independent review / DENY"]
 KYB -->|verified| ACC["Organisation Admission (CP)"]
 ACC --> PA["PlatformAccount / COMMERCIAL subscription"]
 PA --> TN["Own Tenant + current IAM/CP grants and providers"]
 S -.->|no automatic copying of pricing, KYB, contracts or secrets| TN
 TN --> SH["Only explicitly contracted bilateral disclosed facts"]
~~~

A supplier's independent tenant must **not** inherit ZuriBeans' supplier qualifications, account terms, market mandates, ERP AD_Client, CRM contacts or user access. Existing relationship records remain under their respective tenant's authority and retention. If verified identities refer to the same real entity, reconcile references and prevent duplicates; do not transfer ownership of another tenant's data.

Cooperative participation further separates member society, farmer, collection agent, cooperative legal representative, exporter and finance beneficiary. Member voting/equity, procurement agency, grower records and third-party lending/funding must have **distinct verified authority and privacy controls**. Proposed [SCF ADR-SCF-0031](https://github.com/baobab-platform/baobab-scf/blob/main/docs/adr/ADR-SCF-0031%20%E2%80%94%20Agricultural%2C%20Cooperative%20and%20Inclusive%20Supplier%20Finance.md) is deferred and grants no funder authority or bank disbursement.

### 6.1 Source provenance / transformation model

~~~mermaid
flowchart LR
 S1["Grower / cooperative verified collection"] --> L1["Origin lots: grade, weight, custody"]
 S2["Other verified supplier / farm"] --> L2["Origin lots: grade, weight, custody"]
 L1 --> AGR["Agricultural processing: drying / grading / milling / blending"]
 L2 --> AGR
 AGR --> EXP["New export lots with input-output genealogy, yield and QA"]
 M1["Imported industrial parts with import evidence"] --> BOM["Approved BOM / work order / WIP"]
 M2["Local parts"] --> BOM
 BOM --> FG["Finished goods + serials with costs and QA"]
 EXP --> RULE["Regulations: applicable source+origin evaluation"]
 FG --> RULE
 RULE --> DOC["Trade Docs: evidence, no inferred permit/clearance"]
~~~

**Do not model coffee drying as equivalent to industrial BOM assembly.** Both share provenance, quality, custody and quantity reconciliation but differ in inventory measures, transformation yields, valuation, origin rules and regulatory source requirements. A product-level 'coffee' field in a generic workflow is a smell; a totally abstract production engine with no domain-specific quality semantics is also a smell.

## 7. Baobab CRM — dedicated ERP-repository product-family architecture

CRM is a **commercial relationship product family inside baobab-erp repository**, alongside Baobab People, **not** a new repo/Engine or compulsory in-process iDempiere module. Explicit runtime separation and CP-governed provider selection are permitted. No provider monopoly: iDempiere relationship functionality, Salesforce and later qualified adapters must be interchangeable behind versioned semantics.

| CRM capability demand (candidate only) | CRM responsibility | Explicit non-authority |
| --- | --- | --- |
| Lead and qualification | Prospect source/consent, qualification, lead conversion request | Cannot canonically verify/incorporate an Organisation |
| Relationship engagement / contacts | Tenant-private contacts, interactions, opt-in/out, channel permissions | Cannot grant CP/IAM access or cross-tenant disclose |
| Opportunity / pipeline / forecast | Probability, stage, revenue estimate, industrial equipment or commodity pipeline | Won stage ≠ approved RFQ, committed order or invoice |
| Supplier/account 360 projections | Authorised composite of source-owned records only | Cannot overwrite ERP BP, KYB, CP legal actor or supplier qualification |
| Service cases / disputes / warranties | CRM case workflow; trade quality dispute/returns routed to domain owner | Case closed ≠ credit note, refund, customs release |
| Partner/cooperative engagement | Farm/field visit and cooperative representative relationship | Not farmer member registry, shareholder ledger, lending authority |

**Proposed, NOT REGISTERED Shared capability candidates:** crm.lead.manage; crm.opportunity.manage; crm.engagement.manage; crm.case.manage; crm.pipeline.read; crm.relationship-view.read. Formal naming/ownership/version and data classifications require an ERP/Shared ADR and catalogue approval. Avoid an ambiguous crm.account.manage that competes with CP Organisation, PlatformAccount and native ERP accounts.

~~~mermaid
flowchart LR
 CRM["CRM contract/adapter facade (baobab-erp repo)"]
 SF["Salesforce adapter"] --> CRM
 ID["iDempiere CRM/BP adapter"] --> CRM
 OT["Other qualified provider"] --> CRM
 CP["CP canonical Organisation + binding"] --> CRM
 IAM["IAM human/workload auth"] --> CRM
 CRM -->|authorised lead/opportunity refs only| T["Trade RFQ/quotation"]
 T -->|native commitment fence| E["ERP order/AR/AP/stock"]
 E --> P["Payments / separate money authority"]
 CRM -.->|no invoice or ledger posting| E
~~~

**CRM-to-Trade admission gate:** a CRM opportunity accepted by the buyer/seller workflow becomes a **proposal**, not execution. Resolve current party, tenant, legal entity, Market, currency/limit, contract/approval and buyer/seller IAM/CP authority *at Trade's consequential commit*, not solely at CRM stage conversion. Return the Trade transaction ID and denial reason to CRM via idempotent reconciliation. CRM may display but not override accepted Trade/ERP statuses.

**Salesforce adapter benchmark (not a default provider):** review current External Client App OAuth policy, object/field permissions, API and licensing quotas, API version, tenant-specific client credentials, REST/Bulk read/write and CDC/PubSub event integration; Salesforce event retention is finite (official Pub/Sub documentation describes a 72-hour retention window), so persist consumer offsets and detect/reconcile missed windows. Neither Salesforce object IDs nor iDempiere C_BPartner_ID may appear as canonical shared Organisation identifiers. End-to-end readiness requires *two heterogeneous provider implementations or justified adapter conformance* and tenant-specific data/consent isolation.

**ERP #116 scope decision:** retain as native manufacturing assessment with explicit CRM handoff dependency; track CRM qualification separately through proposed XB-CRM workstream, not by declaring ERP #116 completed or appending arbitrary CRM acceptance to native BOM tests.

## 8. Engine-level correction matrix

| Owner / product | New work imposed by EA-XB v1.1 | Required integration proof / current qualification caution |
| --- | --- | --- |
| Shared | Profile semantics/manifest, old→new case crosswalk, cross-enterprise correlation, external evidence receipt, contract/version authority | No automatic new CRM/manufacturing keys; existing L4 registry and historical XBE retained |
| CP | Existing-party admission, market/actor/relationship/related-party separation; runtime per capability and legal actor | Hostile identity claim, role inheritance, cross-tenant and missing legal actor denial |
| IAM | Supplier/partner/delegated representatives, step-up and revocation, independent organisational identity | Token alone does not prove current commercial authority |
| Trade | Supplier and buyer RFQs/quotes, buyer commitment fencing, party-local orders and external partner correlation | No B2C bypass, replay or seller/buyer authority substitution |
| ERP / CRM / People | Independent finance/manufacturing/agricultural process, BP projections, CRM relationship provider, workforce only | Actual native iDempiere 13+PG17 data/posting, provider separation; payroll not a trade settlement |
| Regulations | Direction/product/actor/effective-dated jurisdictional packs, provenance for origin, SPS, industrial conformity | UG→ZA coffee profile **does not** qualify ZA→UG equipment |
| Trade Docs | Exact-version declarations/evidence, purpose-limited disclosure, receipt and revocation | Proposed ADR-TDOC-0018 requires acceptance and real-provider qualification |
| TMS | Neutral carrier selection, booking, multiple legs, custody/POD and exceptions | Thamani must not be hard-coded as carrier or required logistics tenant |
| Payments | Cross-border currency/beneficiary/PSP outcome and ERP reconciliation | Sandbox payments are NOT real movement; no blind retry |
| Pulse | Market research, FX/commodity intelligence, estimates and source confidence | Advisory only, never origin/customs/credit enforcement |
| Subscriptions | COMMERCIAL products/entitlements for BCU, independent ZA firm and other customers | Subscription does not create legal actor or capability grant |
| CMS / Digital Estates | Optional user experience and scoped product content | No DigitalEstate required for external tenant or external buyer |
| SCF | Future agricultural, inventory and supplier financing evidence integration | Proposed/deferred; no lender or funding claim without qualified partner |
| Infrastructure / baobab-dev | Cross-repo real-component harness; tenant/market source pins, negative/replay/teardown | CI green != protected certification; retain per-provider and per-execution trust class |

## 9. Acceptance-profile design and migration

The [proposed machine-readable profile inventory](ea-xb-v1.1-proposed-acceptance-profiles.json) defines:
- **XB-CORE:** mandatory for every cross-border *business-execution* qualification, including seller-side accounting/settlement, external participants, current legal actor/commit/document/regulatory truth, isolation and failure recovery.
- **XB-AGR:** source provenance, commodity collection and lot processing, corridor-specific agricultural origin/SPS/quality.
- **XB-MFG:** effective BOM/routing, WIP/production/quality/genealogy/real native costing, manufactured-origin evidence.
- **XB-NET:** verified counterparty-to-tenant continuity, relationship isolation, bilateral financial proof *only when independently qualified on both sides*, heterogeneous providers.
- **XB-LOG:** carrier qualification, shipment/movement, custody/POD, cost/exception reconciliation where physical movement is claimed.

### 9.1 Applicability rules — no accidental global block

| Claimed business outcome | Required profiles | Not implied |
| --- | --- | --- |
| ZuriBeans UG→ZA coffee shipment | CORE + AGR + LOG | Any other corridor, origin preference, manufacturer BOM, buyer ERP, Nabhold roll-up |
| ZA-MFG-01→UG equipment shipment | CORE + MFG + LOG | Coffee SPS pack, mandatory Thamani carrier, actual manufactured-origin preference |
| BCU-like supplier becomes independent Baobab customer (without shipment) | NET: XBN-01..03 only, with normal CP admission/identity gates | A cross-border execution PASS or group access |
| BCU-like Baobab tenant sells cross-border to another qualified Baobab tenant | CORE + AGR (if agricultural lot) + NET + LOG (if physical movement) | Globally shared CRM/order/ledger, automatically valid intercompany pricing |
| Independent freight provider delivery | LOG for its service claim; CORE added if claiming **whole cross-border trade execution** | External trader's ERP or customs/legal compliance without evidence |
| ZuriBeans R0 public website | Own CMS/digital-estate launch gates, not EA-XB | Trade or payment production acceptance |

**Machine applicability is authoritative, not a prose exception.** Each of the five reference scenarios declares a closed set of boolean `claims`, the ordered `applicable_case_ids`, and a reasoned `excluded_cases` partition covering all 30 IDs before any run. Each case has a pinned `required_when_all` predicate. The validator independently computes the required cases and rejects omissions, duplicate IDs, unknown/non-boolean claims, changed reference scope and exclusions that hide mandatory cases. `required: true` means mandatory **when applicable**; excluded cases have no execution result and confer no PASS or whole-profile qualification.

The onboarding-only reference requires XBN-01..03. XBN-04 applies only to claimed independently qualified bilateral accounting, XBN-05 to heterogeneous providers and XBN-06/07 to actual CRM use/handoff. The two bilateral reference transactions explicitly claim all these capabilities and must prove them. CORE is mandatory for cross-border execution; XBC-06's positive non-tenant exchange applies to the external-buyer variants, while the dual-tenant variants still retain CORE isolation and negative evidence. CRM is optional: XBC-02 always proves the native commercial fence, and XBN-07 separately proves CRM admission. Agriculture processing and cooperative representation are explicit claim predicates; a different corridor or product needs a separately reviewed manifest, never a reversed commodity rule pack. Missing evidence for an applicable claim is BLOCKED/NOT_RUN; changing facts after a failure cannot turn it into exclusion.

The coffee reference is explicitly the non-tenant-buyer variant. The cooperative export and manufacturer dual variants cover independently qualified bilateral evidence. Neither substitutes for another's evidence. The historical 18-case manifest is retained byte-for-byte; accepted v1.1 composition governs future claims, while historical validators remain historical design checks.

Each profile is evaluated at **exact** market direction, product/tariff classification, legal seller/importer/exporter, counterpart configuration, qualified provider/version, effective time and evidence class. A different profile/corridor cannot be masked by an aggregate green metric.

### 9.2 Historical case reconciliation

The prior XBE-01..18 design inventory MUST remain byte-preserved for historical source and its checker may continue to validate its historical 18 mandatory scenario descriptions. **Upon the reviewed v1.1 acceptance merge**, the new profile inventory becomes authoritative **for future new qualification claims only**. Every old ID has an exact owner-reviewed mapping; old receipts (if any) remain attached to their original case, evidence class and timestamp. No historical PASS inferred. XBE-15 explicitly maps to (a) seller-side qualified accounting in CORE and (b) independently qualified dual-party accounting in NET; the external-buyer variant does NOT pretend to assert buyer AP. XBE-08/09 remain mandatory for MFG, not AGR. The original Shared L4 scenarios are untouched.

**Acceptance dimensions:** ARCH, CONTRACT, SOURCE, CI, CONNECTED-SYNTHETIC, EXTERNAL-SANDBOX, PROTECTED-STAGING, REAL-LEGAL/PROVIDER, OPS-GO. Do not combine them into a single numeric percentage or automatically promote a lesser trust class. Each mandatory applicable case has independent positive and negative receipts; missing critical evidence is BLOCKED/NOT_RUN, never SKIPPED as PASS. An explicit applicability decision is recorded *before* an execution run and reviewed; owners may not mark cases N/A to evade failing negatives.

## 10. Rollout and controlling evidence

~~~mermaid
flowchart TD
 A["Review EA-XB v1.1 proposal; approve or request revision"] --> B{"Platform Owner accepts?"}
 B -- No --> HOLD["Keep v1.0 Accepted; proposal only; no merge"]
 B -- Yes --> C["Shared profile/semantic ADR and conformance contracts"]
 C --> D["CP existing-party admission + Shared transaction refs"]
 D --> E["Trade Docs scoped exchange + CRM adapter authority"]
 E --> F["Parallel engine proof: AGR sourcing / MFG production"]
 F --> G["Regulations: each direction/product corridor pack"]
 G --> H["TMS / PSP independent provider qualification"]
 H --> I["Connected physical and financial business outcomes + negatives"]
 I --> J{"Every applicable profile PASS at required trust level?"}
 J -- No --> BLOCK["Scoped BLOCKED; no unsupported production claim"]
 J -- Yes --> GO["Independent protected legal/provider/ops approval per corridor"]
~~~

| Phase | Owner | Concrete artifacts and proof | Required negative evidence |
| --- | --- | --- | --- |
| A / Shared design reconciliation | Shared / Platform Owner | Approved ADR, complete old-case crosswalk, manifest schema/CI; no old L4 changes | missing profile/case/source, fabricated PASS rejected |
| B / Authority and enterprise continuity | CP, IAM, Subscriptions | Existing-party resolution, independent tenant without estate, verified representation, current role/market grants | duplicate/hijack, self-asserted identity, inherited group access |
| C / Commercial and evidence exchange | Trade, Trade Docs, Shared | Transaction correlation, authoritative quote/commit, disclosed document/version/receipt, contract/schema pins | stale mandate, B2C fallback, wrong recipient or leaked version |
| D / CRM and industry processing | ERP CRM, ERP manufacturer, ZuriBeans supplier/ERP | Independent CRM provider audit/handoff, agricultural lots, real iDempiere BOM/WIP/Fact_Acct | stage-won != commit, bad lots, stale BOM, double-post or wrong client |
| E / Jurisdiction and external providers | Regulations, Trade Docs, TMS, Payments | Two distinct effective-dated corridors, externally authenticated customs/carrier/PSP integration | invented tariff/origin/permit/POD/PSP outcome |
| F / Enterprise qualification | Infrastructure, all domain owners, independent reviewers | One eligible corridor/actor/product/provider evidence bundle with positive/negative/replay/restore/teardown | cross-tenant leak, fake foreign ledger, unreconciled partial failures |

**Mandatory receipt contents:** case/profile/variant ID; exact actor, role, Tenant (if any), legal entity, Market, direction, product, versioned effective rule, counterparty type; source SHA and artifact/image digest; provider ID/version/qualification; real issuer & current CP decision/expiry; event/document reference; idempotency replay result; native transaction readback, independent external receipt; redacted log hash, observed result, reviewer, teardown/restore status and explicit BLOCKED reasons. Never publish credentials, sensitive farmer/bank data, tax IDs or signed customs originals.

**Architecture approval ≠ operational approval.** An independently qualified public website may launch before XR cross-border execution, but must never advertise unqualified live trade capability. External provider/relevant market legal clearance must be real and current.

## 11. ADR/issue package for owner review

This acceptance approves programme design only. Do **not** assign new Accepted ADR numbers or change domain ADR/provider statuses from this design. Those decisions retain their own reviewed owner changes. Suggested owning decisions, with numbers assigned only after register review:

| Repository / proposed decision | What must be decided and approved | Dependency |
| --- | --- | --- |
| Shared: composable EA-XB profile & evidence authority | D1, D2, scenario/variant applicability, legacy XBE→new mapping, audit receipts | Accepted #411; canonical L4 unchanged |
| Shared + Trade + Trade Docs: bilateral correlation and evidence exchange | D3, canonical reference/version, disclosure receipt/authorised distribution; event namespace separately accepted | Trade ADR-0019; TDOC-0018 Proposed |
| CP + IAM: existing-counterparty admission and lawful representation | D4 with privacy, legal actor and anti-hijack safeguards | BCP-014/017/018; existing supplier identities |
| ERP + Shared: Baobab CRM product family / provider-neutral adapters | D5; CRM ontology, provider routing, Salesforce/iDempiere port, CRM-to-Trade fence | ERP-023 People co-location precedent; ERP #116 handoff |
| ERP + Shared: transformation evidence, costing, lot/BOM semantics | D6; shared provenance envelope and *distinct* AGR/MFG processes | ERP #116, native posting authority |
| Regulations: effective-dated corridor product pack composition | D7's regulatory dimension; UG→ZA commodity and ZA→UG equipment separately | REG-0027 Proposed, sourced customs/standards review |
| Trade Docs: approve/implement cross-organisation disclosure | Exact-version grants and receipt/revocation and retention | TDOC-0018 Proposed, legal/privacy counsel |
| TMS / Payments / Infrastructure: actual provider and acceptance gates | Physical custody/POD, payment settlement, replay/teardown | Domain provider qualification and protected acceptance |

**ERP #116 explicit companion recommendation:** leave ERP #116 open as the real-iDempiere manufacturing/costing native veto assessment. Link a separate CRM issue and state that XB-01 cannot be treated as complete CRM qualification. No ERP #116 scope or issue body is modified by this Shared proposal.

## 12. Risk and open-decision register

| Risk / unresolved decision | Severity | Required next authority | Default safe state |
| --- | --- | --- | --- |
| External buyer AP/GL treated as Baobab-certifiable | Critical | Shared/ERP/Trade owners | Buyer accounting UNOBSERVABLE; seller-side only |
| Manufacturer WIP blocks qualified agricultural corridor | High | Shared / Platform Owner | Profiles independent; historical XBE not deleted |
| Supplier identity hijacked through supplied Organisation UUID | Critical | CP/IAM + legal admission reviewer | DENY pending verified representation |
| BCU contemplated shareholding silently grants seller/admin rights | Critical | Corporate legal + CP governance | No ownership or cross-tenant grants assumed |
| Kyagulanyi person/organisation legal form guessed | High | Supplier KYB/authorised legal actor owner | UNVERIFIED; no fabricated incorporated entity |
| CRM Opportunity Closed Won creates Trade/ERP commitment | Critical | ERP CRM + Trade + CP owners | No commitment without current native execution authority |
| Imported components assumed to confer AfCFTA origin | Critical | Regulations + relevant official rules/customs experts | UNKNOWN/BLOCKED |
| Customs document generated treated as authority release | Critical | Trade Docs + competent external authority | NOT_RELEASED |
| Shipment status sent by unqualified provider | High | TMS provider qualification | BLOCKED |
| ERP payment record treated as bank settlement | Critical | Payments / ERP / PSP evidence | UNCONFIRMED; reconcile before retry |
| Direct cross-tenant data sharing or platform-owned shadow ledger | Critical | CP/IAM/Trade Docs/Shared | DENY; tenant-local sources only |
| Customer launch blocked by unrelated manufacturer acceptance | High | Platform Owner / release owner | Release gates independently scoped |

## 13. Reviewer acceptance checklist

- [x] Retain the founding objective: cross-border **execution**, not only SaaS onboarding.
- [x] Preserve ZuriBeans R0/R1/R2/R3 and Uganda/South Africa bidirectionality.
- [x] Preserve all 18 historical XBE IDs and all canonical L4 case meanings.
- [x] Approve independent CORE, AGR, MFG, NET and LOG profiles and their applicability rules.
- [x] Approve explicit non-tenant buyer evidence and prohibit unsupported foreign GL claims.
- [x] Approve immutable correlation plus purpose-limited, exact-version, receipt-based document exchange.
- [x] Approve lawful existing-counterparty admission without identity duplication or inherited access.
- [x] Confirm BCU potential co-ownership and Kyagulanyi legal form remain unverified.
- [x] Keep Baobab CRM inside ERP repository, separately qualified and provider-neutral.
- [x] Confirm manufacturing and agricultural processes share provenance primitives, not false equivalence.
- [x] Require official effective-dated origin/customs/product requirements per direction and product.
- [x] Require owner-reviewed ADRs and current-qualified TMS/PSP/Regulations before production claims.
- [x] Record the Platform Owner’s conditional merge authorisation; require satisfactory corrected final-head review and green CI before merge.

---

**Accepted design end-state:** EA-XB v1.0 remains the historical Accepted cross-border-execution objective. EA-XB v1.1, **effective upon reviewed CI-green merge**, corrects business-outcome *composition, external evidence semantics, independent-enterprise continuity and CRM inclusion* while keeping enterprise-domain authority, real-component testing and independent approval intact. No real-world BCU/Kyagulanyi JV, incorporated company, regulatory decision, payment, shipment or provider qualification is asserted.
