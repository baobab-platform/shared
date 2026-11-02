# ADR-SHARED-040 — Baobab Experience System: Cross-Estate Design, Frontend Engineering and Geospatial Presentation

**Status:** Accepted — Normative Cross-Repository Experience Architecture; refined 17 October 2026 (Base UI)  
**Decision date:** 17 October 2026  
**Authority:** Baobab Platform Architecture / Platform Owner  
**Primary repository:** baobab-platform/shared  
**Consumers:** Nabhold, ZuriBeans, Thamani, baobab-cp Console, subsequent Group or external Digital Estates where voluntarily adopted  
**Programme:** EA Implementation Plan v2.2; Nabhold Go-Live Master Plan v2.0; BXS-01 onwards  
**Depends on:** ADR-SHARED-007/017/018/021/036; ADR-BCP-002/004/007/009/018/019/026/027; ADR-NAB-0001/0002/0006/0012–0014; ZuriBeans frontend ADRs; ADR-THA-0003–0018, especially ADR-THA-0014; accepted ADR-TMS-0001/0002  
**Does not promote:** proposed TMS ADR-0007/0016/0019, any candidate logistics capability, protected production readiness, or real market/geographic facts.

> **Normative decision.** Baobab SHALL develop and publish a cohesive, premium-quality, accessible, secure and performant **Baobab Experience System (BXS)** from the EXISTING Shared repository. Every first-party frontend SHALL conform to the common foundation and measurable experience gates, while retaining its own branding, independent deployment and authoritative business boundaries. **Shared owns reusable experience code, never a new runtime engine or universal customer frontend.**

## 1. Intent, scope and quality bar

Baobab aspires to match or exceed the strongest contemporary institutional, commerce, logistics and enterprise software experiences, judged by demonstrated user outcomes rather than visual fashion. Quality means clarity, compositional coherence, precision, accessibility, task success, robustness, trustworthy data provenance, device responsiveness and perceived responsiveness. A pretty interface with broken keyboard controls, guessed shipment locations or inconsistent authorisation is **not** a premium experience.

In scope: design tokens; branding/theming contracts; React-compatible primitive and composite component foundations; typography; iconography; interaction and motion; data tables/charts; maps and geospatial presentation; public, partner, customer, staff and executive UX; testing and documentation; release/version governance. Components built by individual estates remain in those repositories until reuse and compatibility are proven.

Out of scope: replacing the Digital Estates; acquiring a new backend domain authority; introducing a mandatory map provider; requiring customers to purchase or deploy a Baobab Digital Estate; granting subsidiary cross-tenant access; assuming an AWS account or running service is activated.

This decision is **Accepted now**. Actual package maturity, consumer migrations, real-service integration, protected staging and production authorisation are independently evidenced. The status of this ADR SHALL NOT be used to claim those later outcomes.

## 2. Decision and architecture

### 2.1 Home and ownership

All shared experience packages SHALL live under baobab-platform/shared/packages/experience-* using existing pnpm workspaces, Turborepo, Changesets and the approved package registry. No baobab-experience repository or service SHALL be created by default. Shared governs versioned package interfaces, source and consumer compatibility. Product teams remain owners of their business-oriented presentation, content, workflows and release cadence.

The initial package family is:

| Package | Scope | Authority exclusion |
|---|---|---|
| experience-tokens | DTCG-inspired source tokens, validated brand themes, CSS custom-property artifacts | No canonical market/legal facts; no product-specific content |
| experience-ui | Portable primitive composition conventions and accessible shared components when mature | No embedded IAM/CP, domain decisions or provider SDKs |
| experience-charts | Neutral display and interaction conventions for charts, tables and timelines | No financial calculation, prediction, KPIs or canonical aggregates |
| experience-geo-core | Validated coordinates, boundaries/projections, source/accuracy display models and accessible map state conventions | No routing, shipment execution, geocoding or tracking authority |
| experience-geo-maplibre | Optional client-side MapLibre canvas, controls and viewport/layer presentation | No mandatory proprietary map vendor or persistent telemetry |
| experience-geo-deckgl | Optional high-volume analytical overlays/temporal replay | No authoritative movement/event store |

Foundation packages MAY be delivered independently in phases. A planned or empty adapter MUST NOT be labelled implemented or publishable. Dependencies SHALL flow from tokens/utilities to primitives and visualisations, never from Shared presentation packages into CP, IAM, ERP, Trade, TMS or estate-specific domain SDKs.

### 2.2 Consumer boundaries

| Consumer | Owns | Shared contributes |
|---|---|---|
| Nabhold | Group editorial identity, public pages, corporate dashboard, CMS composition | Brand-theme aliases, primitives, editorial and Africa footprint visualisations |
| ZuriBeans | B2B buyer/supplier journeys, sourcing and trade context | Trade-oriented theming, map display, forms/tables |
| Thamani | Customer/partner/operations/field/executive logistics UX | Multi-layer maps, accessible timeline/data presentation, geospatial display adapters |
| CP Console | Privileged platform administration, effective context, approval workbenches | Enterprise components and neutral geographic views, never a Tenant Digital Estate |
| External consumer | Its own independent frontend or no frontend | Opt-in packages on standard public interfaces; never an admission prerequisite |

