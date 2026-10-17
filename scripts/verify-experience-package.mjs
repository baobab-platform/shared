/**
 * BXS-05: verify an npm registry archive. This code neither publishes nor
 * creates business authority. It fails closed on source/version/SHA drift.
 */
import assert from "node:assert/strict"
import { createHash } from "node:crypto"
import { readFileSync } from "node:fs"
import { execFileSync } from "node:child_process"
import { resolve } from "node:path"
import { fileURLToPath } from "node:url"

const required={
  "@baobab-platform/experience-tokens": [
    "package/dist/base.css","package/dist/themes/nabhold.css",
    "package/dist/themes/zuribeans.css","package/dist/themes/thamani.css",
    "package/dist/themes/baobab-platform.css",
  ],
  "@baobab-platform/experience-ui": [
    "package/dist/index.js","package/dist/index.d.ts","package/styles.css",
  ],
  "@baobab-platform/experience-geo-core": [
    "package/dist/index.js","package/dist/index.d.ts",
  ],
}
export function verifyExperiencePackage({name,version,tarball,integrity}) {
  assert.ok(Object.hasOwn(required,name),"Unknown BXS package")
  assert.match(version,/^\d+\.\d+\.\d+(?:-[A-Za-z0-9.-]+)?$/)
  assert.match(integrity,/^sha512-[A-Za-z0-9+/]+={0,2}$/)
  const actual="sha512-"+createHash("sha512").update(readFileSync(tarball)).digest("base64")
  assert.equal(actual,integrity,"Registry archive integrity mismatch")
  const paths=new Set(execFileSync("tar",["-tzf",tarball],{encoding:"utf8"})
    .split("\n").filter(Boolean).map(x=>x.replace(/\/$/,"")))
  for(const path of paths){
    assert.ok(path.startsWith("package/"),"Unexpected archive root")
    assert.ok(!path.split("/").includes(".."),"Unsafe path traversal")
  }
  assert.ok(paths.has("package/package.json"),"Manifest missing")
  for(const path of required[name])assert.ok(paths.has(path),"Published export missing: "+path)
  const manifest=JSON.parse(execFileSync("tar",["-xOzf",tarball,"package/package.json"],{encoding:"utf8"}))
  assert.equal(manifest.name,name,"Wrong package in archive")
  assert.equal(manifest.version,version,"Published version differs from source")
  assert.equal(manifest.private,false,"Archive marked private")
  assert.equal(manifest.publishConfig?.registry,"https://npm.pkg.github.com")
  return {name,version,integrity,artifacts:required[name].length}
}
if(process.argv[1]&&resolve(process.argv[1])===fileURLToPath(import.meta.url)){
  const [name,version,tarball,integrity]=process.argv.slice(2)
  if(!name||!version||!tarball||!integrity)throw Error("Expected name version tarball integrity")
  console.log(JSON.stringify(verifyExperiencePackage({name,version,tarball,integrity})))
}
