<template>
  <view class="relative h-screen w-screen overflow-hidden bg-[#050505] flex flex-col">
    <!-- Main Scroll Content -->
    <scroll-view scroll-y class="flex-1 pb-[90px]">
      <view class="px-4 pt-[calc(env(safe-area-inset-top)+10px)] pb-10">
        
        <!-- Top Nav Settings Icon -->
        <view class="flex items-center justify-end h-10">
          <view class="i-mdi-cog-outline text-[24px] text-white/80 active:opacity-70" />
        </view>

        <!-- Profile Header -->
        <view class="mt-2 flex items-center gap-4">
          <view class="h-[76px] w-[76px] overflow-hidden rounded-full border border-white/10 bg-white/5">
            <image :src="avatarSrc" class="h-full w-full object-cover" />
          </view>
          <view class="flex flex-col flex-1">
            <view class="flex items-center gap-2">
              <text class="text-[20px] font-bold text-white tracking-wide">{{ displayName }}</text>
              <view class="flex items-center rounded-full bg-gradient-to-r from-[#eec787] to-[#b37b3b] px-[5px] py-[2px]">
                <text class="text-[9px] font-bold text-[#302619]">LV3</text>
              </view>
            </view>
            <view class="mt-1 flex items-center gap-1 opacity-60">
              <text class="text-[12px] text-white">ID: {{ displayId }}</text>
              <view class="i-mdi-content-copy text-[14px] text-white" />
            </view>
            <text class="mt-2 text-[11px] text-white/40">这个人很懒，什么都没有写~</text>
          </view>
        </view>

        <!-- Stats Row -->
        <view class="mt-8 flex items-center justify-around">
          <view class="flex flex-col items-center gap-1">
            <text class="text-[22px] font-bold text-white">{{ dash.watch_history_count }}</text>
            <text class="text-[12px] text-white/60">历史记录</text>
          </view>
          <view class="flex flex-col items-center gap-1">
            <text class="text-[22px] font-bold text-white">{{ dash.favorite_count }}</text>
            <text class="text-[12px] text-white/60">我的收藏</text>
          </view>
          <view class="flex flex-col items-center gap-1">
            <text class="text-[22px] font-bold text-white">{{ dash.like_count }}</text>
            <text class="text-[12px] text-white/60">我的点赞</text>
          </view>
          <view class="flex flex-col items-center gap-1">
            <text class="text-[22px] font-bold text-white">{{ dash.watching_drama_count }}</text>
            <text class="text-[12px] text-white/60">追更剧集</text>
          </view>
        </view>

        <!-- Login Banner -->
        <view v-if="!user.token" @click="goLogin" class="mt-6 flex items-center justify-between rounded-[16px] p-4 shadow-lg active:opacity-90" style="background: linear-gradient(135deg, #302619, #1c150c);">
          <view class="flex items-center gap-3">
            <view class="i-mdi-crown text-[38px] text-[#eec787] drop-shadow-md" />
            <view class="flex flex-col gap-1">
              <text class="text-[15px] font-bold text-[#eec787] tracking-wider">登录后解锁更多功能</text>
              <text class="text-[11px] text-[#eec787]/70">登录后可同步数据，多端观看更便捷</text>
            </view>
          </view>
          <view class="flex items-center justify-center rounded-full bg-gradient-to-r from-[#fef0d2] to-[#d4a055] px-4 py-[6px] shadow-sm">
            <text class="text-[13px] font-bold text-[#302619]">立即登录</text>
          </view>
        </view>

        <view v-else class="mt-6 flex items-center justify-between rounded-[16px] border border-white/10 bg-white/[0.03] p-4">
          <text class="text-[13px] text-white/70">已登录</text>
          <text class="text-[13px] text-[#a855f7] active:opacity-70" @click="logout">退出</text>
        </view>

        <!-- Common Features Grid -->
        <view class="mt-6 rounded-[16px] bg-[#121216] p-4 shadow-lg">
          <text class="text-[15px] font-bold text-white tracking-wide">常用功能</text>
          <view class="mt-6 grid grid-cols-4 gap-y-7">
            <view class="flex flex-col items-center gap-2 active:opacity-70" @click="goWatchHistory">
              <view class="flex h-[42px] w-[42px] items-center justify-center rounded-[12px] bg-gradient-to-br from-[#9a5cf6]/10 to-[#7c3aed]/5">
                <view class="i-mdi-clock-time-four-outline text-[24px] text-[#a855f7]" />
              </view>
              <text class="text-[11px] text-white/80">历史记录</text>
            </view>
            <view class="flex flex-col items-center gap-2 active:opacity-70">
              <view class="flex h-[42px] w-[42px] items-center justify-center rounded-[12px] bg-gradient-to-br from-[#60a5fa]/10 to-[#3b82f6]/5">
                <view class="i-mdi-star text-[24px] text-[#60a5fa]" />
              </view>
              <text class="text-[11px] text-white/80">我的收藏</text>
            </view>
            <view class="flex flex-col items-center gap-2 active:opacity-70">
              <view class="flex h-[42px] w-[42px] items-center justify-center rounded-[12px] bg-gradient-to-br from-[#f472b6]/10 to-[#ec4899]/5">
                <view class="i-mdi-heart text-[24px] text-[#f472b6]" />
              </view>
              <text class="text-[11px] text-white/80">我的点赞</text>
            </view>
            <view class="flex flex-col items-center gap-2 active:opacity-70" @click="goWatchHistory">
              <view class="flex h-[42px] w-[42px] items-center justify-center rounded-[12px] bg-gradient-to-br from-[#a855f7]/10 to-[#7c3aed]/5">
                <view class="i-mdi-play-box-multiple text-[24px] text-[#a855f7]" />
              </view>
              <text class="text-[11px] text-white/80">观看记录</text>
            </view>
            <view class="flex flex-col items-center gap-2 active:opacity-70">
              <view class="flex h-[42px] w-[42px] items-center justify-center rounded-[12px] bg-gradient-to-br from-[#a855f7]/10 to-[#7c3aed]/5">
                <view class="i-mdi-download text-[24px] text-[#a855f7]" />
              </view>
              <text class="text-[11px] text-white/80">离线缓存</text>
            </view>
            <view class="flex flex-col items-center gap-2 active:opacity-70">
              <view class="flex h-[42px] w-[42px] items-center justify-center rounded-[12px] bg-gradient-to-br from-[#a855f7]/10 to-[#7c3aed]/5">
                <view class="i-mdi-message-processing text-[24px] text-[#a855f7]" />
              </view>
              <text class="text-[11px] text-white/80">意见反馈</text>
            </view>
            <view class="flex flex-col items-center gap-2 active:opacity-70">
              <view class="flex h-[42px] w-[42px] items-center justify-center rounded-[12px] bg-gradient-to-br from-[#a855f7]/10 to-[#7c3aed]/5">
                <view class="i-mdi-help-circle text-[24px] text-[#a855f7]" />
              </view>
              <text class="text-[11px] text-white/80">帮助中心</text>
            </view>
            <view class="flex flex-col items-center gap-2 active:opacity-70">
              <view class="flex h-[42px] w-[42px] items-center justify-center rounded-[12px] bg-gradient-to-br from-[#a855f7]/10 to-[#7c3aed]/5">
                <view class="i-mdi-nut text-[24px] text-[#a855f7]" />
              </view>
              <text class="text-[11px] text-white/80">设置</text>
            </view>
          </view>
        </view>

        <!-- More Services -->
        <view class="mt-4 rounded-[16px] bg-[#121216] p-4 shadow-lg mb-4">
          <text class="text-[15px] font-bold text-white mb-5 block tracking-wide">更多服务</text>
          <view class="grid grid-cols-2 gap-x-6 gap-y-6">
            <view class="flex items-center justify-between active:opacity-70">
              <view class="flex items-center gap-2.5">
                <view class="i-mdi-trash-can-outline text-[20px] text-white/70" />
                <text class="text-[13px] text-white/80">清理缓存</text>
              </view>
              <view class="i-mdi-chevron-right text-[20px] text-white/30" />
            </view>
            <view class="flex items-center justify-between active:opacity-70">
              <view class="flex items-center gap-2.5">
                <view class="i-mdi-shield-check-outline text-[20px] text-white/70" />
                <text class="text-[13px] text-white/80">隐私政策</text>
              </view>
              <view class="i-mdi-chevron-right text-[20px] text-white/30" />
            </view>
            <view class="flex items-center justify-between active:opacity-70">
              <view class="flex items-center gap-2.5">
                <view class="i-mdi-file-document-outline text-[20px] text-white/70" />
                <text class="text-[13px] text-white/80">用户协议</text>
              </view>
              <view class="i-mdi-chevron-right text-[20px] text-white/30" />
            </view>
            <view class="flex items-center justify-between active:opacity-70">
              <view class="flex items-center gap-2.5">
                <view class="i-mdi-information-outline text-[20px] text-white/70" />
                <text class="text-[13px] text-white/80">关于我们</text>
              </view>
              <view class="i-mdi-chevron-right text-[20px] text-white/30" />
            </view>
          </view>
        </view>

      </view>
    </scroll-view>

    <!-- Bottom Tabbar -->
    <view class="absolute bottom-0 left-0 right-0 z-20 flex h-[56px] items-center justify-around bg-[#0a0a0f] pb-[env(safe-area-inset-bottom)] border-t border-white/5">
      <!-- Home Tab -->
      <view @click="switchTab('/pages/index/index')" class="flex flex-1 flex-col items-center justify-center gap-0.5 active:opacity-70">
        <view class="i-mdi-home text-[24px] text-white/50" />
        <text class="text-[10px] font-medium text-white/50">首页</text>
      </view>

      <!-- Theater Tab -->
      <view @click="switchTab('/pages/theater/index')" class="flex flex-1 flex-col items-center justify-center gap-1 active:opacity-70">
        <view class="flex h-[28px] w-[36px] items-center justify-center rounded-[8px] border border-white/30 bg-white/[0.08]">
          <view class="i-mdi-play text-[20px] text-white/80" />
        </view>
        <text class="text-[10px] font-medium text-white/50">剧场</text>
      </view>

      <!-- Mine Tab (Active) -->
      <view class="flex flex-1 flex-col items-center justify-center gap-0.5">
        <view class="i-mdi-account text-[24px] text-[#9a5cf6]" />
        <text class="text-[10px] font-medium text-[#9a5cf6]">我的</text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { computed, reactive } from 'vue'
