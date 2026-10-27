# DEV-07 live buyer identity companion

Authority: Accepted ADR-SHARED-042/043 and EA-DEV DEV-07. This is a bounded
implementation increment, not a provider, protected or INT-05 acceptance record.

The named `baobab-dev-trade-buyer-validator` may resolve the human Principal
and BFF estate binding through CP, using separate workload credentials and
`subject_principal_audiences: [baobab-trade]`. The named
`baobab-dev-zuribeans-bff` may authenticate its own handoff to Trade. Both
registrations are **development only** and contain no buying grant. The existing
production Trade and estate entries retain their previous ceilings. Buyer JIT
registration, native commitment submission and commerce-profile resolution
remain unallocated in this increment. `trade:buy` remains human-only.

ADR-SHARED-012 remains unchanged: public engine-instance IDs are `ei_` keys;
CP's topology UUIDs remain internal surrogates. The CP companion reads the
existing public engine-instance key and adds the corresponding CP-owned public
estate key to its native estate table. No consumer derives an alias, and no
Shared identifier grammar is broadened. CP verifies the public keys against
the exact existing leased native rows before binding them.

Owning delivery:

- Shared owns this registration and compatible identifier definition.
- CP owns leased synthetic Principal/tenant assignments, current native estate
  binding and readback in its guarded development command, outside the production
  image. No harness SQL creates CP authority.
- IAM owns native Hydra client configuration, issuance and claim normalization;
  issuer claims remain identity evidence only.
- Infrastructure composes exact owner source pins, real issuer/CP calls, secret
  custody, bounded execution and independent host teardown.
- Trade #176 owns the maintained buyer handler, native buyer fixtures and its
  eight-case live component qualifier. Source tests cannot promote it.

Deployment must consume reviewed pinned owner source. Pending companion pins
and a prepared code packet are not live qualification. All earlier receipts
remain unchanged; independently run, hash and retain new evidence before
changing DEV-07's joined acceptance status.
