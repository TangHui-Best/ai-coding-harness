# Quickstart

1. 安装并重启 Agent。

   ```powershell
   .\scripts\install.ps1 codex
   ```

2. 当任务可能改变功能行为、规格、架构边界、接口契约、数据语义或验收条件时，使用 `agentmentor` 读取一次 `docs/INDEX.md`。主 Agent 基于 Brief 自主选择默认 0–3 个相关 Feature，并按需直接选择 ADR 或展开关联的 Lesson / Evidence。纯机械、局部、无行为语义的改动可以跳过 Index。

3. 使用 Feature 作为 Feature 级 SDD Spec：明确 Goal、Scope、Specification、Acceptance 和 Current State。默认让 Acceptance 场景驱动 TDD。

4. 只在事件存在时沉淀：范围冲突用 intent，稳定取舍用 ADR，漂移/回归用 learning，关键声明用 Evidence。

5. 任务结束或暂停时用 closeout 压缩已知状态；它不会重跑检索、扫描或强制建文档。

不要为普通小改动创建任何 AgentMentor 文档；Index 中没有相关条目是有效结果。
