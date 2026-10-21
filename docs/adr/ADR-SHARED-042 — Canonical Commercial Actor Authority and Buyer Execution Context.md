# ADR-SHARED-042 — Canonical Commercial Actor Authority and Buyer Execution Context

**Status:** **Accepted — Normative Cross-Engine Identity, Commercial Authorization and Execution Architecture**
**Decision date:** 2026-10-21
**Decision authority:** Baobab Platform Owner (explicit approval, 21 October 2026)
**Authority home:** `baobab-platform/shared/docs/adr`
**Scope:** All first-party and governed external consumers of Baobab Trade; first adopter ZuriBeans B2B. B2C-specific policies remain independent.
**Implementation state:** `ARCHITECTURE_ACCEPTED` only. No registration endpoint, capability grant, IAM client, protected runtime, production buyer, live trading permission or product release is activated by this ADR.
**Reconciles, does not repeal:** Accepted Shared ADR-SHARED-017/021/035/036/039/040/041; CP ADR-0004, ADR-BCP-004/014/016/018/024/026/027; IAM ADR-IAM-0023/0033 and the IAM buyer-access ruling; existing Shared `identity/v1/buyer-identity-handoff`, `buyer-organisation/v1`, `control-plane/v1/platform-context` and `trade/v2` contracts; Accepted Shared EA Plan v2.3; ZuriBeans Go-Live Masterplan v2.0.
**Normative vocabulary:** SHALL / MUST is mandatory; SHOULD requires a documented justified exception; MAY is optional within existing authority.

## 1. Problem, decision and scope

A human may authenticate successfully with Kratos/Hydra and possess a valid Trade-audience access token but have no CP Principal, no verified company relationship, no active Trade membership or no permission for the desired purchase. Conversely, a buyer can belong to multiple companies and have different roles, sites, markets, approvals and spending limits in each. A Medusa customer and a seller's CP workload identity cannot fill the missing authority.

**Decision:** The platform SHALL establish a **Commercial Actor Authority Binding**:

```
IAM-verified human or authorised machine identity
  -> CP canonical Principal and active ExternalIdentity / workload identity
  -> expressly selected, CP-attested canonical buyer Organisation
  -> Trade buyer Organisation and current commercial membership or delegated mandate
  -> current operation-specific Trade policy
  -> independently current CP market/capability/context and seller-of-record mandate
  -> bounded buyer decision + applicable seller decision + native execution fence
```

Trade SHALL derive a `TradeBuyerExecutionContext` from these independent facts. This is **a derived, purpose-bound Trade execution object**, not a new global identity, not a CP PlatformContext, not a bearer credential, not a claim the browser can mint, and not perpetual purchasing authority. An IAM token with `trade:buy` requests consideration; it grants no company access.

This decision governs protected B2B account/catalogue/contract-price access, invitations, RFQs, quotations, carts, approvals, orders, background continuations and all eventual native mutations. It provides a reusable foundation for other Baobab Trade tenants without imposing B2B membership semantics on B2C consumers.

## 2. Non-negotiable authority separation

| Fact or decision | Authoritative owner | Consumers / prohibition |
|---|---|---|
| Human session, trust, token status, assurance; workload credentials | IAM (Kratos/Hydra first; Keycloak federation/transition) | ZuriBeans BFF and Trade verify evidence; no Medusa-only platform identity |
| Canonical human/workload `Principal`, `ExternalIdentity` and identity references | CP | Trade resolves; never mints or links a canonical person |
| Canonical Organisation and tenant-to-Organisation attestation | CP | Trade supplies requested company as *untrusted intent* |
| Tenant, Market, Digital Estate, legal actor, CP capabilities, binding, provider/instance | CP and the relevant independently governed legal/evidence authorities | Trade may not infer buyer tenancy from a seller workload or a browser header |
| Tenant-scoped buyer account, `BuyerMembership`, member role, commercial approval/spend policy | Trade | CP does not confer buying permission merely by attesting an Organisation |
| Engine-native customer, cart, RFQ, quotation, order and transaction history | Trade/Medusa | Medusa IDs are scoped references, not canonical identities |
| Seller Operating Binding, current seller mandate, legal activity authorization | CP under ADR-SHARED-039 | A positive buyer decision never substitutes for seller authority |
| Credit, accounting, receivables and posting | ERP; relevant governed financial evidence | Trade cannot turn credit projection into a cash-movement or journal authorization |
| Money movement and settlement | Payments/approved provider under ADR-SHARED-035 | Trade payment intent is not funds-transfer authority |
| Regulatory source/evaluation, documentary issuance and physical transport | Regulations, Trade Docs and TMS/qualified providers as applicable | Their independent vetoes remain operative |
| User interface and private session custody | Digital Estate confidential BFF | No authority decision minted in browser, cookies or UI |

