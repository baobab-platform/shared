import test from "node:test";
import assert from "node:assert/strict";
import {
  toAccessibleChartTable,
  validateChartSeries,
  type ChartSeriesProjection,
} from "../src/index.ts";

const example: ChartSeriesProjection = {
  title: "Synthetic portfolio values",
  valueLabel: "Reported amount",
  unitLabel: "ZAR",
  availability: "available",
  sourceReference: "fixture:already-authorised:synthetic",
  asOf: "2026-10-17T12:00:00+02:00",
  points: [
    { id: "a", label: "Alpha", value: 0 },
    { id: "b", label: "Beta", value: -10.5 },
    { id: "c", label: "No authorised value", value: null },
  ],
};

test("preserves reported zero, negative values and explicit absence without aggregation", () => {
  const rows = toAccessibleChartTable(example);
  assert.equal(rows.availability, "available");
  assert.equal(rows.unitLabel, "ZAR");
  assert.equal(rows.sourceReference, example.sourceReference);
  assert.equal(rows.asOf, example.asOf);
  assert.deepEqual(rows.rows.map((row) => row.displayValue), ["0", "-10.5", "Not reported"]);
  assert.deepEqual(rows.rows.map((row) => row.value), [0, -10.5, null]);
  assert.equal(rows.message, null);
});

test("a stale source is labelled as stale, never live or current", () => {
  const table = toAccessibleChartTable({ ...example, availability: "stale" });
  assert.match(table.message!, /Stale reporting data — not live/);
  assert.equal(table.asOf, example.asOf);
});

test("restricted and unavailable states cannot accidentally expose records or provenance", () => {
  for (const availability of ["restricted", "unavailable"] as const) {
    const empty = {
      ...example, availability, points: [], sourceReference: null, asOf: null,
    };
    const result = toAccessibleChartTable(empty);
    assert.equal(result.rows.length, 0);
    assert.match(result.message!, availability === "restricted" ? /restricted/ : /unavailable/);
    assert.throws(() => validateChartSeries({ ...empty, points: example.points }), TypeError);
    assert.throws(() => validateChartSeries({ ...empty, sourceReference: "private-ref" }), TypeError);
  }
});

test("rejects transport-corrupted IDs, values, statuses and timestamps", () => {
  assert.throws(() => validateChartSeries({ ...example, sourceReference: "  " }), TypeError);
  assert.throws(() => validateChartSeries({ ...example, asOf: "2026-02-30T12:00:00Z" }), TypeError);
  assert.throws(() => validateChartSeries({
    ...example, availability: "certified" as ChartSeriesProjection["availability"],
  }), TypeError);
  assert.throws(() => validateChartSeries({
    ...example, points: [{ id: "a", label: "First", value: 1 }, { id: "a", label: "Second", value: 2 }],
  }), TypeError);
  for (const value of [Number.NaN, Infinity, -Infinity]) {
    assert.throws(() => validateChartSeries({
      ...example, points: [{ id: "finite", label: "Test", value }],
    }), RangeError);
  }
  assert.throws(() => validateChartSeries({
    ...example, points: Array.from({ length: 2001 }, (_, index) => ({
      id: String(index), label: "Sample", value: 1,
    })),
  }), RangeError);
});

test("unrecognised provider properties never survive the display projection", () => {
  const polluted = {
    ...example,
    privateProviderCredential: "not-for-browser",
    points: [{ ...example.points[0], hiddenLegalActor: "internal" }],
  };
  const safe = validateChartSeries(polluted);
  assert.equal(Object.hasOwn(safe, "privateProviderCredential"), false);
  assert.equal(Object.hasOwn(safe.points[0]!, "hiddenLegalActor"), false);
  const table = toAccessibleChartTable(polluted);
  assert.equal(Object.hasOwn(table, "privateProviderCredential"), false);
});

test("validated projections and accessible rows are immutable defensive copies", () => {
  const original = example.points.map((point) => ({ ...point }));
  const source = { ...example, points: original };
  const validated = validateChartSeries(source);
  source.points[0]!.value = 999;
  assert.equal(validated.points[0]!.value, 0);
  assert.ok(Object.isFrozen(validated));
  assert.ok(Object.isFrozen(validated.points));
  assert.ok(Object.isFrozen(validated.points[0]));
  const table = toAccessibleChartTable(validated);
  assert.ok(Object.isFrozen(table));
  assert.ok(Object.isFrozen(table.rows));
  assert.ok(Object.isFrozen(table.rows[0]));
});
