/**
 * BXS-04: native/semantic React presentation. No domain grants or engine SDK.
 * Components accept caller-authorised view models. Nothing here grants access.
 */
import {forwardRef, type ReactNode, type ButtonHTMLAttributes, type DetailsHTMLAttributes} from "react";
import {Button as BaseButton} from "@base-ui/react/button";
import {assertEvidenceTimestamp} from "@baobab-platform/experience-geo-core";
export {ExperienceDialog,ExperienceTabs,type ExperienceTab} from "./interactive.js";

export type ActionButtonProps = Omit<ButtonHTMLAttributes<HTMLButtonElement>,"children"> & Readonly<{
  children:ReactNode;
  intent?:"primary"|"secondary"|"quiet"|"danger";
  pending?:boolean;
}>;
/** A click and pending request do not constitute an acknowledged domain action. */
export const ActionButton=forwardRef<HTMLButtonElement,ActionButtonProps>(
  function ActionButton({intent="primary",pending=false,disabled,type="button",className="",children,...props},ref){
    return <BaseButton {...props} ref={ref} type={type} disabled={Boolean(disabled||pending)}
      aria-busy={pending||undefined}
      className={["bx-button","bx-button--"+intent,className].filter(Boolean).join(" ")}>{children}</BaseButton>;
  }
);

export type BreadcrumbItem=Readonly<{label:string;href?:string}>;
export type BreadcrumbTrailProps=Readonly<{items:readonly BreadcrumbItem[];label?:string;className?:string}>;
/** The caller supplies published page labels/hierarchy, never slug guesses. */
export function BreadcrumbTrail({items,label="Breadcrumb",className=""}:BreadcrumbTrailProps){
  if(!items.length)return null;
  return <nav aria-label={label} className={["bx-breadcrumbs",className].filter(Boolean).join(" ")}>
    <ol>{items.map((item,i)=><li key={i}>{
      i===items.length-1||!item.href
      ? <span aria-current={i===items.length-1?"page":undefined}>{item.label}</span>
      : <a href={item.href}>{item.label}</a>
    }</li>)}</ol>
  </nav>;
}

export type DisclosureProps=Omit<DetailsHTMLAttributes<HTMLDetailsElement>,"children"> & Readonly<{
  summary:ReactNode;children:ReactNode;
}>;
/** Native details/summary gives keyboard control without a client runtime. */
export function Disclosure({summary,children,className="",...props}:DisclosureProps){
  return <details {...props} className={["bx-disclosure",className].filter(Boolean).join(" ")}>
    <summary>{summary}</summary><div className="bx-disclosure__content">{children}</div>
  </details>;
}

export type FeedbackState="empty"|"loading"|"error"|"unavailable"|"restricted"|"stale"|"pending"|"success";
export type FeedbackPanelProps=Readonly<{
  state:FeedbackState;title:string;description:string;action?:ReactNode;className?:string;
}>;
/** Restricted content only displays a prior BFF decision; it is not itself a policy check. */
export function FeedbackPanel({state,title,description,action,className=""}:FeedbackPanelProps){
  const urgent=state==="error"||state==="restricted";
  return <section role={urgent?"alert":["loading","pending","success"].includes(state)?"status":undefined}
    aria-busy={state==="loading"||undefined} aria-label={title}
    className={["bx-feedback","bx-feedback--"+state,className].filter(Boolean).join(" ")}>
    <h2 className="bx-feedback__title">{title}</h2><p>{description}</p>
    {action?<div className="bx-feedback__action">{action}</div>:null}
  </section>;
}

export type StatusTone="neutral"|"info"|"success"|"warning"|"danger";
export type StatusLabelProps=Readonly<{tone?:StatusTone;children:ReactNode;className?:string}>;
/** Always show a human-readable state; colour does not replace meaning. */
export function StatusLabel({tone="neutral",children,className=""}:StatusLabelProps){
  return <span className={["bx-status","bx-status--"+tone,className].filter(Boolean).join(" ")}>{children}</span>;
}

export type MilestoneItem=Readonly<{
  id:string;label:string;detail?:string;timestamp?:string;timestampLabel?:string;
  state:"completed"|"current"|"pending"|"uncertain";
}>;
export type MilestoneTimelineProps=Readonly<{items:readonly MilestoneItem[];label?:string;className?:string}>;
/**
 * Timeline is a view of caller-provided milestones, not a transport event
 * generator. Estimated positions must never be rendered as actual arrivals.
 */
export function MilestoneTimeline({items,label="Progress timeline",className=""}:MilestoneTimelineProps){
  const seen=new Set<string>();
  for(const item of items){
    if(typeof item.id!=="string"||!item.id.trim()||seen.has(item.id))throw new Error("Timeline IDs must be unique and nonempty");
    seen.add(item.id);
    // Types do not validate JSON at runtime. Never promote unknown source
    // states or normalised impossible dates into a trustworthy milestone.
    if(typeof item.label!=="string"||!item.label.trim())throw new TypeError("Milestone label is required");
    if(!["completed","current","pending","uncertain"].includes(item.state))throw new TypeError("Unknown milestone state");
    if(item.timestamp!==undefined)assertEvidenceTimestamp(item.timestamp);
  }
  return <section aria-label={label} className={["bx-timeline",className].filter(Boolean).join(" ")}>
    <ol>{items.map(item=><li key={item.id} className={"bx-timeline__item bx-timeline__item--"+item.state}>
      <span aria-hidden="true" className="bx-timeline__marker"/>
      <div className="bx-timeline__body">
        <strong>{item.label}</strong>
        <span className="bx-timeline__state">{item.state}</span>
        {item.timestamp?<time dateTime={item.timestamp}>{item.timestampLabel??item.timestamp}</time>:null}
        {item.detail?<p>{item.detail}</p>:null}
      </div>
    </li>)}</ol>
  </section>;
}