`Principal`, `ExternalIdentity`, canonical Organisation, Trade BuyerOrganisation, BuyerMembership, Medusa customer, Tenant, Digital Estate, Market and seller LegalEntity are distinct typed identifiers. Corporate-group relationship, IAM organisation projection, common PlatformAccount, matching email/domain and a historical order SHALL NOT confer another organisation's access.

## 3. Identity and evidence handoff

The confidential estate BFF SHALL retain the IAM human access token on the server. It SHALL hand off the subject evidence for an explicit Trade operation under the existing Shared `identity/v1/buyer-identity-handoff` semantics. Trade verifies issuer, signature or approved introspection, `aud=baobab-trade`, `actor_type=human`, registered `azp`, scope, expiry, session/revocation and required assurance. An ID token, Medusa JWT, unverified `principal_id`, email or user-supplied role never substitutes for the human access token.

Trade SHALL authenticate its separate request to CP as an ACTIVE registered **workload**, with a CP-audience workload credential and exact least-privilege grant. It SHALL transmit the human evidence as a separately typed *subject-evidence* input over authenticated TLS. CP SHALL independently verify that subject evidence through a registered validator relationship, explicitly scoped to the expected Trade audience, before resolving the canonical Principal. **A human Trade-audience token MUST NOT be accepted as the CP API caller credential.** Subject-token validation MUST NOT import its `tenant_id`, `organisation` or `role` claim as authorization. IAM-managed OAuth token exchange to a CP-audience delegated subject token MAY replace raw subject-evidence transport after separate certification; no homemade on-behalf-of tokens.

The existing CP `/v1/platform-context/resolve` remains the **workload-owned context** for the consuming Trade service. The CP context's workload Principal SHALL NOT be represented as the human buyer Principal. The new human evidence and Trade binding SHALL be joined **in Trade only**, with CP independently attesting the canonical Organisation and seller/runtime context.

A new strictly scoped CP read operation SHALL resolve verified `(issuer, subject)` to an ACTIVE human Principal and ACTIVE ExternalIdentity. This SHALL NOT reuse the privileged, platform-wide `/internal/federation/v1/identity` reader as a general Trade people-directory service; a buyer-purpose API requires specific registered caller, issuer/client/audience and data-minimisation policy. Unknown, mismatched, suspended, revoked, inactive or unavailable facts deny. Its exact route, contract, scoped capability and error vocabulary are CAA-01 deliverables, **not yet registered** by this ADR.

## 4. First-login Principal policy — narrow, atomic and non-authorising

Buyer onboarding SHALL support a **separate governed just-in-time registration operation** for eligible authenticated humans. Ordinary read-only resolution SHALL never provision silently. Registration must prove trusted issuer, active subject token, registered BFF client, approved onboarding purpose, authorised Trade workload, abuse/rate limits and the absence of suspension, revocation, identity-link conflict or another prohibited previous identity.

