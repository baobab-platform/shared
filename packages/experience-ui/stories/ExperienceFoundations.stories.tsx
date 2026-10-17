/* Portable CSF stories: no engine/transport state or account identifiers. */
import {ActionButton,BreadcrumbTrail,Disclosure,FeedbackPanel,StatusLabel,MilestoneTimeline} from "../src/index.js";
export default {title:"Baobab Experience/Foundations",parameters:{layout:"padded"}};
export const Action={render:()=> <ActionButton>Review proposal</ActionButton>};
export const Pending={render:()=> <ActionButton pending>Awaiting confirmation</ActionButton>};
export const Breadcrumbs={render:()=> <BreadcrumbTrail items={[{label:"Home",href:"/"},{label:"Markets",href:"/markets"},{label:"Uganda"}]}/>};
export const NativeDisclosure={render:()=> <Disclosure summary="About this result">Source-labelled, authorised projection.</Disclosure>};
export const Restricted={render:()=> <FeedbackPanel state="restricted" title="Restricted" description="Not available in this context."/>};
export const Status={render:()=> <StatusLabel tone="warning">Review required</StatusLabel>};
export const Timeline={render:()=> <MilestoneTimeline items={[{id:"a",label:"Pickup reported",state:"uncertain"},{id:"b",label:"Arrival pending",state:"pending"}]}/>};
