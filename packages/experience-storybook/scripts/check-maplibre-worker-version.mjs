// Fail early when Dependabot upgrades MapLibre but the application-owned
// worker URL and Storybook static asset directory still name an older SDK.
// This never dynamically imports MapLibre or makes an external tile request.
import assert from "node:assert/strict";
import {readFileSync} from "node:fs";
import {fileURLToPath} from "node:url";

function read(relative) {
  return readFileSync(fileURLToPath(new URL(relative, import.meta.url)), "utf8");
}
const pkg=JSON.parse(read("../package.json"));
const geo=JSON.parse(read("../../experience-geo-maplibre/package.json"));
const version=pkg.devDependencies["maplibre-gl"];
assert.match(version,/^6\.[0-9]+\.[0-9]+$/,"MapLibre must be pinned in the Storybook fixture");
assert.equal(geo.devDependencies["maplibre-gl"],version,"Geo package and Storybook must test the same MapLibre SDK");
const story=read("../src/Map.stories.tsx");
const config=read("../.storybook/main.ts");
assert.ok(story.includes(`url:"/maplibre-${version}/maplibre-gl-worker.mjs"`),
  "MapLibre worker URL must match the installed runtime version");
assert.ok(story.includes(`version:"${version}"`),
  "MapLibre worker version check must match the installed runtime version");
assert.ok(config.includes(`to:"/maplibre-${version}"`),
  "Storybook must serve the correct SDK worker assets under its versioned path");
console.log(`MapLibre version ${version}, same-origin worker URL and static assets aligned`);
