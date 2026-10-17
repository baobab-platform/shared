/**
 * ADR-SHARED-040: source-labelled, authority-neutral map presentation utilities.
 * No SDK, route optimiser, tracking store, tenant resolver or execution logic.
 */
export type LonLat = readonly [longitude: number, latitude: number];
export type LocationKind = "observed-gps" | "carrier-reported" | "milestone-derived" | "estimated";
export type LocationObservation = Readonly<{
  kind: LocationKind;
  position: LonLat | null;
  source: string;
  observedAt: string | null;
  accuracyMeters?: number | null;
  confidence?: number | null;
}>;
export type MapBounds = Readonly<{
  west: number; east: number; south: number; north: number;
  crossesAntimeridian: boolean;
}>;

/** Reject rather than silently clamping an invalid observation. */
export function assertLonLat(p: readonly number[]): asserts p is LonLat {
  if (p.length !== 2 || !Number.isFinite(p[0]) || !Number.isFinite(p[1]) ||
      p[0]! < -180 || p[0]! > 180 || p[1]! < -90 || p[1]! > 90)
    throw new RangeError("Expected finite [longitude -180..180, latitude -90..90]");
}

/** Angular delta for visual display only; never a transport/routing decision. */
export function shortestLongitudeDelta(from: number, to: number): number {
  assertLonLat([from,0]);
  assertLonLat([to,0]);
  const delta = ((to - from + 540) % 360) - 180;
  return delta === -180 ? 180 : delta;
}
function norm(lon: number): number {
  const result=((lon+180)%360+360)%360-180;
  return result===-180 && lon>0 ? 180 : result;
}
/**
 * Minimal longitude span on the circle. Remove the largest gap, allowing
 * a west > east interval to explicitly indicate anti-meridian crossing.
 */
export function boundsForPositions(points: readonly LonLat[]): MapBounds | null {
  if(points.length===0) return null;
  for(const p of points)assertLonLat(p);
  const sorted=points.map(p=>((p[0]%360)+360)%360).sort((a,b)=>a-b);
  let largest=-1,index=0;
  for(let i=0;i<sorted.length;i++){
    const next=i===sorted.length-1 ? sorted[0]!+360:sorted[i+1]!;
    const gap=next-sorted[i]!;
    if(gap>largest){largest=gap;index=i;}
  }
  const west=norm(sorted[(index+1)%sorted.length]!);
  const east=norm(sorted[index]!);
  return Object.freeze({
    west,east,south:Math.min(...points.map(p=>p[1])),
    north:Math.max(...points.map(p=>p[1])),
    crossesAntimeridian:west>east
  });
}
const names: Record<LocationKind,string>={
  "observed-gps":"Observed GPS position",
  "carrier-reported":"Carrier-reported position",
  "milestone-derived":"Milestone-derived approximate location",
  "estimated":"Estimated position — not observed"
};
/** Does not convert observed location into a legal/transport milestone. */
export function validateLocationObservation(o: LocationObservation): LocationObservation {
  if(!Object.hasOwn(names,o.kind)) throw new TypeError("Unknown source kind");
  if(typeof o.source!=="string" || !o.source.trim())throw new TypeError("Missing source attribution");
  if(o.position!==null)assertLonLat(o.position);
  if(o.observedAt!==null && (!/^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?(?:Z|[+-]\d\d:\d\d)$/.test(o.observedAt) ||
     !Number.isFinite(Date.parse(o.observedAt))))throw new TypeError("Expected ISO timestamp with timezone");
  if(o.accuracyMeters!=null && (!Number.isFinite(o.accuracyMeters)||o.accuracyMeters<0))throw new RangeError("Invalid accuracy");
  if(o.confidence!=null && (!Number.isFinite(o.confidence)||o.confidence<0||o.confidence>1))throw new RangeError("Invalid confidence");
  return Object.freeze({...o,position:o.position===null?null:Object.freeze([...o.position]) as unknown as LonLat});
}
/** Always label source, age/absence and estimate vs observed; never say "Live". */
export function locationLabel(o: LocationObservation): string {
  validateLocationObservation(o);
  const status=o.position===null?" — position unavailable":"";
  const time=o.observedAt===null?" (time unavailable)":" as of "+o.observedAt;
  return names[o.kind]+"; source: "+o.source+status+time;
}
