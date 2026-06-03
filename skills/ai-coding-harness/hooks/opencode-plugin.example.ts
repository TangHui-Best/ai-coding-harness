import type { Plugin } from "@opencode-ai/plugin"

type HarnessHookEvent = "post-tool-use" | "stop" | "session-start" | "pre-compact"

type HarnessHookOutput = {
  decision?: "allow" | "block"
  reason?: string
  additional_context?: string
}

export const HarnessHookPlugin: Plugin = async ({ $, client, directory }) => {
  const skillRoot = process.env.HARNESS_SKILL_ROOT
  if (!skillRoot) {
    return {}
  }

  const runHarnessHook = async (event: HarnessHookEvent, payload: unknown): Promise<HarnessHookOutput> => {
    const result = await $`python ${
      skillRoot + "/hooks/harness_hook.py"
    } --event ${event} --platform opencode --root ${directory}`
      .stdin(JSON.stringify(payload))
      .quiet()
      .catch((error) => {
        console.warn(`Harness ${event} hook failed open: ${error}`)
        return undefined
      })

    if (!result) {
      return {}
    }

    let output: HarnessHookOutput
    try {
      output = JSON.parse(result.stdout.toString().trim() || "{}")
    } catch (error) {
      console.warn(`Harness ${event} hook returned invalid JSON and failed open: ${error}`)
      return {}
    }

    if (output.decision === "block") {
      throw new Error(output.reason || "Harness hook blocked this action.")
    }
    return output
  }

  const latestAssistantMessage = async (sessionID: string): Promise<string> => {
    const result = await client.session
      .messages({
        path: { id: sessionID },
        query: { directory, limit: 20 },
      })
      .catch((error) => {
        console.warn(`Harness stop hook could not read OpenCode session messages and failed open: ${error}`)
        return undefined
      })

    const messages = result?.data || []
    for (const message of [...messages].reverse()) {
      const { info, parts } = message
      if (info.role !== "assistant") {
        continue
      }

      const text = parts
        .filter((part) => part.type === "text" && typeof part.text === "string")
        .map((part) => part.text)
        .join("\n")
        .trim()

      if (text) {
        return text
      }
    }
    return ""
  }

  return {
    event: async (input) => {
      if (input.event.type !== "session.idle") {
        return
      }
      const sessionID = input.event.properties.sessionID
      await runHarnessHook("stop", {
        ...input.event.properties,
        session_id: sessionID,
        hook_event_name: input.event.type,
        last_assistant_message: await latestAssistantMessage(sessionID),
      })
    },
    "experimental.session.compacting": async (input, output) => {
      const payload = {
        ...input,
        session_id: input.sessionID,
        source: "compact",
        hook_event_name: "experimental.session.compacting",
      }

      await runHarnessHook("pre-compact", payload)
      const recovery = await runHarnessHook("session-start", payload)
      if (recovery.additional_context) {
        output.context.push(recovery.additional_context)
      }
    },
  }
}
