# ADR-SHARED-036 — Cross-Repository Integration Testing, Tenant-Neutral Consumption and Production Deployment

**Status:** Proposed — architectural decision pending approval  
**Date:** 2026-10-15  
**Decision owners:** Baobab Platform Architecture / Shared Contracts / Infrastructure / Security / Control Plane / IAM / Domain Engines  
**Authority repository:** baobab-platform/shared  
**Implementation orchestrator:** baobab-platform/infrastructure  
**Pioneer:** Nabhold Group Africa — integration-testing pilot; not a revision of the original ZuriBeans production go-live sequence  
**Subsequent consumers:** Thamani Global (B2B/B2C logistics), ZuriBeans (B2B), Equator & Estate Co., and external third-party enterprises  
**Applies to:** Codespaces, developer workstations, GitHub Actions, protected staging acceptance, production topology, external API consumption, tenant isolation and future regional deployments  
**Reconciles and retains:** Shared ADR-0001 as amended by ADR-0003, ADR-SHARED-007/011/012/015/017/018/021/026/032/034/035; CP ADR-BCP-002/003/004/005/006/007/009/017/018/025/026/027; IAM ADR-IAM-0033; Infrastructure ADR-Infra-0002/0005/0006/0007/0008/0009/0010/0011/0012/0013/0014/0015/0016/0017/0018/0019/0020/0021/0022; Nabhold ADR-NAB-0012/0014, Go-Live Master Plan v2.0, EA Plan v2.1  
**Does not itself authorise:** production deployment, live IAM credentials, tenant or legal-actor admission, merchant certification, provider promotion, new administrative grants or any bypass of release gates

---

## 1. Context and problem

Baobab is a headless, capability-centric, contract-governed and multi-tenant platform. Its independently deployable engines and first-party Digital Estates have meaningful individual CI suites. Existing evidence includes Infrastructure L3 Compose smoke tests, IAM live Keycloak/Kratos/Hydra tests, CP PostgreSQL authority tests, Nabhold OIDC and encrypted-session tests, and Payments Gate D1, which runs a real Payments service and CP with a deterministic test processor.

Independent repository CI does not yet prove a complete consumer journey across **real components**. For example, a passed Nabhold OIDC unit test does not demonstrate real IAM token issuance plus active CP principal mapping plus resolved CMS provider plus cross-tenant denial. Likewise an isolated engine test is not a legally or financially approved staging acceptance.

We must not accidentally institutionalise a model where every tenant has a Baobab-developed frontend or where a new company requires one separately installed CP, IAM and copy of every engine. Nabhold is the first **integration test pioneer**, with identical patterns needed for Thamani, ZuriBeans, later Equator & Estate Co., and eventually external enterprise tenants who bring their own frontend, use an ERP integrator, or have no frontend.

## 2. Core decision and invariants

