# Optional evidence map — BGX-02 source increment

React 19 / MapLibre GL JS 6.14 presentation only. No tile vendor is selected.
The caller supplies an already-authorised/redacted projection, exact HTTPS
origin allowlist, reviewed licence reference, attribution and MapLibre style.
No engine SDK, geolocation, routing, ETA, telemetry journal or domain grants.

The renderer loads after explicit activation. Text/list selection remains
complete before activation and on WebGL/network failure. Restricted projections
unmount the renderer; cleanup removes markers, observers, canvas and workers.
All provider requests use dedicated asset origins separate from the application
session and same-origin credential mode, so application cookies are not forwarded.
Same-origin application asset requests and unapproved origins are rejected.
Estimated positions require model/version/generated-at/input provenance.
The 500-marker profile is deliberately bounded; dense analytical overlays need
separate deck.gl qualification. No fake paths connect otherwise unrelated points.

Import optional styles from this package and maplibre-gl/dist/maplibre-gl.css
only in the consuming map entry. Browser CSP must independently approve the
selected worker/style/tile sources. Self-hosted blank synthetic styles are test
fixtures, not production vendor/coverage or legal-border approval.

`./model` is server-import safe. The default entry is a client boundary; do not
put private positions in SSR/HTML merely because a tab or canvas is hidden.

MapLibre 6 requires an explicitly packaged worker asset. Supply `worker.url`
with a same-origin path ending `/maplibre-gl-worker.mjs` and a `worker.version`
matching the SDK. Copy the pinned worker and shared module together. The
application CSP must approve worker execution; tile/style origins remain a
separate cookieless resource boundary. No CDN worker is selected by default.
