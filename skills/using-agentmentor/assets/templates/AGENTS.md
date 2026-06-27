# Agent Instructions

## Core Rules

- 持久知识文档正文优先使用中文；机器可读字段、必需标题、命令、路径和代码标识保持英文或原文。
- 必须保护用户已有改动，不得擅自回滚。
- 未经用户明确批准，不得修改 AGENTS.md 或仓库级 Agent 指令。

## Project Rules

### Rule: 完成声明前必须有证据
- Scope: 非平凡代码变更、行为变更或 AgentMentor artifact 变更。
- Requirement: Agent MUST record verification checks and results before claiming completion.
- Source: F013 Evidence Claim Verification Governance；EV-020 Evidence Claim Verification Governance。
- Rationale: 防止没有证据支撑的“已完成”或虚假完成声明。

### Rule: 非平凡实现前必须运行 Start Gate
- Scope: 非平凡实现、行为变更、多文件修改、重构或高风险工作。
- Requirement: Agent MUST run Start Gate and satisfy required pre-work before coding.
- Source: ADR-001 Start Gate Before Implementation。
- Rationale: 防止在澄清、检索、Feature、ADR 或其它必要锚点缺失时直接开工。

### Rule: 项目规则晋升门槛
- Scope: 任何准备修改 AGENTS.md 或仓库级 Agent 指令的场景。
- Requirement: Agent MUST run the project-rules promotion gate and get explicit user approval before editing project-level rules.
- Source: User instruction, 2026-06-27；project-rules skill。
- Rationale: 防止 AGENTS.md 变成知识垃圾场，或让 Agent 自行扩张控制面。
