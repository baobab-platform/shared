# G-REG-NS step 1: review of ADR-REG-0001 to ADR-REG-0030

**Status:** Review and recommendations. **This page accepts nothing.** Every ADR-REG record stays *Proposed* until the platform architecture owner accepts it individually (`g-reg-ns-resolution.md`: "Do not mass-accept the family").
**Date:** 2026-10-01
**Reviewed:** `baobab-regulations` branch `claude/eloquent-mendel-90t6oy` (30 ADRs, about 2.3 MB), against ADR-SHARED-007 to 018, `g-reg-ns-resolution.md`, ADR-BCP-007/009/018, the workload registry, and the Subscriptions and Trade ADR sets.
**Unmerged PR:** baobab-regulations#4 stays unmerged until the amendments below are made.

## How much of this was read

Be careful how far to trust the per-ADR table. The family is far too large to line-read in one pass, so the review was done in two ways:

- **Read:** the executive decisions, boundary sections and section maps of ADR-REG-0001, 0002, 0004, 0024, 0026 (including the context, identity and Trade/ERP boundaries), 0028 (section map and isolation sections), 0029 (section map) and 0030 (decision, subscription, metering and billing sections), and the ADR-SHARED-018 §8.4 Regulations text.
- **Scanned:** every ADR for platform references, event and capability names, technology commitments, authority claims over Trade/ERP/CP/Subscriptions, and stale terms.

A "Scanned" ADR may still hold a conflict the scan could not see. It needs its owner's read-through before acceptance. The findings below are specific and checkable; the absence of a finding for an ADR is not evidence of correctness.

## What is already right

These are the parts that match current architecture and should be kept:

- **Decision/enforcement split.** ADR-REG-0001 §17–18, ADR-REG-0004 and ADR-REG-0026 §67–68 say Regulations is a Policy Decision Point and the owning engine enforces. That is exactly G-REG-NS Option B and ADR-SHARED-018 §8.4.
- **Control Plane authority.** ADR-REG-0002 §13–14 and ADR-REG-0026 keep capability resolution, tenancy, legal entity, market and isolation requirements with the Control Plane. ADR-REG-0028 §4 keeps isolation *requirements* with the Control Plane.
- **No parallel registries.** ADR-REG-0026 forbids a shadow tenant, legal-entity, market or mapping registry and trusting `X-Tenant-ID` headers.
- **Provider neutrality.** ADR-REG-0010 explicitly rejects a graph database first; PostgreSQL and Qdrant appear as reference implementations, which fits the platform.
- **Commercial boundaries.** ADR-REG-0030 itself says BillableAccount ownership "belongs in the appropriate platform/billing/ERP domain, not Regulations" and that Regulations is not a billing engine.

## Cross-cutting findings

Each needs an amendment before the ADRs named can be accepted.

### F1. Event type names use a namespace the platform retired
- ADR-REG-0024 §20 (and two mentions in 0029) names events `io.baobab.regulations.*.v1`. ADR-SHARED-018 fixes `com.baobab-platform.<context>.<aggregate>.<event>.v<N>`, and the envelope's type pattern rejects anything else.
- The names also differ from ADR-SHARED-018 §8.4, which already names Regulations' two canonical facts: `regulations.product-classification.assigned.v1` and `regulations.compliance-assessment.decided.v1`. ADR-REG-0024's `decision.issued`/`decision.superseded` need mapping onto those, not a second vocabulary.
- The `regulations` event context is `RESERVED` in `contracts/events/v1/context-registry.yaml` until G-REG-NS step 3. No Regulations event type may be used before then.
- **Amend** ADR-REG-0024 (and 0029) to the platform namespace and to §8.4's two facts; register the rest through the event registry after step 3.

### F2. Capability keys are proposals, and one is not a capability
- ADR-REG-0001/0002 §9 list twelve `regulations.*` keys and say they are "conceptual candidate keys". Correct, and they must stay so: the `regulations` domain is not registered, and no key is accepted from an ADR (G-REG-NS "What this is not"). They have to pass the EA-02A census and ADR-SHARED-007 review, and `ea-02a-capability-census.md` lists Regulations as "Pending".
- `regulations.crossborder.evaluate` names a **regulatory profile**, which ADR-REG-0002 §11 itself says is not a capability ("Domain Capability versus Regulatory Profile"). It contradicts its own ADR.
- **Amend** §9 to a candidate list explicitly outside the contract, and reclassify `crossborder` as a profile of `regulations.assessment.evaluate`.

