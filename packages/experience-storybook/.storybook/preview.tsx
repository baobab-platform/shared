import type { Preview } from "@storybook/react-vite"
import "@baobab-platform/experience-tokens/base.css"
import "@baobab-platform/experience-tokens/themes/nabhold.css"
import "@baobab-platform/experience-tokens/themes/zuribeans.css"
import "@baobab-platform/experience-tokens/themes/thamani.css"
import "@baobab-platform/experience-tokens/themes/baobab-platform.css"
import "@baobab-platform/experience-ui/styles.css"
import "./storybook.css"

/* Local canvas theming does not overwrite the consumer's document root. */
const preview: Preview = {
  initialGlobals: { theme: "nabhold" },
  globalTypes: {
    theme: {
      description: "Source-observed estate theme; consumer approval pending",
      toolbar: {
        icon: "paintbrush",
        dynamicTitle: true,
        items: [
          { value: "nabhold", title: "Nabhold" },
          { value: "zuribeans", title: "ZuriBeans" },
          { value: "thamani", title: "Thamani legacy (not approved)" },
          { value: "baobab-platform", title: "Baobab CP" },
        ],
      },
    },
  },
  decorators: [
    (Story, context) => (
      <div data-bx-theme={String(context.globals.theme || "nabhold")} className="bxs-story-shell">
        <Story />
      </div>
    ),
  ],
  parameters: { a11y: { test: "error" }, layout: "fullscreen" },
}
export default preview
