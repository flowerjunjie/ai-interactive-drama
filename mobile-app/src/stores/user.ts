import { defineStore } from 'pinia'
import { ref } from 'vue'
import { API_BASE } from '@/config'

export const useUserStore = defineStore('drama-user', () => {
  const token = ref(uni.getStorageSync('drama_token') || '')
  const profile = ref<{
    user_id?: number
    user_name?: string
    nick_name?: string
    avatar?: string | null
  } | null>(null)

  function setToken(t: string) {
    token.value = t
    uni.setStorageSync('drama_token', t)
  }

  async function login(userName: string, password: string) {
    const res = await new Promise<{ code: number; token?: string; msg?: string }>((resolve, reject) => {
      uni.request({
        url: `${API_BASE}/api/auth/login`,
        method: 'POST',
        header: { 'Content-Type': 'application/json' },
        data: { user_name: userName, password },
        success: (r: any) => resolve(r.data as any),
        fail: reject,
      })
    })
    if (res.code === 200 && res.token) {
      setToken(res.token)
      await fetchMe()
      return true
    }
    uni.showToast({ title: res.msg || '登录失败', icon: 'none' })
    return false
  }

  async function register(userName: string, password: string, nickName?: string) {
    const res = await new Promise<{ code: number; msg?: string }>((resolve, reject) => {
      uni.request({
        url: `${API_BASE}/api/auth/register`,
        method: 'POST',
        header: { 'Content-Type': 'application/json' },
        data: {
          user_name: userName,
          password,
          nick_name: nickName?.trim() || userName,
        },
        success: (r: any) => resolve(r.data as any),
        fail: reject,
      })
    })
    if (res.code === 200) {
      return login(userName, password)
    }
    uni.showToast({ title: res.msg || '注册失败', icon: 'none' })
    return false
  }

  async function fetchMe() {
    if (!token.value) return
    const res = await new Promise<any>((resolve, reject) => {
      uni.request({
        url: `${API_BASE}/api/auth/me`,
        header: { Authorization: 'Bearer ' + token.value },
        success: (r: any) => resolve(r.data),
        fail: reject,
      })
    })
    if (res.code === 200 && res.data) {
      profile.value = res.data
    }
  }

  function logout() {
    token.value = ''
    profile.value = null
    uni.removeStorageSync('drama_token')
  }

  return { token, profile, setToken, login, register, fetchMe, logout }
})
