# 🔐 Security Policy

> 本项目对外披露安全漏洞的标准流程。请不要在公开 Issue 中披露漏洞。

## Supported Versions

下表为**当前受支持**的版本范围，**不在范围内**的版本不会有安全更新。

| 版本 | 支持状态 | EOL |
| --- | --- | --- |
| v1.0.x（main 分支） | ✅ 积极维护 | — |
| v0.x（历史快照） | ⚠️ 仅严重漏洞 | 2026-12-31 |

> 安全更新会发 GitHub **Security Advisory** + 在 Releases 中以 `[Security]` 前缀标注。

## 🚨 Reporting a Vulnerability

**请不要**通过公开 Issue / Discussion / PR 报告安全问题。公开披露会给所有用户带来风险。

### 报告方式（按推荐顺序）

#### 1. GitHub Security Advisories（首选 · 推荐 ⭐）

👉 [创建 Private Security Advisory](https://github.com/flowerjunjie/ai-interactive-drama/security/advisories/new)

- 私有 channel，仅维护者可见
- 披露后可协商 CVE 编号
- 修复后可一键发布 GitHub Security Advisory

#### 2. 邮件（备选）

发送邮件到维护者邮箱（见仓库 About 页面），主题前缀：`[SECURITY]`

#### 3. 微信 / Telegram（不推荐 · 仅紧急情况）

联系 maintainer（`flowerjunjie`）。**仅**在 24h 内邮件无响应时使用。

### 报告内容模板

请尽量提供以下信息（信息越多，修复越快）：

```markdown
## 漏洞描述

[一句话描述]

## 影响范围

- 受影响版本：v1.x.x
- 影响组件：[后端 / 管理后台 / 移动端]
- 影响等级：[Critical / High / Medium / Low]

## 复现步骤

1. ...
2. ...

## 概念验证 (PoC)

```bash
curl -X POST ...
```

## 期望行为 / 实际行为

## 已知缓解措施

[如有，附临时方案]

## 您的环境

- OS / Python / Node 版本
- 部署模式（本地 / docker / 生产）

## 联系方式（可选）

- 是否愿意署名
- 是否接受披露时间线协调
```

### 我们承诺

- ✅ **48 小时内**首次响应（确认收到 + 初步评估）
- ✅ 修复时间表协商（Critical: 7 天内；High: 30 天内；Medium/Low: 下一版本）
- ✅ 修复前**不公开**漏洞细节
- ✅ 修复后致谢（除非您要求匿名）
- ✅ 严重漏洞可走**协调披露**流程，与您同步发布时间

## 🛡 Security Best Practices for Users

部署本项目到生产环境时，**必须**做以下配置：

### 后端

- [ ] 修改 `.env.prod` 中 `JWT_SECRETKEY` 为强随机（≥ 32 字节）
- [ ] 修改默认 admin 密码 `admin / admin123`
- [ ] 启用 HTTPS（Let's Encrypt / Nginx）
- [ ] 数据库密码使用专用账号，**不**用 root
- [ ] 关闭 FastAPI docs（`/docs`）外网访问（生产环境 `DEBUG=false`）
- [ ] 启用 CORS 白名单（不要 `allow_origins=["*"]`）

### 对象存储（TOS / S3）

- [ ] 使用专用子账号，**最小权限**（仅当前 bucket）
- [ ] 启用服务端加密（SSE）
- [ ] 开启访问日志与告警

### 前端 / 移动端

- [ ] 不要把任何 secret 硬编码到前端代码
- [ ] 用 HTTPS 而非 HTTP 调后端
- [ ] 移动端 release build 启用代码混淆

### 部署

- [ ] 使用专用低权限用户运行服务
- [ ] 防火墙仅暴露 80/443
- [ ] 数据库 / Redis 不暴露公网
- [ ] 定期备份（脚本见 `backups/`）
- [ ] 关注 GitHub Security Advisories（Watch → Custom → Security alerts）

## 🔍 Known Security Considerations

| 项 | 说明 | 缓解 |
| --- | --- | --- |
| JWT 默认签名密钥 | `.env.example` 给的是占位 | 生产必须改 |
| CORS 默认配置 | 开发环境放开 | 生产环境收紧 |
| 传输层加解密 | 默认未启用 | 见 `docs/transport_crypto_config.md` |
| TOS 预签名 URL | 默认 1 小时过期 | 缩短到 5-15 分钟 |
| SQL 注入 | SQLAlchemy ORM 防护 | 不要直接拼 SQL |
| XSS | Vue3 默认转义 | 避免 `v-html` |

## 📜 Disclosure Timeline（样例）

| 时间 | 事件 |
| --- | --- |
| D0 | 报告者提交 |
| D0+1d | 维护者确认，评估等级 |
| D0+3d | 与报告者协商披露日期 |
| D0+7d | Critical 漏洞修复 PR |
| D0+14d | 测试 + Review + 合并 |
| D0+21d | 发布修复版本 + Security Advisory |
| D0+30d | 公开披露 |

## 🙏 Thanks

我们感谢每一位负责任地披露漏洞的研究者。安全是社区共建的事。