Corporate affiliation conveys neither grants nor cross-tenant visibility. A platform operator's CP Console remains a privileged administrative surface, not another generic estate. All leaf UIs receive typed, already-authorised view models from their owning application/BFF; they NEVER resolve tenant/Organisation/LegalActor/market/capability authoritatively in the browser.

### 2.4 Base UI as the first-party interactive primitive standard (Refinement, 17 October 2026)

Baobab SHALL standardise on @base-ui/react as the default interactive primitive engine across Nabhold, ZuriBeans, Thamani, CP Console and subsequent first-party frontends. shadcn/ui continues as the preferred curated component-authoring approach; it is not a competing runtime primitive engine. The platform MUST retain separate company branding, app deployment, independent authority boundaries and consumer-controlled package adoption.

Base UI SHALL underpin newly added or migrated dialogs, menus, tabs, selects, comboboxes, popovers, tooltips and complex interactive components wherever an appropriate accessible primitive exists. Noninteractive native semantic HTML such as anchors, headings, breadcrumbs, tables, ordered milestone lists and disclosure where native behaviour is sufficient SHALL remain native. No artificial Base UI wrapper is required for static content.

Migration SHALL proceed component-family by component-family with audited real call sites, preserved business semantics and shippable intermediate state. Base UI render is NOT a mechanical drop-in for Radix asChild; controlled state, keyboard focus, portal layering, Escape, touch interaction, event handlers and accessibility contracts SHALL be separately verified. Native link semantics may not be replaced by Button semantics. Old libraries MAY coexist temporarily only through an explicit tracked migration inventory; they SHALL be removed only after replacement coverage is proven.

The Shared experience-ui package SHALL depend on Base UI for its interactive primitives, retain React as a peer dependency and avoid mandatory heavyweight client hydration for otherwise server-rendered pages. Both estate-local component implementations and Shared wrappers SHALL follow a Node 24 build/test profile with version-pinned React and Base UI. Actual migration acceptance requires frozen-lockfile CI, type/lint checks, browser keyboard/focus and reduced-motion tests, accessibility scan, viewport visual regression, and protected workflow tests wherever relevant. Merely declaring Base UI in package.json does not qualify a migration.

Do not rewrite IAM, CP, TMS, ERP or legal authority merely because the frontend primitive runtime changes. An accepted UX standard is not protected staging or production acceptance.

---

### 2.3 Product identity and theming

Foundation tokens SHALL cover semantic colour pairs, typography, spacing, layout/container measures, radii, elevations, focus, motion durations, z-index/layering, map symbology and status palettes. Each estate SHALL apply an independently owned brand-theme layer, and may use different editorial layouts/imagery/tone. Brand-specific raw colours SHALL NOT leak into generic primitives. The identity of Nabhold's gold, ZuriBeans' trade-house warmth, Thamani's logistics experience and Baobab's enterprise administration must remain distinguishable.

Token source SHOULD follow the Design Tokens Community Group 2025.10 stable format for portability, retaining traceability to compiled CSS and potential design-tool variables. Compilers and CI SHALL reject missing semantic aliases, invalid values, unreadable contrast combinations and unapproved brand override drift. Shared SHALL not change a consumer's public brand identity by publishing an unrelated package update.

Visual identity MUST include approved, correctly licensed media and provenance; no invented office, fleet, warehouse, legal presence, coverage, publication or operating metric may be portrayed as actual. Real CMS content takes precedence over explicitly labelled editorial fallbacks.

## 3. Approved engineering runtime baseline

**baobab-dev is the runtime/version source of truth.** Its current controlled manifest specifies Node.js major **24**, PostgreSQL major **17**, pnpm **11.24.0** and Java **17** for relevant JVM engines. Frontend projects and package CI SHALL adopt **at least Node.js 24** (the approved Node 24 major), exact shared package-manager pin and an immutable baobab-dev profile/image meeting the current repository environment contract. An older consumer baseline is migration debt, NOT evidence that Node 22 is an approved enduring exception. CI SHALL report/fail runtime drift in protected/current enforcement profiles; upgrades must use PRs and compatibility evidence rather than unreviewed automatic major bumps.

PostgreSQL 17 is the approved data-store major for engines and application contexts *that actually require PostgreSQL*. An entirely stateless shared token/map rendering package SHALL NOT acquire a database solely to satisfy a version number. Backend-owned databases remain in their respective engines; frontend packages SHALL have no direct SQL/store access. Java 17 applies only where the Java runtime is required, not to browser bundles. Future baobab-dev changes govern through reviewed image/environment-contract upgrades, with no invented universal upgrades.

Next.js App Router, React, TypeScript, Tailwind v4 and accessible shadcn-style primitives are the preferred first-party web baseline. Server Components are default; client components are isolated for interactions. The approved version set SHALL be pinned per consumer lockfile; Node 24 does not excuse runtime or peer-dependency incompatibilities. CSS, JavaScript and React packages SHALL declare exports/types/peers correctly, avoid duplicate React, and remain tree-shakeable. The first-party Base UI decision in §2.4 governs interactive primitives. Migration SHALL remain incremental and verified per consumer; it does not require wrapping sufficient native semantic content.

