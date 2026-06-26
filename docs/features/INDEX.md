# Feature Index

这个索引用于粗召回，不是 AgentMentor knowledge artifact。它只帮助 Agent 在打开 Feature 正文之前做第一层候选判断；真正的能力边界、验收门禁、证据和恢复信息仍以具体 Feature 页面为准。

维护规则：

- 新增 Feature、重命名 Feature、拆分/合并 Feature 时更新。
- `Owned Paths` 或 `Trigger Terms` 明显失真时更新。
- Feature 被 archived、deprecated、superseded 时更新状态或读法。
- 普通 Feature 正文补充、Evidence 增加、Patch History 增加时默认不更新本索引。

| Feature | Domain | Trigger Terms | Owned Paths | Read When |
| --- | --- | --- | --- | --- |
| [F001 closeout entry anchor validation](F001-closeout-entry-anchor-validation.md) | closeout, evidence gate | completion claim, closeout, exit gate, evidence validation | `skills/knowledge-capture/`, closeout scripts | 任务涉及完成声明、closeout 入口、Evidence gate 或完成前校验时读取。 |
| [F002 canonical harness artifact placement](F002-canonical-harness-artifact-placement.md) | artifact placement | docs location, canonical path, superpowers specs, feature refs | `docs/features/`, `docs/decisions/`, `docs/lessons/`, `docs/evidence/` | 任务涉及 AgentMentor 文档放置、Superpowers spec/plan 与 AgentMentor artifact 边界、路径归属时读取。 |
| [F003 optional harness hook runtime](F003-optional-harness-hook-runtime.md) | hook runtime | optional hooks, stop hook, session start, fail open | `skills/using-agentmentor/hooks/`, `hooks.json` | 任务涉及可选 hook runtime、Stop/SessionStart/PreCompact 行为或安装示例时读取。 |
| [F004 delegation gate three outcomes](F004-delegation-gate-three-outcomes.md) | delegation gate | delegate, single agent, blocked, subagent decision | `skills/delegation-gate/`, start-gate delegation wording | 任务涉及是否派 subagent、Delegation Gate 输出或三态决策时读取。 |
| [F005 session recovery hooks](F005-session-recovery-hooks.md) | session recovery | compact, pre-compact, handoff, recovery snapshot | `.agentmentor/session-recovery/`, hook diagnostics | 任务涉及上下文压缩、会话恢复、handoff 或 recovery hook 证据时读取。 |
| [F006 skill naming compatibility](F006-skill-naming-compatibility.md) | naming compatibility | AgentMentor rename, legacy harness slugs, compatibility | `skills/`, skill metadata checks | 任务涉及 AgentMentor 命名迁移、legacy harness slug 或兼容性判断时读取。 |
| [F007 agentmentor semantic skill routing](F007-agentmentor-semantic-skill-routing.md) | semantic routing | skill routing, semantic workflow names, AgentMentor entrypoint | `skills/using-agentmentor/`, routing tests | 任务涉及 AgentMentor skill 路由、入口命名或语义 workflow slug 时读取。 |
| [F008 spec drift guardrails](F008-spec-drift-guardrails.md) | spec drift | stale spec, acceptance drift, spec reality conflict | `skills/spec-drift/`, routing rules | 任务涉及 spec 与现实冲突、验收标准漂移或过期规格判断时读取。 |
| [F009 feature intake governance](F009-feature-intake-governance.md) | feature governance | Feature intake, Feature template, Acceptance Map, Feature Index, recall, recall governance | `templates/FEATURE.md`, `skills/using-agentmentor/assets/templates/FEATURE.md`, `docs/features/INDEX.md` | 任务涉及 Feature 结构、命名、召回入口、Feature Intake、Acceptance Map、Feature Index 治理或 Feature 模板时读取。 |
| [F010 goal driven feature flow](F010-goal-driven-feature-flow.md) | goal-driven flow | goal boundary, feature approval, empty approval guard | `skills/using-agentmentor/SKILL.md`, start/capture gate wording | 任务涉及 Goal 授权边界、是否需要逐 Feature 审批、空审批防护时读取。 |
