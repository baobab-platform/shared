# EA-DEV implementation register

Generated from [the JSON register](ea-dev-implementation-register.json); edit JSON and run `python3 scripts/ea_dev_register.py --write-view`.

**Observed:** 2026-10-24. **Register validation:** SOURCE reporting only. Runtime evidence is scoped to the linked package receipts. **Protected staging, external certification and production:** not accepted.

Shared and selected CP/IAM/Infrastructure source/CI; actual scoped DEV-01 lifecycle/recovery receipts downloaded and hash-verified. Other owner packages remain NOT_ASSESSED; no INT-03C/NAB-03 or protected acceptance is inferred.

Observations become STALE after 7 days; compare the observation date with today. CI validates structure and does not refresh evidence.

[Decision precedence, CI policy and closure rules](ea-dev-00-gate-reconciliation.md). NOT_ASSESSED means no new progress claim. Baseline CI does not qualify a current composed runtime.

| Package | Accountable team | Dependencies | Progress / assessment | Observed | CI / runtime | Next action |
| --- | --- | --- | --- | --- | --- | --- |
| **DEV-00** — Decision/gate reconciliation | Shared Platform Architecture | None | SOURCE_MERGED / ACCEPTED | 2026-10-24 | SUCCESS / NOT_OBSERVED | Maintain source/evidence observations as each owner gate lands; retain protected acceptance separately. |
| **DEV-01** — One paved-road integration command | Infrastructure / baobab-dev | DEV-00 | REAL_COMPONENT_SYNTHETIC_DATA / ACCEPTED | 2026-10-24 | SUCCESS / PASS | DEV-02: qualify accurate CP Organisation/tenant/mandate variants, then DEV-03 real issuer and CP authorisation; reuse this lifecycle without the optional #49 packet. |
| **DEV-02** — Accurate CP Organisation/tenant/mandate fixtures | CP / Shared | DEV-00, DEV-01 | NOT_ASSESSED / PARTIAL_SOURCE_RUNTIME_UNPROVEN | 2026-10-24 | BASELINE_ONLY / NOT_OBSERVED | Qualify mandate variants through CP-owned APIs and PostgreSQL tests using the closed contract. |
| **DEV-03** — Real issuer and CP authority chain | IAM / CP / Infrastructure | DEV-01, DEV-02 | NOT_ASSESSED / PARTIAL_SOURCE_RUNTIME_UNPROVEN | 2026-10-24 | BASELINE_ONLY / NOT_OBSERVED | Compose actual IAM-issued identities and CP mappings; prove audience, revocation and distinct-Principal workflow denials. |
| **DEV-04** — Seven-case INT-03C qualification | Infrastructure / IAM / CP | DEV-03 | NOT_ASSESSED / PARTIAL_SOURCE_RUNTIME_UNPROVEN | 2026-10-24 | BASELINE_ONLY / NOT_OBSERVED | Execute and retain all seven real cases under fresh development source/image pins and complete teardown. |
| **DEV-05** — Nabhold IAM/CP/BFF/CMS vertical | Nabhold / CMS / IAM / CP / Infrastructure | DEV-03, DEV-04 | NOT_ASSESSED / PARTIAL_SOURCE_RUNTIME_UNPROVEN | 2026-10-24 | BASELINE_ONLY / NOT_OBSERVED | Repin and adopt current CMS rows, then run all fourteen NAB-03 subcases without broadening caller ceilings. |
| **DEV-06** — External client without estate | Infrastructure / CP / IAM / selected provider | DEV-03 | NOT_ASSESSED / PARTIAL_SOURCE_RUNTIME_UNPROVEN | 2026-10-24 | BASELINE_ONLY / NOT_OBSERVED | Owner reconciles the current source and mandatory cases, then implements the next scoped increment. |
| **DEV-07** — ZuriBeans B2B capability slice | ZuriBeans / Trade / ERP / Trade Docs / Regulations | DEV-03 | NOT_ASSESSED / NOT_AUDITED | 2026-10-24 | NOT_ASSESSED / NOT_OBSERVED | Owner reconciles the current source and mandatory cases, then implements the next scoped increment. |
| **DEV-08** — Thamani B2B logistics capability slice | Thamani / TMS / Trade Docs / Regulations / Infrastructure | DEV-03 | NOT_ASSESSED / NOT_AUDITED | 2026-10-24 | NOT_ASSESSED / NOT_OBSERVED | Owner reconciles the current source and mandatory cases, then implements the next scoped increment. |
| **DEV-09** — ERP, finance and Subscriptions references | ERP / Payments / Subscriptions / Finance / Infrastructure | DEV-02, DEV-03 | NOT_ASSESSED / NOT_AUDITED | 2026-10-24 | NOT_ASSESSED / NOT_OBSERVED | Owner reconciles the current source and mandatory cases, then implements the next scoped increment. |
| **DEV-10** — Developer tooling and contracts | baobab-dev / Shared Foundation / consumers | DEV-01 | NOT_ASSESSED / NOT_AUDITED | 2026-10-24 | NOT_ASSESSED / NOT_OBSERVED | Owner reconciles the current source and mandatory cases, then implements the next scoped increment. |
| **DEV-11** — Observability, browser experience and CI test routing | Infrastructure / Shared / estates | DEV-01 | NOT_ASSESSED / NOT_AUDITED | 2026-10-24 | NOT_ASSESSED / NOT_OBSERVED | Owner reconciles the current source and mandatory cases, then implements the next scoped increment. |
| **DEV-12** — Database, migration and resilience drills | Persistent-engine owners / Infrastructure | DEV-01, DEV-02 | NOT_ASSESSED / NOT_AUDITED | 2026-10-24 | NOT_ASSESSED / NOT_OBSERVED | Owner reconciles the current source and mandatory cases, then implements the next scoped increment. |
| **DEV-13** — Independent staging/production entry | Infrastructure / Security and Operations / legal and domain owners | DEV-04, DEV-05, DEV-06, DEV-07, DEV-08, DEV-09, DEV-10, DEV-11, DEV-12 | NOT_ASSESSED / NOT_AUDITED | 2026-10-24 | NOT_ASSESSED / NOT_OBSERVED | Owner reconciles the current source and mandatory cases, then implements the next scoped increment. |
| **DEV-14** — Reusable engine onboarding framework | Shared / Infrastructure / baobab-dev / engine-template | DEV-01, DEV-02, DEV-03 | NOT_ASSESSED / PARTIAL_SOURCE_RUNTIME_UNPROVEN | 2026-10-24 | BASELINE_ONLY / NOT_OBSERVED | Owner reconciles the current source and mandatory cases, then implements the next scoped increment. |
| **DEV-15** — Pulse/Payments first-adopter runtime profiles | Infrastructure / Pulse / Payments / IAM / CP | DEV-14, DEV-03 | NOT_ASSESSED / PARTIAL_SOURCE_RUNTIME_UNPROVEN | 2026-10-24 | BASELINE_ONLY / NOT_OBSERVED | Owner reconciles the current source and mandatory cases, then implements the next scoped increment. |

