/**
 * Loopback-only static CI server: no backend, BFF, auth or data provider.
 * Responds from the built Storybook folder, rejecting path traversal.
 */
import { createServer } from "node:http"
import { readFile, stat } from "node:fs/promises"
import { dirname, resolve, sep, extname } from "node:path"
import { fileURLToPath } from "node:url"
const root=resolve(dirname(fileURLToPath(import.meta.url)),"../storybook-static")
const mime={".html":"text/html; charset=utf-8",".js":"text/javascript; charset=utf-8",
  ".mjs":"text/javascript; charset=utf-8",".css":"text/css; charset=utf-8",
  ".json":"application/json; charset=utf-8",".svg":"image/svg+xml",".png":"image/png",
  ".woff2":"font/woff2",".webp":"image/webp"}
createServer(async (request,response)=>{
  try{
    const url=new URL(request.url||"/","http://127.0.0.1")
    const local=decodeURIComponent(url.pathname)
    const file=resolve(root,"."+(local==="/"?"/index.html":local))
    if(file!==root&&!file.startsWith(root+sep)){response.writeHead(403).end("Forbidden");return}
    const info=await stat(file)
    if(!info.isFile())throw Error("Not a file")
    response.setHeader("Content-Type",mime[extname(file)]||"application/octet-stream")
    response.setHeader("Cache-Control","no-store")
    response.end(await readFile(file))
  }catch{response.writeHead(404).end("Not found")}
}).listen(6006,"127.0.0.1")