1. **One version-pinned L4 integration harness SHALL be shared between local workstations, GitHub Codespaces and GitHub Actions.** The identical validated manifest, Docker Compose profiles, preflight, start, test, evidence and teardown entrypoints SHALL be used in every executor. This is nonproduction test infrastructure, never production hosting.
2. **Infrastructure SHALL own the cross-repository orchestration** in baobab-platform/infrastructure. Shared SHALL own canonical interface/evidence schemas only when they become cross-provider contracts. Each engine remains authoritative for its own business semantics and test fixtures. The consumer Digital Estate remains presentation/BFF owner.
3. **Nabhold SHALL be the pioneering L4 consumer**, starting with IAM + CP + Nabhold confidential BFF + CMS. The first test suite SHALL be tenant-neutral and parameterised; Nabhold never receives implicit platform privileges.
4. **Every approved tenant MAY consume Baobab with or without a Digital Estate.** A tenant does not need any frontend created or hosted by Baobab. An existing third-party website, customer backend, partner integration, a service workload or a separately purchased Baobab-managed estate are all valid consumption modes.
5. **Baobab CP/IAM and approved headless engines SHALL be deployed as independent shared production services by default**, with policy-driven shared or dedicated EngineInstances. Logical tenancy, legal-actor authority, capability grants and provider bindings remain independent even when compute or storage is pooled.
6. **CP is the canonical authority and resolver, not a universal proxy.** After CP resolves the caller's current context, permitted capability and provider, a consumer normally invokes that provider through governed ingress. The domain engine independently validates token, context and execution-point authorisation.
7. **Group ownership does not authorise cross-tenant data access.** Nabhold, Thamani, ZuriBeans, Equator & Estate Co. and external enterprises remain independent Organisations/Tenants. CorporateRelationship, PlatformRelationship and PlatformAccount cannot substitute for an AdministrativeGrant, capability binding or legal mandate.
8. **Tests SHALL distinguish evidence grades.** Synthetic mocks, real components with synthetic identities, protected staging with real approved identities and external provider certification are separate categories. No skipped mandatory check or dummy approval counts as a pass.
9. **Accepted Infrastructure decisions remain controlling.** No Codespaces container, test fixture or pipeline may change the initial ECS/Fargate, account, managed data, security or release architecture without a separately accepted ADR.
10. **Fail closed.** Missing IAM issuer, audience, valid CP context, legal evidence, required instance, provider readiness, test dependency or staging approval SHALL deny the operation or qualification.

## 3. Terminology and authority table

| Concept | Authority | Rule |
|---|---|---|
| Canonical Organisation | CP | Real-world identity may exist before tenant onboarding |
| LegalEntity and responsible legal actor | CP with verified source evidence | Jurisdiction, role, activity, market and period are consequential; never inferred from group ownership |
| Tenant | CP | Operational, security and isolation boundary; not a website |
| CorporateRelationship | CP | Effective-dated group ownership and affiliation, not access |
| PlatformRelationship and PlatformAccount | CP | Owner/operator, group affiliate or external customer; customer accounts do not collapse tenants |
| Market | CP | Jurisdiction/business activity context, not necessarily an AWS Region |
| DigitalEstate | Owning consumer, with CP registration when applicable | Optional; may be first-party, third-party, multiple or absent |
| Subscription, grant and binding | Subscriptions and CP under separate authorities | Define commercial eligibility, capability scope and actually selected provider |
| Engine / EngineInstance | CP registry, engine declaration, Infrastructure observation | Capability implementation versus deployed operational instance |
| IsolationProfile | CP desired state, Infrastructure physical execution | Shared, bridged or dedicated compute/data/region isolation as appropriate |
| Human or workload token | IAM | Authentication and narrow audience/scope; does not imply platform tenant authority |
| Domain operation | Respective headless engine | Business validity, persistence, domain vetoes, execution, event and reconciliation |

No email, frontend hostname, untrusted tenant header, IAM role name or AWS role automatically establishes a canonical CP Principal or entitled tenant.

## 4. Consumer channel architecture: external enterprises are first-class

The platform SHALL support the following consumer modes without rewriting the platform:

| Mode | Example | Frontend ownership | Integration |
|---|---|---|---|
| First-party corporate | Nabhold institutional website and executive workplace | Nabhold | Server-side BFF, IAM and CP, authorised domain APIs |
| Autonomous B2B/B2C subsidiary | Thamani logistics businesses and individual courier users | Thamani | BFF and separate person/organisation business authorisation |
| Autonomous B2B subsidiary | ZuriBeans buyer/supplier portals | ZuriBeans | Buyer/supplier Organisation contexts, market-aware capability resolution |
| Subsequent subsidiary | Equator & Estate Co. | Subsidiary or chosen provider | Only owner-approved property/construction/finance/operations capabilities |
| External bring-your-own app | Enterprise frontend, website, mobile app or vendor BFF | External customer or integrator | Approved OAuth/OIDC application and resource APIs |
| External API-only | External ERP, automation, B2B integration, batch customer | No frontend required | Approved workload/API registration, CP context and domain resources |
| Optional managed estate | Customer explicitly buys a managed presentation product | Contractually designated owner | Optional DigitalEstate provisioning, not a tenant admission prerequisite |

