<template>
  <view class="min-h-screen bg-[#050505]">
    <!-- Search Bar -->
    <view class="flex items-center gap-3 px-4 pt-[calc(env(safe-area-inset-top)+12px)] pb-3 bg-[#050505]">
      <view class="flex h-10 flex-1 items-center gap-2 rounded-full bg-white/[0.08] px-4">
        <view class="i-mdi-magnify text-[20px] text-white/50" />
        <input
          v-model="keyword"
          class="flex-1 text-[14px] text-white placeholder-white/35"
          placeholder="搜索短剧名称"
          placeholder-class="text-white/35"
          confirm-type="search"
          @confirm="onSearch"
          @input="onInput"
        />
        <view v-if="keyword" class="i-mdi-close-circle text-[18px] text-white/30" @click="clearSearch" />
      </view>
      <text class="text-[14px] text-white/70 active:opacity-70" @click="goBack">取消</text>
    </view>

    <!-- Search Results -->
    <scroll-view scroll-y class="h-[calc(100vh-80px)] pb-[env(safe-area-inset-bottom)]">
      <!-- Empty state -->
      <view v-if="!keyword" class="py-16 text-center">
        <view class="i-mdi-magnify text-[48px] text-white/20" />
        <text class="mt-4 block text-[14px] text-white/40">输入关键词搜索短剧</text>
      </view>

      <!-- No results -->
      <view v-else-if="loaded && !rows.length" class="py-16 text-center">
        <text class="text-[14px] text-white/40">未找到相关短剧</text>
      </view>

      <!-- Results -->
      <view
        v-for="row in rows"
        :key="row.drama_id"
        class="flex gap-3 border-b border-white/[0.06] px-4 py-3 active:bg-white/[0.03]"
        @click="goDrama(row)"
      >
        <image :src="row.cover_url || placeholderCover" class="h-[72px] w-[52px] shrink-0 rounded-lg bg-white/5" mode="aspectFill" />
        <view class="min-w-0 flex-1 py-0.5">
          <text class="line-clamp-2 text-[15px] font-medium leading-snug text-white">{{ row.title || '剧目' }}</text>
          <view class="mt-1 flex items-center gap-1">
            <text class="text-[11px] text-white/45">{{ dramaTypeLabel(row.drama_type) }}</text>
            <text class="text-[11px] text-white/30">·</text>
            <text class="text-[11px] text-white/45">{{ row.heat || 0 }} 热</text>
          </view>
          <text v-if="row.tags" class="mt-1 block text-[10px] text-[#a855f7]/80">{{ row.tags }}</text>
        </view>
        <view class="flex shrink-0 items-center">
          <view class="i-mdi-chevron-right text-[20px] text-white/30" />
        </view>
      </view>

      <!-- Loading -->
      <view v-if="loading" class="py-8 text-center">
        <text class="text-[12px] text-white/40">搜索中...</text>
      </view>

      <!-- Recent searches -->
      <view v-if="!keyword && recentSearches.length" class="px-4">
        <view class="mb-3 flex items-center justify-between">
          <text class="text-[13px] text-white/50">最近搜索</text>
          <text class="text-[12px] text-white/30 active:opacity-70" @click="clearRecent">清除</text>
        </view>
        <view class="flex flex-wrap gap-2">
          <view
            v-for="s in recentSearches"
            :key="s"
            class="rounded-full bg-white/[0.06] px-3 py-1.5 text-[12px] text-white/70 active:bg-white/[0.1]"
            @click="useRecent(s)"
          >
            {{ s }}
          </view>
        </view>
      </view>
    </scroll-view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { onShow } from '@dcloudio/uni-app'
import { appApi } from '@/config'
import { authHeaders } from '@/utils/app-http'

const placeholderCover = 'https://images.unsplash.com/photo-1618331835717-801e976710b2?q=80&w=300&auto=format&fit=crop'

const keyword = ref('')
const rows = ref<Record<string, any>[]>([])
const loaded = ref(false)
const loading = ref(false)

const recentSearches = ref<string[]>([])

function dramaTypeLabel(t: string | null | undefined): string {
  const map: Record<string, string> = {
    urban: '都市', fantasy: '玄幻', romance: '言情',
    horror: '悬疑', comedy: '喜剧', sci_fi: '科幻',
    live_action: '真人', comic_drama: '漫剧',
  }
  return map[t ?? ''] || '短剧'
}

function onInput() {
  if (!keyword.value.trim()) {
    rows.value = []
    loaded.value = false
  }
}

function onSearch() {
  const kw = keyword.value.trim()
  if (!kw) return
  if (!recentSearches.value.includes(kw)) {
    recentSearches.value.unshift(kw)
    if (recentSearches.value.length > 10) recentSearches.value.pop()
    uni.setStorageSync('recent_searches', recentSearches.value)
  }
  fetchResults(kw)
}

function fetchResults(kw: string) {
  loading.value = true
  loaded.value = false
  uni.request({
    url: appApi('/dramas'),
    header: authHeaders({}),
    success: (res: any) => {
      const b = res.data as any
      loading.value = false
      loaded.value = true
      if (b.code !== 200 || !Array.isArray(b.data)) {
        rows.value = []
        return
      }
      const lowerKw = kw.toLowerCase()
      rows.value = b.data.filter((d: any) => {
        const title = (d.title || '').toLowerCase()
        const tags = (d.tags || '').toLowerCase()
        const dramaType = (d.drama_type || '').toLowerCase()
        return title.includes(lowerKw) || tags.includes(lowerKw) || dramaType.includes(lowerKw)
      })
    },
    fail: () => {
      loading.value = false
      loaded.value = true
      rows.value = []
    },
  })
}

function clearSearch() {
  keyword.value = ''
  rows.value = []
  loaded.value = false
}

function clearRecent() {
  recentSearches.value = []
  uni.removeStorageSync('recent_searches')
}

function useRecent(s: string) {
  keyword.value = s
  onSearch()
}

function goDrama(row: Record<string, any>) {
  const did = row.drama_id
  if (!did) {
    uni.showToast({ title: '数据异常', icon: 'none' })
    return
  }
  uni.navigateTo({ url: `/pages/drama-detail/index?drama_id=${did}` })
}

function goBack() {
  uni.navigateBack()
}

onShow(() => {
  const saved = uni.getStorageSync('recent_searches')
  if (Array.isArray(saved)) recentSearches.value = saved
})
</script>

<style scoped>
::-webkit-scrollbar { display: none; }
</style>