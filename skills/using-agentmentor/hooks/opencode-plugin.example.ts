import type { Plugin } from "@opencode-ai/plugin"

type AgentMentorHookEvent = "post-tool-use" | "stop"

type AgentMentorHookOutput = {
  decision?: "allow" | "block"
  reason?: string
}

export const AgentMentorHookPlugin: Plugin = async ({ $, client, directory }) => {
  const skillRoot = process.env.AGENTMENTOR_SKILL_ROOT
  if (!skillRoot) {
    return {}
  }

  const runAgentMentorHook = async (event: AgentMentorHookEvent, payload: unknown): Promise<AgentMentorHookOutput> => {
    const result = await $`python ${
      skillRoot + "/hooks/agentmentor_hook.py"
    } --event ${event} --platform opencode --root ${directory}`
      .stdin(JSON.stringify(payload))
      .quiet()
      .catch((error) => {
        console.warn(`AgentMentor ${event} hook failed open: ${error}`)
        return undefined
      })

    if (!result) {
      return {}
    }

    let output: AgentMentorHookOutput
    try {
      output = JSON.parse(result.stdout.toString().trim() || "{}")
    } catch (error) {
      console.warn(`AgentMentor ${event} hook returned invalid JSON and failed open: ${error}`)
      return {}
    }

    if (output.decision === "block") {
      throw new Error(output.reason || "AgentMentor hook blocked this action.")
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
        console.warn(`AgentMentor stop hook could not read OpenCode session messages and failed open: ${error}`)
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
      await runAgentMentorHook("stop", {
        ...input.event.properties,
        session_id: sessionID,
        hook_event_name: input.event.type,
        last_assistant_message: await latestAssistantMessage(sessionID),
      })
    },
  }
}
