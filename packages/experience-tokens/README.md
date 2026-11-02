# Baobab Experience Tokens — BXS-02

DTCG 2025.10-shaped, source-validated neutral token and four consumer themes.
All values use the namespaced --bx-* CSS variables, so existing estate styles
are not silently replaced. Source-observed palettes are NOT approvals: especially
Thamani's legacy retail palette is not its future logistics brand decision.

Build/test under baobab-dev Node 24 and pnpm 11.24.0:

    pnpm --filter @baobab-platform/experience-tokens lint
    pnpm --filter @baobab-platform/experience-tokens test
    pnpm --filter @baobab-platform/experience-tokens build

Import the published base.css and one themes/<consumer>.css; set the corresponding
data-bx-theme attribute at the document root. All consumers must independently
approve brand, screenshot and contrast acceptance before replacing current tokens.
Build time contrast assertions do not replace whole-page accessibility testing.

BXS-VFA v1.0 adds a deterministic, machine-readable **source-level** colour-pair
report covering canvas/surface text, focus and foreground/on-status roles:

    node packages/experience-tokens/scripts/report-visual-profile.mjs

The CI workflow attaches the JSON evidence receipt. This is NOT estate brand
sign-off, browser screenshot review, accessibility certification, evidence of
Display P3 appearance, or proof of real-device consistency. Semantic themes use
sRGB six-digit hexadecimal tokens; optional wide-gamut imagery/rendering and
approved palettes remain consumer-owned with an sRGB fallback.

