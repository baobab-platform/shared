import {test,expect} from "@playwright/test"
import AxeBuilder from "@axe-core/playwright"

test("optional map renders real WebGL after activation and cleans up on revocation",async({page})=>{
  const external:string[]=[]
  page.on("request",request=>{if(/^https?:/.test(request.url())&&new URL(request.url()).hostname!=="127.0.0.1")external.push(request.url())})
  await page.goto("/iframe.html?id=bxs-map--evidence&viewMode=story")
  await expect(page.getByRole("list",{name:"Authorised location evidence"})).toContainText("Carrier-reported position")
  await expect(page.locator(".maplibregl-canvas")).toHaveCount(0)
  await page.getByRole("button",{name:"Enable interactive map"}).click()
  await expect(page.locator(".maplibregl-canvas")).toBeVisible({timeout:20000})
  await expect(page.getByRole("status")).toContainText("Map ready")
  const {violations}=await new AxeBuilder({page}).withTags(["wcag2a","wcag2aa","wcag21aa","wcag22aa"]).analyze()
  expect(violations).toEqual([])
  await page.getByRole("button",{name:"Synthetic carrier report",exact:true}).focus()
  await page.keyboard.press("Enter")
  await expect(page.getByRole("button",{name:"Synthetic carrier report",exact:true})).toHaveAttribute("aria-pressed","true")
  await page.getByRole("button",{name:"Revoke synthetic visibility"}).click()
  await expect(page.getByRole("alert")).toContainText("access revoked")
  await expect(page.locator(".maplibregl-canvas")).toHaveCount(0)
  await expect(page.getByRole("list",{name:"Authorised location evidence"})).toHaveCount(0)
  expect(external).toEqual([])
})
