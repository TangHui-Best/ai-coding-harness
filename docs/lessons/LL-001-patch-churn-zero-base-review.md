---
id: LL-001
doc_kind: lesson
status: active
scope: project
feature_refs: []
applies_to: [harness-skills, start-gate, knowledge-retrieval, knowledge-capture, incident-learning, vision-gate, readiness-dashboard, project-rules]
created: 2026-05-16
updated: 2026-05-20
---

# LL-001: Patch Churn Requires Zero-Base Review

## Pitfall

同一个 Feature 在验收后持续打补丁时，Agent 容易把每一轮失败都当成孤立 bug，继续增加关键词、规则分支、过滤条件或下游兜底逻辑。这样会让测试数量增加、当前样本变绿，但系统模型并不一定收敛。

## Root Cause

Harness 原本强调 Start Gate、Vision Gate、Evidence 和 Incident Learning，但没有把“补丁链条本身也是证据”写成显式触发器。Agent 因此会沿着既定实现路径继续局部修复，而不是主动质疑原始抽象、边界或不变量是否错误。

后续复盘发现，仅有“3 次补丁触发归零审视”还不够。如果 Agent 在修 bug 前没有检索并归属到原 Feature，修完后也没有更新 `## Patch History`，补丁次数就不会被可靠记录，归零审视阈值自然无法触发。

## Trigger

当出现以下任一信号时触发：

- 同一 Feature 出现 3+ follow-up fixes，或类似 `Fxxx.n` 的连续补丁链。
- 手工验收在测试通过后继续暴露同类失败。
- 修复越来越依赖场景枚举、关键词匹配、过滤规则、fallback 或下游 cleanup。
- 新补丁增加复杂度，但没有减少失败类别。

## Fix

把 patch churn 加入 `using-harness`、`harness-start-gate`、`harness-vision-gate`、`harness-incident-learning`、`harness-knowledge-capture`、`harness-readiness-dashboard` 和 `harness-project-rules` 的触发面与判断流程。

核心行为是：当补丁震荡出现时，Agent 必须暂停继续打补丁，检索相关 Feature/Evidence/ADR/Lesson，执行 Patch Churn Review，并判断是否需要 Vision Gate、ADR、Lesson 或 Evidence。

补充行为是：对非 tiny bugfix，Agent 必须先判断是否可能属于已有 Feature 或历史修复链；若可能，先运行 Knowledge Retrieval 完成 Feature attribution。修复完成后，Knowledge Capture 必须判断是否更新原 Feature 的 `## Patch History`。这条记录是后续 3+ patch churn 阈值的计数来源。

## Protection

- `harness-start-gate` 在 repeated patch chain 下不得直接返回 `ready`，必须先完成 Patch Churn Check。
- `harness-start-gate` 对非 tiny bugfix 必须显式报告 Bug attribution；归属未知且可能影响修复路径时返回 `needs retrieval`。
- `harness-knowledge-retrieval` 必须提供 Bug Retrieval Mode，用症状、错误、模块、Feature ID、Patch History 和 Evidence 搜索历史。
- `harness-incident-learning` 必须列出补丁轨迹、分组根因，并判断修复是否向上游不变量或边界移动。
- `harness-vision-gate` 使用 Patch Churn lens 判断当前抽象是否仍然能解释原始目标和已观察失败。
- `harness-knowledge-capture` 必须在非 tiny bugfix 收尾时报告 Bugfix attribution；若归属到已完成 Feature，必须更新 `## Patch History`。
- `harness-readiness-dashboard` 必须报告 Bugfix Attribution 和 `Patch Churn Review` 状态；没有该状态时，重复补丁 Feature 不能无条件标记 ready。
- `harness-project-rules` 只有在本 Lesson 或同类 Evidence 支撑下，才允许把“补丁震荡触发归零审视”晋升为项目级 Agent 规则。

## Source

该 Lesson 来自 F018 多 Agent evidence-grounded workflow 的连续补丁经验。F018.1 到 F018.7 逐步修复触发、展示、格式、流式边界和 Composer 过滤问题，最终才收敛到 `retrieved candidate != accepted evidence` 这个更上游的 evidence boundary 判断。

详细方案见 [Patch Churn 与归零审视：Harness Skill 迭代方案](../proposals/2026-05-15-patch-churn-zero-base-review.md)。

## Principle

补丁震荡本身就是证据。持续局部修复如果不能减少失败类别，就必须触发归零审视：当前问题是在修实现，还是在替错误抽象续命。
