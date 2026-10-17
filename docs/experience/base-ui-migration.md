# Base UI migration register — ADR-SHARED-040 §2.4

Shared engineering selection: @base-ui/react for interactive primitives; Node 24, pnpm 11.24.0. Component migrations are **not** equivalent to a dependency declaration.

| Product | Present source implementation | Next migration wave | Acceptance remaining |
|---|---|---|---|
| Shared | Native ActionButton, semantic Breadcrumb/Disclosure/Feedback/Timeline | Base UI ActionButton, later interactive forms/dialogs | Build, peer/bundle, SSR, stories, browser focus |
| Nabhold | Base UI-based shadcn components present; Node 22 package metadata | Audit, adopt Node 24, prove interaction and visual coverage | CI, upgraded runtime, keyboard/axe |
| ZuriBeans | Native dialog/form controls; standalone Storybook | Dialog and selection interactions using Base UI | Portal/escape/focus and buyer/supplier tests |
| Thamani | Older retail storefront, no modern interactive primitives | Introduce Base UI as logistics experience is built | Logistics-native flows and tracking provenance; no fake live TMS |
| CP Console | Radix Slot button, native controlled dialog | Base UI Button/Dialog; remove stale Radix when unused | Role/permission, confirm/cancel, focus/escape/axe |

The migration procedure is one component family plus real call sites per PR. Record changed API/props, tested keyboard behavior, reduced-motion and screenshot evidence; do not merge a broken conversion. Keep each estate's authorised BFF/domain projections and independent brand themes.