CP SHALL create one canonical Principal + one ACTIVE ExternalIdentity bound to the exact `(issuer, subject)` **atomically** with durable audit/outbox and a uniqueness constraint. A concurrent first login MUST return the same winner without an orphan Principal, duplicate link or duplicate event. This expressly requires correcting `IdentityService.Resolve`'s current create-then-link race behaviour before enabling the buyer policy. Account linking, recovery or federated-provider migration requires independently verified subject-link evidence; equal emails never auto-link.

JIT creates **identity only**. It SHALL NOT create a verified company, ACTIVE membership, Tenant, role, platform grant, commercial credit limit, buyer approval or permission to place an order. An authenticated but unmapped human may access only the safe onboarding activities independently authorized for that purpose.

## 5. Canonical Organisation and Trade relationship

An ACTIVE Trade B2B buyer account used for protected transactions SHALL have an attested link to the exact CP canonical Organisation. The Trade relationship SHALL retain `buyer_organisation_id`, `canonical_organisation_id`, seller-side `tenant_id`, Trade engine instance, status, effective version and provenance. The same canonical Organisation MAY have separate, independently scoped buyer accounts at different sellers/tenants.

CP SHALL verify a currently ACTIVE permitted Organisation relationship for the **seller-side trading Tenant** (including the accepted ADR-BCP-018 TenantOrganisationMapping semantics) rather than assuming the buyer has a Baobab Tenant or that the ZuriBeans Tenant's PRIMARY Organisation is the buyer. CP attestation establishes legitimacy of the context **only**; Trade independently resolves buyer-account activity, commercial relationships and membership.

Legacy `BUYER_ORGANISATION` / `SUPPLIER_ORGANISATION` records SHALL follow their explicitly accepted compatibility rules pending governed reconciliation to generic `ORGANISATION`; this ADR does not override CP ADR-BCP-016/018/024 exact-kind decisions or create a duplicate canonical Organisation. Missing, conflicting, expired or uncertain mappings deny protected buying and enter controlled reconciliation; no fuzzy auto-merge.

## 6. Binding a human to current Trade membership

Trade SHALL load a `BuyerMembership` within the correct seller Tenant and Trade BuyerOrganisation and prove:

1. Membership status ACTIVE, currently effective, neither revoked nor superseded.
2. Its `principal_id` is exactly the canonical human Principal resolved from the authenticated subject.
3. Its `buyer_organisation_id` is the explicitly selected and currently ACTIVE Trade account.
4. That account maps to the CP-attested canonical buyer Organisation.
5. Current roles, sites, markets, spend/approval limits, PO requirements, contractual conditions and resource/operation restrictions permit the requested action.
6. All underlying actor, session, tenant, estate, binding and legal requirements remain valid.

Membership's `customer_id` is a separate native commerce mapping. It MAY be present to drive Medusa workflows but SHALL NOT establish identity or membership on its own. Canonical-to-Medusa mappings SHALL carry provider/instance scope, be idempotent and exclude blind email linking.

Trade SHALL bind invites only on acceptance by the currently authenticated canonical Principal. The existing Shared request `principal_id`, if present, MUST equal that server-resolved Principal; it is never a self-asserted authority. Invite issuance and consumption SHALL be one-time, expiry-bound, replay-safe, auditable and constrained to granted role/site scope. No invite delivers a reusable session or access token.

A buyer with several memberships SHALL explicitly select an acting company before consequential actions. The browser selection is intent only. The server SHALL NOT infer it from default customer, email domain, corporate parent or previous cart. Switching Organisations invalidates the derived actor context; cart/quote/contract pricing/approval remain bound to the original Organisation, and cross-company transfer is denied absent a separately governed transaction.

## 7. Derived TradeBuyerExecutionContext and operation decision

Trade SHALL assemble the following **logical contract** from validated evidence; Shared CAA-01 SHALL publish its formal versioned schema before runtime adoption.

