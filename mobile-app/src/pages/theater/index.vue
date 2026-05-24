<template>
  <view class="relative h-screen w-screen overflow-hidden bg-[#050505]">
    <view class="flex h-full flex-col px-4 pt-[calc(env(safe-area-inset-top)+10px)]">
      <!-- Title -->
      <text class="mt-2 text-[26px] font-bold tracking-wide text-white">剧场</text>

      <!-- Search & Filter -->
      <view class="mt-4 flex items-center justify-between gap-3">
        <!-- Search -->
        <view class="flex h-[38px] flex-1 items-center rounded-full bg-white/[0.08] px-4">
          <view class="i-mdi-magnify mr-2 text-[18px] text-white/50" />
          <input
            v-model="keyword"
            class="flex-1 bg-transparent text-[14px] text-white/50"
            placeholder="搜索剧名、演员、角色"
            placeholder-class="text-white/50"
            confirm-type="search"
            @confirm="loadDramas"
          />
        </view>
        <!-- Filter -->
        <view class="flex h-[38px] items-center rounded-full border border-white/5 bg-white/[0.05] px-4 active:bg-white/10" @click="showFilterSheet">
          <view class="i-mdi-filter-variant mr-1.5 text-[16px] text-white/80" />
          <text class="text-[14px] text-white/80">筛选</text>
        </view>
        <!-- Share -->
        <view class="flex h-[38px] w-[38px] items-center justify-center rounded-full border border-white/5 bg-white/[0.05] active:bg-white/10" @click="onShare">
          <view class="i-mdi-share-variant text-[18px] text-white/80" />
        </view>
      </view>

      <!-- Tabs -->
      <view class="mt-6 flex items-center gap-4 px-1 overflow-x-auto">
        <view
          v-for="tab in typeTabs"
          :key="tab.value"
          class="relative flex shrink-0 flex-col items-center"
          @click="setTypeTab(tab.value)"
        >
          <text :class="dramaType === tab.value ? 'text-[17px] font-medium text-white' : 'text-[16px] text-white/50'">{{ tab.label }}</text>
          <view
            :class="
              dramaType === tab.value ? 'mt-1.5 h-[3px] w-[14px] rounded-full bg-[#9a5cf6]' : 'mt-1.5 h-[3px] w-[14px] rounded-full bg-transparent'
            "
          ></view>
        </view>
      </view>

      <!-- Sub-filters / Sort -->
      <view class="mt-5 flex items-center justify-between px-1">
        <view class="flex items-center gap-2.5">
          <view
            v-for="s in sortOptions"
            :key="s.value"
            class="rounded-full px-3.5 py-1.5"
            :class="sortType === s.value ? 'bg-[#9a5cf6]' : 'bg-white/[0.06]'"
            @click="setSort(s.value)"
          >
            <text :class="sortType === s.value ? 'text-[12px] font-medium text-white' : 'text-[12px] text-white/70'">{{ s.label }}</text>
          </view>
        </view>
        <view class="flex items-center active:opacity-70" @click="clearTagFilter">
          <text :class="selectedTag ? 'text-[12px] text-[#9a5cf6]' : 'text-[12px] text-white/70'">{{ selectedTag || '全部标签' }}</text>
          <view class="i-mdi-chevron-down ml-0.5 text-[16px] text-white/70" />
        </view>
      </view>

      <!-- Drama Grid -->
      <scroll-view scroll-y class="mt-4 flex-1 overflow-y-auto pb-[90px]">
        <!-- Empty State -->
        <view v-if="!gridItems.length" class="flex flex-col items-center justify-center py-24">
          <view class="i-mdi-filmstrip-off text-[56px] text-white/20" />
          <text class="mt-4 text-[14px] text-white/40">暂无短剧内容</text>
        </view>
        <!-- Skeleton Loading -->
        <view v-if="isLoading" class="grid grid-cols-2 gap-3 pb-8">
          <view v-for="n in 6" :key="n" class="overflow-hidden rounded-[12px] bg-[#121216]">
            <view class="aspect-[3/4] w-full animate-pulse bg-[#1e1e28]" />
            <view class="p-2.5">
              <view class="mt-2 h-4 w-3/4 rounded bg-[#1e1e28] animate-pulse" />
              <view class="mt-2 flex gap-1.5">
                <view class="h-3 w-10 rounded bg-[#1e1e28] animate-pulse" />
                <view class="h-3 w-10 rounded bg-[#1e1e28] animate-pulse" />
              </view>
              <view class="mt-2 h-3 w-12 rounded bg-[#1e1e28] animate-pulse" />
            </view>
          </view>
        </view>
        <!-- Grid -->
        <view v-else class="grid grid-cols-2 gap-3 pb-8">
          <view
            v-for="d in gridItems"
            :key="d.id"
            class="relative overflow-hidden rounded-[12px] bg-[#121216] transition-transform active:scale-[0.98]"
            @click="goDetail(d.id)"
          >
            <!-- aspect ratio container for card -->
            <view class="relative aspect-[3/4] w-full">
              <image :src="d.cover" class="h-full w-full object-cover" mode="aspectFill" />

              <!-- Top Left Label -->
              <view
                v-if="d.label === '热播' || d.label === '热剧'"
                class="absolute left-0 top-0 rounded-br-[10px] rounded-tl-[12px] bg-gradient-to-r from-[#9a5cf6] to-[#d946ef] px-2 py-0.5"
              >
                <text class="text-[10px] font-medium text-white">{{ d.label }}</text>
              </view>
              <view v-else class="absolute left-0 top-0 rounded-br-[10px] rounded-tl-[12px] bg-gradient-to-r from-[#7c3aed] to-[#6366f1] px-2 py-0.5">
                <text class="text-[10px] font-medium text-white">{{ d.label }}</text>
              </view>

              <!-- Bottom Gradient overlay -->
              <view class="absolute bottom-0 left-0 right-0 h-[60%] bg-gradient-to-t from-black via-black/70 to-transparent"></view>

              <!-- Bottom Content Info -->
              <view class="absolute bottom-0 left-0 right-0 flex flex-col p-2.5">
                <text class="truncate text-[15px] font-bold text-white shadow-sm">{{ d.title }}</text>
                <view class="mt-1.5 flex flex-wrap gap-1.5">
                  <view v-for="tag in d.tags" :key="tag" class="rounded-[4px] bg-white/[0.15] px-1.5 py-[2px] backdrop-blur-sm">
                    <text class="text-[10px] text-white/80">{{ tag }}</text>
                  </view>
                </view>
                <view class="mt-2 flex items-center">
                  <text class="text-[10px] text-[#ff9900]">🔥</text>
                  <text class="ml-1 text-[11px] font-medium text-[#facc15]">{{ d.hot }}</text>
                </view>
              </view>
            </view>
          </view>
        </view>
      </scroll-view>
    </view>

    <!-- Bottom Tabbar -->
    <view class="absolute bottom-0 left-0 right-0 z-20 flex h-[56px] items-center justify-around border-t border-white/5 bg-[#0a0a0f] pb-[env(safe-area-inset-bottom)]">
      <!-- Home Tab -->
      <view @click="switchTab('/pages/index/index')" class="flex flex-1 flex-col items-center justify-center gap-0.5 active:opacity-70">
        <view class="i-mdi-home text-[24px] text-white/50" />
        <text class="text-[10px] font-medium text-white/50">首页</text>
      </view>

      <!-- Theater Tab (Active) -->
      <view class="flex flex-1 flex-col items-center justify-center gap-1">
        <view class="flex h-[28px] w-[36px] items-center justify-center rounded-[8px] border border-[#9a5cf6] bg-[#9a5cf6]/20">
          <view class="i-mdi-play text-[20px] text-[#9a5cf6]" />
        </view>
        <text class="text-[10px] font-medium text-[#9a5cf6]">剧场</text>
      </view>

      <!-- Mine Tab -->
      <view @click="switchTab('/pages/mine/index')" class="flex flex-1 flex-col items-center justify-center gap-0.5 active:opacity-70">
        <view class="i-mdi-account-outline text-[24px] text-white/50" />
        <text class="text-[10px] font-medium text-white/50">我的</text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { appApi } from '@/config'

