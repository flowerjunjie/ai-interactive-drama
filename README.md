<h1 align="center" style="margin: 30px 0 30px; font-weight: bold;">AI Interactive Drama</h1>
<h4 align="center">AI 互动短剧平台 · 基于 RuoYi-Vue3 + FastAPI</h4>
<p align="center">
    <a href="https://gitee.com/min1314/ai-interactive-drama">
        <img alt="Gitee" src="https://gitee.com/min1314/ai-interactive-drama/badge/star.svg?theme=dark">
    </a>
    <img alt="project version" src="https://img.shields.io/badge/version-1.9.0-brightgreen.svg">
    <img alt="LICENSE" src="https://img.shields.io/github/license/mashape/apistatus.svg">
    <img alt="node version" src="https://img.shields.io/badge/node-≥18-blue">
    <img alt="python version" src="https://img.shields.io/badge/python-≥3.10-blue">
    <img alt="mysql version" src="https://img.shields.io/badge/MySQL-≥5.7-blue">
    <img alt="redis version" src="https://img.shields.io/badge/redis-≥6.2-blue">
</p>

## 平台简介

AI Interactive Drama 是一套 **AI 互动短剧** 业务平台，在 [RuoYi-Vue3-FastAPI](https://gitee.com/insistence2022/RuoYi-Vue3-FastAPI) 基础上扩展短剧 C 端、管理后台与移动端能力。

| 端 | 技术栈 | 目录 |
| --- | --- | --- |
| 管理后台 | Vue3、Element Plus | `ruoyi-fastapi-frontend/` |
| 短剧移动端 | uni-app、Vue3、Vite、Tailwind CSS | `mobile-app/` |
| 后端 API | FastAPI、SQLAlchemy、MySQL、Redis、OAuth2 & JWT | `ruoyi-fastapi-backend/` |
| 若依原生 App | uni-app（可选） | `ruoyi-fastapi-app/` |

**短剧核心能力**

- C 端：Feed 流、点赞收藏、评论、互动节点、广告位
- 后台：短剧管理、视频节点、审核、上传（TOS 预签名）、用户与数据统计
- 认证：C 端 `/api/auth/*`，业务 `/api/*` 与 `/api/app/*` 规格别名并存

## 项目结构

| 模块 | 路径说明 |
| --- | --- |
| 后端业务包 | `ruoyi-fastapi-backend/module_drama` |
| 管理端页面 | `ruoyi-fastapi-frontend/src/views/drama/*` |
| 管理端 API | `ruoyi-fastapi-frontend/src/api/drama/index.js` |
| 表结构（新建库） | `ruoyi-fastapi-backend/sql/drama_tables_mvp_mysql.sql` |
| 表结构增量（已有库） | `ruoyi-fastapi-backend/sql/drama_tables_align_v2_mysql.sql` |
| 管理端菜单 SQL（首轮） | `ruoyi-fastapi-backend/sql/drama_platform_menu_mysql.sql` |
| 管理端菜单对齐 SQL | `ruoyi-fastapi-backend/sql/drama_platform_menu_v2_mysql.sql` |
| Alembic 迁移 | `250515_drama` → `250516_drama_align_v2` |
| 移动端 | `mobile-app/`（默认 `VITE_APP_API_PREFIX=/api/app`，登录 `/api/auth/*`） |
| 环境变量示例 | `ruoyi-fastapi-backend/.env.example` |

**规格路径对照（节选）**

- `GET /api/app/feed` ↔ `GET /api/feed`
- `POST /api/app/like`、`POST /api/app/favorite` ↔ `POST /api/likes`、`POST /api/favorites`
- `POST /api/admin/upload/sign|complete` ↔ `/api/admin/drama/upload/sign|complete`

接口详情见后端 OpenAPI：`http://localhost:19199/docs`（开发环境默认端口，见 `.env.dev` 中 `APP_PORT`）。

## 快速开始

```bash
# 克隆项目
git clone https://gitee.com/min1314/ai-interactive-drama.git

# 进入项目根目录
cd ai-interactive-drama
```

### 后端

```bash
cd ruoyi-fastapi-backend

# MySQL
pip install -r requirements.txt
# PostgreSQL
# pip install -r requirements-pg.txt

# 在 .env.dev 中配置数据库与 Redis
# 1. 新建数据库 ruoyi-fastapi（默认名，可改）
# 2. 执行 sql/ruoyi-fastapi.sql（MySQL）或 ruoyi-fastapi-pg.sql（PostgreSQL）
# 3. 短剧表：启动时 ORM 自动建表，或手动执行 sql/drama_tables_mvp_mysql.sql

ruoyi app run --env=dev
```

CLI 说明：[ruoyi-fastapi-backend/docs/cli_usage.md](./ruoyi-fastapi-backend/docs/cli_usage.md)

传输层加解密：[ruoyi-fastapi-backend/docs/transport_crypto_config.md](./ruoyi-fastapi-backend/docs/transport_crypto_config.md)

### 管理后台

```bash
cd ruoyi-fastapi-frontend

npm install --registry=https://registry.npmmirror.com
npm run dev
```

默认访问：`http://localhost:5188`（见 `vite.config.js`）

默认账号：`admin` / `admin123`

### 短剧移动端

```bash
cd mobile-app

pnpm install
pnpm dev:h5
```

详细说明：[mobile-app/README.md](./mobile-app/README.md)

## 内置功能（若依基础）

除短剧业务外，继承 RuoYi-Vue3-FastAPI 全套管理能力：用户/角色/菜单/部门/字典/参数/日志/定时任务/监控/代码生成/AI 对话等。完整列表见 [上游 README](https://gitee.com/insistence2022/RuoYi-Vue3-FastAPI)。

## 发布与部署

### 前端构建

```bash
cd ruoyi-fastapi-frontend
npm run build:prod
```

### 后端生产

```bash
cd ruoyi-fastapi-backend
# 配置 .env.prod 后
ruoyi app run --env=prod
```

### Docker Compose

> 默认未做数据持久化，请注意备份或自行配置持久化。

```bash
# MySQL
docker compose -f docker-compose.my.yml up -d --build

# PostgreSQL
docker compose -f docker-compose.pg.yml up -d --build
```

## 致谢

本项目基于以下开源项目二次开发：

- [RuoYi-Vue3-FastAPI](https://gitee.com/insistence2022/RuoYi-Vue3-FastAPI)
- [RuoYi-Vue3](https://github.com/yangzongzhuan/RuoYi-Vue3)
- [RuoYi-App](https://github.com/yangzongzhuan/RuoYi-App)
