---
id: ADR-007
doc_kind: adr
status: accepted
scope: project
feature_refs: [docs/features/F006-skill-naming-compatibility.md]
decision_area: harness-skill-naming
created: 2026-06-03
updated: 2026-06-03
---

# ADR-007: AI Coding Harness Breaking Skill Rename

## Context

`harness` 是工程领域常见词，很多项目会把测试夹具、评测容器、运行编排或业务内治理能力命名为 harness。旧 skill slug 使用 `using-harness` 和 `harness-*`，在单一项目内短期可读，但放到多个真实项目后会出现概念冲突：用户或 Agent 说“检查 harness”时，可能指项目内部 test harness，也可能指 AI Coding Harness 的 Start Gate、Evidence、ADR 或 closeout 流程。

最初的保守方案是保留旧 slug 兼容并只约束未来新增命名。但用户确认当前优先目标是概念清晰，接受卸载本机旧 skill 后重新安装新版本，因此兼容成本不再是主要约束。

## Decision

正式系统名统一为 `AI Coding Harness`。在面向用户和未来文档时，第一次出现应使用全称；`Harness` 只能作为已经定义后的短称。

硬切重命名公开 skill slug：

```text
using-harness -> ai-coding-harness
harness-*     -> ai-coding-harness-*
```

不保留 wrapper，不继续支持旧 slug 兼容。`skill_metadata_check.py` 对 `using-harness` 和裸 `harness-*` skill slug 报错。本机安装需要先删除旧 skill 目录，再安装新版本。

内部脚本文件名例如 `harness_hook.py`、`harness_closeout_check.py` 暂不重命名，因为它们不是公开 skill slug，且重命名会扩大 hook runtime 风险。

## Decision Boundary

### Applies To

- Public AgentMentor skill slugs and user-facing suite naming during the F006 transition.
- Validator rules rejecting legacy `using-harness` and bare `harness-*` skill slugs.
- Local install guidance for removing old skill directories during the breaking rename.

### Does Not Apply To

- Historical Evidence/ADR text that records the old naming as fact.
- Internal script filenames that were intentionally left unchanged in this ADR.
- The later AgentMentor semantic routing decision in ADR-008, which supersedes the public naming direction.

## Rejected Options

- 保留旧 slug 兼容：拒绝。它降低短期安装风险，但会长期保留同一概念冲突，且用户已经明确接受本机卸载重装。
- 新增一整套 wrapper skill：拒绝。wrapper 会让 skill 列表翻倍，继续制造触发歧义，与“不要兼容”的用户决策相反。
- 继续保持裸 `harness-*` 扩张：拒绝。它会把项目内部 harness 和 AI Coding Harness 治理流程长期混在同一个词里。
- 只改 README，不改 skill slug：拒绝。不能解决 agent skill discovery 和用户调用层面的概念冲突。

## Consequences

收益：

- 立即降低概念冲突：正式概念和公开 skill slug 都是 `AI Coding Harness` 命名族。
- 移除旧 slug 后，Agent 不会在 skill discovery 层看到裸 `harness-*`。
- Validator 把命名策略变成可检测的工程约束，而不是只靠记忆。

代价：

- 这是 breaking change；本机和用户安装目录需要删除旧 skill 后重新安装。
- 历史 Evidence/ADR 中会出现旧路径语境；本次允许将可搜索引用更新到新路径，但不试图重写历史事实。
- 部分用户仍可能口头说 Harness，因此入口 skill 必须继续承担语义澄清责任。

## Before Changing This Decision

- 先检查 ADR-008，因为当前公开 skill routing 已由 AgentMentor 语义命名取代。
- 区分历史事实、当前推荐命名和内部脚本路径，不要把三者混成一个规则。
- 运行 skill metadata checks，确认 legacy slug 兼容策略和当前命名策略一致。

## Evidence

- [F006 Skill Naming Compatibility](../features/F006-skill-naming-compatibility.md)
- [EV-009 Skill Naming Compatibility](../evidence/EV-009-skill-naming-compatibility.md)
- `skills/ai-coding-harness/SKILL.md`
- `scripts/skill_metadata_check.py`
- `tests/test_skill_metadata_check.py`
