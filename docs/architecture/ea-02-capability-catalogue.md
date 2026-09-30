# EA-02 — Canonical Capability Catalogue: implementation record

**Governing decision:** ADR-SHARED-017 — Canonical Capability Catalogue, Provider Declaration, Engine Registry and Runtime Capability Convergence (**Accepted — Normative Target Architecture**)
**Supporting decisions:** ADR-SHARED-007, -008, -011, -012, -016; ADR-0020; ADR-BCP-002, -003, -006, -007, -009, -021
**Related, not normative:** ADR-BCP-025, Engine Release, Artifact Identity and Deployment Observation (**Proposed**; not implemented or relied on here)
**Date:** 2026-09-29

This record covers what the first EA-02 implementation cycle delivered, how
it settled the ambiguities it met, and the exact follow-up gates that remain.
The contract details live in `contracts/capability/v1/README.md`.

## 1. Baseline audited (2026-09-29)

| Repository | `main` audited |
|---|---|
| `shared` | `6de807b` |
| `baobab-cp` | `1ae59be` |
| `engine-template` | `f7116d4` |
| `baobab-regulations` | `a625bc0` |
| `baobab-trade` / `-erp` / `-cms` / `-pulse` / `-iam` / `-payments` / `-subscriptions` | `170c54e` / `de39818` / `1d74258` / `004b748` / `6891527` / `03ff405` / `a7a3bf4` |

The audit confirmed the baseline ADR-SHARED-017 described:

- Shared held three capability manifests in three shapes:
  `payments/v1/capabilities.json` and `subscriptions/v1/capabilities.json`
  (combined `EngineRegistration`: definitions plus provider plus support),
  and `trade/v1/capabilities.yaml` (`version`/`capabilities`, with no name,
  domain, lifecycle, maturity or contract majors).
- The Control Plane (`internal/billing/registration.go`) registers every
  embedded path that ends in `/capabilities.json`, so Trade was never
  registered. `RegisterEngine` inserts unknown capabilities
  (`ON CONFLICT (code) DO NOTHING`); provider registration therefore still
  originates canonical vocabulary.
- No engine repository has `.baobab/capability-provider.yaml`.
  `engine-template` had a provisional, schema-less
  `capability-provider.yaml.example` pre-filled with Payments values.
  `baobab-regulations/.baobab/capabilities.yaml.example` was a copy of the
  development-environment template.
- `baobab-payments` (`src/contracts.rs`) and `baobab-subscriptions` read
  vendored copies of their `capabilities.json` bundles, so the bundle shape
  cannot change without coordinated engine changes.
- The only open PR touching these paths is `engine-template#3` (stale
  Foundation CI v2 adoption; it edits `TEMPLATE-USAGE.md`). This cycle adds
  to that file rather than rewriting lines #3 changes.

## 2. What this cycle delivered

| Gate | Delivered |
|---|---|
| 1 Provider declaration schema | `capability/v1/provider-declaration.schema.json`: several providers per engine, several capabilities per provider, contract majors, `PARTIAL`/`IMPLEMENTED`, `simulated ⇒ ¬production_permitted`, logical invocation, provenance, evidence, and planned capabilities kept separate. Closed objects, so it cannot express certification or runtime state |
| 2 Catalogue | `catalogue.schema.json` and `catalogue.yaml` index all 9 existing canonical capabilities; `CapabilityDefinitionDocument` in `capability.schema.json` is the one definition shape |
| 2 Normalization | `payments/v1/capabilities.yaml` and `subscriptions/v1/capabilities.yaml` extracted (WHAT); `trade/v1/capabilities.yaml` normalized in place; the `.json` bundles are unchanged and now transitional (WHAT + WHO) |
| 3–4 Validation | `scripts/capability_catalogue.py` (`validate-catalogue`, `validate-declaration`, `generate-registration`) plus 59 tests in `scripts/tests/test_capability_catalogue.py`, both run by Shared CI |
| 5 Template | `engine-template/.baobab/capability-provider.yaml.example` rewritten against the schema with generic placeholders; `--template` validation |
| 6 Regulations | `baobab-regulations/.baobab/capabilities.yaml.example` removed; engine-template is the scaffold source |
| 8 Discovery | `registration-bundles.yaml` explicitly lists the transitional bundles; CI fails on any unlisted bundle |
| Vocabulary | `implementationKey`, `providerImplementationStatus`, `capabilityProposalStatus`, `implementationEvidenceType`, `architectureDecisionId` and `platformRepository` added; `engineKey` marked deprecated/transitional; `capabilityProviderKey` redefined as `<engine-id>.<provider-name>` |

