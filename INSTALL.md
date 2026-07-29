# 安装 AgentMentor vNext

AgentMentor vNext 安装六个 Skill，不安装默认 Hook，也不安装旧 Gate。安装器会移除已知的 v1 Skill 目录；`v1.0.0` 已由发布标签保留，不会被修改。

## Codex

```powershell
.\scripts\install.ps1 codex
.\scripts\install.ps1 -Verify codex
```

或在 Bash 环境：

```bash
bash scripts/install.sh codex
bash scripts/install.sh --verify codex
```

## Claude Code

将 `codex` 替换为 `claude`；`both` 可安装到两个目标。安装后重启相应 Agent。

## 使用

以 `agentmentor` 开始有项目上下文依赖的工作。传入任务语义和已知路径后，执行一次有界 `context` 召回；正常的任务拆分、TDD、实现和验证由模型自主完成。

仅在事件发生时使用其余 Skill：意图冲突、稳定设计取舍、规格漂移或重复失败、关键声明、任务暂停或交接。

## 验证

```powershell
python scripts\skill_metadata_check.py --root . --strict
python scripts\knowledge_check.py --root . --docs-path docs --strict
pytest -q
```

安装器的环境变量 `AGENTMENTOR_CODEX_SKILLS_DIR` 和 `AGENTMENTOR_CLAUDE_SKILLS_DIR` 可指定临时目标，适合 CI 或沙箱验证。
