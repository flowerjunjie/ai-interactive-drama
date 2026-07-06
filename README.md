<h1 align="center" style="margin: 30px 0 30px; font-weight: bold;">AI Interactive Drama</h1>
<h4 align="center">AI 互动短剧平台 · 基于 RuoYi-Vue3 + FastAPI · 管理后台 + 移动端 C 端 + 后端 API</h4>

<p align="center">
  🇨🇳 <b>中文</b> · <a href="./README.en.md">🇬🇧 English</a>
</p>

<p align="center">
    <a href="https://github.com/flowerjunjie/ai-interactive-drama/stargazers">
        <img alt="GitHub stars" src="https://img.shields.io/github/stars/flowerjunjie/ai-interactive-drama?style=social">
    </a>
    <a href="https://github.com/flowerjunjie/ai-interactive-drama/network/members">
        <img alt="GitHub forks" src="https://img.shields.io/github/forks/flowerjunjie/ai-interactive-drama?style=social">
    </a>
    <img alt="release" src="https://img.shields.io/github/v/release/flowerjunjie/ai-interactive-drama?include_prereleases">
    <img alt="license" src="https://img.shields.io/github/license/flowerjunjie/ai-interactive-drama">
    <img alt="node" src="https://img.shields.io/badge/node-≥18-blue">
    <img alt="python" src="https://img.shields.io/badge/python-≥3.10-blue">
    <img alt="mysql" src="https://img.shields.io/badge/MySQL-≥5.7-blue">
    <img alt="redis" src="https://img.shields.io/badge/redis-≥6.2-blue">
</p>

---

## 📌 平台简介

