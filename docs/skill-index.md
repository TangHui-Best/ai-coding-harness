# Skill Index

| Skill | 触发事件 | 不做什么 |
| --- | --- | --- |
| `agentmentor` | 任务可能影响功能、规格、架构、接口、数据语义或验收 | 不编排开发流程，不替主 Agent 路由正文。 |
| `agentmentor-intent` | 目标、范围、Feature 或 ADR 冲突 | 不做例行开工检查。 |
| `agentmentor-decision` | 稳定且会影响未来的取舍 | 不记录局部可逆实现细节。 |
| `agentmentor-learning` | Spec 漂移、回归、重复失败 | 不做形式化复盘。 |
| `agentmentor-evidence` | 关键完成、发布、交接或决策声明 | 不写设计理由或计划。 |
| `agentmentor-closeout` | 暂停、交接、结束 | 不重启检索或全量校验。 |

历史 v1 的 12 个 Skill 已归档，不属于 vNext 运行时表面。