import { onShow } from '@dcloudio/uni-app'
import { appApi } from '@/config'
import { useUserStore } from '@/stores/user'
import { authHeaders, needLogin } from '@/utils/app-http'

const user = useUserStore()

const dash = reactive({
  watch_history_count: 0,
  favorite_count: 0,
  like_count: 0,
  watching_drama_count: 0,
})

const displayName = computed(() => user.profile?.nick_name || user.profile?.user_name || '剧迷小丸子')
const displayId = computed(() => String(user.profile?.user_id ?? '—'))
const avatarSrc = computed(() => user.profile?.avatar || 'https://api.dicebear.com/7.x/avataaars/svg?seed=Felix')

function goLogin() {
  uni.navigateTo({ url: '/pages/login/index' })
}

function logout() {
  user.logout()
  dash.watch_history_count = 0
  dash.favorite_count = 0
  dash.like_count = 0
  dash.watching_drama_count = 0
  uni.showToast({ title: '已退出', icon: 'none' })
}

function loadDashboard() {
  if (!user.token) {
    dash.watch_history_count = 0
    dash.favorite_count = 0
    dash.like_count = 0
    dash.watching_drama_count = 0
    return
  }
  uni.request({
    url: appApi('/me/dashboard'),
    header: authHeaders(),
    success: (res: any) => {
      const b = res.data as any
      if (b.code !== 200 || !b.data) return
      const d = b.data
      dash.watch_history_count = Number(d.watch_history_count ?? 0)
      dash.favorite_count = Number(d.favorite_count ?? 0)
      dash.like_count = Number(d.like_count ?? 0)
      dash.watching_drama_count = Number(d.watching_drama_count ?? 0)
    },
  })
}

function goWatchHistory() {
  if (!needLogin()) return
  uni.navigateTo({ url: '/pages/watch-history/index' })
}

function switchTab(url: string) {
  uni.reLaunch({ url })
}

onShow(() => {
  user.fetchMe()
  loadDashboard()
})
</script>

<style scoped>
/* Scoped styles */
::-webkit-scrollbar {
  display: none;
}
</style>
