import {test} from "node:test";
import assert from "node:assert/strict";
import {compileBase,compileTheme,contrast,readTokens,themeNames,validateTheme} from "../scripts/tokens.mjs";
const base=readTokens("base.tokens.json");
test("source palettes generate deterministic CSS with namespaced tokens",()=>{
  assert.equal(themeNames.length,4);
  assert.match(compileBase(base),/--bx-space-1: 4px/);
  for(const name of themeNames){
    const theme=readTokens("themes/"+name+".tokens.json");
    const css=compileTheme(base,theme,name);
    assert.equal(css,compileTheme(base,theme,name));
    assert.match(css,/--bx-color-primary:/);
  }
});
test("unsafe and unknown CSS token values fail closed",()=>{
  const theme=structuredClone(readTokens("themes/nabhold.tokens.json"));
  theme.color.primary.$value="#fca300;url(evil)";
  assert.throws(()=>validateTheme(base,theme),/Invalid colour/);
  theme.color.primary.$value="#fca300";
  theme.color.customTenantGrant={$type:"color",$value:"#000000"};
  assert.throws(()=>validateTheme(base,theme),/Unknown semantic theme alias/);
});
test("contrast validates mandated text colour pairs",()=>{
  assert.ok(contrast("#000000","#ffffff")>20);
  const theme=structuredClone(readTokens("themes/zuribeans.tokens.json"));
  theme.color.foreground.$value="#aaaaaa";
  assert.throws(()=>validateTheme(base,theme),/Insufficient contrast/);
});
