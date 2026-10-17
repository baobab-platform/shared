/**
 * BGX-02 / ADR-SHARED-040: opt-in deck.gl presentation for BFF-authorised,
 * redacted evidence. No WebGL runtime import, IAM/CP provider, movement journal,
 * routing, interpolation or tracking truth is implemented in Shared.
 */
import {
  assertEvidenceTimestamp,
  validateLocationObservation,
  type LocationKind,
  type LocationObservation,
  type LonLat,
} from "@baobab-platform/experience-geo-core";

export type EvidenceFreshness = "current" | "stale" | "unknown";
export type EvidenceEstimate = Readonly<{
  model: string;
  version: string;
  generatedAt: string;
  inputsReference: string;
}>;
export type EvidencePoint = Readonly<{
  id: string;
  label: string;
  evidenceReference: string;
  freshness: EvidenceFreshness;
  observation: LocationObservation;
  estimate?: EvidenceEstimate;
}>;
export type EvidenceFrame = Readonly<{
  at: string;
  points: readonly EvidencePoint[];
}>;
export type EvidenceProjection =
  | Readonly<{ visibility: "restricted"; explanation: string }>
  | Readonly<{
      visibility: "authorised";
      /** Opaque BFF snapshot identifier; must change with context or grant. */
      projectionReference: string;
      sourceReference: string;
      frames: readonly EvidenceFrame[];
    }>;

export type EvidenceRow = Readonly<{
  id: string;
  label: string;
  evidenceReference: string;
  source: string;
  observedAt: string | null;
  freshness: EvidenceFreshness;
  kind: LocationKind;
  location: string;
  estimate: EvidenceEstimate | null;
  confidence: number | null;
}>;

const MAX_FRAMES = 100;
const MAX_POINTS_PER_FRAME = 2_000;
const MAX_TOTAL_POINTS = 20_000;
const FRESHNESS: readonly EvidenceFreshness[] = ["current", "stale", "unknown"];

function required(value: unknown, field: string): asserts value is string {
  if (typeof value !== "string" || !value.trim() || value.length > 256) {
    throw new TypeError(`A bounded, nonempty ${field} is required`);
  }
}
function observationCopy(value: LocationObservation): LocationObservation {
  // validateLocationObservation checks coordinates, date and numeric ranges.
  // Explicitly project the allowlisted fields: transport DTOs can carry
  // arbitrary internal/provider metadata even after structural validation.
  validateLocationObservation(value);
  const position: LonLat | null = value.position === null
    ? null
    : Object.freeze([value.position[0], value.position[1]]) as LonLat;
  return Object.freeze({
    kind: value.kind,
    position,
    source: value.source,
    observedAt: value.observedAt,
    ...(value.accuracyMeters === undefined ? {} : { accuracyMeters: value.accuracyMeters }),
    ...(value.confidence === undefined ? {} : { confidence: value.confidence }),
  });
}

/**
 * One approved projection is a bounded, immutable snapshot. Restricted data
 * must be absent rather than hidden in canvas, text, hit-testing or exports.
 * No source timestamp is silently converted to a "live" status.
 */