| Field / group | Rule |
|---|---|
| `context_id`, `decision_id`, `correlation_id` | Unique decision lineage; distinguish from CP `context_id`; correlation IDs follow existing Shared UUID rule |
| `actor_type`, `actor_principal_id` | Verified HUMAN or WORKLOAD identity; human from CP resolution |
| `external_identity_id` / `delegation_reference` | Validated human link or approved workload mandate, not both inferred |
| `tenant_id`, `digital_estate_id`, `market_id`, `engine_instance_id` | Authoritatively resolved consuming context, exact resource scope |
| `canonical_organisation_id`, `buyer_organisation_id` | CP-attested buyer company + Trade commercial relationship |
| `buyer_membership_id`, `membership_revision` | Required for human B2B membership policy; not invented for machines |
| `seller_legal_entity_id`, `seller_binding_reference` | Independently established seller execution authority |
| `cp_context_id`, `capability_decision_reference` | Current bounded CP runtime/capability context |
| `operation`, `resource_id`, `resource_version`, `transaction_digest` | Exact requested action and immutable commercial facts |
| `policy_revision`, `approval_references`, `decision` | Evaluated Trade policy and applicable independent approvals |
| `evaluated_at`, `expires_at`, `evidence_references` | Bounded lifetime and redacted upstream provenance |

Only the server constructs the context. No browser, direct client, Medusa customer JWT or background job may submit it as a source of truth. A positive decision SHALL require all applicable IAM, CP, Trade, seller and independent financial/regulatory preconditions; an `APPROVAL_REQUIRED` decision is **not** executable purchase permission.

A proposed maximum **60-second lifetime** for a derived buyer decision is a ceiling for contract design, **not** a grace period for revoked authority or a substitute for fresh consequential checks. Formal freshness, invalidation and retry contracts SHALL be documented before activation; the current seller CP decision remains bounded under ADR-SHARED-039 (at most 30 seconds). No derived buyer decision may outlive its earliest required evidence.

## 8. Operation-specific authority, approvals and delegation

Trade SHALL maintain explicit operation policy for private pricing, catalogue exposure, RFQ submission, quote acceptance, cart modification, order commitment, draft finalization, administrative writes, fulfilment and payment-related transitions. Roles (`BUYER`, `SENIOR_BUYER`, `APPROVER`, `PROCUREMENT_MANAGER`, `ACCOUNT_ADMIN`, `VIEWER`) are **inputs** to scoped policy, never universal permission or platform grants.

Trade SHALL independently enforce separation of duties whenever required: a buyer cannot approve their own transaction by switching a role, account or user interface. Approvals bind initiating and approving canonical Principals, required approver distinctness, the exact Organisation, amount/currency, Market, cart/quote version, digest, policy revision and valid effective interval. Any material change to buyer, company, seller, line, quantity, negotiated price, currency, tax/Incoterm or transaction scope invalidates relevant approval and requires re-evaluation.

Future ERP procurement integrations and autonomous agents SHALL be registered **workload** Principals with their own current, explicit, revocable Organisation mandate and operation limits. They SHALL NOT impersonate humans, borrow a user's BuyerMembership or fabricate a human Principal. Their commercial delegation and machine authority form a separate profile under the same decision model and require their own versioned contract before activation.

## 9. Native execution, immutability and seller/buyer composition

**Buyer ALLOW alone does not execute a transaction. Seller ALLOW alone does not execute a transaction.** Trade SHALL compose both on the exact operation, bound resource version, digest, Market, seller legal entity, current mandate and CP capability/binding.

Existing ADR-SHARED-039 seller-authority, `trade/v2` operation catalogue, TA-05/TA-07 receipt persistence and TA-08 real-runtime acceptance remain binding and SHALL NOT be bypassed or repurposed. Buyer-authority receipts are separate auditable facts to be integrated with those same native entry and commit fences through a reviewed contract and migration; this ADR does **not** claim that buyer fences already exist.

At consequential execution (Store/Admin HTTP routes, native Medusa workflows, payment callbacks, direct order creation, draft conversion, background retries and database commit), Trade SHALL require current applicable authority and a purpose-bound receipt tied to the exact immutable operation facts. Receipt replays, mismatches, expiration, cross-tenant references, bypass by direct workflow/SQL or unauthorized reuse MUST deny. A webhook/job SHALL use a separately governed continuation authorization or transaction intent, not replay an old browser session as fresh human authority.

