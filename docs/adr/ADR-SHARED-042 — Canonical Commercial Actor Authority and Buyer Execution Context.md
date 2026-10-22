# ADR-SHARED-042 — Canonical Commercial Actor Authority and Buyer Execution Context

**Status:** **Accepted — Normative Cross-Engine Identity, Commercial Authorization and Execution Architecture**
**Decision date:** 2026-10-21 (implementation ruling on CAA-03/CAA-04 recorded 2026-10-22, §14)
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

**Decision record (22 October 2026) — CAA-03 and CAA-04 implementation ruling.** Decision authority: Baobab Platform Owner. Status: Accepted for architectural implementation. It authorises implementation only: no protected buyer operation is activated, ADR-SHARED-039 seller authority is unchanged, and no draft PR is thereby ready to merge.

1. **CAA-04 — Digital Estate binding.** The Digital Estate behind a buyer request SHALL be established only by a Control Plane attestation of a governed, versioned binding between the confidential estate BFF's registered OAuth client and the estate it serves. The binding holds issuer, `bff_client_id`, `digital_estate_id`, `tenant_id`, `engine_instance_id`, `environment`, `deployment_reference`, status (ACTIVE, SUSPENDED, REVOKED), a monotonic revision, an effective interval and evidence provenance.
   - `azp` identifies the OAuth client. It never, by itself, establishes estate, tenant, environment or Trade instance.
   - Several estates per client are allowed only where each binding is separately governed. An ambiguous match is never resolved by choosing the first record.
   - A client-supplied estate identifier may narrow a selection but never establishes one.
   - The BFF SHALL authenticate to Trade as itself, independently of the human token, so that a stolen buyer token cannot let another caller act as the BFF.
   - Until the contract and its CP implementation exist, a route that needs the Digital Estate returns `UNAVAILABLE`. No environment variable, request header, hostname or commerce session is a substitute.
   - This extends CP's estate-aware context resolution. It is not a second estate registry.
   - Contracts: `control-plane/v1/estate-client-binding.schema.json` and `.openapi.yaml` (scope `estate:client-binding:resolve`), and `identity/v1/buyer-identity-handoff` v1.1 (`BffCallerTokenClaims`, `BuyerOperationHandoffRequest`, scope `trade:buyer-handoff`). Both scopes are allocated to no workload.
2. **CAA-03 — assurance.** Shared publishes the versioned, provider-neutral buyer assurance policy (`identity/v1/assurance-policy.schema.json`). IAM owns the verified evidence and the meaning of its `acr`/`amr` values.
   - A policy is scoped to one trusted issuer and the Trade audience.
   - `acr` values match exactly; no ordering between strings is assumed.
   - Required methods and authentication freshness are enforced where a profile sets them.
   - The operation-to-profile mapping is canonical, so no policy can downgrade an operation.
   - Until the policy and IAM's issuer-backed values are qualified, Trade MAY enforce a configured `acr` allowlist as a strict interim verifier: fail closed, scoped to one issuer and to the operations of a single approved profile, and only with security-approved values backed by IAM evidence. It is never a permissive default.
   - The BFF cannot raise assurance by supplying claims.
   - Missing configuration, unverified evidence or an unavailable authoritative source prevents protected buyer execution.
   - Meeting a profile never by itself establishes permission to buy.
3. **Sequence.** Shared contracts (this record), then IAM assurance normalisation and BFF registration, then CP estate binding resolution, then Trade enforcement, then ZuriBeans BFF handoff and company/Market selection, then Infrastructure real-component acceptance. Tests SHALL prove that each of the following is refused:
   - a wrong estate or environment;
   - a revoked binding;
   - an ambiguous binding;
   - missing or downgraded assurance.

   The derived buyer decision never exceeds 60 seconds or its earliest evidence.

**Decision record (22 October 2026) — CAA-05 buyer operation policy ruling.** Decision authority: Baobab Platform Owner. Status: Accepted for implementation. It authorises implementation only; no protected buyer operation is activated. The absence of a financial or scope restriction is never evidence of permission.

1. **Spend authority.** `trade.order.commit`, `trade.draft-order.finalize` and `trade.quotation.accept` SHALL be denied unless an explicit, active and applicable spend authority exists for the seller Tenant, buyer Organisation, canonical Principal and membership, operation, Market and currency.
   - A missing, inactive, expired or inapplicable record, a `NULL` or a zero is never unlimited authority: `DENY` with `SPEND_POLICY_NOT_CONFIGURED`.
   - An amount above an applicable limit is `DENY` with `SPEND_LIMIT_EXCEEDED`, or `APPROVAL_REQUIRED` only where an independently configured, active approval policy explicitly permits escalation. Missing spend configuration never escalates to approval.
   - Broader organisational policy applies only through an explicit, versioned and governed inheritance rule. A future `NO_PER_TRANSACTION_CAP` mode requires its own documented governance and never overrides credit, budget, legal or seller controls.
   - A Market or currency switch cannot bypass a limit. The evaluator accounts for applicable cumulative or outstanding commitments, concurrent purchases cannot exceed an available balance, and native commit revalidates the authority and transaction version. An unavailable spend-policy source is `UNAVAILABLE`.
