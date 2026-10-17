import test from "node:test";
import assert from "node:assert/strict";
import {
  createDeckOverlay, evidenceFrameAt, scatterplotForFrame,
  toEvidenceRows, validateEvidenceProjection, type EvidenceProjection,
} from "../src/index.ts";

const gps = {
  id: "a", label: "Synthetic reported location",
  evidenceReference: "fixture:observation:1", freshness: "stale" as const,
  observation: {
    kind: "carrier-reported" as const, position: [179, -1] as const,
    source: "Synthetic carrier", observedAt: "2026-10-17T10:00:00Z",
    accuracyMeters: 120,
  },
};
const missing = {
  id: "b", label: "Synthetic unknown",
  evidenceReference: "fixture:observation:2", freshness: "unknown" as const,
  observation: {
    kind: "milestone-derived" as const, position: null, source: "Synthetic event",
    observedAt: null,
  },
};
const projection: EvidenceProjection = {
  visibility: "authorised",
  projectionReference: "opaque:authorised:revision-01",
  sourceReference: "fixture:synthetic-projection",
  frames: [
    { at: "2026-10-17T10:00:00Z", points: [gps, missing] },
    { at: "2026-10-17T11:00:00Z", points: [
      { ...gps, observation: { ...gps.observation, position: [-179, -1] as const } },
    ] },
  ],
};

test("only approved data fields survive validation; stale and absent positions remain distinguishable", () => {
  const unsafe = {
    ...projection,
    secretApiKey: "never-for-browser",
    frames: [{
      at: "2026-10-17T10:00:00Z",
      points: [{
        ...gps, hiddenLegalActor: "private-legal-id",
        observation: { ...gps.observation, privateToken: "private" },
      }, missing],
    }],
  };
  const safe = validateEvidenceProjection(unsafe);
  assert.equal(safe.visibility, "authorised");
  assert.equal(Object.hasOwn(safe, "secretApiKey"), false);
  if (safe.visibility === "authorised") {
    assert.equal(Object.hasOwn(safe.frames[0]!.points[0]!, "hiddenLegalActor"), false);
    assert.equal(Object.hasOwn(safe.frames[0]!.points[0]!.observation, "privateToken"), false);
    assert.ok(Object.isFrozen(safe.frames[0]!.points[0]!.observation.position));
  }
  const rows = toEvidenceRows(projection, "2026-10-17T10:00:00Z");
  assert.equal(rows.length, 2);
  assert.equal(rows[0]!.freshness, "stale");
  assert.equal(rows[1]!.location, "Position unavailable");
  assert.match(rows[0]!.location, /Longitude 179/);
});

test("restricted data stays absent and cannot create WebGL controls", () => {
  const restricted = { visibility: "restricted" as const, explanation: "No capability" };
  assert.equal(toEvidenceRows(restricted, "2026-10-17T10:00:00Z").length, 0);
  assert.throws(() => validateEvidenceProjection({
    ...restricted, frames: [projection.visibility === "authorised" ? projection.frames[0] : []],
  } as unknown as EvidenceProjection), /cannot contain/);
  assert.throws(() => createDeckOverlay({
    consent: true, projection: restricted, frameAt: "2026-10-17T10:00:00Z",
    map: { addControl() {}, removeControl() {} },
    layerFactory: props => props, overlayFactory: _ => ({ setProps() {} }),
  }), /Restricted overlay/);
});

test("timestamps are exact, chronological and never interpolated or converted to live", () => {
  assert.equal(evidenceFrameAt(projection, "2026-10-17T10:30:00Z"), null);
  assert.equal(evidenceFrameAt(projection, "2026-10-17T10:00:00Z")?.at, "2026-10-17T10:00:00Z");
  assert.throws(() => validateEvidenceProjection({
    ...projection, frames: [
      { at: "2026-10-17T11:00:00Z", points: [gps] },
      { at: "2026-10-17T10:00:00Z", points: [gps] },
    ],
  }), /strictly increasing/);
  assert.throws(() => validateEvidenceProjection({
    ...projection, frames: [{ at: "2026-02-30T10:00:00Z", points: [] }],
  }), TypeError);
  assert.throws(() => validateEvidenceProjection({
    ...projection, frames: [{ at: "2026-10-17T10:00:00Z", points: [gps, gps] }],
  }), /Duplicate evidence/);
});