An authority change after cart creation and before order commitment SHALL trigger re-validation. Withholding or losing required CP/IAM/Trade evidence SHALL not be softened to success. **No new native operation class is activated by this ADR:** TA-08 staging-only certifications and production deny posture remain unchanged.

## 10. Revocation, isolation, resilience and privacy

Immediate user/member/role/delegation revocation must prevent new protected actions under the current-source and commit-freshness contract. IAM session, token or Principal status; canonical Organisation relationship; Trade account/membership; seller binding/mandate; Tenant, Market, capability or legal permission may each veto independently. Events SHOULD accelerate invalidation, but asynchronous delivery is not sufficient standalone proof: enforce bounded authoritative freshness at the consequential point. Reconciliation SHALL tolerate duplicate, delayed and reordered events.

Cross-service state changes are not globally ACID. Implementers SHALL describe the revocation/commit race window, verify it in real components, and deny or compensate operations where the platform cannot prove the required guarantees. An unresolved source, split-brain mapping, stale registry, timeout or missing receipt is DENY or retryable UNAVAILABLE (never ALLOW).

Protected data queries SHALL filter by tenant, Organisation and relevant estate before access; opaque not-found responses MUST not reveal foreign records. Audit SHALL preserve canonical actor, acting Organisation, role/delegation, decision/receipt versions, initiator/approver separation, selected Market, seller legal entity, exact operation and correlation; it SHALL exclude access/refresh tokens, credential material, payment secrets and unnecessary PII. Identity or membership revocation never rewrites historical financial/order attribution. POPIA and applicable jurisdictional data controls and retention remain independently binding.

## 11. Failure semantics and compatibility

| Condition | Required outcome |
|---|---|
| Login valid, no CP Principal | Registration eligible only through narrow onboarding policy; no buying until active membership |
| Wrong issuer, audience, actor type, client, scope, token status or CP workload grant | Deny |
| CP / IAM necessary authoritative source unavailable | Retryable unavailable or deny; no protected mutation |
| Suspended/revoked Principal, ExternalIdentity, membership, Organisation, tenant, grant or mandate | Deny |
| Missing buyer company selection or company/membership mismatch | Selection required / deny; no disclosure of foreign resource |
| Approval threshold exceeded / SoD violation | Approval required / deny; not order commit |
| Changed transaction digest/version or stale buyer receipt | Invalidate, re-evaluate or deny |
| Seller binding absent or suspended | Deny even if buyer is fully authorised |
| Replayed invite, authorization receipt or command | One-time consumption / idempotent original result / bounded conflict |
| Migrated Medusa customer with no verifiable Principal link | Quarantine for reconciliation, no implicit elevated rights |

Existing customer, membership and cart records SHALL not be auto-promoted to canonical authority. Reconciliation uses verified identity/organisation evidence, preserves order history, does not fuzzy-merge records, and follows versioned adoption/rollback plans. Existing Shared v1 contracts and consumer pins SHALL remain valid until a **separately reviewed** versioned migration; this ADR registers no live capability or route by implication.

## 12. Mandatory engineering work packages and acceptance

All packages are **outstanding unless independently evidenced**; implementation shall proceed in dependency order with cross-repo parallel work where boundaries permit.

