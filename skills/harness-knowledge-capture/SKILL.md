---
name: harness-knowledge-capture
description: MUST use before claiming engineering work is complete, fixed, verified, reviewed, ready to commit, ready for PR, ready for handoff, or safely closed; also use when Start Gate or project risk requires durable pre-work memory such as Feature state, specs, plans, ADRs, Backlog, handoff anchors, Evidence, Lessons, incident records, patch-churn review, repeated-fix trajectory, 知识沉淀, 经验沉淀, 完成声明, 收尾, 反复补丁, 归零审视, 准备提交, 准备 PR, or 交接.
---

# Harness Knowledge Capture

## Purpose

Use this skill to turn required pre-work, completed engineering work, or handoff state into durable project memory without creating documentation tax.

Core boundary:

```text
Skill is the knowledge-capture entry point.
Scripts and gates are the reliability layer.
```

This skill does not build the whole Harness. Use it to capture the smallest durable knowledge artifact before work when Start Gate requires an anchor, or after work, review, handoff, or incident learning.

Do not write documents just to look disciplined. Capture only the smallest artifact that prevents future confusion, repeated mistakes, or unverifiable completion claims.

Treat Markdown documents as the source of truth. Treat search indexes, summaries, and retrieval databases as compiled outputs.

## Language Policy

Prefer Chinese for human-written prose in Feature, ADR, Lesson, Evidence, spec, plan, Backlog, and handoff documents.

Keep machine-facing structure stable in English:

- YAML frontmatter keys and enum values.
- Required Markdown section headings checked by scripts.
- Code identifiers, commands, logs, paths, APIs, and quoted source text.

When an artifact is intended for external or open-source readers, add a short English summary instead of duplicating the whole document.

## Trigger Discipline

If you are about to say work is done, complete, verified, reviewed, ready to commit, ready for PR, ready for handoff, or safely closed, stop and use this skill first.

This skill may conclude "no formal artifact needed." The required behavior is checking Evidence, ADR, Lesson, Feature, Backlog, and Handoff status before completion claims.

If this skill has not produced a `Completion claim allowed` verdict, do not use completion language. Say `implementation done, harness closeout pending` and finish the missing closeout work or report the blocker.

## Workflow

1. Read the current task, changed files, verification output, user constraints, `AGENTS.md`, `docs/BACKLOG.md`, active Feature pages, recent commits, and existing ADR/Lesson/Evidence docs when present.
2. Identify the smallest knowledge boundary that matters: active work state, handoff, Feature delivery, decision, failure mode, evidence, or none.
3. Use the Artifact Decision Matrix, then run the trigger checklist below.
4. Create or update only the lightest durable artifact that fits the risk.
5. Link ADR, Lesson, and Evidence artifacts from the Feature page when a Feature is involved.
6. Update `docs/BACKLOG.md` or a handoff note when active work state changes.
7. Before marking work complete, run the Completion Closeout Gate below.
8. Run the bundled `using-harness/scripts/knowledge_check.py` against the target docs directory when dedicated Harness artifacts were created or updated. If the project vendors its own copy, that copy may be used instead.
9. Run the bundled `using-harness/scripts/harness_closeout_check.py` against the final closeout block before claiming completion. If the project vendors its own copy, that copy may be used instead.
10. Report Backlog/Handoff, Plan lifecycle, Readiness, Vision Gate Exit, ADR, Lesson, Evidence, Feature, Check, closeout verdict, and completion-claim permission explicitly.

## Integration

Use this skill as the closeout around other workflow skills:

| Upstream event | Knowledge-capture action |
| --- | --- |
| Start Gate requires Feature/spec/plan/ADR | Create or update only that pre-work anchor before implementation starts. |
| Brainstorming writes a spec | Link spec from the Feature page; add Feature linkback when ownership is clear. |
| Planning writes a plan | Link plan from the Feature page; update next step and BACKLOG if active work changed. |
| Implementation or verification finishes | Record Evidence in the lightest durable place. |
| Code review or PR preparation starts | Check Feature, ADR, Lesson, Evidence, and handoff status before claiming readiness. |
| Bug, incident, repeated failure, or repeated patch chain is resolved | Confirm Feature attribution, update Patch History when applicable, and consider Lesson, Evidence, Patch Churn Review, and stronger gates before closing. |
| Architecture or process decision is made | Consider ADR before the rationale is lost. |

Use `harness-change-narrative` as the change-level narrative layer when commit, PR, merge, release, handoff, non-trivial bugfix, rejected-option, or history-aware context needs to be explained first.

## Artifact Decision Matrix

Choose the smallest durable carrier that matches the knowledge boundary:

