import { assertEvidenceTimestamp, validateLocationObservation, type LocationObservation } from "@baobab-platform/experience-geo-core";

export type MapPoint = Readonly<{
  id:string;label:string;evidenceReference:string;observation:LocationObservation;
  /** Supplied by the authorised BFF; the browser does not certify freshness. */
  freshness:"current"|"stale"|"unknown";
  estimate?:Readonly<{model:string;version:string;generatedAt:string;inputsReference:string}>;
}>;
export type MapProjection = Readonly<{visibility:"restricted";explanation:string}> |
  Readonly<{visibility:"authorised";projectionReference:string;points:readonly MapPoint[]}>;
export type MapResourcePolicy = Readonly<{allowedOrigins:readonly string[];attribution:string;licenceReference:string}>;
export type MapWorkerAsset=Readonly<{url:string;version:string}>;

/** Worker executable code must be a version-matched, application-owned asset. */
export function approvedWorkerUrl(asset:MapWorkerAsset,applicationOrigin:string,runtimeVersion:string):string {
  const url=new URL(asset.url,applicationOrigin);
  if(asset.version!==runtimeVersion||url.origin!==applicationOrigin||url.username||url.password||url.search||url.hash||!url.pathname.endsWith("/maplibre-gl-worker.mjs"))throw new TypeError("A same-origin version-matched MapLibre worker asset is required");
  return url.href;
}

/** Data is already redacted by the BFF. Reject unknown metadata, never infer facts. */
export function validatePoints(points:readonly MapPoint[]):void {
  if(points.length>500)throw new RangeError("Marker profile supports at most 500 points; use a separately qualified analytical adapter");
  const ids=new Set<string>();
  for(const point of points){
    if(!point.id.trim()||ids.has(point.id)||!point.label.trim()||!point.evidenceReference.trim())throw new TypeError("Map evidence requires unique IDs, labels and references");
    ids.add(point.id);validateLocationObservation(point.observation);
    if(!["current","stale","unknown"].includes(point.freshness))throw new TypeError("Unknown freshness classification");
    if(point.observation.kind==="estimated"){
      const e=point.estimate;
      if(point.observation.confidence==null)throw new TypeError("Estimated positions require explicit confidence");
      if(!e||![e.model,e.version,e.inputsReference].every(v=>typeof v==="string"&&v.trim()))throw new TypeError("Estimated positions require model, version and input provenance");
      assertEvidenceTimestamp(e.generatedAt);
    }
  }
}

/**
 * Explicit browser egress boundary. No default tile vendor, ambient cookies,
 * URL credentials, donation tile SLA, or arbitrary scheme is permitted.
 * Errors intentionally omit URLs because provider URLs may contain identifiers.
 */
export function validateResourcePolicy(policy:MapResourcePolicy):void {
  if(!policy.attribution.trim()||!policy.licenceReference.trim())throw new TypeError("Map attribution and reviewed licence reference are required");
  for(const origin of policy.allowedOrigins){
    const url=new URL(origin);
    if(url.protocol!=="https:"||url.origin!==origin||url.username||url.password)throw new TypeError("Approved map origins must be exact HTTPS origins");
    if(url.hostname==="tile.openstreetmap.org"||url.hostname.endsWith(".tile.openstreetmap.org"))throw new TypeError("Donation-operated public tiles are not an enterprise provider");
  }
}
export function approvedResourceUrl(value:string,policy:MapResourcePolicy,applicationOrigin?:string):string {
  validateResourcePolicy(policy);
  const url=new URL(value);
  if(url.protocol!=="https:"||url.username||url.password||!policy.allowedOrigins.includes(url.origin))throw new TypeError("Map resource origin is not approved");
  // MapLibre's credentials type supports same-origin, not fetch's omit.
  // A dedicated asset origin plus same-origin mode prevents forwarding the
  // application's ambient session cookies without lying to the type system.
  if(applicationOrigin!==undefined&&url.origin===applicationOrigin)throw new TypeError("Map assets require a dedicated origin separate from the application session");
  return url.href;
}
