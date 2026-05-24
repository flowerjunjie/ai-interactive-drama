<template>
  <view class="relative min-h-screen w-screen overflow-x-hidden bg-[#0a0a14]">
    <!-- Background Image / Glow -->
    <view class="absolute inset-0 z-0">
      <image src="https://images.unsplash.com/photo-1618331835717-801e976710b2?q=80&w=400&auto=format&fit=crop" class="h-[50vh] w-full object-cover opacity-10" mode="aspectFill" />
      <view class="absolute inset-0 bg-gradient-to-b from-[#0a0a14]/70 via-[#0a0a14] to-[#0a0a14]"></view>
    </view>

    <!-- Top Nav -->
    <view class="relative z-10 flex h-11 items-center justify-between px-4 pt-[calc(env(safe-area-inset-top)+10px)]">
      <view class="flex h-8 w-8 items-center active:opacity-70" @click="goBack">
        <view class="i-mdi-chevron-left text-[32px] text-white" />
      </view>
      <text v-if="isLogin" class="text-[13px] text-white/70 active:opacity-70">验证码登录</text>
    </view>

    <view class="relative z-10 px-6 pt-4 pb-10">
      <!-- Login Header -->
      <view v-if="isLogin" class="mb-10 flex flex-col items-center">
        <view class="flex h-[76px] w-[76px] items-center justify-center rounded-[22px] bg-gradient-to-br from-[#d8b4fe] via-[#a855f7] to-[#7c3aed] shadow-[0_0_24px_rgba(168,85,247,0.35)]">
          <view class="i-mdi-play ml-1.5 text-[44px] text-white" />
        </view>
        <text class="mt-5 text-[24px] font-bold tracking-widest text-white">欢迎登录</text>
        <text class="mt-2.5 text-[12px] text-white/50 tracking-widest">沉浸互动，选择你的剧情人生</text>
      </view>

      <!-- Register Header -->
      <view v-else class="mb-8 mt-2 flex flex-col items-center">
        <text class="text-[24px] font-bold tracking-widest text-white">注册账号</text>
        <text class="mt-3.5 text-[11px] tracking-wider text-white/50">注册即表示同意《<text class="text-[#9a5cf6]" @tap="goAgreement">用户协议</text>》和《<text class="text-[#9a5cf6]" @tap="goPrivacy">隐私政策</text>》</text>
      </view>

      <!-- Form Box -->
      <view class="rounded-[20px] bg-white/[0.04] p-5 shadow-lg border border-white/5">
        <!-- Username -->
        <view class="flex items-center border-b border-white/5 py-4">
          <view class="i-mdi-account-outline mr-3.5 text-[22px] text-white/60" />
          <input v-model="userName" class="flex-1 text-[14px] text-white placeholder:text-white/30" placeholder="请输入用户名" />
        </view>

        <!-- Password -->
        <view class="flex items-center border-b border-white/5 py-4">
          <view class="i-mdi-lock-outline mr-3.5 text-[22px] text-white/60" />
          <input v-model="password" password class="flex-1 text-[14px] text-white placeholder:text-white/30" placeholder="请输入密码" />
          <view class="i-mdi-eye-outline ml-2 text-[20px] text-white/30" />
        </view>

        <!-- Confirm Password (Register Only) -->
        <view v-if="!isLogin" class="flex items-center border-b border-white/5 py-4">
          <view class="i-mdi-lock-outline mr-3.5 text-[22px] text-white/60" />
          <input v-model="password2" password class="flex-1 text-[14px] text-white placeholder:text-white/30" placeholder="请再次输入密码" />
          <view class="i-mdi-eye-outline ml-2 text-[20px] text-white/30" />
        </view>

        <!-- Phone (Register Only) -->
        <view v-if="!isLogin" class="flex items-center border-b border-white/5 py-4">
          <view class="i-mdi-cellphone mr-3.5 text-[22px] text-white/60" />
          <input v-model="phoneDecoy" type="number" class="flex-1 text-[14px] text-white placeholder:text-white/30" placeholder="请输入手机号" />
        </view>

        <!-- Verification Code (Register Only) -->
        <view v-if="!isLogin" class="flex items-center border-b border-white/5 py-4">
          <view class="i-mdi-shield-check-outline mr-3.5 text-[22px] text-white/60" />
          <input v-model="codeDecoy" class="flex-1 text-[14px] text-white placeholder:text-white/30" placeholder="请输入验证码" />
          <text class="ml-2 text-[13px] text-[#a855f7] active:opacity-70">获取验证码</text>
        </view>

        <!-- Nickname (Register, optional backend) -->
        <view v-if="!isLogin" class="flex items-center border-b border-white/5 py-4">
          <view class="i-mdi-card-account-details-outline mr-3.5 text-[22px] text-white/60" />
          <input v-model="nickName" class="flex-1 text-[14px] text-white placeholder:text-white/30" placeholder="昵称（可选）" />
        </view>

        <!-- Options Row -->
        <view v-if="isLogin" class="mt-6 flex items-center justify-between">
          <view class="flex items-center gap-2.5 active:opacity-70" @click="toggleRemember">
            <view :class="rememberPwd ? 'i-mdi-checkbox-marked text-[#a855f7]' : 'i-mdi-checkbox-blank-outline text-white/30'" class="text-[18px]" />
            <text class="text-[12px] text-white/60 tracking-wider">记住密码</text>
          </view>
          <text class="text-[12px] text-white/60 tracking-wider active:opacity-70">忘记密码？</text>
        </view>
        <view v-else class="mt-6 flex items-center gap-2.5 active:opacity-70">
          <view class="flex h-[18px] w-[18px] shrink-0 items-center justify-center rounded-full border border-white/20"></view>
          <text class="text-[11px] text-white/60 tracking-wider">我已阅读并同意《<text class="text-[#9a5cf6]" @tap="goAgreement">用户协议</text>》和《<text class="text-[#9a5cf6]" @tap="goPrivacy">隐私政策</text>》</text>
        </view>

        <!-- Submit Button -->
        <view
          class="mt-8 flex w-full items-center justify-center rounded-[12px] py-[14px] active:opacity-90 shadow-[0_4px_14px_rgba(168,85,247,0.3)]"
          style="background: linear-gradient(90deg, #9a5cf6, #d946ef)"
          @click="onSubmit"
        >
          <text class="text-[15px] font-bold tracking-widest text-white">{{ submitting ? '提交中…' : isLogin ? '登录' : '注册' }}</text>
        </view>
      </view>

      <!-- Other Login Methods -->
      <view class="mt-12 flex flex-col items-center">
        <view class="flex w-full items-center justify-center gap-4 px-12">
          <view class="h-[1px] flex-1 bg-white/5"></view>
          <text class="text-[11px] text-white/30 tracking-widest">其他登录方式</text>
          <view class="h-[1px] flex-1 bg-white/5"></view>
        </view>

        <view class="mt-6 flex flex-col items-center gap-3 active:opacity-70">
          <view class="flex h-[44px] w-[44px] items-center justify-center rounded-[14px] border border-white/10 bg-white/[0.02]">
            <view class="i-mdi-cellphone text-[20px] text-white/60" />
          </view>
          <text class="text-[10px] text-white/50 tracking-wider">手机验证码登录</text>
        </view>

        <!-- Switch State -->
        <view class="mt-10 flex items-center gap-1">
          <text class="text-[12px] text-white/50 tracking-widest">{{ isLogin ? '还没有账号？' : '已有账号？' }}</text>
          <text class="text-[12px] font-bold text-[#a855f7] tracking-widest active:opacity-70" @click="toggleMode">{{ isLogin ? '立即注册' : '立即登录' }}</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useUserStore } from '@/stores/user'