**AI Interactive Drama** 是一套面向短剧业务的 AI 互动平台：在开源 [RuoYi-Vue3-FastAPI](https://gitee.com/insistence2022/RuoYi-Vue3-FastAPI) 之上扩展 **C 端用户端**、**短剧管理后台**、**移动端 H5/小程序**、**AI 节点编排** 能力，并提供对接 TOS 等对象存储的上传链路。

> 适用场景：互动短剧投放与运营、剧情分支数据采集、用户增长转化漏斗、内容审核工作流。

## 🧩 端到端架构

```
                    ┌─────────────────────────────────────┐
                    │           管理后台 (Web)             │
                    │   ruoyi-fastapi-frontend (Vue3)    │
                    │   Element Plus + Vite · :5188       │
                    └──────────────┬──────────────────────┘
                                   │ HTTPS / JWT
                                   ▼
┌─────────────────────┐    ┌─────────────────────────────────────┐
│  移动端 (uni-app)   │    │          后端 API (FastAPI)          │
│  mobile-app         │◀──▶│   ruoyi-fastapi-backend              │
│  Vue3 + Vite + TW   │    │   SQLAlchemy · MySQL/PG · Redis      │
│  H5 / 小程序        │    │   · OAuth2 + JWT · :19199            │
└─────────────────────┘    └──────┬───────────────┬───────────────┘
                                  │               │
                                  ▼               ▼
                         ┌────────────┐    ┌────────────┐
                         │  MySQL/PG  │    │   Redis    │
                         │  业务数据  │    │  缓存/限流 │
                         └────────────┘    └────────────┘
                                  │
                                  ▼
                         ┌────────────────────────────────────┐
                         │ 对象存储 (TOS / S3 兼容)           │
                         │ 短剧视频 / 海报 / 分片上传         │
                         └────────────────────────────────────┘
```

## ✨ 核心能力

### C 端（短剧用户端）
- Feed 流推荐、点赞、收藏、评论
- **互动节点** —— 剧情分支选择，关键节点埋点
- 广告位接入、用户成长体系
- 鉴权：`/api/auth/*`（登录），`/api/app/*` 与 `/api/*` 别名共存

### 管理后台
- 短剧 CRUD、视频节点编排、剧集管理
- 内容审核工作流、TOS 预签名分片上传
- 用户、订单、数据统计、运营位管理
- 完整 RuoYi 体系：用户/角色/菜单/部门/字典/参数/日志/定时任务/监控/代码生成/AI 对话

### 移动端
- uni-app + Vue3 + Tailwind，H5 / 微信小程序 / 多端编译
- 登录走 `/api/auth/*`，业务走 `VITE_APP_API_PREFIX=/api/app`

## 🧱 技术栈

| 端 | 技术 |
| --- | --- |
| **后端** | FastAPI · SQLAlchemy · Pydantic · Alembic · MySQL 5.7+ / PostgreSQL · Redis 6.2+ · OAuth2 + JWT · ruoyi CLI |
| **管理后台** | Vue 3 · Vite · Element Plus · Pinia · Vue Router · Axios |
| **移动端** | uni-app · Vue 3 · Vite · Tailwind CSS · pnpm |
| **存储** | TOS（对象存储）/ S3 兼容 · 预签名分片上传 |
| **AI** | 多模型适配（见 `ruoyi-fastapi-backend/module_ai/`） |
| **运维** | Docker Compose · Nginx · Gunicorn/Uvicorn |

## 📁 仓库结构

```
ai-interactive-drama/
├── ruoyi-fastapi-backend/        # 后端 API（FastAPI）
│   ├── module_drama/             # 短剧业务模块
│   ├── module_admin/             # RuoYi 后台模块
│   ├── module_ai/                # AI 集成模块
│   ├── module_task/              # 定时任务
│   ├── module_generator/         # 代码生成
│   ├── sql/                      # 初始化与增量 SQL
│   ├── alembic/                  # 数据库迁移
│   ├── docs/                     # CLI / 传输加解密 / 部署文档
│   ├── .env.dev / .env.prod / .env.dockermy / .env.dockerpg
│   └── docker-compose.my.yml / docker-compose.pg.yml
├── ruoyi-fastapi-frontend/       # 管理后台（Vue3）
├── mobile-app/                   # 短剧移动端（uni-app）
├── ruoyi-fastapi-app/            # 若依原生 App（可选）
├── download-page/                # APK 下载页（部署到 Nginx /download-page/）
├── docker-compose.*.yml          # 后端编排
├── CLAUDE.md                     # Claude Code 项目指引
└── CHANGELOG.md                  # 变更日志
```

### 关键路径速查

| 内容 | 路径 |
| --- | --- |
| 短剧业务包 | `ruoyi-fastapi-backend/module_drama/` |
| 短剧后台页面 | `ruoyi-fastapi-frontend/src/views/drama/` |
| 短剧后台 API 封装 | `ruoyi-fastapi-frontend/src/api/drama/index.js` |
| 新建库 SQL | `ruoyi-fastapi-backend/sql/drama_tables_mvp_mysql.sql` |
| 已有库增量 | `ruoyi-fastapi-backend/sql/drama_tables_align_v2_mysql.sql` |
| 平台菜单（首轮） | `ruoyi-fastapi-backend/sql/drama_platform_menu_mysql.sql` |
| 平台菜单（对齐 v2） | `ruoyi-fastapi-backend/sql/drama_platform_menu_v2_mysql.sql` |
| Alembic 迁移 | `250515_drama` → `250516_drama_align_v2` |
| 环境变量样例 | `ruoyi-fastapi-backend/.env.example` |
| CLI 文档 | `ruoyi-fastapi-backend/docs/cli_usage.md` |
| 传输加解密 | `ruoyi-fastapi-backend/docs/transport_crypto_config.md` |

### API 路径别名（节选）

| 别名路径 | 等价路径 |
| --- | --- |
| `GET /api/app/feed` | `GET /api/feed` |
| `POST /api/app/like` | `POST /api/likes` |
| `POST /api/app/favorite` | `POST /api/favorites` |
| `POST /api/admin/upload/sign` | `POST /api/admin/drama/upload/sign` |

完整接口见后端 OpenAPI：`http://localhost:19199/docs`

## 🚀 快速开始

### 0. 前置依赖

| 工具 | 版本 |
| --- | --- |
| Python | ≥ 3.10 |
| Node.js | ≥ 18 |
| pnpm | ≥ 8（移动端） |
| MySQL | ≥ 5.7（或 PostgreSQL ≥ 12） |
| Redis | ≥ 6.2 |

### 1. 克隆

```bash
git clone https://github.com/flowerjunjie/ai-interactive-drama.git
cd ai-interactive-drama
```

### 2. 后端

```bash
cd ruoyi-fastapi-backend

# 安装依赖（MySQL）
pip install -r requirements.txt
# PostgreSQL 用户改用：pip install -r requirements-pg.txt

# 复制环境变量并按需修改
cp .env.example .env.dev

# 初始化数据库
#   1) 新建数据库 ruoyi_fastapi（默认名，可改）
#   2) 导入 sql/ruoyi-fastapi.sql（MySQL）或 sql/ruoyi-fastapi-pg.sql（PG）
#   3) 短剧表可由 ORM 自动创建，或手动执行 sql/drama_tables_mvp_mysql.sql

# 启动（默认端口 19199）
ruoyi app run --env=dev

# 健康检查：浏览器访问 http://localhost:19199/docs
```

> 💡 `ruoyi` CLI 必须在 `ruoyi-fastapi-backend/` 目录下执行，且以 `python -m` 形式或已安装入口运行。

### 3. 管理后台

```bash
cd ruoyi-fastapi-frontend

# 推荐使用 npmmirror 国内镜像
npm install --registry=https://registry.npmmirror.com

npm run dev   # 默认 http://localhost:5188
```

默认账号：`admin` / `admin123`（**生产环境请立即修改**）

### 4. 短剧移动端

```bash
cd mobile-app

# 推荐使用 npmmirror 国内镜像
pnpm config set registry https://registry.npmmirror.com
pnpm install

pnpm dev:h5               # H5 开发
pnpm dev:mp-weixin         # 微信小程序开发（默认）
pnpm build:mp-weixin       # 生产构建
```

> `VITE_APP_API_PREFIX` 默认 `/api/app`，登录走 `/api/auth/*`。详见 `mobile-app/README.md`。

## ⚙️ 环境变量

后端 `ruoyi-fastapi-backend/.env.dev` 关键项（完整列表见 `.env.example`）：

| 变量 | 说明 | 默认 |
| --- | --- | --- |
| `APP_PORT` | API 端口 | `19199` |
| `MYSQL_HOST` / `MYSQL_PORT` / `MYSQL_USER` / `MYSQL_PASSWORD` / `MYSQL_DATABASE` | 数据库连接 | 见 `.env.dev` |
| `REDIS_HOST` / `REDIS_PORT` / `REDIS_DATABASE` | Redis 连接 | `127.0.0.1:6379/2` |
| `JWT_SECRETKEY` | JWT 签名密钥 | **必须修改** |
| `TOS_*` | 对象存储凭证 | 上传功能需配 |

前端 `ruoyi-fastapi-frontend/.env.development`：

| 变量 | 说明 |
| --- | --- |
| `VITE_APP_BASE_API` | 后端地址 |
| `VITE_APP_TITLE` | 站点标题 |

## 🛠 CLI 常用命令

> 所有命令均在 `ruoyi-fastapi-backend/` 目录下执行。

```bash
# 启动 / 诊断
ruoyi app run   --env=dev               # 启动
ruoyi app doctor --env=dev              # 启动前健康检查（推荐）
ruoyi app routes --env=dev              # 列出全部路由

# 数据库
ruoyi db upgrade   --env=dev --revision=head --yes
ruoyi db revision  --env=dev --message="..." --autogenerate --yes

# 缓存
ruoyi cache clear --env=dev --all --yes

# 代码风格
ruoyi dev lint
```

## 📦 发布与部署

### 前端生产构建

```bash
cd ruoyi-fastapi-frontend
npm run build:prod   # 产物在 dist/
```

### 后端生产

```bash
cd ruoyi-fastapi-backend
# 配置 .env.prod 后
ruoyi app run --env=prod
```

### Docker Compose

```bash
# MySQL 编排
docker compose -f docker-compose.my.yml up -d --build

# PostgreSQL 编排
docker compose -f docker-compose.pg.yml up -d --build

# 仅短剧业务编排（叠加）
docker compose -f docker-compose.drama.yml up -d --build
```

> ⚠️ 默认 compose **未做数据持久化**，上线前请配置 volume 与定期备份。备份样例见 `backups/`。

### Nginx 反向代理（示例）

```nginx
location /api/ {
    proxy_pass http://127.0.0.1:19199/api/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
location /download-page/ {
    alias /opt/ai-interactive-drama/download-page/;
    autoindex off;
}
```

## 🩺 故障排查（Troubleshooting）

| 症状 | 可能原因 | 解决 |
| --- | --- | --- |
| `ruoyi: command not found` | CLI 未安装或不在 PATH | `pip install -e .` 或检查 `requirements.txt`；确认在 `ruoyi-fastapi-backend/` 下执行 |
| 启动报 `pymysql.err.OperationalError` | 数据库连接失败 | 检查 `MYSQL_*` 环境变量；确认 MySQL 已启动且账号可远程登录 |
| 启动报 `redis.exceptions.ConnectionError` | Redis 未启动 | `redis-server` 或 `brew services start redis`；检查 `REDIS_*` |
| 前端 `npm install` 超时 | 默认 registry 慢 | 加 `--registry=https://registry.npmmirror.com` |
| 前端 `5173`/`5188` 被占用 | 端口冲突 | 修改 `vite.config.js` 中 `server.port` |
| 后端 `19199` 被占用 | 端口冲突 | 修改 `.env.dev` 中 `APP_PORT` |
| 接口 401 | JWT 过期 / 未登录 | 重新登录；检查 `JWT_SECRETKEY` 是否变更导致旧 token 失效 |
| `git push` SSH 失败 | 默认 key 不匹配 | 仓库已配 `core.sshCommand`，如新环境 clone 请确保 `~/.ssh/id_rsa` 可用 |
| 短剧表缺失 | 增量 SQL 未执行 | 执行 `sql/drama_tables_mvp_mysql.sql` 或 `sql/drama_tables_align_v2_mysql.sql` |
| 上传 403 / 签名失败 | TOS 凭证错误 | 检查 `.env.dev` 中 `TOS_*` 与对象存储控制台密钥是否一致 |
| Alembic 与 ORM 冲突 | 自定义字段未迁移 | `ruoyi db revision --autogenerate` 后 review 再 `upgrade` |

## 🧪 验收清单

- [ ] `GET http://localhost:19199/docs` 可见 OpenAPI 文档
- [ ] 管理后台 `http://localhost:5188` 用 `admin/admin123` 登录成功
- [ ] 短剧列表页可见示例数据（执行 SQL 后）
- [ ] 移动端 H5 在浏览器能看到首页
- [ ] `ruoyi app doctor --env=dev` 全绿

## 🗺 路线图

- [x] 短剧 MVP 表结构与后台 CRUD
- [x] TOS 分片上传
- [x] 互动节点编排
- [ ] 软著申请
- [ ] 应用商店上架
- [ ] AI 节点推荐增强（Round 2200+ 迭代）

完整变更记录见 [CHANGELOG.md](./CHANGELOG.md) · 工作日志见 [.worklog/WORKLOG.md](./.worklog/WORKLOG.md)

## 🤝 贡献

欢迎 Issue 与 PR。本项目遵循若依代码风格，建议提交前：

```bash
cd ruoyi-fastapi-backend
ruoyi dev lint
```

完整贡献指南：[CONTRIBUTING.md](./CONTRIBUTING.md) · 行为准则：[CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md) · 路线图：[ROADMAP.md](./ROADMAP.md) · 本版本说明：[docs/releases/v1.0.0.md](./docs/releases/v1.0.0.md)

安全漏洞披露：[SECURITY.md](./SECURITY.md) · **请勿在公开 Issue 披露安全问题**

GitHub 仓库配置清单（Topics / Social Preview / Discussions / Release）：[docs/github-setup-todo.md](./docs/github-setup-todo.md)

## 📄 许可证

本项目基于 [MIT License](./LICENSE) 开源。

## 🙏 致谢

本项目基于以下开源项目二次开发：

- [RuoYi-Vue3-FastAPI](https://gitee.com/insistence2022/RuoYi-Vue3-FastAPI)
- [RuoYi-Vue3](https://github.com/yangzongzhuan/RuoYi-Vue3)
- [RuoYi-App](https://github.com/yangzongzhuan/RuoYi-App)

## ⭐ Star History

<a href="https://github.com/flowerjunjie/ai-interactive-drama/stargazers">
  <img src="https://api.star-history.com/svg?repos=flowerjunjie/ai-interactive-drama&type=Date" alt="Star History Chart">
</a>