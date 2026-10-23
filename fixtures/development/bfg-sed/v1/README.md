# BFG-SED v1 — global synthetic enterprises, multi-market capability scenarios

**Status: Proposed development fixtures.** Source/data only; no running CP/IAM provider, real market grant, financial settlement, actual legal verification or production readiness. This dataset implements input scenarios for the **Accepted EA-DEV**, ADR-SHARED-043, CP BCP-026/027, Shared ADR-017/036 and relevant domain ADRs.

## Governing boundary and enterprise profiles

The existing Shared canonical development profile at contracts/development/v1/enterprise-profiles.schema.json and its CP implementation still accept five named enterprises **and only ZA/UG** as currently valid development-bootstrapped markets. This overlay is a separate fixture, not a change to canonical CP markets.

| Profile | Operating market scenario | Additional footprints or sourcing | Identity / operating semantics |
| --- | --- | --- | --- |
| nabhold | ZA | representative presence: UG, NG, KE | non-trading holding; group membership does not grant raw subsidiary access |
| zuribeans | ZA | sourcing/footprints: KE, ET, TZ, UG, AO, CO, VN | separate B2B operating Organisation, no separately incorporated ZuriBeans legal entity |
| thamani | ZA, EG, DE, GB, UG, KE, TZ, GH, MZ, AO, NG, ET, DJ, SZ | no separate sourcing list | B2B logistics; declared incorporated separately, but fixture cannot verify CIPC |
| equator-estate | UG, ZA | — | independent property operation, not a separately incorporated legal entity in the current governing baseline |
| external-client | UG | pharmaceutical imports/sources from CN, IN | unrelated fictional Ugandan importer; **zero digital estates** and no group entitlement |

ISO 3166-1 alpha-2 codes: **GB** is United Kingdom; **SZ** is Eswatini (formerly Swaziland). Test market currencies, time zones, number amounts and locales are scenario values, not live rate sources, quotes, compliant commercial disclosures or legal permissions.

The v1 blueprint contains **18 countries**, **34 cross-region scenario templates** and **35 product/service/property/fictional-medical templates**. Commercial activities include RFQ/quotation, buyer/supplier onboarding, portfolio work, freight forwarding/exception handling, documentary/regulatory denial and pharmaceutical cold-chain/recall. Capabilities requested in the file use Shared's accepted catalogue vocabulary; there is **no** automatic provider implementation, certification, registration or grant.

## Run the deterministic offline generator

From Shared repository root:

~~~sh
python3 -m unittest discover -s tests/development -p 'test_generate_bfg_sed.py' -v

BAOBAB_ENVIRONMENT=development python3 scripts/development/generate_bfg_sed.py \
  --scale small --seed 20261023 \
  --run-id 0123456789abcdef0123456789abcdef \
  --output /tmp/bfg-sed-small.json

BAOBAB_ENVIRONMENT=development python3 scripts/development/generate_bfg_sed.py \
  --scale medium --seed 20261023 \
  --run-id 0123456789abcdef0123456789abcdef \
  --output /tmp/bfg-sed-medium.json

# Opt-in stress fixture, not part of every Codespace startup.
BAOBAB_ENVIRONMENT=development python3 scripts/development/generate_bfg_sed.py \
  --scale large --seed 20261023 \
  --run-id 0123456789abcdef0123456789abcdef \
  --output /tmp/bfg-sed-large.json
~~~

| Scale | Cases (scenario templates x repetitions) | Intended use |
| --- | --- | --- |
| small | 34 | smoke and simple development |
| medium | 170 | everyday integration/data test input |
| large | 1,360 | opt-in load and recovery exercises |

The stdlib-only Python script makes no requests, connects to no databases, touches no other repository, creates no identities and moves no funds. It refuses protected staging/production environment markers. References are deterministic for a seed and run ID, and disjoint across different run IDs. Reuse a run ID only to replay the same offline fixture. Run keys identify deterministic **fictional fixture objects**, not valid CP canonical IDs. The demo run ID is also just offline metadata.

