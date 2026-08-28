---
name: agentmentor-decision
description: Use when an engineering choice changes a future-facing architecture, module or public boundary, cost, risk, data contract, or rejected alternative and the reason must survive beyond the current task. Create or update a vNext ADR only when the decision is stable enough to record.
---

# AgentMentor Decision

Record only durable choices that future work could reasonably reopen.

1. Confirm the decision boundary, alternatives, and consequences are concrete.
2. Create or update `docs/decisions/ADR-xxx-*.md` from `assets/templates/ADR.md`.
3. Link the owning Feature when one exists. State the rejected options and a falsifiable `Revisit When` condition.
4. Run `python <skill-root>/scripts/knowledge_check.py --root <project-root> --docs-path docs --strict` after editing the artifact.

Do not create an ADR for implementation details, task planning, or a reversible local choice.
