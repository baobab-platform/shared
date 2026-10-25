# EA-DEV implementation register

Generated from [the JSON register](ea-dev-implementation-register.json); edit JSON and run `python3 scripts/ea_dev_register.py --write-view`.

**Observed:** 2026-10-25. **Register validation:** SOURCE reporting only. Runtime evidence is scoped to the linked package receipts. **Protected staging, external certification and production:** not accepted.

Selected merged CP/IAM/Infrastructure sources and actual DEV-01..05 receipts. DEV-05 native component results are 12 PASS/2 canonical-provider BLOCKED with verified hashes/teardown; they do not qualify NAB-03. DEV-06 candidate source/runtime progress is separately reported; no canonical provider, legal, protected or production acceptance is inferred. DEV-09 observed on 2026-10-25 from the linked native component receipt; earlier package observation dates remain unchanged. DEV-10 source tooling was inspected on 2026-10-25; the twelve-source matrix and Actions experiments do not refresh or qualify older package observations or user Codespaces.

Observations become STALE after 7 days; compare the observation date with today. CI validates structure and does not refresh evidence.

[Decision precedence, CI policy and closure rules](ea-dev-00-gate-reconciliation.md). NOT_ASSESSED means no new progress claim. Baseline CI does not qualify a current composed runtime.

