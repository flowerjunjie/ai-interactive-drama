# Social Preview 制作指引

> GitHub Social Preview 尺寸：**1280×640** PNG/JPG，< 1 MB。

## 推荐设计

### 配色

- 主色：`#2563EB`（蓝）
- 辅色：`#10B981`（绿）/ `#F59E0B`（橙）
- 文字色：`#FFFFFF`
- 背景：渐变 `#0F172A` → `#1E293B`（深空蓝）

### 布局

```
┌──────────────────────────────────────────┐
│                                          │
│   AI Interactive Drama                   │
│   AI 互动短剧平台 · 开源                   │
│                                          │
│   [FastAPI] [Vue3] [uni-app]             │
│                                          │
└──────────────────────────────────────────┘
```

### 字体

- 标题：思源黑体 / Inter / SF Pro（48-72 px）
- 副标题：同上 Regular（24 px）

## 上传路径

GitHub → Settings → Social preview → Upload an image

## 临时占位（如无设计稿）

```bash
# 用 ImageMagick 生成一张占位图
convert -size 1280x640 \
  -define gradient:angle=135 \
  gradient:'#0F172A-#1E293B' \
  -font 'Inter-Bold' -pointsize 72 -fill white \
  -gravity center -annotate +0-50 'AI Interactive Drama' \
  -font 'Inter-Regular' -pointsize 28 -fill '#94A3B8' \
  -annotate +0+40 'AI 互动短剧平台 · 开源 · FastAPI + Vue3 + uni-app' \
  assets/social-preview.png
```

## 参考模板

- https://github.com/sponsors/open-source-badges
- https://www.canva.com/ 搜 "GitHub social banner"