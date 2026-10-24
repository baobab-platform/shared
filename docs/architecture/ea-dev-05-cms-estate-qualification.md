# DEV-05 — native CMS and Nabhold vertical

Implementation follows the original fourteen NAB-03 cases under Accepted
EA-DEV and ADR-SHARED-043. The CMS, IAM and CP assessments in `docs/assessments/`
identify source readiness separately from current provider/estate acceptance.
DEV-04 is accepted; its seven-case results cannot substitute for this gate.

Engineering spans [CP #436](https://github.com/baobab-platform/baobab-cp/pull/436),
[CMS #48](https://github.com/baobab-platform/baobab-cms/pull/48),
[Nabhold #92](https://github.com/baobab-platform/nabhold/pull/92) and
[Infrastructure #57](https://github.com/baobab-platform/infrastructure/pull/57).
The maintained runbook is Infrastructure `development/NAB03.md`: exact commands,
source/image/contract pins, scoped credentials, case semantics, evidence custody,
interruption recovery and rollback. GitHub Actions and Codespaces use the same
private integration image and lifecycle.

Two source defects were found during implementation: CP's audience-specific
subject verifier and CMS's inbound caller path did not both enforce current
issuer status; Nabhold requested `openid` while its current-session check
requires `authority:self`. The owner fixes preserve signature/issuer/audience,
S256/nonce/state, exact issuer strings, separate credentials, encrypted TLS Redis
custody and token-free opaque BFF sessions. Missing/malformed issuer status is
unavailable, not definite inactive. No positive revocation cache is introduced.
CMS's failing container scan also identified vulnerable Next 16.4.0; the patch
updates it to 16.4.2 and reruns owner checks rather than waiving the scan.

The current CMS declaration is PARTIAL, with production_permitted:false.
Infrastructure cannot invent a provider support, certification, ACTIVE binding,
entitlement or invocation descriptor to turn a native component read into estate
acceptance. The executor checks actual CP capability resolution. Canonical
published-home/navigation/footer and controlled missing-grant cases remain
BLOCKED if their valid positive prerequisite cannot be established. The other
original cases still require actual signed tokens, native expiry/revocation,
real tenant/context denials, Payload draft/withdraw transitions, actual CP outage
and restoration, independent validator negatives and host teardown. Every
unexecuted or failed case remains visible; green source CI cannot qualify NAB-03.

The BFF path independently exercises actual Next handlers, Hydra code/S256 and
signed ID tokens, Kratos native sessions, canonical CP self-authority, encrypted
TLS Redis custody, opaque secure browser handles and server-side logout replay
denial. A native HTTP observation does not assert an independently observed
browser UI, MFA/step-up, provider conformance or protected/production acceptance.

Current implementation progress is recorded in the official JSON register.
Final acceptance requires the actual original per-case receipts, hash-verified
custody, reviewed exact owner sources and all mandatory CI. Provider eligibility,
legal-source verification and protected release remain separately governed.
The dated assessment snapshots and earlier DEV-01/02/03/04 evidence are preserved.
