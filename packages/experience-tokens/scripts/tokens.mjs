/**
 * ADR-SHARED-040: deterministic DTCG-to-CSS compilation, no provider SDK.
 * Invalid values fail closed to prevent injection into generated CSS.
 */
import { readFileSync } from "node:fs";
const root = new URL("../tokens/", import.meta.url);
export const themeNames = Object.freeze(["nabhold", "zuribeans", "thamani", "baobab-platform"]);
const required = ["canvas","foreground","surface","mutedText","primary","onPrimary","focus","border"];
/** Small closed vocabulary: source tokens are data, never arbitrary CSS. */
function dimension(v) {
  if (!v || typeof v.value !== "number" || !Number.isFinite(v.value) || v.value < 0 || v.unit !== "px") throw Error("Invalid dimension");
  return String(v.value)+"px";
}
export function readTokens(path) { return JSON.parse(readFileSync(new URL(path, root), "utf8")); }
export function flattenTokens(tree) {
  const result = new Map();
  const visit = (node, path) => {
    for (const [key, value] of Object.entries(node)) {
      if (key.startsWith("$")) continue;
      if (!/^(?:[A-Za-z][A-Za-z0-9]*|[1-9][0-9]*)$/.test(key)) throw Error("Invalid token key: " + key);
      const parts = [...path, key];
      if (value && typeof value === "object" && "$value" in value) {
        let css;
        if (value.$type === "color") {
          if (typeof value.$value !== "string" || !/^#[0-9a-fA-F]{6}$/.test(value.$value)) throw Error("Invalid colour: " + parts.join("."));
          css = value.$value.toLowerCase();
        } else if (value.$type === "dimension" || value.$type === "duration") {
          const v = value.$value;
          if (!v || typeof v.value !== "number" || !Number.isFinite(v.value) || v.value < 0 || v.unit !== (value.$type==="duration"?"ms":"px")) throw Error("Invalid dimension: "+parts.join("."));
          css = String(v.value)+v.unit;
        } else if (value.$type === "number") {
          if (typeof value.$value !== "number" || !Number.isFinite(value.$value) || value.$value < 0 || value.$value > 1e6) throw Error("Invalid number");
          css = String(value.$value);
        } else if (value.$type === "fontFamily") {
          const fonts=value.$value;
          if (!Array.isArray(fonts) || !fonts.length || fonts.some(f=>typeof f!=="string" || !/^[A-Za-z][A-Za-z -]*$/.test(f))) throw Error("Invalid font family");
          css=fonts.map(f=>["serif","sans-serif","monospace","system-ui"].includes(f)?f:JSON.stringify(f)).join(", ");
        } else if (value.$type === "cubicBezier") {
          const curve=value.$value;
          if (!Array.isArray(curve) || curve.length!==4 || curve.some(v=>typeof v!=="number" || !Number.isFinite(v)) || curve[0]<0 || curve[0]>1 || curve[2]<0 || curve[2]>1) throw Error("Invalid easing");
          css="cubic-bezier("+curve.join(", ")+")";
        } else if (value.$type === "shadow") {
          const shadow=value.$value;
          if (!shadow || typeof shadow.color!=="string" || !/^#[0-9a-fA-F]{8}$/.test(shadow.color)) throw Error("Invalid shadow colour");
          css=[shadow.offsetX,shadow.offsetY,shadow.blur,shadow.spread].map(dimension).join(" ")+" "+shadow.color.toLowerCase();
        } else { throw Error("Unknown type: " + parts.join(".")); }
        const name = "--bx-" + parts.map(s => s.replace(/[A-Z]/g,c=>"-"+c.toLowerCase())).join("-");
        if (result.has(name)) throw Error("Duplicate: " + name);
        result.set(name, css);
      } else if (value && typeof value === "object" && !Array.isArray(value)) visit(value, parts);
      else throw Error("Malformed token: " + parts.join("."));
    }
  };
  visit(tree,[]);
  return result;
}
function luminance(hex) {
  const c = [1,3,5].map(i => parseInt(hex.slice(i,i+2),16)/255);
  const a = c.map(v => v<=0.04045?v/12.92:Math.pow((v+0.055)/1.055,2.4));
  return a[0]*0.2126+a[1]*0.7152+a[2]*0.0722;
}
export function contrast(a,b) {
  const x = [luminance(a),luminance(b)].sort((a,b)=>b-a);
  return (x[0]+0.05)/(x[1]+0.05);
}
export function validateTheme(base,theme) {
  const source=flattenTokens(base), colors=flattenTokens(theme);
  const aliases=new Set([...source.keys()].filter(x=>x.startsWith("--bx-color-")));
  for(const key of colors.keys())if(!aliases.has(key))throw Error("Unknown semantic theme alias: "+key);
  const color=k=>{
    const name="--bx-color-"+k.replace(/[A-Z]/g,c=>"-"+c.toLowerCase());
    if(!colors.has(name)&&!source.has(name))throw Error("Missing theme colour: "+k);
    return colors.get(name)??source.get(name);
  };
  for(const k of required){
    const name="--bx-color-"+k.replace(/[A-Z]/g,c=>"-"+c.toLowerCase());
    if(!colors.has(name))throw Error("Missing theme colour: "+k);
  }
  for(const [text,bg,minimum] of [["foreground","canvas",4.5],["mutedText","canvas",4.5],["onPrimary","primary",4.5],["focus","canvas",3]]) {
    if(contrast(color(text),color(bg))<minimum)throw Error("Insufficient contrast: "+text+"/"+bg);
  }
  // Every text/surface combination used by Shared primitives is checked,
  // including semantic states inherited by a brand's additive theme layer.
  for(const [text,bg] of [["foreground","surface"],["mutedText","surface"],
    ["onSuccess","success"],["onWarning","warning"],["onDanger","danger"],["onInfo","info"]]) {
    if(contrast(color(text),color(bg))<4.5)throw Error("Insufficient contrast: "+text+"/"+bg);
  }
  if(contrast(color("focus"),color("surface"))<3)throw Error("Insufficient contrast: focus/surface");
  return colors;
}
function render(map,selector) {
  const content=[...map].sort(([a],[b])=>a.localeCompare(b)).map(([k,v])=>"  "+k+": "+v+";").join("\n");
  return "/* Generated by experience-tokens. DO NOT EDIT. */\n"+selector+" {\n"+content+"\n}\n";
}
export function compileBase(base) { return render(flattenTokens(base),":root"); }
export function compileTheme(base,theme,name) {
  if(!themeNames.includes(name))throw Error("Unknown theme name");
  return render(validateTheme(base,theme),':root[data-bx-theme="'+name+'"], [data-bx-theme="'+name+'"]');
}