### F3. Platform context: ADR-REG-0026 designs a mechanism the platform has already scoped
- ADR-REG-0026 §22–24 proposes a `PlatformContextAssertion` (JWT, PASETO or signed object, representation "not mandated").
- The platform already has two things: (a) a stored `context_id` the Control Plane resolves and others redeem (`platform-context` contract; ADR-BCP-004; ADR-SHARED-014 for mapping), and (b) resolution assertions in ADR-BCP-007 §61–69, which are explicitly **not production-authoritative until their security model is approved** under ADR-BCP-009 or a child ADR.
- **Amend** ADR-REG-0026: Phase 1 consumes the Control Plane's stored `context_id` and resolves through capability resolution; any assertion is deferred to ADR-BCP-007 §61–69 and must not be defined here.
- ADR-REG-0026's mapping text (§76–82, shared mapping concepts) should cite ADR-SHARED-014 (context redeemed, never supplied) and the mapping findings recorded in `baobab-trade` docs (UUID canonical-entity subjects only).

### F4. Workload identity predates the workload registry
- ADR-REG-0002 §22 and ADR-REG-0026 §34–38 describe service authentication abstractly ("exact IAM technology is outside this ADR"; token exchange "optional").
- The platform has since made Shared's `workload-registry.yaml` the authority for workload id, audience, scopes and lifecycle (`PROVISIONED` until proven end to end, then `ACTIVE`), federated workload tokens with no static secrets (EA-04), and mandatory registry enforcement in production Control Plane (`er-04-production-gates.md`).
- **Amend** both to require a registered workload with scopes drawn from `scope-registry.yaml`, and state that Regulations' own workload starts `PROVISIONED`.
- ADR-REG-0026 §286 names "IAM / Ory" in an example flow; replace with provider-neutral wording consistent with the IAM provider declaration (still planned-only).

### F5. ADR-REG-0030 (commercial) ignores the Subscriptions and Payments engines
- It names "future Ledger/Billing capabilities" and "OpenMeter/Konnect as reference implementation" (§38). The platform has since decided billing: `baobab-subscriptions` adopts Kill Bill (ADR-SUB-0001), owns usage metering and rating (ADR-SUB-0004), billing accounts (ADR-SUB-0011) and the Control Plane billing projection (ADR-SUB-0003), with `baobab-payments` executing payments. ADR-BCP-005/017/018 keep product, subscription, entitlement and classification with the Control Plane.
- Its `BillableAccount` concept (§31) duplicates ADR-SUB-0011 and platform accounts (ADR-BCP-018), even though §31 says ownership is elsewhere.
- **Recommendation: do not accept as written. Split it.**
  - Keep, as a small Regulations ADR: emitting a usage fact (`RegulatoryUsageEvent`, §58–61), what is and is not a billable regulatory unit (§49–57), idempotency (§55–56), and meter versioning (§64–66).
  - Replace the product, subscription, entitlement, pricing, rating and invoicing sections with references to Control Plane and Subscriptions authority.

### F6. Trade overlap: three Trade ADRs, not two
- G-REG-NS step 2 names Trade ADR-0018 and ADR-0021. ADR-SHARED-018 §8.4 also amends **ADR-0024** by reference, and ADR-0024 §1386 still says it "owns the canonical product classification/profile semantics". ADR-REG-0027 puts HS classification in Regulations. Both are *Proposed*, and ADR-REG-0027 does not mention ADR-0024 (no Regulations ADR cites any Trade ADR).
- Trade's ADR headers still say `nabhold/…`; that is a Trade clean-up, noted so it is not mistaken for Regulations' problem.
- **Action** (step 2): amend Trade ADR-0018, 0021 and 0024 so Regulations owns classification and assessment, Trade owns enforcement and logistics/transaction facts; add the Trade ADR cross-references to ADR-REG-0001 §24 and ADR-REG-0027.

### F7. The family does not cite the decisions that now govern it
- None of the 30 ADRs cites ADR-SHARED-014 (trusted mapping), -016 (engine/provider declarations), -017 (capability census and provider declaration; G-FCI-1), -018 (event contexts), `g-reg-ns-resolution.md`, ADR-0007 workload registry, or ADR-SUB-*. They are dated 2026-09-27 to 09-29, before or alongside those decisions.
- **Action:** one pass adding a "Related decisions" block to each ADR, and accepting nothing without it.

### F8. Where engine ADRs live is still unsettled in the repo
- `docs/adr/README.md` in Regulations is the engine template's placeholder, saying ecosystem ADRs live centrally in Shared and that repo-local ADRs are an open question. Pulse and Subscriptions already keep repo-local ADR sets, so repo-local is the working practice.
- **Action:** replace the placeholder README with the actual register (status per ADR) once acceptances begin.

## Recommended path

Accept in waves, each ADR individually, only after its amendments.

| Wave | ADRs | Why | Gate |
|---|---|---|---|
| **1: boundary and integration** | 0001, 0002, 0004, 0019, 0024, 0026, 0028 | They define how Regulations meets the platform. They are mostly aligned (F1–F4, F7 to fix). 0004/0019 need little | amendments F1–F4, F7; Trade amendments F6 in parallel |
| **2: regulatory knowledge model** | 0003, 0005–0018, 0020–0023, 0025, 0027 | Regulations-internal domain design. The scan found no platform conflict, but it is the bulk of the material and was scanned, not line-read | owner read-through per ADR; F7 references; 0027 waits on F6 |
| **3: defer or split** | 0029, 0030 | 0030 per F5. 0029's pack, module and coverage model is plausible, but marketplace admission, signed third-party distribution and publisher governance have no counterpart in the platform and are speculative for a first release | split 0030; for 0029 accept the coverage/pack model later and defer the marketplace sections |

