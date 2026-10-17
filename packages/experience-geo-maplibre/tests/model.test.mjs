import test from "node:test";
import assert from "node:assert/strict";
import {validatePoints,validateResourcePolicy,approvedResourceUrl} from "../dist/model.js";
const policy={allowedOrigins:["https://maps.example.test"],attribution:"Synthetic blank style",licenceReference:"Internal synthetic fixture; no provider selected"};
const point={id:"one",label:"Reported hand-off",evidenceReference:"synthetic:one",freshness:"stale",observation:{kind:"carrier-reported",position:[32,0],source:"Synthetic carrier",observedAt:"2026-10-17T10:00:00Z"}};
test("rejects foreign origins, cookies-in-URL, schemes and donation tile hosts",()=>{
  assert.doesNotThrow(()=>validateResourcePolicy(policy));
  assert.equal(approvedResourceUrl("https://maps.example.test/style.json",policy),"https://maps.example.test/style.json");
  for(const url of ["https://foreign.test/tiles","https://user:password@maps.example.test/x","javascript:alert(1)","file:///private"]){assert.throws(()=>approvedResourceUrl(url,policy));}
  assert.throws(()=>validateResourcePolicy({...policy,allowedOrigins:["https://tile.openstreetmap.org"]}));
  assert.throws(()=>validateResourcePolicy({...policy,licenceReference:""}));
  assert.throws(()=>approvedResourceUrl("https://maps.example.test/private",policy,"https://maps.example.test"));
});
test("rejects invalid or duplicate evidence and unproven estimates",()=>{
  assert.doesNotThrow(()=>validatePoints([point]));
  assert.throws(()=>validatePoints([point,point]));
  assert.throws(()=>validatePoints([{...point,freshness:"live"}]));
  assert.throws(()=>validatePoints([{...point,observation:{...point.observation,kind:"estimated"}}]));
  assert.throws(()=>validatePoints([{...point,observation:{...point.observation,observedAt:"2026-02-30T12:00:00Z"}}]));
  assert.doesNotThrow(()=>validatePoints([{...point,observation:{...point.observation,kind:"estimated",confidence:0.5},estimate:{model:"Synthetic model",version:"1",generatedAt:"2026-10-17T10:00:00Z",inputsReference:"synthetic:inputs"}}]));
});
