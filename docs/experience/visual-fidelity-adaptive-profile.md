# BXS Visual Fidelity and Adaptive Experience Profile — BXS-VFA v1.0

**Normative parent:** [ADR-SHARED-040 §7.2](../adr/ADR-SHARED-040%20%E2%80%94%20Baobab%20Experience%20System%2C%20Frontend%20Engineering%20and%20Geospatial%20Presentation.md); **conformance category:** Mandatory BXS-M01/M02/M03/M06/M07, with conditional extensions for BXS-C01..C07.  
**Status:** Proposed for adoption with the governing ADR amendment. This document governs design/acceptance outcomes, **not** brand choices or domain authority.  
**Version:** 1.0, 2 November 2026.

## 1. Goals and non-goals

Deliver recognisable, readable, stable and task-complete experiences across supported viewports, browser engines, operating system accessibility modes, font availability and realistically constrained networks/devices. Common **meaning and behaviour** matter more than pixel-identical screenshots.

**In scope:** sRGB-safe semantic pairings and theme provenance; text and fallback behaviour; reflow and zoom; touch/pointer/keyboard focus; forced-colours and reduced-motion; responsive media; performance and visual-regression release gates; privacy-preserving test evidence.

**Out of scope:** group-wide palette uniformity, forced dark themes, unsupported P3-only colours, a universal frontend, rewriting Django to React, mandatory map/chart runtimes, new domain computations or any transfer of IAM/CP/provider authority.

## 2. Normative requirements

| ID | Area | Consumer SHALL | Verification |
|---|---|---|---|
| VFA-01 | Brand semantics and perceptual safety | Resolve the approved estate palette into standard canvas/foreground/surface/action/on-action/focus/muted/status roles. Use an sRGB fallback for any optional wide-gamut/P3 enhancement; do not rely on physical colour matching or colour alone for information. Maintain 4.5:1 normal text, 3:1 large text where applicable, 3:1 for essential nontext indicators. Evaluate actual background/text combinations, including image overlays and transient states. | Compile/contrast report plus DOM computed-style and manual screenshots; brand-owner acceptance separately |
| VFA-02 | Typography and language | Declare approved font stacks and appropriate fallback metrics. Avoid layout-dependent line breaks, hidden overflow and font-loading layout shifts. Support at least 200% text resize without loss of function; allow larger OS text and locale/currency expansion, maintain visible labels and stable accessible names. Use browser-native and glyph-appropriate fallbacks if licensed face unavailable; no font payload is a mandatory Shared dependency. | Real browser increased-text/long-label tests, sample language/symbol coverage, font-loading/CLS traces, editorial review |
| VFA-03 | Reflow and responsive layout | At 320 CSS pixels equivalent width, preserve function and reading order without horizontal document scrolling, except narrowly justified two-dimensional content such as a map, diagram or grid with an accessible equivalent. Check 320/390/768/1024/1440 viewport classes and relevant landscape/orientation changes. Compose responsively rather than scaling down desktop content. | Actual consumer browser overflow, focus and screenshot receipts; explicit exceptions for 2D widgets |
| VFA-04 | Accessibility preferences | Respect reduced-motion; show focus visibly under keyboard use, and preserve accessible semantics and state under forced-colours/high contrast. Do not override user-forced palette with forced-color-adjust:none except for narrowly tested essential images. Colour scheme (light/dark) SHALL not silently replace an unapproved brand theme. | Browser forced-colours, reduced-motion, colour-scheme, keyboard/AT checks; manual AT review |
| VFA-05 | Inputs and device capabilities | Provide focus and touch target sizing consistent with WCAG 2.2, with appropriate pointer and keyboard paths. No hover-only information or touch-only critical commands. Do not bind business confirmations to gestures or optimistic visual transitions; read back authoritative state. | Keyboard-only, touch pointer, focus restoration, cancellation and denied/revoked tests |
| VFA-06 | Media and resource budgets | Optimise images for density and viewport, use appropriate aspect ratios and width/height reservation, avoid unnecessary wide-gamut/pixel-heavy images, lazy-load optional analytics/maps and follow route-class performance budgets. Fallback visual content SHALL remain truthful and accessible. | Produced asset reports, route-aware Lighthouse and field p75 LCP/INP/CLS where available; disabled-image/failure test |
| VFA-07 | Evidence and state invariants | Preserve readable source, date/as-of, uncertainty and restricted/unavailable labels at every breakpoint and contrast mode. A cosmetic responsive reduction SHALL NOT suppress crucial warnings or approval/mandate provenance. | State-by-viewport fixtures; BXS-M04/M05 negatives maintained without relaxation |
| VFA-08 | Reproducible approval | Attach exact consumer head, locked Shared package versions, browser/tool versions, screenshots and trace class to CI. Reviews of changed visuals SHALL remain distinct from snapshot generation; automation cannot certify all displays or replace manual AT review. | Reviewed committed baselines, immutable CI URLs and explicit pending manual/brand gates |