## Verified source baselines

| Baseline | Merge/source | Reviewed head | Evidence limits / CI |
| --- | --- | --- | --- |
| shared | [e1c0f4535e143a584dc8e03377129977d440a0cf](https://github.com/baobab-platform/shared/commit/e1c0f4535e143a584dc8e03377129977d440a0cf) ([PR #375](https://github.com/baobab-platform/shared/pull/375)) | `3e0683bedb69ee2f0813a8eadaf16bda2ae4af17` | Offline BFG-SED source and accepted programme; no composed runtime; [run 1](https://github.com/baobab-platform/shared/actions/runs/40017765873), [run 2](https://github.com/baobab-platform/shared/actions/runs/40017765971), [run 3](https://github.com/baobab-platform/shared/actions/runs/40017766169), [run 4](https://github.com/baobab-platform/shared/actions/runs/40017765874) |
| cp-bootstrap | [3b1ca63f85dd18d9d82c162c2777ab3313091328](https://github.com/baobab-platform/baobab-cp/commit/3b1ca63f85dd18d9d82c162c2777ab3313091328) ([PR #433](https://github.com/baobab-platform/baobab-cp/pull/433)) | `2863e9a145aabf386454bc99c936e41acb469b75` | Guarded CP bootstrap source and owner PostgreSQL CI; not composed L4; [run 1](https://github.com/baobab-platform/baobab-cp/actions/runs/39982169937), [run 2](https://github.com/baobab-platform/baobab-cp/actions/runs/39982167869), [run 3](https://github.com/baobab-platform/baobab-cp/actions/runs/39982168024), [run 4](https://github.com/baobab-platform/baobab-cp/actions/runs/39982168537), [run 5](https://github.com/baobab-platform/baobab-cp/actions/runs/39982167837), [run 6](https://github.com/baobab-platform/baobab-cp/actions/runs/39982167914), [run 7](https://github.com/baobab-platform/baobab-cp/actions/runs/39982167859) |
| iam-native | [ca5eb723c7845ed9a60e19fd0ef1a1e900d7b97a](https://github.com/baobab-platform/baobab-iam/commit/ca5eb723c7845ed9a60e19fd0ef1a1e900d7b97a) ([PR #137](https://github.com/baobab-platform/baobab-iam/pull/137)) | `d107e5b21e8c9cb21d8e98440ccd8644a0d30e28` | Native issuer/deadline source; not seven-case qualification; [run 1](https://github.com/baobab-platform/baobab-iam/actions/runs/39819133492), [run 2](https://github.com/baobab-platform/baobab-iam/actions/runs/39819132648), [run 3](https://github.com/baobab-platform/baobab-iam/actions/runs/39819132578), [run 4](https://github.com/baobab-platform/baobab-iam/actions/runs/39819131953) |
| infra-49 | [d573582e6302da40a68215746371980e096a8b3c](https://github.com/baobab-platform/infrastructure/commit/d573582e6302da40a68215746371980e096a8b3c) ([PR #52](https://github.com/baobab-platform/infrastructure/pull/52)) | `0de8be75fadb808f1a12469185a85b61fc1bc2b6` | Optional #49 private packet source; older integration locks remain; [run 1](https://github.com/baobab-platform/infrastructure/actions/runs/39986035880), [run 2](https://github.com/baobab-platform/infrastructure/actions/runs/39986036568), [run 3](https://github.com/baobab-platform/infrastructure/actions/runs/39986034668), [run 4](https://github.com/baobab-platform/infrastructure/actions/runs/39986034505), [run 5](https://github.com/baobab-platform/infrastructure/actions/runs/39986034955) |
| dev00-shared | [e2acbed153e8868bc07679374815971acac48f5b](https://github.com/baobab-platform/shared/commit/e2acbed153e8868bc07679374815971acac48f5b) ([PR #376](https://github.com/baobab-platform/shared/pull/376)) | `62d5e4686c2d9b6514eadaa47bc12d2b92cb94e2` | Merged DEV-00 source and reporting; no domain runtime acceptance; [run 1](https://github.com/baobab-platform/shared/actions/runs/40049590842), [run 2](https://github.com/baobab-platform/shared/actions/runs/40049591099), [run 3](https://github.com/baobab-platform/shared/actions/runs/40049590850), [run 4](https://github.com/baobab-platform/shared/actions/runs/40049590809) |
| dev01-infrastructure | [1445195e5304accaf38b29617dc223d12680cd03](https://github.com/baobab-platform/infrastructure/commit/1445195e5304accaf38b29617dc223d12680cd03) ([PR #53](https://github.com/baobab-platform/infrastructure/pull/53)) | `97c6a65cdf0ae191ef9d96c2b9beaa118f2476b4` | Actual native Keycloak setup and CP guarded-bootstrap lifecycle/recovery only; not full authorisation, a domain provider or protected acceptance; [run 1](https://github.com/baobab-platform/infrastructure/actions/runs/40052632487), [run 2](https://github.com/baobab-platform/infrastructure/actions/runs/40052631751), [run 3](https://github.com/baobab-platform/infrastructure/actions/runs/40052631757), [run 4](https://github.com/baobab-platform/infrastructure/actions/runs/40052631801), [run 5](https://github.com/baobab-platform/infrastructure/actions/runs/40052631759), [run 6](https://github.com/baobab-platform/infrastructure/actions/runs/40052631765) |

## Case obligations requiring runtime evidence

Descriptive labels preserve the existing INT-03C obligations and NAB-03 subcases; they do not create canonical scenario IDs.

| Package | Case | Result | Reason |
| --- | --- | --- | --- |
| DEV-01 | expired_orphan_without_state_recovered | PASS | OBSERVED_DEV01_LIFECYCLE_ONLY_NOT_DOMAIN_QUALIFICATION |
| DEV-01 | failed_health_rejected | PASS | OBSERVED_DEV01_LIFECYCLE_ONLY_NOT_DOMAIN_QUALIFICATION |
| DEV-01 | fresh_real_iam_cp_bootstrap_and_replay | PASS | OBSERVED_DEV01_LIFECYCLE_ONLY_NOT_DOMAIN_QUALIFICATION |
| DEV-01 | interrupted_startup_recovered | PASS | OBSERVED_DEV01_LIFECYCLE_ONLY_NOT_DOMAIN_QUALIFICATION |
| DEV-01 | recovery_retested | PASS | OBSERVED_DEV01_LIFECYCLE_ONLY_NOT_DOMAIN_QUALIFICATION |
| DEV-01 | teardown_without_compose_verified | PASS | OBSERVED_DEV01_LIFECYCLE_ONLY_NOT_DOMAIN_QUALIFICATION |
| DEV-04 | issuer-issuance-and-readback | BLOCKED | CURRENT_PROFILE_RUNTIME_NOT_OBSERVED |
| DEV-04 | current-cp-principal-and-link | BLOCKED | CURRENT_PROFILE_RUNTIME_NOT_OBSERVED |
| DEV-04 | wrong-audience-denial | BLOCKED | CURRENT_PROFILE_RUNTIME_NOT_OBSERVED |
| DEV-04 | wrong-tenant-denial | BLOCKED | CURRENT_PROFILE_RUNTIME_NOT_OBSERVED |
| DEV-04 | issuer-revocation-before-expiry | BLOCKED | CURRENT_PROFILE_RUNTIME_NOT_OBSERVED |
| DEV-04 | cp-principal-deactivation | BLOCKED | CURRENT_PROFILE_RUNTIME_NOT_OBSERVED |
| DEV-04 | complete-teardown | BLOCKED | CURRENT_PROFILE_RUNTIME_NOT_OBSERVED |
| DEV-05 | published-home-nav-footer | BLOCKED | CURRENT_PROFILE_RUNTIME_NOT_OBSERVED |
| DEV-05 | wrong-audience-token | BLOCKED | CURRENT_PROFILE_RUNTIME_NOT_OBSERVED |
| DEV-05 | wrong-credential | BLOCKED | CURRENT_PROFILE_RUNTIME_NOT_OBSERVED |
| DEV-05 | disabled-caller | BLOCKED | CURRENT_PROFILE_RUNTIME_NOT_OBSERVED |
| DEV-05 | expired-caller-token | BLOCKED | CURRENT_PROFILE_RUNTIME_NOT_OBSERVED |
| DEV-05 | revoked-caller-token | BLOCKED | CURRENT_PROFILE_RUNTIME_NOT_OBSERVED |
| DEV-05 | missing-grant | BLOCKED | CURRENT_PROFILE_RUNTIME_NOT_OBSERVED |
| DEV-05 | wrong-owner-or-context | BLOCKED | CURRENT_PROFILE_RUNTIME_NOT_OBSERVED |
| DEV-05 | neighbour-tenant | BLOCKED | CURRENT_PROFILE_RUNTIME_NOT_OBSERVED |
| DEV-05 | draft-or-preview | BLOCKED | CURRENT_PROFILE_RUNTIME_NOT_OBSERVED |
| DEV-05 | withdrawn-content | BLOCKED | CURRENT_PROFILE_RUNTIME_NOT_OBSERVED |
| DEV-05 | dependency-outage-and-restoration | BLOCKED | CURRENT_PROFILE_RUNTIME_NOT_OBSERVED |
| DEV-05 | validator-negatives | BLOCKED | CURRENT_PROFILE_RUNTIME_NOT_OBSERVED |
| DEV-05 | teardown | BLOCKED | CURRENT_PROFILE_RUNTIME_NOT_OBSERVED |
