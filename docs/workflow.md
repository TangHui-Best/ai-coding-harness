# AgentMentor vNext 工作流

```text
任务 + 已知路径
  -> agentmentor context（一次，0–3 份正文）
  -> 模型自主计划 / TDD / 实现 / 验证
  -> 发生事件时才调用 intent / decision / learning / evidence
  -> closeout 压缩当前状态
```

`context` 不命中时明确返回 `no relevant context`。它不扫描 `docs/archive/v1/`，也不在其他 Skill 中重复执行。

事件不是阶段：只有方向冲突、稳定取舍、现实与 Spec 冲突、重复失败、关键发布/完成声明或暂停/交接发生时，才需要额外治理能力。