const isLogin = ref(true)
const userName = ref('')
const password = ref('')
const password2 = ref('')
const nickName = ref('')
const phoneDecoy = ref('')
const codeDecoy = ref('')
const submitting = ref(false)
const rememberPwd = ref(false)
const userStore = useUserStore()

// 记住密码：仅回填用户名（密码明文存储有XSS风险，不再保存）
const savedUser = uni.getStorageSync('saved_user_name')
if (savedUser) userName.value = savedUser

function goBack() {
  uni.navigateBack()
}

function goPrivacy() {
  uni.navigateTo({ url: '/pages/privacy/index' })
}

function goAgreement() {
  uni.navigateTo({ url: '/pages/privacy/agreement' })
}

function toggleMode() {
  isLogin.value = !isLogin.value
}

function toggleRemember() {
  rememberPwd.value = !rememberPwd.value
}

async function onSubmit() {
  const u = userName.value.trim()
  const p = password.value
  if (!u || !p) {
    uni.showToast({ title: '请输入用户名和密码', icon: 'none' })
    return
  }
  if (p.length < 6) {
    uni.showToast({ title: '密码至少 6 位', icon: 'none' })
    return
  }
  if (!isLogin.value && p !== password2.value) {
    uni.showToast({ title: '两次密码不一致', icon: 'none' })
    return
  }
  if (submitting.value) return
  submitting.value = true
  try {
    const ok = isLogin.value
      ? await userStore.login(u, p)
      : await userStore.register(u, p, nickName.value.trim() || undefined)
    if (ok) {
      // 记住密码：仅保存用户名（密码不能存明文，XSS落地后可被窃取）
      if (rememberPwd.value) {
        uni.setStorageSync('saved_user_name', userName.value.trim())
        uni.removeStorageSync('saved_password')
      } else {
        uni.removeStorageSync('saved_user_name')
        uni.removeStorageSync('saved_password')
      }
      uni.showToast({ title: isLogin.value ? '登录成功' : '注册并登录成功', icon: 'success' })
      setTimeout(() => {
        uni.reLaunch({ url: '/pages/mine/index' })
      }, 400)
    }
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
/* Scoped styles */
</style>
