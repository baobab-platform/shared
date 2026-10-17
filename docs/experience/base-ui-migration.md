# Base UI migration register — ADR-SHARED-040 §2.4

Audited 17 October 2026. @base-ui/react 1.9.0, React 19.3.0 and Node 24
are the observed common baseline. Package installation alone is not migration.

| Consumer | Existing implementation | Outstanding family / acceptance |
|---|---|---|
| Shared | Base UI ActionButton; native breadcrumbs/disclosure; controlled Dialog/Tabs in current increment | Browser focus, Escape, portal/RTL tests; release and consumer adoption; manual AT review |
| Nabhold | Base UI shadcn families and Node 24; pinned Shared tokens/geo-core in editorial footprint | Full country-list keyboard equivalence, reviewed map visuals, accessibility/performance budgets and semantic token migration |
| ZuriBeans | Base UI Button/Dialog; pinned Shared tokens/UI; real browser, axe and landing visual tests | Audit selection/navigation families at real call sites; geography utilities when needed, not a mandatory dynamic map |
| CP | Base UI shadcn Button; Shared Disclosure/StatusLabel in non-production showcase | Existing native modal, command palette and custom ARIA tabs require family migration with workflow/focus tests |
| Thamani | Base UI logistics Tabs; published Shared source-labelled tracking evidence | PR #28 workspace validation; real logistics browser tests; future confidential BFF/customer routes and independently approved logistics brand |

Native anchors, headings, tables and sufficient native disclosures remain native.
Custom modal/tab interaction is migrated where Base UI supplies an appropriate
primitive. Preserve controlled state, focus restoration, Escape, directionality,
portal layers and all existing authoritative command checks. Navigation retains
anchor semantics. Remove old dependencies only after their call-site census is empty.

## Release acceptance

For each family, record exact source head and package version, frozen install,
type/lint/build results, browser keyboard/focus/axe/reduced-motion/viewport tests,
visual baseline review, and workflow negatives. A historical green run or a
screenshot attachment does not qualify an edited consumer automatically.
