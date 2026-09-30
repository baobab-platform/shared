# EA-02C — Contract Work Implementation Plan

**Status:** In progress  
**Order:** Per EA-02B candidate review (smallest gaps first)  
**Governance:** ADR-SHARED-017 §12–14 contractability test

## Steps

### Step 1: erp/v1 InventoryAvailabilityQuery ✅ DONE

- Formalizes query parameters for `inventory.availability.query` capability
- Request schema: `inventory-availability-query.schema.json`
- Response schema: existing `inventory-availability.schema.json`
- Merged in shared#149

### Step 2: buyer-organisation/v1 commands ✅ DONE (shared#150)

**Scope:** Two capabilities
- `customer.buyer-application.manage` — apply, provide evidence, review, decide
- `customer.buyer-membership.manage` — invite, accept, revoke, manage roles

**Deliverables:**
- `buyer-application-request.schema.json` — apply, evidence, withdrawal
- `buyer-application-response.schema.json` — status, timeline, decision
- `buyer-membership-request.schema.json` — invite, accept, revoke, role update
- `buyer-membership-response.schema.json` — membership state, site access

**Authority:** Trade (buyer-organisation/v1 README §Authority Boundaries)  
**Reference:** trade-buyer branch or live implementation

### Step 3: identity/v1 authentication profile ✅ DONE (shared#150; corrected for provider neutrality in its follow-up)

**Scope:** Two capabilities  
- `identity.authentication.perform` — human interactive + session
- `identity.workload-token.issue` — client credentials, workload actor_type

**Deliverables:**
- `human-authentication-request.schema.json` — Authorization Code + PKCE, OIDC `acr_values`; no realm
- `human-authentication-response.schema.json` — access token, ID token
- `workload-token-request.schema.json` — workload_id, audience, scopes; no credential, grant type or realm (the mechanism follows the workload's registered `credential_type` behind the provider boundary)
- `workload-token-response.schema.json` — access token and workload claims

**Authority:** IAM (baobab-iam)  
**Dependency:** M1-C Ory fixtures (baobab-cp#224, #225) merged ✅; federated path in baobab-iam#42
**Reference:** ADR-0006 token profile, ADR-IAM-0024 assurance

### Step 4: content/v1 resolution ✅ DONE (shared#150)

**Scope:** One capability  
- `content.entry.resolve` — deterministic content by market/locale/context

**Deliverables:**
- `content-resolve-request.schema.json` — entry_id, market, locale, context
- `content-resolve-response.schema.json` — resolved entry, provenance, fallback

**Authority:** CMS (baobab-cms)  
**Reference:** CMS README ADR-0015, content-resolution antipatterns

### Step 5: intelligence/v1

**Scope:** Two capabilities  
- `intelligence.research-mission.manage` — manage intelligence research requests
- `intelligence.evidence.search` — semantic evidence retrieval

**Deliverables:**
- `research-mission-request.schema.json` — query, scope, constraints
- `research-mission-response.schema.json` — mission, status, results
- `evidence-search-request.schema.json` — search terms, filters, pagination
- `evidence-search-response.schema.json` — results, relevance, provenance

**Authority:** Pulse (baobab-pulse)  
**Status:** Deferred until Pulse first production domain (per EA-02B)  
**Reference:** baobab_pulse/contracts/api

## Timeline

- Steps 1–4: done. `inventory.availability.query` (step 1) still needs its catalogue entry.
- Step 5 (intelligence): Deferred pending Pulse production lifecycle
- Catalogue expansion is subordinate to EA-01 consumer-lock convergence: engines pin current Shared before more keys are added.

## Validation

Each step:
1. ✅ Reads existing schemas from engine code or package definition
2. ✅ Extracts request/response message shapes
3. ✅ Writes formal JSON Schema per ADR-SHARED-017 §12
4. ✅ Adds contract URI ($id) and references
5. ✅ Updates catalogue.yaml with contract majors
6. ✅ Validates with `scripts/capability_catalogue.py`
7. ✅ Commits to Shared PR

## Blockers

None identified. Each engine's implementation is documented and available for schema extraction.