2. **Role matrix.** Roles are necessary, never sufficient, and there is no implicit hierarchy: `SENIOR_BUYER` is not an `APPROVER` and `ACCOUNT_ADMIN` holds only its listed permissions. Unknown roles, unsupported operations and missing permissions are `DENY` (`ROLE_NOT_PERMITTED`).

   | Operation | Permitted roles |
   |---|---|
   | `trade.buyer-context.resolve`, `trade.private-catalogue.view`, `trade.contract-price.view` | All six roles (contract price also subject to its visibility policy) |
   | `trade.rfq.submit`, `trade.quotation.accept`, `trade.cart.modify`, `trade.order.commit`, `trade.draft-order.finalize` | `BUYER`, `SENIOR_BUYER`, `PROCUREMENT_MANAGER`, `ACCOUNT_ADMIN` |
   | `trade.purchase-approval.decide` | `APPROVER`, `PROCUREMENT_MANAGER`, `ACCOUNT_ADMIN` |
   | `trade.buyer-member.manage` | `ACCOUNT_ADMIN` only |
   | `trade.buyer-invitation.accept` | The verified invitation recipient; no existing role required |

   Separation of duties is mandatory: no Principal approves a transaction they initiated, whatever roles they hold. Granting elevated roles, changing spend or approval policy, or removing the last active administrator requires additional governance, including independent approval where applicable.
3. **Role-bound Site and Market scope.** Trade owns explicit grants bound to the role assignment, not merely to the membership: a Market grant per role and a Site grant per role, each with status, effective interval, revision, granting Principal, provenance and revocation.
   - No grant, `NULL` or an empty set never means all Markets or all Sites: `MARKET_NOT_PERMITTED` / `SITE_NOT_PERMITTED`, never more specific than `BUYER_NOT_AUTHORISED` for a foreign Organisation.
   - The same role assignment SHALL satisfy the operation, Market and Site; permissions are never composed across roles.
   - A Site belongs to the selected ACTIVE buyer Organisation, is active, is associated with the operation's Market and respects its shipping and billing capabilities. Site and Market grants never imply each other, and new Sites or Markets grant no existing member access.
   - CP remains the Market authority: Trade verifies that the Market is active and permitted for the seller-side Tenant and buyer relationship. Legacy `market_key` values require a governed, exact mapping to canonical CP Market identifiers; names, currencies and country codes are not substitutes.
   - Grant changes atomically advance the membership revision and invalidate derived contexts. Existing memberships receive no scope by migration; legacy access stays unavailable for protected transactions until reconciled through a governed workflow.
   - Market grants are required for every operation except context resolution; Site grants wherever the operation references, selects or binds a Site, including approval of a Site-bound transaction.
4. **Approver authority.** Approval requires an explicit, active and applicable approval limit for the approver's Principal, membership, role, Organisation, Market, currency and operation.
   - Missing, `NULL`, expired or revoked: `DENY` with `APPROVAL_AUTHORITY_NOT_CONFIGURED`, never `APPROVAL_REQUIRED`.
   - An amount above a valid limit, or self-approval, is `DENY` (`APPROVAL_THRESHOLD_EXCEEDED`, `SEPARATION_OF_DUTIES`). No currency conversion or other Market's limit substitutes without a separately approved policy.
   - The limit is revalidated when the decision is made, and the approval is checked for continued applicability before native commit. An unavailable approval-authority source is `UNAVAILABLE`.

`SPEND_POLICY_NOT_CONFIGURED` and `APPROVAL_AUTHORITY_NOT_CONFIGURED` are registered in `trade/v2` `decisionReason` by this record.

**Decision record (22 October 2026) — Decision 5: cumulative buyer spending authority and reservations.** Decision authority: Baobab Platform Owner. Status: Accepted for CAA-05/CAA-06 implementation. It authorises the next engineering increment only; it neither activates purchasing nor certifies the native runtime.

1. **Layered ceilings.** Every applicable ceiling SHALL pass independently, and no role, `ACCOUNT_ADMIN` included, may disregard a cumulative budget:
   - the per-transaction limit (`order_limit_minor`, mandatory, meaning unchanged);
   - a mandatory calendar-month cumulative budget per membership, the baseline for every Baobab Trade deployment;
   - an agreement-specific ceiling, binding when configured;
   - an organisation-wide shared budget, binding when configured.

   A governed escalation policy MAY let an independently authorised approval exceed the per-transaction cap only. Approving one purchase never raises a budget, so a cumulative shortfall is `DENY` (`SPEND_LIMIT_EXCEEDED`), never `APPROVAL_REQUIRED`.
