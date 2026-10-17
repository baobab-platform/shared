# BXS-05 — Versioned package publication and consumer adoption gates

Governing ADR: Accepted ADR-SHARED-040. Source release increment: Shared
experience-tokens, experience-ui and experience-geo-core at version 0.2.0.

**Package versioning is not package publication.** Even a merged 0.2.0
version-change PR does not show that GitHub Packages has served an approved
immutable 0.2.0 tarball. Consumers MUST NOT reference an unverified release.

## Release gate

1. Review/merge 0.2.0 source version PR only after Shared CI,
   Experience Foundations, browser and security/foundation gates pass.
2. Use the existing authorised Shared release workflow to build, test,
   publish and audit each version from a commit contained in main. Never
   bypass the repository's Changesets and protected tag/release policy.
3. Verify each package independently exists in the approved GitHub Packages
   registry and contains the expected manifest/export targets. Record exact
   semver, integrity digest and reproducible build evidence.
4. Only then open per-consumer, version-pinned adoption PRs for Nabhold and
   ZuriBeans with protected build, visual regression, keyboard/axe, performance
   and actual market/status-provenance gates.
5. CP Console and Thamani may consume separate bounded versions on their own
   release schedules; do not assume installation grants access to engine data.

## Package adoption boundaries

| Consumer | Initial adoption | Acceptance requirement |
|---|---|---|
| Nabhold | Scoped tokens + geo-core adaptation of editorial Africa footprint | Approved colours, no market-status fabrication, 47-country dataset disclosure, full mobile/browser a11y |
| ZuriBeans | Scoped brand tokens and optional geo-core for B2B footprint | Maintain buyer/supplier authority, map provenance, country list/keyboard alternative |
| CP Console | Scoped design tokens / UI where compatible | No privileged action without CP IAM/PEP checks, no React duplicate |
| Thamani | Base UI logistics views; later map renderer | No unapproved logistics brand migration or claimed live GPS |

The source-observed Thamani palette is explicitly NOT approval of the
future logistics branding. A package release SHALL NOT change a Digital
Estate's production identity, theme or component routing without its own PR.

## BXS-04 residual acceptance

Shared browser Storybook checks and screenshot evidence are real source
acceptance. Goldens require human screenshot review and a committed,
stable baseline before pixel-to-pixel comparisons are mandatory. Manual
screen-reader verification still requires independent review. Mark this
difference in programme dashboards rather than calling everything production
certified.

## Reconciled audit, 17 October 2026

0.2.0 publication and registry verification have passed; all four consumers
have bounded pinned adoption. See the current implementation inventory for
exact historical receipts and remaining acceptance. The preceding release
procedure applies again to each subsequent version. Source changes here do
not update already-published immutable 0.2.0 artifacts.