The existing mapping is:

| Artefact | Canonical WHAT | Provider WHO | Treatment |
|---|---|---|---|
| `payments/v1/capabilities.json` | 4 definitions | `baobab-payments.sandbox` | Definitions moved to `capabilities.yaml`; bundle kept and must equal them |
| `subscriptions/v1/capabilities.json` | 2 definitions | `baobab-subscriptions.temporary-billing` | Same |
| `trade/v1/capabilities.yaml` | 3 definitions | none | Normalized; now registrable once a provider is declared |

## 3. Decisions and contradictions settled

1. **Status.** ADR-SHARED-017 was *Proposed* when Phase 1 landed and has
   since been *Accepted*, so its "SHALL"s now bind the Control Plane and
   engines and the follow-up gates below are normative work, not options.
   Phase 1 itself was additive and changed no runtime behaviour.
   ADR-BCP-025 is still *Proposed*, and nothing here depends on it.
2. **What an Engine is.** ADR-BCP-006 still describes Engine as a
   technology family (`medusa`, `idempiere`). ADR-SHARED-012 and CP
   persistence use the Baobab engine/service (`baobab-trade`). This cycle
   follows ADR-SHARED-012/017: `engine_id` is the engine, `provider_key` is
   the provider, and `implementation_key` is the technology. **ADR-BCP-006
   needs a matching amendment in `baobab-cp`**; it is not edited here.
3. **`engine_key`.** Unchanged in v1 and deprecated. The committed bundles
   keep `sandbox-payments` and `temporary-billing`. The generator maps
   `implementation_key` to `engine_key`, and the round-trip check ignores
   that one deprecated field. A v2 contract removes it.
4. **Envelope.** ADR-SHARED-017 SS19 sketches `schema_version: 1` and SS46
   sketches `schema: {name, version}`. All three new documents use
   `schema: {name, version}`, the envelope the development-environment
   contract already uses.
5. **Provenance.** SS46 writes `provenance.repository`; the task brief and
   SS48 imply an authority object. The schema uses
   `provenance.authority.{repository, decision}`, with `decision` optional
   and an optional `source_revision`.
6. **Trade lifecycle and maturity.** The old Trade manifest declared none.
   Normalization sets `ACTIVE`/`EXPERIMENTAL`, following the only
   precedent (Payments and Subscriptions), and adds names and descriptions
   taken from the Trade README. **Trade owners should confirm these
   values.** They have no runtime effect until a Trade provider registers.
7. **"PARTIAL cannot be promoted" (SS56).** Enforced where promotion
   happens: `generate-registration` registers only `IMPLEMENTED` support.
8. **Owner validity.** Shared has no registry of engines alone. An owner
   must be a `baobab-*` repository name, and the catalogue owner must equal
   the definition owner.
9. **Key identity.** Vendor, tenant and geographic tokens are denied per
   `.`/`-` token. A geographic key that is inherently semantic needs an
   architecture decision and an explicit `GEOGRAPHIC_EXCEPTIONS` entry.
10. **"Every engine should publish `capabilities.json`".** The
    Production-Readiness Assessment (SS56, *EA-02 — Canonical Engine
    Registry*) framed EA-02 this way. ADR-SHARED-017 deliberately refines
    it: engines publish `.baobab/capability-provider.yaml` (WHO), Shared
    publishes definitions indexed by `catalogue.yaml` (WHAT), and neither
    membership nor format is decided by a file name. The assessment's
    `capabilities.json` wording is kept for history and is not a target.
