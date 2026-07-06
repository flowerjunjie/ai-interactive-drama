# 🔧 GitHub 网页端一次性配置清单

> 仓库内的文件我已全部代为落地。剩下 6 项需要你在 GitHub 网页点 2 分钟。
> 每项都给了**具体路径 + 鼠标动作 + 校验方式**，照着点就行。

---

## ☐ 1. 仓库 Topics（5 个核心关键词）

**作用**：让仓库在 GitHub Search 和 Topics 浏览里被发现。

**路径**：仓库首页 → 右侧 About 栏 → ⚙️ 齿轮 → Topics

**填入**（每行一个）：

```
fastapi
vue3
uni-app
short-drama
ai-interactive
ruoyi
mysql
python
```

**校验**：Topics 显示在 About 栏的徽章里。

---

## ☐ 2. 仓库 Description（一句话定位）

**路径**：同上 → Description 输入框

**填入**（英文优先，中文可选）：

```
Open-source AI interactive short-drama platform: FastAPI backend + Vue3 admin + uni-app mobile. Built on RuoYi-Vue3-FastAPI.
```

**校验**：About 栏卡片下方显示。

---

## ☐ 3. Website URL

**路径**：同上 → Website 输入框

**填入**（暂留空，等有官网/演示站时填）

---

## ☐ 4. Social Preview（1280×640 banner）

**作用**：转发到 X / 微信 / 任何地方都显示一张正经卡片。

**路径**：
1. Settings → General → Social preview → **Upload an image**
2. 设计稿指引：见 [`.github/SOCIAL_PREVIEW_GUIDE.md`](../.github/SOCIAL_PREVIEW_GUIDE.md)
3. 没设计稿快速占位：执行下方命令（需 ImageMagick）

```bash
# 在仓库根目录
convert -size 1280x640 \
  -define gradient:angle=135 \
  gradient:'#0F172A-#1E293B' \
  -font 'Inter-Bold' -pointsize 72 -fill white \
  -gravity center -annotate +0-50 'AI Interactive Drama' \
  -font 'Inter-Regular' -pointsize 28 -fill '#94A3B8' \
  -annotate +0+40 'AI 互动短剧平台 · 开源 · FastAPI + Vue3 + uni-app' \
  assets/social-preview.png
```

**校验**：分享仓库链接到任何 IM，展开卡片显示自定义图。

---

## ☐ 5. 启用 Discussions

**作用**：让用户开 Q&A / Ideas / Show and tell 板块，避免 Issue 被灌水。

**路径**：Settings → General → Features → ✅ Discussions

**点击启用后还要设置分类**：

```
Q&A          (提问求助)
Ideas        (功能建议)
Show and tell (用户案例)
Announcements (项目公告，仅 maintainer 可发)
```

**校验**：仓库顶部出现 `Discussions` 标签。

---

## ☐ 6. 打首个 Release Tag v1.0.0

**作用**：让用户能 clone 稳定快照，触发关注者的邮件通知。

**路径**：Releases → **Create a new release**

- **Tag**：`v1.0.0`
- **Target**：`main`
- **Title**：`v1.0.0 · First public release`
- **Description**（粘贴下面）：

```markdown
## 🎉 首个公开版本

完整短剧平台 MVP：后端 + 管理后台 + 移动端 + 互动节点 + TOS 上传。

### ✨ 特性

- FastAPI + SQLAlchemy 2.0 (async) + MySQL/PostgreSQL + Redis
- Vue3 + Element Plus + Vite 管理后台
- uni-app + Tailwind CSS 移动端（H5 / 微信小程序）
- 短剧 CRUD、互动节点编排、Feed 流、点赞收藏
- TOS / S3 兼容 预签名分片上传
- OAuth2 + JWT 鉴权
- Alembic 迁移、ruoyi CLI、Docker Compose

### 📦 安装

参见 [README](https://github.com/flowerjunjie/ai-interactive-drama#-快速开始)

### 🙏 致谢

基于 [RuoYi-Vue3-FastAPI](https://gitee.com/insistence2022/RuoYi-Vue3-FastAPI) 二次开发。
```

**校验**：Releases 页面出现 v1.0.0 条目。

---

## ✅ 全部完成后

仓库将从「骨架」升级成「门面」：

- ✅ Topics 让陌生人搜得到
- ✅ Description 一眼看清是啥
- ✅ Social Preview 让转发不掉价
- ✅ Discussions 让提问有去处
- ✅ v1.0.0 让关注者收到通知

下一步可以执行 `docs/articles/` 下的草稿到对应平台（掘金 / Show HN / V2EX）。

---

## 📞 卡在哪一步？

直接在仓库 Issue 里 @ 维护者，或开 Discussion。