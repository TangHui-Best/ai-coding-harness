import type { Plugin } from "@opencode-ai/plugin"

export const HarnessHookPlugin: Plugin = async ({ $, directory }) => {
  const skillRoot = process.env.HARNESS_SKILL_ROOT
  if (!skillRoot) {
    return {}
  }

  const runHarnessHook = async (event: "post-tool-use" | "stop" | "session-start" | "pre-compact", payload: unknown) => {
    const result =
      await $`python ${skillRoot + "/hooks/harness_hook.py"} --event ${event} --platform opencode --root ${directory}`.stdin(
        JSON.stringify(payload),
      ).quiet()

    const output = JSON.parse(result.stdout.toString() || "{}")
    if (output.decision === "block") {
      throw new Error(output.reason || "Harness hook blocked this action.")
    }
  }

  return {
    "session.created": async (input) => {
      await runHarnessHook("session-start", input)
    },
    "experimental.session.compacting": async (input) => {
      await runHarnessHook("pre-compact", input)
    },
    "session.idle": async (input) => {
      await runHarnessHook("stop", input)
    },
  }
}
