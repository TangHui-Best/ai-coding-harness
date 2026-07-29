# Quickstart

1. 安装并重启 Agent。

   ```powershell
   .\scripts\install.ps1 codex
   ```

2. 在需要项目历史的任务开始时使用 `agentmentor`。它只执行一次 `context`，按“已知路径 → Feature Index → Feature → 直接关联 ADR/Lesson/Evidence”返回最多三份正文文档。

3. 使用 Feature 作为 Feature 级 SDD Spec：明确 Goal、Scope、Specification、Acceptance 和 Current State。默认让 Acceptance 场景驱动 TDD。

4. 只在事件存在时沉淀：范围冲突用 intent，稳定取舍用 ADR，漂移/回归用 learning，关键声明用 Evidence。

5. 任务结束或暂停时用 closeout 压缩已知状态；它不会重跑检索、扫描或强制建文档。

不要为普通小改动创建任何 AgentMentor 文档；`no relevant context` 是有效结果。
