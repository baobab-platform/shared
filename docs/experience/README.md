# Baobab Experience System — implementation and acceptance register

Governing decision: Accepted ADR-SHARED-040. Audited 17 October 2026.
**Gate names below follow §8, the implementation sequence.** Architecture,
source, package publication, browser CI and protected operation are separate receipts.

| Gate | Source / publication | Remaining acceptance |
|---|---|---|
| BXS-01 architecture | Accepted ADR, ownership, this inventory and migration register | Keep each change tied to its exact PR/head and release |
| BXS-02 tokens | Published 0.2.0 baseline; this increment adds typography, layout, elevations, layers, focus, semantic statuses, map and motion tokens without replacing brand colours | Updated release and per-consumer visual/contrast acceptance |
| BXS-03 geography/evidence | Published 0.2.0 baseline; strict calendar validation and large-coordinate bounds hardening in this increment | New exact-version publication; approved estimate/model provenance and real-service source receipts |
| BXS-04 primitives | Published 0.2.0 baseline; Shared Chromium Storybook; controlled Base UI Dialog/Tabs and strict timelines in this increment | Reviewed visual baselines, manual assistive-technology review and consumer compatibility on the new release |
| BXS-05 consumers | Nabhold tokens/geo-core, ZuriBeans tokens/UI, CP showcase tokens/UI, Thamani tokens/UI/geo-core all pin 0.2.0 | Bounded adoption is not complete migration; see per-consumer register |
| BGX-01 synthetic logistics | Thamani #28 merged shipment workspace, strict evidence validation and real browser keyboard/axe/denial acceptance | Reviewed logistics visual acceptance, approved logistics theme and protected route composition |
| BGX-02 map adapters | Optional MapLibre presentation source in current increment; explicit activation, licensed-origin policy and full evidence list | Exact-version package/browser qualification, publication and consumer adoption; production provider selection remains separate |
| BGX-03 real services | Infrastructure main has dependency harness; PR #35 carries IAM/CP qualification | PR #35 passes four scenario groups but deliberately blocks L4-CP-02 until a real currently certified provider is exercised; TMS tracking remains Proposed/unimplemented |
| BGX-04 protected operation | Not demonstrated | Protected staging, current authorised providers and independently approved go-live |

## Verified historical receipts

- [Publish 0.2.0 packages](https://github.com/baobab-platform/shared/actions/runs/39028924001).
- [SHA512 and published-export verification](https://github.com/baobab-platform/shared/actions/runs/39029098417).
- [Shared foundation/browser CI](https://github.com/baobab-platform/shared/actions/runs/39028293510): 10 browser tests at release-source `15c072d2b7a46c70d16aae635ae14e6bd3a7a525`.
- Consumer audited main: Nabhold `4c90988`, ZuriBeans `5f41021`, CP `35c01d0`, Thamani `1457f81`.

These receipts cover their recorded source, not subsequent unpublished changes.
New package APIs require Changesets, source CI, publication, integrity verification
and separately pinned consumer PRs. Do not replace a registry dependency with Git
main or a local source alias to manufacture consumer acceptance.

Node 24, pnpm 11.24.0 and PostgreSQL 17 where persistence is required remain
baobab-dev standards. No presentation package acquires database/domain authority.

## BXS follow-up evidence and planned chart foundation — 17 October 2026

The earlier audit table is a historical source baseline. Later changes are
independently evidenced rather than retroactively treated as protected go-live:

| Scope | Latest source receipt | Limit |
|---|---|---|
| Shared release sources | [Shared #336](https://github.com/baobab-platform/shared/pull/336), merged | Versioned Geo MapLibre 0.2.0 and core tokens/UI 0.3.1; registry publication not established by merge |
| Nabhold editorial footprint | [Nabhold #66](https://github.com/baobab-platform/nabhold/pull/66), merged; 20 passed checks | Keyboard-equivalent 51-feature Natural Earth map, reviewed screenshots; no legal market or cross-tenant authorisation |
| Thamani shipment workspace | [Thamani #29](https://github.com/baobab-platform/thamani/pull/29), merged; 24 passed checks | Synthetic desktop/mobile visual acceptance only; no live TMS or production customer route |
| ZuriBeans B2B navigation/forms | [ZuriBeans #116](https://github.com/baobab-platform/zuribeans/pull/116), merged; 23 passed checks | Base UI selection and real browser tests; no provider or trade authority changes |
| Chart evidence/table foundation | [Shared #337](https://github.com/baobab-platform/shared/pull/337), under review | New source-only package; no published artifact, charting runtime or production consumer admission |

The proposed Charts module is an optional **presentation model**. It consumes
already-authorised BFF projections and explicitly rejects hidden restricted
data, invalid timestamps and non-finite values. Missing data is not zero.
Nabhold Go-Live v2.0 G12/G15 still requires legitimate CP/context grants,
independent finance/provider contracts, and authenticated real-service tests
before executive group reporting can be called operational. The BXS package
does not calculate portfolio figures, authorise a business relationship or
activate any release.