11. **Regulations namespace.** Not registered. ADR-SHARED-017 SS43 calls
    `regulations` a candidate that "SHALL undergo the architecture review
    required by ADR-SHARED-007". The ADR-REG family is also *Proposed*.
    Until that review, Regulations can declare `planned_capabilities` with
    `proposed_key: regulations.*` (the schema allows an unregistered domain
    in a proposal) but no support.

## 4. Follow-up gates

Each gate is independently shippable. Where one depends on another, it
names the dependency.

### G-CP-1 — Index-driven bootstrap (replaces the `/capabilities.json` suffix)

**Status: done** in baobab-cp#218 (merged 2026-09-29), which pins Shared
`66b0178`. CP embeds `registration-bundles.yaml` (`catalogue.yaml` waits
for G-CP-2) and registers exactly the bundles it lists.

*Repository:* `baobab-cp`. *Depends on:* this Shared change merged, and CP
pinning a Shared commit that contains it.

1. Add `contracts/capability/v1/registration-bundles.yaml` (and
   `catalogue.yaml`) to CP's `contracts.lock.yaml` file list, then run
   `make sync-shared-contracts`.
2. In `internal/billing/registration.go`, make `RegisterEmbeddedEngines`
   read `capability/v1/registration-bundles.yaml` and register exactly the
   listed `path`s, checking each bundle's `repository` and `provider_key`
   against the index. Delete the `strings.HasSuffix(path, "/capabilities.json")`
   loop. A listed bundle that is not embedded is a startup error, not a
   silent skip.
3. Tests: the registered set equals the index; an embedded but unlisted
   `capabilities.json` is **not** registered; a listed but missing path
   fails.

### G-CP-2 — CapabilityCatalogueSync

**Status: deployed** in baobab-cp#220 (merged 2026-09-30, sync mechanism)
and baobab-cp#223 (merged 2026-09-30, pinned Shared `a7ca1ed` with 11 capabilities).
CP embeds `catalogue.yaml` and its definition documents and syncs them at startup,
before any provider registers. The sync creates missing capabilities,
updates changed ones by definition digest, refuses domain changes and
removal of a contract major that is still supported, and records
provenance (`canonical_owner`, `canonical_source`, `canonical_digest`,
`canonical_synced_at`). The view `capability.capability_outside_catalogue`
lists rows no sync has projected, for operator remediation. The catalogue now
includes two new capabilities from the EA-02B review (`payment.intent.cancel`,
`finance.order-consequence.process`).

*Repository:* `baobab-cp`. *Depends on:* G-CP-1.

Project `catalogue.yaml` plus its definitions into `capability.capability`
independently of provider registration. Compare canonical revision, update
allowed mutable projection fields (name, description, lifecycle, maturity,
contract majors), refuse incompatible mutation under an unchanged key, and
record `source_digest` and Shared revision (ADR-SHARED-017 SS29). Replace
`ON CONFLICT (code) DO NOTHING`. This covers Trade's three capabilities
and the two new EA-02B keys, which exist in CP independently of provider registration.

### G-CP-3 — Provider registration stops originating capabilities

**Status: rejection deployed** in baobab-cp#222 (merged 2026-09-30, reject
unregistered capabilities) and baobab-cp#223 (merged 2026-09-30, tested
with Payments and ERP registrations against expanded catalogue).
`RegisterEngine` no longer inserts capabilities: every capability, domain and contract
major a registration names must already be in the catalogue projection,
or it fails with `ErrRegistrationOutsideCatalogue` and writes nothing.
The G-CP-2 dependency holds by construction, because CP syncs the
catalogue at startup before any registration. Payments sandbox support for
`payment.intent.cancel` (contract 1) and ERP contracted support for
`finance.order-consequence.process` (contract 1) both register against the
expanded catalogue successfully. **Open:** registering new providers as `DRAFT`. 
It waits for a Changeset path to promote a provider; without one, a fresh 
environment's bootstrap providers would be unroutable.

*Repository:* `baobab-cp`. *Depends on:* G-CP-2 in every environment.

