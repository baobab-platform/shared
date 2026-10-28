import test from "node:test";
import assert from "node:assert/strict";
import {readFileSync} from "node:fs";
const proposal=JSON.parse(readFileSync("proposals/tms-native-execution/v1/decision.schema.json","utf8"));
test("TMS proposal requires legal/tenant, exact intent and fencing, no extensible extra fields",()=>{
 assert.equal(proposal.additionalProperties,false);
 for(const key of ["tenant_id","operating_organisation_id","legal_entity_id","market_id","principal_id","capability_binding_revision","native_provider_kind","intent_digest","fencing_generation","expires_at"]){assert(proposal.required.includes(key),key)}
 assert(proposal.$id.includes("/proposals/"));assert.deepEqual(proposal.properties.decision.enum,["ALLOW","DENY"]);
});
test("proposed scope never claims accepted or executable",()=>{
 const text=readFileSync("docs/architecture/proposals/tms-native-execution-authority-v1.md","utf8");
 assert(text.includes("PROPOSED / NOT ACCEPTED"));assert(text.includes("remain HELD"));
});