export function validateEvidenceProjection(value: EvidenceProjection): EvidenceProjection {
  if (!value || typeof value !== "object") throw new TypeError("Invalid evidence projection");
  if (value.visibility === "restricted") {
    required(value.explanation, "denial explanation");
    if ("frames" in value || "sourceReference" in value || "projectionReference" in value) {
      throw new TypeError("Restricted projection cannot contain private evidence");
    }
    return Object.freeze({ visibility: "restricted", explanation: value.explanation });
  }
  if (value.visibility !== "authorised") throw new TypeError("Unknown projection visibility");
  required(value.projectionReference, "projection reference");
  required(value.sourceReference, "source reference");
  if (!Array.isArray(value.frames) || value.frames.length > MAX_FRAMES) {
    throw new RangeError("Evidence frame limit exceeded");
  }
  let total = 0, previousTime = -Infinity;
  const frames = value.frames.map((frame: EvidenceFrame) => {
    if (!frame || typeof frame !== "object") throw new TypeError("Invalid evidence frame");
    assertEvidenceTimestamp(frame.at);
    const time = Date.parse(frame.at);
    if (time <= previousTime) throw new RangeError("Frames must have strictly increasing times");
    previousTime = time;
    if (!Array.isArray(frame.points) || frame.points.length > MAX_POINTS_PER_FRAME) {
      throw new RangeError("Evidence point limit exceeded");
    }
    total += frame.points.length;
    if (total > MAX_TOTAL_POINTS) throw new RangeError("Evidence projection budget exceeded");
    const ids = new Set<string>();
    const points = frame.points.map((point: EvidencePoint) => {
      if (!point || typeof point !== "object") throw new TypeError("Invalid evidence point");
      required(point.id, "point identifier");
      required(point.label, "point label");
      required(point.evidenceReference, "evidence reference");
      if (ids.has(point.id)) throw new TypeError("Duplicate evidence point identifier");
      ids.add(point.id);
      if (!FRESHNESS.includes(point.freshness)) throw new TypeError("Unknown freshness status");
      const observation = observationCopy(point.observation);
      let estimate: EvidenceEstimate | undefined;
      if (observation.kind === "estimated") {
        if (observation.confidence == null) throw new TypeError("Estimate requires confidence");
        const supplied = point.estimate;
        if (!supplied) throw new TypeError("Estimate requires model provenance");
        required(supplied.model, "estimate model");
        required(supplied.version, "estimate version");
        required(supplied.inputsReference, "estimate input reference");
        assertEvidenceTimestamp(supplied.generatedAt);
        estimate = Object.freeze({
          model: supplied.model, version: supplied.version,
          inputsReference: supplied.inputsReference, generatedAt: supplied.generatedAt,
        });
      } else if (point.estimate !== undefined) {
        throw new TypeError("Non-estimated evidence cannot carry estimate metadata");
      }
      return Object.freeze({
        id: point.id, label: point.label, evidenceReference: point.evidenceReference,
        freshness: point.freshness, observation,
        ...(estimate ? { estimate } : {}),
      });
    });
    return Object.freeze({ at: frame.at, points: Object.freeze(points) });
  });
  return Object.freeze({
    visibility: "authorised",
    projectionReference: value.projectionReference,
    sourceReference: value.sourceReference,
    frames: Object.freeze(frames),
  });
}

/** Select ONLY a frame with this exact source timestamp; never interpolate. */
export function evidenceFrameAt(projection: EvidenceProjection, timestamp: string): EvidenceFrame | null {
  const validated = validateEvidenceProjection(projection);
  if (validated.visibility === "restricted") return null;
  assertEvidenceTimestamp(timestamp);
  return validated.frames.find(frame => frame.at === timestamp) ?? null;
}

/** Text/table alternative is complete even when WebGL is missing or disabled. */
export function toEvidenceRows(projection: EvidenceProjection, frameAt: string): readonly EvidenceRow[] {
  const frame = evidenceFrameAt(projection, frameAt);
  if (!frame) return Object.freeze([]);
  return Object.freeze(frame.points.map(point => {
    const o = point.observation;
    return Object.freeze({
      id: point.id, label: point.label, evidenceReference: point.evidenceReference,
      source: o.source, observedAt: o.observedAt, freshness: point.freshness, kind: o.kind,
      location: o.position === null
        ? "Position unavailable"
        : `Longitude ${o.position[0]}, latitude ${o.position[1]}`,
      estimate: point.estimate ?? null, confidence: o.confidence ?? null,
    });
  }));
}

/** Only complete, authorised positions reach the canvas. No fabricated path. */
export type DeckMarker = Readonly<{
  id: string; position: LonLat; kind: LocationKind; freshness: EvidenceFreshness;
}>;
export type ScatterplotContract = Readonly<{
  id: string;
  data: readonly DeckMarker[];
  getPosition: (point: DeckMarker) => LonLat;
  getFillColor: (point: DeckMarker) => readonly [number, number, number, number];
  getRadius: (point: DeckMarker) => number;
  radiusUnits: "pixels";
  radiusMinPixels: number;
  radiusMaxPixels: number;
  pickable: false;
  autoHighlight: false;
}>;