## 4. Experience quality rules (mandatory)

### 4.1 Information architecture and accessibility

Every public or protected estate SHALL deliver coherent navigation, semantic landmarks (exactly one main landmark per rendered document), hierarchical headings, purpose-driven breadcrumbs on interior pages, meaningful page titles and route completeness. Corporate pages SHOULD offer compelling storytelling, not copy a generic dashboard. Complex workflows SHOULD progressively disclose only necessary controls. Primary actions must be unmistakable; destructive/consequential actions require explainable confirmation and resulting authoritative receipts.

**WCAG 2.2 AA** is the minimum release target; accessibility is not reduced to an automated scan. All essential actions SHALL be keyboard-operable with visible focus, correctly labelled controls, sufficient colour contrast, understandable errors, screen-reader semantics, accessible dialogs, mobile touch targets and reduced-motion support. Maps, charts, drag-and-drop and high-density tables SHALL have complete meaningful textual/tabular alternatives. Selected map objects must be keyboard/list selectable.

Internationalisation, localisation, currency, dates/time zones and jurisdictional content SHALL be context-sensitive. Locale or user-selected currency SHALL NOT manufacture market participation, legal standing or commercial authorisation. Public claim wording MUST distinguish proposed, registered, active, verified and unavailable, citing scoped approved evidence.

### 4.2 Motion, visual composition and content

Motion SHALL convey hierarchy, causality and state—not obscure latency or interfere with essential actions. Prefer CSS for simple transitions, an approved motion library only where layout/gesture choreography merits the cost, and disable nonessential motion on reduced-motion preference. Typography SHALL use a documented scale and licensed/approved font loading, fallbacks and responsive line lengths. Layouts SHALL work from narrow mobile widths through operational desktop displays without fixed-width overflow.

Components SHALL provide designed loading, empty, error, unavailable, restricted, stale, pending and success states. Preview/synthetic/unverified data SHALL be permanently distinguishable from authenticated authoritative information, not merely hidden in development. Optimistic UI MUST NOT declare shipment dispatch, payment, customs release, legal verification or other consequential action complete before the domain owner acknowledges execution.

### 4.3 Performance and operational budgets

For **public and standard portal journeys**, primary field targets at the 75th percentile are LCP <= 2.5 s, INP <= 200 ms and CLS <= 0.1. Lab Lighthouse budgets are at least Performance 90, Accessibility 95, Best Practices 95 and SEO 95 on applicable public routes; protected workflows SHALL use appropriate route-specific comparable targets rather than fake SEO scores. P75 field data and reproducible laboratory measures must be separately reported. Exception-heavy maps MAY use documented, reviewed profile budgets but may not simply waive responsiveness.

Each route SHALL enforce justified JS/CSS/image budgets, lazy-load expensive WebGL/mapping bundles, use accessible static/low-power fallbacks, prefer server composition and Next image optimisation, and avoid costly hydration of purely editorial content. CI SHALL test representative viewport/connection profiles and record regressions; a target is not achieved until measured.

### 4.4 Security, privacy and authority

Browser bundles MUST NOT contain workload/client secrets, service tokens, CP admin credentials, third-party privileged map API secrets, private documents or raw sensitive telemetry. Confidential OIDC/BFF flows, current CP contexts, grants and provider-level PEP checks follow ADR-SHARED-036; a UI role badge, selected tab, group relationship or hidden button does not confer authorisation. Restrict map feature payloads server-side for the requesting tenant/actor/purpose; public shipment share links must be bounded and revocable. Prevent cross-tenant leaks through HTTP caches, WebSockets, SSE streams, vector tiles, CDN assets, popups and exports. No tracking provider receives personal location data without an approved legal and security basis.

## 5. Geospatial presentation and Thamani flagship

### 5.1 Two presentation profiles, not two business authorities

**Editorial geography (Nabhold and ZuriBeans):** lightweight SVG/D3/TopoJSON and reviewed boundary inventory, documented projection, provenance and accessible list controls. A mapped business state must be a verified scoped statement—not polygon coloration derived from an incorporation alone. Missing countries/territories, disputed boundaries and incomplete evidence must be disclosed.

**Operational geography (Thamani and appropriate consumers):** prefer MapLibre GL JS as the rendering candidate for interactive vector maps, with optional deck.gl for dense markers/route visualisation and temporal replay. They are view technologies, not routing, geocoding, real-time position or ETA providers. A reusable interface SHALL support interchangeable, contractually licensed tile/style/geocoding sources, no unauthorized telemetry, explicit attribution, offline/degraded modes and cost/performance evaluation. Production vendor selection requires separate licence, coverage, hosting, retention and region review. Do not use donation-operated public map-tile endpoints as a contracted enterprise SLA.

### 5.2 Source/provenance and accuracy

Location presentation MUST preserve what was observed versus predicted:

| Class | UI treatment | Evidence |
|---|---|---|
| GPS/authorised observed position | Clearly mark observation time and precision | authenticated source, timestamp, accuracy when known |
| Carrier-reported position | Label source and last update | provider/adapter evidence |
| Milestone-derived approximate point | Approximate/last known, never live vehicle | canonical milestone reference |
| Predicted/interpolated position | Distinct estimated styling and confidence | model, inputs, version and generated-at |
| No trustworthy position | Unknown/unavailable; use timeline | no fabricated interpolation |

