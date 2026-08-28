---
name: agentmentor-intent
description: Use only when a proposed change conflicts with a Feature, an accepted ADR, an explicit user goal, a public boundary, or when the user asks for a whole-product direction review. Do not use as a default pre-coding or pre-closeout gate.
---

# AgentMentor Intent

Resolve a real direction conflict using the current context package and explicit user intent.

1. State the conflicting goal, scope, or boundary and cite the concrete source.
2. Return exactly one outcome: `aligned`, `revise-scope`, `needs-user-decision`, or `record-decision`.
3. For `revise-scope`, name the smallest safe scope change. For `needs-user-decision`, ask only the decision that cannot be inferred safely.
4. Route a durable trade-off to `agentmentor-decision`; otherwise continue work without creating an artifact.

Do not repeat context retrieval or perform routine task classification.
