# ❓ FAQ · 社区问答

> 这里收录社区里**反复出现**的问题。提新问题前先翻这里。
>
> 没找到答案？去 [Discussions Q&A](https://github.com/flowerjunjie/ai-interactive-drama/discussions/categories/q-a) 提问。
>
> 发现文档错误？[开 Issue 标签 `documentation`](https://github.com/flowerjunjie/ai-interactive-drama/issues/new?template=documentation.md)（如未启用文档模板，用普通 Bug 模板）。

## 📦 安装与启动

### Q: `ruoyi: command not found`

**A**: CLI 必须在 `ruoyi-fastapi-backend/` 目录下执行。如果系统找不到命令：

```bash
cd ruoyi-fastapi-backend
pip install -e .            # 开发模式安装
# 或确保 requirements.txt 里包含 ruoyi 相关入口
```

### Q: 启动报 `pymysql.err.OperationalError: (2003, "Can't connect to MySQL server")`

**A**: 三件事挨个查：

1. MySQL 是否启动：`sudo systemctl status mysql` 或 `brew services list | grep mysql`
2. `.env.dev` 中 `MYSQL_HOST` / `MYSQL_PORT` / `MYSQL_USER` / `MYSQL_PASSWORD` 是否正确
3. MySQL 是否允许你的用户远程连接（开发环境通常是 `localhost`，生产不要 `root`）

### Q: 启动报 `redis.exceptions.ConnectionError`

**A**: 启动 Redis：

```bash
# macOS
brew services start redis

# Ubuntu/Debian
sudo systemctl start redis-server

# 验证
redis-cli ping    # 应返回 PONG
```

### Q: `npm install` 卡住 / 超时

**A**: 切到国内镜像：

```bash
npm install --registry=https://registry.npmmirror.com
# 或永久设置
npm config set registry https://registry.npmmirror.com
```

### Q: `pnpm dev:h5` 启动后浏览器空白 / 报错

**A**: 检查：

1. 后端是否在 `:19199` 运行（移动端 H5 需要后端 API）
2. `mobile-app/.env.development` 中 `VITE_APP_API_PREFIX` 是否正确
3. 浏览器 DevTools Network 面板看请求是否 CORS 报错 → 后端 `.env.dev` 配置 CORS 白名单

## 🐛 运行时问题

### Q: 接口 401 Unauthorized

**A**: 三种可能：

1. JWT token 过期（默认 30 分钟） → 重新登录
2. `JWT_SECRETKEY` 变更 → 旧 token 全部失效，全员重新登录
3. 前端请求没带 token → 检查 axios interceptor / 移动端 request.js 封装

### Q: TOS / S3 上传失败，提示签名错误

**A**:

1. 检查 `.env.dev` 中 `TOS_*` 与对象存储控制台密钥是否一致
2. 检查 `TOS_ENDPOINT` 是否带协议（如 `https://`）
3. 检查 `TOS_BUCKET` 是否存在、IAM 子账号是否有 `PutObject` 权限
4. 时钟偏差：服务器时间与对象存储时间偏差 > 5 分钟会签名失败，`sudo ntpdate ntp.aliyun.com`

### Q: Alembic 迁移与 ORM 模型不一致

**A**:

```bash
# 检测漂移
ruoyi db upgrade --env=dev --sql     # 打印当前 head 的 SQL

# 如有未生成迁移
ruoyi db revision --env=dev --message="add xxx field" --autogenerate
# 务必 review 生成的迁移文件再 apply
```

### Q: 短剧互动节点不显示分支选项

**A**: 检查：

1. `drama_node.choices` 字段是否为 JSON 数组：`[{"label": "...", "next_node_id": N}]`
2. 前端是否正确解析 `choices`（Element Plus 树形组件的 `children`）
3. 节点 `is_branch` 字段值（前端用它过滤渲染逻辑）

## 🚀 部署相关

### Q: 生产环境应该改哪些配置？

**A**: 必改清单（缺一不可）：

- [ ] `JWT_SECRETKEY` → 强随机 32+ 字节
- [ ] `MYSQL_PASSWORD` / `REDIS_PASSWORD` → 强密码
- [ ] `admin / admin123` → 首次登录后立即改
- [ ] `DEBUG=false`（FastAPI 文档页关闭外网访问）
- [ ] `CORS_ALLOW_ORIGINS` → 精确白名单
- [ ] `TOS_*` → 专用子账号 + 最小权限
- [ ] Nginx 启用 HTTPS（Let's Encrypt）
- [ ] 数据库 / Redis 不暴露公网

详见 [SECURITY.md](../SECURITY.md) 与 [README 生产部署](../README.md#-发布与部署)。

### Q: Docker Compose 启动后数据丢了

**A**: 默认 compose 没做 volume 持久化。生产前必须加：

```yaml
services:
  mysql:
    volumes:
      - mysql_data:/var/lib/mysql
volumes:
  mysql_data:
```

## 🤝 贡献相关

### Q: 我第一次提 PR，需要做什么？

**A**:

1. Fork 仓库，从 `main` 拉新分支
2. 提交前跑 `pre-commit run --all-files`（如已 `pip install pre-commit && pre-commit install`）
3. PR 标题遵循 Conventional Commits（如 `feat: 短剧收藏埋点`）
4. CI 会自动跑 lint + build，等绿灯即可
5. 详细见 [CONTRIBUTING.md](../CONTRIBUTING.md)

### Q: 我发现一个 Bug 但不知道怎么修

**A**: 直接 [开 Issue](https://github.com/flowerjunjie/ai-interactive-drama/issues/new?template=bug.md)，把环境、复现步骤、期望 / 实际、截图 / 日志贴全。**会修的人会认领**，认领不了我们也会讨论方案。

### Q: 我想加新功能，但不确定是否被接受

**A**: 先 [开 Feature Request Issue](https://github.com/flowerjunjie/ai-interactive-drama/issues/new?template=feature.md) 描述需求。讨论通过后再写代码，避免做无用功。

## 📜 许可与商用

### Q: 我能用这个项目做商业产品吗？

**A**: 可以。本项目使用 [MIT License](../LICENSE)，你可以：

- ✅ 商用
- ✅ 修改
- ✅ 分发
- ✅ 私有 fork

唯一要求：在分发时保留版权声明。

### Q: 我能拿这个项目去申请软著吗？

**A**: 我们已经在申请中（见 [ROADMAP.md](../ROADMAP.md)）。如果你也想申请：

- ✅ 基于 MIT 项目二次开发的产物，**可以**申请软著
- ⚠️ 但**不能**声称是 RuoYi 原作者（保留上游致谢）

### Q: 我 fork 后能改名字发布吗？

**A**: 可以，但请：

- 保留上游版权与致谢（MIT 要求）
- 不要用原项目的 star 数冒充自己（违反 GitHub TOS）

## 🆘 找不到答案？

1. 搜 [Issues](https://github.com/flowerjunjie/ai-interactive-drama/issues) 是否有同类问题
2. 去 [Discussions Q&A](https://github.com/flowerjunjie/ai-interactive-drama/discussions/categories/q-a) 提问
3. 实在卡住，发邮件给 maintainer（见 GitHub About 页面）

---

> 📝 **维护 FAQ**：FAQ 是社区共建的。你遇到的问题 + 解决方案，欢迎 PR 追加到这里。