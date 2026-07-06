<h1 align="center">AI Interactive Drama</h1>
<h4 align="center">Open-source AI-powered interactive short-drama platform · FastAPI + Vue3 + uni-app</h4>

<p align="center">
  <a href="#english">🇬🇧 English</a> · <a href="./README.md">🇨🇳 中文</a>
</p>

<p align="center">
  <a href="https://github.com/flowerjunjie/ai-interactive-drama/stargazers">
    <img alt="GitHub stars" src="https://img.shields.io/github/stars/flowerjunjie/ai-interactive-drama?style=social">
  </a>
  <a href="https://github.com/flowerjunjie/ai-interactive-drama/network/members">
    <img alt="GitHub forks" src="https://img.shields.io/github/forks/flowerjunjie/ai-interactive-drama?style=social">
  </a>
  <img alt="release" src="https://img.shields.io/github/v/release/flowerjunjie/ai-interactive-drama">
  <img alt="license" src="https://img.shields.io/github/license/flowerjunjie/ai-interactive-drama">
  <img alt="python" src="https://img.shields.io/badge/python-≥3.10-blue">
  <img alt="node" src="https://img.shields.io/badge/node-≥18-blue">
</p>

---

## 📌 What is this?

**AI Interactive Drama** is a complete, production-tested open-source platform for building
AI-driven interactive short-drama apps. It is built on top of the well-known
[RuoYi-Vue3-FastAPI](https://gitee.com/insistence2022/RuoYi-Vue3-FastAPI) admin scaffold
and adds three concrete capabilities for the short-drama domain:

- **C-end**: feed, like/favorite, comment, **interactive node picker** (branching narrative)
- **Admin**: drama CRUD, node editor, review workflow, TOS multipart upload, ops dashboards
- **Mobile**: uni-app + Vue3 + Tailwind, compiles to H5 / WeChat mini-program / MP

The platform targets the booming short-drama market (interactive fiction for mobile users
in China and increasingly SEA). Whether you want a Netflix-style "choose your own adventure"
video service or an internal authoring tool for branching narratives, this is the
full-stack starting point.

## 🧩 End-to-end Architecture

```
                    ┌─────────────────────────────────────┐
                    │           Admin Web (Vue3)           │
                    │   ruoyi-fastapi-frontend · :5188    │
                    └──────────────┬──────────────────────┘
                                   │ HTTPS / JWT
                                   ▼
┌─────────────────────┐    ┌─────────────────────────────────────┐
│  Mobile (uni-app)   │    │          Backend API (FastAPI)       │
│  mobile-app         │◀──▶│   ruoyi-fastapi-backend · :19199     │
│  Vue3 + Vite + TW   │    │   SQLAlchemy 2.0 async · MySQL/PG    │
│  H5 / MiniProgram   │    │   · OAuth2 + JWT · Redis · Alembic   │
└─────────────────────┘    └──────┬───────────────┬───────────────┘
                                  │               │
                                  ▼               ▼
                         ┌────────────┐    ┌────────────┐
                         │  MySQL/PG  │    │   Redis    │
                         │  business  │    │ cache/rate │
                         └────────────┘    └────────────┘
                                  │
                                  ▼
                         ┌────────────────────────────────────┐
                         │ Object Storage (TOS / S3)          │
                         │ multipart upload + resume          │
                         └────────────────────────────────────┘
```

## ✨ Core Capabilities

### C-end (user-facing)

- Feed with simple rule-based ranking (age / region / history / tag affinity)
- Like, favorite, comment
- **Interactive node picker** — branching narrative, key events instrumented
- OAuth2 + JWT auth (`/api/auth/*`)
- API aliasing: `/api/app/*` ↔ `/api/*` (mobile + web both work)

### Admin

- Drama CRUD, episode management, node editor (tree view)
- Review workflow: draft → pending → online
- TOS / S3-compatible **pre-signed multipart upload with resume**
- Full RuoYi admin base: user / role / menu / dept / dict / monitor / code-gen / AI chat
- Alembic migrations, `ruoyi` CLI (`app run | doctor | routes | db upgrade | cache clear | lint`)

### Mobile

- uni-app + Vue3 + Tailwind, single codebase for H5 / mini-program / MP
- Default API prefix: `VITE_APP_API_PREFIX=/api/app`

## 🧱 Tech Stack

| Layer | Tech |
| --- | --- |
| **Backend** | FastAPI · SQLAlchemy 2.0 async · Pydantic v2 · Alembic · MySQL 5.7+ / PostgreSQL 12+ · Redis 6.2+ · OAuth2 + JWT |
| **Admin Web** | Vue 3 · Vite · Element Plus · Pinia · Vue Router 4 · Axios |
| **Mobile** | uni-app · Vue 3 · Vite · Tailwind CSS · pnpm |
| **Storage** | TOS / S3-compatible, pre-signed multipart upload |
| **AI** | Multi-model adapter (see `ruoyi-fastapi-backend/module_ai/`) |
| **Ops** | Docker Compose · Nginx · Gunicorn / Uvicorn |

## 🚀 Quick Start (5 minutes)

### Prerequisites

| Tool | Version |
| --- | --- |
| Python | ≥ 3.10 |
| Node.js | ≥ 18 |
| pnpm | ≥ 8 (mobile) |
| MySQL | ≥ 5.7 (or PostgreSQL ≥ 12) |
| Redis | ≥ 6.2 |

### 1. Clone

```bash
git clone https://github.com/flowerjunjie/ai-interactive-drama.git
cd ai-interactive-drama
```

Or use the one-shot bootstrap:

```bash
./scripts/setup-dev.sh    # backend + admin + mobile, all idempotent
```

### 2. Backend

```bash
cd ruoyi-fastapi-backend

pip install -r requirements.txt
cp .env.example .env.dev          # edit DB / Redis / JWT settings

# Init DB
#   1) Create database ruoyi_fastapi (default name)
#   2) Import sql/ruoyi-fastapi.sql
#   3) Drama tables: ORM auto-creates on first run, or run sql/drama_tables_mvp_mysql.sql manually

ruoyi app doctor --env=dev        # pre-flight health check
ruoyi app run --env=dev           # http://localhost:19199/docs
```

### 3. Admin Web

```bash
cd ruoyi-fastapi-frontend
npm install --registry=https://registry.npmmirror.com
npm run dev                        # http://localhost:5188
```

Default credentials: `admin` / `admin123` — **change before production**.

### 4. Mobile (H5)

```bash
cd mobile-app
pnpm config set registry https://registry.npmmirror.com
pnpm install
pnpm dev:h5
```

## 🐳 Docker

```bash
docker compose -f docker-compose.my.yml up -d --build   # MySQL bundle
docker compose -f docker-compose.pg.yml up -d --build   # PostgreSQL bundle
```

> ⚠️ Bundles do NOT persist data by default — add volumes for production.

## 📚 Documentation

- [Chinese README](./README.md) · 中文版完整说明
- [ROADMAP.md](./ROADMAP.md) · Q3 SaaS / Q4 commercial / Q1 AI direction
- [CONTRIBUTING.md](./CONTRIBUTING.md) · how to contribute
- [SECURITY.md](./SECURITY.md) · vulnerability disclosure (please read before filing issues)
- [docs/releases/v1.0.0.md](./docs/releases/v1.0.0.md) · release notes
- [docs/risks.md](./docs/risks.md) · risk register
- [docs/adr/](./docs/adr/) · architecture decision records

## 🩺 Troubleshooting (top 5)

| Symptom | Fix |
| --- | --- |
| `ruoyi: command not found` | Run from `ruoyi-fastapi-backend/`; or `pip install -e .` |
| `pymysql.err.OperationalError` | Check `MYSQL_*` env vars; confirm MySQL is up |
| `redis.exceptions.ConnectionError` | Start `redis-server`; check `REDIS_*` |
| `npm install` timeout | Add `--registry=https://registry.npmmirror.com` |
| API returns 401 | JWT expired or `JWT_SECRETKEY` changed |

See [README.md Troubleshooting](./README.md#-故障排查troubleshooting) for the full matrix.

## 🛡️ Security

- See [SECURITY.md](./SECURITY.md) for the vulnerability disclosure process (please do NOT file public issues for security bugs)
- CodeQL weekly scan enabled in CI
- Dependabot auto-updates enabled

## 🤝 Contributing

PRs and Issues welcome. Please read [CONTRIBUTING.md](./CONTRIBUTING.md) first.
The project follows Conventional Commits.

```bash
# Pre-commit (recommended)
pip install pre-commit && pre-commit install

# Backend lint
cd ruoyi-fastapi-backend && ruoyi dev lint
```

## 📜 License

[MIT](./LICENSE) © 2024-2026 insistence & flowerjunjie

## 🙏 Credits

Built on:

- [RuoYi-Vue3-FastAPI](https://gitee.com/insistence2022/RuoYi-Vue3-FastAPI) (8k+ stars on Gitee)
- [RuoYi-Vue3](https://github.com/yangzongzhuan/RuoYi-Vue3)
- [RuoYi-App](https://github.com/yangzongzhuan/RuoYi-App)

## ⭐ Star History

<a href="https://github.com/flowerjunjie/ai-interactive-drama/stargazers">
  <img src="https://api.star-history.com/svg?repos=flowerjunjie/ai-interactive-drama&type=Date" alt="Star History Chart">
</a>