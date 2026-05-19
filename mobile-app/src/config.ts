/** 后端直连地址，H5 开发时与 FastAPI 同机可填局域网 IP */
export const API_BASE = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:19199'
/** C 端业务接口前缀，默认 /api/app；登录仍为 /api/auth */
export const APP_API_PREFIX = import.meta.env.VITE_APP_API_PREFIX || '/api/app'

export function appApi(path: string): string {
  const p = path.startsWith('/') ? path : `/${path}`
  return `${API_BASE}${APP_API_PREFIX}${p}`
}