An external tenant with no Digital Estate is a normal, valid state. If a canonical API supports optional estate context, it SHALL accept an absent estate when the operation does not require one. If an existing API contract incorrectly forces DigitalEstate even for a headless workload, that contract MUST be amended through its owning Shared/CP decision before enabling the flow. A fake or universal placeholder DigitalEstate is prohibited.

Thamani's clarified B2B/B2C logistics commercial model requires formal amendment of its accepted B2B-only ADRs in its owning repository. This ADR records the consumer requirement but does not silently override that decision or imply that consumer parcel services require retail catalogue/cart/checkout.

### 4.1 First-party or BYO browser flow

1. The caller uses an HTTPS frontend owned by Nabhold, a subsidiary or an external integrator.
2. Its BFF completes an approved IAM user transaction (Kratos/Hydra or retained Keycloak federation under ADR-IAM-0033). Exact issuer/signature/audience, PKCE/state/nonce, session confidentiality and revocation checks apply.
3. The BFF resolves the current CP-mapped Principal, Organisation/Tenant, market, responsibility/mandate and permitted context. It does not trust a tenant selected only by the browser.
4. CP resolves permitted entitlement/capability, selected EngineInstance, IsolationProfile and current provider binding.
5. The BFF invokes the resource server directly through the approved gateway/private routing with the correct provider-specific token and bound context.
6. The provider rechecks identity/context/domain scope and records authorised business consequences; durable events are emitted through its accepted outbox.
7. Browser JavaScript never gains workload client secrets, CP admin credentials or privileged cross-tenant tokens.

### 4.2 API-only / third-party service flow

An external organisation MAY register only its canonical Organisation, appropriate PlatformAccount and Tenant admission, an authorised workload/client, product subscription and applicable provider bindings, without a frontend. The client obtains a short-lived, narrowly scoped token, resolves CP context, then calls the authorised provider resource API.

External JWTs, self-supplied tenant IDs, unsigned webhooks and customer API keys alone SHALL NOT constitute CP-authorised tenant context. APIs SHALL bind service identity, exact audience, subscription/capability, legal authority, market and expiry. Inbound webhooks SHALL have authenticated ingress, replay/idempotency protection, isolation checks and current governance. Tenants never receive direct cloud credentials or raw engine databases merely by subscribing.

### 4.3 CP is not a shared business service bus

CP SHALL resolve identity, platform context, tenancy, topology, capability binding and legal authority; it SHALL NOT route all domain payloads, execute payments, own CMS content or become ERP/Trade/TMS business authority. API gateway authentication alone is necessary but insufficient; provider operations must recheck current domain execution rules. Platform admin console is a separate privileged surface from each tenant's Digital Estate.

## 5. Production deployment architecture (existing decisions restated)

### 5.1 Logical production topology

    FIRST-PARTY DIGITAL ESTATES       EXTERNAL BYO FRONTENDS        EXTERNAL API-ONLY
    Nabhold/Thamani/ZuriBeans         Customer apps/BFFs           Customer services
                     \                      |                       /
                      \_____________________|______________________/
                                            |
                                  Route 53 / ACM / ALB
                                   WAF where required
                                            |
                               Private APISIX traffic plane
                                    |                 |
                                    v                 v
                           PLATFORM CONTROL       HEADLESS ENGINE SERVICES
                           CP APIs + workers      Trade, ERP, CMS, Pulse
                           IAM Kratos/Hydra       Subscriptions, Payments
                           Keycloak federation    Regulations, Trade Docs
                           Context/entitlements   TMS and further engines
                           Engine/binding index   Domain execution and events
                                    \                 /
                                     \__ provisioned /
                                        EngineInstances
                                        (shared/dedicated)
                                            |
                                 MANAGED SERVICE FOUNDATION
                            RDS PostgreSQL 17 / Multi-AZ / PITR
                            ElastiCache Valkey or reviewed Redis
                            Amazon MQ for RabbitMQ / durable queues
                            Private S3/object storage as appropriate
                            secrets/KMS / telemetry / backup and DR