Coordinates must be validated (longitude -180..180, latitude -90..90), canonicalised and tested for anti-meridian/poles/empty geometry; **latitude/longitude is not a legal market or permission**. Route/leg/stop, corridor, border-crossing, destination and jurisdiction are different canonical concepts. The browser MUST NOT decide that a border was legally crossed or customs released based on position.

### 5.3 Thamani requirements and maturity

Thamani SHALL compose customer tracking, booking/quotes, partner and field UX, exception-first operations and eventually 4PL control-tower modes through approved, independently authoritative services. The map SHOULD support route and leg selection, multimodal display, milestone timeline, stale/location badges, authorised fleet clusters, scoped geofences, source-referenced exceptions and textual equivalents. Future ETA, optimisation, predictive interruption, replay and advanced overlays MUST be explicit gated enhancements: approved transport-domain contracts, provider support, synthetic real-component tests and staging evidence first.

Thamani **must not** put routing/optimisation algorithms, canonical shipment state machines, raw track journals, carrier authority or regulatory decisions into Shared presentation libraries. TMS owns transport execution and accepted observations; CP context/grants/bindings; IAM authentication; Trade Docs and Regulations own their decisions/evidence; Pulse produces clearly labelled advisory intelligence. An accepted Thamani experience ADR is not evidence that TMS proposed tracking/ETA/optimisation ADRs are operational.

## 6. Component and package API rules

- Generic packages SHALL NOT import estate applications or platform engine SDKs, persistent domain repositories, browser-only global APIs during server import, or provider-specific DTOs. They accept immutable/typed display models and callbacks.
- Shared UI primitives SHALL expose accessible names, directionality, state and theme variations with semantic, not business-authority, props. Domain-specific cards, permission logic, workflows and view-model adapters stay with product owners.
- Packages SHALL publish conditional exports where needed (CSS, ESM, types, browser-safe entry); TypeScript types and compiled artifacts SHALL match; consumers SHALL pin immutable approved semver versions and package digests/lockfiles.
- Changesets SHALL version public package changes. Breaking exports, token renames or accessibility semantics require major-version change or explicit migration pathway and consumer matrix. No floating Git main dependencies.
- Security/SBOM/dependency licence verification SHALL cover runtime and tooling dependencies. WebGL and motion libraries SHALL be optional peer/capability additions, not core startup costs.
- Shared SHALL supply maintained examples, component stories and test fixtures. Showcase examples SHALL use clearly synthetic content and cannot simulate access rights.

## 7. Conformance, assurance and release gates

| Gate | Mandatory receipt |
|---|---|
| BXS-01 architecture | This Accepted ADR, implementation inventory, README/ADR index updated; no hidden authority change |
| BXS-02 tokens | Deterministic source-to-CSS build, brand tokens, schema/alias validation, contrast tests, package and licence manifest |
| BXS-04 primitives | Keyboard/focus/a11y tests, SSR compatibility, responsive and reduced-motion demos |
| BXS-03 geography | Coordinate/bounds/accuracy tests, accessible non-map equivalent, data attribution, anti-meridian and no-live-fabrication tests |
| BXS-05 consumers | Per-app pinned package adoption, meaningful visual regression, screenshot review, responsive/a11y/performance budgets |
| BGX-01 Thamani synthetic | Route/milestone/source badges and failure/fallback scenarios under explicitly synthetic fixtures |
| BGX-02+ real transport | Current IAM/CP/TMS/provider contracts, valid binding/context, negative cross-tenant/expired data proofs, real service receipts |
| Protected release | Actual secured staging and independently authorised go-live; never inferred from component CI |

CI SHALL execute Node 24+ compatible package builds and tests, run foundation security gates, require lockfile reproducibility and reject a missing or skipped mandatory receipt. Consumers SHALL test the exact package version they are proposing to adopt; a passing Shared CI does not qualify every consumer deployment. Provide keyboard and assistive-technology manual review, viewport visual snapshots, performance trace, licence/provenance review and accessibility findings with traceable remediation. Security negatives include cross-tenant GeoJSON/position fetches, revoked public share links, leaking map tiles/streams, and stale state represented as real time.

Use EA v2.2 evidence classes honestly: ACCEPTED ADR != MERGED CODE != CI PASS != REAL_COMPONENT_SYNTHETIC_DATA != PROTECTED_STAGING != PRODUCTION_ACCEPTANCE. Package publication is not production activation.


### 7.1 Cross-estate BXS conformance profile — BXS-CXP v1.0 (2 November 2026)

**Normative status and precedence.** This section is an accepted refinement of ADR-SHARED-040 upon its merge to the protected Shared main branch. It establishes **three exhaustive classification categories** for first-party frontend experience concerns: **Mandatory**, **Conditional**, and **Estate-owned**. It does not transfer product, business, legal, identity, data, provider or deployment authority to Shared. Existing Accepted platform and estate ADRs remain controlling for those domains; conflicts MUST be escalated through an explicit architecture decision, never decided by a browser component.

