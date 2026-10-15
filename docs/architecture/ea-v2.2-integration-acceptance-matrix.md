# EA v2.2 — Mandatory L4 cross-engine integration and acceptance matrix

**Status:** Accepted programme test inventory under EA v2.2 and ADR-SHARED-036; suite implementation not yet completed  
**Date:** 15 October 2026  
**Authority:** [EA v2.2](EA-implementation-plan-v2.2-ADR-SHARED-036-integration-reconciliation.md); [ADR-SHARED-036](../adr/ADR-SHARED-036%20%E2%80%94%20Cross-Repository%20Integration%20Testing%2C%20Tenant-Neutral%20Consumption%20and%20Production%20Deployment.md)  
**Test owner:** Infrastructure orchestrates; component/resource-server owners define and maintain assertions; Security independently reviews denial and custody tests.

## 1. Evidence rules

Every profile SHALL report PASS, FAIL, BLOCKED or NOT_APPLICABLE **per scenario**. NOT_APPLICABLE requires a profile schema exclusion and owning-authority approval, never an automatically skipped required scenario. A mandatory BLOCKED or missing result fails profile acceptance. All HTTP calls shall target actual version-pinned processes if labelled REAL_COMPONENT_SYNTHETIC_DATA; independent protected staging requires actual approved deployments and credentials. All positive cases must establish an actual durable or correctly observed allowed action. All negative cases must prove the prohibited consequence did not occur, not merely a 403 in an unrelated endpoint.

Run manifest records exact engine commits, OCI digests, contract versions, real/mock boundary, databases, Principal/Tenant fixture lineage, runtime region (if protected), scenario IDs, execution time, correlation/traces, sanitised logs, failure causation, evidence digest, signature/custody and approvals. Source/test notes do not grant legal or financial operational authority.

## 2. Universal L4 mandatory tests

| ID | Positive assertion | Mandatory negative/failure assertion | Owner | Minimum profile |
|---|---|---|---|---|
| L4-MAN-01 | Every source, schema and image equals lock manifest | Floating ref, missing checksum, wrong digest, compromised dependency denied | Infrastructure/Shared | ALL |
| L4-MAN-02 | The same runner commands work in Codespace and Actions | Missing Docker, executable bit, resource budget or required health probe fails before launch | Infrastructure | INT-01 |
| L4-MAN-03 | Separate ephemeral project network, TLS test CA and broker/DB role | No exposed management port, cross-run credential reuse or unexpected outbound network | Infrastructure/Security | ALL |
| L4-MAN-04 | Scrubbed evidence receipt includes every required test ID | Missing mandatory result, token/password/PII leak or missing cleanup fails | Infrastructure/Security | ALL |
| L4-IAM-01 | IAM-issued human code+PKCE OIDC, signed issuer, correct audience, nonce, single-use state/code | Forged signature, wrong issuer, rejected callback, replay, expired token | IAM/estate | INT-02/03 |
| L4-IAM-02 | Issued workload token limited to registered client and resource audience/scope | Cross-audience, nonactive client, mismatched claims and revoked token denied | IAM/Shared/provider | INT-02 |
| L4-CP-01 | Actual CP canonical Principal / PRIMARY Organisation / Tenant / market context read | Missing or fabricated Organisation, swapped Tenant, unmapped principal, revoked grant denied | CP | INT-02 |
| L4-CP-02 | Entitled capability resolves to current certified provider/EngineInstance | Missing grant/binding, wrong market/instance, stale provider or invalid isolation denies | CP/owner | INT-02 |
| L4-CP-03 | Parent, independently governed subsidiary, sibling and external user see only permitted records | Group ownership, PlatformAccount and self-asserted Tenant do not grant neighbour access | CP/engines | INT-02/07 |
| L4-CP-04 | Correct legal actor scoped to role/activity/market/time where required | Expired/revoked/ambiguous or user-overridden actor; no pending action succeeds | CP/provider | INT-02/08 |
| L4-ENG-01 | Domain resource server executes allowed operation and durable state/event owner records receipt | Gateway-only authentication cannot bypass provider PEP; no cross-engine DB read | Owning engine | Profile-specific |
| L4-OPS-01 | Real token/CP/provider/broker failure produces safe bounded error and recovery path | No fallback provider, duplicate irreversible command, stale cache grants or leaked record | CP/engines/Infrastructure | Profile-specific |

## 3. Consumer-specific profile requirements

### INT-03 — Nabhold corporate / institutional

| ID | Positive | Negative | Owner |
|---|---|---|---|
| NAB-01 | Valid confidential login callback and BFF session in TLS Redis | Wrong PKCE/nonce/state/callback, CSRF, session replay/eviction denied | Nabhold/IAM |
| NAB-02 | Current IAM token passes CP effective-authority/self mapped Principal read | Revoked token or unmapped Principal cannot retain executive session | Nabhold/CP |
| NAB-03 | CMS PUBLISHED home/nav/footer resolves for exact Organisation/Tenant and registered capability | Preview/draft, tenant mismatch, unauthorised/expired workload denied | CMS/Nabhold/CP |
| NAB-04 | Public page and console navigation resolve, no broken route | Executive UI never invents binding, legal actor or fabricated data | Nabhold |

