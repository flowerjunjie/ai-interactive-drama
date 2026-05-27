<template>
  <view class="relative h-screen w-screen overflow-hidden bg-[#050505]">
    <!-- Search Icon (Top Right) -->
    <view class="absolute left-0 right-0 z-30 flex items-center justify-end px-4 pt-[calc(env(safe-area-inset-top)+8px)]">
      <view class="flex h-9 w-9 items-center justify-center active:opacity-70" @click="goSearch">
        <view class="i-mdi-magnify text-[24px] text-white" />
      </view>
    </view>

    <!-- Background Image (Click to play) -->
    <navigator :url="heroPlayPath" hover-class="none" class="absolute inset-0 z-0">
      <image :src="heroCover" class="h-full w-full object-cover" mode="aspectFill" />
    </navigator>

    <!-- Gradient Overlay for better text readability and dark theme -->
    <view class="absolute inset-0 bg-gradient-to-b from-black/30 via-transparent to-black/80"></view>

    <!-- Right Sidebar Interaction -->
    <view class="absolute bottom-[90px] right-3 z-10 flex w-12 flex-col items-center gap-5">
      <!-- Profile -->
      <view class="relative flex flex-col items-center">
        <view class="h-11 w-11 overflow-hidden rounded-full border-[1.5px] border-white">
          <image src="https://api.dicebear.com/7.x/avataaars/svg?seed=Felix" class="h-full w-full object-cover" />
        </view>
        <view class="absolute -bottom-2 left-1/2 flex h-[18px] w-[18px] -translate-x-1/2 items-center justify-center rounded-full bg-[#ff2442] shadow-sm">
          <text class="text-xs font-bold leading-none text-white">+</text>
        </view>
        <text class="mt-3 text-[11px] font-medium text-white drop-shadow-md">关注</text>
      </view>

      <!-- Like -->
      <view class="flex flex-col items-center gap-0.5" @click.stop="onLikeTap">
        <view class="i-mdi-heart text-[34px] text-white drop-shadow-md" />
        <text class="text-[11px] font-medium text-white drop-shadow-md">{{ formatShortCount(likeTotal) }}</text>
      </view>

      <!-- Comment -->
      <view class="flex flex-col items-center gap-0.5" @click.stop="onCommentTap">
        <view class="i-mdi-comment-processing text-[32px] text-white drop-shadow-md" />
        <text class="text-[11px] font-medium text-white drop-shadow-md">{{ formatShortCount(commentTotal) }}</text>
      </view>

      <!-- Favorite -->
      <view class="flex flex-col items-center gap-0.5" @click.stop="onFavoriteTap">
        <view class="i-mdi-star text-[34px] text-white drop-shadow-md" />
        <text class="text-[11px] font-medium text-white drop-shadow-md">{{ heatLabel }}</text>
      </view>

      <!-- Share -->
      <view class="flex flex-col items-center gap-0.5" @click.stop="onShareTap">
        <view class="i-mdi-share text-[34px] text-white drop-shadow-md" />
        <text class="text-[11px] font-medium text-white drop-shadow-md">分享</text>
      </view>

      <!-- Record (Music) -->
      <view class="mt-3 flex flex-col items-center gap-1">
        <view class="relative flex h-11 w-11 animate-[spin_4s_linear_infinite] items-center justify-center rounded-full bg-black/60">
          <view class="h-[26px] w-[26px] overflow-hidden rounded-full">
            <image src="https://api.dicebear.com/7.x/avataaars/svg?seed=Felix" class="h-full w-full object-cover" />
          </view>
        </view>
      </view>
    </view>

    <!-- Bottom Left Content -->
    <view class="absolute bottom-[90px] left-4 right-16 z-10 flex flex-col items-start pr-2">
      <!-- Tag -->
      <view class="mb-2.5 flex items-center rounded border border-white/10 bg-black/30 px-1.5 py-0.5 backdrop-blur-sm">
        <text class="text-[11px] text-[#ff9900]">🔥</text>
        <text class="ml-1 text-[11px] text-white/90">热播TOP3</text>
      </view>

      <!-- Title -->
      <text class="mb-2 text-[26px] font-bold tracking-wider text-white drop-shadow-lg">{{ heroTitle }}</text>

      <!-- Status -->
      <view class="mb-2 flex items-center text-white drop-shadow-md">
        <view class="i-mdi-play mr-0.5 text-[15px]" />
        <text class="text-[13px] font-medium text-white/90">{{ heroEpisodeLine }}</text>
      </view>

      <!-- Description -->
      <text class="mb-2.5 text-[13px] leading-[1.6] text-white/90 drop-shadow-md">{{ heroDesc }}</text>

      <!-- Tags -->
      <view class="mb-4 flex flex-wrap gap-2">
        <text v-for="t in heroTagList" :key="t" class="rounded bg-white/10 px-2 py-0.5 text-[11px] text-white/80 backdrop-blur-sm">{{ t }}</text>
      </view>

      <!-- Action Button -->
      <navigator
        :url="dramaDetailPath"
        hover-class="none"
        class="flex w-full items-center justify-between rounded-[10px] px-4 py-[11px] shadow-lg active:opacity-90"
        style="background: linear-gradient(90deg, #2a1147 0%, #763b38 50%, #c4602f 100%)"
      >
        <text class="flex-1 text-center text-[14px] font-medium text-white">{{ watchAllLine }}</text>
        <view class="i-mdi-chevron-right text-[20px] text-white/70" />
      </navigator>
    </view>

    <!-- Bottom Tabbar -->
    <view class="absolute bottom-0 left-0 right-0 z-20 flex h-[56px] items-center justify-around bg-[#0a0a0f] pb-[env(safe-area-inset-bottom)]">
      <!-- Home Tab -->
      <view class="flex flex-1 flex-col items-center justify-center gap-0.5">
        <view class="i-mdi-home text-[24px] text-[#9a5cf6]" />
        <text class="text-[10px] font-medium text-[#9a5cf6]">首页</text>
      </view>

      <!-- Theater Tab -->
      <view @click="switchTab('/pages/theater/index')" class="flex flex-1 flex-col items-center justify-center gap-1 active:opacity-70">
        <view class="flex h-[28px] w-[36px] items-center justify-center rounded-[8px] border border-white/30 bg-white/[0.08]">
          <view class="i-mdi-play text-[20px] text-white/80" />
        </view>
        <text class="text-[10px] font-medium text-white/50">剧场</text>
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
import { authHeaders, needLogin } from '@/utils/app-http'
import { formatShortCount } from '@/utils/format'
import { safeShare } from '@/utils/share'
import { DEFAULT_COVER } from '@/constants'

