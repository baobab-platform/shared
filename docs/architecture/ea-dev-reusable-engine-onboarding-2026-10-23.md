# EA-DEV — Reusable Engine Development Onboarding
## DEV-14/15 delivery specification and first two reference profiles

**Status:** EA-DEV **implementation specification** on `shared/main` after reviewed required CI/merge (candidate beforehand). This approves a delivery backlog, **not** a shipped engine-onboarding CLI, a new capability authority, running integrated service or certified capability.  
**Date:** 23 October 2026  
**Parent:** [EA-DEV-01 implementation plan](ea-v2.3-development-enablement-implementation-plan-2026-10-23.md) and Accepted [EA v2.3](EA-implementation-plan-v2.3-2026-10-20.md).  
**Governs within:** Accepted ADR-SHARED-043 (development approval), -036 (L4), -017 (provider lifecycle and implementation evidence), -015 (provisioning); CP BCP-026/027 and IAM ADR-0033; owners' existing security and domain ADRs.  
**Implementation owners:** Infrastructure (orchestration/receipt), baobab-dev (dev image compatibility/doctor), Shared (descriptor validation and canonical capability contract), CP (canonical tenant/context/provider binding), IAM (actual issuer), each engine (its own adapter/data/test logic).  
**Grounded engine baselines:** baobab-pulse/.baobab/capability-provider.yaml and baobab-payments/.baobab/capability-provider.yaml on their main branches as inspected 23 October. These declarations are *implementation claims*, **not** activation, certification or L4 acceptance.

## A. Design decision: composition over prerequisite chains

**Always separate four artifacts:**

