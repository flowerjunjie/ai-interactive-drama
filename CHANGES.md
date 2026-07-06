# 📝 CHANGES · 本项目独立变更追踪

> 本文件追踪 **flowerjunjie/ai-interactive-drama 自身的变更**。
> 上游 [RuoYi-Vue3-FastAPI](https://gitee.com/insistence2022/RuoYi-Vue3-FastAPI) 的变更记录见 [CHANGELOG.md](./CHANGELOG.md)。

格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，
版本号遵循 [Semantic Versioning](https://semver.org/lang/zh-CN/)。

---

## [Unreleased]

### Added · 新增

- 🏛️ 开源治理：CONTRIBUTING / CODE_OF_CONDUCT / SECURITY / ROADMAP
- 📋 GitHub Issue + PR 模板（含 contact links）
- 🤖 CI：lint + build + CodeQL + Dependabot + Release 自动发布
- 📦 Release notes：docs/releases/v1.0.0.md
- 📣 推广稿件草稿：docs/articles/{launch-juejin, launch-showhn, launch-v2ex}.md
- 🛠️ GitHub 网页端 6 步配置 SOP：docs/github-setup-todo.md
- 🎨 跨 IDE 规范：.editorconfig
- 🔒 Pre-commit 钩子：.pre-commit-config.yaml
- 📜 学术引用：CITATION.cff
- 🏗️ 架构决策记录：docs/adr/
- ⚠️ 风险登记册：docs/risks.md
- 🐳 Docker 优化：.dockerignore
- 🚀 一键启动：scripts/setup-dev.sh
- 📸 演示资产占位：assets/screenshots/, assets/demo/
- 🧠 SSH key 备忘录：项目 memory `github-ssh-id_rsa-pin.md`

### Changed · 变更

- 🔀 远程仓库切换：gitee (min1314) → github (flowerjunjie)
- 🔐 SSH 通道固话：仓库级 `core.sshCommand` 指定 `id_rsa`
- 📚 README 重写：14 节丰满版（架构图 / 技术栈 / Troubleshooting / 验收清单 / 路线图）
- 📋 仓库描述：英文 + 中文双语

### Fixed · 修复

- 🐛 LICENSE 徽章：占位符 `mashape/apistatus` → 真实仓库路径
- 🐛 README 项目简介：明确区分上游 RuoYi 归属 vs 本项目绑定
- 📝 移动端 pnpm 镜像源说明补齐

### Security · 安全

- 🛡️ 启用 CodeQL 安全扫描（每周一 + PR）
- 🔒 SECURITY.md 漏洞披露流程落地
- ⚠️ 默认 admin 密码警示入 README

---

## [1.0.0] · 2026-07-06 · 首个公开版本

🎉 **First Public Release** — 完整短剧平台 MVP：后端 + 管理后台 + 移动端 + 互动节点 + TOS 上传。

详见 [docs/releases/v1.0.0.md](./docs/releases/v1.0.0.md)。

---

## 关联

- [CHANGELOG.md](./CHANGELOG.md) — 上游 RuoYi-Vue3-FastAPI 的变更记录
- [ROADMAP.md](./ROADMAP.md) — 未来规划
- [docs/releases/](./docs/releases/) — 各版本 release notes 索引