"use client";

import {useEffect,useRef,useState} from "react";
import {ActionButton} from "@baobab-platform/experience-ui";
import type {Map as MapInstance,Marker,StyleSpecification} from "maplibre-gl";
import {locationLabel} from "@baobab-platform/experience-geo-core";
import {approvedResourceUrl,validatePoints,validateResourcePolicy,type MapPoint,type MapProjection,type MapResourcePolicy} from "./model.js";
export type {MapPoint,MapProjection,MapResourcePolicy} from "./model.js";

export type EvidenceMapProps=Readonly<{projection:MapProjection;policy:MapResourcePolicy;style:StyleSpecification;label:string}>;
/** Restricted projections unmount the entire renderer and discard its resources. */
export function EvidenceMap(props:EvidenceMapProps){
  if(props.projection.visibility==="restricted")return <section aria-label={props.label}><p role="alert">{props.projection.explanation}</p></section>;
  if(props.projection.visibility!=="authorised")throw new TypeError("Unknown map visibility");
  validatePoints(props.projection.points);validateResourcePolicy(props.policy);
  return <AuthorisedEvidenceMap {...props} points={props.projection.points}/>;
}

/**
 * MapLibre is imported only after an explicit request to enable the map. The
 * meaningful evidence list remains available when WebGL is absent, rendering
 * fails, the network is offline, or the user chooses a low-power presentation.
 * This component never fetches shipment projections or requests geolocation.
 */
function AuthorisedEvidenceMap({points,policy,style,label}:EvidenceMapProps&Readonly<{points:readonly MapPoint[]}>){
  const [enabled,setEnabled]=useState(false);
  const [phase,setPhase]=useState<"inactive"|"loading"|"ready"|"unavailable">("inactive");
  const [selected,setSelected]=useState<string|null>(null);
  const host=useRef<HTMLDivElement>(null),map=useRef<MapInstance|null>(null);
  useEffect(()=>{
    if(!enabled||!host.current)return;
    let disposed=false,instance:MapInstance|null=null,observer:ResizeObserver|null=null;
    const markers:Marker[]=[];
    setPhase("loading");
    void import("maplibre-gl").then(library=>{
      if(disposed||!host.current)return;
      instance=new library.Map({container:host.current,style,center:[20,0],zoom:1,
        attributionControl:false,collectResourceTiming:false,
        transformRequest:(url)=>({url:approvedResourceUrl(url,policy,window.location.origin),credentials:"same-origin"})});
      map.current=instance;
      instance.on("error",()=>{if(!disposed)setPhase("unavailable");});
      instance.on("load",()=>{if(!disposed)setPhase("ready");});
      for(const point of points){
        if(!point.observation.position)continue;
        const button=document.createElement("button");
        button.type="button";button.className="bx-map-marker";
        button.textContent=point.label;button.setAttribute("aria-label","Select "+point.label);
        button.addEventListener("click",()=>setSelected(point.id));
        markers.push(new library.Marker({element:button}).setLngLat([...point.observation.position]).addTo(instance));
      }
      observer=new ResizeObserver(()=>instance?.resize());observer.observe(host.current);
    }).catch(()=>{if(!disposed)setPhase("unavailable");});
    return ()=>{
      disposed=true;observer?.disconnect();for(const marker of markers)marker.remove();
      instance?.remove();map.current=null;
    };
  },[enabled,points,policy,style]);

  function select(point:MapPoint){
    setSelected(point.id);
    // A jump avoids nonessential motion and never interpolates an observation.
    if(point.observation.position)map.current?.jumpTo({center:[...point.observation.position]});
  }
  return <section aria-label={label} className="bx-evidence-map">
    <ActionButton type="button" onClick={()=>{setEnabled(v=>!v);setPhase("inactive");}}>{enabled?"Use text only":"Enable interactive map"}</ActionButton>
    <p role="status">{phase==="ready"?"Map ready; observations retain their source and age.":phase==="loading"?"Loading optional map…":phase==="unavailable"?"Map unavailable. All authorised evidence remains in the list.":"Text alternative active; no map resources loaded."}</p>
    {enabled?<div ref={host} className="bx-map-canvas" aria-label={label+" canvas"}/>:null}
    <p>{policy.attribution} · Licence: {policy.licenceReference}</p>
    {!points.length?<p>No authorised location evidence is available.</p>:<ul aria-label="Authorised location evidence">{points.map(point=><li key={point.id}>
      <ActionButton type="button" aria-pressed={selected===point.id} onClick={()=>select(point)}>{point.label}</ActionButton>
      <p>{locationLabel(point.observation)}</p><p>Freshness: {point.freshness}; evidence: {point.evidenceReference}</p>
      {point.estimate?<p>Estimate confidence: {point.observation.confidence}; model: {point.estimate.model}; version: {point.estimate.version}; generated: {point.estimate.generatedAt}; inputs: {point.estimate.inputsReference}</p>:null}
    </li>)}</ul>}
  </section>;
}
