# 📸 Screenshots

> 本目录用于存放项目演示截图，供 README / 推广文案 / 文档引用。

## 待补截图清单

| # | 名称 | 路径 | 状态 |
| --- | --- | --- | --- |
| 1 | 管理后台登录页 | `admin-login.png` | ⬜ 待补 |
| 2 | 管理后台首页（仪表盘） | `admin-dashboard.png` | ⬜ 待补 |
| 3 | 短剧列表（CRUD） | `admin-drama-list.png` | ⬜ 待补 |
| 4 | 短剧编辑 / 节点编排 | `admin-drama-edit.png` | ⬜ 待补 |
| 5 | 视频节点管理 | `admin-drama-nodes.png` | ⬜ 待补 |
| 6 | TOS 上传面板 | `admin-upload.png` | ⬜ 待补 |
| 7 | 用户管理 | `admin-users.png` | ⬜ 待补 |
| 8 | 移动端 H5 Feed | `mobile-feed.png` | ⬜ 待补 |
| 9 | 移动端 H5 短剧详情 + 互动节点 | `mobile-drama-detail.png` | ⬜ 待补 |
| 10 | 移动端 H5 个人中心 | `mobile-profile.png` | ⬜ 待补 |

## 截图规范

- **尺寸**：建议 1440×900（管理后台），375×812（移动端 H5 模拟）
- **格式**：PNG，无压缩损耗
- **水印**：无（如要带版本号，放右下角小字）
- **真实数据**：建议先用测试库脱敏数据，避免泄漏
- **命名**：kebab-case，描述清楚页面意图

## 引用方式

```markdown
![管理后台-短剧列表](./assets/screenshots/admin-drama-list.png)
```

## 自动化建议

未来可接入 Playwright 自动截图脚本（CI 跑）：

```ts
await page.goto('http://localhost:5188/drama/list');
await page.screenshot({ path: 'assets/screenshots/admin-drama-list.png', fullPage: true });
```

参考脚本位置建议：`scripts/screenshots/`（待建）。