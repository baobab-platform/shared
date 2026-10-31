# DEV-08 / IAM-N07 TMS development workload ceilings

31 October 2026. PROPOSED CANONICAL CONTRACTS, NOT ACCEPTED OR ACTIVE.

This additive draft changes no existing ACTIVE client. It introduces only
a workload-only resource admission scope tms:booking:submit at audience
baobab-tms, with grants_authority=false, and two separately revocable
PROVISIONED development identities:

- baobab-dev-tms-subject: source owner baobab-tms; allowed_audiences
  baobab-control-plane and baobab-tms; allowed_scopes context:resolve
  and tms:booking:submit; development only.
- baobab-dev-tms-validator: source owner baobab-tms; audience
  baobab-control-plane; allowed_scopes context:validate;
  validates_audiences [baobab-tms]; development only.

Neither is Active. The scope is transport admission, NOT a carrier booking,
legal actor mandate, assignment, native provider grant or access to any
other tenant. Thamani's confidential human BFF is a separate identity
and cannot present its human token as this workload.

Governing ADR-SHARED-042/043 and IAM ADR-IAM-0033 require provider/client
registration, real Hydra issuance, a current signed/opaque subject
with distinct CP validator, CP /v1/platform-context/validate real read,
exact canonically bound Organisation/Tenant/Market, CP provider/capability
binding/operation approval, and TMS-native durable idempotent PEP before
a new endpoint may perform any carrier or booking effect. Review
TMS draft PR #28 for the non-executable real issuer/CP HTTP readback.

Only after all original private development evidence, cross-tenant,
wrong-audience, revoked-unexpired, missing mandate and provider-native
negative cases, separate real operator readback and independently
verified teardown may these identities be considered for promotion
from PROVISIONED to ACTIVE. Such promotion needs a separately reviewed
Shared/CP/IAM change and is not automatic in this PR.

No staging/production client, public provider endpoint, protected
credential or native booking is created by this proposal.
