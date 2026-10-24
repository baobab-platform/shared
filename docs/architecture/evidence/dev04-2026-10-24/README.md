# DEV-04 — original seven-case native qualification, 24 October 2026

This record retains actual native Hydra/Kratos → current CP development proof,
all seven original INT-03C cases with 45 closed assertions, and final owned
resource/private-state cleanup. It does not infer cases from DEV-03's sixteen.

- Engineering: https://github.com/baobab-platform/infrastructure/pull/56
- Merged Infrastructure source: `5d70e40da1c5b3f22b46fe5a1177f843b26ec411`
- Reviewed Infrastructure head: `a7867adf637ceeb4062d199617b2071807f13f6b`
- Actual executed CI harness merge: `7a0b520f949a8d0a3e7364fe5cfb1dfae83e5335`
- Native workflow: https://github.com/baobab-platform/infrastructure/actions/runs/40095164501
- Original artifact: https://github.com/baobab-platform/infrastructure/actions/runs/40095164501/artifacts/12560518334
- Downloaded archive SHA-256: `6770f6e5be1ea5ba969d3ada10136d38a21e46912ea6b853e07cfc4535ec58cf`
- Qualified fresh run: `039946c7b987ecb3baa7788aa776c93a`
- Pinned Shared: `6ebd5fd258100fe437837869ab2a1248b2df3988`
- Pinned CP: `718caedca3b9203931b399464e21b0f64ffbe879`
- Pinned IAM: `0ad103606b9705fcb33c468ea01b54d8ce76f9ae`

The archive was downloaded and its digest compared against GitHub's artifact
metadata. All three original per-run receipt SHA-256 sidecars and the original
DEV-04 suite sidecar were verified after download. Producer JSON bytes are
retained unchanged. The suite is byte-identical to its qualified run receipt.
Hashes establish byte integrity, not an external signature or protected approval.

| Retained run | Observed result |
| --- | --- |
| `3ec8e5f33c4a3d73e1769e497284f58b` | Interrupted-startup recovery, lifecycle false, no INT-03C qualification; cleanup true |
| `5f0cc70cad5f3e7322132b9284d1c34b` | Six DEV-01 lifecycle/recovery checks, 24 DEV-02 fixture observations and sixteen DEV-03 native cases; INT-03C false; cleanup true |
| `039946c7b987ecb3baa7788aa776c93a` | Fresh, separate original seven-case DEV-04 proof; all 45 assertions and cleanup true |

The final DEV-04 run observed stopped-CP health rejection, restoration/retest,
then the seven cases, and teardown without Compose. Only host resource absence
and private-state removal complete its last case. Receipt publication uses a
recoverable sanitized pending candidate; candidate/final-write/rename failure
and subsequent recovery are covered by focused source regressions. The source
suite has 29 tests; source results never substitute for the native cases.

The issuer verifier is a distinct named authenticated client, not the issuing
owner or CP status credential. It independently binds active/inactive issuer
status, issuer/subject/client/audience/scope/expiry. Provider GET and actual JWT
`exp-iat` enforce the 60-second ceiling. CP independently verifies signatures,
current issuer status and canonical authority. Real maker/checker Principals
and exact CP API provenance are used; no canonical SQL or invented grants.

An earlier candidate run `40080093137` passed but was **not accepted**: review
found incomplete lifetime checks and a receipt-publication recovery gap. Both
were corrected and rerun; removal of the superseded ambiguous transport module
was also verified at this final exact head. Earlier artifacts remain in their
original Actions history; this record adopts only the final artifact above.

The receipt includes actual built CP image identity, immutable runtime images,
lock and four private native-configuration hashes, and three Shared contract
hashes verified byte-for-byte against CP's embedded contracts. Newer CMS, Trade
and ERP assessments are preserved in Shared's adoption source; they change no
runtime contract used by this pinned proof.

The narrow fixture hook/edge overlay is not IAM's registered production provider
hook/conformance. One operator drives distinct synthetic human Principals and
issuer credentials; independent people, external custody and protected release
remain separate. Provider declarations remain PARTIAL. Full canonical L4/C4,
estate BFF/ID-token consumption, CMS/NAB-03, legal-source verification, staging,
production and independently observed interactive Codespaces remain unqualified.
The native owner stores, accepting CP/database, run images, volumes, network,
private credentials/session/configuration and run state were destroyed; shared
nonsecret base-image caches are not claimed absent.

Final engineering review/CI: 29 applicable checks succeeded and 6 were skipped
by applicability, with no open review threads. The separate legacy INT-02
regression passed at the final head without a rerun. No repair of historical
BA-AUD-001 MFA root cause is established. Scoped DEV-04 acceptance closes
BA-AUD-002/030 only for their original DEV-03/04 development case requirements;
BA-AUD-016/032/043 and other provider/engine/estate/protected findings remain
independent. Dated assessments and older failed receipts are unchanged.
