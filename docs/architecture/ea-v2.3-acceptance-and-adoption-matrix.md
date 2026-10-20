# EA v2.3 — Product, engineering and cross-ADR acceptance / adoption matrix

**Status:** Accepted programme acceptance companion to [EA v2.3](EA-implementation-plan-v2.3-2026-10-20.md), 20 October 2026.
**Evidence class:** Designated acceptance obligations; not a record that the listed execution receipts already exist.
**Architecture:** ADR-SHARED-036–041, existing Shared/engine/estate accepted owner decisions, Nabhold Go-Live v2.0.
**Important:** The [v2.2 integration matrix](ea-v2.2-integration-acceptance-matrix.md) remains the **single authoritative registry** for all L4-MAN/IAM/CP, NAB, FIN/EVT/REC and INT-01..08 scenario IDs. This file adds *non-L4 programme acceptance rows* only, and SHALL NOT be used to replace, rename, disable or mark an L4 case NOT_APPLICABLE.

## 1. Evidence and source truth

Each row records **ARCH**, **CONTRACT**, **SOURCE**, **CI**, **L4** (only when relevant), **STAGING**, **EXTERNAL** and **OPS/GO** independently, using YES/PART/NO/EXT/N/A and stable links. A source PR head is a candidate, not SOURCE_MERGED. A candidate source-upgrade or image tag does not equal schema/data migration. An Accepted ADR does not independently confer CURRENT grant, legal mandate, work permit, statutory compliance, active provider, real revenue, shipment, financial transaction or support.

