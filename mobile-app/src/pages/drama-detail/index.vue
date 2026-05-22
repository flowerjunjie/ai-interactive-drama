<template>
  <view class="relative min-h-screen w-screen overflow-x-hidden bg-[#050505]">
    <!-- Custom Navigation Bar -->
    <view class="fixed left-0 right-0 top-0 z-50 bg-[#050505] pt-[env(safe-area-inset-top)]">
      <view class="flex h-11 items-center justify-between px-4">
        <view class="flex h-8 w-8 items-center active:opacity-70" @click="goBack">
          <view class="i-mdi-chevron-left text-[32px] text-white" />
        </view>
        <view class="flex items-center gap-1 active:opacity-70">
          <view class="i-mdi-share-variant-outline text-[18px] text-white" />
          <text class="text-[13px] font-medium text-white">分享</text>
        </view>
      </view>
    </view>

    <!-- Main Content -->
    <scroll-view scroll-y class="h-screen pb-10 pt-[calc(env(safe-area-inset-top)+44px)]">
      <!-- Section 1: Header Info -->
      <view class="flex gap-4 px-4 pt-4">
        <!-- Cover -->
        <view class="relative h-[160px] w-[116px] shrink-0 overflow-hidden rounded-[10px] bg-gray-800">
          <image :src="posterSrc" class="h-full w-full object-cover" mode="aspectFill" />
          <!-- Play icon overlay -->
          <view class="absolute inset-0 flex items-center justify-center bg-black/10" @click="playEntry">
            <view class="flex h-10 w-10 items-center justify-center rounded-full bg-black/40 backdrop-blur-sm">
              <view class="i-mdi-play ml-0.5 text-[24px] text-white" />
            </view>
          </view>
          <!-- Title overlay on image to mimic poster -->
          <view class="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/80 to-transparent pb-6 pt-12 text-center">
            <text class="font-display text-[17px] font-bold italic tracking-widest text-[#f0d0a0] drop-shadow-md">{{ displayTitle }}</text>
          </view>
          <!-- Episode Pill -->
          <view
            class="absolute bottom-1.5 left-1/2 flex -translate-x-1/2 items-center justify-center rounded-full border border-white/20 bg-black/60 px-2 py-[2px] backdrop-blur-md"
          >
            <text class="whitespace-nowrap text-[10px] text-white/90">共{{ episodeTotal }}集</text>
          </view>
        </view>

        <!-- Right Info -->
        <view class="flex flex-1 flex-col">
          <text class="text-[20px] font-bold tracking-wide text-white">{{ displayTitle }}</text>

          <view class="mt-2 flex items-center gap-1">
            <text class="text-[12px] text-[#ff9900]">🔥</text>
            <text class="text-[13px] font-medium text-[#ff9900]">{{ displayHeat }}</text>
          </view>

          <view class="mt-2.5 flex flex-wrap gap-2">
            <view v-for="t in displayTagPills" :key="t" class="rounded-[4px] bg-white/[0.08] px-2 py-0.5 backdrop-blur-sm">
              <text class="text-[11px] text-white/80">{{ t }}</text>
            </view>
          </view>

          <view class="mt-3">
            <text class="line-clamp-3 text-[12px] leading-[1.6] text-white/70" :class="{ 'line-clamp-3': !descExpanded, 'line-clamp-none': descExpanded }">{{ displayDesc }}</text>
            <view class="mt-1 flex items-center active:opacity-70" @click="descExpanded = !descExpanded">
              <text class="text-[12px] text-white/50">{{ descExpanded ? '收起' : '展开' }}</text>
              <view class="i-mdi-chevron-down text-[16px] text-white/50" :class="{ 'rotate-180': descExpanded }" />
            </view>
          </view>
        </view>
      </view>

      <!-- Section 2: Action Buttons -->
      <view class="mt-6 flex flex-col gap-3 px-4">
        <!-- Watch Button -->
        <view
          class="flex w-full items-center justify-center rounded-full py-[11px] shadow-lg active:opacity-90"
          style="background: linear-gradient(90deg, #7e42f5 0%, #d459ad 50%, #f47a61 100%)"
          @click="playEntry"
        >
          <view class="i-mdi-play mr-1 text-[20px] text-white" />
          <text class="text-[15px] font-bold tracking-wide text-white">立即观看</text>
        </view>
        <!-- Favorite Button -->
        <view class="flex w-full items-center justify-center rounded-full bg-white/[0.08] py-[11px] active:bg-white/10" @click="toggleFav">
          <view :class="favorited ? 'i-mdi-star text-[18px] text-[#facc15]' : 'i-mdi-star-outline text-[18px] text-white/90'" />
          <text class="text-[15px] font-medium tracking-wide text-white/90">{{ favorited ? '已收藏' : '收藏' }}</text>
        </view>
        <!-- Subscribe / Chase Button -->
        <view class="flex w-full items-center justify-center rounded-full bg-white/[0.08] py-[11px] active:bg-white/10" @click="toggleSub">
          <view :class="subscribed ? 'i-mdi-bell text-[18px] text-[#9a5cf6]' : 'i-mdi-bell-outline text-[18px] text-white/90'" />
          <text class="text-[15px] font-medium tracking-wide text-white/90">{{ subscribed ? '已追更' : '追更' }}</text>
        </view>
      </view>

      <!-- Section 3: Drama Info -->
      <view class="mx-4 mt-6 rounded-[12px] bg-[#121216] p-4">
        <view class="flex items-center justify-between">
          <text class="text-[14px] font-bold text-white">剧集信息</text>
          <view class="i-mdi-dots-horizontal text-[20px] text-white/50" />
        </view>
        <view class="mt-4 flex justify-between gap-2 overflow-x-auto whitespace-nowrap pb-1">
          <view class="flex shrink-0 flex-col gap-1.5">
            <text class="text-[11px] text-white/40">导演</text>
            <text class="text-[12px] text-white/90">张一白</text>
          </view>
          <view class="flex shrink-0 flex-col gap-1.5">
            <text class="text-[11px] text-white/40">主演</text>
            <text class="text-[12px] text-white/90">林一 / 赵露思</text>
          </view>
          <view class="flex shrink-0 flex-col gap-1.5">
            <text class="text-[11px] text-white/40">类型</text>
            <text class="text-[12px] text-white/90">{{ typeLabel || '漫剧 / 玄幻' }}</text>
          </view>
          <view class="flex shrink-0 flex-col gap-1.5">
            <text class="text-[11px] text-white/40">更新状态</text>
            <text class="text-[12px] text-white/90">已完结</text>
          </view>
          <view class="flex shrink-0 flex-col gap-1.5">
            <text class="text-[11px] text-white/40">更新时间</text>
            <text class="text-[12px] text-white/90">2024-04-20</text>
          </view>
        </view>
      </view>

      <!-- Section 4: Episode List -->
      <view class="mt-8 px-4">
        <view class="mb-4 flex items-center justify-between">
          <text class="text-[15px] font-bold text-white">剧集列表</text>
          <view class="flex items-center active:opacity-70">
            <text class="text-[12px] text-white/60">共{{ episodeTotal }}集</text>
            <view class="i-mdi-chevron-right text-[18px] text-white/60" />
          </view>
        </view>

        <scroll-view scroll-x class="whitespace-nowrap pb-2">
          <view class="inline-flex gap-2.5 pr-4">
            <view
              v-for="ep in episodes"
              :key="ep.node_id"
              class="flex h-[60px] w-[60px] shrink-0 flex-col items-center justify-center rounded-[10px] active:bg-white/10"
              :class="isEntryEpisode(ep) ? 'border border-[#9a5cf6] bg-[#9a5cf6]/10' : 'bg-white/[0.05]'"
              @click="playNode(ep.node_id)"
            >
              <template v-if="isEntryEpisode(ep)">
                <view class="mt-1 flex flex-col items-center gap-[2px]">
                  <view class="flex h-[10px] items-end gap-[2px]">
                    <view class="h-[6px] w-[2px] rounded-full bg-[#9a5cf6] animate-pulse"></view>
                    <view class="h-[10px] w-[2px] rounded-full bg-[#9a5cf6] animate-pulse delay-75"></view>
                    <view class="h-[5px] w-[2px] rounded-full bg-[#9a5cf6] animate-pulse delay-150"></view>
                  </view>
                  <text class="mt-0.5 text-[9px] font-medium text-[#9a5cf6]">播放中</text>
                </view>
              </template>
              <template v-else>
                <text class="text-[16px] font-medium text-white/90">{{ ep.episode_no ?? ep.node_id }}</text>
                <view class="i-mdi-lock mt-0.5 text-[12px] text-white/30" />
              </template>
            </view>
            <view
              v-if="episodes.length > 6"
              class="flex h-[60px] w-[46px] shrink-0 items-center justify-center rounded-[10px] bg-white/[0.04] active:bg-white/10"
            >
              <view class="i-mdi-dots-horizontal text-[24px] text-white/40" />
            </view>
          </view>
        </scroll-view>
      </view>

      <!-- Section: Comments -->
      <view v-if="drama" class="mx-4 mt-6 border-t border-white/5 px-0 pt-5">
        <view class="mb-4 flex items-center justify-between px-0">
          <text class="text-[15px] font-bold text-white">精彩评论</text>
          <text class="text-[12px] text-white/50">共{{ commentList.length }}条</text>
        </view>
        <text v-if="!commentList.length" class="mb-4 block text-[13px] text-white/40">暂无评论，快来抢沙发～</text>
        <view v-for="c in commentList.slice(0, 6)" :key="c.comment_id" class="mb-4 flex gap-3">
          <image :src="fallbackCover" class="mt-0.5 h-8 w-8 shrink-0 rounded-full bg-gray-800" />
          <view class="flex-1">
            <view class="flex items-center gap-1.5">
              <text class="text-[12px] font-medium text-white/60">用户{{ c.user_id }}</text>
            </view>
            <text class="mt-1 block text-[13px] leading-relaxed text-white/90">{{ c.content }}</text>
          </view>
        </view>
        <view class="mt-2 flex items-center gap-2 pb-2">
          <input
            v-model="draftComment"
            class="min-h-[40px] flex-1 rounded-[10px] bg-white/[0.06] px-3 py-2 text-[13px] text-white"
            placeholder="写条评论..."
            placeholder-class="text-white/35"
          />
          <view class="shrink-0 rounded-[10px] bg-[#7e42f5]/90 px-4 py-2 active:opacity-90" @click="postComment">
            <text class="text-[13px] font-medium text-white">发送</text>
          </view>
        </view>
      </view>

      <!-- Section 5: Related Recommendations -->
      <view class="mt-6 px-4">
        <text class="mb-3 block text-[15px] font-bold text-white">相关推荐</text>
        <scroll-view scroll-x class="whitespace-nowrap pb-6">
          <view class="inline-flex gap-2.5 pr-4">
            <view
              v-for="r in relatedCards"
              :key="r.id"
              class="relative w-[90px] shrink-0 overflow-hidden rounded-[6px] bg-[#121216] transition-transform active:scale-[0.98]"
              @click="openDrama(r.id)"
            >
              <view class="relative aspect-[3/4] w-full">
                <image :src="r.cover" class="h-full w-full object-cover" mode="aspectFill" />
                <!-- Label -->
                <view
                  :class="`absolute left-0 top-0 rounded-br-[6px] px-1.5 py-0.5 ${
                    r.label === '热播' ? 'bg-gradient-to-r from-[#d946ef] to-[#c026d3]' : 'bg-gradient-to-r from-[#8b5cf6] to-[#6366f1]'
                  }`"
                >
                  <text class="text-[9px] font-medium text-white">{{ r.label }}</text>
                </view>
                <!-- Bottom Gradient -->
                <view class="absolute bottom-0 left-0 right-0 h-1/2 bg-gradient-to-t from-black/90 via-black/50 to-transparent"></view>
                <!-- Title & Heat -->
                <view class="absolute bottom-0 left-0 right-0 flex flex-col p-1.5">
                  <text class="truncate text-[11px] font-medium text-white/90">{{ r.title }}</text>
                  <view class="mt-[2px] flex items-center">
                    <text class="text-[8px] text-[#ff9900]">🔥</text>
                    <text class="ml-[2px] text-[9px] font-medium text-[#facc15]">{{ r.hot }}</text>
                  </view>
                </view>
              </view>
            </view>
          </view>
        </scroll-view>
      </view>
    </scroll-view>
  </view>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { appApi } from '@/config'
import { authHeaders, needLogin } from '@/utils/app-http'

const fallbackCover = 'https://images.unsplash.com/photo-1618331835717-801e976710b2?q=80&w=300&auto=format&fit=crop'

const dramaId = ref(0)
const drama = ref<Record<string, any> | null>(null)
const episodes = ref<any[]>([])
const entryNodeId = ref<number | null>(null)
const episodeTotal = ref(80)
const relatedRaw = ref<any[]>([])
const commentList = ref<any[]>([])
const draftComment = ref('')
const favorited = ref(false)
const subscribed = ref(false)
const descExpanded = ref(false)

const displayTitle = computed(() => drama.value?.title || '逆天战神')
const posterSrc = computed(() => drama.value?.cover_url || fallbackCover)
const displayDesc = computed(() => drama.value?.description || '少年林辰，遭家族背叛，血脉被夺，绝境之下觉醒上古战神血脉！从此逆天改命，踏上武道巅峰！')
const displayHeat = computed(() => formatHeatLine(drama.value?.heat))

const typeLabel = computed(() => {
  const t = drama.value?.drama_type
  const map: Record<string, string> = {
    urban: '都市', fantasy: '玄幻', romance: '言情',
    horror: '悬疑', comedy: '喜剧', sci_fi: '科幻',
    costume: '古风',
  }
  return map[t ?? ''] || '短剧'
})

const displayTagPills = computed(() => {
  const raw = drama.value?.tags
  if (!raw) return ['漫剧', '逆袭', '战神', '玄幻']
  const s = String(raw)
  try {
    const j = JSON.parse(s)
    if (Array.isArray(j)) return j.map(String).slice(0, 6)
  } catch {
    /* ignore */
  }
  const parts = s
    .split(/[,，、\s]+/)
    .map((x) => x.trim())
    .filter(Boolean)
    .slice(0, 6)
  return parts.length ? parts : ['漫剧', '逆袭', '战神', '玄幻']
})

interface RelatedCard {
  id: number
  title: string
  cover: string
  hot: string
  label: string
}

const relatedCards = computed<RelatedCard[]>(() =>
  relatedRaw.value.map((x) => ({
    id: x.drama_id,
    title: x.title || '',
    cover: x.cover_url || fallbackCover,
    hot: `${formatHeatNum(x.heat)}热度`,
    label: Number(x.heat) >= 500000 ? '热播' : '推荐',
  })),
)

function goBack() {
  uni.navigateBack()
}

function formatHeatNum(h?: number | null) {
  if (h == null || Number.isNaN(Number(h))) return '—'
  const n = Number(h)
  if (n >= 10000) return `${(n / 10000).toFixed(1)}万`
  return String(n)
}

function formatHeatLine(h?: number | null) {
  if (h == null || Number.isNaN(Number(h))) return '986.5万热度'
  const n = Number(h)
  if (n >= 10000) return `${(n / 10000).toFixed(1)}万热度`
  return `${n}热度`
}

function isEntryEpisode(ep: any): boolean {
  const eid = entryNodeId.value
  if (!eid) return false
  return Number(ep.node_id) === Number(eid)
}

function playNode(nodeId: number) {
  if (!nodeId) return
  uni.navigateTo({ url: `/pages/player/index?nodeId=${nodeId}` })
}

function playEntry() {
  const e = entryNodeId.value
  if (e) {
    playNode(e)
    return
  }
  const first = episodes.value[0]
  if (first?.node_id) playNode(Number(first.node_id))
  else uni.showToast({ title: '暂无可播放集数', icon: 'none' })
}

function openDrama(id: number) {
  uni.redirectTo({ url: `/pages/drama-detail/index?id=${id}` })
}

function loadComments(id: number) {
  uni.request({
    url: appApi('/comments'),
    data: { drama_id: id },
    success: (res: any) => {
      const b = res.data as any
      if (b.code === 200 && Array.isArray(b.rows)) commentList.value = b.rows
    },
  })
}

function postComment() {
  if (!needLogin()) return
  const id = dramaId.value
  const text = draftComment.value.trim()
  if (!id || !text) return
  const nid = entryNodeId.value
  uni.request({
    url: appApi('/comments'),
    method: 'POST',
    header: authHeaders(),
    data:
      nid != null
        ? { drama_id: id, node_id: nid, content: text }
        : { drama_id: id, content: text },
    success: (res: any) => {
      const b = res.data as any
      if (b.code === 200) {
        draftComment.value = ''
        loadComments(id)
        uni.showToast({ title: '评论成功', icon: 'none' })
      } else {
        uni.showToast({ title: b.msg || '失败', icon: 'none' })
      }
    },
  })
}

function loadFavState(id: number) {
  if (!uni.getStorageSync('drama_token')) {
    favorited.value = false
    return
  }
  uni.request({
    url: appApi(`/dramas/${id}/favorite-state`),
    header: authHeaders({}),
    success: (res: any) => {
      const b = res.data as any
      if (b.code === 200 && b.data) favorited.value = !!b.data.favorited
    },
  })
}

function toggleFav() {
  if (!needLogin()) return
  const id = dramaId.value
  if (!id) return
  uni.request({
    url: appApi('/favorite'),
    method: 'POST',
    header: authHeaders(),
    data: { drama_id: id },
    success: (res: any) => {
      const b = res.data as any
      if (b.code === 200) {
        favorited.value = !!b.data?.favorited
        uni.showToast({ title: favorited.value ? '已收藏' : '已取消', icon: 'none' })
      }
    },
  })
}

function loadSubState(id: number) {
  if (!uni.getStorageSync('drama_token')) {
    subscribed.value = false
    return
  }
  uni.request({
    url: appApi(`/subscriptions/${id}/new-episode`),
    header: authHeaders({}),
    success: (res: any) => {
      const b = res.data as any
      if (b.code === 200 && b.data) subscribed.value = !!b.data.subscribed
    },
  })
}

function toggleSub() {
  if (!needLogin()) return
  const id = dramaId.value
  if (!id) return
  uni.request({
    url: appApi('/subscriptions'),
    method: 'POST',
    header: authHeaders(),
    data: { drama_id: id, notify_enabled: true },
    success: (res: any) => {
      const b = res.data as any
      if (b.code === 200) {
        subscribed.value = !!b.data?.subscribed
        uni.showToast({ title: subscribed.value ? '已追更' : '已取消追更', icon: 'none' })
      }
    },
  })
}

function fetchRelated(curId: number) {
  uni.request({
    url: appApi('/dramas'),
    success: (res: any) => {
      const body = res.data as any
      if (body.code !== 200 || !Array.isArray(body.data)) return
      relatedRaw.value = body.data.filter((x: any) => x.drama_id !== curId).slice(0, 8)
    },
  })
}

function loadDetail(id: number) {
  drama.value = null
  episodes.value = []
  entryNodeId.value = null
  relatedRaw.value = []
  uni.request({
    url: appApi(`/dramas/${id}`),
    success: (res: any) => {
      const body = res.data as any
      if (body.code !== 200 || !body.data) {
        uni.showToast({ title: body.msg || '加载剧目失败', icon: 'none' })
        return
      }
      const data = body.data
      drama.value = data.drama || null
      entryNodeId.value = data.entry_node_id != null ? Number(data.entry_node_id) : null
      episodes.value = Array.isArray(data.episodes) ? data.episodes : []
      episodeTotal.value = Number(data.episode_total ?? episodes.value.length) || episodes.value.length || 80
      fetchRelated(id)
      loadComments(id)
      loadFavState(id)
      loadSubState(id)
    },
    fail: () => {
      uni.showToast({ title: '网络错误', icon: 'none' })
    },
  })
}

onLoad((q: any) => {
  const id = Number(q?.id || q?.drama_id || 0)
  dramaId.value = id
  if (!id) {
    uni.showToast({ title: '缺少剧目 id', icon: 'none' })
    return
  }
  loadDetail(id)
})
</script>

<style scoped>
/* Scoped styles */
</style>