const heroNodeId = ref(0)
const heroCover = ref(DEFAULT_COVER)
const heroTitle = ref('逆天战神')
const heroDesc = ref('少年林辰，遭家族背叛，血脉被夺，绝境之下觉醒上古战神血脉！')
const heroTagsRaw = ref('')
const heroDramaId = ref<number | null>(null)
const heroEpisodeNo = ref<number | null>(null)
const episodeTotalHint = ref<number | null>(null)

const heroTagList = computed(() => {
  const fromApi = parseTags(heroTagsRaw.value)
  if (fromApi.length) return fromApi
  return ['逆袭', '战神', '玄幻', '热血']
})

const heroEpisodeLine = computed(() => {
  const ep = heroEpisodeNo.value
  const tot = episodeTotalHint.value
  if (ep != null && tot != null) return `第${ep}集 | 共${tot}集`
  if (ep != null) return `第${ep}集`
  return '第1集 | 共80集'
})

const heroPlayPath = computed(() => {
  if (heroNodeId.value) return `/pages/player/index?nodeId=${heroNodeId.value}`
  return '/pages/theater/index'
})

const dramaDetailPath = computed(() => {
  if (heroDramaId.value) return `/pages/drama-detail/index?id=${heroDramaId.value}`
  return '/pages/drama-detail/index'
})

const watchAllLine = computed(() => {
  const t = episodeTotalHint.value
  if (t != null) return `观看全集 · 更新至第${t}集`
  return '观看全集 · 更新至第80集'
})