This diagram shows **logical authorities**, not a sequence requiring all business requests to pass through CP. CP resolves platform authorization and routing; the resource server performs business operations. Platform management surfaces and databases are private, not directly Internet-exposed.

### 5.2 Actual AWS hosting model and constraints

Accepted ADR-Infra-0002/0006/0008/0010/0011/0012/0015/0021 SHALL remain controlling:

- AWS accounts SHALL separate development, staging and production. The initially selected production region is **af-south-1 (Cape Town)**. Operating in South Africa or Uganda as a commercial Market does not implicitly create another region or data replica.
- **Amazon ECS with AWS Fargate** SHALL be the default runtime for compatible stateless CP API replicas, private workers, gateway/application services and independent headless engine APIs. Each service has its own ECS task definition, service identity, least-privilege AWS role, security group, health check, autoscaling and immutable OCI image digest. Finite jobs use governed tasks. A single mega-container holding all engines is rejected.
- Approved public entry is **Route 53 → protected AWS edge/ALB + ACM TLS → private APISIX → authenticated service**. APISIX control/admin endpoints, CP privileged routes and storage are kept private.
- **Amazon RDS PostgreSQL 17 Multi-AZ**, encrypted and backed up with restore/PITR, is the initial managed relational platform. Individual engines own their schemas/databases and DB credentials; shared physical hosting never permits direct cross-engine reads. Additional DB isolation uses accepted IsolationProfiles.
- **Amazon ElastiCache with Valkey preferred**, or a verified Redis-compatible exception, serves cache/session functions; durable business truth stays in domain stores. **Amazon MQ for RabbitMQ clustered deployment** provides private authenticated transport, quorum queues where appropriate, publisher confirms, retries/dead letters and idempotent consumers.
- Stateful vendor runtimes (iDempiere, IAM providers, APISIX control plane/etcd, Qdrant/Pulse and other engine-specific stores) require verified deployment, persistence, licensing, compatibility and HA decisions. Fargate is the default **when compatible**, not a promise every engine can safely run on Fargate with ephemeral volumes.
- Build once, attest and promote **immutable release artifacts** under Infrastructure Terraform, release manifests, protected environments and operation-specific verification. Codespaces cannot deploy production and no mock image/issuer can become a production provider.
- Multiple availability zones, independently tested failover, KMS/secret rotation, audits/observability, data retention, explicit SLOs and backup restoration must be demonstrated before the relevant release is marked production-ready.
- Actual AWS staging/production accounts, role ARNs, state buckets and live IAM/CP/PSP credentials SHALL be entered through separately authorised environment/bootstrap channels; synthetic fixture IDs cannot stand in for them.

### 5.3 Pooled, bridged and dedicated engine cells

| Isolation approach | When selected | Production effect |
|---|---|---|
| Pooled by default | Provider supports certified multi-tenant isolation and resource contention is acceptable | Several tenants share an EngineInstance or underlying managed service; every record/credential/context remains isolated |
| Bridge / selected silo | One engine or data store needs dedicated performance, legal separation or vendor constraints | Dedicated ERP/Trade/Payments instance, database or service for that tenant while other approved engines remain pooled |
| Full dedicated cell | Approved contractual, regulatory, security, availability or residency requirement | Separate account/VPC/engine/runtime/data boundary as governed by IsolationProfile; canonical CP tenancy remains valid |
| Additional regional cell | Future independently accepted residency, latency or continuity requirement | New region-specific EngineInstances and isolation/replication rules, not a new default tenant identity |

