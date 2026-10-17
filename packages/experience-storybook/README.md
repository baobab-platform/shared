# BXS-04 — Central Storybook and Browser Acceptance

Private Storybook 10.6 consumes actual @baobab-platform/experience-ui and
experience-tokens workspace packages. Its four switchable themes are SOURCE
OBSERVED, not a claim of brand approval; Thamani's legacy retail palette
especially needs separate approval for its logistics direction.

Build tokens and UI first, then build Storybook and test real Chromium:

    pnpm --filter @baobab-platform/experience-tokens build
    pnpm --filter @baobab-platform/experience-ui build
    pnpm --filter @baobab-platform/experience-storybook build
    pnpm --filter @baobab-platform/experience-storybook exec playwright install chromium
    pnpm --filter @baobab-platform/experience-storybook test:e2e

The automated tests exercise real keyboard action, native disclosure, pending
state, WCAG A/AA/2.2 AA, 390/1440 viewports, semantic colours, reduced motion
and produce screenshots for review. They are real-component acceptance with
synthetic content: no users, tenants, real fleet, approvals, market facts or ETA.
An approved golden-image comparison and MANUAL screen-reader review are still
outstanding. They are not implied by green CI.
