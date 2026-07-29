# AgentMentor

[English](README.en.md)

AgentMentor vNext 是面向强编码模型的工程记忆与 SDD 约束层，而不是默认开发流水线。

它假定模型可以自行拆分、实现、测试和协作；它只补充模型天然不知道的项目事实：Feature 规格、历史取舍、已发生的失败模式，以及可复核的验证证据。

```text
任务 + 已知路径
  -> 一次 agentmentor context
  -> 模型自主开发与验证
  -> 仅在工程事件发生时沉淀 intent / decision / learning / evidence
  -> compact closeout
```

## 六个 Skill

| Skill | 职责 |
| --- | --- |
| `agentmentor` | 一次、上限三份正文文档的精确上下文召回。 |
| `agentmentor-intent` | 处理真实的目标、范围或边界冲突。 |
| `agentmentor-decision` | 记录可被未来重新提出的稳定取舍。 |
| `agentmentor-learning` | 将规格漂移、回归或重复失败转化为最小知识更新。 |
| `agentmentor-evidence` | 把关键完成、发布、交接或决策声明绑定到验证事实。 |
| `agentmentor-closeout` | 将本轮已知事实压缩为 `done`、`partial` 或 `blocked`。 |

普通小改动不会再被 Start、Vision、Delegation、Readiness 等默认 Gate 拦截；这些旧流程已归档在 `docs/archive/v1/`，稳定基线是 GitHub Release `v1.0.0`。

## 文档模型

- **Feature**：Feature 级 SDD Spec，描述目标、范围、行为、规则和验收。
- **ADR**：记录为什么选此方案、拒绝哪些方案、何时重审。
- **Lesson**：记录真实失败、根因和可执行防护。
- **Evidence**：记录声明、验证范围、检查、结果和限制。
- **Feature Index**：只做一级粗筛，不替代 Feature 正文。

默认使用 TDD：Feature 的 AC 场景驱动测试代码；仅在无法 test-first 时在 Feature 的 `Verification Strategy` 说明替代方式。

## 安装与验证

```powershell
.\scripts\install.ps1 codex
.\scripts\install.ps1 -Verify codex
python scripts\skill_metadata_check.py --root . --strict
python scripts\knowledge_check.py --root . --docs-path docs --strict
```

安装后重启 Agent；以 `agentmentor` 获取上下文。详细说明见 [INSTALL.md](INSTALL.md) 与 [docs/quickstart.md](docs/quickstart.md)。

## 状态

`v1.0.0` 是旧版稳定基线。当前 `vnext` 分支正在实施不兼容的 `v2.0.0` 重构；必须先由真实任务基准证明召回质量和端到端效率，才能宣称性能改善。