A **tenant is not an AWS account, ECS cluster or Digital Estate**. The Infrastructure provisioner converts approved CP desired state into physical configuration. Most tenant admissions SHOULD bind already-running shared instances. It SHALL NOT automatically deploy a new CP, IAM or full headless-engine suite for every external customer.

CP SHALL remain one logically authoritative platform governance system. It may have multiple high-availability API replicas, workers or future geographic cells, but their authority scopes/consistency must be explicitly governed. A stale cache may never create a new tenant or grant. If CP is unavailable, high-consequence authority decisions fail closed under the existing CP assertion and expiry semantics; engines never switch to an unapproved instance.

### 5.4 Tenancy without a digital estate — full lifecycle

    Independent business contract/application
      -> Organisation-first application and evidence/verification
      -> PlatformRelationship = EXTERNAL_CLIENT where applicable
      -> PlatformAccount, independent Tenant, legal actor and IsolationProfile
      -> approved product/subscription/capability scope
      -> approved IAM human federation or machine workload registration
      -> CP context, market, grants and EngineInstance binding
      -> REUSE shared provider or provision approved dedicated resources
      -> secure API/webhook/domain consumption
      -> usage/billing, independent audit, revocation and exit/retention

**DigitalEstate creation is optional throughout.** A customer may bring a frontend, use a certified integration partner, or consume via a backend only. Neither Nabhold group relationship nor the platform-owner role is assigned to an external customer. A customer may use many apps without reminting its tenant.

## 6. Cross-repository L4 Codespaces + CI verification

### 6.1 Canonical implementation owner and target structure

Infrastructure SHALL develop the implementation under the following proposed paths (not yet present):

    infrastructure/
      .devcontainer/platform-integration/devcontainer.json
      tests/platform-integration/
        manifest.lock.yaml
        compose.yaml
        profiles/
          iam-cp.yaml
          nabhold-r0.yaml
          thamani-logistics.yaml
          zuribeans-b2b.yaml
          equator-property.yaml
          external-api-no-estate.yaml
          finance.yaml
        scripts/{preflight,up,test,down}.sh
        scenarios/
        schemas/
        evidence/.gitignore
      .github/workflows/platform-l4.yml

Existing engine-specific devcontainers SHALL remain available. Developers select the heavier integration configuration deliberately; it is not the default for every source edit.

### 6.2 Single deterministic versioned manifest

The test lock SHALL name each participating repository plus full SHA, image digest or documented built-for-test image, Shared contract pin, environment/identity fixture classification, scenario identifiers, engine/profile, mandatory checks, simulated external integrations and resource requirements.

- **Ordinary PR:** test the proposed repository head against approved pinned upstream dependencies.
- **CP/Shared/IAM change:** test the directly affected consumer profiles and contract matrix.
- **Nightly:** detect drift by testing a separately recorded moving-head compatibility matrix without silently modifying the locked PR baseline.
- **Release candidate:** promote the same immutable binaries/images that passed relevant verification. No rebuild just because environment changes.

### 6.3 Same entrypoints on Codespaces and Actions

The following interfaces SHALL be implemented by Infrastructure. Commands are **future interface examples**, not currently runnable scripts:

    tests/platform-integration/scripts/preflight.sh
    tests/platform-integration/scripts/up.sh iam-cp
    tests/platform-integration/scripts/test.sh iam-cp
    tests/platform-integration/scripts/up.sh nabhold-r0
    tests/platform-integration/scripts/test.sh nabhold-r0
    tests/platform-integration/scripts/down.sh

Both Codespaces and Actions SHALL use these exact entrypoints, compatible Compose services, explicit timeouts, health checks and deterministic cleanup. Compose profiles SHALL limit runtime cost and startup time. Test data and credentials SHALL be newly generated and disposable for each run.

### 6.4 Security properties of the integration lab

