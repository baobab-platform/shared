# BGX-02 — optional deck.gl evidence overlay acceptance

**Governing:** Accepted ADR-SHARED-040 §5 and §8, Nabhold Go-Live v2.0.
**Status:** Implementation PR candidate only; publication and production
acceptance require their own receipts.

## Implemented in the Shared source increment

- `experience-geo-deckgl` exposes server-import-safe validation, explicit
  exact-time frame selection, text/table fallback and a consent-based client
  MapLibreOverlay adapter via consumer-supplied factories.
- No direct MapLibre, deck.gl, transport provider or IAM SDK import. Compatible
  consumer-owned runtime packages are `@deck.gl/layers@9.4.0`, `@deck.gl/maplibre@9.4.0`,
  and `maplibre-gl@6.14.0`; consumers must separately pin and test them.
  The package manifest deliberately excludes WebGL peer declarations because
  pnpm 11 auto-installs them. An opt-in consumer explicitly installs the
  version-pinned deck.gl/MapLibre runtime; Shared remains model-only.
- Positive and negative tests exercise observed/estimated distinction, unknown
  points, anti-meridian positions, duplicate IDs, impossible dates, frame
  ordering, runtime budgets, restricted-data rejection, consent and cleanup.
- Overlay never creates routes/ETAs, interpolates location, stores raw telemetry,
  persists snapshots or calls a provider.
- The upstream MapLibre/Deck adapter is overlaid (`interleaved:false`) to
  avoid a default shared WebGL context; choosing interleaving requires separate
  device/CSP/performance qualification and an accepted consumer PR.

## Authority/evidence matrix

| Gate | Required evidence | Current disposition |
|---|---|---|
| BGX-01 source UX | Thamani source workspace #28 and browser visuals #29 | Merged synthetic source only |
| BGX-02 neutral overlay | Shared source CI, pinned package, export and digest verification | This PR proposes source; publication pending |
| BGX-02 real browser | Actual deck.gl 9.4.0/MapLibre 6.14.0 renderer at narrow/desktop widths, axe, keyboard table, WebGL failure and CSP/resource-policy denials | **Not yet demonstrated** |
| BGX-03 real components | IAM-issued identity, CP tenant/Organisation/capability grants, native transport object permission, denied cross-tenant/expired/revoked evidence | **Blocked on real provider/accepted contracts** |
| BGX-04 protected operation | Authorised staging account, real certified endpoint, source coverage/licence/cost/privacy assessment, operations acceptance | **Not yet demonstrated** |

A map snapshot is not a market, legal-actor, organisational or shipment
entitlement. Nabhold is a non-trading holding company and must not acquire
transport authority through a frontend package. Subsidiary autonomous Tenants
remain separate.

## Release sequence (fail closed)

1. Merge the exact Shared source only if Node 24, frozen pnpm, tests, Storybook,
   Foundation/security and release verifier checks are green.
2. Changesets prepares a reviewed source version from main; test and merge the
   exact version PR. No direct manifest rewrite on `main`.
3. An authorised maintainer deliberately runs the existing
   `Publish Shared Packages` release on a commit in main. A source version
   is not a published GitHub Packages artifact.
4. Run `Verify Experience Registry Releases` with read-only packages access
   to prove SHA512, package manifest and compiled exports for every Experience
   package, including deck.gl. Preserve exact run/version/digest.
5. Only then open Thamani consumer integration with exact pinned package
   versions and separate browser/negative acceptance.

No skipped/empty receipt, unverified npm tarball, private workflow approval
bypass, or untrusted public tile endpoint is an acceptable substitute.
