# AgentMentor Index

用于帮助 Agent 判断当前任务需要阅读哪些工程事实。它不是正文，不是规则引擎，也不替代 Feature 或 ADR。

仅收录当前有效的 Feature 与已接受的 ADR；草稿、归档和已替代文档不进入此目录。

| Document | Type | Brief |
| --- | --- | --- |
| [ADR-010: 采用事件触发的工程记忆层](decisions/ADR-010-agentmentor-vnext-event-triggered-memory-layer.md) | adr | 默认不运行 Gate 链；仅在工程事件发生时沉淀可复用的规格、决策、经验与证据。 |
| [ADR-011: 采用主 Agent 选择的统一工程 Index](decisions/ADR-011-agent-selected-engineering-index.md) | adr | 统一 Index 提供当前有效的 Feature 与 ADR 目录，由主 Agent 语义选择需要阅读的工程事实。 |
| [F017: AgentMentor vNext 工作流](features/F017-agentmentor-vnext-gpt56-workflow.md) | feature | 以统一工程 Index 供主 Agent 语义选择 Feature 与 ADR，替代规则型 Top-1 召回。 |
