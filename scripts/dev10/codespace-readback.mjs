#!/usr/bin/env node
// DEV10-R2 observed-user readback. Must execute INSIDE a real hosted Codespace.
// This is evidence collection, not GHCR host-image attestation or a CP grant.
// NEVER record token, stderr, location, username, package URLs or Codespace name.
import { createHash } from "node:crypto";
import { existsSync, mkdirSync, readFileSync, writeFileSync, openSync, closeSync } from "node:fs";
import { execFileSync, spawnSync } from "node:child_process";
import { dirname, join, resolve, relative } from "node:path";

const ALLOWED = new Set(["nabhold", "zuribeans", "thamani", "baobab-cp"]);
function abort(message) { throw new Error(message); }
function digest(value) { return createHash("sha256").update(value).digest("hex"); }
function command(bin, args, cwd, timeout=90000) {
  return spawnSync(bin, args, {cwd, env:{...process.env, CI:"true",
    COREPACK_ENABLE_DOWNLOAD_PROMPT:"0",COREPACK_DEFAULT_TO_LATEST:"0"},
    encoding:"utf8",timeout,maxBuffer:128*1024, shell:false});
}
function source(path) { return readFileSync(path,"utf8"); }
function manifestPackages(root) {
  const paths=[join(root,"package.json"),join(root,"frontend/package.json")];
  const pkgs=join(root,"packages");
  if(existsSync(pkgs)) {
    for(const d of (awaitNoAsyncDirs(pkgs))) paths.push(join(pkgs,d,"package.json"));
  }
  const all=paths.filter(existsSync).map(p=>JSON.parse(source(p)));
  const own=new Set(all.map(m=>m.name));
  const result=new Map();
  for(const m of all) for(const [name,version] of Object.entries({
    ...m.dependencies,...m.devDependencies,...m.optionalDependencies
  })) {
    if(!name.startsWith("@baobab-platform/"))continue;
    if(version.startsWith("workspace:") && own.has(name))continue;
    if(!/^@baobab-platform\/[a-z0-9._-]+$/.test(name) ||
       !/^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$/.test(version))
      abort("NON_EXACT_PRIVATE_DEPENDENCY");
    if(result.has(name) && result.get(name)!==version)
      abort("CONFLICTING_PRIVATE_DEPENDENCY_VERSIONS");
    result.set(name,version);
  }
  return [...result].sort((a,b)=>a[0].localeCompare(b[0]));
}
function awaitNoAsyncDirs(path) {
  // only root-owned package manifests, never recursive traversal of node_modules.
  return (requireReaddir(path)).filter(name=>/^[a-z0-9._-]+$/.test(name));
}
function requireReaddir(path) { return readdirSync(path,{withFileTypes:true})
  .filter(x=>x.isDirectory()).map(x=>x.name); }
