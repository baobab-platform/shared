/**
 * BXS-VFA: deterministic SOURCE-theme contrast receipts.
 * No theme in this module is a consumer/brand approval or UI/AT certification.
 */
import {contrast,flattenTokens,readTokens,themeNames,validateTheme} from "./tokens.mjs";

export const PAIRS=Object.freeze([
  ["foreground","canvas",4.5],["foreground","surface",4.5],
  ["mutedText","canvas",4.5],["mutedText","surface",4.5],
  ["onPrimary","primary",4.5],["onSuccess","success",4.5],
  ["onWarning","warning",4.5],["onDanger","danger",4.5],
  ["onInfo","info",4.5],["focus","canvas",3],["focus","surface",3],
]);

const key = name => "--bx-color-"+name.replace(/[A-Z]/g,c=>"-"+c.toLowerCase());

export function createVisualProfileReport(base=readTokens("base.tokens.json"),
    loadTheme=name=>readTokens("themes/"+name+".tokens.json")) {
  const source=flattenTokens(base);
  const themes=[];
  for(const name of themeNames) {
    const theme=loadTheme(name);
    // Enforces strict validation on top of the independently inspectable report.
    const colors=validateTheme(base,theme);
    const value=k=>colors.get(key(k))??source.get(key(k));
    const pairings=PAIRS.map(([foreground,background,minimum])=>{
      const ratio=Number(contrast(value(foreground),value(background)).toFixed(3));
      if(ratio < minimum)throw Error("Visual profile contrast failed: "+name+" "+foreground+"/"+background);
      return {foreground,background,minimum,ratio,pass:true};
    });
    const status=theme.$extensions?.baobab?.status;
    if(typeof status!=="string"||!status)throw Error("Theme source approval status missing: "+name);
    themes.push({name,status,brandApproved:false,pairings});
  }
  return {
    profile:"BXS-VFA-v1.0",
    classification:"SOURCE_OBSERVED_TOKEN_CONTRAST_ONLY",
    note:"No browser/real-device, manual assistive-technology, consumer or brand certification",
    themes
  };
}
