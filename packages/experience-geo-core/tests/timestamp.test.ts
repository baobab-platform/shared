import test from "node:test";
import assert from "node:assert/strict";
import { assertEvidenceTimestamp, boundsForPositions, validateLocationObservation } from "../src/index.ts";

test("calendar validation rejects normalised dates and unrepresentable times",()=>{
  for(const value of ["2026-02-30T12:00:00Z","2026-04-31T12:00:00Z","1900-02-29T00:00:00Z",
    "2026-01-01T24:00:00Z","2026-01-01T00:00:60Z","2026-01-01T00:00:00+24:00",
    "2026-01-01T00:00:00+02:60","2026-00-01T00:00:00Z","2026-01-00T00:00:00Z",
    "2026-01-01T00:00:00", "", null, 123]) {
    assert.throws(()=>assertEvidenceTimestamp(value),TypeError,String(value));
  }
});
test("leap days, fractional precision and explicit offsets preserve source evidence",()=>{
  for(const value of ["2000-02-29T00:00:00Z","2024-02-29T23:59:59.123456Z","2026-10-17T17:53:56+02:00"]){
    assert.doesNotThrow(()=>assertEvidenceTimestamp(value));
    assert.equal(validateLocationObservation({kind:"carrier-reported",source:"Synthetic carrier",position:null,observedAt:value}).observedAt,value);
  }
});
test("large coordinate sets and both poles remain bounded without argument spreading",()=>{
  const points=Array.from({length:150_000},()=>[32,0] as const);
  points.push([32,0]);
  assert.deepEqual(boundsForPositions(points),{west:32,east:32,south:0,north:0,crossesAntimeridian:false});
  assert.equal(boundsForPositions([[0,-90],[0,90]])?.south,-90);
});
