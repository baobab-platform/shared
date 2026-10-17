/** Deterministically compile published CSS without downloading anything. */
import { mkdirSync, writeFileSync } from "node:fs";
import { compileBase, compileTheme, readTokens, themeNames } from "./tokens.mjs";
const base = readTokens("base.tokens.json");
mkdirSync(new URL("../dist/themes/",import.meta.url),{recursive:true});
writeFileSync(new URL("../dist/base.css",import.meta.url),compileBase(base));
for(const name of themeNames)writeFileSync(new URL("../dist/themes/"+name+".css",import.meta.url),compileTheme(base,readTokens("themes/"+name+".tokens.json"),name));
