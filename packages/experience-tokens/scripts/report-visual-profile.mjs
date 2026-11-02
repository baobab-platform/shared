/** Print a deterministic machine-readable source-level contrast receipt for CI. */
import {createVisualProfileReport} from "./visual-profile.mjs";
process.stdout.write(JSON.stringify(createVisualProfileReport(),null,2)+"\n");