## Output shape

- organisations: five identity scenarios, operating/footprint/source territories, requested capability keys, expressly unverified legal assertions and **null canonical CP IDs**
- personas: entirely fabricated role descriptions and reserved @example.invalid email addresses; IAM must create real scoped test identities independently
- facilities: non-geocodable scenario site placeholders with no real addresses, market activation or registry status
- counterparties: fictional market-specific prospective contacts with unverified qualification and no CP IDs
- catalogue_items: fictional commodities (including vanilla and coffee), transport services, buildings, projects, medical-product concepts and warehouse batches; no actual inventory, drug registration or product approvals
- scenario_transactions: currency, amount, time, timezone, origin/destination, action precondition and failure variants, marked NOT_EXECUTED with no settlement
- documentary_evidence_inputs: explicitly fake sample data marked MISSING/UNVERIFIED and **no licence, verification certificate or official registration**
- test_case_expectations: explicit BLOCKED/DENY/CONDITIONAL expectations with observed_result null until a real native API is actually exercised; BLOCK_UNTIL prerequisites always prevent execution

**All material is development-only.** No actual people, legal documents, bank details, VAT IDs, registration numbers, parcels, shipper addresses, geolocatable sites, import permits, genuine customs approvals, real medicines, manufacturer approvals or authorisation credentials are seeded. Data cannot be promoted or bulk imported into production.

## Correct cross-repository integration sequence

1. Infrastructure creates a fresh, marked baobab_dev_<nonce> database as role baobab_dev in a private isolated **development-only** environment, owns one <=24h lease and cleanup.
2. IAM issues the real isolated synthetic Principal subjects. CP performs **its accepted guarded development bootstrap** on the original closed five profile definitions; it returns canonical Organisation/Tenant/Market IDs. Offline SYN-* references are merely join keys.
3. A future reviewed integration adapter joins fixture profile keys to the **CP-assigned** real IDs, then seeds engine-owned records via approved engine APIs/native test ports, never through arbitrary CP direct SQL.
4. Where this overlay cites non-ZA/UG markets, the CP v1 bootstrap is currently insufficient. Record **CP_MARKET_UNAVAILABLE/BLOCKED**, and design a separately reviewed compatible versioned Shared/CP market enrolment path with legal-actor and native enforcement before attempting a real multi-country L4 result. Never silently add all footprints as ACTIVE Markets.
5. Native engine tests require current IAM audience/scope, CP context, correct capability binding and grants. No missing, stale, wrong-role/wrong-tenant/wrong-market, unverified legal actor or unsupported provider operation passes.
6. Every real test produces actual domain-specific evidence and then destroys issued identities, run DB/storage, credentials, leased resources and assets. A generated expectation is **not** an actual test receipt.

### Uganda medicine import scenario

Uganda NDA processes pharmaceutical importer licensing and import control, including permits and consignment verification. External-client fixture inputs intentionally carry missing or unverified licence, product and per-consignment states; actual import, payment/regulated settlement, marketing or carriage SHALL remain denied unless a properly authorised domain policy and real legal/provider evidence exist. Test placeholders are never substituted for official permits. Refer to:
- https://ulii.org/en/akn/ug/act/statute/1993/13/eng%402023-12-31
- https://www.nda.or.ug/directorate-of-inspectorate-services/

The synthetic dataset does not encode a timeless legal checklist; Regulations and domain owners must verify current source law for the actual action before protected execution.

## Next engineering increments

Shared owns this offline source plus validators. CP/Shared owners must extend development tenancy and market profile support **through a reviewed versioned contract**, with Organisation-first mandates and no invented incorporated LegalEntity. IAM/Infrastructure owners implement the existing EA-DEV reusable profile orchestration. Domain engines create native seed adapters and tests independently. This proposal **does not claim** that integration adapters or an 18-market canonical CP topology already run.

Keep small fixtures light for Codespaces; use medium for per-engine development and large only for deliberate test loads. Keep source/CI/L4/protected statuses separately and preserve BLOCKED cases.