| Boundary | Preferred carrier | Rule |
| --- | --- | --- |
| Current active work, next step, recovery context | `docs/BACKLOG.md` or handoff note | Update only when future sessions need this state. |
| Delivery boundary, Vision Anchor, status, acceptance criteria, related links | Feature page | Create or update when the task advances a Feature or when non-trivial work needs a durable original-intent anchor. |
| Detailed requirement or scope | Spec linked from Feature | Link it; do not copy the spec into the Feature page. |
| Execution route or task breakdown | Plan linked from Feature | Link it; update Feature status and next step if they changed. |
| Decision conversation, issue thread, review thread | Discussion linked from Feature | Link it when it explains current state or open questions. |
| Defect reproduction, impact, expected behavior | Bug report linked from Feature | Link it; create a Lesson only if the failure mode can recur. |
| Exploration before a decision | Research linked from Feature or ADR | Link it; create an ADR only when a decision is made. |
| Why this option, why not alternatives | ADR | Create a dedicated ADR when the decision will be questioned later. |
| Recurring failure mode and protection | Lesson | Create a dedicated Lesson when caution must become a guardrail. |
| Proof of completion | Evidence location or Evidence doc | Record proof every time; create an Evidence doc only when retrieval or audit matters. |

Feature pages are indexes, not containers for all material. Prefer linking spec, plan, discussion, bug report, research, and detailed Vision Gate Evidence over copying their content. Keep the Feature page's Vision Anchor short enough to remain a stable source for later Exit Gates.

## Trigger Checklist

### Backlog or Handoff

Update `docs/BACKLOG.md` or write a handoff note when the task changes current active work state.

Trigger on:

- A Feature starts, pauses, unblocks, ships, or changes next step.
- Important recovery context would be lost in a new session.
- There are unresolved risks, open decisions, or follow-up commands.
- The work spans multiple sessions, agents, or collaborators.

Do not update BACKLOG for a one-off low-risk task with no future recovery value.

### ADR

Write an ADR when the task makes a decision future agents are likely to question.

Trigger on:

- High-cost rollback technical choices.
- Changes to module boundaries, data models, or interface contracts.
- New frameworks, infrastructure, storage, or messaging mechanisms.
- Rejected alternatives that are likely to be proposed again.
- Decisions affecting multiple Features or long-term evolution.
- Security, performance, cost, compliance, or operational tradeoffs.

Decision sentence:

```text
If a future person or agent is likely to ask "why did we choose this?", write an ADR.
```

### Lesson

Write a Lesson when a failure mode can recur and needs a protection mechanism.

Trigger on:

- Similar issues may recur or have already recurred.
- A bug exposes a process gap, missing rule, or weak gate.
- Future agents are likely to repeat the same error.
- Code changes alone cannot fully prevent recurrence.
- A Feature required repeated patches because the initial abstraction, boundary, invariant, or rule strategy was wrong or incomplete.
- The only post-fix guidance would otherwise be "be careful next time."
- The fix requires tests, gates, CI, permissions, docs, or workflow rules.

Decision sentence:

```text
If the fix ends with "be careful next time", write a Lesson and turn caution into protection.
```

### Evidence

Evidence is required as proof for every completion claim. A dedicated Evidence document is optional.

Choose an Evidence level before claiming readiness or completion:

| Level | Use when | Minimum proof |
| --- | --- | --- |
| `quick` | Tiny or routine low-risk work. | Final response, commit message, manual inspection note, or the smallest relevant command. |
| `standard` | Non-trivial feature, bugfix, refactor, or user-visible behavior. | Tests, build or lint when available, key workflow check, and a concise diff or behavior summary. |
| `exhaustive` | High-risk release, architecture, data model, security, migration, major UX, RPA/browser flow, or external contract. | Standard proof plus E2E/browser/screenshot/trace when relevant, reviewer record, rollback note, and dedicated Evidence when retrieval or audit matters. |

Evidence should include final outcome, command output, environment or diff context, and trace or trajectory when relevant.

For patch churn, Evidence must include the fix trajectory: what each relevant patch exposed, which shared root cause was found or ruled out, why another local patch is sufficient or insufficient, and whether the final protection moved upstream to the right invariant, contract, or boundary.

Do not create a separate QA workflow by default. Treat QA as the risk-adjusted Evidence question: "what proof is enough for this task?" If the requested transition is review, release, or handoff, summarize the chosen level through `harness-readiness-dashboard`.

### Feature Page

Create or update a Feature page when:

