# Baobab Experience Geo deck.gl — BGX-02

**Status: source candidate, not published or production approved.** This optional
Shared presentation package converts a bounded, already-authorised geospatial
projection into a deck.gl ScatterplotLayer, with an explicitly selected evidence
frame and an accessible text equivalent. It does not source, estimate,
interpolate, track, route, optimise, or authorise any position or shipment.

## Runtime boundary

The package itself imports **no WebGL/browser runtime** and is safe to load
from a server module for validation or accessible rows. A client must **opt in**
to mounting an overlay, using its separately installed, exactly pinned
`@deck.gl/layers@9.4.0`, `@deck.gl/maplibre@9.4.0` and approved
`maplibre-gl@6.14.0`. deck.gl is MIT-licensed; transitive licence, security,
bundle and exact-registered versions must be independently checked by the
consumer. The three runtime packages are **consumer-owned** and intentionally absent
from the Shared manifest: pnpm's autoInstallPeers would otherwise install
WebGL code even for model-only consumers. A real opt-in estate adds, pins and
locks these dependencies itself; unused estates download none.

An illustrative, consent-gated caller can wire the official factories:

```ts
import { ScatterplotLayer } from "@deck.gl/layers"
import { MapLibreOverlay } from "@deck.gl/maplibre"
import { createDeckOverlay, toEvidenceRows } from "@baobab-platform/experience-geo-deckgl"

// The caller has already enforced IAM, CP context, TMS object access and
// redaction. 'map' is the authorised MapLibre map, independently configured
// with reviewed style/tile origins, CSP, attribution and optional worker.
const controller = createDeckOverlay({
  map,
  projection: redactedProjection,
  frameAt: selectedExactFrameTimestamp,
  consent: true,
  layerFactory: props => new ScatterplotLayer(props),
  overlayFactory: props => new MapLibreOverlay(props),
})
// On auth revocation, context switch, navigation or consent withdrawal:
controller.dispose()
// Always render toEvidenceRows(projection, selectedFrame) as a keyboard-readable
// alternative, whether WebGL loads or not.
```

The overlay uses `interleaved: false` (no shared graphics context), requires
explicit user consent, and only draws fixed evidence markers. It never
constructs a line between observations or infers a border crossing/ETA.
Unknown positions are excluded from the canvas but remain in the text view.
No layer is pickable and no tooltip reads hidden provider fields.

## Contract and limits

- A projection reference identifies **one BFF-approved snapshot**, not a grant.
- Maximum 100 frames, 2,000 observations in each frame, 20,000 across a
  projection; strict chronological order, unique per-frame identifiers.
- Exact timestamp frame selection only; no auto-advance, interpolation,
  animation, background polling, local persistence or WebSocket connection.
- Estimated positions require model/version/input/generated-at provenance and
  confidence; stale/unknown classifications are caller-supplied, never inferred.
- Changing a projection reference invalidates the overlay controller; caller
  must unmount on revocation or context change. Restricted projections cannot
  mount, and their data must be absent, not visually hidden.

For BGX-03/BGX-04, real IAM/CP/TMS bindings, cross-tenant denial, revocation,
provider certification, lawful sharing/retention, MapLibre style & tile-origin
contracts and protected staging must be independently demonstrated. A passed
synthetic test is neither real tracking nor production authorisation.
