import {fileURLToPath} from "node:url"
import type { StorybookConfig } from "@storybook/react-vite"

/** Versioned UI package stories: no tenant, IAM or domain authority. */
const config: StorybookConfig = {
  stories: ["../src/**/*.stories.@(ts|tsx)"],
  addons: ["@storybook/addon-a11y", "@storybook/addon-docs"],
  framework: "@storybook/react-vite",
  staticDirs:[{from:fileURLToPath(new URL("../node_modules/maplibre-gl/dist/",import.meta.url)),to:"/maplibre-6.14.0"}],
}
export default config