`RegisterEngine` rejects a registration whose capabilities are not already
in the catalogue projection instead of inserting them (SS28, SS59). New
providers register in `DRAFT` or an equivalent non-routing state; promotion
to `ACTIVE` goes through the ADR-BCP-021 Changeset path (SS33, SS65). The
existing sandbox and temporary-billing providers keep today's state.

### G-CP-4 — Binding integrity

*Repository:* `baobab-cp`.

- `capability_binding_active_provider_check` remains `NOT VALID`. Do **not**
  validate it until `capability.binding_without_provider` is empty in every
  environment, which requires an operator remediation run; then add a
  migration `ALTER TABLE ... VALIDATE CONSTRAINT`.
- **Done** in baobab-cp#219 (merged 2026-09-29): `CreateBinding` and
  `SaveBinding` now refuse an ACTIVE binding whose contract major is not
  one of its provider's `provider_capability_support.contract_versions`
  for the capability (`ErrBindingContractUnsupported`). So ACTIVE binding
  ⇒ provider supports the bound capability ⇒ supports its contract major
  (SS36, SS60). Existing ACTIVE bindings are re-checked when next saved as
  ACTIVE. The constraint validation above remains open.

### G-FCI-1 — Foundation CI enforcement

**Status: validation gate delivered; requirement pending.** The reusable
environment job (`reusable-foundation-environment.yml`) runs
`validate-declaration` against the caller's pinned `foundation_ref` whenever
`.baobab/capability-provider.yaml` exists, with the repository name as
`--engine-id`. An invalid declaration fails Foundation. Engines pick this up
when they bump their Foundation pin. Making the file *required* for active
engines is still open, below. All five current declarations (Payments,
Subscriptions, Trade, ERP, IAM) and the engine-template example pass at
Shared `59b577d`.

*Repository:* `shared` (reusable workflow) and engines. *Depends on:* this
change, at least one engine declaration in real use, and lifecycle
semantics reconciled.

Add a reusable Foundation step that runs `validate-declaration` against the
pinned Shared ref with `--engine-id ${repository name}
--repository-root .`, whenever `.baobab/capability-provider.yaml` exists.
Make the file *required* only for `repository.lifecycle: active` engines
with the `engine` trait. Experimental scaffolds may carry a planned-only
declaration. Passing it proves structure, references and evidence
existence; it does **not** mean certified.

### G-02A — Capability census and declarations

