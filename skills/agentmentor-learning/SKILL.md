---
name: agentmentor-learning
description: Use when real behavior conflicts with a Feature specification, a regression recurs, a patch chain repeats, or a failure pattern has a reusable root cause and concrete prevention. Decide whether to update the Feature, record a Lesson, update an ADR, or only fix the issue.
---

# AgentMentor Learning

Turn a durable engineering signal into the smallest appropriate memory change.

1. Separate observed signal, root cause, and prevention. Do not promote a guess into a Lesson.
2. Choose one outcome: `update-feature`, `create-lesson`, `update-decision`, or `fix-only`.
3. Use `assets/templates/LESSON.md` only when there is a real case and executable protection; update the Feature when its specification is wrong or incomplete.
4. Run the strict knowledge check after changing a knowledge artifact.

Do not perform a ceremonial retrospective for ordinary one-off mistakes.
