# Show HN · Draft

> **Status**: Draft for HackerNews Show HN submission
> **Repo**: https://github.com/flowerjunjie/ai-interactive-drama
> **Target post time**: Tuesday–Thursday, US East 8-10am

---

## Title (≤ 80 chars)

```
Show HN: Open-source AI interactive drama platform (FastAPI + Vue3 + uni-app)
```

> ✅ No "best/awesome/amazing" — HN penalizes hype
> ✅ Says what it is + tech stack
> ❌ Avoid: "I built", "look at my project", "revolutionary"

## URL to submit

`https://github.com/flowerjunjie/ai-interactive-drama`

## First Comment (post immediately after submission)

```
Hi HN,

We built and open-sourced a complete AI interactive drama platform — the
backend that powers a short-drama C-end (web + H5 + mini-program) with
branching interactive nodes, like a "choose your own adventure" video
service that has been booming in China.

Stack: FastAPI + SQLAlchemy 2 (async) + MySQL/PostgreSQL + Redis on the
backend; Vue 3 + Element Plus for the admin; uni-app + Tailwind for the
mobile client (compiles to H5, WeChat mini-program, MP, etc.).

What you get out of the box:
- C-end Feed, like/favorite, comment, and interactive node picker
- Admin for drama CRUD, node editing, review workflow
- TOS / S3-compatible pre-signed multipart upload with resume
- Alembic migrations, CLI tooling, OAuth2 + JWT auth, ruoyi admin base

It is built on top of the RuoYi-Vue3-FastAPI admin scaffold (which itself
has 8k+ stars on Gitee), so the admin side inherits the standard user/
role/menu/dept/dict/monitor/AI features.

We are at v1.9.0 (admin) and 1.0.1 (mobile), MIT licensed.

Why open-source: short-drama systems in China are mostly closed Java/Spring
stacks. There is very little readable, modifiable, commercially-usable code
in this niche. We hope this fills a gap.

Looking for: feedback on the architecture, code review, contributors for
the AI node recommendation engine, and honest criticism.

GitHub: https://github.com/flowerjunjie/ai-interactive-drama
Docs: see README in-repo
```

## Risk-mitigation reminders

- ❌ Do NOT include "we are looking for stars" or any upvote-begging
- ❌ Do NOT cross-post to Reddit same day
- ✅ Reply to every question within 1 hour for first 6 hours
- ✅ Have a self-hosted demo or clear setup instructions ready
- ✅ Be ready to defend the architecture choices (Why FastAPI? Why not Java?)

## Follow-up timing (Day plan)

| Hour | Action |
| --- | --- |
| 0   | Post + first comment |
| 1   | Reply to all early comments |
| 3   | If trending top 30, prepare longer write-up as blog post |
| 6   | Final sweep on unanswered threads |
| 24  | Triage any bugs reported into Issues |
| 48  | Write up "what we learned from HN" retrospective |