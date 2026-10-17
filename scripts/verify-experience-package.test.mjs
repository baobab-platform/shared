import test from "node:test"
import assert from "node:assert/strict"
import { mkdtempSync,mkdirSync,writeFileSync,rmSync,readFileSync } from "node:fs"
import { join } from "node:path"
import { tmpdir } from "node:os"
import { execFileSync } from "node:child_process"
import { createHash } from "node:crypto"
import { verifyExperiencePackage } from "./verify-experience-package.mjs"

function fixture(omit=[]){
  const root=mkdtempSync(join(tmpdir(),"bxs-verify-"))
  const dir=join(root,"package")
  mkdirSync(join(dir,"dist"),{recursive:true})
  for(const file of ["dist/index.js","dist/index.d.ts","styles.css"]){
    if(!omit.includes(file))writeFileSync(join(dir,file),"synthetic local test export")
  }
  const name="@baobab-platform/experience-ui",version="0.2.0"
  writeFileSync(join(dir,"package.json"),JSON.stringify({
    name,version,private:false,publishConfig:{registry:"https://npm.pkg.github.com"}
  }))
  const tarball=join(root,"test.tgz")
  execFileSync("tar",["-czf",tarball,"-C",root,"package"])
  const integrity="sha512-"+createHash("sha512").update(readFileSync(tarball)).digest("base64")
  return {root,name,version,tarball,integrity}
}
test("accepts an exact archive and genuine SHA512",()=>{
  const f=fixture()
  try{assert.equal(verifyExperiencePackage(f).artifacts,3)}
  finally{rmSync(f.root,{recursive:true,force:true})}
})
test("rejects forged name, altered digest, wrong version and missing exports",()=>{
  const f=fixture(),missing=fixture(["styles.css"])
  try{
    assert.throws(()=>verifyExperiencePackage({...f,name:"@baobab-platform/unknown"}),/Unknown BXS/)
    assert.throws(()=>verifyExperiencePackage({...f,integrity:"sha512-"+("A".repeat(86))+"=="}),/integrity mismatch/)
    assert.throws(()=>verifyExperiencePackage({...f,version:"0.4.0"}),/version differs/)
    assert.throws(()=>verifyExperiencePackage(missing),/export missing/)
  }finally{
    rmSync(f.root,{recursive:true,force:true})
    rmSync(missing.root,{recursive:true,force:true})
  }
})