| Package | Accountable team | Dependencies | Progress / assessment | Observed | CI / runtime | Next action |
| --- | --- | --- | --- | --- | --- | --- |
| **DEV-00** — Decision/gate reconciliation | Shared Platform Architecture | None | SOURCE_MERGED / ACCEPTED | 2026-10-24 | SUCCESS / NOT_OBSERVED | Maintain source/evidence observations as each owner gate lands; retain protected acceptance separately. |
| **DEV-01** — One paved-road integration command | Infrastructure / baobab-dev | DEV-00 | REAL_COMPONENT_SYNTHETIC_DATA / ACCEPTED | 2026-10-24 | SUCCESS / PASS | Reuse the DEV-02-adopted lifecycle for DEV-03 real issuer and CP authorisation; retain the original DEV-01 lifecycle receipts as historical observations. |
| **DEV-02** — Accurate CP Organisation/tenant/mandate fixtures | CP / Shared | DEV-00, DEV-01 | REAL_COMPONENT_SYNTHETIC_DATA / ACCEPTED | 2026-10-24 | SUCCESS / PASS | DEV-03: qualify actual signed issuer -> canonical CP Principal/context/current grant, wrong-audience/tenant and revocation/deactivation denials through this reusable lifecycle. |
| **DEV-03** — Real issuer and CP authority chain | IAM / CP / Infrastructure | DEV-01, DEV-02 | REAL_COMPONENT_SYNTHETIC_DATA / ACCEPTED | 2026-10-24 | SUCCESS / PASS | DEV-04: qualify the original seven INT-03C cases with independent readback, failure recovery and private exact receipts; preserve provider/estate and protected acceptance boundaries. |
| **DEV-04** — Seven-case INT-03C qualification | Infrastructure / IAM / CP | DEV-03 | REAL_COMPONENT_SYNTHETIC_DATA / ACCEPTED | 2026-10-24 | SUCCESS / PASS | DEV-05: qualify the original fourteen NAB-03 cases over actual IAM/CP/BFF/CMS services; preserve provider, legal and protected acceptance boundaries. |
| **DEV-05** — Nabhold IAM/CP/BFF/CMS vertical | Nabhold / CMS / IAM / CP / Infrastructure | DEV-03, DEV-04 | REAL_COMPONENT_SYNTHETIC_DATA / PARTIAL_SOURCE_RUNTIME_UNPROVEN | 2026-10-24 | SUCCESS / BLOCKED | Complete actual CMS provider support and normal CP eligibility/binding/grant qualification, then rerun the unchanged original fourteen-case NAB-03 inventory. |
| **DEV-06** — External client without estate | Infrastructure / CP / IAM / selected provider | DEV-03 | REAL_COMPONENT_SYNTHETIC_DATA / PARTIAL_SOURCE_RUNTIME_UNPROVEN | 2026-10-24 | SUCCESS / BLOCKED | Revisit after baobab-subscriptions onboarding: establish independent subscription/grant provenance, normal provider eligibility and CP binding, and actual entitled resource invocation/audited effect; rerun unchanged INT-07 absent-subscription, unentitled-resource and retired-binding obligations. |
| **DEV-07** — ZuriBeans B2B capability slice | ZuriBeans / Trade / ERP / Trade Docs / Regulations | DEV-03 | REAL_COMPONENT_SYNTHETIC_DATA / PARTIAL_SOURCE_RUNTIME_UNPROVEN | 2026-10-25 | SUCCESS / BLOCKED | Compose actual IAM/CP buyer Principal/Organisation/Market authority, qualify exact RFQ/quotation lifecycle and composed native commitment/replay enforcement, and connect available supplier/ERP/documentary/Regulations providers with explicit unavailable cases. |
| **DEV-08** — Thamani B2B logistics capability slice | Thamani / TMS / Trade Docs / Regulations / Infrastructure | DEV-03 | SOURCE_MERGED / PARTIAL_SOURCE_RUNTIME_UNPROVEN | 2026-10-25 | SUCCESS / BLOCKED | Implement/qualify the owning TMS runtime and accepted contracts; compose actual customer/partner commercial and provider-bound legal/Market/object authority, then execute all INT-04 cases and verified Infrastructure teardown. |
| **DEV-09** — ERP, finance and Subscriptions references | ERP / Payments / Subscriptions / Finance / Infrastructure | DEV-02, DEV-03 | REAL_COMPONENT_SYNTHETIC_DATA / PARTIAL_SOURCE_RUNTIME_UNPROVEN | 2026-10-25 | SUCCESS / BLOCKED | Onboard Subscriptions with current IAM/CP authority and its original negative cases, then revisit DEV-06/INT-07 with CP binding/resource enforcement and unchanged negatives. Implement real Kill Bill and supported owner Payments/ERP/Trade joins; separately qualify human/legal authority, external settlement and protected entry without treating development fixtures as acceptance. |
| **DEV-10** — Developer tooling and contracts | baobab-dev / Shared Foundation / consumers | DEV-01 | SOURCE_IN_PROGRESS / PARTIAL_SOURCE_RUNTIME_UNPROVEN | 2026-10-25 | PENDING_THIS_PR / BLOCKED | Repair provider vulnerabilities and reconcile its reviewed lock without bypassing checks; qualify PR48 final-head owner CI. Adopt the checked Shared Foundation and exact project pins per consumer, prepare Subscriptions Java21/isolated PG17 and Payments Rust tooling, then observe clean user Codespaces and upgrade/rollback drills. Keep DEV-06/INT-07 deferred until Subscriptions onboarding; a source/tooling change is not onboarding or acceptance. |
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
| dev02-cp | [a21f48a80cd5b2387c85aea7f6d97ff3811f2dbb](https://github.com/baobab-platform/baobab-cp/commit/a21f48a80cd5b2387c85aea7f6d97ff3811f2dbb) ([PR #434](https://github.com/baobab-platform/baobab-cp/pull/434)) | `6ed4c63f4e28b3370c4f83c097f22d2308f4d474` | DEV-02 CP-owned fixture v2; 24 non-authorising mandate/scope checks, real PG rollback and routed API negatives. No fictitious legal verification or canonical mandate activation.; [run 1](https://github.com/baobab-platform/baobab-cp/actions/runs/40058008694), [run 2](https://github.com/baobab-platform/baobab-cp/actions/runs/40058008550), [run 3](https://github.com/baobab-platform/baobab-cp/actions/runs/40058008112), [run 4](https://github.com/baobab-platform/baobab-cp/actions/runs/40058008050), [run 5](https://github.com/baobab-platform/baobab-cp/actions/runs/40058007987), [run 6](https://github.com/baobab-platform/baobab-cp/actions/runs/40058008037), [run 7](https://github.com/baobab-platform/baobab-cp/actions/runs/40058007980), [run 8](https://github.com/baobab-platform/baobab-cp/actions/runs/40058005043) |
| dev02-infrastructure | [631e59dc0787f81bec0fed3516a97572e825d949](https://github.com/baobab-platform/infrastructure/commit/631e59dc0787f81bec0fed3516a97572e825d949) ([PR #54](https://github.com/baobab-platform/infrastructure/pull/54)) | `bd181655bf8b2c64420beeeab72129f9811df3bc` | DEV-02 fixture v2 adoption; exact 24-case read-only checks and native lifecycle/recovery/teardown. 29 checks succeeded, 6 skipped. INT-02 passed a targeted rerun; original MFA failure remains BA-AUD-001, not a root-cause repair.; [run 1](https://github.com/baobab-platform/infrastructure/actions/runs/40058049607), [run 2](https://github.com/baobab-platform/infrastructure/actions/runs/40058050105), [run 3](https://github.com/baobab-platform/infrastructure/actions/runs/40058049472), [run 4](https://github.com/baobab-platform/infrastructure/actions/runs/40058049452), [run 5](https://github.com/baobab-platform/infrastructure/actions/runs/40058049454), [run 6](https://github.com/baobab-platform/infrastructure/actions/runs/40058048081) |
| dev03-cp | [718caedca3b9203931b399464e21b0f64ffbe879](https://github.com/baobab-platform/baobab-cp/commit/718caedca3b9203931b399464e21b0f64ffbe879) ([PR #435](https://github.com/baobab-platform/baobab-cp/pull/435)) | `05964feeed9636a9210cc669395f3481ce841007` | Current issuer status enforcement after JWT verification, normalized authority scope binding, fail-closed outage handling. 24 successful owner checks; 6 applicable skips. Native joined proof is separate.; [run 1](https://github.com/baobab-platform/baobab-cp/actions/runs/40074374606), [run 2](https://github.com/baobab-platform/baobab-cp/actions/runs/40074374077), [run 3](https://github.com/baobab-platform/baobab-cp/actions/runs/40074373729), [run 4](https://github.com/baobab-platform/baobab-cp/actions/runs/40074373705), [run 5](https://github.com/baobab-platform/baobab-cp/actions/runs/40074373658), [run 6](https://github.com/baobab-platform/baobab-cp/actions/runs/40074370154) |
| dev03-infrastructure | [ed2fd8ddb6e98edc29820b3e79165b234695876f](https://github.com/baobab-platform/infrastructure/commit/ed2fd8ddb6e98edc29820b3e79165b234695876f) ([PR #55](https://github.com/baobab-platform/infrastructure/pull/55)) | `49037c32206656aef4871c9f94e2a65934267f59` | Native Hydra/Kratos/current CP authority profile and sixteen-case proof, lifecycle recovery and verified teardown. 29 successful checks, 6 applicable skips. INT-02 targeted rerun passed after IMAGE_UNAVAILABLE; no MFA root-cause repair asserted.; [run 1](https://github.com/baobab-platform/infrastructure/actions/runs/40076614129), [run 2](https://github.com/baobab-platform/infrastructure/actions/runs/40076614681), [run 3](https://github.com/baobab-platform/infrastructure/actions/runs/40076614067), [run 4](https://github.com/baobab-platform/infrastructure/actions/runs/40076614049), [run 5](https://github.com/baobab-platform/infrastructure/actions/runs/40076614110), [run 6](https://github.com/baobab-platform/infrastructure/actions/runs/40076612873) |
| dev04-infrastructure | [5d70e40da1c5b3f22b46fe5a1177f843b26ec411](https://github.com/baobab-platform/infrastructure/commit/5d70e40da1c5b3f22b46fe5a1177f843b26ec411) ([PR #56](https://github.com/baobab-platform/infrastructure/pull/56)) | `a7867adf637ceeb4062d199617b2071807f13f6b` | Original seven-case INT-03C native development qualifier; 45 real assertions, independent issuer/CP/provider/host readbacks and teardown, 29 source/failure regressions. 29 applicable CI checks successful, 6 applicable skips. Legacy INT-02 passed without rerun; historical MFA cause remains unestablished.; [run 1](https://github.com/baobab-platform/infrastructure/actions/runs/40095165274), [run 2](https://github.com/baobab-platform/infrastructure/actions/runs/40095164470), [run 3](https://github.com/baobab-platform/infrastructure/actions/runs/40095164458), [run 4](https://github.com/baobab-platform/infrastructure/actions/runs/40095164459), [run 5](https://github.com/baobab-platform/infrastructure/actions/runs/40095164501), [run 6](https://github.com/baobab-platform/infrastructure/actions/runs/40095161115) |
| dev05-infrastructure | [ad3c501932db7b5e5cfb5a3a5bab0c47ada44318](https://github.com/baobab-platform/infrastructure/commit/ad3c501932db7b5e5cfb5a3a5bab0c47ada44318) ([PR #57](https://github.com/baobab-platform/infrastructure/pull/57)) | `8430ffc25868232359fd3b5379fb5d76c4bacc9a` | Native DEV-05 component observation: 12 PASS/2 canonical-provider BLOCKED; hash-verified receipts and teardown. Not NAB-03 or provider/protected qualification.; [run 1](https://github.com/baobab-platform/infrastructure/actions/runs/40115479241), [run 2](https://github.com/baobab-platform/infrastructure/actions/runs/40115479995), [run 3](https://github.com/baobab-platform/infrastructure/actions/runs/40115479219), [run 4](https://github.com/baobab-platform/infrastructure/actions/runs/40115479222), [run 5](https://github.com/baobab-platform/infrastructure/actions/runs/40115479232) |
| dev06-shared | [935be8b6c3598743fb4f553b29f47998308ad5cc](https://github.com/baobab-platform/shared/commit/935be8b6c3598743fb4f553b29f47998308ad5cc) ([PR #389](https://github.com/baobab-platform/shared/pull/389)) | `1f41939abdf26091509592469beb12661ae95f8b` | Development-only external API caller and separate unassigned Pulse validator registry; exact ceiling regressions.; [run 1](https://github.com/baobab-platform/shared/actions/runs/40118059230), [run 2](https://github.com/baobab-platform/shared/actions/runs/40118059159), [run 3](https://github.com/baobab-platform/shared/actions/runs/40118059200), [run 4](https://github.com/baobab-platform/shared/actions/runs/40118056061) |
| dev06-cp | [50a130576f6b126066a56e97a09676b2015f1261](https://github.com/baobab-platform/baobab-cp/commit/50a130576f6b126066a56e97a09676b2015f1261) ([PR #437](https://github.com/baobab-platform/baobab-cp/pull/437)) | `0929e678833f686e833ec569385cf80466eb6f31` | Opt-in leased API-only Principal; actual zero-estate and assignment readback; PostgreSQL owner integration evidence.; [run 1](https://github.com/baobab-platform/baobab-cp/actions/runs/40119240689), [run 2](https://github.com/baobab-platform/baobab-cp/actions/runs/40119240269), [run 3](https://github.com/baobab-platform/baobab-cp/actions/runs/40119240171), [run 4](https://github.com/baobab-platform/baobab-cp/actions/runs/40119240148), [run 5](https://github.com/baobab-platform/baobab-cp/actions/runs/40119240173), [run 6](https://github.com/baobab-platform/baobab-cp/actions/runs/40119240111), [run 7](https://github.com/baobab-platform/baobab-cp/actions/runs/40119240109), [run 8](https://github.com/baobab-platform/baobab-cp/actions/runs/40119235470) |
| dev06-pulse | [1ec50d9b1fefaae888b600e8836834cb777ecccb](https://github.com/baobab-platform/baobab-pulse/commit/1ec50d9b1fefaae888b600e8836834cb777ecccb) ([PR #56](https://github.com/baobab-platform/baobab-pulse/pull/56)) | `e8b41d4f5762bec8a19a40e3b1da4d6db2105208` | Native validator explicit CP audience and case-insensitive OAuth Bearer; vulnerable dependency locks updated without scan suppression.; [run 1](https://github.com/baobab-platform/baobab-pulse/actions/runs/40118681823), [run 2](https://github.com/baobab-platform/baobab-pulse/actions/runs/40118681410), [run 3](https://github.com/baobab-platform/baobab-pulse/actions/runs/40118681244), [run 4](https://github.com/baobab-platform/baobab-pulse/actions/runs/40118681301), [run 5](https://github.com/baobab-platform/baobab-pulse/actions/runs/40118680985), [run 6](https://github.com/baobab-platform/baobab-pulse/actions/runs/40118681270), [run 7](https://github.com/baobab-platform/baobab-pulse/actions/runs/40118677011) |
| dev06-infrastructure | [eeea864f3764038223793fd5dc3ed88791751914](https://github.com/baobab-platform/infrastructure/commit/eeea864f3764038223793fd5dc3ed88791751914) ([PR #58](https://github.com/baobab-platform/infrastructure/pull/58)) | `a45e4792614407eb0fc1ef55b1dc9482f7a993e0` | Native external API-only IAM/CP/Pulse/PG17/Qdrant component observation: 14 PASS, 4 canonical-entitlement/binding BLOCKED; 49 source/failure/custody tests. Verified source identity, receipt hashes, zero estates and complete owned teardown; no canonical INT-07/provider/protected qualification.; [run 1](https://github.com/baobab-platform/infrastructure/actions/runs/40119778054), [run 2](https://github.com/baobab-platform/infrastructure/actions/runs/40119777292), [run 3](https://github.com/baobab-platform/infrastructure/actions/runs/40119777293), [run 4](https://github.com/baobab-platform/infrastructure/actions/runs/40119777295), [run 5](https://github.com/baobab-platform/infrastructure/actions/runs/40119777298), [run 6](https://github.com/baobab-platform/infrastructure/actions/runs/40119777300), [run 7](https://github.com/baobab-platform/infrastructure/actions/runs/40119771152) |
| dev07-trade | [afea037ba8e32154ac920667609ac1016a9fb02a](https://github.com/baobab-platform/baobab-trade/commit/afea037ba8e32154ac920667609ac1016a9fb02a) ([PR #172](https://github.com/baobab-platform/baobab-trade/pull/172)) | `0b99f4aed188361bfaafd198ed5ae577585a3322` | DEV-07 native Medusa/PostgreSQL components only: 16 PASS/9 joined BLOCKED; real persisted missing-role refusal, UG/ZA catalogue, mandatory current clearance and native active-fixture cleanup. No joined IAM/CP/BFF, canonical INT-05/provider/protected qualification or Infrastructure host teardown. 27 successful checks and 8 applicable skips.; [run 1](https://github.com/baobab-platform/baobab-trade/actions/runs/40157210941), [run 2](https://github.com/baobab-platform/baobab-trade/actions/runs/40157211635), [run 3](https://github.com/baobab-platform/baobab-trade/actions/runs/40157211228), [run 4](https://github.com/baobab-platform/baobab-trade/actions/runs/40157211246), [run 5](https://github.com/baobab-platform/baobab-trade/actions/runs/40157210945), [run 6](https://github.com/baobab-platform/baobab-trade/actions/runs/40157208140) |
| dev08-tha | [8a18b0b1613b236f6107b3a6e2e76f9339184b46](https://github.com/baobab-platform/thamani/commit/8a18b0b1613b236f6107b3a6e2e76f9339184b46) ([PR #42](https://github.com/baobab-platform/thamani/pull/42)) | `ae59299e0dc5bfacd8bfec61ed3cacbb341266d9` | DEV-08 source-only admission and dependency hardening: all60 synthetic unit/component tests and authenticated owner build/browser/security gates pass;25 successful checks/7 applicable skips. All20 actual INT-04 logistics obligations BLOCKED on real TMS/contracts/adapters. No native transport receipt, provider qualification or host teardown.; [run 1](https://github.com/baobab-platform/thamani/actions/runs/40160409478), [run 2](https://github.com/baobab-platform/thamani/actions/runs/40160409093), [run 3](https://github.com/baobab-platform/thamani/actions/runs/40160408847), [run 4](https://github.com/baobab-platform/thamani/actions/runs/40160408836), [run 5](https://github.com/baobab-platform/thamani/actions/runs/40160408839), [run 6](https://github.com/baobab-platform/thamani/actions/runs/40160406885) |
| dev09-erp | [62c5e1d6bfc438f17eb442ab26a8e218e5c2cb2b](https://github.com/baobab-platform/baobab-erp/commit/62c5e1d6bfc438f17eb442ab26a8e218e5c2cb2b) ([PR #112](https://github.com/baobab-platform/baobab-erp/pull/112)) | `d205edebd14a970d6c438ac2878b313b72c9aac6` | Native ERP DEV-09 receipt: 39 persisted iDempiere purchase/recording assertions and owned Compose teardown PASS; eight joined finance obligations BLOCKED. Includes source native company/org ownership hardening and 39-case JDBC/PG suite. Synthetic issuer/legal rows/payment evidence; no bank/PSP settlement, current estate IAM, company-B JVM qualification, Subscriptions onboarding or full INT-08 acceptance.; [run 1](https://github.com/baobab-platform/baobab-erp/actions/runs/40164469582), [run 2](https://github.com/baobab-platform/baobab-erp/actions/runs/40164469161), [run 3](https://github.com/baobab-platform/baobab-erp/actions/runs/40164469383), [run 4](https://github.com/baobab-platform/baobab-erp/actions/runs/40164469335), [run 5](https://github.com/baobab-platform/baobab-erp/actions/runs/40164469183), [run 6](https://github.com/baobab-platform/baobab-erp/actions/runs/40164469192), [run 7](https://github.com/baobab-platform/baobab-erp/actions/runs/40164467399) |
| dev09-ory | [182f48c74c2e738b937345694011f87032517e11](https://github.com/baobab-platform/baobab-erp/commit/182f48c74c2e738b937345694011f87032517e11) ([PR #113](https://github.com/baobab-platform/baobab-erp/pull/113)) | `ba4493768dda313ca1f21567ca67942c3cd990a3` | Real Hydra workload/CP contexts and independent native company B. Native InitialClientSetup and synthetic GL accounts are fixture bootstrap only; after restart the unchanged acceptance veto authorises B-only balanced Fact_Acct under an exact CP-persisted decision. Connected component receipt 4 PASS / 3 BLOCKED; native base receipt 40 PASS / 8 BLOCKED. Composed fixed DEV-09 roster 42 PASS / 6 BLOCKED, not full INT-08 or protected/provider acceptance. Synthetic CP human/legal facts; no money moves.; [run 1](https://github.com/baobab-platform/baobab-erp/actions/runs/40177788171), [run 2](https://github.com/baobab-platform/baobab-erp/actions/runs/40177787813), [run 3](https://github.com/baobab-platform/baobab-erp/actions/runs/40177787758), [run 4](https://github.com/baobab-platform/baobab-erp/actions/runs/40177787671), [run 5](https://github.com/baobab-platform/baobab-erp/actions/runs/40177787571), [run 6](https://github.com/baobab-platform/baobab-erp/actions/runs/40177785611), [run 7](https://github.com/baobab-platform/baobab-erp/actions/runs/40177782636) |

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
| DEV-02 | equator-estate:missing | PASS | OBSERVED_DEV02_NON_AUTHORISING_POLICY_INPUTS_NO_APPLICABLE_MANDATE |
| DEV-02 | equator-estate:pending | PASS | OBSERVED_DEV02_NON_AUTHORISING_POLICY_INPUTS_NO_APPLICABLE_MANDATE |
| DEV-02 | equator-estate:revoked | PASS | OBSERVED_DEV02_NON_AUTHORISING_POLICY_INPUTS_REVOKED_OR_EXPIRED |
| DEV-02 | equator-estate:stale | PASS | OBSERVED_DEV02_NON_AUTHORISING_POLICY_INPUTS_REVOKED_OR_EXPIRED |
| DEV-02 | equator-estate:valid_scoped | PASS | OBSERVED_DEV02_NON_AUTHORISING_POLICY_INPUTS_ACTOR_NOT_VERIFIED |
| DEV-02 | equator-estate:boundary_wrong_role | PASS | OBSERVED_DEV02_NON_AUTHORISING_POLICY_INPUTS_NO_APPLICABLE_MANDATE |
| DEV-02 | equator-estate:boundary_wrong_activity | PASS | OBSERVED_DEV02_NON_AUTHORISING_POLICY_INPUTS_NO_APPLICABLE_MANDATE |
| DEV-02 | equator-estate:boundary_wrong_capability | PASS | OBSERVED_DEV02_NON_AUTHORISING_POLICY_INPUTS_NO_APPLICABLE_MANDATE |
| DEV-02 | equator-estate:boundary_wrong_tenant | PASS | OBSERVED_DEV02_NON_AUTHORISING_POLICY_INPUTS_NO_APPLICABLE_MANDATE |
| DEV-02 | equator-estate:boundary_wrong_organisation | PASS | OBSERVED_DEV02_NON_AUTHORISING_POLICY_INPUTS_NO_APPLICABLE_MANDATE |
| DEV-02 | equator-estate:boundary_wrong_market | PASS | OBSERVED_DEV02_NON_AUTHORISING_POLICY_INPUTS_NO_APPLICABLE_MANDATE |
| DEV-02 | equator-estate:wrong_market | PASS | OBSERVED_DEV02_NON_AUTHORISING_POLICY_INPUTS_NO_APPLICABLE_MANDATE |
| DEV-02 | zuribeans:missing | PASS | OBSERVED_DEV02_NON_AUTHORISING_POLICY_INPUTS_NO_APPLICABLE_MANDATE |
| DEV-02 | zuribeans:pending | PASS | OBSERVED_DEV02_NON_AUTHORISING_POLICY_INPUTS_NO_APPLICABLE_MANDATE |
| DEV-02 | zuribeans:revoked | PASS | OBSERVED_DEV02_NON_AUTHORISING_POLICY_INPUTS_REVOKED_OR_EXPIRED |
| DEV-02 | zuribeans:stale | PASS | OBSERVED_DEV02_NON_AUTHORISING_POLICY_INPUTS_REVOKED_OR_EXPIRED |
| DEV-02 | zuribeans:valid_scoped | PASS | OBSERVED_DEV02_NON_AUTHORISING_POLICY_INPUTS_ACTOR_NOT_VERIFIED |
| DEV-02 | zuribeans:boundary_wrong_role | PASS | OBSERVED_DEV02_NON_AUTHORISING_POLICY_INPUTS_NO_APPLICABLE_MANDATE |
| DEV-02 | zuribeans:boundary_wrong_activity | PASS | OBSERVED_DEV02_NON_AUTHORISING_POLICY_INPUTS_NO_APPLICABLE_MANDATE |
| DEV-02 | zuribeans:boundary_wrong_capability | PASS | OBSERVED_DEV02_NON_AUTHORISING_POLICY_INPUTS_NO_APPLICABLE_MANDATE |
| DEV-02 | zuribeans:boundary_wrong_tenant | PASS | OBSERVED_DEV02_NON_AUTHORISING_POLICY_INPUTS_NO_APPLICABLE_MANDATE |
| DEV-02 | zuribeans:boundary_wrong_organisation | PASS | OBSERVED_DEV02_NON_AUTHORISING_POLICY_INPUTS_NO_APPLICABLE_MANDATE |
| DEV-02 | zuribeans:boundary_wrong_market | PASS | OBSERVED_DEV02_NON_AUTHORISING_POLICY_INPUTS_NO_APPLICABLE_MANDATE |
| DEV-02 | zuribeans:wrong_market | PASS | OBSERVED_DEV02_NON_AUTHORISING_POLICY_INPUTS_NO_APPLICABLE_MANDATE |
| DEV-02 | postgres-identity-projections-and-atomic-rollback | PASS | OWNER_REAL_POSTGRES_AND_HTTP_COMPONENT_TESTS_SYNTHETIC_VERIFIER_NOT_IAM_QUALIFICATION |
| DEV-02 | routed-context-api-positives-and-negatives | PASS | OWNER_REAL_POSTGRES_AND_HTTP_COMPONENT_TESTS_SYNTHETIC_VERIFIER_NOT_IAM_QUALIFICATION |
| DEV-02 | canonical-resolver-separation-and-protected-route-absence | PASS | OWNER_REAL_POSTGRES_AND_HTTP_COMPONENT_TESTS_SYNTHETIC_VERIFIER_NOT_IAM_QUALIFICATION |
| DEV-03 | absent_capability_grant_denied | PASS | OBSERVED_NATIVE_PROVIDER_CURRENT_CP_AUTHORITY_ONLY_NOT_PROVIDER_OR_PROTECTED_QUALIFICATION |
| DEV-03 | actual_signed_issuer_and_cp_context | PASS | OBSERVED_NATIVE_PROVIDER_CURRENT_CP_AUTHORITY_ONLY_NOT_PROVIDER_OR_PROTECTED_QUALIFICATION |
| DEV-03 | authorization_code_replay_denied | PASS | OBSERVED_NATIVE_PROVIDER_CURRENT_CP_AUTHORITY_ONLY_NOT_PROVIDER_OR_PROTECTED_QUALIFICATION |
| DEV-03 | cp_denial_independent_of_issuer_status | PASS | OBSERVED_NATIVE_PROVIDER_CURRENT_CP_AUTHORITY_ONLY_NOT_PROVIDER_OR_PROTECTED_QUALIFICATION |
| DEV-03 | cp_principal_deactivation_while_unexpired | PASS | OBSERVED_NATIVE_PROVIDER_CURRENT_CP_AUTHORITY_ONLY_NOT_PROVIDER_OR_PROTECTED_QUALIFICATION |
| DEV-03 | expired_issuer_token_denied | PASS | OBSERVED_NATIVE_PROVIDER_CURRENT_CP_AUTHORITY_ONLY_NOT_PROVIDER_OR_PROTECTED_QUALIFICATION |
| DEV-03 | fresh_credential_after_revoke_succeeds | PASS | OBSERVED_NATIVE_PROVIDER_CURRENT_CP_AUTHORITY_ONLY_NOT_PROVIDER_OR_PROTECTED_QUALIFICATION |
| DEV-03 | issuer_revocation_while_unexpired | PASS | OBSERVED_NATIVE_PROVIDER_CURRENT_CP_AUTHORITY_ONLY_NOT_PROVIDER_OR_PROTECTED_QUALIFICATION |
| DEV-03 | real_kratos_hydra_pkce_distinct_humans | PASS | OBSERVED_NATIVE_PROVIDER_CURRENT_CP_AUTHORITY_ONLY_NOT_PROVIDER_OR_PROTECTED_QUALIFICATION |
| DEV-03 | same_principal_deactivation_approval_denied | PASS | OBSERVED_NATIVE_PROVIDER_CURRENT_CP_AUTHORITY_ONLY_NOT_PROVIDER_OR_PROTECTED_QUALIFICATION |
| DEV-03 | same_principal_provenance_approval_denied | PASS | OBSERVED_NATIVE_PROVIDER_CURRENT_CP_AUTHORITY_ONLY_NOT_PROVIDER_OR_PROTECTED_QUALIFICATION |
| DEV-03 | wrong_audience_denied | PASS | OBSERVED_NATIVE_PROVIDER_CURRENT_CP_AUTHORITY_ONLY_NOT_PROVIDER_OR_PROTECTED_QUALIFICATION |
| DEV-03 | wrong_external_tenant_denied | PASS | OBSERVED_NATIVE_PROVIDER_CURRENT_CP_AUTHORITY_ONLY_NOT_PROVIDER_OR_PROTECTED_QUALIFICATION |
| DEV-03 | wrong_pkce_denied_by_issuer | PASS | OBSERVED_NATIVE_PROVIDER_CURRENT_CP_AUTHORITY_ONLY_NOT_PROVIDER_OR_PROTECTED_QUALIFICATION |
| DEV-03 | wrong_sibling_tenant_denied | PASS | OBSERVED_NATIVE_PROVIDER_CURRENT_CP_AUTHORITY_ONLY_NOT_PROVIDER_OR_PROTECTED_QUALIFICATION |
| DEV-03 | wrong_state_denied_by_relying_party | PASS | OBSERVED_NATIVE_PROVIDER_CURRENT_CP_AUTHORITY_ONLY_NOT_PROVIDER_OR_PROTECTED_QUALIFICATION |
| DEV-04 | issuer-issuance-and-readback | PASS | OBSERVED_ORIGINAL_INT03C_DEVELOPMENT_CASE_WITH_FINAL_TEARDOWN |
| DEV-04 | current-cp-principal-and-link | PASS | OBSERVED_ORIGINAL_INT03C_DEVELOPMENT_CASE_WITH_FINAL_TEARDOWN |
| DEV-04 | wrong-audience-denial | PASS | OBSERVED_ORIGINAL_INT03C_DEVELOPMENT_CASE_WITH_FINAL_TEARDOWN |
| DEV-04 | wrong-tenant-denial | PASS | OBSERVED_ORIGINAL_INT03C_DEVELOPMENT_CASE_WITH_FINAL_TEARDOWN |
| DEV-04 | issuer-revocation-before-expiry | PASS | OBSERVED_ORIGINAL_INT03C_DEVELOPMENT_CASE_WITH_FINAL_TEARDOWN |
| DEV-04 | cp-principal-deactivation | PASS | OBSERVED_ORIGINAL_INT03C_DEVELOPMENT_CASE_WITH_FINAL_TEARDOWN |
| DEV-04 | complete-teardown | PASS | OBSERVED_ORIGINAL_INT03C_DEVELOPMENT_CASE_WITH_FINAL_TEARDOWN |
| DEV-05 | dependency-outage-and-restoration | PASS | OBSERVED |
| DEV-05 | disabled-caller | PASS | OBSERVED |
| DEV-05 | draft-or-preview | PASS | OBSERVED |
| DEV-05 | expired-caller-token | PASS | OBSERVED |
| DEV-05 | missing-grant | BLOCKED | CANONICAL_CAPABILITY_NOT_RESOLVED |
| DEV-05 | neighbour-tenant | PASS | OBSERVED |
| DEV-05 | published-home-nav-footer | BLOCKED | PROVIDER_NOT_ELIGIBLE |
| DEV-05 | revoked-caller-token | PASS | OBSERVED |
| DEV-05 | teardown | PASS | OBSERVED |
| DEV-05 | validator-negatives | PASS | OBSERVED |
| DEV-05 | withdrawn-content | PASS | OBSERVED |
| DEV-05 | wrong-audience-token | PASS | OBSERVED |
| DEV-05 | wrong-credential | PASS | OBSERVED |
| DEV-05 | wrong-owner-or-context | PASS | OBSERVED |
| DEV-06 | absent-subscription-denied | BLOCKED | CANONICAL_ENTITLEMENT_NOT_ESTABLISHED |
| DEV-06 | bound-resource-and-audited-effect | BLOCKED | CANONICAL_ENTITLEMENT_NOT_ESTABLISHED |
| DEV-06 | dependency-outage-and-recovery | PASS | OBSERVED |
| DEV-06 | expired-token-denied | PASS | OBSERVED |
| DEV-06 | fake-estate-injection-denied | PASS | OBSERVED |
| DEV-06 | forged-tenant-denied | PASS | OBSERVED |
| DEV-06 | independent-registered-workload | PASS | OBSERVED |
| DEV-06 | nabhold-tenant-denied | PASS | OBSERVED |
| DEV-06 | own-context | PASS | OBSERVED |
| DEV-06 | retired-binding-denied | BLOCKED | CANONICAL_BINDING_NOT_ESTABLISHED |
| DEV-06 | revoked-token-replay-denied | PASS | OBSERVED |
| DEV-06 | teardown | PASS | OBSERVED |
| DEV-06 | thamani-tenant-denied | PASS | OBSERVED |
| DEV-06 | unentitled-resource-denied | BLOCKED | CANONICAL_ENTITLEMENT_NOT_ESTABLISHED |
| DEV-06 | wrong-audience-denied | PASS | OBSERVED |
| DEV-06 | wrong-owner-denied | PASS | OBSERVED |
| DEV-06 | zero-estates | PASS | OBSERVED |
| DEV-06 | zuribeans-tenant-denied | PASS | OBSERVED |
| DEV-07 | independent-buyer-relationships | PASS | OBSERVED_NATIVE_COMPONENT |
| DEV-07 | persisted-principal-reference | PASS | OBSERVED_NATIVE_COMPONENT |
| DEV-07 | other-buyer-relationship-refused | PASS | OBSERVED_NATIVE_COMPONENT |
| DEV-07 | unknown-customer-refused | PASS | OBSERVED_NATIVE_COMPONENT |
| DEV-07 | revoked-membership-refused | PASS | OBSERVED_NATIVE_COMPONENT |
| DEV-07 | role-bound-market-grants | PASS | OBSERVED_NATIVE_COMPONENT |
| DEV-07 | absent-role-refused | PASS | OBSERVED_NATIVE_COMPONENT |
| DEV-07 | missing-canonical-market-fails-closed | PASS | OBSERVED_NATIVE_COMPONENT |
| DEV-07 | ug-native-catalogue | PASS | OBSERVED_NATIVE_COMPONENT |
| DEV-07 | za-native-catalogue | PASS | OBSERVED_NATIVE_COMPONENT |
| DEV-07 | public-clearance-cannot-be-relaxed | PASS | OBSERVED_NATIVE_COMPONENT |
| DEV-07 | current-market-assortment | PASS | OBSERVED_NATIVE_COMPONENT |
| DEV-07 | expired-market-assortment-refused | PASS | OBSERVED_NATIVE_COMPONENT |
| DEV-07 | future-market-assortment-refused | PASS | OBSERVED_NATIVE_COMPONENT |
| DEV-07 | withdrawn-market-assortment-refused | PASS | OBSERVED_NATIVE_COMPONENT |
| DEV-07 | owned-active-fixtures-removed | PASS | OBSERVED_NATIVE_COMPONENT |
| DEV-07 | current-iam-cp-buyer-principal | BLOCKED | CONNECTED_BUYER_AUTHORITY_NOT_QUALIFIED |
| DEV-07 | supplier-organisation-and-erp-onboarding | BLOCKED | CONNECTED_SUPPLIER_PROVIDER_NOT_QUALIFIED |
| DEV-07 | entitled-private-catalogue-and-price | BLOCKED | CANONICAL_BUYER_MARKET_AUTHORITY_NOT_IMPLEMENTED |
| DEV-07 | rfq-and-controlled-approval | BLOCKED | CANONICAL_RFQ_PROVIDER_NOT_IMPLEMENTED |
| DEV-07 | quotation-lifecycle | BLOCKED | CANONICAL_QUOTATION_PROVIDER_NOT_IMPLEMENTED |
| DEV-07 | guarded-native-order-and-replay | BLOCKED | COMPOSED_BUYER_COMMIT_FENCE_NOT_QUALIFIED |
| DEV-07 | erp-native-step | BLOCKED | CONNECTED_ERP_PROVIDER_NOT_QUALIFIED |
| DEV-07 | shipment-and-document-access | BLOCKED | CONNECTED_DOCUMENTARY_PROVIDER_NOT_QUALIFIED |
| DEV-07 | cross-jurisdiction-seller-authority | BLOCKED | CONNECTED_LEGAL_ACTOR_AUTHORITY_NOT_QUALIFIED |
| DEV-08 | b2b-customer-quote | BLOCKED | TMS_PROVIDER_NOT_IMPLEMENTED |
| DEV-08 | b2b-partner-booking | BLOCKED | TMS_PROVIDER_NOT_IMPLEMENTED |
| DEV-08 | native-tracking | BLOCKED | TMS_PROVIDER_NOT_IMPLEMENTED |
| DEV-08 | native-proof-of-event | BLOCKED | TMS_PROVIDER_NOT_IMPLEMENTED |
| DEV-08 | independent-customer-partner-organisations | BLOCKED | TMS_PROVIDER_NOT_IMPLEMENTED |
| DEV-08 | own-shipment-access | BLOCKED | TMS_PROVIDER_NOT_IMPLEMENTED |
| DEV-08 | unrelated-shipment-denied | BLOCKED | TMS_PROVIDER_NOT_IMPLEMENTED |
| DEV-08 | cross-tenant-denied | BLOCKED | TMS_PROVIDER_NOT_IMPLEMENTED |
| DEV-08 | wrong-market-denied | BLOCKED | TMS_PROVIDER_NOT_IMPLEMENTED |
| DEV-08 | unapproved-transport-legal-actor-denied | BLOCKED | TMS_PROVIDER_NOT_IMPLEMENTED |
| DEV-08 | invented-carrier-denied | BLOCKED | TMS_PROVIDER_NOT_IMPLEMENTED |
| DEV-08 | invented-eta-denied | BLOCKED | TMS_PROVIDER_NOT_IMPLEMENTED |
| DEV-08 | invented-custody-denied | BLOCKED | TMS_PROVIDER_NOT_IMPLEMENTED |
| DEV-08 | recipient-scope-denied | BLOCKED | TMS_PROVIDER_NOT_IMPLEMENTED |
| DEV-08 | absent-grant-denied | BLOCKED | TMS_PROVIDER_NOT_IMPLEMENTED |
| DEV-08 | expired-revoked-authority-denied | BLOCKED | TMS_PROVIDER_NOT_IMPLEMENTED |
| DEV-08 | booking-duplicate-replay-denied | BLOCKED | TMS_PROVIDER_NOT_IMPLEMENTED |
| DEV-08 | dependency-outage-and-recovery | BLOCKED | TMS_PROVIDER_NOT_IMPLEMENTED |
| DEV-08 | unqualified-b2c-interface-denied | BLOCKED | TMS_PROVIDER_NOT_IMPLEMENTED |
| DEV-08 | teardown | BLOCKED | TMS_PROVIDER_NOT_IMPLEMENTED |
| DEV-09 | erp-a-s01 | PASS | PERSISTED_NATIVE_ASSERTION |
| DEV-09 | erp-a-s02 | PASS | PERSISTED_NATIVE_ASSERTION |
| DEV-09 | erp-a-s03 | PASS | PERSISTED_NATIVE_ASSERTION |
| DEV-09 | erp-a-s04 | PASS | PERSISTED_NATIVE_ASSERTION |
| DEV-09 | erp-a-s05 | PASS | PERSISTED_NATIVE_ASSERTION |
| DEV-09 | erp-a-s06 | PASS | PERSISTED_NATIVE_ASSERTION |
| DEV-09 | erp-a-s07 | PASS | PERSISTED_NATIVE_ASSERTION |
| DEV-09 | erp-a-s08 | PASS | PERSISTED_NATIVE_ASSERTION |
| DEV-09 | erp-a-s09 | PASS | PERSISTED_NATIVE_ASSERTION |
| DEV-09 | erp-a-s10 | PASS | PERSISTED_NATIVE_ASSERTION |
| DEV-09 | erp-a-s11 | PASS | PERSISTED_NATIVE_ASSERTION |
| DEV-09 | erp-a-s12 | PASS | PERSISTED_NATIVE_ASSERTION |
| DEV-09 | erp-a-s13 | PASS | PERSISTED_NATIVE_ASSERTION |
| DEV-09 | erp-a-s14 | PASS | PERSISTED_NATIVE_ASSERTION |
| DEV-09 | erp-a-s15 | PASS | PERSISTED_NATIVE_ASSERTION |
| DEV-09 | erp-a-s16 | PASS | PERSISTED_NATIVE_ASSERTION |
| DEV-09 | erp-a-s17 | PASS | PERSISTED_NATIVE_ASSERTION |
| DEV-09 | erp-a-s18 | PASS | PERSISTED_NATIVE_ASSERTION |
| DEV-09 | erp-a-s19 | PASS | PERSISTED_NATIVE_ASSERTION |
| DEV-09 | erp-a-s20 | PASS | PERSISTED_NATIVE_ASSERTION |
| DEV-09 | erp-a-s21 | PASS | PERSISTED_NATIVE_ASSERTION |
| DEV-09 | erp-a-s22 | PASS | PERSISTED_NATIVE_ASSERTION |
| DEV-09 | erp-a-s23 | PASS | PERSISTED_NATIVE_ASSERTION |
| DEV-09 | erp-a-s24 | PASS | PERSISTED_NATIVE_ASSERTION |
| DEV-09 | erp-a-s25 | PASS | PERSISTED_NATIVE_ASSERTION |
| DEV-09 | erp-a-s26 | PASS | PERSISTED_NATIVE_ASSERTION |
| DEV-09 | erp-a-s04b | PASS | PERSISTED_NATIVE_ASSERTION |
| DEV-09 | erp-a-s22b | PASS | PERSISTED_NATIVE_ASSERTION |
| DEV-09 | erp-a-b01 | PASS | PERSISTED_NATIVE_ASSERTION |
| DEV-09 | erp-a-b02 | PASS | PERSISTED_NATIVE_ASSERTION |
| DEV-09 | erp-a-b03 | PASS | PERSISTED_NATIVE_ASSERTION |
| DEV-09 | erp-a-b04 | PASS | PERSISTED_NATIVE_ASSERTION |
| DEV-09 | erp-a-b05 | PASS | PERSISTED_NATIVE_ASSERTION |
| DEV-09 | erp-a-b06 | PASS | PERSISTED_NATIVE_ASSERTION |
| DEV-09 | erp-a-b07 | PASS | PERSISTED_NATIVE_ASSERTION |
| DEV-09 | erp-a-b08 | PASS | PERSISTED_NATIVE_ASSERTION |
| DEV-09 | erp-a-b09 | PASS | PERSISTED_NATIVE_ASSERTION |
| DEV-09 | erp-a-b10 | PASS | PERSISTED_NATIVE_ASSERTION |
| DEV-09 | erp-a-b11 | PASS | PERSISTED_NATIVE_ASSERTION |
| DEV-09 | owned-resource-teardown | PASS | RUN_OWNED_COMPOSE_CONTAINERS_VOLUMES_NETWORKS_AND_TEMP_FILES |
| DEV-09 | current-iam-and-cp-joined-authority | BLOCKED | REAL_HYDRA_WORKLOAD_AND_CURRENT_CP_CONTEXT_PROVEN; KRATOS_CP_HUMAN_BINDING_AND_INDEPENDENT_LEGAL_FACTS_UNQUALIFIED |
| DEV-09 | independent-company-org-isolation | PASS | NATIVE_COMPANY_B_SETUP_AND_ACCEPTANCE_MODE_B_ONLY_BALANCED_FACT_ACCT_WITH_CURRENT_CP_DECISION; SYNTHETIC_LEGAL_CONTEXT |
| DEV-09 | gl-journal-joined-provenance | PASS | NATIVE_COMPANY_B_SETUP_AND_ACCEPTANCE_MODE_B_ONLY_BALANCED_FACT_ACCT_WITH_CURRENT_CP_DECISION; SYNTHETIC_LEGAL_CONTEXT |
| DEV-09 | subscriptions-internal-current-authority | BLOCKED | SUBSCRIPTIONS_NOT_JOINED |
| DEV-09 | subscriptions-commercial-killbill | BLOCKED | KILL_BILL_ADAPTER_NOT_IMPLEMENTED |
| DEV-09 | payments-simulated-lifecycle | BLOCKED | PAYMENTS_NOT_JOINED |
| DEV-09 | external-provider-settlement | BLOCKED | NO_BANK_OR_PSP_PROVIDER_QUALIFIED |
| DEV-09 | trade-native-commit | BLOCKED | TRADE_NOT_JOINED |
| DEV-10 | manifest-and-language-compatibility | BLOCKED | SOURCE_CHECK_IMPLEMENTED; TMS_DECLARATION_AND_SUBSCRIPTIONS_PAYMENTS_RUNTIME_GAPS |
| DEV-10 | exact-node-pnpm-fleet-pins | BLOCKED | SHARED_PIN_IMPLEMENTED; REMAINING_CONSUMER_ADOPTION_UNQUALIFIED |
| DEV-10 | codespace-user-private-image-and-package-access | BLOCKED | ACTIONS_ACCESS_IS_NOT_CODESPACES_USER_ENTITLEMENT |
| DEV-10 | clean-hosted-codespace-noninteractive-onboarding | BLOCKED | NO_FRESH_HOSTED_CODESPACE_OBSERVED |
| DEV-10 | secure-provider-image-and-lock | BLOCKED | PROVIDER_PR48_SECURITY_AND_TOOLCHAIN_LOCK_CHECKS_FAILING |
| DEV-10 | affected-consumer-upgrade-branch | BLOCKED | NO_NEW_TOOLCHAIN_RELEASE_OR_FULL_CONSUMER_UPGRADE_QUALIFICATION |
| DEV-10 | physical-postgresql-migration-separation | BLOCKED | PG16_TO_PG17_PHYSICAL_MIGRATION_NOT_OBSERVED; NEVER_REUSE_VOLUME |
| DEV-10 | coordinated-rollback-drill | BLOCKED | PROCEDURE_IMPLEMENTED; ACTUAL_FLEET_ROLLBACK_NOT_OBSERVED |