**Applicability.** The profile applies to Nabhold, ZuriBeans, Thamani, Equator & Estate Co., the baobab-cp Console (public and privileged surfaces), and subsequent first-party Group or Platform experiences, including React/Next.js and server-rendered Django/HTML frontends. An externally owned tenant frontend is **not** compelled to use BXS solely because it consumes Baobab APIs; an express contract or voluntary adoption is required. Adoption MAY use compiled, validated CSS/tokens and framework-neutral test contracts without installing React. A qualifying frontend SHALL NOT be rewritten merely to satisfy a package-import quota.

**Classification rule.** Mandatory describes the **outcome and evidence required of every applicable frontend**, not an obligation to import every published package. Conditional requirements activate **when the relevant functionality exists, is introduced, is materially changed, or is offered to users**, including a visually equivalent local implementation. Estate-owned design choices remain independent, but SHALL satisfy Mandatory requirements and all triggered Conditional requirements. Classifying a feature as local, bespoke, synthetic, or behind a flag does not waive safety requirements on a route that is actually available. Production-disconnected synthetic demonstrations remain clearly labelled and gated.

#### 7.1.1 Mandatory — minimum shared experience contract

Every first-party frontend SHALL meet all applicable controls below; a consumer MAY implement them via approved Shared packages, a tested local adapter, or (where appropriate) native semantic HTML. A migration plan does not itself constitute compliance.

| ID | Mandatory concern | Enforceable requirement | Minimum independently reviewable evidence |
|---|---|---|---|
| BXS-M01 | Semantic foundation and theming | Use explicit semantic roles for canvas/surface, foreground/on-colour, interactive emphasis, focus, borders, positive/warning/error/info states, spacing, type scale, motion, layers and responsive layout. Themes SHALL be scoped and validated; brand aliases SHALL resolve to accessible meaning and SHALL NOT silently overwrite another estate's identity. | Versioned token/alias contract, deterministic compilation or equivalent CSS checks, colour-pair/focus contrast checks, responsive screenshots, brand approval record |
| BXS-M02 | Accessibility and information architecture | Target WCAG 2.2 AA on public and protected journeys; provide exactly one main landmark per document, usable skip link, meaningful headings/titles, labelled navigation, contextual breadcrumbs where useful, clear form errors, visible focus, touch/keyboard equivalence and reduced-motion support. Nonvisual alternatives SHALL provide equivalent task information. | Automated axe/static assertions, real keyboard/focus tests, representative mobile/desktop tests, documented manual assistive-technology review and remediation |
| BXS-M03 | Native interaction correctness | Navigation SHALL use links; commands SHALL use buttons/forms. Native semantic HTML is preferred when sufficient. For complex React interactions, Base UI is the first-party primitive standard under §2.4; menus, dialogs, selects, tabs and popovers SHALL preserve controlled state, focus restoration, Escape, portal layering, disabled/pending states and safe event handling. | Unit/component plus real-browser interaction tests on changed call sites, including negative, mobile and cancellation paths |
| BXS-M04 | Evidence, state and feedback presentation | Represent loading, empty, error, unavailable, restricted, stale, pending and success explicitly when applicable. Human-readable status SHALL accompany colour. Missing values SHALL not become zero; estimates, unverified/preview/synthetic data and timestamps SHALL not appear as established facts. An optimistic acknowledgement SHALL never be presented as a completed consequential operation. | State fixtures, negative/revocation/staleness tests, source/as-of and accessible text receipts, explicit verified-vs-synthetic labels |
| BXS-M05 | Security, privacy and authority boundaries | Presentation consumes pre-authorised, minimal, redacted view models; IAM/CP/provider PEP decisions remain server/native-owned. No client-derived tenant, Organisation, LegalActor, market, capability or grant authority. Confidential credentials SHALL NOT enter browser bundles or serialised client/SSR payloads; private data SHALL be disclosed only to an authenticated and appropriately authorised recipient, limited to purpose, and protected against leakage through SSR payloads, shared caches, telemetry/traces, screenshots, tiles, downloads and cross-tenant channels. Fail closed on unavailable authority. | Source/secret scans, browser-network and cache inspection, relevant unauthorised/expired/revoked/context-switch negatives, BFF/native authority tests, controlled artifact custody |
| BXS-M06 | Performance, resilience and responsive quality | Server-first composition, purposeful hydration, responsive layouts without horizontal overflow, efficient media, defined loading/failure recovery and no unauthorised telemetry. Existing §4.3 field p75 Core Web Vitals and public Lighthouse targets remain binding; protected, analytical and geospatial routes require justified route-class profiles rather than fabricated SEO claims. | Production-build tests, route-aware JS/CSS/image receipts, isolated repeatable Lighthouse tests where applicable, visual/layout evidence across representative widths, field data separately identified from lab measurements |
| BXS-M07 | Reproducible consumer and release assurance | Pin approved package versions and immutable lockfiles; build, lint, typecheck where applicable, component/browser/a11y/visual/security checks SHALL run on the proposed consumer source and fail on missing mandatory receipts. Snapshots SHALL be reviewed and approved separately from regeneration; failure artifacts SHALL not expose protected information. | CI workflow run IDs and head SHA, exact packages/integrities, browser versions, reviewed screenshots, documented exceptions and unchanged negative-case evidence |
| BXS-M08 | Honest identity and content | Labels, contact details, product promises, accessibility copy, currency, locale, timezone, market/legal status and enterprise affiliation SHALL be truthful, scoped and traceable to approved product/content authorities. No presentation library may infer registration, activity, affiliation, consent or operational readiness. | Content-owner/brand sign-off, route/locale and no-placeholder checks, provenance review for material claims and cross-estate links |

