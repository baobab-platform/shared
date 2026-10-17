/** Read-only validation shares precisely the production build rules. */
import {compileBase,compileTheme,readTokens,themeNames} from "./tokens.mjs";
const base=readTokens("base.tokens.json");
compileBase(base);
for(const name of themeNames)compileTheme(base,readTokens("themes/"+name+".tokens.json"),name);
