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

BXS-VFA v1.0 adds a synthetic `AdaptiveConditions` fixture. Its actual Chromium
checks exercise the **source-observed** themes across 320/390/768/1024/1440
CSS-pixel viewports, reflow/long text, 200% root text-size stress, reduced
motion, forced-colours, system dark-preference stability and touch/keyboard
semantics. The test attaches reviewable screenshots, but does not regenerate
baselines or claim a physical-device, true browser 400% zoom, non-Chromium,
brand-owner or manual assistive-technology acceptance. Consumers must run their
own route-focused tests and record them in the BXS conformance register.

