# LA-05G — Engine assessor enrolment and cross-engine acceptance gate

**Status:** Implemented registry staging profiles; **runtime integrations remain unaccepted**  
**Authority:** ADR-BCP-027 LA-05; Shared LA-05A PR #261; Control Plane LA-05A PR #299; IAM LA-05B PR #107

## Dependency graph

```text
Shared canonical LA-05A schema + transport scope                 MERGED
  └── CP context-owner-bound assessment, default OFF             MERGED
       └── IAM non-default scope definition/admission            MERGED
            └── Shared staging PROVISIONED assessor profiles     THIS PR
                 ├── Trade seller PEP foundation                 PR #118 — dependency security gate RED
                 ├── ERP invoice/accounting PEP foundation      PR #78 — MERGED, native posting not wired
                 ├── Payments beneficiary PEP foundation        PR #25 — MERGED, simulated sandbox only
                 └── Trade Docs issuer PEP reference             PR #9 — MERGED, no deployed runtime
```

All four new profiles are **staging-only, PROVISIONED**, with **only** `context:resolve` and `legal-actor:assess`, `aud=baobab-control-plane`, `context_purposes=[RUNTIME]`, and federated credentials (no static secret). Neither registry presence nor IAM scope definition issues a token; CP rejects PROVISIONED clients. No production workload's allowed scopes were changed.

## Required proof before a candidate may be promoted to ACTIVE

1. **Account-level staging identity:** a separately deployed workload principal, concrete issuer+subject, owner, environment, audience, signed short-lived provider token and rotation evidence; the identical canonical client_id is registered with IAM and CP. Workload remains PROVISIONED until the owner verifies it; do not reuse production service credentials.
2. **Dual scope issuance:** authenticated token has precisely approved `context:resolve` and `legal-actor:assess`, and no payment execution, document signing, ERP posting or Trade seller-provider scopes as a side effect.
3. **Owned RUNTIME context:** CP resolves and stores a current principal-owned RUNTIME PlatformContext for the exact operating Organisation, tenant and market. Attacker possession of somebody else's `context_id` is denied; provisioning-purpose and expired contexts are refused.
4. **Three-person mandate:** maker, independent checker and distinct activator approval; current verified legal profile, approved source evidence and actual PRIMARY Organisation mapping. Event arrival/cached ACTIVE not accepted as authorization.
5. **Live consumer decision:** every regulated operation asks CP afresh; validate exact `role`, `activity`, `market`, `capability`, `operation_reference`, `context_id`, `AUTHORIZED`, actor equality, trusted validity and the provider's OWN readiness. No provider permission from CP alone.
6. **Lifecycle and revocation:** deny direct unapproved activation, scope overlap, revoked/suspended/expired mandates, withdrawn legal evidence, wrong tenant and market, failure or latency at CP, and repeated idempotent operations after authority changes. No offline event authority fallback.
7. **Native execution path:** prove the *actual* Medusa commit, iDempiere posting, payment-provider mutation or document signing/submission calls the PEP before irreversible execution; standalone ports and reference tests do not pass this requirement.
8. **Production hold:** CP assessment and LA-04D mutation endpoints are hard-disabled in production; do not promote these profiles or a `PROVIDER_SUPPORTED` capability until audited staging integration, critical CVE remediation and explicit operator/security acceptance. Founding Nabhold onboarding requires PEO-02 and PEO-03, then LA-06.

## Readiness classification

| Engine | CP decision adapter | Real enforcement and independent provider | Acceptance |
|---|---|---|---|
| IAM | Non-default scope declared | Real issuer/client grant deferred | `PROVISIONED` |
| Trade | LA-05C guarded order adapter | Existing Medusa native checkout bypasses adapter; Foundation vulnerability gate red | `NOT_ACCEPTED` |
| ERP | LA-05D financial gate | Native iDempiere posting/inbox not wired | `NOT_ACCEPTED` |
| Payments | LA-05E beneficiary gate | In-memory simulated provider only, no HyperSwitch KYC/settlement | `NOT_ACCEPTED` |
| Trade Docs | LA-05F tested issuer reference | `ARCHITECTURE_ONLY`, no deployed issuing service | `NOT_ACCEPTED` |

A Nabhold holding-to-subsidiary corporate affiliation never implies a mandate. This PR creates **zero** tenant records, legal actor mandates, payments, certificates or operational grants.