1. **Toolchain requirement**, the existing consuming-repo \`.baobab/environment.yaml\`, validated against \`shared/contracts/development-environment/schema.yaml\` and the \`baobab-dev\` version lock. This is about runtimes/tools; it does not create business capability or run services.
2. **Capability provider declaration**, the existing \`.baobab/capability-provider.yaml\`, validated against \`shared/contracts/capability/v1\`. This states only which canonical capabilities an engine claims to implement; it cannot certify, activate, bind or grant them.
3. **Synthetic enterprise declaration**, the existing \`shared/contracts/development/v1/enterprise-profiles.schema.json\` and examples. It is the CP-owned tenant/Organisation/legal-context seed contract. A group profile's \`required_engines\` describes *desired enterprise readiness*, **not** an instruction to start every engine on each test run.
4. **Proposed integration-run profile** (new artifact, DEV-14), a declarative, unprivileged **composition** of one subject engine and exactly the IAM/CP/dependency processes and test journeys it needs. It references the three existing artifacts rather than copying their authority. It must never be interpreted as an EngineInstance registration or provider activation.

As a consequence, **CMS is mandatory only for scenarios exercising CMS**, such as the Nabhold corporate website. A Pulse/Payments profile can choose the \`external-client\` synthetic tenant (no DigitalEstate) or a selected synthetic first-party tenant, without booting CMS. Do not change the enterprise contract to remove legitimate future CMS readiness; simply report \`NOT_STARTED\`/BLOCKED for untested *other* enterprise capabilities and do not certify that tenant as fully provisioned.

An integration profile may share IAM and CP service processes across multiple *test* tenants/engines while maintaining strict issuer audiences, scopes, principal mappings, tenant partitions and engine-owned storage. The dependency planner calculates the required process subgraph, not an entire per-subsidiary infrastructure cluster. No engine acquires another engine's database or direct CP write access.

### Executable milestones

- **Component mode**: engine-owned unit/contract/real native database tests; issuer/CP can be represented by expressly **mocked** adapters, classified as component/contract evidence. No L4 PASS claim.
- **L4 developer integration mode**: real independently launched IAM, CP, subject engine, native dependencies and actual current-scope issuer/CP calls; seeded synthetic CP state. Evidence \`REAL_COMPONENT_SYNTHETIC_DATA\` **only after runtime observations**.
- **Protected acceptance**: independently provisioned staged or production services/credentials with their own controls and qualified domain provider; the developer profile is disabled and cannot be imported to bypass approval.

Profiles may run in local Codespaces, local Docker Compose or Actions; they must produce comparable functional receipts and must not claim *identical machine security*.

## B. DEV-14 — versioned profile descriptor and CLI integration

### Descriptor implementation backlog (Shared + Infrastructure)

Propose \`shared/contracts/development/v1/engine-integration-profile.schema.json\` **after** a reviewed schema/ADR-alignment PR; reference examples under \`shared/contracts/development/v1/examples/engines/\`. Suggested descriptive fields, **not current Shared schema**:

| Field | Meaning | Validation |
| --- | --- | --- |
| \`schema\` and \`profile_key\` | exact version, stable unique profile id | closed schema; explicit supported version |
| \`subject_engine\` | registered engine ID, not vendor technology | must match owner \`.baobab/capability-provider.yaml\` |
| \`enterprise_seed\` | name of an existing synthetic enterprise scenario + legal-actor variant | CP allocates all IDs; cannot submit arbitrary LegalEntity UUID or claim VERIFIED |
| \`mode\` | \`component\` or \`l4\`; \`protected\` excluded from developer descriptor | \`l4\` requires actual issuer and CP |
| \`services.required\`/\`services.optional\` | IAM, CP, engine + engine-local native services (e.g. Qdrant); dependency type and owner | a missing required provider is BLOCKED; optional provider cannot silently pass |
| \`iam\` | expected real issuer audiences, workload/human client classes and delegated scopes | **assertion only**; IAM issues credentials and owns lifecycle |
| \`cp\` | needed current context/capability resolutions and relevant operating-legal-actor cases | no fixture-supplied active bindings, grants or certification |
| \`capability_scenarios\` | canonical capability keys/major versions, positive/negative case IDs and action preconditions | Shared catalogue match; mandatory case IDs preserved |
| \`native_dependencies\` | engine-owned database, projection, broker/PSP simulation as applicable | pin exact image digest and source; no prod endpoint |
| \`run_policy\` | synthetic-only, isolation, max lease 86400 seconds, no exposed admin ports, cleanup | startup refuses staging/prod, protected tokens, malformed marker |
| \`reporting\` | actual scenario execution and evidence mapping | never accepts caller-supplied PASS/certified flags |

**Reject** fields \`certified\`, \`production_permitted_override\`, \`force_active\`, \`allow_all_tenants\`, \`skip_security\`, \`accept_as_staging\`, literal secrets, source-level minted IDs, arbitrary SQL, and host/prod endpoint strings in a Shared profile. Native configuration secrets reside in generated private runtime state and environment-specific secret inputs, not in versioned descriptors.

Implementation must enforce strict schema validation, deny unknown keys, verify provider declarations and Shared lock, resolve exact service image digests, use private networks, and compare actual owner/current source identity before admitting a profile. A mere YAML file cannot create authority. Register and bind implemented runtime providers only through normal CP-owned development lifecycle/API; **no direct SQL** outside CP's guarded disposable bootstrap, and do not label UNKNOWN providers healthy.

### Proposed commands (API target, NOT commands currently available)

\`\`\`sh
baobab dev doctor --profile pulse-intelligence
baobab dev plan --profile pulse-intelligence --mode l4
baobab dev up --profile pulse-intelligence --mode l4
baobab dev test --profile pulse-intelligence --mode l4
baobab dev evidence --profile pulse-intelligence
baobab dev down --profile pulse-intelligence
\`\`\`

A compatible Infrastructure \`l4.py\` facade is acceptable if it retains preflight/prepare/up/test/evidence/down semantics. The exact CLI name/flags are **design proposals**; do not show them as documented working commands until implemented. A \`plan\` operation must identify the precise IAM/CP/engine/dependency subgraph, required Docker resources, capability keys and contract pins, and **why** any requested provider is unavailable. A \`doctor\` operation must verify Docker/Compose, GHCR and package access, Python/Rust/JVM toolchain as applicable, file locks, environment contract, certificates, DNS and no unexpected forwarded/public ports.

### Runtime orchestration protocol

1. Read existing toolchain, capability and enterprise profiles; validate compatibility and proposed run profile.
2. Lock immutable Shared/CP/IAM/engine SHAs, container image digests, native migration versions and the run-scoped trace.
3. Allocate private temporary Compose project/namespace, isolated databases/volumes per engine, secrets and short-lived issuer clients. Deny any protected storage, real private records or unsafe production-like DB URL.
4. Start actual issuer and CP in the minimal subgraph. Invoke **CP's guarded development bootstrap** with CP-supplied synthetic maker/checker issuer subjects, nonce and lease. IAM, not the orchestrator or test file, issues signed tokens.
5. Ask normal CP APIs to register/resolve only existing implemented provider support in the disposable instance, with authentic caller/grant/market/actor scope. Missing instance/implementation cannot be auto-promoted.
6. Start the subject engine's real native data services. Migrate its own DB; seed domain-specific test data using its own public/test APIs/approved fixtures and CP-issued IDs.
7. Run declared positive/negative/failure/retry/teardown tests; verify process calls, token expiry/revocation, CP current context and provider-specific effects. Classify simulated-vs-real domain operations accurately.
8. Write redacted run receipt: source SHA/lock, image digests, profile version, CP-issued references, issuer/audience class (no bearer), actual case IDs/results, failures/retries, teardown, machine/CI type. Set \`protected_acceptance=false\`.
9. In \`finally\` and after crash recovery revoke test credentials, stop containers, securely destroy owned volumes and secrets, and detect leftovers. Expired lease must revoke accessible resources, not just hide records.

**Shared lab supply chain:** use \`baobab-dev\` for user tooling, not as an excuse to couple all native runtime languages into one giant image. Pulse is Python 3.14 and uses its own service; Payments is **Rust** (axum/tokio), layered through its approved devcontainer/tooling; iDempiere is a separate JVM service. Each engine still owns its Dockerfile and native data.

## C. DEV-15 — two qualified first-adopter journeys

### 1. Pulse: \`pulse-intelligence\`

**Source-grounded implemented capability declarations:** \`intelligence.evidence.search@1\` and \`intelligence.research-mission.manage@1\`, provider key \`baobab-pulse.core\`. Implementation/capability declarations **do not** mean CP has activated the provider. Pulse owns PostgreSQL canonical EvidenceSet; Qdrant is a **rebuildable projection**, Haystack is an adapter rather than authority.

**Minimum actual L4 subgraph:** real IAM + CP + baobab-pulse API + Pulse-owned PostgreSQL + Qdrant (and only required messaging/native dependencies). **No CMS, Trade, ERP or Payments prerequisite.** Test enterprise: first-party or the unrelated \`external-client\` API-only synthetic tenant, with a second tenant for cross-tenant denial. Seed evidence using Pulse's owning application/contract API, not by direct modifying CP tables.

**Positive cases:** real IAM workload issuer→CP current Principal/tenant/context→correct Intelligence capability binding/scope→ingest or materialise synthetically sourced canonical evidence→search by classified scope→research mission creation/inspection where implementation is actually callable→traceable provenance and canonical PostgreSQL hydration.

**Negatives/failures:** wrong audience/expired token, disabled Principal, missing intelligence grant, wrong-tenant evidence lookup, insufficient CONFIDENTIAL/RESTRICTED clearance, orphaned Qdrant vector, unavailable Qdrant (honest degraded/block outcome), mismatch of PostgreSQL/Qdrant projections, invalid event context and revoked access. Rebuild projection from PostgreSQL; no vector hit may leak canonical material from a different Tenant.

**Exit:** full real-component own-tenant and negative results with authentic IAM/CP/Pulse operations and **separate** per-capability declaration/availability/certification status; no claims that FX research, LLM quality or regulated recommendations are certified.

### 2. Payments: \`payments-sandbox\`

**Source-grounded declared provider:** \`baobab-payments.sandbox\`, \`simulated=true\`, \`production_permitted=false\`. Capabilities include \`payment.intent.create@1\`, \`payment.intent.cancel@1\`, \`payment.payment.authorize@1\`, \`payment.payment.capture@1\`, and \`payment.refund.create@1\`. The declared sandbox is in-memory and is **not** a real HyperSwitch/PSP settlement certification. Other locally built adapters/journals have separate bounded proof, not automatically part of this sandbox profile.

**Minimum actual L4 subgraph:** IAM + CP + the relevant actual calling workload (prefer an actual baobab-subscriptions test caller or minimal genuine workload using its registered IAM identity) + baobab-payments sandbox + its required native dependencies. **No CMS, Pulse or general commerce frontend.** Use an authorised disposable operating Organisation and a second tenant for denials. Real caller token must be issued by IAM for \`aud=baobab-payments\` with expected scopes (\`payment:execute\`, \`payment:read\`, \`payment:refund\` where used); CP must resolve current legal-actor/context/merchant constraints **for the tested path**. Do not mint/bypass CP authority or infer entitlement from the sandbox result.

**Positive cases:** authorised synthetic intent/confirm/authorise/capture/cancel/refund through actually implemented sandbox routes; correct separate amount/currency/idempotency and contract receipts, **every result explicitly simulated** and no external money movement. Exercise genuinely connected CP resolution only where actual adapter wiring exists; otherwise mark that subcase BLOCKED, not PASS.

**Negatives/failures:** wrong issuer/audience/scope/workload, sibling Tenant, missing or revoked mandate, wrong legal actor/market/currency, over-refund, duplicate idempotency key with changed body, event replay, lost response and retry, untrusted webhook claim and intentionally missing PSP/bank eligibility. No sandbox output unlocks subscription entitlements. No direct money transaction, bank account, merchant/provider activation or actual PSA/KYB asserted.

**Exit:** supported sandbox route operations and actual negative runtime proof, with **simulated payment outcomes**; separate \`PSP_NOT_CONFIGURED\`, \`NATIVE_PAYMENT_NOT_CERTIFIED\` and \`PRODUCTION_BLOCKED\`. A simulated settlement must never count as an actual settlement or pass the provider-protected financial D2 gate.

### Canonical run-level coverage grid (proposed IDs only; do not replace existing INT cases)

| New engineering case group | Pulse | Payments | Must be actually observed at L4 |
| --- | --- | --- | --- |
| ENG-ONB-01 profile parse/contract/schema | yes | yes | valid manifest and negative unknown field |
| ENG-ONB-02 authentic IAM+CP current authority | yes | yes | signed issuer and CP read-back |
| ENG-ONB-03 tenant/legal-actor permission | tenant, data classification | merchant/operating actor | own-tenant positive, sibling denied |
| ENG-ONB-04 canonical capability resolution | intelligence v1 | payments v1 | absent grant/provider not ACTIVE |
| ENG-ONB-05 domain operation | canonical search, mission | simulation-marked payment intent/lifecycle | executed real native engine endpoint |
| ENG-ONB-06 domain security failure | classification/projection leak | replay/duplicate/refund/PSP denial | original relevant PEP denies |
| ENG-ONB-07 process failure/recovery | PostgreSQL/Qdrant | issuer/CP and lost response | no false recover/second money dispatch |
| ENG-ONB-08 cleanup and expiry | full | full | IAM clients, CP lease, DB/volumes gone |
| ENG-ONB-09 evidence classification | real evidence vs mock | real service vs simulated payment | receipt contains provenance, no protected GO |

The new ENG-ONB IDs are **engineering profile criteria**, not aliases for the seven INT-03C or fourteen NAB-03 mandatory cases. Keep those scenario owners and IDs untouched. Implementations can proceed in parallel once real issuer+CP bootstrap is available; **DEV-05 CMS success is not a prerequisite**.

## D. Incremental cross-repository change order

| PR sequence | Owner / repo | Scope | Merge validation |
| --- | --- | --- | --- |
| 1 — descriptor review | Shared | propose and review closed machine-readable profile schema, examples, versioning and security invariants; reuse existing declared providers and enterprise profiles | schema validation + malicious fixture negatives; no altered canonical catalogue |
| 2 — orchestrator | Infrastructure | composition graph, pinned sources, IAM/CP adapter, owned native services, private evidence/teardown, command facade | Actions and Codespaces same profiles; no external credentials; negative startup |
| 3 — developer tooling | baobab-dev | environment compatibility/doctor and lightweight profile tools, exact source image pins | clean Codespaces, Rust feature/Python toolchain check and GHCR noninteractive |
| 4 — Pulse adoption | baobab-pulse + Infra | real Postgres/Qdrant and API adapter/tests linked to profile | ENG-ONB-01..09 applicable actual pass/blocked outcomes; evidence independent of mocks |
| 5 — Payments adoption | baobab-payments + IAM/CP + Infra | real sandbox caller/token/context + payment scenarios | simulation truth; native money/PSP remains fail-closed, no unapproved live movement |
| 6 — generalisation | engine-template + Shared + each engine | optional template and adopter guide; add ERP/Trade/Regulations/Docs/TMS only as native adapters exist | new engine can onboard without editing bespoke IAM/CP/CMS source |

**No global adoption deadline** requires every engine to exist before other code work. First pass may have PARTIAL/BLOCKED profile cells; those states are explicit and do not disable unrelated engines. Dependency-owner PRs shall declare exact Shared SHA/contract and run manifests, so cross-repo drift can be diagnosed and reconciled.

## E. Definition of Done for reusable onboarding

1. A new engine's owner can add a **validated** integration-run descriptor referencing its existing \`.baobab\` declarations and choosing a synthetic tenant, without creating another CP bootstrap, IAM impersonation implementation or per-engine authorisation authority.
2. A developer can run the minimal engine/issuer/CP/native data subgraph, **without CMS unless needed**, in an isolated Codespace and in Actions, with reproducible source/image pins.
3. At least Pulse and Payments report actually observed current-token/CP tenant permission and real engine endpoint results, including mandatory negative/security and correct provider truth (Pulse projection vs canonical DB; Payments simulated money).
4. Failure cleanup, TTL, no cross-tenant leak, no secret disclosure, no production/posting bypass and wrong-environment refusal are automated and independently checkable.
5. Per-capability outcomes distinguish source/test/real-synthetic/protected certification. No generic \`engine_ready=true\` or \`development_pass=>production\` flag.
6. Documentation and templates explain how the next engine plugs in; all upstream source statuses are checked at implementation time, and owners do not silently edit earlier Accepted ADR contracts.

**Delivery status at authorship:** this is a planned implementation profile and adoption path; no CLI, schema file, Pulse/Payments L4 receipt or stage acceptance is claimed by creating this document.
