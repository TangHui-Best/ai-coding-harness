---
id: ADR-002
doc_kind: adr
status: accepted
scope: project
feature_ids: []
decision_area: knowledge-language
created: 2026-05-09
updated: 2026-05-18
---

# ADR-002: Chinese Prose For Knowledge Artifacts

## Context

Harness 知识文档的主要读者是未来的项目维护者和 Agent。当前项目的需求讨论、约束表达和长期判断以中文为主，如果知识文档正文默认英文，会增加恢复上下文和复核决策的成本。

同时，现有 `knowledge_check.py` 依赖稳定的 frontmatter 字段和英文 Markdown section 标题。命令、日志、路径、API 和代码标识也不应该被翻译。

## Decision

Feature、ADR、Lesson、Evidence、spec、plan、Backlog 和 handoff 文档的人类说明正文默认使用中文。

保持以下机器可读或源文本内容稳定：

- YAML frontmatter keys and enum values.
- Required Markdown section headings checked by scripts.
- Code identifiers, commands, logs, paths, APIs, and quoted source text.

如果文档面向外部或开源读者，优先增加短英文摘要，而不是全文双语复制。

## Alternatives

- 强制全文中文：拒绝，因为会破坏现有校验脚本、命令记录、代码标识和外部引用的稳定性。
- 保持全文英文：拒绝，因为这会提高项目内部恢复上下文和复核决策的阅读成本。
- 为每份文档写中英双语全文：拒绝，因为会制造维护负担，且容易出现两个语言版本语义漂移。

## Consequences

项目内部知识文档更贴近真实讨论语言，后续会话更容易恢复上下文。

代价是模板和 skill 必须明确区分“人类说明正文”和“机器可读结构”。未来如果要支持中文 section 标题，应先升级 `knowledge_check.py` 支持标题别名，再迁移模板。

## Evidence

- `skills/harness-knowledge-capture/SKILL.md`
- `skills/using-harness/assets/templates/FEATURE.md`
- `skills/using-harness/assets/templates/ADR.md`
- `skills/using-harness/assets/templates/LESSON.md`
- `skills/using-harness/assets/templates/EVIDENCE.md`
- `skills/using-harness/assets/templates/AGENTS.md`
