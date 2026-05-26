---
id: EV-001
doc_kind: evidence
scope: feature
feature_refs: [docs/features/F001-closeout-entry-anchor-validation.md]
created: 2026-05-22
---

# EV-001: Closeout Entry And Vision Anchor Validation

## Scope

验证 F001 的通用 closeout 阻断能力：脚本要求完成声明显式包含 Entry Gate、Vision Anchor、Patch Churn Review，并在 `Completion claim allowed: yes` 时拦截 missing、未解释豁免、以及 retroactive 未补救的入口状态。

## Commands

```text
python -m unittest ai-coding-harness.tests.test_harness_closeout_check
python -m unittest discover ai-coding-harness\tests
python ai-coding-harness\scripts\knowledge_check.py --root ai-coding-harness --docs-path docs
python ai-coding-harness\scripts\harness_closeout_check.py --file ai-coding-harness\docs\evidence\EV-001-closeout-entry-anchor-validation.md
python ai-coding-harness\scripts\skill_metadata_check.py --root ai-coding-harness
python ai-coding-harness\skills\using-harness\scripts\skill_metadata_check.py --root ai-coding-harness
```

## Results

Pass。

- `python -m unittest ai-coding-harness.tests.test_harness_closeout_check`: 8 tests passed.
- `python -m unittest discover ai-coding-harness\tests`: 18 tests passed.
- `knowledge_check.py`: scanned 12 Markdown files, checked 6 knowledge artifacts, 0 errors, 0 warnings.
- `harness_closeout_check.py`: closeout block structure passed.
- `skill_metadata_check.py`: scanned 11 skill files, 0 errors, 0 warnings from both root and bundled script entrypoints.

## Harness Validation

`knowledge_check.py` command path and result:

```text
python ai-coding-harness\scripts\knowledge_check.py --root ai-coding-harness --docs-path docs
Scanned 12 markdown file(s). Checked 6 knowledge artifact(s). Errors: 0. Warnings: 0.
```

`harness_closeout_check.py` command path and result:

```text
python ai-coding-harness\scripts\harness_closeout_check.py --file ai-coding-harness\docs\evidence\EV-001-closeout-entry-anchor-validation.md
Harness closeout block structure: pass
```

## Artifacts

- `scripts/harness_closeout_check.py`
- `skills/using-harness/scripts/harness_closeout_check.py`
- `tests/test_harness_closeout_check.py`
- `skills/harness-knowledge-capture/SKILL.md`
- `skills/using-harness/SKILL.md`
- `docs/features/F001-closeout-entry-anchor-validation.md`

## Notes

Closeout verdict: pass
Completion claim allowed: yes
Entry Gate: satisfied by Feature F001 before implementation
Vision Anchor: Feature F001
Backlog/Handoff: not triggered because this change is completed in-session with Feature and Evidence records
Plan lifecycle: not triggered because no separate plan artifact was needed for this bounded script and skill-contract change
Readiness: dashboard pass
Vision Gate Exit: pass
Patch Churn Review: not triggered because F001 has no follow-up patch history
Bugfix attribution: not triggered because this is a Harness contract enhancement, not a bugfix against delivered behavior
ADR: not triggered because ADR-001 already owns the Start Gate decision and this change enforces the existing direction
Lesson: not triggered because the reusable protection is implemented as a deterministic checker
Evidence: docs/evidence/EV-001-closeout-entry-anchor-validation.md
Evidence level: standard
Feature: updated F001
Check: knowledge_check.py passed; harness_closeout_check.py passed; skill_metadata_check.py passed
