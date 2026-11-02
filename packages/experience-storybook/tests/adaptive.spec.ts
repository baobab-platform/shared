import { test, expect } from "@playwright/test"
import AxeBuilder from "@axe-core/playwright"

/** BXS-VFA: neutral source-observed theme stress, not estate brand certification. */
const themes = ["nabhold", "zuribeans", "thamani", "baobab-platform"] as const
const viewports = [320, 390, 768, 1024, 1440] as const
const url = (theme:string) =>
  "/iframe.html?id=bxs-foundations--adaptive-conditions&viewMode=story&globals=theme:"+theme

async function assertReflow(page: import("@playwright/test").Page, label:string) {
  const result = await page.evaluate(() => ({
    viewport: document.documentElement.clientWidth,
    scroll: document.documentElement.scrollWidth,
    hasContent: Boolean(document.querySelector("h1")),
  }))
  expect(result.hasContent, label+" must render").toBe(true)
  expect(result.scroll, label+" has unexpected horizontal document scroll").toBeLessThanOrEqual(result.viewport + 1)
}

test("four observed themes preserve semantic content and reflow across five widths", async ({ page }, info) => {
  for (const theme of themes) {
    for (const width of viewports) {
      await page.setViewportSize({width, height:900})
      await page.goto(url(theme))
      await expect(page.getByRole("heading", {name:/Longer regional procurement information/})).toBeVisible()
      await expect(page.getByRole("alert", {name:"Access remains restricted in this example"})).toBeVisible()
      await expect(page.getByText("Documentation review required before proceeding")).toBeVisible()
      const button = page.getByRole("button", {name:/Review procurement quotation with additional/})
      await expect(button).toBeVisible()
      const bounds = await button.boundingBox()
      expect(bounds, theme+" at "+width+"px").not.toBeNull()
      expect(bounds!.x, theme+" button left at "+width).toBeGreaterThanOrEqual(-1)
      expect(bounds!.x + bounds!.width, theme+" button right at "+width).toBeLessThanOrEqual(width+1)
      await assertReflow(page, theme+" "+width+"px")
      if (width === 320 && (theme === "nabhold" || theme === "zuribeans")) {
        await info.attach("vfa-"+theme+"-"+width, {
          body: await page.screenshot({fullPage:true,animations:"disabled"}), contentType:"image/png"
        })
      }
    }
  }
})

test("200% root text-size stress preserves content and action geometry", async ({page}) => {
  for (const theme of themes) {
    await page.setViewportSize({width:320,height:900})
    await page.goto(url(theme))
    await page.evaluate(() => {document.documentElement.style.fontSize="200%"})
    await page.evaluate(() => document.fonts.ready)
    await assertReflow(page, theme+" enlarged text")
    const action=page.getByRole("button",{name:/Review procurement quotation with additional/})
    await expect(action).toBeVisible()
    const box=await action.boundingBox()
    expect(box).not.toBeNull()
    expect(box!.width).toBeLessThanOrEqual(320)
    expect(box!.height).toBeGreaterThanOrEqual(44)
    await expect(page.getByRole("alert",{name:"Access remains restricted in this example"})).toBeVisible()
  }
})

test("forced colours, reduced motion and keyboard focus retain meaning", async ({page})=>{
  await page.emulateMedia({forcedColors:"active",reducedMotion:"reduce"})
  await page.goto(url("nabhold"))
  const button=page.getByRole("button",{name:/Review procurement quotation with additional/})
  await button.focus()
  await expect(button).toBeFocused()
  expect(await button.evaluate(el=>getComputedStyle(el).outlineStyle)).not.toBe("none")
  await expect(page.getByText("Documentation review required before proceeding")).toBeVisible()
  await expect(page.getByRole("alert",{name:"Access remains restricted in this example"})).toBeVisible()
  expect(await page.evaluate(()=>matchMedia("(forced-colors: active)").matches)).toBe(true)
  await assertReflow(page,"forced-colours")
})

test("dark system preference does not silently swap estate identity",async({page})=>{
  await page.emulateMedia({colorScheme:"light"})
  await page.goto(url("zuribeans"))
  const initial=await page.locator(".bxs-story-shell").evaluate(el=>getComputedStyle(el).getPropertyValue("--bx-color-primary").trim())
  expect(initial).toBe("#0f2c24")
  await page.emulateMedia({colorScheme:"dark"})
  const after=await page.locator(".bxs-story-shell").evaluate(el=>getComputedStyle(el).getPropertyValue("--bx-color-primary").trim())
  expect(after).toBe(initial)
  await expect(page.getByRole("alert",{name:"Access remains restricted in this example"})).toBeVisible()
})

test("adaptive foundation is axe-clean at small width and visibly supports focus",async({page})=>{
  await page.setViewportSize({width:320,height:720})
  await page.goto(url("baobab-platform"))
  const action=page.getByRole("button",{name:/Review procurement quotation with additional/})
  await action.focus()
  await expect(action).toBeFocused()
  const result=await new AxeBuilder({page}).withTags(["wcag2a","wcag2aa","wcag21a","wcag21aa","wcag22aa"]).analyze()
  expect(result.violations).toEqual([])
})

test("touch does not require hover-only affordances",async({page},info)=>{
  test.skip(info.project.name !== "mobile","touch interaction is only asserted in mobile project")
  await page.goto(url("nabhold"))
  const disclosure=page.getByText("Read additional source, accuracy and data freshness information")
  await disclosure.tap()
  await expect(page.getByText(/This example is not live tracking/)).toBeVisible()
})
