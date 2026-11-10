# RTD-10 architecture-only Trade Docs candidate conformance

**Date:** 10 November 2026. **Decisions:** Accepted ADR-SHARED-017 and ADR-SHARED-026.

## Reproduced conflict

Shared RTD-10 treated the existence of `.baobab/capability-provider.yaml` as a claim of implemented provider support. But ADR-SHARED-017 expressly permits an engine to carry **candidate-only planned capabilities**, which confer **no** provider, certification, capability registration, binding, grant, execution authority or runtime readiness. Trade Docs remains ARCHITECTURE_ONLY under its RTD-10 profile. A real Trade Docs source declaration containing only CANDIDATEs therefore falsely failed the conformance job.

## Fix

- Distinguish *declared candidate intent* from *implemented provider support* for architecture-only Trade Docs.
- Reuse the actual Shared canonical provider declaration validator to check schema, engine identity, candidate grammar, provenance and no forbidden fields. No private RTD shadow schema.
- Continue rejecting any `providers` entries, even PARTIAL ones. Keep the preexisting checks rejecting `src/` and copies of canonical document contracts.
- Retain RTD-10's maturity constraint; this is not approval for the HYB-01 scaffold to become a provider.
- Add source regression vectors for valid candidate, invalid provider support, empty intent, wrong engine, invented canonical capability and forged ACTIVE state.

## Downstream adoption constraint

Existing RTD consumers use immutable Shared action refs. The new logic does **not** take effect until a separately reviewed Shared release/merge and consumer pin update. The dependent [Trade Docs #23](https://github.com/baobab-platform/baobab-trade-docs/pull/23) should not be merged before its RTD-10 workflow runs against the accepted new policy and returns green. Do not game the old conformance by hiding or renaming the declared file during tests.

## Unqualified

No native documentary provider, accepted canonical `documents.*` capability, event producer, regulated document issuance, CP migration, production deployment or legal authority. SOURCE-ONLY semantic reconciliation; external runtime evidence is outstanding.