2. **Reservations.** A purchase formally submitted for approval SHALL reserve its full applicable amount from submission. Drafts and unsubmitted quotations reserve nothing.
   - **Holding:** the reservation is held while approval is pending and after approval until commit.
   - **Commit:** at order commit it converts atomically into committed consumption, never counted twice.
   - **Release:** only the verified unused portion is released, on rejection, cancellation, governed expiry or reduction. An increase atomically acquires additional capacity.
   - **Expiry:** an expired hold never authorises commitment.
   - **No restoration:** refunds, returns and historical adjustments do not restore capacity without a separately approved reversal policy.
3. **Period and accounting.**
   - **The period** is a calendar month, never a rolling interval. It has an explicit start, an exclusive end, currency, Market, membership, revision and governing time zone; UTC is the default unless the policy names an IANA zone.
   - **Available capacity** = monthly limit − committed − active reservations. Consumption is authorised purchasing commitment, not cash or invoice settlement. ERP remains the accounting authority and Payments the funds-movement authority; Trade owns the spending-control ledger.
   - **Crossing a month boundary:** a reservation never silently becomes authority in the new month. Trade atomically releases the old-period hold and acquires new-period capacity, and any approval bound to the former period or policy is revalidated.
4. **Engineering model.**
   - **Policy and ledger:** `SpendLimit` is extended, not redefined. A separate versioned budget policy and an append-only reservation and commitment ledger identify the tenant, buyer Organisation, membership, Market, currency, period, transaction digest, resource version, reservation or commitment reference and idempotency key.
   - **Concurrency:** capacity is reserved and the balance updated in one PostgreSQL transaction under database-enforced locking or serializable control. Commands are idempotent, and every applicable member, agreement and organisation ceiling is enforced atomically.
   - **Binding:** reservations bind to one immutable purchase and never move between buyers, Markets or currencies.
   - **Execution fence:** the native Medusa fence verifies a current reservation and the exact transaction before commit; a standalone evaluator ALLOW is insufficient.
   - **Fail closed:** missing policy, ledger balance, canonical Market mapping or transactional guarantee is refused. Missing mandatory budget configuration is `SPEND_POLICY_NOT_CONFIGURED`, insufficient capacity is `SPEND_LIMIT_EXCEEDED`, and an unavailable authoritative source is `SOURCE_UNAVAILABLE`.
5. **Sequencing.**
   - **Shared:** the versioned budget-period, reservation and commitment contracts (`trade/v2/buyer-spend-budget.schema.json`).
   - **Trade, CAA-05 extension:** monthly and agreement budget evaluation, capacity calculation and migrations.
   - **Trade, CAA-06:** atomic reservation and commit transitions, buyer/seller composition and native fences.
   - **CP:** the governed `market_key` → canonical Market mapping and Market attestation.
   - **CAA-08:** real PostgreSQL 17 concurrency, retry, cancellation, rollover, revocation and direct-workflow bypass tests.

   No migration backfills a monthly limit from `order_limit_minor`. Existing members need explicitly governed budget allocation before cumulative-budget-controlled operations are activated.

**Decision record (22 October 2026) — Decisions 6 and 7: native buyer-commitment coverage and spend valuation.** Decision authority: Baobab Platform Owner. Status: Accepted as an ADR-SHARED-042 CAA-06 implementation clarification. They close two policy questions; they neither certify an implementation nor activate an unqualified native order path. Two rules underlie both: buyer authority follows the commercial obligation, not the API or workflow that creates it; and spending authority covers the buyer's complete contractual purchase amount, not the merchandise subtotal or the amount paid now. They apply across Baobab Trade's B2B digital estates, beginning with ZuriBeans, and impose no B2B membership requirement on B2C commerce (Thamani).

