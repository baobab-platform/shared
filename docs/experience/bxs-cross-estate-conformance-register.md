# BXS cross-estate conformance register — BXS-CXP v1.0

**Governing authority:** Accepted ADR-SHARED-040 §7.1; owner: Shared BXS architecture.  
**Record class:** Initial source inspection and consumer-adoption inventory (2 November 2026). **NOT** independent browser rerun, brand approval, protected staging or production certification.

## Profile interpretation

- **Mandatory BXS-M01..M08** apply to every first-party frontend. Framework-neutral outcomes apply to Django as well as React. Required means verified quality, not every package installed.
- **Conditional BXS-C01..C07** apply whenever their capabilities are actually delivered. NOT APPLICABLE requires feature inventory evidence, not an assertion that Shared is not imported.
- **Estate-owned** identity/typography/logo/layout/content/journeys stay with the owning product. Estate-owned is not exempt from Mandatory or triggered Conditional requirements.

## Observed, not certified, starting point

| Consumer | Observed implementation at audit | Mandatory/conditional verification outstanding | Product-owned distinction |
|---|---|---|---|
| Nabhold | Published tokens + Geo Core; institutional public layout, SVG editorial map, local Base UI; corporate chart and dashboard | Reconcile direct shared UI reuse and chart source/null contract; finish public quality parity consumer evidence in Nabhold #99; authoritative CMS/role and protected validations remain separate | Corporate gold/ink identity; group portfolio and editorial investment UX |
| ZuriBeans | Published tokens + UI; local Base UI and substantial public interaction/visual/axe/Lighthouse gates; full six-package BXS proposed in #147 | Qualify exact #147 head with all required checks and independently reviewed screenshots; retain buyer/supplier segregation and brand evidence | Figma-led B2B commodity trade house |
| Thamani | All six packages on main following merged #46; read-only chart/map/overlay presentation, synthetic shipping workspaces and public quality gates | Real provider/CP/IAM/TMS and approved MapLibre runtime remain out of scope; verify final consumer evidence separately; approve logistics brand | Distinct B2B transport/logistics experience |
| Equator & Estate Co. | Legacy Django template/Bootstrap site without BXS direct packages | Repair broken placeholder navigation/content; choose architecture, record theme and establish framework-neutral quality gates; do not force React adoption | Property and real-assets identity and workflows |
| baobab-cp | Published tokens + UI, mainly nonproduction design-system demonstration; locally owned Base UI Console components and Go/Next contracts | Actual protected Console browser accessibility/visual/performance and native-authority negatives; no UI badge substitutes for CP checks | Administrative context, approval, organisation/tenant and operations UX |

These observations SHALL be replaced by current source and test receipts per consumer; no row is marked VERIFIED by this initial document.

## Required consumer record schema (one record per control and affected surface)

| Field | Meaning |
|---|---|
| consumer / surface / framework | Exact deployable app, public/privileged route profile, technology |
| control_id / category / applicability | BXS-M01..M08 or triggered BXS-C01..C07; conditional absence explanation if N/A |
| accountable_owner / approvers | Technical, design/brand and security/domain owners as appropriate |
| approved_theme / pinned_packages | Design sign-off plus name, version, lock/digest; package absence allowed when justified |
| source_head / environment / evidence_class | Commit SHA, controlled test environment, source/unit/browser/real-component/protected evidence class |
| reproducible_receipts | Immutable CI URLs, browser/version/tool profile, screenshots and manual AT review |
| assessment / review_date | NOT ASSESSED, IN PROGRESS, VERIFIED, NONCONFORMING, NOT APPLICABLE (Conditional only), EXCEPTION APPROVED |
| findings / remediation / due_date | Concrete drift, responsible fix and next review |
| exception_id / expiry / compensating_controls | Required for EXCEPTION APPROVED, including security approval when relevant |

## Governance and release rule

A package install or Shared release SHALL NOT automatically change this register to VERIFIED. Reviewer must see the **current consumer head SHA**, exact package versions, appropriately scoped tests and evidence class. CI success establishes only its covered gates; verified development source does not certify production authorisation. Before a protected deployment, independently enforce the applicable estate, IAM/CP, provider, security and environment controls. Reconcile records at each consumer adoption PR and at least quarterly; document exceptions with approval and expiry.

This register is intentionally an **evidence template**, not a fabricated compliance matrix.