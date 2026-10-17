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
| BGX-01 synthetic logistics | Thamani main has internal tabs/tracking evidence; PR #28 adds shipment workspace | Actual logistics browser/visual acceptance, approved logistics theme and route composition |
| BGX-02 map adapters | Not implemented at audited main | Bounded optional renderer, licensed provider/style decision, accessible fallback, attribution and privacy acceptance |
| BGX-03 real services | Infrastructure main has dependency harness; PR #35 carries IAM/CP qualification | Real IAM/CP acceptance must pass; TMS tracking contracts remain Proposed and no tracking service is implemented |
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
