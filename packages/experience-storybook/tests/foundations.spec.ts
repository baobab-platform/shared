import { test, expect } from "@playwright/test"
import AxeBuilder from "@axe-core/playwright"

const story=(id:string,theme="nabhold")=>
  "/iframe.html?id=bxs-foundations--"+id+"&viewMode=story&globals=theme:"+theme

test("Base UI action is keyboard operable and updates local demonstration state",async ({page})=>{
  await page.goto(story("action"))
  const action=page.getByRole("button",{name:"Review proposal"})
  await expect(action).toBeVisible()
  await action.focus()
  await expect(action).toBeFocused()
  await page.keyboard.press("Enter")
  await expect(page.getByRole("status",{name:"Local click count"})).toHaveText("1")
})
test("native disclosure expands with Enter and preserves readable text",async ({page})=>{
  await page.goto(story("native-disclosure"))
  const trigger=page.getByText("Source and accuracy")
  await trigger.focus()
  await page.keyboard.press("Enter")
  await expect(page.getByText(/An estimate is never live GPS/)).toBeVisible()
})
test("pending controls deny activation and reveal busy status",async ({page})=>{
  await page.goto(story("pending"))
  const button=page.getByRole("button",{name:"Waiting for confirmation"})
  await expect(button).toBeDisabled()
  await expect(button).toHaveAttribute("aria-busy","true")
})
test("all primary foundation stories meet automated WCAG 2.2 AA",async ({page})=>{
  for(const id of ["action","pending","breadcrumbs","native-disclosure","restricted","milestones"]){
    await page.goto(story(id))
    await expect(page.locator("#storybook-root")).not.toBeEmpty()
    const {violations}=await new AxeBuilder({page}).withTags(["wcag2a","wcag2aa","wcag21a","wcag21aa","wcag22aa"]).analyze()
    expect(violations,id+": "+JSON.stringify(violations)).toEqual([])
  }
})
test("approved source-observed semantic styles are responsive and honour reduced motion",async ({page},testInfo)=>{
  await page.goto(story("action","nabhold"))
  const button=page.getByRole("button",{name:"Review proposal"})
  await expect(button).toHaveCSS("background-color","rgb(252, 163, 0)")
  const rectangle=await button.boundingBox()
  expect(rectangle).not.toBeNull()
  expect(rectangle!.x).toBeGreaterThanOrEqual(0)
  expect(rectangle!.x+rectangle!.width).toBeLessThanOrEqual(page.viewportSize()!.width)
  await page.emulateMedia({reducedMotion:"reduce"})
  await expect(button).toHaveCSS("transition-duration","0s")
  await testInfo.attach("theme-and-viewport",{body:await page.screenshot({animations:"disabled",fullPage:true}),contentType:"image/png"})
  await page.goto(story("action","baobab-platform"))
  await expect(page.getByRole("button",{name:"Review proposal"})).toHaveCSS("background-color","rgb(31, 95, 63)")
})