- Codespaces is private, ephemeral nonproduction compute. Only approved repository reads and private port-forwarding are permitted; no Internet-exposed IAM admin, CP admin, database, broker or Kubernetes/Docker socket APIs.
- Actions PR runners execute **untrusted source** without protected environment credentials. Use ephemeral installation-token checkout or explicit least-privilege repository access. Do not expose real AWS accounts, operator credentials, PSC/PSP credentials, legal records or production data to PR jobs.
- Real-component tests SHALL have verified TLS origins, exact OIDC issuer/redirect/PKCE/state/nonce/audience; no disabling TLS verification. Externally browser-visible Codespaces URLs do not magically provide valid internal issuer or confidential callback origins.
- Synthetic test principals, fixture keys, TLS CAs, datasets and mock processor credentials SHALL never become persistent production credentials. Sanitise artifacts, logs and exception bodies before upload.
- A required service that does not start, a nonexecutable test script, a missing mandatory scenario, stale image digest, accidental public port, or a disallowed mocked dependency SHALL result in FAIL rather than PASS with skips.
- Docker test containers, volumes and networks SHALL be destroyed even on failed tests. Resource quotas and concurrency SHALL keep the profiles operationally bounded.
- Actions will reuse pinned Shared workflows where appropriate, but their scopes and implementation shall remain owned by the appropriate repo. Production roles require separate protected GitHub Environment OIDC trust and approved release source.

### 6.5 Profiles and rollout sequence

| Work item | Profile / consumer | Real-component minimum | Exit |
|---|---|---|---|
| INT-01 | L4 foundation | Infra Compose, version locks, DB/broker/cache, TLS, evidence | Same start/test/teardown in one Codespace and CI |
| INT-02 | IAM ↔ CP | Human/workload IAM issuer, CP executable and owned DB | Real tokens, CP identity mapping, current context, negatives |
| INT-03 | **Nabhold pioneer** | INT-02 + Nabhold BFF + TLS session store + CMS | Real OIDC callback, CP binding, published-only CMS, revocation/recovery |
| INT-04 | Thamani B2B/B2C logistics | Shared identity/context plus Thamani estate and domain APIs | Organisation vs consumer isolation, quote/booking/tracking under accepted owner decisions |
| INT-05 | ZuriBeans B2B | Shared identity/context plus buyer/supplier estate and trade APIs | Buyer/supplier, market and cross-tenant boundaries |
| INT-06 | Equator & Estate Co. | Owner-approved property/finance providers once implemented | Domain-specific test, no assumed capabilities |
| INT-07 | **External API-only** | IAM + CP + approved provider; deliberately no owned frontend | Valid subscription and context; real machine API use, no DigitalEstate requirement |
| INT-08 | Financial and event provider mesh | Payments, Subscriptions, Trade, ERP, TMS as certified | Execution veto, outbox/idempotency, provider recovery; PSP simulation declared |

Nabhold is the first **test-profile pilot**. Earlier accepted ZuriBeans go-live compute decisions are unaffected.

All initial profiles SHALL have a generic fixture schema; a test tenant shall not gain capabilities because its name is Nabhold. Thamani's B2B/B2C direction SHALL be reconciled in its own accepted ADRs; the cross-platform runner does not rewrite business ownership decisions.

### 6.6 Common scenario matrix

| Scenario | Required behaviour |
|---|---|
| OIDC human login | Signed token, correct issuer/client/audience/nonce, PKCE and single-use code |
| IAM workload access | Exact registered client, scope and target audience |
| CP authority | Active canonical Principal, Organisation/Tenant, mandate, binding; current grant |
| Cross-tenant denial | Nabhold, each subsidiary and a separate external tenant cannot see each other's records without independent lawful authority |
| Market/isolation | Binding resolves only for authorised market, legal actor, location and IsolationProfile |
| Provider execution | Actual provider checks token/context/capability at the execution point |
| CMS | Published allowed; draft, other-tenant and unauthorised preview denied |
| Revocation | Identity, membership, grant, client or provider revocation blocks fresh consequential operations |
| Onboarding | Independent maker/checker and verified evidence; no fake registered legal persons |
| No frontend | API-only tenant works with no DigitalEstate and rejects forged context |
| Messaging | Durable outbox/event, replay-safe inbox, retry/DLQ, crash recovery |
| Finance | CP legal veto independent of Payments financial approval and ERP posting; replay and uncertain outcome reconciled |
| Provider outage | No fallback to unauthorised EngineInstance; preserved durable state and denial |