### INT-04 — Thamani logistics B2B/B2C

Test real enterprise B2B company/order contracts, individual B2C courier quotes/bookings/tracking when accepted owner domain interfaces exist. Human consumer role SHALL NOT acquire B2B Organisation/merchant grants merely through customer status; B2B agreement SHALL NOT become an unrestricted person/customer service identity. Logistics tracking access must validate shipment custody, owner and intended recipient. Do not silently restore legacy retail checkout without owner-approved Thamani ADR reconciliation.

### INT-05 — ZuriBeans B2B

Test independent buyer/supplier organisation identities, RFQ and controlled approval, shipment/document access, vanilla/coffee or other seeded catalogues only where canonical provider supports them, pricing/market context, cross-jurisdiction seller/issuer authority, private buyer price and supplier document denial. Do not assume South Africa/Uganda markets imply two AWS production regions.

### INT-06 — Equator & Estate Co.

Test independent Organisation/Tenant and lawful responsible actor, protected project/property records and contract/procurement/accounting permissions. Owner-approved engine capabilities are prerequisite; where not implemented, the relevant suite reports BLOCKED, never fabricated success.

### INT-07 — External API-only (mandatory platform invariant)

Create synthetic EXTERNAL_CLIENT and canonical Tenant with **zero DigitalEstate records**. Authenticate a registered external workload; establish independent subscription/grant/context; resolve and invoke an actual bound resource server. Verify correct audited effect, tenancy isolation from Nabhold, Thamani and ZuriBeans, revocation and replay. Negative: fake estate injection, forged tenant ID, wrong audience, absent subscription or retired binding and external cross-tenant reads denied. A made-up placeholder DigitalEstate invalidates the entire acceptance result.

### INT-08 — Finance, events and regulations

| ID | Positive | Negative / independent proof | Owner |
|---|---|---|---|
| FIN-01 | Correct current legal actor/market binding at actual execution point | CP legal veto cannot be replaced by a negative-only regulatory result | CP/Payments/ERP/Trade |
| FIN-02 | Payments legal AND financial decision both current, exact instruction fingerprint | Capture/refund/void with changed merchant, amount, destination or expired mandate denied | Payments/CP |
| FIN-03 | PSP request dispatched once after durable reservation; unknown outcome reconciled | No blind duplicate on timeout; sandbox/deterministic PSP explicitly labelled | Payments |
| FIN-04 | ERP journal/posting carries CP decision and correct AD_Client/AD_Org placement | Unplaced legal actor, inactive mandate, wrong legal entity and direct native bypass fail | ERP/CP |
| FIN-05 | Trade full domain completion uses valid legal actor and native COMMIT enforcement | Revoked/expired binding, lease replay, duplicate order/payment effect denied | Trade/CP |
| EVT-01 | Transactional outbox persists event with canonical context and history | Broker failure, redelivery, replay, DLQ and idempotency prevent double consequence | All producers/consumers |
| REG-01 | Accepted source-pinned requirement and policy evaluation is replayable | Unverified official source/test-law fixture must not become certified production law | Regulations/Pulse/Trade Docs |
| REC-01 | Backup/restore and key rotation in protected approved state | Synthetic fixture restore cannot satisfy real RPO/RTO or live custody signoff | Infrastructure/owners |

## 4. Cross-engine graduation rules

| Stage | Minimum condition | Never implied |
|---|---|---|
| Profile implementation | All mandatory scenarios exist, versioned and CI-visible | Passed result |
| L4 source qualification | All required real-component synthetic cases PASS, verified pins and no test-only bypass | Real legal-person evidence or G17 |
| Release candidate | Stable manifest and selected profile compatibility against actual candidate image digest | Deployed production EngineInstance |
| Protected staging | Current real issuer and CP credentials, approved account/endpoints, capability-by-capability real execution and negative tests | PSP live certification or production by itself |
| Provider and production acceptance | Actual source/PSP/merchant/registry authority, audit, restore, signed multi-owner release | Permission for unrelated tenants/markets/operations |

## 5. Immediate acceptance backlog

- INT-01: Same source manifest/run scripts produce comparable scrubbed receipt on Codespaces and GitHub Actions, isolated credentials, refusal of a missing prerequisite, and deterministic teardown.
- INT-02: Real IAM/CP process test over verified local TLS; wrong audience/current authority/revocation negatives and no group authority leakage.
- INT-03: Complete Nabhold OIDC/BFF/CMS flow; protected staging remains NOT COMPLETE.
- INT-07: External without DigitalEstate verified before asserting the platform is tenant-neutral for production.
- INT-04/05/06/08: Add each profile only when actual owner-approved domain/provider capabilities exist; do not call missing operations available.

The live state of each scenario belongs in the [EA v2.2 dashboard](ea-dashboard.md) with evidence run links, not in this fixed normative test inventory.