# Baobab Experience System — implementation inventory

Governing [ADR-SHARED-040](../adr/ADR-SHARED-040%20%E2%80%94%20Baobab%20Experience%20System%2C%20Frontend%20Engineering%20and%20Geospatial%20Presentation.md), Accepted 17 October 2026.

| Increment | Repository source status | Production evidence |
|---|---|---|
| BXS-01 | Accepted ADR and documented ownership | Architecture only |
| BXS-02 | experience-tokens: four source-observed palettes, contrast validation, deterministic CSS | Consumer branding/release approval not yet shown |
| BXS-03 | experience-geo-core: source-labelled coordinates, anti-meridian, negative tests | No real tracking or MapLibre provider |
| BXS-04 | Accessible primitives and central multi-brand Storybook with Chromium browser acceptance | Browser CI and reviewed visual/assistive-tech evidence required; no golden baselines yet |
| BXS-05 | Nabhold/ZuriBeans pinned adoption | Not implemented |
| BGX-01 | Thamani synthetic logistics UX | Not implemented |
| BGX-02+ | TMS/CP/IAM and dynamic map integrations | Not implemented |

Node 24+, pnpm 11.24.0, PostgreSQL 17 for services needing database persistence;
a pure CSS/geometry package has no database. Run each package's lint/test/build
or the experience-foundations CI job. Tag-gated Shared Changesets publication
remains separate from merge. No synthetic fixture conveys domain authority.

## BXS-04 remaining acceptance

The initial React primitives have semantic SSR/negative tests and opt-in CSS. Portable CSF stories are shipped as source examples; they are not evidence of a running Shared Storybook, visual snapshots or real-browser keyboard/assistive-technology acceptance. Provider-agnostic primitive migration into Nabhold, ZuriBeans, Thamani and CP remains separately gated.

## Base UI refinement

ADR-SHARED-040 §2.4 governs new interactive primitives. See [cross-estate migration register](base-ui-migration.md). This decision does not claim all four applications have migrated.

## BXS-04 browser harness

The new private Storybook workspace builds from the actual versioned package APIs. Chromium verifies keyboard behavior, native focus/activation, automated axe WCAG checks, brand semantic visual contracts, responsive bounds and reduced-motion behavior. Screenshots are preserved for review but **not yet authoritative golden baselines**. Production accessibility and manual screen-reader reviews remain independently gated.
