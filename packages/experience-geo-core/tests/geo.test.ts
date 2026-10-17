import test from "node:test";
import assert from "node:assert/strict";
import { assertLonLat, boundsForPositions, shortestLongitudeDelta, locationLabel, validateLocationObservation } from "../src/index.ts";
test("rejects malformed and nonfinite coordinates",()=>{
  for(const invalid of [[181,0],[0,91],[NaN,0],[0],[-181,0]])assert.throws(()=>assertLonLat(invalid),RangeError);
  assert.doesNotThrow(()=>assertLonLat([180,90]));
});
test("minimal bounds cross the international date line when appropriate",()=>{
  assert.deepEqual(boundsForPositions([[170,-10],[-175,20],[178,4]]),{
    west:170,east:-175,south:-10,north:20,crossesAntimeridian:true
  });
  assert.equal(shortestLongitudeDelta(170,-175),15);
  assert.equal(boundsForPositions([]),null);
});
test("source attribution remains distinct from estimation and unknown position",()=>{
  const value=validateLocationObservation({
    kind:"estimated",position:[32.5,0.5],source:"model-version-two",
    observedAt:"2026-10-17T09:00:00+02:00",confidence:0.6
  });
  assert.match(locationLabel(value),/Estimated position — not observed/);
  assert.match(locationLabel(value),/model-version-two/);
  assert.match(locationLabel({...value,position:null}),/position unavailable/);
  assert.throws(()=>validateLocationObservation({...value,confidence:1.2}),RangeError);
  assert.throws(()=>validateLocationObservation({...value,source:" "}),TypeError);
  assert.throws(()=>validateLocationObservation({...value,observedAt:"today"}),TypeError);
});