**Status: declarations merged, contract work in progress.**
`docs/architecture/ea-02a-capability-census.md` records the survey. Payments,
Subscriptions, Trade, IAM, CMS, ERP and Pulse are surveyed. The declarations
for Payments (baobab-payments#12), Subscriptions (baobab-subscriptions#18),
Trade (baobab-trade#109, planned-only) and ERP (baobab-erp#40, planned-only:
`finance.order-consequence.process` CONTRACTED) are merged. IAM and CMS can
declare now that their capabilities are catalogued; Pulse waits for its
contract (step 5 below). Regulations waits for the G-REG-NS decision.

The EA-02B candidate review (`docs/architecture/ea-02b-candidate-review.md`)
accepted `payment.intent.cancel` and `finance.order-consequence.process`
(catalogue of 11, projected into CP by baobab-cp#223). Contract work steps
2–4 below catalogued five more keys, so Shared's catalogue holds **16**. The
Control Plane projects them once it pins a Shared commit that contains them.

Per ADR-SHARED-017 SS12 and Phase 2, every engine gets a census. Accepted
candidates become catalogue entries through Shared PRs, and each engine then
adds `.baobab/capability-provider.yaml`. Do not bulk-populate declarations
or catalogue entries before the census accepts them. The first natural
adopters are `baobab-payments` and `baobab-subscriptions`, whose
declarations can then generate their bundles.

### Contract work (smallest gaps first)

Keys reserved by EA-02B need Shared request/response contracts before engines
can declare support (`ea-02c-contract-work-plan.md`):

1. **erp/v1 InventoryAvailabilityQuery** — contract DONE (shared#149).
   `inventory-availability-query.schema.json` formalizes the `sku_id` and
   `warehouse_id` query parameters. `inventory.availability.query` is **not
   yet catalogued**: it needs a Shared PR that adds its definition to
   `erp/v1/capabilities.yaml` and `catalogue.yaml`. Until then ERP lists it
   as a `proposed_key` CANDIDATE, as its declaration already does.
2. **buyer-organisation/v1 commands** — DONE (shared#150). Four schemas cover
   apply/evidence/review/decision and invite/accept/revoke/role-update.
   Catalogued: `customer.buyer-application.manage` and
   `customer.buyer-membership.manage`.
3. **identity/v1 authentication profile** — DONE (shared#150), **corrected
   for provider neutrality** by the follow-up to shared#150. Catalogued:
   `identity.authentication.perform` and `identity.workload-token.issue`.
   - As first merged, the workload request fixed `grant_type` to
     `client_credentials` and carried `client_secret` and `realm`. That
     conflicted with the registered `federated_workload_token` workloads
     (`baobab-cp-workload`, `baobab-subscriptions-workload`), which must
     hold no static secret, and with the RFC 7523 path in baobab-iam#42.
   - The corrected contract names the workload, audience and scopes, and
     carries no credential. The mechanism follows the workload's
     `credential_type` behind the provider boundary (ADR-0007,
     ADR-IAM-0019/0020).
   - The human request drops `realm`, and requests assurance as OIDC
     `acr_values` instead of a LOW/MEDIUM/HIGH level.
   - Event names were invented and never defined. They are removed.
4. **content/v1 resolution** — DONE (shared#150). Two schemas formalize the
   ADR-0014 content inheritance. Catalogued: `content.entry.resolve`.
5. **intelligence/v1** — PENDING Pulse's first production domain: contracts
   for research missions and evidence search.

### G-REG-NS — `regulations` namespace review

**Status: open decision.** shared#150 recorded this as resolved against a
Regulations engine. That conclusion is withdrawn, because it would have
settled a fork with the *Proposed* ADR-REG family by implication.
`g-reg-ns-resolution.md` sets out the options and the interim state:
`regulations` stays unregistered, and the Regulations census is paused, not
deferred indefinitely.

### G-06 / G-09 — Events and certification

- **EA-06.** `capability/v1/asyncapi.yaml` already has
  `com.baobab-platform.capability.registered.v1`, `.deprecated.v1`,
  `.retired.v1` and `capability.provider.registered/suspended/retired.v1`.
  The gap is provider-capability **support** events (added, changed,
  retired). They go in the same file under the same convention, e.g.
  `com.baobab-platform.capability.provider-support.added.v1`, never under the
  bare `provider-capability.*` names sketched in ADR-SHARED-017 SS66.
- **EA-09.** `ProviderCapabilityCertification(provider_id, capability_id,
  contract_major, engine_release_id, evidence_digest, status, certified_at,
  revoked_at)`. Every key except the release is explicit in declarations
  today, and the release waits on the accepted successor of ADR-BCP-025.

## 5. Architecture tests

| Scenario | How the model represents it without renaming a capability |
|---|---|
| Procurement extraction | `procurement.sourcing.manage` is supported by `baobab-erp.idempiere`, and later by `baobab-procurement.<provider>` in that engine's own declaration. The key, compositions, grants and consumer contract are unchanged; only provider support and bindings move |
| WMS | `inventory.*`, `logistics.*` and `fulfilment.*` move from the current provider to a WMS provider in the same way |
| Ledger | A future ledger engine declares support for `finance.*` or `settlement.*` keys. The engine id never creates a namespace |
| IAM Keycloak→Ory | One `identity.*` key has two providers, `baobab-iam.keycloak` and `baobab-iam.ory`, in one declaration; ADR-SHARED-016 migrates between them. `keycloak` and `ory` are denied as key tokens |
| Ory Kratos/Hydra | Implementation components beneath `baobab-iam.ory`. Deployment topology is EA-03; neither is an engine or provider by default |