**WCAG interpretation:** reflow at 320 CSS px equivalent width is not a mandate that a physically narrow 320px phone at 400% browser zoom work in 80 CSS px. The latter is a different, narrower viewport; test actual 320px reflow, 200% text resizing, and browser zoom separately and record conditions. Real browser zoom and root font-size overrides are not identical mechanisms. The 24×24 CSS px WCAG 2.2 minimum target requirement contains exceptions; use a sensible 44 CSS px shared control-height baseline without falsely presenting 44 as WCAG's minimum.

## 3. Baseline matrix and evidence levels

| Dimension | Automated Shared foundation baseline | Consumer requirement | Evidence limitation |
|---|---|---|---|
| Estate source themes | Current Nabhold, ZuriBeans, Thamani **legacy**, CP semantic sources in isolated Storybook | Independently approved theme and local rules at consumer build | Shared themes are source-observed, not automatic approvals |
| Reflow | Five viewport widths: 320, 390, 768, 1024 and 1440 | Route-specific actual content/navigation and appropriate landscape | Foundation story is not a consumer route |
| Fonts and resizing | Synthetic long labels and 200% root font-size stress | Real font loading, fallback languages and user browser zoom | Root font-size change is not browser zoom certification |
| Operating-system preferences | Chromium forced-colours, reduced-motion and prefers-color-scheme sampling | Additional browsers/OS and manual high-contrast/AT as available | Chromium emulation is not a real Windows high-contrast session |
| Interaction | Keyboard focus, 44px baseline buttons and touch interaction where applicable | Real workflows, hover/keyboard/touch parity, negative consequences | Local Storybook click is not a domain action |
| Performance | Deterministic build, unchanged foundation snapshots; real browser traces | Public route Lighthouse and per-class budgets, field p75 vital thresholds | Lighthouse lab does not measure field p75 |
| Image/wide-gamut | Source-controlled sRGB theme hex values | Actual art-directed images and approved P3 enhancements with sRGB fallback | sRGB CSS validation does not ensure every photograph matches |

A first-party frontend is not VFA-VERIFIED until its **own** consumer gates and reviews are recorded in the [cross-estate BXS conformance register](bxs-cross-estate-conformance-register.md). Shared source tests can support but cannot replace consumer evidence.

## 4. Design and component implementation rules

1. Shared CSS SHALL use semantic `--bx-*` variables and permit estates to scope themes without clobbering the document. Typography and brand voice stay estate-owned. Do not introduce a common `font-family` or generic homepage into Shared UI.
2. Component flexboxes, buttons, disclosures, tabs, dialogs, status chips and feedback SHALL wrap lengthy words and labels without clipping; do not obscure focus or information under text enlargement.
3. Shared controls SHALL use semantically appropriate native elements/Base UI, readable focus boundaries in forced colours, and colour-independent labels. A danger action SHALL use the danger semantics already provided in the neutral token palette.
4. Read-only charts/maps remain Conditional. Their data/table alternatives, explicit provenance and no-guesstimation constraints survive responsive/device adaptation.
5. Visual snapshots SHALL remain pinned and reviewer-approved; add synthetic **behavioural stress** tests without auto-updating golden images. Keep CI artifacts privacy-safe.
6. Public routes use existing approved Lighthouse/performance requirements; private CP/operational routes use justified route-class profiles. Re-evaluate budgets from measured emitted artifacts, not by simply raising limits to pass.

## 5. Ownership and review cadence

**Shared** owns reusable assertions, neutral token/compiler checks, browser component fixtures, package version contracts and this profile. **Estate owners** approve brands, fonts, media and route-specific design and collect consumer receipts. **Security, IAM/CP and engine owners** independently approve data/access/operational boundaries. **Architecture** owns breaking or cross-estate profile changes.

Review this matrix quarterly and after material changes to browser/OS, accessibility expectations, font rendering, framework or display technologies. Update VFA minor versions for additive evidence refinements; changing mandatory conformance scope or weakening guarantees requires an accepted ADR amendment with an impact and migration record. For existing nonconforming code, log a dated and owned remediation; time-limited exceptions follow ADR-SHARED-040 §7.1.6.

## 6. Standards anchors

- W3C [WCAG 2.2](https://www.w3.org/TR/WCAG22/) (contrast, text resize, reflow, non-text contrast, target sizing, focus)
- W3C [Understanding Reflow](https://www.w3.org/WAI/WCAG21/Understanding/reflow) (320 CSS px equivalent width and 200% text sizing distinction)
- MDN [forced-colours and system colours](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/system-color)
- Google [Core Web Vitals](https://developers.google.com/search/docs/appearance/core-web-vitals) (field performance metrics distinguished from synthetic lab)