A token stylesheet without semantic use, a declared Base UI dependency without keyboard coverage, a synthetic screenshot without review, and a green unit test without the applicable consumer browser gate are each **insufficient** evidence for these controls. Accessibility automation does not replace manual assistive-technology verification. Protected-environment grants and real-provider certification are separate from development component conformance.

#### 7.1.2 Conditional — capability-triggered presentation contract

The following capabilities are **not** universally required dependencies. They become required **conformance profiles** when the consumer offers the corresponding feature. Consumers MAY retain their chosen renderer and business-specific composition if the Shared presentation contract and its verification outcomes are met. Heavy map/WebGL/analytics runtimes SHALL remain optional and lazy-loaded.

| ID | Trigger | Required shared contract and guardrails | Additional acceptance |
|---|---|---|---|
| BXS-C01 | Charts, KPIs, financial or other quantitative series | Apply neutral, already-authorised chart view projections: units, source, as-of, available/stale/restricted/unavailable, true nulls, finite values and an equivalent accessible table. Calculations, financial aggregation, forecasting and data ownership remain with the competent domain/BFF. | Correct null/restricted/invalid-value and provenance negatives, table navigation, visual contrast, route bundle/performance tests |
| BXS-C02 | Editorial or interactive geography | Validate coordinates/bounds/accuracy and source labels through Geo Core or an equivalently qualified adapter; provide a keyboard-selectable country/object list, boundary/dataset attribution and an explicit distinction between geography and legal or operating status. | Coordinate/anti-meridian tests, no-market-inference negatives, keyboard and source disclosure evidence |
| BXS-C03 | Interactive MapLibre maps | Use the separately versioned MapLibre adapter only after consumer approval for licensed style/tile origin, CSP/worker, attribution, privacy, consent/activation, context-revocation teardown and accessible non-map view. Never activate the renderer by merely installing the package. | Network egress/cookie negatives, revocation teardown, WebGL failure fallback, mobile/keyboard/a11y and performance evidence |
| BXS-C04 | deck.gl/high-density overlays, temporal playback or analytical replay | Use bounded and exact-source/exact-time projections, explicit activation, strict redaction, non-WebGL equivalent and teardown. Never interpolate or invent trajectories, ETA, border crossings or customs state. | Invalid/missing-frame, denied, stale, teardown, resource/bundle and screen-reader fallback cases |
| BXS-C05 | Data tables, directories and high-volume grids | Preserve headings, row identity, accessible sorting/filtering/pagination, responsive overflow strategy, empty/restricted/stale distinctions, focus continuity and server-authoritative filtering or mutation; virtualisation cannot remove access to data without an equivalent mechanism. | Keyboard/screen-reader rows, large-data performance, sort/filter invariants, cross-scope denial and empty-result cases |
| BXS-C06 | Milestone timelines, step-based onboarding or operational progress | Preserve chronological/source precision, clearly distinguish completed/current/pending/uncertain and actor-authorised outcome; timestamps and event order originate from the owning domain. Never turn a UI step into proof of shipment movement, admission or approval. | Sequence/invalid-time tests, accessible list/timeline, negative unknown/revoked transitions |
| BXS-C07 | Advanced controls (command palette, dialogs, combobox, select, tabs, multi-step forms, confirmations) | Base UI/native semantics as appropriate, predictable keyboard navigation, complete focus management, clear errors, mobile touch usability and controlled pending/cancel semantics. Consequential actions require domain-specific authorised confirmation and authoritative readback. | Full open/close/escape/focus return, keyboard/touch, cancellation, double-submit, unauthorised and stale-context tests |

A Conditional control becomes **NOT APPLICABLE** only after a documented feature inventory shows that the trigger is absent. If implemented locally before a Shared component is mature, the local owner SHALL maintain an explicit compatibility/migration record; adoption of a published replacement requires consumer-level tests. Conditional maps, charts, tables and timelines do not grant new data collection, analysis, routing, approval, tracking or provider authority.

#### 7.1.3 Estate-owned — protected product differentiation

Shared **SHALL NOT** standardise, select, rebrand, import or centrally control an estate's logos/marks, approved palette and distinctive typography, photographs and illustration, hero/media composition, editorial storytelling, commercial site taxonomy, menu grouping, page sections, product positioning, role journeys, domain forms or backend workflows. Estate-owned is an **ownership category, not a quality or security exemption**.

