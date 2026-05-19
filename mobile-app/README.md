# 互动短剧 · uni-app（H5 优先）

本目录由 `ruoyi-fastapi-app` 的同版本 `@dcloudio/uni-app` / `vite-plugin-uni` 模板复制而来（`package.json`、`vite.config.ts`、`tailwind` 等）。

## 开发

```bash
cd mobile-app
pnpm install
pnpm dev:h5
```

- 接口基址：`.env.development` 中 `VITE_API_BASE`（默认 `http://127.0.0.1:19199`，需与 FastAPI `APP_PORT` 一致；真机调试改为局域网 IP）。
- 若遇传输层加密拦截，请在后端为 `/api` 路径增加 `TRANSPORT_CRYPTO_EXCLUDE_PATHS` 排除，或关闭相关 required 模式。

## 页面与组件

- `src/pages/index`：竖屏信息流 + `VideoFeed`
- `theater` / `drama-detail` / `player` / `mine` / `login`
- `src/components`：`VideoFeed`、`DramaCard`、`ChoicePopup`、`AdCard`
- `src/stores/user.ts`：Pinia + `/api/auth/login`、`/api/auth/me`
