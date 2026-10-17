/**
 * ADR-SHARED-040: neutral chart evidence for an already authorised view.
 *
 * This module does not aggregate finance, derive KPIs, determine stale-data
 * policy or grant access to an Organisation/Tenant. The owning server/BFF
 * must produce a redacted projection from the authoritative capability.
 */
import { assertEvidenceTimestamp } from "@baobab-platform/experience-geo-core";

export type ChartAvailability = "available" | "stale" | "unavailable" | "restricted";

export type ChartPoint = Readonly<{
  /** Stable caller-supplied row identifier, not an entity permission. */
  id: string;
  label: string;
  /** Null means no publishable value. In particular it MUST NOT become zero. */
  value: number | null;
}>;

export type ChartSeriesProjection = Readonly<{
  title: string;
  valueLabel: string;
  unitLabel: string;
  /** Classification supplied by the authorised domain/BFF, not inferred here. */
  availability: ChartAvailability;
  /** Source and as-of timestamp are mandatory for publishable values. */
  sourceReference: string | null;
  asOf: string | null;
  points: readonly ChartPoint[];
}>;

export type ChartTableRow = Readonly<{
  id: string;
  label: string;
  value: number | null;
  /** A semantic fallback; never a guessed, rounded or formatted aggregate. */
  displayValue: string;
}>;

export type AccessibleChartTable = Readonly<{
  caption: string;
  labelColumn: string;
  valueColumn: string;
  unitLabel: string;
  availability: ChartAvailability;
  sourceReference: string | null;
  asOf: string | null;
  /** Restricted/unavailable projections have no transmitted data rows. */
  rows: readonly ChartTableRow[];
  message: string | null;
}>;

const AVAILABILITY: readonly ChartAvailability[] = [
  "available",
  "stale",
  "unavailable",
  "restricted",
];

function requireLabel(value: unknown, field: string): asserts value is string {
  if (typeof value !== "string" || !value.trim()) {
    throw new TypeError(`A nonempty ${field} is required`);
  }
}

/**
 * Runtime validation is required even with TypeScript because transport JSON
 * may contain unknown status values, NaN/Infinity or missing provenance.
 * Return defensive immutable copies: a caller cannot mutate an already
 * validated display projection after checking it.
 */
export function validateChartSeries(input: ChartSeriesProjection): ChartSeriesProjection {
  if (typeof input !== "object" || input === null) {
    throw new TypeError("A chart projection object is required");
  }
  requireLabel(input.title, "chart title");
  requireLabel(input.valueLabel, "value label");
  requireLabel(input.unitLabel, "unit label");
  if (!AVAILABILITY.includes(input.availability)) {
    throw new TypeError("Unknown chart availability");
  }
  if (!Array.isArray(input.points)) {
    throw new TypeError("Chart points must be an array");
  }
  // This is a bounded presentation profile, not a high-volume analytics API.
  if (input.points.length > 2_000) {
    throw new RangeError("Chart presentation supports at most 2000 points");
  }

  if (input.availability === "available" || input.availability === "stale") {
    requireLabel(input.sourceReference, "source reference");
    requireLabel(input.asOf, "as-of timestamp");
    assertEvidenceTimestamp(input.asOf);
  } else {
    // No restricted projection should accidentally carry source identifiers or
    // rows that a visually hidden chart could expose through the DOM/exports.
    if (input.points.length !== 0 || input.sourceReference !== null || input.asOf !== null) {
      throw new TypeError("Restricted or unavailable charts must not carry data");
    }
  }

  const ids = new Set<string>();
  const points = input.points.map((point) => {
    if (typeof point !== "object" || point === null) {
      throw new TypeError("Chart point must be an object");
    }
    requireLabel(point.id, "point ID");
    requireLabel(point.label, "point label");
    if (ids.has(point.id)) throw new TypeError("Duplicate chart point ID");
    ids.add(point.id);
    if (point.value !== null &&
      (typeof point.value !== "number" || !Number.isFinite(point.value))) {
      throw new RangeError("Chart values must be finite numbers or explicit null");
    }
    return Object.freeze({ id: point.id, label: point.label, value: point.value });
  });

  // Never copy unknown transport properties. A payload can carry privileged
  // provider data even when its known display fields are valid; an explicit
  // allowlist prevents these accidental extras reaching browser composition.
  return Object.freeze({
    title: input.title,
    valueLabel: input.valueLabel,
    unitLabel: input.unitLabel,
    availability: input.availability,
    sourceReference: input.sourceReference,
    asOf: input.asOf,
    points: Object.freeze(points),
  });
}

/**
 * Produce complete text/table fallback data without HTML or charting library
 * dependencies. The consumer decides markup and styles; it must render the
 * source and as-of fields alongside the rows. No summation or conversion occurs.
 */
export function toAccessibleChartTable(input: ChartSeriesProjection): AccessibleChartTable {
  const projection = validateChartSeries(input);
  const message =
    projection.availability === "restricted" ? "Chart data restricted" :
    projection.availability === "unavailable" ? "Chart data unavailable" :
    projection.availability === "stale" ? "Stale reporting data — not live" : null;
  const rows = projection.points.map((point) =>
    Object.freeze({
      id: point.id,
      label: point.label,
      value: point.value,
      displayValue: point.value === null ? "Not reported" : String(point.value),
    }),
  );
  return Object.freeze({
    caption: projection.title,
    labelColumn: "Category",
    valueColumn: projection.valueLabel,
    unitLabel: projection.unitLabel,
    availability: projection.availability,
    sourceReference: projection.sourceReference,
    asOf: projection.asOf,
    rows: Object.freeze(rows),
    message,
  });
}
