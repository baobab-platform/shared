import {test} from "node:test";
import assert from "node:assert/strict";
import {compileBase,compileTheme,contrast,readTokens,themeNames,validateTheme,flattenTokens} from "../scripts/tokens.mjs";
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

test("brand themes can be scoped to independent component workbench subtrees",()=>{
  const css=compileTheme(base,readTokens("themes/nabhold.tokens.json"),"nabhold");
  assert.match(css,/\[data-bx-theme="nabhold"\]\s*\{/);
});

test("complete foundation vocabulary rejects injected fonts, shadows and nonfinite values",()=>{
  const css=compileBase(base);
  for(const group of ["font-sans","type-size-3","layout-reading","layer-dialog","focus-width","motion-standard","elevation-overlay","map-route-width","color-on-warning"])assert.ok(css.includes("--bx-"+group+":"),group);
  for(const token of [{$type:"fontFamily",$value:["Arial;url(evil)"]},{$type:"number",$value:Infinity},
    {$type:"cubicBezier",$value:[2,0,0,1]},{$type:"shadow",$value:{color:"url(evil)"}}]){
    assert.throws(()=>flattenTokens({unsafe:token}));
  }
});
test("semantic contrast is enforced on surfaces and all status pairs",()=>{
  const theme=structuredClone(readTokens("themes/nabhold.tokens.json"));
  theme.color.warning={$type:"color",$value:"#ffffff"};
  assert.throws(()=>validateTheme(base,theme),/onWarning\/warning/);
  delete theme.color.warning;
  delete theme.color.focus;
  assert.throws(()=>validateTheme(base,theme),/Missing theme colour/);
});