Then the rest of G-REG-NS in order, each on its own approval:

1. (this review) steps 1 and 2 are the work above.
2. Step 3: register the `regulations` namespace after the ADR-SHARED-007 review. This unblocks F1 and F2.
3. Step 4: the Regulations capability census (EA-02A method).
4. Step 5: canonical contracts for accepted candidates (EA-02C method).
5. Step 6: Regulations' provider declaration, planned-only until contracts exist.

## Per-ADR disposition

*Depth* is **R** (the sections named above were read) or **S** (scanned only). *Disposition* is a recommendation, not a decision.

| ADR | Subject | Depth | Recommendation |
|---|---|---|---|
| 0001 | Mission, authority, system boundary | R | Wave 1. Amend: Related decisions (F7); §24 Trade boundary and Trade ADR-0018/0021/0024 reconciliation (F6); §52–55 capability and commercial model defer to the registered namespace (F2) and to Control Plane/Subscriptions (F5) |
| 0002 | Headless engine and capability provider | R | Wave 1. Amend §9 (F2); §22 workload registry (F4); §41–48 events to platform namespace and outbox conventions (F1) |
| 0003 | Authority, authenticity, interpretation | S | Wave 2 |
| 0004 | Advisory, review, enforcement classes | R | Wave 1. Aligned with G-REG-NS; add Related decisions (F7) |
| 0005 | Provider-neutral intelligence, anti-corruption | S | Wave 2. Cites ADR-SHARED-012/013; add -014 (F7) |
| 0006 | Canonical regulatory domain model, identity | S | Wave 2. Check identifier grammar against ADR-SHARED-012 |
| 0007 | Jurisdiction, authority, legal hierarchy | S | Wave 2 |
| 0008 | Instrument, provision, rule, obligation model | S | Wave 2 |
| 0009 | Normative semantics, defeasibility | S | Wave 2 |
| 0010 | Knowledge graph and traversal | S | Wave 2. Technology choice is already deferred ("graph database not first") |
| 0011 | Source registry and trust model | S | Wave 2 |
| 0012 | Content licensing, AI processing rights | S | Wave 2. Needs the legal owner |
| 0013 | Source ingestion and adapters | S | Wave 2. Qdrant named as a derived projection; mark reference implementation |
| 0014 | Provenance, citation, evidentiary chain | S | Wave 2. Cross-check ADR-BCP-023 evidence records |
| 0015 | Temporal and bitemporal versioning | S | Wave 2 |
| 0016 | Machine-executable rules | S | Wave 2 |
| 0017 | Regulatory context and applicability | S | Wave 2. Align with F3 |
| 0018 | Decision and evaluation engine | S | Wave 2. Align decision/event names with F1 |
| 0019 | PDP/PEP separation | S | Wave 1 with 0004: matches G-REG-NS; confirm Trade as PEP wording against amended Trade ADRs |
| 0020 | Explainability, replay | S | Wave 2 |
| 0021 | AI extraction boundary | S | Wave 2. Relate to Pulse AI boundary (ADR-PULSE) |
| 0022 | Human verification and governance workflow | S | Wave 2 |
| 0023 | Change detection and impact | S | Wave 2 |
| 0024 | Events, subscriptions, notifications | R | Wave 1. Amend names and vocabulary (F1) |
| 0025 | Testing, golden cases | S | Wave 2 |
| 0026 | Platform integration and context boundary | R | Wave 1. Amend §22–24 (F3), identity (F4), mapping citations |
| 0027 | Cross-border trade profile | S | Wave 2, after F6 (classification authority) |
| 0028 | Multi-tenancy, isolation, residency | R | Wave 1. Aligned with Control Plane isolation authority; add Related decisions |
| 0029 | Packs, modules, coverage, marketplace | R | Wave 3. Accept the pack/coverage model later; defer marketplace sections |
| 0030 | Commercial product, entitlements, metering | R | Wave 3. Split (F5) |

## Decisions needed from the owner

1. **Wave order and scope:** is Wave 1 first, with Trade ADR-0018/0021/0024 amendments in parallel?
2. **ADR-REG-0030:** split as in F5 (keep usage-event emission, delegate product and billing to the Control Plane and Subscriptions)?
3. **ADR-REG-0029:** defer the marketplace and third-party distribution sections, keeping pack and coverage for a later wave?
4. **Wave 2:** who reads which ADR? The scan cannot replace a domain owner's read (legal-content rights in 0012, rule semantics in 0008/0009/0016, AI governance in 0021).

Nothing in this page registers a namespace, catalogues a key or records an acceptance.