A mandatory scenario is not PASS if it is skipped, uses the wrong source version, or substitutes a simulator without an explicit declared boundary. A missing domain implementation is **BLOCKED**, not secretly skipped or made up.

### 6.7 Evidence schema and evaluation

Every run SHALL produce a scrubbed, machine-readable receipt with run and profile IDs, commit/image/contract digests, real versus simulated component declaration, test scenario IDs, PASS/FAIL/BLOCKED outcomes, evidence hash and correlation, failure/retry reason, timestamps, custody reference and verification-review status.

Evidence grades are distinct:

1. STATIC / UNIT: source and contract logic only.
2. REAL_COMPONENT_SYNTHETIC_DATA: actual process/database/issuer implementation, synthetic identities.
3. PROTECTED_STAGING: actually deployed, approved IAM/CP/providers, human-reviewed environment evidence.
4. EXTERNAL_CERTIFICATION: external PSP/registry/government/provider facts certified under their owners.
5. PRODUCTION_ACCEPTANCE: independently authorised release and operational signoff.

No CI-generated artifact promotes itself from (2) to (3)-(5). Protected GitHub Environments, real reviewer principal separation, deployment identity, protected secrets, AWS least-privilege OIDC roles, runbooks and signed G17 release dossiers govern those promotions.

### 6.8 CI/CD trigger matrix

| Trigger | Minimum suite | Enforcement |
|---|---|---|
| Per-engine PR | Unit/contracts/security plus affected L4 profile | Required status checks for PR |
| Shared/CP/IAM PR | Core L4 + affected downstream consumer and no-estate profile | Compatibility block on change |
| Harness PR | Manifest/schema/permission validation, one full profile, cleanup/security negatives | Infrastructure-specific required check |
| Main merge/nightly | Pinned smoke plus drift compatibility matrix | Baseline monitoring and actionable regression |
| Release candidate | Full declared critical-path matrix with immutable artifacts | Release qualification |
| Protected staging workflow dispatch | Real approved IAM/CP/engine credentials and deployment endpoints | Protected technical evidence only |
| Production approval | G17/gate-specific legal, financial, security and operational signoff | Human-authorised release |

An Actions runner cannot turn into production deployment merely because it can start Compose. Codespaces cannot bypass release controls. Runtime deployments remain Infrastructure-controlled and use approved immutable build artifacts and release manifests.

## 7. Deployment and tenant onboarding operational sequence

1. Build and security attest approved engine versions independently, then publish immutable OCI images.
2. Promote pinned release manifests and validate Terraform, migrations, data compatibility, network and secrets under protected environment policies.
3. Provision shared CP API, CP workers, IAM runtime/federation, APISIX and approved engine services under ECS/Fargate where compatible, with private task networking and managed durable services.
4. Independently register each service's EngineInstance, deployed digest, capabilities, health, audiences and topology observations. Only reviewed provider support is activatable.
5. Admit each real Organisation/Tenant progressively, using verified registration/identity evidence and current legal-actor responsibilities.
6. Bind only subscribed/granted capabilities to qualified shared or dedicated EngineInstances. Use the chosen isolation/residency profile; do not create a new deployment for each tenant by default.
7. Permit the tenant's own BFF, external frontend or API-only workload to authenticate and request CP context; resource servers enforce the resulting authority and domain rules.
8. Operate with SLOs, observability, metering/billing where contracted, independent audit, revocation, drift alarms, backups/restore and controlled customer exit.
9. For a dedicated tenant or new AWS region, create a new approved isolated resource cell and map it to the existing canonical tenant, retaining historical facts and requiring separate migration/drift acceptance.

