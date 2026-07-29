# Feature Index

用于 `agentmentor context` 的一级粗筛。它不替代 Feature 正文，也不应在普通任务中触发全量扫描。

仅在新增、归档、拆分或合并 Feature，或者 `Goal`、`trigger_terms`、`owned_paths` 发生实质变化时更新。

| Feature | Status | Trigger Terms | Owned Paths | Read When |
| --- | --- | --- | --- | --- |
| [F017 AgentMentor vNext 工作流](F017-agentmentor-vnext-gpt56-workflow.md) | active | AgentMentor vNext, GPT-5.6, workflow cost, context retrieval, engineering memory | `skills/`, `scripts/`, `templates/`, `docs/features/` | 修改 vNext Skill、Schema、召回、安装器或验证流程时读取。 |