test("sub-millisecond source instants retain ordering across offsets and duplicate precision", () => {
  const permitted = {
    ...projection,
    frames: [
      { at: "2026-10-17T12:00:00.0001+02:00", points: [gps] },
      { at: "2026-10-17T10:00:00.0002Z", points: [gps] },
      { at: "2026-10-17T10:00:00.001Z", points: [gps] },
    ],
  };
  assert.doesNotThrow(() => validateEvidenceProjection(permitted));
  assert.throws(() => validateEvidenceProjection({
    ...permitted,
    frames: [
      { at: "2026-10-17T10:00:00.100Z", points: [] },
      { at: "2026-10-17T12:00:00.10+02:00", points: [] },
    ],
  }), /strictly increasing/);
  assert.throws(() => validateEvidenceProjection({
    ...permitted,
    frames: [
      { at: "2026-10-17T10:00:00.0002Z", points: [] },
      { at: "2026-10-17T10:00:00.0001Z", points: [] },
    ],
  }), /strictly increasing/);
});

test("estimated points require independent model provenance and confidence", () => {
  const estimated = {
    ...gps, observation: {
      kind: "estimated" as const, position: [33, 0] as const, source: "Synthetic model",
      observedAt: "2026-10-17T10:00:00Z", confidence: 0.45,
    },
  };
  assert.throws(() => validateEvidenceProjection({
    ...projection, frames: [{ at: "2026-10-17T10:00:00Z", points: [estimated] }],
  }), /model provenance/);
  assert.doesNotThrow(() => validateEvidenceProjection({
    ...projection, frames: [{
      at: "2026-10-17T10:00:00Z", points: [{
        ...estimated, estimate: {
          model: "Synthetic predictor", version: "1",
          inputsReference: "fixture:inputs", generatedAt: "2026-10-17T09:00:00Z",
        },
      }],
    }],
  }));
  assert.throws(() => validateEvidenceProjection({
    ...projection, frames: [{
      at: "2026-10-17T10:00:00Z", points: [{
        ...estimated, estimate: {
          model: "Synthetic", version: "1",
          inputsReference: "synthetic", generatedAt: "2026-02-30T12:00:00Z",
        },
      }],
    }],
  }), TypeError);
});

test("explicit point and frame limits fail without fallback or truncation", () => {
  assert.throws(() => validateEvidenceProjection({
    ...projection, frames: [{
      at: "2026-10-17T10:00:00Z",
      points: Array.from({ length: 2001 }, (_, i) => ({ ...gps, id: String(i) })),
    }],
  }), /point limit/);
  assert.throws(() => validateEvidenceProjection({
    ...projection, frames: Array.from({ length: 101 }, (_, i) => ({
      at: new Date(Date.parse("2026-10-17T10:00:00Z") + i * 60000).toISOString(),
      points: [],
    })),
  }), /frame limit/);
  assert.throws(() => validateEvidenceProjection({
    ...projection, frames: Array.from({ length: 11 }, (_, i) => ({
      at: new Date(Date.parse("2026-10-17T10:00:00Z") + i * 60000).toISOString(),
      points: Array.from({ length: 2000 }, (_, j) => ({ ...gps, id: String(j) })),
    })),
  }), /budget exceeded/);
});

test("markers have no hit-testing, animated location interpolation, or invented path", () => {
  if (projection.visibility !== "authorised") throw Error("Fixture changed");
  const spec = scatterplotForFrame(projection.frames[0]!);
  assert.equal(spec.data.length, 1); // unknown position only appears in text
  assert.equal(spec.pickable, false);
  assert.equal(spec.autoHighlight, false);
  assert.equal(spec.radiusUnits, "pixels");
  assert.deepEqual(spec.getPosition(spec.data[0]!), [179, -1]);
  assert.equal(Object.hasOwn(spec, "getPath"), false);
  assert.equal(Object.hasOwn(spec, "transitions"), false);
});

test("consent activation, exact frame update and cleanup never outlive the map", () => {
  const events: string[] = [];
  const layers: unknown[][] = [];
  const control = {
    setProps: ({ layers: next }: { layers: readonly unknown[] }) => {
      events.push("update");
      layers.push([...next]);
    },
  };
  const controller = createDeckOverlay({
    projection, consent: true, frameAt: "2026-10-17T10:00:00Z",
    map: { addControl: c => { assert.equal(c, control); events.push("add"); },
      removeControl: c => { assert.equal(c, control); events.push("remove"); } },
    layerFactory: props => ({ ...props }),
    overlayFactory: opts => {
      assert.equal(opts.interleaved, false);
      assert.equal(opts.layers.length, 1);
      return control;
    },
  });
  assert.equal(controller.selectFrameAt("2026-10-17T11:00:00Z"), true);
  assert.equal(controller.selectFrameAt("2026-10-17T10:30:00Z"), false);
  assert.deepEqual(layers.at(-1), []);
  controller.dispose();
  controller.dispose(); // idempotent on repeat revocation/navigation
  assert.equal(controller.selectFrameAt("2026-10-17T10:00:00Z"), false);
  assert.deepEqual(events, ["add", "update", "update", "update", "remove"]);
});
