# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AI Interactive Drama is a platform for AI-powered interactive short dramas, built on RuoYi-Vue3 + FastAPI. The project has four main components:

| Component | Tech Stack | Directory |
|-----------|-----------|-----------|
| Admin Backend | FastAPI, SQLAlchemy, MySQL, Redis | `ruoyi-fastapi-backend/` |
| Admin Frontend | Vue3, Element Plus | `ruoyi-fastapi-frontend/` |
| Mobile App | uni-app, Vue3, Vite, Tailwind CSS | `mobile-app/` |
| RuoYi App (optional) | uni-app | `ruoyi-fastapi-app/` |

## Common Commands

### Backend (run from `ruoyi-fastapi-backend/`)

```bash
# Install dependencies
pip install -r requirements.txt  # MySQL
pip install -r requirements-pg.txt  # PostgreSQL

# Start development server (port 19199)
ruoyi app run --env=dev

# Pre-flight checks
ruoyi app doctor --env=dev

# Database migrations (Alembic)
ruoyi db upgrade --env=dev --revision=head --yes
ruoyi db revision --env=dev --message="description" --autogenerate --yes

# Cache operations
ruoyi cache clear --env=dev --all --yes

# View routes
ruoyi app routes --env=dev
```

### Frontend Admin (run from `ruoyi-fastapi-frontend/`)

```bash
npm install --registry=https://registry.npmmirror.com
npm run dev      # Development (port 5188)
npm run build:prod  # Production build
```

### Mobile App (run from `mobile-app/`)

```bash
pnpm install
pnpm dev:h5
```

## Architecture

### Backend Module Structure

- `module_drama/` - Drama business logic (controllers, services, entities, aspects)
- `module_admin/` - RuoYi admin system (users, roles, menus, departments)
- `module_ai/` - AI integration module
- `module_generator/` - Code generation module
- `module_task/` - Scheduled tasks module
- `cli/` - CLI commands (`ruoyi` entry point)
- `common/` - Shared utilities, response wrappers
- `config/` - Environment and application configuration
- `middlewares/` - Request/response middleware

### API Path Conventions

- C端认证: `/api/auth/*`
- Business API: `/api/*` and `/api/app/*` (aliased paths coexist)
- Admin upload: `/api/admin/upload/sign|complete`

Example equivalences:
- `GET /api/app/feed` ↔ `GET /api/feed`
- `POST /api/app/like` ↔ `POST /api/likes`

### Drama SQL Migrations

- Initial tables: `sql/drama_tables_mvp_mysql.sql`
- Incremental: `sql/drama_tables_align_v2_mysql.sql`
- Admin menus: `sql/drama_platform_menu_mysql.sql`
- Alembic migrations: `250515_drama` → `250516_drama_align_v2`

## Configuration

- Backend env files: `.env.dev`, `.env.prod`, `.env.dockermy`, `.env.dockerpg`
- Frontend env files: `.env.development`, `.env.production`, `.env.staging`
- Mobile app: `VITE_APP_API_PREFIX=/api/app` (login uses `/api/auth/*`)

Default ports: Backend 19199, Frontend 5188

## Development Notes

- The `ruoyi` CLI must be run from the `ruoyi-fastapi-backend/` directory
- Use `--env=dev` for development, `--env=prod` for production (dangerous commands require `--allow-prod --yes`)
- The CLI reuses `config/env.py` for configuration, not a separate config system
- Run `ruoyi dev lint` before committing to check code style

## Work Log System

Daily work logs are stored in `.worklog/WORKLOG.md` with the following table format:

| 日期 | 当日研发工作内容 | 工作进度 | 遇到的问题及解决方案 | 次日工作计划 |
|------|------------------|----------|---------------------|--------------|