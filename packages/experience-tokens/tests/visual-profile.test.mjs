import {test} from "node:test";
import assert from "node:assert/strict";
import {createVisualProfileReport,PAIRS} from "../scripts/visual-profile.mjs";
import {readTokens} from "../scripts/tokens.mjs";

test("all four theme receipts cover every documented text/status/focus pair",()=>{
  const report=createVisualProfileReport();
  assert.equal(report.profile,"BXS-VFA-v1.0");
  assert.equal(report.classification,"SOURCE_OBSERVED_TOKEN_CONTRAST_ONLY");
  assert.equal(report.themes.length,4);
  assert.equal(PAIRS.length,11);
  for(const theme of report.themes){
    assert.equal(theme.brandApproved,false);
    assert.ok(theme.status.length>0);
    assert.equal(theme.pairings.length,PAIRS.length);
    for(const pair of theme.pairings)assert.ok(pair.pass&&pair.ratio>=pair.minimum);
  }
  assert.equal(report.themes.find(x=>x.name==="thamani").status,"legacy-retail-not-approved-for-logistics");
});

test("reported palette remains deterministic and rejects perceptually unsafe changes",()=>{
  assert.deepEqual(createVisualProfileReport(),createVisualProfileReport());
  const loadTheme=name=>{
    const theme=structuredClone(readTokens("themes/"+name+".tokens.json"));
    if(name==="zuribeans")theme.color.primary.$value="#ffffff";
    return theme;
  };
  assert.throws(()=>createVisualProfileReport(readTokens("base.tokens.json"),loadTheme),/Insufficient contrast/);
});

test("no theme report silently upgrades a source-observed theme to approval",()=>{
  const loadTheme=name=>{
    const theme=structuredClone(readTokens("themes/"+name+".tokens.json"));
    if(name==="nabhold")delete theme.$extensions.baobab.status;
    return theme;
  };
  assert.throws(()=>createVisualProfileReport(readTokens("base.tokens.json"),loadTheme),/source approval status missing/);
});