| Estate | Identity and journey ownership retained | Shared may enforce |
|---|---|---|
| Nabhold | Institutional gold/ink direction, corporate editorial layout, group/portfolio/investment and executive compositions, CMS content | Semantic token aliases, navigation/CTA behaviour, accessible reporting views and conformance receipts |
| ZuriBeans | Distinctive agricultural commodity trade-house identity, approved Figma layout and typography, product/quality/origin content, separately governed buyer and supplier journeys | Accessible primitives, source-labelled data/geography, responsive and release gates |
| Thamani | Independently approved logistics branding (not inherited from legacy retail), B2B customer/partner/operations workflows and specialised shipment UX | Status/timeline/provenance controls, advanced navigation, optional protected map/overlay presentation |
| Equator & Estate Co. | Property/infrastructure brand, editorial/asset presentation, lead and customer journeys, frontend framework transition choice | Framework-neutral semantic CSS, markup, accessibility and performance contracts; React-only imports are not mandatory for Django |
| Baobab Control Plane | Privileged administrative information architecture, effective context, governed organisation/tenant/approval/operation experiences and operator language | Common primitives and feedback standards; CP alone remains authority for administration and access decisions |

Every estate SHALL own its theme approval record and change-control process. The presence of source-observed colours in Shared is **not** brand approval. No Shared patch, theme upgrade, brand inheritance, or family resemblance decision may silently alter an approved local identity. Conversely, a brand-specific design must not override contrast, focus, clarity, restricted-data, security or evidence rules. Shared may provide **unopinionated composition patterns** as optional tools, never a mandatory common homepage or a universal company UI.

#### 7.1.4 Package adoption, extraction and compatibility policy

1. The six published distributable modules remain experience-tokens, experience-ui, experience-charts, experience-geo-core, experience-geo-maplibre and experience-geo-deckgl. Storybook is a private source/test workspace, **not** a seventh distributable dependency. Consumers SHALL install **only the packages and rendering runtimes their actual usage requires**; full six-package installation is not itself a conformance measure.
2. Dependency direction remains tokens/neutral utilities → primitives and presentations → estate-owned adapters/compositions. Presentation modules SHALL NOT import engine SDKs, IAM/CP authority logic, market/organisation resolvers, customer sessions or persistent domain stores. React remains a peer, not a secretly duplicated renderer.
3. A proposed Shared extraction SHALL document at least two actual consumer contexts **or** a specific cross-estate safety/accessibility need, its stable authority-neutral API, SSR/hydration and tree-shaking behaviour, semantic theming, tests, portability cost, and a staged de-duplication plan. Copying an entire estate shell merely for reuse is prohibited.
4. Package sources and published artifacts are separate gates. Changesets, pinned versions/integrities, conditional exports, Node/toolchain compatibility, release receipts and per-consumer acceptance SHALL precede promotion. Changing a theme, public component signature, keyboard model or semantic state requires compatibility review and an appropriate version/migration policy; no consumer is silently rewritten by a Shared release.
5. Native HTML, standard CSS and reviewed local components remain legitimate when Shared offers no equivalent or the equivalent introduces unjustified cost. Document the comparison, do not invent a wrapper. Existing local implementations SHALL be migrated family-by-family as they are touched, without breaking product journeys.

#### 7.1.5 Verification, conformance registry and sign-off

Shared SHALL maintain a cross-estate BXS consumer register linked from `docs/experience/README.md`. Each first-party estate SHALL record, for every applicable BXS-M and triggered BXS-C control: owner; frontend/framework and surface; applicability and justification; approved theme/version; direct package versions and digest/lock reference (if installed); revision under test; automated/manual evidence links; profile and test-tool versions; findings; release tier; last review date; planned remediation; and any time-limited exception. **No evidence means NOT VERIFIED**, not compliant.

Use the following distinct lifecycle values: **NOT ASSESSED**, **IN PROGRESS**, **VERIFIED** (only for the explicitly recorded evidence class and source), **NONCONFORMING**, **NOT APPLICABLE** (Conditional only, with rationale), and **EXCEPTION APPROVED** (with expiry and controls). A VERIFIED development source/browser gate is **not** a certification of real IAM/CP/TMS providers, protected staging, legal readiness or production. Shared package publication alone is not per-estate VERIFIED. CI SHALL reject a missing, skipped or failing receipt when that control is a mandatory gate for the affected change.

Verification SHALL be at the **actual consumer head SHA** with immutable package resolution. Representative browser tests SHALL include responsive layout, keyboards, meaningful focus, a11y, reduced motion, loading/denial/error states and domain-relevant negatives. The approved ZuriBeans-style emitted asset ceilings (800 KiB aggregate JS / 250 KiB largest chunk / 64 KiB CSS / 250 KiB raster image) are a **reference public-estate profile, not an unconditional whole-platform rule**: a route-class threshold or change requires measurements and documented architectural review, never a silent budget increase to make CI pass. Lighthouse results and production field p75 measurements SHALL be recorded separately.

**Ownership and approval.** Shared maintainers own published BXS contracts and reusable conformance tooling. Each estate's technical owner owns application compliance, brand approval and product UX; its security/domain owners own confidentiality, grants and consequential operations. The Platform Architect or authorised Architecture Review function adjudicates profile interpretation and cross-estate changes. Merge of a docs/implementation PR is not an independent grant to deploy or operate a protected service.

#### 7.1.6 Exceptions, migration, and controlled evolution

