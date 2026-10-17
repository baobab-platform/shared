import { useState } from "react"
import type { Meta, StoryObj } from "@storybook/react-vite"
import { ActionButton, BreadcrumbTrail, Disclosure, FeedbackPanel, MilestoneTimeline, StatusLabel } from "@baobab-platform/experience-ui"

function ActionDemo() {
  // Clicks are local example UI state, not a domain operation or approval.
  const [clicks, setClicks] = useState(0)
  return <div style={{display:"grid",justifyItems:"start",gap:16}}>
    <ActionButton onClick={() => setClicks(n => n + 1)}>Review proposal</ActionButton>
    <output aria-label="Local click count">{clicks}</output>
  </div>
}
const meta = { title:"BXS/Foundations", tags:["autodocs"], parameters:{layout:"fullscreen"} } satisfies Meta
export default meta
type Story = StoryObj<typeof meta>
export const Action: Story = { render:() => <ActionDemo /> }
export const Pending: Story = { render:() => <ActionButton pending>Waiting for confirmation</ActionButton> }
export const Breadcrumbs: Story = { render:() => <BreadcrumbTrail items={[
  {label:"Home",href:"/"},{label:"Markets",href:"/markets"},{label:"Uganda"}]} /> }
export const NativeDisclosure: Story = { render:() => <Disclosure summary="Source and accuracy">
  Observations require provider attribution. An estimate is never live GPS.
</Disclosure> }
export const Restricted: Story = { render:() => <FeedbackPanel state="restricted" title="Access restricted"
  description="This information is unavailable in the current authorised context." /> }
export const Milestones: Story = { render:() => <div style={{maxWidth:600}}>
  <StatusLabel tone="warning">Source review required</StatusLabel>
  <MilestoneTimeline items={[
    {id:"pickup",label:"Pickup reported",state:"uncertain",detail:"Provider-reported; not verified",timestamp:"2026-10-17T09:00:00Z"},
    {id:"delivery",label:"Arrival pending",state:"pending"},
  ]}/>
</div> }
