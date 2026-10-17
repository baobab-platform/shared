# Baobab Geo Core — BXS-03

Versioned, authority-neutral geospatial presentation helpers. Immutable longitude/
latitude tuples, validated coordinate bounds, anti-meridian envelopes, explicit
source classifications and accessible provenance labels. This does NOT implement
a map renderer or domain-owned tracking, ETA, route choice, customs, legal state,
telemetry collection or CP authorisation.

All positions passed to this package must already be authorised and redacted by
the application BFF. Predicted coordinates cannot be presented as observed GPS.

Node 24 and pnpm 11.24.0 are mandatory per baobab-dev. Run:

    pnpm --filter @baobab-platform/experience-geo-core lint
    pnpm --filter @baobab-platform/experience-geo-core test
    pnpm --filter @baobab-platform/experience-geo-core build
