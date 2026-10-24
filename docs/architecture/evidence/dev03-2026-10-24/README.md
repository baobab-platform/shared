# DEV-03 — verified native issuer and current CP authority evidence

Observed 24 October 2026. Scope: actual isolated Hydra/Kratos, CP, PostgreSQL,
sixteen native authority/protocol cases and complete owned-resource teardown.

- CP engineering: https://github.com/baobab-platform/baobab-cp/pull/435
- CP merged source: `718caedca3b9203931b399464e21b0f64ffbe879`
- Reviewed and runtime-pinned CP head: `05964feeed9636a9210cc669395f3481ce841007`
- Infrastructure engineering: https://github.com/baobab-platform/infrastructure/pull/55
- Reviewed Infrastructure head: `49037c32206656aef4871c9f94e2a65934267f59`
- Actual executed CI harness merge SHA: `0b0657bce228874bdb813c2dbe892377c9b95ea4`
- Native run: https://github.com/baobab-platform/infrastructure/actions/runs/40076614067
- Artifact: https://github.com/baobab-platform/infrastructure/actions/runs/40076614067/artifacts/12553716835
- Downloaded archive SHA256: `d6c82272e39fb8dbff5c5953ee450b7cae03aef51bb2c231f1234cb1dc86a548`

The archive digest was verified against GitHub artifact metadata after download.
Original suite/per-run JSON bytes are retained unchanged, and both original
receipt hashes were verified. The authority-suite sidecar was computed locally
from those unchanged downloaded bytes; it is not an independent signature.
The interrupted run retains lifecycle failure. The successful run records
six lifecycle/recovery checks, the exact sixteen authority cases, native image
pins, generated configuration hashes and verified teardown. Both runs record
complete cleanup. Prior DEV-01/02 evidence remains unchanged in its own folder.

The issuer actually signs the access tokens. Native Kratos password sessions
supply the two human subjects. Real Hydra authorization code/S256 PKCE and the
actual current CP HTTP APIs provide the positive and negative observations.
Revocation and CP-only deactivation qualify only while the original bearer
remains unexpired after the denial response. The CP-only case independently
confirms that issuer status remains active. Wrong audience uses an actual
same-subject token with a different audience, not edited signed claims.

The authenticated fixture hook normalizes identity; it does not implement IAM's
registered canonical provider hook. The protocol driver is not an estate BFF or
OIDC ID-token consumer. Canonical provider qualification, DEV-04 seven-case,
NAB-03, protected acceptance and production authorisation remain false. No real
legal-source or provider registration is invented. These scoped package cases
do not establish the complete canonical L4 scenarios or C4-03/C4-04 acceptance.

Raw bearer tokens, passwords, private keys, native session/callback material,
provider response bodies and run-state directories are excluded. Configuration
hashes identify actual private overlays without publishing their secret values.
No independent interactive Codespaces or protected production execution is
asserted; Actions uses the shared integration container and lifecycle commands.

Engineering startup failures were resolved before this final native run. The
separate mandatory INT-02 regression's image-fetch failure and targeted rerun
are recorded separately; they do not substitute for these native observations
and do not establish repair of the earlier BA-AUD-001 MFA finding.
