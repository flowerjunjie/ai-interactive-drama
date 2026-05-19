import { API_BASE, appApi } from '@/config'

/** 与 Pinia 无关，适合任意脚本中附带 C 端 JWT */
export function authHeaders(extra: Record<string, string> = {}): Record<string, string> {
  const t = uni.getStorageSync('drama_token') as string | undefined
  const h: Record<string, string> = { ...extra }
  if (!h['Content-Type']) h['Content-Type'] = 'application/json'
  if (t) h.Authorization = 'Bearer ' + t
  return h
}

export function needLogin(): boolean {
  const t = uni.getStorageSync('drama_token')
  if (t) return true
  uni.showToast({ title: '请先登录', icon: 'none' })
  return false
}

/** 审核反馈等走 `/api` 前缀的接口 */
export function legacyApi(path: string): string {
  const p = path.startsWith('/') ? path : `/${path}`
  return `${API_BASE}/api${p}`
}

export { API_BASE, appApi }