export function checkSource({repository,root,devcontainer,manifest,observedNode,observedPnpm}) {
  if(!ALLOWED.has(repository))abort("UNREVIEWED_REPOSITORY");
  if(devcontainer.waitFor!=="postCreateCommand")abort("POSTCREATE_NOT_READINESS_GATE");
  if(devcontainer.remoteUser!=="vscode")abort("UNTRUSTED_RUNTIME_USER");
  if(!/^ghcr\.io\/baobab-platform\/baobab-dev:[a-z0-9.-]+@sha256:[a-f0-9]{64}$/.test(devcontainer.image))
    abort("MISSING_IMMUTABLE_IMAGE");
  if(devcontainer.otherPortsAttributes?.visibility!=="private")
    abort("UNSAFE_DEFAULT_PORT_VISIBILITY");
  const expected=manifest.packageManager || (repository==="baobab-cp"?manifest.frontendPackageManager:null);
  if(expected && !/^pnpm@\d+\.\d+\.\d+$/.test(expected))abort("UNPINNED_MANAGER");
  if(expected && observedPnpm!==expected.split("@")[1])abort("PINNED_PNPM_MISMATCH");
  if(observedNode && !/^v\d+\.\d+\.\d+$/.test(observedNode))abort("INVALID_NODE_READBACK");
  return {image:devcontainer.image,expected,readiness:devcontainer.waitFor};
}
export function run({repository,root,out}) {
  if(process.env.CODESPACES!=="true" || !process.env.CODESPACE_NAME)
    abort("NOT_HOSTED_CODESPACE");
  if(!ALLOWED.has(repository))abort("UNREVIEWED_REPOSITORY");
  if(!out.startsWith("/tmp/") || out.startsWith(root+"/"))
    abort("RECEIPT_DIRECTORY_MUST_BE_PRIVATE_TEMPORARY");
  const dc=JSON.parse(source(join(root,".devcontainer/devcontainer.json")));
  const m=JSON.parse(source(join(root,"package.json")));
  const actualRepo=process.env.GITHUB_REPOSITORY || "";
  if(actualRepo && actualRepo!==`baobab-platform/${repository}`)abort("CODESPACE_SOURCE_REPOSITORY_MISMATCH");
  const node=process.version;
  const pnpm=command("pnpm",["--version"],root);
  if(pnpm.error || pnpm.status!==0)abort("PNPM_UNAVAILABLE");
  const pin=checkSource({repository,root,devcontainer:dc,manifest:m,
    observedNode:node, observedPnpm:pnpm.stdout.trim()});
  const git=command("git",["rev-parse","HEAD"],root);
  if(git.status!==0 || !/^[a-f0-9]{40}\s*$/.test(git.stdout))abort("SOURCE_SHA_UNAVAILABLE");
  const origin=command("git",["config","--get","remote.origin.url"],root);
  if(origin.status!==0 || !origin.stdout.includes("baobab-platform/"+repository))
    abort("UNTRUSTED_SOURCE_ORIGIN");
  const packages=manifestPackages(root);
  if(packages.length && !process.env.BAOBAB_PACKAGES_READ_TOKEN && !process.env.GITHUB_TOKEN)
    abort("PRIVATE_REGISTRY_TOKEN_NOT_AVAILABLE");
  let reads=0;
  for(const [name,version] of packages) {
    const p=command("pnpm",["view",name+"@"+version,"version","--registry",
      "https://npm.pkg.github.com"],root,90000);
    // Never include raw stdout, stderr or package URL in failure reports.
    if(p.error || p.status!==0 || p.stdout.trim().replace(/^"|"$/g,"")!==version)
      abort("PRIVATE_PACKAGE_READ_DENIED");
    reads++;
  }
  // Real fresh installation is already performed in postCreateCommand.
  // Verify again without Corepack interactive downloads or lock regeneration.
  const install=command("pnpm",["install","--frozen-lockfile"],root,1200000);
  if(install.error || install.status!==0)abort("FROZEN_INSTALL_FAILED");
  const verify=command("baobab-verify",["--contract"],root,90000);
  if(verify.error || verify.status!==0)abort("BAOBAB_CONTRACT_VERIFICATION_FAILED");
  const receipt={schema:"dev10-hosted-codespace-readback.v1",
    execution:"HOSTED_CODESPACE_OBSERVED",repository,source_sha:git.stdout.trim(),
    image_declaration:pin.image,image_runtime_digest_attested:false,
    principal_observed_id_sha256:digest(process.env.CODESPACE_NAME),
    node:node.slice(1),pnpm:pnpm.stdout.trim(),private_packages_read:reads,
    private_read_test:packages.length?"PASSED":"NOT_APPLICABLE",
    frozen_install:"PASSED",developer_contract:"PASSED",
    independent_cleanup:"NOT_OBSERVED",fresh_create_independently_attested:false,
    qualified:false,
    limits:"Codespace user readback only; GHCR pre-start auth, resource freshness, independent cleanup and released image provenance need external verification"};
  mkdirSync(out,{recursive:true,mode:0o700});
  const target=join(out,"receipt.json");
  const h=openSync(target,"wx",0o600);
  try { writeFileSync(h,JSON.stringify(receipt,null,2)+"\n"); } finally {closeSync(h);}
  writeFileSync(join(out,"receipt.sha256"),digest(source(target))+"  receipt.json\n",
    {flag:"wx",mode:0o600});
  return target;
}
import {readdirSync} from "node:fs";
if(process.argv[1] && process.argv[1]===new URL(import.meta.url).pathname) {
  try {
    const args=process.argv.slice(2);
    if(args.length!==3)abort("USAGE: node codespace-readback.mjs REPOSITORY WORKSPACE_ROOT PRIVATE_TMP_OUTPUT");
    const [repository,workspace,output]=args;
    const receipt=run({repository,root:resolve(workspace),out:resolve(output)});
    console.log("DEV10_R2_USER_READBACK_CAPTURED; NOT_RELEASE_QUALIFIED; receipt="+receipt);
  } catch (e) {
    console.error("DEV10_R2_DENIED: "+(/^[_A-Z0-9]+$/.test(e.message)?e.message:"UNCLASSIFIED_VALIDATION_ERROR"));
    process.exitCode=2;
  }
}