- A Feature status changes.
- A spec, plan, discussion, bug report, research, ADR, Lesson, or Evidence artifact is added.
- Acceptance criteria change.
- New constraints are discovered.
- The task advances a Feature.
- Non-trivial work would otherwise rely on chat history as the only Vision Gate source.
- A bugfix or follow-up patch changes a Feature after it was considered done or accepted; record it in `## Patch History` on the original Feature with a patch id such as `F010.1`.

Feature pages express delivery boundaries and the durable Vision Anchor for the delivery. ADRs express decision boundaries. Lessons express failure-mode boundaries. Evidence expresses proof of completion.

Patch History rows are not new Feature documents. They are follow-up fix records on the original Feature. When a Feature reaches 3 Patch History rows, add `## Patch Churn Review` before another patch can be cleanly closed.

### Bugfix Attribution And Patch History

For every non-tiny bugfix, record the attribution result before allowing completion language:

- `existing Feature <id>`: update that Feature's `## Patch History` when the bug changes a completed, accepted, or previously delivered behavior.
- `none found after retrieval`: record the negative retrieval result in Evidence or the final closeout; create a new Feature only when the bugfix itself needs a durable Vision Anchor.
- `not triggered`: use only for tiny local fixes where project memory cannot change the outcome, and state why.
- `ambiguous`: keep completion blocked or conditional until the owner is clarified, unless the claim is explicitly limited to investigation.

Patch History is the counter that makes the 3+ patch-churn threshold observable. Do not hide completed follow-up fixes only in a final response, commit message, or PR body when an existing Feature owns the behavior.

When updating Patch History, include the symptom and root cause or suspected root cause clearly enough that `harness-incident-learning` can later group repeated failures without replaying the whole conversation.

### Vision Anchor

Capture the smallest durable statement that lets future Entry and Exit Gates judge alignment without replaying the chat transcript. Prefer the Feature page when a Feature exists or should exist. Use a linked spec when the detailed requirement already lives there, and summarize only the anchor on the Feature page.

Include:

- Original request or source link.
- User pain point or engineering problem.
- Desired outcome or success shape.
- Non-goals or scope boundaries.
- Exit Gate source: the artifact later reviewers should compare against.

Do not create a standalone Vision Gate document by default. Record lightweight Entry Gate results in the Feature Evidence section. Create a dedicated Evidence record only when review, release, handoff, audit, or multi-agent recovery needs the full Gate report.

## Completion Closeout Gate

Run this gate before claiming a Feature, non-trivial change, review, release, handoff, or completion is ready. Do not treat passing tests as enough.

| Check | Required action |
| --- | --- |
| Plan lifecycle | If linked plans were executed, set them to `completed`, archive them, or explicitly record why they remain `active`. A completed Feature must not silently link to an active executed plan. |
| Evidence validation | Record verification commands and results. When Harness artifacts changed, Evidence must include the `knowledge_check.py` command path used and actual result. |
| Readiness | For non-trivial work, use `harness-readiness-dashboard` before review, release, handoff, or completion claims. If not needed, state why. |
| Vision Gate Exit | For non-trivial, user-facing, architecture, scope-sensitive, or behavior-changing work, use `harness-vision-gate` in Exit Gate mode before done/acceptance/handoff. If not needed, state why. |
| Patch Churn Review | If a Feature has 3+ `## Patch History` rows, `Fxxx.n` patch slices, or equivalent repeated validation misses, record whether Patch Churn Review was not triggered, passed, routed to Vision Gate, routed to ADR, routed to Lesson, or blocked. |
| Bugfix attribution | For non-tiny bugfixes, record whether retrieval found an existing Feature, no Feature, or an ambiguous owner; if an existing completed Feature owns the behavior, update Patch History before closeout. |
| Feature and Backlog consistency | Ensure Feature status, Backlog section, Evidence links, ADR/Lesson links, and next step describe the same state. |
| Completion verdict | Set `Closeout verdict` to `pass`, `conditional`, or `blocked`, then set `Completion claim allowed` to `yes` only when no required closeout item is missing. |

If any required closeout item is missing, choose one:

- Complete the missing item now.
- Mark readiness as blocked or conditional and name the blocker.
- Keep the Feature active instead of calling it completed.

Use these verdicts:

| Verdict | Meaning | Completion language |
| --- | --- | --- |
| `pass` | Required closeout items are satisfied for the task risk level. | Completion/readiness claims are allowed. |
| `conditional` | Work can move to a named next stage with explicit residual risk. | Use conditional wording only; do not say release-ready unless release is the permitted stage. |
| `blocked` | Required Evidence, gate, decision, artifact validation, or recovery context is missing. | Completion/readiness claims are not allowed. |

When a formal artifact is not needed, still mark the category `not triggered` and explain why. Lightweight is allowed; invisible is not.

## Artifact Placement

Prefer these paths unless the project already has a stronger convention:

