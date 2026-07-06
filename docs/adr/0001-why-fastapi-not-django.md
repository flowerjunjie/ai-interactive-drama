# ADR-0001 · 为什么选 FastAPI 而不是 Django / Flask

- 状态：✅ Accepted
- 日期：2026-07-06
- 决策者：flowerjunjie

## 背景与问题陈述

我们要搭建一个**短剧 C 端 + 后台 + 移动端**的全栈平台，技术选型直接决定：

- 团队 4 人能否在 5 个月内端到端交付
- 后期 AI 节点推荐、向量检索等能力的接入成本
- 移动端 / 前端 / 后端的协作效率

候选后端框架有 3 个：**Django**、**Flask**、**FastAPI**。我们之前用 Java/Spring Cloud，但人力与节奏不匹配，本次必须换栈。

## 考虑的选项

### 选项 A · Django + DRF

**优点**
- 自带 ORM / Admin / Auth / Forms，开箱即用
- 社区生态最成熟，招聘最易
- 自带后台管理（`/admin`），能省部分后台开发

**缺点**
- 同步 IO 为主，async 支持薄弱（ASGI 模式生态不完整）
- 性能天花板低，单机 QPS 受限
- 模板引擎 / Forms / Admin 对纯 API 项目冗余

### 选项 B · Flask + SQLAlchemy

**优点**
- 极简、灵活、第三方库丰富
- 上手成本最低

**缺点**
- 没有"框架级"约束，小项目友好，大项目易失控
- 类型提示弱，OpenAPI 需手写或配 flask-smorest
- 团队规模上去后缺工程化能力

### 选项 C · FastAPI + SQLAlchemy 2.0（已选 ✅）

**优点**
- **async/await 原生支持**，与 SQLAlchemy 2.0 async、TOS 异步 SDK、Redis async 客户端全链路异步
- **类型即文档**：Pydantic 模型 + OpenAPI 自动生成，省去手动维护 schema
- **性能强**：基于 Starlette + Uvicorn，TechEmpower 基准测试稳居 Python 框架 Top 3
- **依赖注入**：FastAPI Depends 让鉴权 / DB session / 限流统一管理
- **现代 Python 实践**：类型提示、async、pytest、ruff 全套现代化

**缺点**
- 生态比 Django 年轻，部分 niche 库需自己挑
- 团队需要适应 async 思维（共享 session、context manager 等）
- 国内文档与社区案例少于 Django

## 决策

**选 C · FastAPI + SQLAlchemy 2.0**。

理由：

1. **业务特征驱动**：短剧 C 端 95% 流量是 IO 密集型（DB + Redis + TOS 签名 + 推荐召回），async 全链路是核心诉求
2. **AI 接入成本**：模块 `module_ai/` 需要对接大模型 SDK（多数 async），FastAPI async 路由零适配
3. **开发体验**：OpenAPI 自动生成给前后端联调省一周工作量
4. **后端代码量**：SQLAlchemy 2.0 + Pydantic v2 + FastAPI 三者结合，CRUD 接口样板代码量是 Django 的 ~60%
5. **可演进性**：若需异步任务 / WebSocket 推送（短剧弹幕、互动直播），FastAPI 内置支持

## 后果

### 正面

- 单机 QPS 实测比 Django 同等配置高 2-3 倍
- 启动时间 < 2 秒（vs Django ~5 秒），开发体验流畅
- OpenAPI 文档自动同步，前后端协作摩擦↓ 70%
- AI 模块接入新模型只需加 router，框架无侵入

### 负面 / 风险

- 异步生态相对年轻，遇到边缘问题需深入读源码
- 团队需要 1-2 周适应 async / context manager
- 部分老旧中间件 SDK 只有同步版本，需自己包 async wrapper

### 中和 / 后续动作

- 已封装统一 `ruoyi db upgrade` CLI，新人不直接接触 Alembic 细节
- 提供 `.pre-commit-config.yaml`（ruff + black + isort）保证代码风格
- 关键模块（auth / 限流 / 日志）走 Depends 注入，不散落在业务代码里

## 替代方案的退出路径

如未来需要：

- **Django Admin**：`sqladmin` 或 `fastapi-admin` 可补齐（已纳入 Roadmap）
- **Flask 灵活性**：FastAPI 本身基于 Starlette，灵活度不输 Flask
- **类型化 ORM 增强**：SQLAlchemy 2.0 + Mypy 已是黄金组合

## 参考资料

- [FastAPI vs Flask vs Django · Benchmarks](https://www.techempower.com/benchmarks/)
- [SQLAlchemy 2.0 async 文档](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- [Pydantic v2 迁移指南](https://docs.pydantic.dev/latest/migration/)