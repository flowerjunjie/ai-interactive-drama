# ⚠️ 风险登记册（Risk Register）

> 记录**已知风险**与**缓解措施**。新增风险请 PR 追加，按"严重度 × 概率"评估优先级。
>
> 严重度：🔴 Critical（业务中断 / 数据丢失）/ 🟠 High（功能受损）/ 🟡 Medium（体验下降）/ 🟢 Low（边缘 case）
> 概率：📈 Likely（>30%）/ 〰️ Possible（5-30%）/ 📉 Unlikely（<5%）

---

## 🔴 R-001 · 默认 `admin / admin123` 未改

- **严重度**：🔴 Critical
- **概率**：📈 Likely（90% 新部署忘记改）
- **影响**：攻击者拿到后台完全控制权，可删改所有业务数据
- **缓解**：
  - ✅ README 已加生产警示
  - ✅ 启动脚本检测默认密码并 warn
  - 🟡 待办：首次登录强制改密（已入 Roadmap）
- **Owner**：TBD
- **状态**：缓解中

---

## 🔴 R-002 · JWT `SECRETKEY` 泄露或默认值

- **严重度**：🔴 Critical
- **概率**：〰️ Possible
- **影响**：伪造任意用户 token，越权访问
- **缓解**：
  - ✅ `.env.example` 给的是占位符，部署必改
  - ✅ README Troubleshooting 矩阵已列出
  - 🟡 待办：启动时若 SECRETKEY 为占位值直接拒绝启动
- **Owner**：TBD
- **状态**：缓解中

---

## 🟠 R-003 · CORS 默认放开

- **严重度**：🟠 High
- **概率**：📈 Likely（开发环境配置容易遗留到生产）
- **影响**：恶意网站可跨域调用 API
- **缓解**：
  - 🟡 待办：生产环境强制白名单 + 启动时检测
  - 🟡 待办：`.env.prod` 中 `CORS_ALLOW_ORIGINS` 强校验
- **Owner**：TBD
- **状态**：未缓解

---

## 🟠 R-004 · SQL 注入

- **严重度**：🟠 High
- **概率**：📉 Unlikely（SQLAlchemy ORM 防护）
- **影响**：数据库被读/写/删
- **缓解**：
  - ✅ 全量使用 SQLAlchemy ORM，禁止裸 SQL
  - ✅ CodeQL 安全扫描每周运行
- **Owner**：TBD
- **状态**：已缓解

---

## 🟠 R-005 · TOS / S3 凭证泄露

- **严重度**：🟠 High
- **概率**：〰️ Possible
- **影响**：攻击者可上传恶意文件 / 删除线上资源 / 巨额账单
- **缓解**：
  - ✅ 使用专用子账号 + 最小权限（仅当前 bucket）
  - ✅ 凭证走环境变量，不入库
  - ✅ 预签名 URL 有效期默认 1 小时（建议缩短到 5-15 分钟）
  - 🟡 待办：开启 TOS 服务端访问日志与异常告警
- **Owner**：TBD
- **状态**：缓解中

---

## 🟡 R-006 · 依赖供应链攻击

- **严重度**：🟡 Medium
- **概率**：📉 Unlikely
- **影响**：恶意代码通过 pip / npm 包植入
- **缓解**：
  - ✅ Dependabot 自动监测 + 周更
  - 🟡 待办：CI 集成 `pip-audit` 与 `npm audit`
  - 🟡 待办：核心依赖固定 hash（`pip install --require-hashes`）
- **Owner**：TBD
- **状态**：部分缓解

---

## 🟡 R-007 · Alembic 迁移与 ORM 漂移

- **严重度**：🟡 Medium
- **概率**：〰️ Possible
- **影响**：本地能跑、线上炸；或反之
- **缓解**：
  - ✅ 强制 PR 流程：`autogenerate` 后必须人工 review 再 `upgrade`
  - ✅ 迁移脚本随 PR 提交，code owner review
  - 🟡 待办：CI 跑 `alembic check` 检测漂移
- **Owner**：TBD
- **状态**：缓解中

---

## 🟡 R-008 · 上传大文件 OOM

- **严重度**：🟡 Medium
- **概率**：📉 Unlikely（前端分片限制）
- **影响**：后端进程被恶意大文件撑爆
- **缓解**：
  - ✅ 前端分片 5 MB 上限
  - ✅ 后端校验单片大小
  - 🟡 待办：Nginx `client_max_body_size` 限制
- **Owner**：TBD
- **状态**：已缓解

---

## 🟢 R-009 · XSS via `v-html` / `dangerouslySetInnerHTML`

- **严重度**：🟢 Low（Vue3 默认转义）
- **概率**：📉 Unlikely
- **影响**：管理员后台被钓鱼
- **缓解**：
  - ✅ CodeQL 检测可疑用法
  - 🟡 待办：ESLint 规则禁止 `v-html` + 强制 `DOMPurify` 包裹
- **Owner**：TBD
- **状态**：缓解中

---

## 🟢 R-010 · Redis 未授权访问

- **严重度**：🟢 Low（仅本地 Redis）
- **概率**：📉 Unlikely
- **影响**：攻击者读 / 写所有缓存
- **缓解**：
  - ✅ `.env.dev` 中 Redis 默认带密码占位
  - 🟡 待办：生产 compose 强制 Redis 密码 + bind 127.0.0.1
- **Owner**：TBD
- **状态**：缓解中

---

## 🟢 R-011 · 短剧内容审核绕过

- **严重度**：🟢 Low
- **概率**：〰️ Possible
- **影响**：违规内容上线（合规风险）
- **缓解**：
  - ✅ 后台审核工作流：草稿 → 待审 → 上下架
  - 🟡 待办：接入 AI 审核 + 关键词过滤
- **Owner**：TBD
- **状态**：缓解中

---

## 🟢 R-012 · Docker 镜像体积过大

- **严重度**：🟢 Low
- **概率**：📉 Unlikely
- **影响**：CI / 部署耗时、存储成本
- **缓解**：
  - ✅ 已加 `.dockerignore`
  - 🟡 待办：多阶段构建 + Alpine 基础镜像（已入 Roadmap）
- **Owner**：TBD
- **状态**：部分缓解

---

## 📊 风险热力图

```
        📉 Unlikely   〰️ Possible    📈 Likely
🔴 Crit  R-004, R-008,    R-002, R-005     R-001
🟠 High                    R-003, R-007
🟡 Med   R-006, R-012      R-007 (overlap)
🟢 Low   R-009, R-010      R-011
```

## 🔄 更新流程

1. 发现新风险 → 开 Issue 标签 `risk`
2. 评估严重度 + 概率 → 落入对应象限
3. 给出缓解方案 → 加入"缓解中"或"已缓解"
4. 季度回顾：移出已闭环风险，标注新出现风险