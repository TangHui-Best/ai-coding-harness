---
id: EV-013
doc_kind: evidence
scope: project
feature_refs: [docs/features/F010-goal-driven-feature-flow.md]
created: 2026-06-18
---

# EV-013: Goal Driven Feature Flow

## Supports Claim

This Evidence supports the completion or validation claim for EV-013: Goal Driven Feature Flow.


## Verification Scope
验证 F010：AgentMentor 默认不逐 Feature 请求设计审批；清晰 Goal 是授权边界；Feature page 是工程记忆；空审批请求被禁止；closeout 门禁继续保留。

## Checks
```text
python -m unittest tests.test_goal_driven_feature_flow
python -m unittest tests.test_goal_driven_feature_flow tests.test_closeout_convergence_contract tests.test_skill_progressive_disclosure
python scripts\knowledge_check.py --root . --docs-path docs --strict
python scripts\skill_metadata_check.py
powershell -ExecutionPolicy Bypass -File scripts\install.ps1 codex
Select-String -Path C:\Users\HUAWEI\.codex\skills\using-agentmentor\SKILL.md,C:\Users\HUAWEI\.codex\skills\start-gate\SKILL.md,C:\Users\HUAWEI\.codex\skills\knowledge-capture\SKILL.md -Pattern "Goal-Driven Feature Flow|Empty Approval Guard|Feature pages are engineering memory|This skill owns closeout"
```

## Results

Pass. 新增 focused regression、closeout convergence、progressive disclosure、knowledge check、skill metadata check 均通过；`using-agentmentor`、`start-gate`、`knowledge-capture` 已补入同等热路径规则并由 `Select-String` 确认。

### AgentMentor Validation
`knowledge_check.py --strict` 和 `skill_metadata_check.py` 已通过。实际输出见本次会话验证记录。

## Artifacts

- `skills/using-agentmentor/SKILL.md`
- `skills/start-gate/SKILL.md`
- `skills/knowledge-capture/SKILL.md`
- `tests/test_goal_driven_feature_flow.py`
- `docs/features/F010-goal-driven-feature-flow.md`
- Local Codex skills: `using-agentmentor`, `start-gate`, `knowledge-capture`

## Limitations

This Evidence does not prove behavior outside the verification scope recorded above.

## Notes
本次变更刻意不新增复杂状态机。主判断仍由 Start Gate/Knowledge Capture 承担，只把“Goal 是授权边界、Feature 不是审批关卡、空审批禁止”放回热路径 Skill 文档中。
