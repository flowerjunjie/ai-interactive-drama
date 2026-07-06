# 🗺 Roadmap

> 本文档是**对外**路线图（季度粒度）+ **对内**近期迭代池（双周粒度）。
> 详细每日进展见 [.worklog/WORKLOG.md](./.worklog/WORKLOG.md)。

## 状态总览

| 阶段 | 状态 | 备注 |
| --- | --- | --- |
| MVP（短剧业务闭环） | ✅ 已完成 | 表结构 + 后台 CRUD + Feed + 上传 |
| 互动节点编排 | ✅ 已完成 | 埋点 + 分支选择 |
| 移动端 H5 / 小程序 | ✅ 已完成 | uni-app + Tailwind |
| TOS 分片上传 | ✅ 已完成 | 预签名 + 断点续传 |
| AI 节点推荐 | 🟡 进行中 | Round 2200+ 迭代中 |
| 软著申请 | ⬜ 待启动 | — |
| 应用商店上架 | ⬜ 待启动 | — |

---

## 🎯 2026 下半年方向

### Q3 · 平台化（7-9 月）

- [ ] **多租户**：saas 模式，租户隔离数据 + 独立域名
- [ ] **后台 RBAC 升级**：数据权限（按部门/区域/创作者）
- [ ] **互动节点可视化编排**：拖拽式剧本编辑器
- [ ] **运营后台 v2**：ABTest、灰度发布、配置中心

### Q4 · 商业化（10-12 月）

- [ ] **支付与订单**：支付宝 / 微信支付接入
- [ ] **会员体系**：VIP 等级、积分、观看券
- [ ] **广告平台对接**：穿山甲 / 优量汇 / GroMore
- [ ] **数据看板**：用户漏斗、节点转化、留存曲线

### Q1 · 智能与生态（次年）

- [ ] **AI 剧本生成**：从一句话提示生成短剧大纲 + 分支
- [ ] **AI 数字人演员**：口型对齐、TTS、表情
- [ ] **插件市场**：第三方创作者可发布自定义节点类型
- [ ] **开放 API + Webhook**：与第三方 CDP / CRM 对接

---

## 📦 当前迭代池（next 2-4 周）

### 高优 P0

- [ ] README 演示资产（截图 / GIF）
- [ ] GitHub Topics + Description + Social Preview
- [ ] Discussions 启用 + 分类
- [ ] 首条 Release v1.0.0 tag

### 中优 P1

- [ ] 软著申请材料准备
- [ ] 应用商店上架材料（应用宝 / 华为 / 小米）
- [ ] Show HN / 掘金首篇长文
- [ ] Docker Compose 持久化样例

### 低优 P2

- [ ] CI：GitHub Actions 跑 lint / build
- [ ] 国际化（i18n）：英文 README + 错误码
- [ ] 加入 awesome-ruoyi / awesome-fastapi
- [ ] 微信交流群 / Discord

---

## 🌱 已规划但未定档

- 大模型对话能力（剧本创作助手）
- 短剧评分 / 评论运营工具
- 视频 CDN 智能调度
- 短剧创作者平台（U 端）

---

## 📜 变更原则

1. **业务驱动**：所有功能对齐「短剧投放与运营」主链路
2. **小步快跑**：可独立交付的能力独立 PR，避免巨型 feature branch
3. **兼容优先**：MySQL 5.7 / PG 12 / Node 18+ / Python 3.10+ 不升
4. **可观测**：每个核心链路有日志、有埋点、有 CLI 验证命令

---

## 💬 反馈

- 想投票某个功能？→ 在 [Feature Request Issue](https://github.com/flowerjunjie/ai-interactive-drama/issues/new?template=feature.md) 里 👍
- 想贡献方向？→ [Discussion · Ideas](https://github.com/flowerjunjie/ai-interactive-drama/discussions/categories/ideas)
- 想知道每月进展？→ Watch 仓库 Releases only