/**
 * Strict RFC 3339 calendar validation for presentation evidence. Date.parse
 * normalises impossible dates (30 February becomes March), which would make
 * an invalid source observation look trustworthy. Preserve valid offsets and
 * precision rather than silently rewriting the caller's evidence timestamp.
 * Leap seconds are rejected: the JavaScript date runtime cannot represent them.
 */
export function assertEvidenceTimestamp(value: unknown): asserts value is string {
  if (typeof value !== "string") throw new TypeError("Expected an ISO timestamp with timezone");
  const parts = /^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})(?:\.\d+)?(Z|([+-])(\d{2}):(\d{2}))$/.exec(value);
  if (!parts) throw new TypeError("Expected an ISO timestamp with timezone");
  const [year, month, day, hour, minute, second] = parts.slice(1, 7).map(Number);
  const leap = year! % 4 === 0 && (year! % 100 !== 0 || year! % 400 === 0);
  const days = [31, leap ? 29 : 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
  if (month! < 1 || month! > 12 || day! < 1 || day! > days[month! - 1]! ||
      hour! > 23 || minute! > 59 || second! > 59 ||
      (parts[7] !== "Z" && (Number(parts[9]) > 23 || Number(parts[10]) > 59)) ||
      !Number.isFinite(Date.parse(value))) {
    throw new TypeError("Expected a valid ISO calendar timestamp with timezone");
  }
}
