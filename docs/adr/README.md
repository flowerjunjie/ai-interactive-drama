# 📐 Architecture Decision Records (ADR)

> 本目录记录本项目**重要的架构与技术选型决策**。每条 ADR 描述**背景 / 决策 / 后果**，
> 帮助新人理解"为什么是这样"，避免后人重复争论。

## 📋 ADR 列表

| # | 标题 | 状态 | 日期 |
| --- | --- | --- | --- |
| [0001](./0001-why-fastapi-not-django.md) | 为什么选 FastAPI 而不是 Django / Flask | ✅ Accepted | 2026-07-06 |

## 📝 ADR 模板

新建 ADR 时复制以下结构（参考 [MADR](https://adr.github.io/madr/)）：

```markdown
# ADR-XXXX · 简短决策标题

- 状态：Proposed / Accepted / Deprecated / Superseded by ADR-YYYY
- 日期：YYYY-MM-DD
- 决策者：maintainer

## 背景与问题陈述

[2-3 段：业务背景、要解决什么问题]

## 考虑的选项

1. 选项 A
2. 选项 B
3. 选项 C

## 决策

[选了哪个，为什么]

## 后果

### 正面

- ...

### 负面 / 风险

- ...

### 中和 / 后续动作

- ...
```

## 📚 参考

- [Michael Nygard · Documenting Architecture Decisions](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
- [MADR · Markdown ADR](https://adr.github.io/madr/)
- [GitHub · ADR 实践](https://github.com/joelparkerhenderson/architecture-decision-records)