function parseTags(raw: string): string[] {
  if (!raw) return []
  try {
    const j = JSON.parse(raw)
    if (Array.isArray(j)) return j.map(String).slice(0, 6)
  } catch {
    /* ignore */
  }
  return raw
    .split(/[,，、\s]+/)
    .map((s) => s.trim())
    .filter(Boolean)
    .slice(0, 6)
}

const likeTotal = ref(286000)
const commentTotal = ref(3689)
const heroHeat = ref(9865000)

const heatLabel = computed(() => formatShortCount(heroHeat.value))

function refreshSideStats() {
  const nid = heroNodeId.value
  const did = heroDramaId.value
  if (nid) {
    uni.request({
      url: appApi(`/video-nodes/${nid}`),
      success: (res: any) => {
        const b = res.data as any
        if (b.code === 200 && b.data?.like_count != null) {
          likeTotal.value = Number(b.data.like_count)
        }
      },
    })
  }
  if (did) {
    uni.request({
      url: appApi('/comments'),
      data: { drama_id: did },
      success: (res: any) => {
        const b = res.data as any
        if (b.code === 200 && Array.isArray(b.rows)) {
          commentTotal.value = b.rows.length
        }
      },
    })
  }
}

function onLikeTap() {
  if (!needLogin()) return
  const nid = heroNodeId.value
  if (!nid) return
  uni.request({
    url: appApi('/like'),
    method: 'POST',
    header: authHeaders(),
    data: { target_type: 'node', target_id: nid },
    success: (res: any) => {
      const b = res.data as any
      if (b.code === 200) {
        refreshSideStats()
        uni.showToast({ title: b.data?.liked ? '已点赞' : '已取消', icon: 'none' })
      }
    },
  })
}

function onFavoriteTap() {
  if (!needLogin()) return
  const did = heroDramaId.value
  if (!did) return
  uni.request({
    url: appApi('/favorite'),
    method: 'POST',
    header: authHeaders(),
    data: { drama_id: did },
    success: (res: any) => {
      const b = res.data as any
      if (b.code === 200) {
        uni.showToast({ title: b.data?.favorited ? '已收藏剧目' : '已取消收藏', icon: 'none' })
      }
    },
  })
}

function onCommentTap() {
  if (!needLogin()) return
  const did = heroDramaId.value
  if (did) uni.navigateTo({ url: `/pages/drama-detail/index?id=${did}` })
  else uni.showToast({ title: '暂无剧目', icon: 'none' })
}

function onShareTap() {
  safeShare({ title: 'AI 互动短剧 — 沉浸式分支剧情，体验不一样的人生' })
}

function switchTab(url: string) {
  uni.reLaunch({ url })
}

function goSearch() {
  uni.navigateTo({ url: '/pages/search/index' })
}

function applyFirstVideoRow(rows: any[]) {
  const first = rows?.find((it) => it?.kind === 'video' && it.node && it.drama)
  if (!first) return
  heroNodeId.value = Number(first.node.node_id) || 0
  heroCover.value = first.node.cover_url || first.drama.cover_url || heroCover.value
  heroTitle.value = first.drama.title || heroTitle.value
  heroDesc.value = first.drama.description || heroDesc.value
  heroDramaId.value = first.drama.drama_id ?? null
  heroTagsRaw.value = first.drama.tags != null ? String(first.drama.tags) : ''
  heroEpisodeNo.value = first.node.episode_no != null ? Number(first.node.episode_no) : null
  heroHeat.value = Number(first.drama.heat ?? heroHeat.value)
}

onMounted(() => {
  uni.request({
    url: appApi('/feed'),
    data: { page_num: 1, page_size: 15 },
    success: (res: any) => {
      const body = res.data as any
      if (body.code === 200 && Array.isArray(body.rows)) {
        applyFirstVideoRow(body.rows)
        const dId = heroDramaId.value
        if (dId) {
          uni.request({
            url: appApi(`/dramas/${dId}`),
            success: (r: any) => {
              const b = r.data as any
              if (b.code === 200 && b.data?.episode_total != null) {
                episodeTotalHint.value = Number(b.data.episode_total)
              }
            },
          })
        }
        refreshSideStats()
      }
    },
  })
})
</script>

<style scoped>
/* Scoped styles if needed */
</style>