- **Pre-existing debt:** Existing code predating this refinement MAY be tracked as IN PROGRESS with an owner, affected surfaces, concrete remediation, test plan and target review. New or materially changed code SHALL comply with triggered controls immediately unless a formally approved exception applies. A vague future migration or a passing unrelated CI job is not an exception.
- **Exceptions:** An exception request SHALL identify control ID/surface, business justification, risk and affected users/tenants, compensating controls, measurable exit criteria, accountable approver and expiry/re-review date. Security and privacy exceptions require independent security approval. No exception may authorise fabricated business/legal facts, cross-tenant disclosure, client-side privilege escalation, concealed restricted data or false protected-release claims. Expired exceptions revert to NONCONFORMING until remediated or explicitly renewed.
- **Adaptation:** Improvements to token names, components, tools, thresholds, device/assistive-technology coverage, supported frameworks or optional technology choices SHALL be evaluated on outcomes, compatibility, rollout cost and actual consumer evidence. Additive clarifications may use a reviewed minor profile revision with register and test updates; changes to category semantics, mandatory scope, authority boundaries, removal of guarantees, or incompatible component semantics require an explicit accepted ADR amendment with impact analysis and a migration window.
- **Review cadence and promotion:** Reconcile the register on each affected consumer adoption PR and before protected release; review platform-wide at least quarterly or after a material framework/security/accessibility change. Any new mandatory third-party dependency or universal frontend rewrite requires its own architecture justification and owner approval. First-party exception practice cannot be imposed automatically on external tenants.
- **Order of migration:** Prefer verified semantic tokens and critical native interactions, then feedback/provenance and reusable quality workflows, then high-value conditional views. Do not block independent product design evolution on unrelated WebGL or analytical packages. Preserve existing negative tests and approved baselines during each migration.

This profile is **outcome-oriented, enforceable and evolvable**: common standards govern trust and usability; product owners govern their distinctive brands and journeys; competent platform engines govern business truth and authority.

## 8. Work sequence, ownership and adoption

| Sequence | Work | Repository / owner | Dependency |
|---|---|---|---|
| BXS-01 | Accepted ADR and inventory | Shared | This decision |
| BXS-02 | experience-tokens package + branded theme validation | Shared | BXS-01 |
| BXS-03 | experience-geo-core and neutral accuracy/source types | Shared | BXS-01 |
| BXS-04 | Accessible experience-ui and stories + CI | Shared | BXS-02 |
| BXS-05 | Nabhold footprint and ZuriBeans map adoption | Each estate | BXS-02/03 + local acceptance |
| BGX-01 | Thamani synthetic interactive tracking/control-tower visual prototype | Thamani | BXS-03, ADR-THA-0014 |
| BGX-02 | MapLibre/deck.gl adapters with provider selection and security review | Shared | BXS-03, need proven |
| BGX-03 | TMS, CP, IAM and Thamani real-component acceptance | Infrastructure orchestrates; domain owners own assertions | Accepted operational contracts, EA INT profiles |
| BGX-04 | Protected staging and real geographic/telemetry validation | Infrastructure, TMS, Thamani, Security | Actual operational readiness |

Existing estate code is not automatically nonconforming merely because it predates package extraction; **new frontend work and actively changed code SHALL follow this decision**, with a tracked migration plan for prior patterns. In particular Node 22 and duplicative raw theme tokens are current migration items, not permanent opt-outs. Gate owners SHALL separate architectural adoption from runtime certification.

## 9. Alternatives and consequences

**Separate experience repository — rejected now.** It duplicates workflows, version governance and authority without sufficient benefit. Revisit only with independently evidenced scale/ownership need and accepted Shared supersession.

**One branded universal application — rejected.** Violates autonomy, product personas, independent deployment and external API-only adoption.

**One large mandatory component/map package — rejected.** Creates unnecessary bundle weight, coupling and impossible upgrade coordination.

**Browser-composed domain authority / map as truth — prohibited.** It would silently bypass CP/engines, leak cross-tenant data and misrepresent logistics facts.

**Do nothing / copied UI primitives — rejected.** Produces accessibility drift, redundant maintenance and inconsistent user trust.

Consequences: Shared gains responsible frontend package ownership and compatibility/test obligations; each consuming repository gains an explicit migration and acceptance workload; maintaining a high-quality experience is a continuous engineering discipline rather than a one-off design exercise.

## 10. External standards and follow-up

- WCAG 2.2 Recommendation — https://www.w3.org/TR/WCAG22/
- Core Web Vitals thresholds — https://web.dev/articles/vitals
- DTCG Format Module 2025.10 (Community Group report; NOT a W3C Recommendation) — https://www.w3.org/community/reports/design-tokens/CG-FINAL-format-20251028/
- MapLibre GL JS documentation — https://maplibre.org/maplibre-gl-js/docs/
- WAI Authoring Practices — https://www.w3.org/WAI/ARIA/apg/
- Baobab baobab-dev version manifest — https://github.com/baobab-platform/baobab-dev/blob/main/config/versions.yaml

**Implementation rule:** new packages must be accompanied by real package tests, deterministic generated artifacts and a bounded consumer contract. The first foundation increment SHALL focus on source-validated tokens and geospatial display utilities; it SHALL NOT falsely claim a complete React component system, live logistics map or certified provider integration.
