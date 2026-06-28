---
id: F016
doc_kind: feature
status: completed
created: 2026-06-28
updated: 2026-06-28
---

# F016: Doc Usage Telemetry

## Goal

为 AgentMentor 增加最小文档使用观测机制：当 Feature、ADR、Lesson、Evidence 或 AGENTS 文档真实影响当前任务判断或变更叙事时，追加一条 usage JSONL 记录。

## Vision Anchor

- 原始请求或来源：用户提出文档价值不应只看沉淀数量，而应关注文档是否被后续 Agent 召回、判断、使用，并且这次明确只先在 `knowledge-retrieval` 和 `change-narrative` 中记录真实使用。
- 用户痛点或工程问题：没有 usage 观测时，只能靠感觉判断哪些文档真的进入闭环；但如果记录所有 read，又会变成噪音日志系统，并和 AgentMentor 辅助开发的定位偏离。
- 期望结果：提供一个脚本化、低冲突、低噪音的 usage 追加机制，按 Git 用户写入 `.agentmentor/usage/events/<git-user-name>.jsonl`，只记录产生影响的文档使用。
- 非目标或边界：不新增独立 Skill；不记录单纯阅读、候选扫描或 Feature Index 粗召回；不做统计报表；不做文件分片；不回写 Feature / ADR / Lesson / Evidence 本体；不维护 `usage_count`。
- Exit Gate 对照来源：本 Feature、EV-023、usage script tests、skill progressive disclosure tests、strict knowledge check。

## Feature Intake

- Original problem: AgentMentor 的第一性原理关注文档是否进入未来决策闭环，但当前只有召回入口和内容质量治理，缺少最小的真实使用观测。
- User pain point: 如果文档没有被二次使用，沉淀数量再多也不能证明价值；如果把所有阅读都记下来，又会制造冲突、噪音和日志系统复杂度。
- Capability promise: 当文档实际影响 `knowledge-retrieval` 的判断或 `change-narrative` 的解释时，Agent 可以调用脚本追加一条精简 usage 记录。
- Non-goals: 不记录 read log；不覆盖所有 Skill；不自动判断使用；不统计开发者绩效；不把 usage 变成单独工作流。
- Acceptance source: 用户确认的第一阶段方案：只在 `knowledge-retrieval`、`change-narrative` 中记录 used，不记录 read；使用脚本追加到 Git 跟踪的按用户隔离 JSONL 文件。
- Open questions: 未来是否需要统计报表、长期无 usage 分析、按月分片或更多 Skill 入口，等待真实使用数据后再判断。

## Capability Contract

- `scripts/usage_record.py` 和 bundled `skills/using-agentmentor/scripts/usage_record.py` 负责追加 usage JSONL。
- usage 文件路径为 `.agentmentor/usage/events/<git-user-name>.jsonl`，Git 用户名会被规范化为小写安全文件名。
- 每条记录只包含 `ts`、`doc`、`doc_type`、`task`、`impact`。
- `.gitignore` 允许 `.agentmentor/usage/events/*.jsonl` 进入 Git，但仍默认忽略 `.agentmentor` 下的其他运行文件。
- `knowledge-retrieval` 只在文档真实改变 scope、design、fix direction、verification gate、completion-claim judgment 或 recurrence prevention 时记录。
- `change-narrative` 只在文档真实塑造 commit、PR、handoff、release note 或 progress summary 的解释时记录。
- 第一阶段不去重；同一任务里同一文档多次真实发挥作用可以多次记录。

## Decision Context

### Why

AgentMentor 的核心不是“写了多少文档”，而是文档是否改变未来 Agent 的行为。Usage 观测补上了这个闭环里的最小证据：某个文档在某个任务中实际影响了判断、行动、验证或叙事。它必须进入 Git，才能支持团队级统计；但不能所有人写同一个文件，否则会增加 merge conflict。因此按 Git 用户隔离 JSONL 是当前成本最低的全局可聚合方案。

### Why Not

没有新增 `usage-telemetry` Skill，因为 usage 不是开发主流程，而是 `knowledge-retrieval` 和 `change-narrative` 的副作用。没有记录 `event` 字段，因为第一阶段每一行都默认代表 doc used。没有记录 read、candidate、stale detected 或 promoted to rule，因为这些会把机制推向日志系统。没有做文件分片，因为 5000 行以内足够长期使用，过早分片会增加结构复杂度。