**Current rollout status:** Architecture and several nonproduction test/release assets exist. Actual AWS production services, approved account-specific configuration and protected G17 certifications SHALL NOT be assumed complete.

## 8. Alternatives

| Alternative | Result | Why |
|---|---|---|
| Separate bespoke CI stack per estate | Rejected | Duplicate contracts, unpredictable drift and poor negative coverage |
| Always run every engine in one giant Codespace | Rejected | High cost, resource starvation and poor test focus |
| Mock-only end-to-end acceptance | Rejected | Does not verify actual issuers, databases, gateways or resource-server enforcement |
| Codespaces for staging/production hosting | Rejected | Ephemeral development compute cannot satisfy protected deployment, HA or custody |
| One CP/IAM/all-engines instance per tenant | Rejected default | Contradicts governed shared multi-tenancy and isolation-by-requirement |
| Baobab-designed Digital Estate mandatory for tenancy | Rejected | Incompatible with third-party/API-only enterprise SaaS |
| CP relays every business request | Rejected | Violates CP decision/resource-server execution boundary |
| Immediate EKS migration | Deferred | Fargate remains accepted; require measured unmet workload needs |
| Dedicated engine/account when justified | Permitted | Must satisfy IsolationProfile and controlled migration/operations |

## 9. Consequences, acceptance criteria and follow-ups

**Benefits:** Cross-repo realism, reproducible debugging, fewer integration regressions, tenant-neutral tests, simplified first-party rollout, external enterprise adoption without frontend dependencies, and an evidence trail into protected staging.

**Costs/risks:** Real-service CI resource demand, cross-repo access governance, IAM issuer/callback consistency, engine-specific fixtures, CI runtimes, test matrix evolution, evidence sanitisation, and partial provider simulations. These are mitigated with scoped profiles, exact version locks, security preflight and honest evidence grades.

**To accept as implemented**, prove: (a) one Codespace and an Actions runner execute an identical pinned IAM+CP+Nabhold journey; (b) CMS and principal revocation deny correctly; (c) Thamani and ZuriBeans scenarios work with independent legal/tenant contexts; (d) an external API-only tenant successfully invokes its approved engine without a DigitalEstate; (e) false or absent mandatory evidence fails; (f) no CI fixture can become a provider or production credential; (g) protected staging retains independent signed approval.

**Implementation ownership:** Infrastructure = L4 orchestrator, manifest and runtime lifecycle; Shared = cross-provider contract/evidence governance; IAM = real issuer and client profile; CP = context, entitlement, no-estate API-only conformance and isolation; Nabhold = first test consumer; Thamani = reconcile commercial ADR and add own profile; ZuriBeans = B2B profile; Equator = later property/operations profile; providers = real domain fixtures; Security/Operations = protected review/certification.

This Proposed ADR does **not** claim operational acceptance, expand any authority or update commercial domain ADRs by implication.

## 10. External research references

- GitHub Codespaces devcontainer configurations: https://docs.github.com/en/codespaces/setting-up-your-project-for-codespaces/adding-a-dev-container-configuration/introduction-to-dev-containers
- GitHub Actions OIDC and reusable workflow trust: https://docs.github.com/en/actions/reference/security/oidc
- GitHub Actions deployment environments and required reviewers: https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments
- AWS SaaS control plane vs application plane: https://docs.aws.amazon.com/whitepapers/latest/saas-architecture-fundamentals/control-plane-vs.-application-plane.html
- AWS SaaS tenant isolation strategies: https://docs.aws.amazon.com/whitepapers/latest/saas-tenant-isolation-strategies/saas-tenant-isolation-strategies.html
- AWS SaaS Lens full stack isolation: https://docs.aws.amazon.com/wellarchitected/latest/saas-lens/full-stack-isolation.html
