# 🤝 Contributing to AI Interactive Drama

感谢你愿意贡献代码 / 文档 / Issue / Discussion。本项目基于 [RuoYi-Vue3-FastAPI](https://gitee.com/insistence2022/RuoYi-Vue3-FastAPI) 二次开发，欢迎任何形式的参与。

## 📋 目录

- [行为准则](#-行为准则)
- [我能贡献什么](#-我能贡献什么)
- [如何提 Issue](#-如何提-issue)
- [如何提 PR](#-如何提-pr)
- [开发约定](#-开发约定)
- [本地开发](#-本地开发)
- [提交流程清单](#-提交流程清单)

## 🧭 行为准则

参与即代表同意 [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md)：尊重、包容、技术优先。违反者将被静默封禁。

## 🎁 我能贡献什么

| 类型 | 适合人群 | 影响面 |
| --- | --- | --- |
| 🐛 Bug 修复 | 后端 / 前端 / 移动端开发者 | 高 |
| ✨ 新功能 | 业务方、平台架构师 | 中 |
| 📝 文档 / 翻译 | 技术写作 | 中 |
| 🎨 Demo / 截图 / 视频 | 设计、内容运营 | 高 |
| 💬 Discussion 答疑 | 老用户、布道师 | 中 |
| ⭐ Star / Fork / Watch | 任何人 | 高（信号放大） |

## 🐞 如何提 Issue

请先搜一下 [Issues](https://github.com/flowerjunjie/ai-interactive-drama/issues) 是否已有同类问题。三种模板：

- **🐛 Bug Report**：环境信息、复现步骤、期望 / 实际、日志
- **✨ Feature Request**：业务背景、目标用户、替代方案、愿意出力否
- **❓ Question / Help**：环境、已尝试、相关 issue 链接

> 🚫 **不要**：用 Issue 当聊天（请去 [Discussions](https://github.com/flowerjunjie/ai-interactive-drama/discussions)）；在 Bug Report 里夹带 Feature。

## 🔧 如何提 PR

1. **Fork** 仓库 → 从 `main` 拉新分支（命名：`feat/xxx`、`fix/xxx`、`docs/xxx`）
2. 在分支上开发，**commit 信息**遵循：[Conventional Commits](https://www.conventionalcommits.org/)
   - `feat: 短剧点赞埋点`
   - `fix: 前端路由 hash 模式刷新 404`
   - `docs: 补充 TOS 凭证配置说明`
3. **推送前自检**：
   ```bash
   cd ruoyi-fastapi-backend && ruoyi dev lint
   cd ruoyi-fastapi-frontend && npm run build:prod
   ```
4. 发起 PR，标题清晰，描述引用相关 Issue（`Closes #123`）
5. 等待 CI + 维护者 review。**小型 PR（< 200 行）合并最快**

### PR 会被拒的常见原因

- ❌ 没描述改了什么 / 为什么改
- ❌ 包含无关重构（拆 PR）
- ❌ 没跑通 lint / build
- ❌ 把上游 RuoYi 代码原样搬运没声明出处
- ❌ 引入新的重型依赖未事先 Discussion

## 📐 开发约定

### 后端（Python / FastAPI）

- **风格**：Black + Ruff（仓库已配）
- **目录**：业务代码入 `module_drama/`，通用能力入 `module_admin/` 或 `common/`
- **模型**：SQLAlchemy 2.0 异步风格；表结构变更必须同步 Alembic 迁移
- **接口**：业务路径优先 `/api/*`；移动端别名 `/api/app/*` 由路由器自动挂载

### 管理后台（Vue3 / Element Plus）

- **状态管理**：Pinia（按模块拆 store）
- **路由**：vue-router 4 hash 模式
- **API 封装**：`src/api/drama/index.js` 集中维护
- **样式**：SCSS，禁用内联 style

### 移动端（uni-app）

- **样式**：Tailwind CSS utility 优先
- **状态**：组件内 `ref` 为主，跨页用 Pinia
- **接口**：经 `utils/request.js` 封装

### 数据库

- **MySQL 5.7+** 与 **PostgreSQL 12+** 双兼容（SQL 关键词大小写、双引号）
- **绝不**手改生产库；变更走 Alembic

## 💻 本地开发

参见 [README.md](./README.md) 的「🚀 快速开始」。最少要能跑起来：

```bash
# 后端
cd ruoyi-fastapi-backend && ruoyi app run --env=dev

# 前端
cd ruoyi-fastapi-frontend && npm run dev

# 移动端 H5
cd mobile-app && pnpm dev:h5
```

启动前跑一遍：

```bash
ruoyi app doctor --env=dev   # 后端健康检查
```

## ✅ 提交流程清单

- [ ] 我读过 [README](./README.md)
- [ ] 我搜过相关 Issue / Discussion
- [ ] 我在最新 `main` 上 fork
- [ ] commit 信息符合 Conventional Commits
- [ ] 我跑了 `ruoyi dev lint` 通过
- [ ] 我跑了 `npm run build:prod` 通过
- [ ] 我更新了相关文档 / README
- [ ] PR 描述里链接了相关 Issue

---

> 我们珍视每一次贡献。即使是拼写错误修正，也是有价值的 PR。⭐