### If Modifying This Area, Check

- 修改 usage schema 时，同步检查 `scripts/usage_record.py`、bundled 脚本、`tests/test_usage_record.py`、`knowledge-retrieval` 和 `change-narrative`。
- 修改 `.agentmentor` 忽略规则时，确认 `.agentmentor/usage/events/*.jsonl` 仍可进入 Git，其他运行文件仍默认忽略。
- 修改 impact 枚举时，确认 Skill 文案和脚本 choices 一致。
- 不要把 usage 写入 Feature / ADR / Lesson / Evidence 本体，也不要新增 `usage_count`。
- 不要把 usage 机制扩散到所有 Skill，除非真实使用证明漏记比额外复杂度更严重。

## Current Status

Completed。第一阶段最小 usage 机制已经落地到脚本、两个 Skill 入口、Git ignore 规则、测试、Feature Index 和 Evidence。

## Links

### Evidence

- [EV-023 Doc Usage Telemetry](../evidence/EV-023-doc-usage-telemetry.md)

### Decisions / ADRs

- None.

### Lessons

- None.

### Specs / Plans

- None.

### Related Features

- [F009 Feature Intake Governance](F009-feature-intake-governance.md)
- [F014 Project Rules Human Authorized Governance](F014-project-rules-human-authorized-governance.md)

### External Context

- [Knowledge Retrieval skill](../../skills/knowledge-retrieval/SKILL.md)
- [Change Narrative skill](../../skills/change-narrative/SKILL.md)
- [Usage record script](../../scripts/usage_record.py)
- [Bundled usage record script](../../skills/using-agentmentor/scripts/usage_record.py)

## Acceptance Criteria

- [x] 提供 root/bundled `usage_record.py`，可以追加 usage JSONL。
- [x] usage 文件按 Git 用户隔离，路径为 `.agentmentor/usage/events/<git-user-name>.jsonl`。
- [x] usage record 字段保持精简：`ts`、`doc`、`doc_type`、`task`、`impact`。
- [x] 脚本校验 doc 路径存在、doc_type 枚举、impact 枚举和 task 非空。
- [x] `knowledge-retrieval` 明确只记录真实影响判断的 used 文档，不记录 read 或 candidate。
- [x] `change-narrative` 明确只记录真实塑造变更叙事的 used 文档。
- [x] `.gitignore` 允许 usage JSONL 进入 Git，同时继续忽略其他 `.agentmentor` 运行文件。

## Acceptance Map

| Claim | Acceptance | Evidence | Status |
| --- | --- | --- | --- |
| Usage 是 used telemetry，不是 read log | 两个 Skill 都明确只记录实际影响判断或叙事的文档 | [EV-023](../evidence/EV-023-doc-usage-telemetry.md) | completed |
| Usage 通过脚本追加 | root/bundled `usage_record.py` 生成按 Git 用户隔离的 JSONL | [EV-023](../evidence/EV-023-doc-usage-telemetry.md) | completed |
| Usage schema 保持最小 | 测试校验字段只有 `ts`、`doc`、`doc_type`、`task`、`impact` | [EV-023](../evidence/EV-023-doc-usage-telemetry.md) | completed |

## State Timeline

| Date | State | Trigger | Evidence | Note |
| --- | --- | --- | --- | --- |
| 2026-06-28 | completed | Minimal doc usage telemetry iteration | [EV-023](../evidence/EV-023-doc-usage-telemetry.md) | First phase covers knowledge-retrieval and change-narrative only. |

## Patch History

None yet.

## Evidence

- [EV-023 Doc Usage Telemetry](../evidence/EV-023-doc-usage-telemetry.md)

## Recovery Snapshot

- Read first: this Feature page, then EV-023, `skills/knowledge-retrieval/SKILL.md`, `skills/change-narrative/SKILL.md`, and `scripts/usage_record.py`.
- Current capability state: completed; usage telemetry is a lightweight side effect of retrieval/narrative decisions.
- Known risks: 第一阶段不去重、不统计、不分片，也不覆盖所有 Skill；这是有意收敛，不是遗漏。
- Next safe action: 如果要扩展记录入口，先证明当前两个入口漏掉了高价值 used 事件，再扩展。
- Unblock condition: not blocked.

## Next Step

同步安装后的 Codex skills，使本机后续会话能读取 usage 记录规则和 bundled 脚本。
