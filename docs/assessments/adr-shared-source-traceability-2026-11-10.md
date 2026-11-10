# Shared ADR source traceability and external-qualification register (001–045)

**Audit date:** 10 November 2026. **Pinned source baseline:** `2a2ac16a26e0c217875002f25d7f00e181cf8c5b`.

## Scope, methods and limitations

All numbered Shared decisions 001–045 have been located and read for scope, decision status, amendment chain, intended source contracts and owning runtimes. This is an **artifacts and boundary audit**, not an end-to-end assertion that every ADR's invariants execute. The accompanying machine-readable register names one primary source artifact and one **related** source check per decision where available. The check's existence **does not** establish full conformance of every clause, nor does it imply that a consuming repository is pinned to the audited revision. Current source contracts were checked against the main tree; historical decision approvals have not been changed.

Baseline classification: **44 accepted decisions, 1 proposal (ADR-SHARED-033)**. The first six predate the `ADR-SHARED-*` filename convention and retain historic `ADR-0001`…`ADR-0006` identifiers. The source register is evidence inventory, not compliance certification.

## Identified corrective implementation work

- **ADR-001/003:** missing strict first-party identity-registry schema and semantic negative fixtures; isolated implementation in [shared #446](https://github.com/baobab-platform/shared/pull/446). It guards Shared declarations but not CP's legal-actor runtime.
- **ADR-006/010:** stale Organisation ownership, event count and broker claims in supplier docs; correction in [shared #447](https://github.com/baobab-platform/shared/pull/447). Supplier KYB and ERP projection still need hosting-estate/runtime evidence.
- **ADR-033/044:** the ADR index omitted both documents despite their presence. This PR indexes them, preserving 033 **Proposed**, and adds an inventory-completeness regression test to the existing EA-governance CI suite.

## Decision-by-decision source inventory

| ADR | Topic | Decision | Verified Shared source | Related source check | Downstream qualification still required |
|---|---|---|---|---|---|
| `ADR-0001` | Digital Estate architecture | ACCEPTED | `contracts/tenancy/tenancy.yaml` | `scripts/validate-governance-contracts.rb` | CP / digital estates: current boundaries and consumer adoption |
| `ADR-0002` | Control Plane polyrepo boundaries | ACCEPTED | `README.md` | `.github/workflows/foundation-repository-gates.yml` | CP / Infrastructure: no owner bypass |
| `ADR-0003` | Tenant / Legal Entity / Estate separation | ACCEPTED | `contracts/tenancy/tenancy.yaml` | `scripts/validate-governance-contracts.rb` | CP / IAM / engines: isolation and governed mappings |
| `ADR-0004` | Cross-engine event/error/idempotency metadata | ACCEPTED | `contracts/events/v1/envelope.schema.json` | `scripts/validate-cross-engine-contracts.rb` | Trade / ERP / Infra: native replay and causal traces |
| `ADR-0005` | ERP system of record | ACCEPTED | `contracts/erp/v1/system-of-record.yaml` | `scripts/validate-erp-contracts.rb` | ERP: native iDempiere execution and provenance |
| `ADR-0006` | Supplier-onboarding contract | ACCEPTED | `contracts/supplier-onboarding/v1/asyncapi.yaml` | `scripts/validate-event-registry.py` | Estates / ERP: live KYB and supplier projection |
| `ADR-SHARED-007` | Capability model and provider neutrality | ACCEPTED | `contracts/capability/v1/catalogue.yaml` | `scripts/validate-capability-contracts.rb` | CP / engines: provider eligibility and consumer conformance |
| `ADR-SHARED-008` | Capability namespaces and canonical events | ACCEPTED | `contracts/capability/v1/namespace-registry.yaml` | `scripts/validate-capability-contracts.rb` | Trade / CP: versioned adoption and no legacy event publication |
| `ADR-SHARED-009` | Product, provisioning, readiness and drift schemas | ACCEPTED | `contracts/product/v1/subscription.schema.json` | `scripts/validate-capability-contracts.rb` | CP: durable lifecycle and reconciliation |
| `ADR-SHARED-010` | Supplier KYB decisions and evidence | ACCEPTED | `contracts/supplier-onboarding/v1/supplier-kyb-decision-recorded.schema.json` | `scripts/validate-event-registry.py` | Estate: decision-time KYB enforcement and evidence custody |
| `ADR-SHARED-011` | Commercial subscription, billing and payments | ACCEPTED | `contracts/product/v1/subscription.schema.json` | `scripts/validate-commercial-contracts.py` | CP / Subscriptions / Payments: native classification and billing |
| `ADR-SHARED-012` | Topology identifiers and external systems | ACCEPTED | `contracts/control-plane/v1/external-systems.yaml` | `scripts/validate-control-plane-contracts.py` | CP: registered system pairs and opaque topology IDs |
| `ADR-SHARED-013` | External Reference and Mapping administration | ACCEPTED | `contracts/control-plane/v1/canonical-mapping.schema.json` | `scripts/validate-control-plane-contracts.py` | CP: approve/validate, If-Match, SoD and ambiguity refusal |
| `ADR-SHARED-014` | Trusted context mapping resolution | ACCEPTED | `contracts/control-plane/v1/examples/mapping-resolution.json` | `scripts/validate-control-plane-contracts.py` | CP: context redemption and tenant isolation |
| `ADR-SHARED-015` | Provisioning desired-state convergence | ACCEPTED | `contracts/control-plane/v1/provisioning-desired-state.schema.json` | `scripts/validate-control-plane-contracts.py` | CP: plan approval, freshness, execution and drift |
| `ADR-SHARED-016` | Provider migration and engine tasks | ACCEPTED | `contracts/control-plane/v1/engine-migration-task.schema.json` | `scripts/validate-control-plane-contracts.py` | CP / engines: migration task lease fencing and safe rollback |
| `ADR-SHARED-017` | Catalogue, provider declaration and registration | ACCEPTED | `contracts/capability/v1/catalogue.yaml` | `scripts/capability_catalogue.py` | All engines / CP: adoption and EA-09 certification |
| `ADR-SHARED-018` | Event context and producer registry | ACCEPTED | `contracts/events/v1/event-registry.yaml` | `scripts/validate-event-registry.py` | Trade / ERP / estates: producer activation and legacy quarantine |
| `ADR-SHARED-019` | Regulations, Docs and Pulse authority boundaries | ACCEPTED | `contracts/cross-engine-reference/v1/domain.schema.json` | `scripts/validate-cross-engine-reference-contracts.py` | Regulations / Trade Docs / Pulse: independent authority |
| `ADR-SHARED-020` | TradeDocument v2 contract | ACCEPTED | `contracts/trade-document/v2/domain.schema.json` | `scripts/validate-trade-document-contracts.py` | Trade Docs: immutable versions and real documentary custody |
| `ADR-SHARED-021` | Cross-engine references and historical pinning | ACCEPTED | `contracts/cross-engine-reference/v1/domain.schema.json` | `scripts/validate-cross-engine-reference-contracts.py` | Consumers: owner authentication and replayable snapshots |
| `ADR-SHARED-022` | Regulations ↔ Trade Docs documentary exchange | ACCEPTED | `contracts/regulatory-document-exchange/v1/domain.schema.json` | `scripts/validate-regulatory-document-exchange-contracts.py` | Regulations / Docs: witnessed bidirectional choreography |
| `ADR-SHARED-023` | Documents event producer activation contract | ACCEPTED | `contracts/regulatory-document-evidence/v1/asyncapi.yaml` | `scripts/validate-documents-event-activation.py` | Trade Docs: actual producer, durable events and replay |
| `ADR-SHARED-024` | Regulations namespace and events | ACCEPTED | `contracts/regulatory-document-assessment/v1/asyncapi.yaml` | `scripts/validate-regulations-event-activation.py` | Regulations: event issuer and legal-time source evidence |
| `ADR-SHARED-025` | Intelligence namespace / Pulse boundary | ACCEPTED | `contracts/capability/v1/namespace-registry.yaml` | `scripts/validate-intelligence-namespace-boundary.py` | Pulse: non-authorising intelligence consumers |
| `ADR-SHARED-026` | RTD cross-repository conformance | ACCEPTED | `contracts/rtd-conformance/v1/profile.schema.json` | `scripts/rtd_conformance.py` | Regulations / Docs / Pulse: independent pinned contract runs |
| `ADR-SHARED-027` | Regulations capability census | ACCEPTED | `contracts/regulations/v1/capabilities.yaml` | `scripts/tests/test_regulations_capability_census.py` | Regulations: runtime capability readiness vs catalogue |
| `ADR-SHARED-028` | Regulatory decision evaluate contract | ACCEPTED | `contracts/regulatory-decision/v1/domain.schema.json` | `scripts/validate-regulatory-decision-contracts.py` | Regulations: rule/time/evidence and no false permission |
| `ADR-SHARED-029` | Pulse intelligence capability census | ACCEPTED | `contracts/intelligence/v1/capabilities.yaml` | `scripts/tests/test_intelligence_capability_census.py` | Pulse: provider support and authority checks |
| `ADR-SHARED-030` | Pulse PARTIAL provider promotion boundary | ACCEPTED | `contracts/intelligence/v1/pulse-registration.json` | `scripts/tests/test_intelligence_capability_census.py` | Pulse: independently verified PARTIAL support |
| `ADR-SHARED-031` | Pulse IMPLEMENTED readiness boundary | ACCEPTED | `contracts/intelligence/v1/pulse-registration.json` | `scripts/tests/test_intelligence_capability_census.py` | Pulse / IAM / CP: authenticated operational readiness |
| `ADR-SHARED-032` | EA-09 provider capability certification | ACCEPTED | `contracts/capability/v1/certification.schema.json` | `scripts/tests/test_ea09_provider_certification.py` | CP: durable certification, expiry and revoke |
| `ADR-SHARED-033` | Corporate finance capability proposal | PROPOSED | `contracts/finance/v1/README.md` | — (proposal) | Proposed only: steward and ERP owner decision required |
| `ADR-SHARED-034` | ERP posting authority and native boundary | ACCEPTED | `contracts/erp/v2/posting-authority.schema.json` | `scripts/validate-erp-posting-authority-contract.py` | ERP: live CP actor/mandate check at native commit |
| `ADR-SHARED-035` | Payments money-movement authority | ACCEPTED | `contracts/payments/v2/money-movement-authority.schema.json` | `scripts/validate-payments-money-movement-authority-contract.py` | Payments: real mandate, no replayed money movement |
| `ADR-SHARED-036` | Cross-repository L4 integration and deployment | ACCEPTED | `docs/architecture/ea-v2.2-integration-acceptance-matrix.md` | `scripts/tests/test_ea_v23_governance.py` | Infrastructure: real broker, trace and protected staging evidence |
| `ADR-SHARED-037` | ERP purchase-side recording classes | ACCEPTED | `contracts/erp/v2/posting-operations.yaml` | `scripts/validate-erp-posting-authority-contract.py` | ERP: recorded outcomes under appropriate mandates |
| `ADR-SHARED-038` | ERP payable provenance and negative controls | ACCEPTED | `contracts/erp/v2/payment-execution-evidence.schema.json` | `scripts/validate-erp-posting-authority-contract.py` | ERP: native deny-by-name and financial evidence |
| `ADR-SHARED-039` | Trade order and seller authority | ACCEPTED | `contracts/trade/v2/order-authority.schema.json` | `scripts/validate-trade-order-authority-contract.py` | Trade / CP: real seller actor and native order commit |
| `ADR-SHARED-040` | Baobab Experience System | ACCEPTED | `docs/experience/bxs-cross-estate-conformance-register.md` | `.github/workflows/verify-experience-registry.yml` | Digital estates: actual imports, Playwright, Lighthouse and accessibility |
| `ADR-SHARED-041` | Engineering philosophy and excellence | ACCEPTED | `docs/governance/engineering-philosophy-review.md` | `scripts/tests/test_engineering_philosophy_governance.py` | All repositories: demonstrable code, security, UX and provenance |
| `ADR-SHARED-042` | Commercial actor and buyer context | ACCEPTED | `contracts/trade/v2/buyer-execution-context.schema.json` | `scripts/tests/test_buyer_execution_context.py` | Trade / IAM / CP: real BFF checkout and native commitments |
| `ADR-SHARED-043` | Development provisioning boundaries | ACCEPTED | `docs/adr/ADR-SHARED-043-Development-Provisioning-and-Environment-Approval-Boundaries.md` | `scripts/tests/test_development_profiles.py` | Infra / engines: isolation and protected approval separation |
| `ADR-SHARED-044` | Current ProductSubscription workload authority | ACCEPTED | `contracts/product/v1/current-authority.schema.json` | `scripts/validate-commercial-contracts.py` | CP / Subscriptions: live current read and pre-dispatch denial |
| `ADR-SHARED-045` | Provider-neutral People and tenant choice | ACCEPTED | `contracts/people/v1/domain.schema.json` | `scripts/tests/test_people_contracts.py` | People / ERP / CP: BYO provider, payroll and employer tenancy |

## Evidence rules and next-action ownership

1. **Source check:** inspect the live version of the referenced artifact and run the associated source test, plus negative fixtures. The register is a starting index, not the test's result.
2. **Consumer check:** pin the exact accepted Shared revision in the owning repository, verify semantic compatibility and ensure no private implementation bypasses CP/IAM authority.
3. **Runtime check:** use a persisted transaction or material native effect where relevant, with independent database/readback, broker delivery, retry, duplicate prevention, stale/revoked authority and telemetry evidence. Do not substitute a synthetic provider result for a real financial or logistics consequence.
4. **Protected gate:** keep provider/legal certification, cloud approval, staging and production explicit and independent. Neither this audit nor a passing Shared CI authorises deployment.
5. **Proposal handling:** ADR-SHARED-033 stays Proposed until its designated Shared/ERP owners accept its scope; candidate finance contracts are not approval.
6. **Revision:** this inventory is a dated source snapshot. Before merge or certification, refresh the PR/head SHA, verify test and review outcomes, then update affected row statuses with independently witnessed evidence.

**No runtime qualification is claimed in this register for any ADR.**
