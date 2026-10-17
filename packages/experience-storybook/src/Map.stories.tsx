import {useState} from "react"
import type {Meta,StoryObj} from "@storybook/react-vite"
import {EvidenceMap,type MapProjection} from "@baobab-platform/experience-geo-maplibre"
import "@baobab-platform/experience-geo-maplibre/styles.css"
import "maplibre-gl/dist/maplibre-gl.css"

const projection:MapProjection={visibility:"authorised",projectionReference:"synthetic:view:1",points:[{
  id:"synthetic-one",label:"Synthetic carrier report",evidenceReference:"synthetic:observation:1",freshness:"stale",
  observation:{kind:"carrier-reported",position:[32.5,0.3],source:"Synthetic carrier",observedAt:"2026-10-17T10:00:00Z"},
}]}
const policy={allowedOrigins:[],attribution:"Local synthetic blank map — no provider tiles",licenceReference:"Internal fixture; provider selection pending"}
const worker={url:"/maplibre-6.14.0/maplibre-gl-worker.mjs",version:"6.14.0"}
const style={version:8 as const,sources:{},layers:[{id:"background",type:"background" as const,paint:{"background-color":"#fffdf8"}}]}
function Demo(){
  const [restricted,setRestricted]=useState(false)
  return <><button onClick={()=>setRestricted(true)}>Revoke synthetic visibility</button>
    <EvidenceMap label="Synthetic location evidence" policy={policy} worker={worker} style={style} projection={restricted?{visibility:"restricted",explanation:"Synthetic projection access revoked"}:projection}/></>
}
const meta={title:"BXS/Map",parameters:{layout:"fullscreen",a11y:{manual:true}}} satisfies Meta
export default meta
type Story=StoryObj<typeof meta>
export const Evidence:Story={render:()=> <Demo/>}
