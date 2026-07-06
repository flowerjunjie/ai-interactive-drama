# 🚀 GO-LIVE.md · 上线作战手册

> 上线不是「git push 然后部署」。**这是把赌注放到 1 亿用户面前的最后一道关卡**。
> 本文档是**生产环境上线前必须逐项打勾**的 checklist。
> 任何一项不达标，**禁止**切流量。

---

## 📋 4 阶段 · 24 项必查

### 阶段 1 · 代码冻结（上线前 7 天）

- [ ] 当前 commit 已打 `v1.x.x` tag
- [ ] CI 全绿（lint / build / CodeQL / Dependabot）
- [ ] 已知 P0/P1 bug 已全部修复或显式延期
- [ ] CHANGES.md / docs/releases/v1.x.x.md 更新
- [ ] 无未合入的「紧急 hotfix」分支悬空

### 阶段 2 · 配置审计（上线前 3 天）

#### 2.1 密钥与凭证

- [ ] `.env.prod` 中 `JWT_SECRETKEY` 已替换为**强随机 32+ 字节**
  ```bash
  python -c "import secrets; print(secrets.token_urlsafe(32))"
  ```
- [ ] `MYSQL_PASSWORD` / `REDIS_PASSWORD` 均为强密码（≥ 16 字符）
- [ ] `TOS_*` 凭证使用**专用子账号** + 最小权限（仅当前 bucket）
- [ ] 没有任何密钥进入 git 历史（`git log -p | grep -E 'secret|password'`）
- [ ] 生产服务器 `.env.prod` 文件权限 `chmod 600`

#### 2.2 应用开关

- [ ] `DEBUG=false`
- [ ] `CORS_ALLOW_ORIGINS` 设置为精确白名单（**不要** `*`）
- [ ] FastAPI docs（`/docs` / `/redoc`）外网不可访问
- [ ] 后台 `/admin/*` 外网不可访问（或仅内网 VPN）

#### 2.3 数据库

- [ ] 数据库已升级到目标版本
- [ ] Alembic 迁移在生产 dry-run 跑过一次：
  ```bash
  ruoyi db upgrade --env=prod --sql | less
  ```
- [ ] 已确认无 ORM 与迁移漂移（`alembic check`）
- [ ] 数据库账号最小权限（应用账号无 DROP / ALTER 全表权限）

### 阶段 3 · 基础设施（上线前 1 天）

- [ ] **HTTPS 证书**就绪（Let's Encrypt / 阿里云 SSL）
- [ ] Nginx 反向代理配置完成（参考 [README Nginx 示例](./README.md#nginx-反向代理示例)）
- [ ] **强制 HTTPS**（`server { return 301 https://... }`）
- [ ] HSTS 头已加（`Strict-Transport-Security: max-age=31536000`）
- [ ] 防火墙：仅暴露 80 / 443（数据库 / Redis 不暴露公网）
- [ ] 监控告警就绪（CPU / 内存 / 磁盘 / 接口 5xx 率 / 接口延迟 P99）
- [ ] 日志收集就绪（stdout → 集中日志）
- [ ] 备份策略就绪：DB 每日全量 + 增量，保留 30 天
- [ ] 备份恢复演练已做（**不是写了脚本就完事**）

### 阶段 4 · 上线当天（流量切换）

#### 4.1 部署顺序

- [ ] 部署后端 → `ruoyi app doctor --env=prod` 全绿
- [ ] 部署管理后台 → `/login` 可访问
- [ ] 部署移动端 H5 → 首页可访问
- [ ] 对象存储 bucket 配置就绪
- [ ] DNS 解析切到新服务（**先 1% 灰度**）

#### 4.2 灰度验证（5 分钟内必查）

- [ ] 注册 / 登录 流程通
- [ ] 上传短剧（走 TOS 完整链路）通
- [ ] 播放 + 互动节点选择 通
- [ ] 支付（如果上线）通
- [ ] 监控大盘无异常告警
- [ ] 错误日志无新增 5xx

#### 4.3 全量切换

- [ ] DNS 100% 切流
- [ ] 旧版本服务保留 N 小时作回滚兜底
- [ ] 监控持续盯盘 24 小时

### 阶段 5 · 上线后（24-72 小时）

- [ ] 监控告警阈值二次校准（首日数据可能与预估有偏差）
- [ ] 收集用户反馈 → 入 [Discussion](https://github.com/flowerjunjie/ai-interactive-drama/discussions)
- [ ] 性能基线建立（P50 / P95 / P99 延迟）
- [ ] 异常事件复盘（如有）

---

## 🚨 回滚预案

> **没有回滚预案的上线 = 裸奔**。

```bash
# 1. 立即回切 DNS / Nginx upstream
# 2. 拉回上一版本代码 + 依赖
git checkout v1.x.x-1
pip install -r requirements.txt  # 锁版本
ruoyi app run --env=prod

# 3. 数据库回滚（如果迁移破坏数据）
ruoyi db downgrade --env=prod --revision=<previous_head>

# 4. 清理：本次新增的对象存储文件保留 N 天后再删
```

回滚 RTO 目标：**15 分钟内恢复 90% 流量**。

---

## 📞 紧急联系人

| 角色 | 联系方式 | 备注 |
| --- | --- | --- |
| 维护者 | 见 GitHub About | first responder |
| 数据库 DBA | （填） | 迁移失败 / 数据损坏 |
| 运维 | （填） | 服务器 / 网络 / DNS |
| 对象存储 | （填） | TOS / S3 服务 |
| 安全应急 | （填） | 漏洞披露响应 |

---

## ✅ 上线签字

```
___________    ___________
上线批准人    日期
___________    ___________
运维负责人    日期
___________    ___________
安全审核人    日期
```

> 一项不签字 = 不上线。**对结果负责**不是挂在墙上的。