| Gate | Authority | Exit evidence |
|---|---|---|
| CAA-01 — canonical schemas/census | Shared | Versioned commercial-actor, Principal-register/resolve, delegated evidence, decision/receipt and negative-path contracts; no unregistered capability key |
| CAA-02 — human Principal lifecycle | CP | Atomic JIT creation + strict read-only resolution, non-orphaning concurrent requests and governed scopes |
| CAA-03 — IAM subject evidence | IAM + ZuriBeans | Real Kratos/Hydra confidential-client issuance, token validation/revocation, Trade vs CP audience separation |
| CAA-04 — canonical-commercial linkage | CP + Trade | Attested Organisation↔Trade account, Principal↔membership and engine-native customer mappings, invalid links refused |
| CAA-05 — buyer evaluator | Trade | Active roles, membership, multi-company context, SoD, spending/site/Market policies, invites and revocation |
| CAA-06 — native transaction protection | Trade + CP | Buyer/seller decision composition and current immutable receipt consumption at actual native commit |
| CAA-07 — estate adoption | ZuriBeans | BFF/server-side client, onboarding and company selection; RFQ/cart UI only when individually qualified |
| CAA-08 — release acceptance | Infrastructure + owners | Shared EA v2.3 evidence: isolated negative tests, real signed tokens, actual CP/Trade/PG17 execution, L4 and independently protected staging |

At minimum, regression and real-component tests SHALL cover: first sign-in and concurrent first sign-ins without orphan records; federated identity linking without email auto-merge; wrong issuer/audience/client; unknown/revoked human and workload; two-company switching; foreign Tenant/Organisation/Market access; suspended company/membership; invitation spoof/replay; elevated roles and self-approval; spend and PO checks; cart edits after approval; seller mandate withdrawal; CP outage; revocation immediately before commit; stale/duplicate receipts; HTTP/Medusa direct-workflow/background and raw-SQL bypass; idempotent retry; positive legitimate checkout with matched buyer/seller evidence; token/PII-free events and logs.

**Acceptance ladder:** `ARCHITECTURE_ACCEPTED` is not `CONTRACT_ACCEPTED`, `SOURCE_MERGED`, `LOCAL_TESTED`, `REAL_COMPONENT_SYNTHETIC_DATA`, `PROTECTED_STAGING`, `EXTERNAL_CERTIFICATION` or `PRODUCTION_ACCEPTANCE`. No skipped scenario is a pass. The Accepted EA v2.3 and its retained v2.2 L4 scenario ID matrix govern evidence and release; no local L4 IDs are fabricated.

## 13. Final normative invariant

> **No protected Baobab Trade operation SHALL execute unless its authenticated actor, canonical Principal, selected and CP-attested buyer Organisation, active commercial membership or independently governed machine mandate, Trade operation policy, market/tenant/estate capability context, seller-of-record legal authority and any further operation-specific requirements are independently verified, mutually consistent, current and bound to the exact execution. A missing, revoked, mismatched, expired or unavailable mandatory authority SHALL prevent consequential execution.**

Commercial authority is **derived and verified, never inferred, inherited or manufactured**.

## 14. References and decision record

- Shared: `contracts/identity/v1/buyer-identity-handoff.schema.json`, `contracts/identity/v1/principal.schema.json`, `contracts/buyer-organisation/v1/`, `contracts/control-plane/v1/platform-context.schema.json`.
- CP: ADR-BCP-014/016/018/024/026/027, `internal/service/identity_service.go`, `internal/domain/organisation_attestation.go` and the existing restricted federation authority source (not a Trade directory).
- Trade: `docs/architecture/zuribeans-b2b-commerce.md`, `src/modules/b2b/models/`, `docs/plans/trade-a-ta08-real-runtime-acceptance.md`.
- ZuriBeans: `docs/adr/0015-iam-confidential-bff.md` (estate implementation ADR remains Proposed until independently adopted), `docs/go-live/ZB-GOLIVE-MP-001.md`.
- Shared architecture: ADR-SHARED-039 order/seller authority; EA Implementation Plan v2.3, EA v2.2 retained L4 matrix.
- OAuth 2.0 Token Exchange (RFC 8693) and OAuth 2.0 Security Best Current Practice (RFC 9700) guide optional delegated token transport. No token-exchange capability is assumed active.

**Decision record (21 October 2026):** Platform Owner explicitly directed **Accepted** status and publication by PR, with merge only after mandatory CI/reviews pass. Architectural acceptance authorizes implementation planning, **not** provisional buyer or seller trading activation.