| Gate/receipt | Product/engineering obligation | Owner and prerequisite | Mandatory positive proof | Mandatory negative/failure proof | Admission threshold at audit |
| --- | --- | --- | --- | --- | --- |
| **EA-R00-V23** | Accepted EA v2.3, cross-repo 20-source audit, current register, index and approval | Shared/Platform Owner; all docs in one reviewed PR | New plan and audit commit on `shared/main`; CI and review fully complete | Stale v2.2 queue/status cannot remain advertised as live; no source completion inferred | Planned until merged |
| **ENG-01** | Organisation repository census and engineering capability classification | Shared + Platform Engineering; ADR-041 | All discoverable first-party repos including `baobab-*`, estates, templates, Infra and Shared classified by exact SHA, owner, legacy drift, source/ADR maturity | Missing/private-unreadable repo recorded unknown; cannot silently count as conforming | PART (20 repo audit; local quality reviews outstanding) |
| **ENG-02** | Repo-local engineering philosophy adoption | Each of 20 audited repo owners + future repos | Link Accepted ADR-041 and review significant feature PRs against adopt/adapt/re-engineer/build decision and accepted authority | Missing local link, copied proprietary source, invalid GPL assumptions, security bypass or fabricated QA not called passed | NO for cross-repo rollout; Shared baseline YES |
| **ENG-03** | Scoped maintainability/toolchain/DRIFT remediation | Each owner; ENG-01/02 | Tested fix for the selected material gap with source comments, contracts and compatibility | CI bypass or unreviewed blanket rewrite/Node major/database image swap forbidden | PART discovery only |
| **ENG-04** | Foundation conformance policy rollout | Shared Foundation + Dev tooling + affected maintainers | Opt-in reporting; later accepted narrow check with false-positive/exception migration evidence | Repo blocked merely for missing retroactive cosmetic motto, false compliant status or missing private visibility | NO |
| **ENG-05** | Continuous independent African enterprise quality | Product/engine owners, QA and customer research | Usability, accessibility, reliability, interoperability, price-to-operate and local legal relevance benchmarked with evidence | Unsupported ranking or claimed market-leader status from source merges alone | NO |
| **BXS-01/02** | Shared experience architecture/tokens | Shared Experience; ADR-040 | Source and exact published version/digest, accessible semantic tokens, validated brand aliases | Mixed brand tokens, unexpected theme inheritance or unreviewed exports | PART |
| **BXS-03/04** | Geo and accessible first-party primitives | Shared Experience, estates | Proper geography accuracy, a11y, SSR, keyboard/focus, controlled dialogs/tabs, optional map/WebGL fallback | Sourced vs estimated location confused, screen-reader failure, forbidden tile origin, PII exposed in overlays | PART |
| **BXS-05** | Consumer package release and browser experience | Nabhold/CP/ZuriBeans/Thamani, Shared publisher | Exact registry artifact and pinned consumer, real browser/mobile/AT/performance and server BFF role grants | Only source/Storybook screenshot, CDN link or obsolete consumer lock used as provider/production acceptance | PART |
| **BGX-Thamani** | Logistics B2B customer/partner interactions | Thamani + TMS + CMS/IAM/CP; owner ADR-THA-0018 | B2B organisation legal buyer, explicit actor, source-backed quote/booking/tracking + current binding and provenance | Legacy B2C checkout used as B2B evidence; made-up carrier, route, ETA or Customs release; sibling leak | BLOCKED by TMS runtime |
| **TMS-FND** | Headless transport provider tech/domain admission | TMS owner + Shared/CP/IAM | Accepted scoped TMS ADRs, executable service/PG17 as approved, actual context/tenant/role and durable transport domain fixture | Merged Proposed ADR treated as live provider; external carrier assumed from mock | NO |
| **LOG-01..05** | Shipment, carrier booking/tracking and regulated corridors | TMS, Thamani, Docs, Regulations, payments | Actual provenance/versioned shipment/consignment, carrier verification, event replay, customer/corridor/legal acceptance | Fabricated events, stale shipment, no tenant grant, duplicate booking, carrier credential leak or silent ETA certainty | NO |
| **INT-03-NAB** | Real connected Nabhold human IAM/CP/BFF/CMS lab | Infrastructure/Nabhold/IAM/CP/CMS; INT-01/02 | Full relevant existing canonical L4/NAB scenario PASS with issued token, current context/binding, TLS Redis/PKCE, published and preview CMS, frozen manifests and teardown | Revoked/wrong audience, inactive client, missing grant, cross-tenant preview and partial CMS denied; no identity/cert inference | NO (Infra #37/Nabhold #77 open) |
| **INT-07-API** | Independent external API-only consumer | Infrastructure/IAM/CP/selected certified provider | Real unrelated EXTERNAL_CLIENT synthetic current right and resource call with **zero** DigitalEstate rows | Synthetic group privilege, forced fake estate, wrong recipient/market, revoked audience, cross-tenant leak | NO |
| **EA-R03-ERP** | Native protected ERP posting with class-specific legal controls | ERP/CP/Shared, ADR-034/037/038 | Actual iDempiere COMMIT with approved current CP mapping, independent payment-execution provenance where relevant, balanced journal | Bank/cash, unclassified inventory/cost/manufacturing, stale actor or unauthorized payment denied **at native execution point** | PART native ERP-A/B; external/protected NO |
| **EA-R03-Trade** | Native sale/order and seller operating bindings | Trade/CP/Shared, ADR-039 | Authorised merchant/seller/market legal role and at-commit order/canonical obligations persisted | Cart-only fence, unactivated binding, admin/native flow, bypassed PEP, expired actor, duplicated order denied | PART |
| **EA-R03-Payments** | Independent money movement lifecycle | Payments + CP/IAM/PSP/Finance | Correct legal/merchant/processor/market mandate and actual authorised PSP outcome with reconciliation | ERP receipt as payment right, self-approved payout, duplicate/refund/replay, wrong merchant/funder/corridor and unknown status handled | D1 PART, D2/production NO |
| **FIN-F1** | Corporate finance source/contract and live ledger | Shared/ERP/Finance; ADR-033 currently Proposed | Accepted relevant finance schema/capability, actual iDempiere current provider, reconciled trial balance and denied restricted salary read | DRAFT F1 declared accepted or group-share grants issued | NO certified provider |
| **BP-00** | Baobab People/PG17 architecture and source baseline | ERP PR #110; ERP/Platform reviewer | Reviewed ERP ADR-023 merged, Gate D mandatory CI green, actual PG17 source defaults/runbook | Permission denied exit 126 skipped as green; PG17 image mistaken for migrated 16 volume | NO (open PR with failed Gate D) |
| **BP-01/02/03** | CDSoftware provenance and iDempiere 13 functional proof | ERP People; source licence and PG17 compatibility | Actual source SHA/SPDX/manifests/deps, build + OSGi resolve + 2Pack + real iDempiere 13/Java17/PG17 synthetic pay run; test rollback | Wiki evidence claimed v13 ready; copied source automatically proprietary; unsupported core fork | NO |
| **BP-04** | Canonical workforce/payroll provider | ERP/Shared/CP/IAM; Shared decisions first | Accepted People capabilities, current grants, sensitive HR PEP, maker-checker and approved result accounting | Cross-employer employee leak, self-approval or payroll alone executing bank payout | NO |
| **BP-05 ZA / 06 UG** | Effective-dated country payroll localisation | ERP, Regulations evidence, qualified ZA/UG tax/payroll reviewers | Independent legal-source coverage, historical and current golden vectors, errors/refunds/filings, practitioner acceptance and parallel run | AI rule automatically promoted, wrong tax year/jurisdiction, guessed social contribution or withholding | NO |
| **BP-07** | Baobab People commercial tenant admission | ERP product, CP, Finance, Subscriptions and Security | Qualified customer contract/support, per-jurisdiction certified provider, compliant release and isolated payroll flows | Global "Africa payroll compliant" flag without country proofs | NO |
| **RTD-Reg-Pulse** | Documentary regulatory knowledge/provider composite | Trade Docs/Regulations/Pulse and Shared | Source-owned evidence, actual deterministic legal requirement and independently typed document state, nonauthorising intelligence | AI extraction/estimate as legal official decision, missing authority, direct database joins, fake Customs output | PART reference, real services/provider certifications NO |
| **SCF-FND** | Conditional partner-led financing feasibility | SCF owner, legal/funders, Shared/Payments | Signed role/licensing evaluation, approved case evidence boundary, source-backed independent funder product decision | Proposed charter as finance licence, auto credit, funding or lending provider | NO; not R0/INT-03 blocker |
| **TOOL-01** | Current devcontainer/Node/PG safety and template | baobab-dev, Infra, Shared/Foundation, owners | Exact pinned image, compatible toolchain, documented 16→17 physical DB migration, current org repo paths, new engine template acceptance | Stale `nabhold/` paths, unchecked Node 26 bot bumps, changing image on PG16 volume, secret leak | PART |
| **EA-09B-GO** | Protected actual staging + live independent GO | Infra/Security/CP/IAM/domain/legal/vendor owners | Authenticated real env, exact deployed digest/approved roles, monitoring/restorable backup, current provider/legal/market actor and signed release | Synthetic Actions, fake credentials, screenshots or unverified PSP/carrier/funder as protected live | NO |

## 2. Critical path rule

**Current P0:** INT-03 real IAM/CP/BFF/CMS; real legal-actor/custody; native Trade/ERP/Payments guards; INT-07 external API-only; actual AWS protected staging prerequisites. **Parallel P1:** BXS consumer/published-package/quality, ADR-041 local engineering adoption and toolchain risk, TMS-B2B first provider, ERP People BP-00/01 then eventual ZA/UG qualification, Regulations/Docs/Pulse production provider readiness. **Deferred/optional:** SCF until legal/funder/product gate.

A blocked People country pack does not block INT-03. A blocked TMS carrier does not block unrelated ZuriBeans/ERP source engineering. A funded live SCF operation is prohibited without independent legal/partner/Payments control regardless of a green workflow.

## 3. Per-PR minimum immutable evidence fields

```yaml
work_item: <programme-id>
owner: <actual-repository-and-approver>
governing_adr: <accepted-adr-references>
decision: <adopt|adapt|re-engineer|build-independently|not-applicable>
source:
  candidate_head_sha: <full-git-sha>
  merged_main_sha: <full-git-sha-or-NOT_MERGED>
  contract_pin: <full-git-sha-and-schema-version-or-NOT_APPLICABLE>
  image_digests: <explicit-immutable-list-or-NOT_BUILT>
  database_migration: <id-and-actual-status-or-NONE>
checks:
  mandatory_ci: <specific-run-ids-and-conclusions>
  local_suite: <test-and-actual-runtime-details>
  l4_receipt: <canonical-scenario-ids-and-digest-or-NOT_RUN>
assurance:
  protected_staging: <named-actual-observation-or-NOT_EXECUTED>
  legal_or_provider_certification: <independent-authority-evidence-or-NOT_GRANTED>
  production_go: <signer-and-scope-or-NOT_AUTHORISED>
open_blockers: <ids>
rollback: <rehearsed-plan-or-specific-limitation>
```

This template illustrates what must be recorded; it does not create a canonical machine schema or a new capability namespace. Never commit tokens, taxpayer records, payroll PII, credentials or private certificates as evidence.

## 4. Acceptance and change control

The Platform Owner approves workstream sequencing through Accepted EA v2.3; **no domain's execution authority is transferred by these rows**. Shared owns the L4 canonical scenario registry and contracts, CP owns current grants/provider bindings, IAM owns credentials/issuance, each domain owner owns execution and appropriate expert reviewers own independent legal/PSP/carrier/payroll acceptance.

Owners may extend this *companion* matrix for product/engineering work while preserving evidence history. New common L4 scenario identifiers, capability keys, actor roles or Shared contract semantics require an independently accepted Shared decision and consumer conformance—not a silent row rename.