function markerColor(point: DeckMarker): readonly [number, number, number, number] {
  // Colour is a secondary cue; toEvidenceRows exposes explicit status text.
  if (point.freshness !== "current") return [111, 121, 130, 130];
  switch (point.kind) {
    case "observed-gps": return [15, 124, 92, 220];
    case "carrier-reported": return [44, 100, 180, 220];
    case "milestone-derived": return [175, 110, 20, 210];
    case "estimated": return [120, 84, 155, 190];
  }
}
export function scatterplotForFrame(frame: EvidenceFrame): ScatterplotContract {
  // Validation remains mandatory even for directly supplied frames.
  const validated = validateEvidenceProjection({
    visibility: "authorised", projectionReference: "frame-only",
    sourceReference: "frame-only", frames: [frame],
  });
  if (validated.visibility !== "authorised") throw new TypeError("Frame denied");
  const points = validated.frames[0]!.points.filter(p => p.observation.position !== null)
    .map(p => Object.freeze({
      id: p.id, position: p.observation.position as LonLat,
      kind: p.observation.kind, freshness: p.freshness,
    }));
  return Object.freeze({
    id: "bxs-authorised-evidence",
    data: Object.freeze(points),
    getPosition: (p: DeckMarker) => p.position,
    getFillColor: markerColor,
    getRadius: (_p: DeckMarker) => 5,
    radiusUnits: "pixels",
    radiusMinPixels: 5,
    radiusMaxPixels: 5,
    pickable: false,
    autoHighlight: false,
  });
}

export type OverlayControl<L> = {
  setProps(props: { layers: readonly L[] }): void;
};
export type MapControlPort<C> = {
  addControl(control: C): unknown;
  removeControl(control: C): unknown;
};
export type DeckOverlayOptions<L, C extends OverlayControl<L>> = Readonly<{
  /** Consent is a deliberate user action, never a default. */
  consent: true;
  map: MapControlPort<C>;
  projection: EvidenceProjection;
  frameAt: string;
  layerFactory(props: ScatterplotContract): L;
  overlayFactory(props: { interleaved: false; layers: readonly L[] }): C;
}>;

/**
 * The consuming app owns dynamic imports for its approved deck.gl runtime,
 * MapLibre map, CSP, tile origin policy and worker. No automatic imports,
 * network access, polling or location service occur inside this package.
 *
 * Always call dispose() when the user revokes consent or IAM/CP context
 * changes. A different projectionReference cannot reuse an old controller.
 */
export function createDeckOverlay<L, C extends OverlayControl<L>>(
  options: DeckOverlayOptions<L, C>,
): Readonly<{
  selectFrameAt(timestamp: string): boolean;
  dispose(): void;
}> {
  if (options.consent !== true) throw new TypeError("Interactive overlay requires consent");
  const validated = validateEvidenceProjection(options.projection);
  if (validated.visibility !== "authorised") throw new TypeError("Restricted overlay");
  const initial = validated.frames.find(frame => frame.at === options.frameAt);
  if (!initial) throw new RangeError("Requested evidence frame unavailable");
  let active = true;
  const overlay = options.overlayFactory({
    interleaved: false, layers: [options.layerFactory(scatterplotForFrame(initial))],
  });
  options.map.addControl(overlay);
  return Object.freeze({
    selectFrameAt(timestamp: string): boolean {
      if (!active) return false;
      assertEvidenceTimestamp(timestamp);
      const frame = validated.frames.find(item => item.at === timestamp);
      if (!frame) {
        // Clearing is safer than retaining stale data at an unknown time.
        overlay.setProps({ layers: [] });
        return false;
      }
      overlay.setProps({ layers: [options.layerFactory(scatterplotForFrame(frame))] });
      return true;
    },
    dispose(): void {
      if (!active) return;
      active = false;
      overlay.setProps({ layers: [] });
      options.map.removeControl(overlay);
    },
  });
}
