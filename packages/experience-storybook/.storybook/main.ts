import type { StorybookConfig } from "@storybook/react-vite"

/** Versioned UI package stories: no tenant, IAM or domain authority. */
const config: StorybookConfig = {
  stories: ["../src/**/*.stories.@(ts|tsx)"],
  addons: ["@storybook/addon-a11y", "@storybook/addon-docs"],
  framework: "@storybook/react-vite",
}
export default config
