# Baobab identity-events contracts v1

This package defines the canonical identity-lifecycle events referenced by
`baobab-iam` ADR-0016 ("Identity Lifecycle, Revocation and Deprovisioning")
and consumed by any engine that needs to react to a principal's or
membership's state changing.

## Contract surfaces

- `asyncapi.yaml` carries all 9 events this domain now defines: identity
  created, identity disabled, identity suspended, identity reactivated,
  membership revoked, entitlement revoked, credential compromised, session
  revoked, and workload revoked.
- JSON Schemas (`identity-created.schema.json`, `identity-disabled.schema.json`,
  `identity-suspended.schema.json`, `identity-reactivated.schema.json`,
  `membership-revoked.schema.json`, `entitlement-revoked.schema.json`,
  `credential-compromised.schema.json`, `session-revoked.schema.json`,
  `workload-revoked.schema.json`) define each event's `data` payload.
  Shared identity types (`ActorType`, etc.) live in `contracts/identity/v1`
  and are referenced, not duplicated.

`workload-revoked.schema.json` keys on `principal_id`, the same field every
other event above uses, rather than a `workload_id` of its own:
`WorkloadIdentity` (`contracts/identity/v1/workload-identity.schema.json`)
extends `Principal`, so a workload's `id` is already in that shared space.
What genuinely differs is the required `client_id` alongside it — ADR-0016
§80 requires every workload identity to be provisioned against an
identified OAuth client, and ADR-0015 §107 ("Compromised service
credentials SHALL be individually revocable") means that client, not just
the abstract identity, is what a consumer actually needs to act on.

`session-revoked.schema.json` deliberately does not embed
`AuthenticationAssurance`: a revocation event records that a session ended
and why, not how it was originally authenticated, and that assurance detail
already lives on the `Session` resource itself
(`contracts/identity/v1/session.schema.json`'s required
`authentication_assurance`) rather than needing to be re-asserted here.

`identity-disabled.schema.json`'s `new_status` was originally `["SUSPENDED",
"DISABLED"]`, letting an ACTIVE-to-SUSPENDED transition be reported under
either `identity.disabled` or the newly-added `identity.suspended`. Narrowed
to `["DISABLED"]` only now that `identity.suspended` exists to own that
transition — one transition, one event type, not two ways to say the same
thing.

All events use `contracts/events/v1/envelope.schema.json` — composed in
`asyncapi.yaml`, not embedded inside the payload schemas themselves (that
was this package's original defect: each payload schema tried to `allOf`
in the envelope directly, via a path — `../../common/event-envelope.schema.json`
— that has never existed in this repository; nothing validated it, so the
break went unnoticed). No message broker exists yet anywhere in this
ecosystem to actually carry these — same position `contracts/erp/v1` and
`contracts/supplier-onboarding/v1` are already in — so this contract exists
for producers and future consumers to build against ahead of one existing,
not because one does.

## History

ADR-0016 §90 ("Event Examples") suggested `baobab-platform/shared` define versioned
events including `identity.suspended`, `identity.reactivated`,
`entitlement.revoked`, `credential.compromised`, `session.revoked`, and
`workload.revoked`, in addition to the `identity.disabled` and
`membership.revoked` this package already had (plus `identity.created`,
which predates ADR-0016's list but is exercised by `baobab-iam`'s bootstrap
flow). All of them are now defined, across several passes rather than one:
fabricating a shape without per-event design work against ADR-0016's
revocation-propagation, staleness (§93-95) and audit (§139) requirements
would just have produced a second, differently-wrong version of the defect
this package originally shipped with (broken `$ref`s to a file that never
existed).

`credential-compromised.schema.json`'s `credential_type` enumerates
ADR-0015 §5's supported human authenticator categories (password, passkey,
security-key WebAuthn, platform WebAuthn, TOTP, recovery code, federated
enterprise IdP, social IdP) — grounded in that table, not invented.
