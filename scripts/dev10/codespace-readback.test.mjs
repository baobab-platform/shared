import test from "node:test";
import assert from "node:assert/strict";
import {checkSource} from "./codespace-readback.mjs";
const image="ghcr.io/baobab-platform/baobab-dev:1.4.4-frontend@sha256:"+"a".repeat(64);
const config={remoteUser:"vscode",image,waitFor:"postCreateCommand",otherPortsAttributes:{visibility:"private"}};
const manifest={packageManager:"pnpm@11.24.0"};
test("valid source conformance has bounded, read-only claim",()=>{
 const v=checkSource({repository:"zuribeans",root:"/tmp",devcontainer:config,manifest,observedNode:"v24.21.0",observedPnpm:"11.24.0"});
 assert.equal(v.readiness,"postCreateCommand");assert.equal(v.image,image);
});
for(const [name,dc] of Object.entries({
 prebuild_ready:{...config,waitFor:"updateContentCommand"},
 public_ports:{...config,otherPortsAttributes:{visibility:"public"}},
 mutable_image:{...config,image:"ghcr.io/baobab-platform/baobab-dev:latest"},
 root_user:{...config,remoteUser:"root"}
}))test("fails closed: "+name,()=>assert.throws(()=>checkSource({
 repository:"zuribeans",root:"/tmp",devcontainer:dc,manifest,observedNode:"v26.13.0",observedPnpm:"11.24.0"
})));
test("incorrect manager pin rejected",()=>assert.throws(()=>checkSource({repository:"nabhold",root:"/tmp",devcontainer:config,manifest,observedNode:"v26.13.0",observedPnpm:"12.16.1"})));
