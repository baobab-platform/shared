import { defineConfig, devices } from "@playwright/test"

/**
 * Tests actual generated Storybook (not a mocked React renderer) in Chromium.
 * Visual screenshots are retained for review, not self-approved goldens.
 */
export default defineConfig({
  testDir: "./tests",
  timeout: 30_000,
  fullyParallel: true,
  forbidOnly: Boolean(process.env.CI),
  retries: process.env.CI ? 1 : 0,
  reporter: [["list"], ["html", { outputFolder:"playwright-report", open:"never" }]],
  use: { launchOptions:{args:["--enable-unsafe-swiftshader"]}, baseURL:"http://127.0.0.1:6006", trace:"retain-on-failure" },
  projects: [
    { name:"desktop", use:{ ...devices["Desktop Chrome"], viewport:{width:1440,height:900} } },
    { name:"mobile", use:{ ...devices["Desktop Chrome"], viewport:{width:390,height:844},isMobile:true,hasTouch:true } },
  ],
  webServer: { command:"node scripts/serve-static.mjs",url:"http://127.0.0.1:6006/iframe.html",reuseExistingServer:!process.env.CI,timeout:45_000 },
})