1. **Decision 6 — which native commitments need buyer authority.** Every B2B native transaction that creates a binding purchase obligation on behalf of a buyer Organisation SHALL require current buyer authority, a valid `BuyerAuthorityReceipt` and a matching current spend reservation, consumed at the native database commit fence.
   - **Classes:** all three activatable Trade-A order classes, `trade.order.commit` (cart checkout), `trade.order.create` (direct order creation) and `trade.draft-order.finalize` (draft conversion), each needing a buyer receipt and a reservation. This holds whether execution starts from a Store or Admin API, a Medusa workflow, a background job, a callback or an internal service. There is no `trade.order.create` bypass: it is added to the buyer-operation catalogue, the buyer assurance mapping (`BUYER_COMMITMENT`) and the receipt contract, and stays disabled for B2B until Trade qualifies it.
   - **Quotation acceptance:** `trade.quotation.accept` needs buyer authority and a reservation when acceptance creates a binding purchase obligation, even if the order record follows later. The later order carries that reservation forward through verified transaction lineage; it never consumes budget twice.
   - **RFQs and non-binding quotations** consume no budget merely by existing. A formally submitted request that constitutes a governed purchase commitment follows Decision 5's reservation rule, and the versioned operation policy states the legal and commercial effect explicitly.
   - **Seller-created drafts:** a seller may prepare a non-binding draft under separately appropriate authority, but may not convert it into a binding B2B order without independently established buyer authority.
   - **B2C:** the B2B receipt and membership-based reservation are not required merely because an order uses the shared Trade engine. B2C keeps its own buyer, seller, payment and native-execution controls.
   - **Fence invariant:** for every B2B commitment Trade SHALL prove that a current `ALLOW` buyer receipt, a current independently authorised seller receipt, an ACTIVE reservation at the matching hold revision and the verified canonical buyer Organisation, Principal, membership and Market describe the same transaction: the same operation reference, native resource version, currency, amount, valuation and transaction digest. The order insert or binding status transition, both receipt consumptions and the reservation's conversion to committed consumption succeed or fail in one PostgreSQL transaction. Workflow validation alone is insufficient, and commands that open their own transaction must participate in the native order's transaction before claiming this guarantee.
   - **Classification:** missing or ambiguous B2B classification denies; it never falls through to the B2C path. It derives from trusted, persistent estate and commercial-relationship evidence, never browser metadata or a sales-channel name. No migration, importer, administrative tool or exceptional order process may create a B2B order without its own explicitly governed and certified operation, or silently claim a B2C exemption.
2. **Decision 7 — which amount is reserved and committed.** Decision 5 spend control reserves and commits the finalised, authoritative gross buyer purchase obligation, net of genuine commercial price reductions, in the transaction currency's minor units. It is named `buyer_commitment_amount_minor` in `trade/v2/buyer-commitment-valuation.schema.json` and populates `amount_minor` of the execution context, the buyer receipt and the spend reservation, each also binding its `valuation_digest`.
   - **Included:** merchandise after valid item-level discounts; order-level commercial discounts, deducted once; freight and shipping, handling, insurance and service charges billed to the buyer; transaction taxes payable through the order; customs duties and import charges billed through the seller under the agreed Incoterm; refundable deposits charged as part of the new obligation.
   - **Excluded:** gift cards, wallet balance, tender credits and payment already collected never reduce it, and the seller's own non-chargeable expenses are never part of it. A genuine seller-issued price adjustment can reduce the obligation; a payment instrument cannot. Example: R40,000 merchandise, a R2,000 discount, R2,000 shipping and handling and R6,000 VAT commit R46,000, even if R10,000 is paid now and the rest on approved credit terms.
   - **Authoritative source:** a mutable `cart.total` is never trusted alone. The amount is calculated or independently reconciled from the finalised native pricing, tax, discount and fulfilment facts with currency-safe integer arithmetic.
   - **No speculative authorization:** an undetermined tax, freight, duty or other buyer-payable charge needs an authoritative final quotation or a separately governed maximum-price commitment; an estimate never authorises an order.
   - **No currency substitution:** the amount is reserved in the exact transaction currency against that currency's Market and budget policies. Cross-currency aggregation needs its own governed FX contract.
   - **No repricing after authorization:** a material change to quantity, negotiated price, discounts, taxes, shipping, currency, Site or Incoterm is a new valuation, digest and authorization evaluation. An increase needs additional capacity; a reduction follows governed replacement and release.
   - **Reserve once, commit once:** when a binding quotation already holds the reservation, conversion to a native order preserves the verified lineage and never creates a second reservation or reuses the earlier receipt for a different operation.
3. **Engineering requirements.**
   - **P0, Shared:** cover `trade.order.create` in the buyer receipt, buyer-operation catalogue and assurance mapping; publish the valuation contract with its amount breakdown and digest rule.
   - **P0, Trade:**
     - an authoritative B2B/B2C classification the caller cannot change;
     - composition of the buyer receipt, seller receipt and reservation inside the native PostgreSQL commit transaction;
     - the same validated amount, currency, revision, valuation and transaction digest across the reservation, both receipts and the native order.
   - **P1, Trade:**
     - qualify binding quotation-to-order transitions and amendment/repricing;
     - test the direct API, native workflow, callback, background job, duplicate request, concurrent commit and raw-SQL bypass paths.

   An absent, stale, mismatched or unverifiable authority or valuation SHALL prevent commitment.