const placeholderCover =
  'https://images.unsplash.com/photo-1618331835717-801e976710b2?q=80&w=600&auto=format&fit=crop'

interface DramaRow {
  drama_id: number
  title: string
  cover_url?: string | null
  drama_type?: string
  tags?: string | null
  heat?: number | null
}

interface GridItem {
  id: number
  title: string
  cover: string
  tags: string[]
  hot: string
  label: string
}

const rawDramas = ref<DramaRow[]>([])
const dramaType = ref<'all' | 'urban' | 'costume' | 'romance' | 'fantasy' | 'sci_fi'>('all')
const keyword = ref('')
const sortType = ref<'recommend' | 'latest' | 'heat'>('recommend')
const selectedTag = ref<string | null>(null)
const isLoading = ref(true)

// Type tab labels
const typeTabs = [
  { value: 'all' as const, label: '全部' },
  { value: 'urban' as const, label: '都市' },
  { value: 'costume' as const, label: '古风' },
  { value: 'romance' as const, label: '甜宠' },
  { value: 'fantasy' as const, label: '玄幻' },
  { value: 'sci_fi' as const, label: '科幻' },
]

const gridItems = computed<GridItem[]>(() => {
  let items = rawDramas.value
  if (selectedTag.value) {
    items = items.filter(d => {
      const tags = tagList(d)
      return tags.some(t => t.includes(selectedTag.value!))
    })
  }
  return items.map((d) => ({
    id: d.drama_id,
    title: d.title,
    cover: d.cover_url || placeholderCover,
    tags: tagList(d),
    hot: heatShort(d.heat),
    label: labelFor(d),
  }))
})

