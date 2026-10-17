import {test} from "node:test";
import assert from "node:assert/strict";
import {createElement} from "react";
import {renderToStaticMarkup} from "react-dom/server";
import {ActionButton,BreadcrumbTrail,Disclosure,FeedbackPanel,StatusLabel,MilestoneTimeline} from "../dist/index.js";
const render=(el)=>renderToStaticMarkup(el);
test("buttons default to a non-submitting type, and pending state is disabled",()=>{
  const html=render(createElement(ActionButton,{pending:true},"Review proposal"));
  assert.match(html,/type="button"/);assert.match(html,/disabled=""/);
  assert.match(html,/aria-busy="true"/);
});
test("breadcrumbs include only one current page and non-nested links",()=>{
  const html=render(createElement(BreadcrumbTrail,{items:[{label:"Home",href:"/"},{label:"Markets",href:"/markets"},{label:"Uganda"}]}));
  assert.match(html,/<nav[^>]+aria-label="Breadcrumb"/);
  assert.match(html,/<ol>/);assert.match(html,/aria-current="page">Uganda/);
  assert.equal((html.match(/aria-current="page"/g)||[]).length,1);
});
test("native details and summary retain browser keyboard semantics",()=>{
  const html=render(createElement(Disclosure,{summary:"Additional information"},"Source-labelled content"));
  assert.match(html,/<details/);assert.match(html,/<summary>Additional information<\/summary>/);
  assert.doesNotMatch(html,/role="button"/);
});
test("restricted feedback is alert; empty feedback is not",()=>{
  assert.match(render(createElement(FeedbackPanel,{state:"restricted",title:"Access denied",description:"Ask your administrator"})),/role="alert"/);
  assert.doesNotMatch(render(createElement(FeedbackPanel,{state:"empty",title:"No records",description:"Try a new filter"})),/role="alert"/);
});
test("timelines expose source-supplied milestone text and ISO datetime",()=>{
  const html=render(createElement(MilestoneTimeline,{items:[{id:"a",label:"Pickup reported",state:"uncertain",timestamp:"2026-10-17T10:00:00Z",detail:"Unverified carrier report"}]}));
  assert.match(html,/<ol>/);assert.match(html,/dateTime="2026-10-17T10:00:00Z"|dateTime="2026-10-17T10:00:00Z"|datetime="2026-10-17T10:00:00Z"/);
  assert.match(html,/Unverified carrier report/);
  assert.match(render(createElement(StatusLabel,{tone:"warning"},"Review required")),/Review required/);
  assert.throws(()=>render(createElement(MilestoneTimeline,{items:[{id:"x",label:"a",state:"pending"},{id:"x",label:"b",state:"pending"}]})),/unique/);
});

test("source timelines reject invalid calendar dates, unknown states and blank evidence",()=>{
  const item={id:"valid",label:"Synthetic carrier report",state:"uncertain",timestamp:"2026-10-17T10:00:00Z"};
  for(const override of [{timestamp:"2026-02-30T12:00:00Z"},{timestamp:"2026-10-17T10:00:00"},
    {state:"delivered-by-browser"},{label:" "},{id:" "}]){
    assert.throws(()=>render(createElement(MilestoneTimeline,{items:[{...item,...override}]})));
  }
  for(const state of ["stale","pending","success"]){
    assert.match(render(createElement(FeedbackPanel,{state,title:"Synthetic state",description:"Presentation only"})),/Synthetic state/);
  }
});