```text
docs/BACKLOG.md
docs/features/Fxxx-slug.md
docs/decisions/ADR-xxx-slug.md
docs/lessons/LL-xxx-slug.md
docs/evidence/EV-xxx-slug.md
```

## Templates

Copy the matching bundled template from `using-harness/assets/templates/` and fill every required field and section. If the project vendors templates, prefer the project copy only when it is intentionally current with the Harness suite.

- Feature: `using-harness/assets/templates/FEATURE.md`
- ADR: `using-harness/assets/templates/ADR.md`
- Lesson: `using-harness/assets/templates/LESSON.md`
- Evidence: `using-harness/assets/templates/EVIDENCE.md`

Use stable IDs:

- Feature: `F001`
- ADR: `ADR-001`
- Lesson: `LL-001`
- Evidence: `EV-001`

Keep titles specific enough to scan in search results.

## Check Script

Run the bundled validator from the installed `using-harness` skill:

```bash
python <skills-root>/using-harness/scripts/knowledge_check.py --root <repo> --docs-path docs
```

Optional:

```bash
python <skills-root>/using-harness/scripts/knowledge_check.py --root <repo> --docs-path docs --strict
python <skills-root>/using-harness/scripts/knowledge_check.py --root <repo> --docs-path docs --all-markdown --strict
```

The script checks Harness knowledge artifacts for Markdown frontmatter, allowed `doc_kind`, required fields, required sections, Feature ID/file-name consistency, Feature references, Feature links, and missing Feature backlinks for ADR/Lesson/Evidence documents that declare Feature relationships.

When available, validate the closeout block itself:

```bash
python <skills-root>/using-harness/scripts/harness_closeout_check.py --file <closeout.md>
```

Use this for PR bodies, handoff notes, Evidence notes, or temporary closeout files that contain the final Harness status block. The script is a structural guardrail; it does not replace judgment about whether the selected Evidence level is sufficient.

## Final Response Contract

Always include this knowledge-capture status before claiming readiness or completion:

```text
Closeout verdict: pass / conditional / blocked
Completion claim allowed: yes / no
Backlog/Handoff: not triggered / updated ...
Plan lifecycle: not triggered / updated ... / intentionally active because ...
Readiness: not triggered / dashboard pass / dashboard conditional ... / blocked ...
Vision Gate Exit: not triggered / pass / needs follow-up / blocked ...
Patch Churn Review: not triggered / pass / routed to Vision Gate / routed to ADR / routed to Lesson / blocked ...
Bugfix attribution: not triggered / existing Feature <id> updated / none found after retrieval / ambiguous ... / blocked ...
ADR: not triggered / written ADR-xxx
Lesson: not triggered / written LL-xxx
Evidence: recorded in ...
Evidence level: quick / standard / exhaustive
Feature: updated ... / not triggered
Check: passed / not run because ... / failed because ...
```

If a trigger was deliberately not satisfied, explain the reason briefly. Do not leave a category blank.

`Completion claim allowed: yes` is valid only when:

- `Closeout verdict` is `pass`, or the claim is explicitly limited to the conditional stage.
- Evidence location and Evidence level are present.
- Required verification commands and outcomes are recorded in Evidence or the final response.
- `Check` records the actual `knowledge_check.py` result when Harness artifacts were created or updated.
- Required Readiness and Vision Gate Exit checks are either satisfied or explicitly not triggered with a reason.
- Non-tiny bugfixes have a Bugfix attribution status, and existing completed Feature owners have an updated Patch History row when applicable.
- Features with 3+ Patch History rows include a non-empty `## Patch Churn Review`.

## Common Mistakes

| Mistake | Correction |
| --- | --- |
| Claiming work is done without Evidence status. | Record where Evidence lives, even if it is only the final response. |
| Saying a spec or plan means Harness is complete. | Treat specs and plans as inputs; run Exit Gate before completion claims. |
| Omitting a category because it did not need an artifact. | Mark it `not triggered` with a reason. |
| Creating a new artifact when an existing one should be updated. | Prefer updating current Feature, ADR, Lesson, or Evidence records. |
| Fixing a bug without updating the owning Feature. | Attribute non-tiny bugfixes first; if the behavior belongs to a completed Feature, add a Patch History row. |
| Copying spec/plan content into a Feature page. | Link source artifacts and summarize only the status or next step. |
| Writing a Lesson that only says to be careful. | Turn caution into a test, gate, CI check, permission rule, or skill. |
| Writing an ADR without rejected alternatives or tradeoffs. | Include alternatives and consequences. |
| Treating a search index as source of truth. | Markdown source artifacts own truth; indexes are compiled outputs. |