const sortOptions = [
  { value: 'recommend' as const, label: '推荐' },
  { value: 'latest' as const, label: '最新' },
  { value: 'heat' as const, label: '热度' },
]

const allTags = computed<string[]>(() => {
  const tagSet = new Set<string>()
  rawDramas.value.forEach(d => tagList(d).forEach(t => tagSet.add(t)))
  return Array.from(tagSet).sort()
})

function showFilterSheet() {
  if (allTags.value.length === 0) {
    uni.showToast({ title: '暂无可筛选标签', icon: 'none' })
    return
  }
  const items = ['全部标签', ...allTags.value]
  uni.showActionSheet({
    itemList: items,
    itemColor: '#9a5cf6',
    success: (res) => {
      if (res.tapIndex === 0) {
        selectedTag.value = null
      } else {
        selectedTag.value = items[res.tapIndex]
      }
    },
  })
}

function clearTagFilter() {
  selectedTag.value = null
}

function setTypeTab(t: 'all' | 'urban' | 'costume' | 'romance' | 'fantasy' | 'sci_fi') {
  dramaType.value = t
  selectedTag.value = null
  loadDramas()
}

function setSort(s: 'recommend' | 'latest' | 'heat') {
  sortType.value = s
  selectedTag.value = null
  loadDramas()
}

function tagList(d: DramaRow): string[] {
  const raw = d.tags
  if (!raw) return ['短剧', '热门']
  try {
    const j = JSON.parse(raw)
    if (Array.isArray(j)) return j.map(String).slice(0, 4)
  } catch {
    /* ignore */
  }
  return raw
    .split(/[,，、\s]+/)
    .map((s) => s.trim())
    .filter(Boolean)
    .slice(0, 4)
}

function heatShort(h?: number | null): string {
  if (h == null || Number.isNaN(Number(h))) return '—'
  const n = Number(h)
  if (n >= 10000) return `${(n / 10000).toFixed(1)}万`
  return String(n)
}

function labelFor(d: DramaRow): string {
  const h = Number(d.heat || 0)
  if (h >= 500000) return '热播'
  return '新剧'
}

function goDetail(id: number) {
  uni.navigateTo({ url: `/pages/drama-detail/index?id=${id}` })
}

function switchTab(url: string) {
  uni.reLaunch({ url })
}

function loadDramas() {
  isLoading.value = true
  uni.request({
    url: appApi('/dramas'),
    data: {
      ...(dramaType.value !== 'all' ? { drama_type: dramaType.value } : {}),
      ...(sortType.value !== 'recommend' ? { sort: sortType.value } : {}),
      ...(keyword.value.trim() ? { keyword: keyword.value.trim() } : {}),
    },
    success: (res: any) => {
      const body = res.data as any
      if (body.code === 200 && Array.isArray(body.rows)) {
        rawDramas.value = body.rows as DramaRow[]
      } else {
        rawDramas.value = []
      }
    },
    fail: () => {
      rawDramas.value = []
    },
    complete: () => {
      isLoading.value = false
    },
  })
}

function onShare() {
  uni.share({
    provider: 'weixin',
    scene: 'WXSceneSession',
    title: 'AI 互动短剧 — 沉浸式分支剧情',
    summary: '海量短剧、互动分支，体验不一样的人生',
    success: () => uni.showToast({ title: '分享成功', icon: 'none' }),
    fail: () => {
      uni.share({
        provider: '',
        type: 0,
        title: 'AI 互动短剧 — 沉浸式分支剧情',
        success: () => {},
        fail: () => {
          /* system share unavailable — no toast spam */
        },
      })
    },
  })
}

onMounted(() => {
  loadDramas()
})
</script>

<style scoped>
::-webkit-scrollbar {
  display: none;
}
</style>
