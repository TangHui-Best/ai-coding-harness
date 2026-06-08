---
id: F008
doc_kind: feature
status: completed
created: 2026-06-08
updated: 2026-06-08
---

# F008: Spec Drift Guardrails

## Goal

为 AgentMentor 增加一层克制的 Spec Drift 防护：当真实案例、验证失败或用户反馈开始推翻旧 spec / acceptance criteria 时，Agent 不应继续把旧 spec 当成圣旨去局部打补丁，而应先判断当前 spec 是否仍然可信。

## Vision Anchor

- 原始请求或来源：用户在分析 AI 编码“越写越复杂、喜欢局部打补丁”的原因后，希望把解决方案落到 AgentMentor 能力中，但第一阶段不做 Architecture Review、Architecture Map、自动 init-project 或自动改写 `AGENTS.md`。
- 用户痛点或工程问题：AI 编码速度很快，如果需求纠察、Spec 纠偏、边界审视和验证证据没有同步增强，旧 spec 很容易被快速实现为长期复杂结构。
- 期望结果：新增 `spec-drift` Skill；`using-agentmentor`、`start-gate` 和 `vision-gate` 能把 stale spec / acceptance criteria drift / implementation follows spec but still wrong 等信号分流到 Spec Drift；README / INSTALL 只提供手动 `AGENTS.md` 模板与规则建议。
- 非目标或边界：不自动修改用户项目 `AGENTS.md`；不新增 Architecture Review；不新增 Architecture Map；不把 Start Gate 或 Vision Gate 扩展成全量架构审查。
- Exit Gate 对照来源：EV-011、`tests/test_spec_drift_guardrails.py`、`skill_metadata_check.py --strict`、全量 unittest discovery、`knowledge_check.py --strict`。

## Current Status

Done。源码中已新增 `spec-drift` Skill 和决策参考；入口路由、Start Gate、Vision Gate、README、INSTALL、Skill Index、metadata validator 与测试均已同步。默认 AGENTS 规则仍保持手动复制与手动添加，不自动接管用户项目配置。

## Links

- [EV-011 Spec Drift Guardrails](../evidence/EV-011-spec-drift-guardrails.md)

## Acceptance Criteria

- [x] 新增正式 Skill：`skills/spec-drift/SKILL.md`，名称、H1、触发表面和 progressive disclosure 结构完整。
- [x] `spec-drift` 覆盖 real cases、validation failure、user feedback、stale spec、acceptance criteria drift、implementation follows spec but still wrong 等核心信号。
- [x] `using-agentmentor` 可以在旧 spec 不可信时把任务路由到 `spec-drift`。
- [x] `start-gate` 增加 `needs spec-drift` 分流，但不承担完整 stale spec 审查。
- [x] `vision-gate` 明确自身守护 original intent，stale spec classification 交给 `spec-drift`。
- [x] README / INSTALL 说明 Optional Project Rules，用户可手动复制 bundled `AGENTS.md` 模板并添加推荐规则，AgentMentor 不自动修改用户项目规则文件。
- [x] 新增或更新测试，覆盖 Skill 存在性、入口路由、Start Gate、Vision Gate、README / INSTALL 手动规则边界和 metadata validator。
- [x] 全量测试、Skill metadata 检查和知识文档检查通过。

## Patch History

None yet.

## Evidence

- [EV-011 Spec Drift Guardrails](../evidence/EV-011-spec-drift-guardrails.md)

## Next Step

后续若真实使用中出现“重复补丁已经明显变成架构边界问题”，再单独评估 Architecture Review 或 Architecture Map，不纳入 F008 第一阶段。
