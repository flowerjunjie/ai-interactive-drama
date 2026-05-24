<template>
  <view class="flex h-screen w-screen flex-col overflow-hidden bg-[#050505]">
    <!-- Top Video Area -->
    <view class="relative h-[62vh] w-full shrink-0 bg-black">
      <video
        v-if="videoSrc"
        id="dramaVideo"
        class="h-full w-full"
        :src="videoSrc"
        :controls="false"
        object-fit="cover"
        playsinline
        webkit-playsinline
        enable-progress-gesture
        @timeupdate="onTimeUpdate"
        @ended="onEnded"
        @loadedmetadata="onLoadedMeta"
      />
      <image
        v-else
        src="https://images.unsplash.com/photo-1618331835717-801e976710b2?q=80&w=600&auto=format&fit=crop"
        class="h-full w-full object-cover"
        mode="aspectFill"
      />

      <view
        class="absolute bottom-0 left-0 right-0 h-40 bg-gradient-to-t from-[#050505] via-[#050505]/60 to-transparent pointer-events-none"
      ></view>

      <!-- Back Button (top-left, minimal) -->
      <view class="absolute left-2 top-[calc(env(safe-area-inset-top)+10px)] z-50 flex items-center justify-center rounded-full bg-black/40 backdrop-blur-md active:bg-black/60" @click="goBack">
        <view class="i-mdi-chevron-left text-[28px] text-white" />
      </view>

      <view v-if="showBranchTip" class="absolute left-4 top-1/2 z-50 -translate-y-1/2">
        <view class="relative rounded-[8px] border border-white/10 bg-black/75 px-3 py-2.5 shadow-lg backdrop-blur-md">
          <text class="text-[13px] font-medium leading-[1.6] text-white/90">{{ branchTipText }}</text>
          <view
            class="absolute -right-[5px] top-1/2 h-[10px] w-[10px] -translate-y-1/2 rotate-45 bg-black/75 border-t border-r border-white/10"
          ></view>
        </view>
      </view>

      <!-- Right Interaction Bar -->
      <view class="absolute bottom-[40px] right-2 z-50 flex flex-col items-center gap-4">
        <view class="relative flex flex-col items-center">
          <view class="h-10 w-10 overflow-hidden rounded-full border-[1.5px] border-white shadow-sm">
            <image src="https://api.dicebear.com/7.x/avataaars/svg?seed=Felix" class="h-full w-full object-cover" />
          </view>
          <view class="absolute -bottom-2.5 flex items-center justify-center rounded-full bg-[#ff2442] px-[5px] py-[2px] shadow-sm">
            <text class="text-[9px] font-bold text-white">+ 关注</text>
          </view>
        </view>
        <view class="mt-2 flex flex-col items-center gap-0.5" @click="toggleNodeLike">
          <view :class="userLiked ? 'i-mdi-heart text-[32px] text-[#ff2442] drop-shadow-md' : 'i-mdi-heart text-[32px] text-white drop-shadow-md'" />
          <text class="text-[10px] font-medium text-white drop-shadow-md">{{ formatShortCount(likeTotal) }}</text>
        </view>
        <view class="flex flex-col items-center gap-0.5" @click="toggleDramaFavorite">
          <view class="i-mdi-star text-[34px] text-white drop-shadow-md" />
          <text class="text-[10px] font-medium text-white drop-shadow-md">{{ formatShortCount(favHint) }}</text>
        </view>
        <view class="flex flex-col items-center gap-0.5">
          <view class="i-mdi-comment-processing text-[30px] text-white drop-shadow-md" />
          <text class="text-[10px] font-medium text-white drop-shadow-md">{{ formatShortCount(commentRows.length) }}</text>
        </view>
        <view class="flex flex-col items-center gap-0.5" @click="onShare">
          <view class="i-mdi-share text-[34px] text-white drop-shadow-md" />
          <text class="text-[10px] font-medium text-white drop-shadow-md">分享</text>
        </view>
      </view>

      <view class="absolute bottom-2 left-0 right-0 z-50 px-3">
        <view class="flex items-center gap-2.5">
          <view class="i-mdi-play text-[24px] text-white drop-shadow-sm" />
          <text class="text-[10px] text-white/90 tracking-wide">{{ progressLabel }}</text>
          <view class="relative h-[3px] flex-1 rounded-full bg-white/20">
            <view
              class="absolute left-0 top-0 h-full rounded-full bg-[#9a5cf6] shadow-[0_0_8px_rgba(154,92,246,0.6)]"
              :style="{ width: progressPct + '%' }"
            ></view>
            <view
              class="absolute top-1/2 h-[10px] w-[10px] -translate-x-1/2 -translate-y-1/2 rounded-full bg-white shadow-md"
              :style="{ left: progressPct + '%' }"
            ></view>
          </view>
          <view class="i-mdi-fullscreen text-[20px] text-white drop-shadow-sm" @click="toggleFullscreen" />
        </view>
      </view>
    </view>

    <scroll-view scroll-y class="flex-1 bg-[#050505] pb-[70px]">
      <view class="px-4 pt-3">
        <view class="flex flex-wrap items-center justify-between gap-2">
          <view class="flex min-w-0 flex-1 flex-wrap items-center gap-2">
            <text class="text-[18px] font-bold tracking-wide text-white">{{ dramaTitle }}</text>
            <view v-for="t in tagPills" :key="t" class="rounded bg-white/[0.08] px-1.5 py-0.5">
              <text class="text-[10px] text-white/80">{{ t }}</text>
            </view>
            <view class="ml-1 flex items-center">
              <text class="text-[10px] text-[#ff9900]">🔥</text>
              <text class="ml-[2px] text-[11px] font-medium text-[#facc15]">{{ heatLine }} ></text>
            </view>
          </view>
          <view
            class="ml-2 flex shrink-0 items-center justify-center rounded-full px-3.5 py-1.5 active:opacity-80 relative"
            style="background: linear-gradient(90deg, #8b5cf6, #f97316)"
            @click="toggleSub"
          >
            <view v-if="subscribed && hasNewEpisode" class="absolute -top-[3px] -right-[3px] h-2.5 w-2.5 rounded-full bg-[#ff2442] shadow-[0_0_6px_rgba(255,36,66,0.8)] animate-ping" />
            <view v-if="subscribed && hasNewEpisode" class="absolute -top-[3px] -right-[3px] h-2.5 w-2.5 rounded-full bg-[#ff2442]" />
            <text class="text-[12px] font-medium text-white">{{ subscribed ? '已追更' : '追更' }}</text>
          </view>
        </view>

        <view class="mt-2.5">
          <text class="text-[12px] leading-relaxed text-white/60" :class="{ 'line-clamp-2': !descExpanded, 'line-clamp-none': descExpanded }">{{ dramaDesc }}</text>
          <text class="float-right ml-1 mt-[2px] text-[11px] text-white/40 active:opacity-70" @click="descExpanded = !descExpanded">{{ descExpanded ? '收起' : '展开' }} ∨</text>
        </view>

        <view class="mt-6">
          <view class="mb-3 flex items-center justify-between">
            <text class="text-[15px] font-bold text-white">选集</text>
            <text class="text-[12px] text-white/50">共{{ episodeTotal }}集 ></text>
          </view>
          <scroll-view scroll-x class="whitespace-nowrap pb-1">
            <view class="inline-flex gap-2.5 pr-2">
              <view
                v-for="ep in episodePanel"
                :key="ep.node_id"
                class="flex h-[54px] w-[54px] shrink-0 flex-col items-center justify-center rounded-[8px] active:bg-white/10"
                :class="Number(ep.node_id) === nodeId ? 'border border-[#9a5cf6] bg-[#9a5cf6]/10' : 'bg-white/[0.05]'"
                @click="switchEpisode(ep.node_id)"
              >
                <template v-if="Number(ep.node_id) === nodeId">
                  <text class="text-[14px] font-medium text-[#9a5cf6]">{{ ep.episode_no ?? ep.node_id }}</text>
                  <view class="mt-[2px] flex items-center gap-[2px]">
                    <view class="flex h-[8px] items-end gap-[1.5px]">
                      <view class="h-[5px] w-[2px] rounded-full bg-[#9a5cf6] animate-pulse"></view>
                      <view class="h-[8px] w-[2px] rounded-full bg-[#9a5cf6] animate-pulse delay-75"></view>
                      <view class="h-[4px] w-[2px] rounded-full bg-[#9a5cf6] animate-pulse delay-150"></view>
                    </view>
                    <text class="text-[9px] text-[#9a5cf6]">播放中</text>
                  </view>
                </template>
                <template v-else>
                  <text class="text-[14px] font-medium text-white/90">{{ ep.episode_no ?? ep.node_id }}</text>
                </template>
              </view>
              <view
                v-if="episodePanel.length > 6"
                class="flex h-[54px] w-[54px] shrink-0 items-center justify-center rounded-[8px] bg-white/[0.04] active:bg-white/10"
              >
                <view class="i-mdi-dots-horizontal text-[20px] text-white/40" />
              </view>
            </view>
          </scroll-view>
        </view>

        <view class="mt-6 border-t border-white/5 pb-6 pt-5">
          <view class="mb-4 flex items-center justify-between">
            <text class="text-[15px] font-bold text-white">精彩评论</text>
            <text class="text-[12px] text-white/50">全部评论 ></text>
          </view>
          <view v-for="c in commentRows.slice(0, 5)" :key="c.comment_id" class="mb-5 flex gap-3">
            <image src="https://api.dicebear.com/7.x/avataaars/svg?seed=Felix" class="mt-0.5 h-8 w-8 shrink-0 rounded-full bg-gray-800" />
            <view class="flex-1">
              <view class="flex items-center gap-1.5">
                <text class="text-[12px] font-medium text-white/60">用户{{ c.user_id }}</text>
                <view class="rounded bg-white/10 px-1 py-[1px]">
                  <text class="text-[8px] font-bold text-white/80">LV5</text>
                </view>
              </view>
              <text class="mt-1 block text-[13px] leading-relaxed text-white/90">{{ c.content }}</text>
              <view class="mt-2 flex items-center justify-between">
                <text class="text-[11px] text-white/40">{{ formatCommentTime(c.create_time) }}</text>
              </view>
            </view>
          </view>
        </view>
      </view>
    </scroll-view>

    <view
      class="fixed bottom-0 left-0 right-0 z-50 flex items-center gap-3 border-t border-white/5 bg-[#111115] px-4 py-2 pb-[calc(8px+env(safe-area-inset-bottom))]"
    >
      <view class="flex h-[36px] flex-1 items-center rounded-full bg-white/[0.06] px-4">
        <input v-model="draftComment" class="flex-1 text-[13px] text-white" placeholder="说点什么..." placeholder-class="text-white/40" />
      </view>
      <view class="flex h-[36px] items-center justify-center rounded-full bg-white/10 px-4 active:bg-white/20" @click="postComment">
        <text class="text-[13px] font-medium text-white/80">发送</text>
      </view>
    </view>

    <ChoicePopup ref="choicePopupRef" :choices="choices" @pick="onPick" />
  </view>
</template>

<script setup lang="ts">
import { onLoad, onUnload } from '@dcloudio/uni-app'
import { computed, ref } from 'vue'
import ChoicePopup from '@/components/ChoicePopup.vue'
import { appApi } from '@/config'
import { authHeaders, legacyApi, needLogin } from '@/utils/app-http'
import { formatShortCount } from '@/utils/format'

const nodeId = ref(0)
const node = ref<any>(null)
const choices = ref<any[]>([])
const choicePopupRef = ref<any>(null)
const branchTriggered = ref(false)
const likeTotal = ref(0)
const userLiked = ref(false)
const subscribed = ref(false)
const hasNewEpisode = ref(false)
const dramaMeta = ref<any>(null)
const episodePanel = ref<any[]>([])
const episodeTotal = ref(0)
const commentRows = ref<any[]>([])
const draftComment = ref('')
const currentSec = ref(0)
const durationSec = ref(1)
const lastReportAt = ref(0)
const showBranchTip = ref(false)
const descExpanded = ref(false)
const savedProgressSec = ref(0)

const videoSrc = computed(() => node.value?.video_url || node.value?.videoUrl || '')

const dramaId = computed(() => Number(node.value?.drama_id ?? 0))

const dramaTitle = computed(() => dramaMeta.value?.title || '短剧')
const dramaDesc = computed(() => dramaMeta.value?.description || '暂无剧情简介')
const heatLine = computed(() => {
  const h = dramaMeta.value?.heat
  if (h == null) return '0热度'
  const n = Number(h)
  return n >= 10000 ? `${(n / 10000).toFixed(1)}万热度` : `${n}热度`
})
const favHint = computed(() => Number(dramaMeta.value?.heat ?? 124000))

const tagPills = computed(() => {
  const raw = dramaMeta.value?.tags
  if (!raw) return ['热门']
  const s = String(raw)
  try {
    const j = JSON.parse(s)
    if (Array.isArray(j)) return j.map(String).slice(0, 3)
  } catch {
    /* ignore */
  }
  return s
    .split(/[,，、\s]+/)
    .map((x) => x.trim())
    .filter(Boolean)
    .slice(0, 3)
})

const barTitle = computed(() => {
  const ep = node.value?.episode_no ?? node.value?.episodeNo
  const t = dramaTitle.value
  if (ep != null) return `${t} · 第${ep}集`
  return `${t} · 正片`
})

const progressPct = computed(() => {
  const d = durationSec.value || 1
  const c = Math.min(Math.max(currentSec.value, 0), d)
  return Math.min(100, Math.round((c / d) * 1000) / 10)
})

const progressLabel = computed(() => {
  const a = formatClock(currentSec.value)
  const b = formatClock(durationSec.value)
  return `${a} / ${b}`
})

const branchTipText = computed(() => {
  const t = triggerSec(node.value)
  return t != null ? `${t}秒后将进行剧情选择\n请做好选择...` : '即将进行剧情选择\n请做好选择...'
})

function formatClock(sec: number) {
  const s = Math.floor(sec || 0)
  const m = Math.floor(s / 60)
  const r = s % 60
  const mm = m < 10 ? `0${m}` : `${m}`
  const rr = r < 10 ? `0${r}` : `${r}`
  return `${mm}:${rr}`
}

function formatCommentTime(t: any) {
  if (!t) return ''
  const d = new Date(t)
  return isNaN(d.getTime()) ? '' : d.toLocaleString()
}

function interactiveFlag(n: any) {
  return n?.is_interactive === '1' || n?.isInteractive === '1'
}

function triggerSec(n: any) {
  const v = n?.choice_trigger_sec ?? n?.choiceTriggerSec
  return v != null ? Number(v) : null
}

function goBack() {
  reportWatch(true)
  uni.navigateBack()
}

function toggleFullscreen() {
  const v = document.querySelector('video')
  if (!v) return
  if (!document.fullscreenElement) {
    v.requestFullscreen?.() || v.webkitRequestFullscreen?.()
  } else {
    document.exitFullscreen?.() || document.webkitExitFullscreen?.()
  }
}

function onShare() {
  const did = dramaId.value
  if (!did) return
  uni.share({
    provider: 'weixin',
    scene: 'WXSceneSession',
    title: dramaTitle.value,
    summary: dramaDesc.value.slice(0, 60),
    success: () => uni.showToast({ title: '分享成功', icon: 'none' }),
    fail: () => {
      // WeChat not configured — silently fall through to system share
      uni.share({
        provider: '',
        type: 0,
        title: dramaTitle.value,
        success: () => {},
        fail: () => {
          /* system share unavailable — no toast spam */
        },
      })
    },
  })
}

function feedbackReview() {
  uni.showModal({
    title: '剧集反馈',
    editable: true,
    placeholderText: '描述问题或建议',
    success: (res) => {
      if (!res.confirm) return
      if (!uni.getStorageSync('drama_token')) {
        uni.showToast({ title: '请先登录', icon: 'none' })
        return
      }
      const content = (res as any).content as string
      if (!content?.trim()) return
      uni.request({
        url: legacyApi('/video-reviews'),
        method: 'POST',
        header: authHeaders(),
        data: {
          drama_id: dramaId.value,
          node_id: nodeId.value,
          rating: 5,
          content: content.trim(),
        },
        success: (r: any) => {
          const b = r.data as any
          uni.showToast({ title: b?.msg || '已提交', icon: 'none' })
        },
      })
    },
  })
}

function switchEpisode(nid: number) {
  if (!nid || nid === nodeId.value) return
  reportWatch(true)
  uni.redirectTo({ url: `/pages/player/index?nodeId=${nid}` })
}

function loadComments() {
  const id = dramaId.value
  if (!id) return
  uni.request({
    url: appApi('/comments'),
    data: { drama_id: id },
    success: (res: any) => {
      const body = res.data as any
      if (body.code === 200 && Array.isArray(body.rows)) commentRows.value = body.rows
    },
  })
}

function postComment() {
  if (!needLogin()) return
  const id = dramaId.value
  const text = draftComment.value.trim()
  if (!id || !text) return
  uni.request({
    url: appApi('/comments'),
    method: 'POST',
    header: authHeaders(),
    data: { drama_id: id, node_id: nodeId.value, content: text },
    success: (res: any) => {
      const b = res.data as any
      if (b.code === 200) {
        draftComment.value = ''
        loadComments()
        uni.showToast({ title: '评论成功', icon: 'none' })
      } else {
        uni.showToast({ title: b.msg || '失败', icon: 'none' })
      }
    },
  })
}

function toggleNodeLike() {
  if (!needLogin()) return
  const nid = nodeId.value
  if (!nid) return
  uni.request({
    url: appApi('/like'),
    method: 'POST',
    header: authHeaders(),
    data: { target_type: 'node', target_id: nid },
    success: (res: any) => {
      const b = res.data as any
      if (b.code === 200) {
        userLiked.value = !!b.data?.liked
        loadNodeBundle()
      }
    },
  })
}

function toggleDramaFavorite() {
  if (!needLogin()) return
  const id = dramaId.value
  if (!id) return
  uni.request({
    url: appApi('/favorites'),
    method: 'POST',
    header: authHeaders(),
    data: { drama_id: id },
    success: (res: any) => {
      const b = res.data as any
      if (b.code === 200) uni.showToast({ title: b.data?.favorited ? '已追更收藏' : '已取消收藏', icon: 'none' })
    },
  })
}

function loadMeLike() {
  const nid = nodeId.value
  if (!nid) return
  uni.request({
    url: appApi(`/video-nodes/${nid}/me-like`),
    header: authHeaders({}),
    success: (res: any) => {
      const b = res.data as any
      if (b.code === 200) userLiked.value = !!b.data?.liked
    },
  })
}

function loadSubState() {
  const id = dramaId.value
  if (!id) return
  uni.request({
    url: appApi(`/subscriptions/${id}/new-episode`),
    header: authHeaders({}),
    success: (res: any) => {
      const b = res.data as any
      if (b.code === 200 && b.data) {
        subscribed.value = !!b.data.subscribed
        hasNewEpisode.value = !!b.data.has_new
      }
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

function loadDramaMeta() {
  const id = dramaId.value
  if (!id) return
  uni.request({
    url: appApi(`/dramas/${id}`),
    success: (res: any) => {
      const body = res.data as any
      if (body.code !== 200 || !body.data) return
      dramaMeta.value = body.data.drama
      episodePanel.value = Array.isArray(body.data.episodes) ? body.data.episodes : []
      episodeTotal.value = Number(body.data.episode_total ?? episodePanel.value.length) || episodePanel.value.length
    },
  })
}

function loadNodeBundle() {
  if (!nodeId.value) return
  if (uni.getStorageSync('drama_token')) {
    uni.request({
      url: appApi('/watch-history'),
      header: authHeaders({}),
      success: (res: any) => {
        const b = res.data as any
        if (b.code === 200 && Array.isArray(b.rows)) {
          const entry = b.rows.find(
            (r: any) => Number(r.node_id || r.nodeId) === nodeId.value,
          )
          if (entry) savedProgressSec.value = Number(entry.progress_sec || 0)
        }
      },
    })
  }
  uni.request({
    url: appApi(`/video-nodes/${nodeId.value}`),
    success: (res: any) => {
      const body = res.data as any
      if (body.code === 200 && body.data) {
        node.value = body.data.node
        choices.value = body.data.choices || []
        if (body.data.like_count != null) likeTotal.value = Number(body.data.like_count)
      }
      loadDramaMeta()
      loadComments()
      loadMeLike()
      loadSubState()
    },
  })
}

function reportWatch(force = false) {
  if (!uni.getStorageSync('drama_token')) return
  const id = dramaId.value
  if (!id || !nodeId.value) return
  const now = Date.now()
  if (!force && now - lastReportAt.value < 8000) return
  lastReportAt.value = now
  uni.request({
    url: appApi('/watch-history'),
    method: 'POST',
    header: authHeaders(),
    data: {
      drama_id: id,
      node_id: nodeId.value,
      progress_sec: Math.floor(currentSec.value),
    },
    fail: () => {},
  })
}

function onLoadedMeta(e: any) {
  const d = Number(e?.detail?.duration ?? 0)
  if (d > 0) durationSec.value = d
  if (savedProgressSec.value > 0) {
    try {
      const ctx = uni.createVideoContext('dramaVideo')
      ctx.seekTo(savedProgressSec.value)
    } catch (err) {
      console.warn('[player] seekTo failed, progress restored silently:', savedProgressSec.value, err)
    }
  }
}

function onTimeUpdate(e: any) {
  const n = node.value
  const cur = Number(e?.detail?.currentTime ?? 0)
  currentSec.value = cur
  if (n && interactiveFlag(n) && choices.value.length && !branchTriggered.value) {
    const trig = triggerSec(n)
    showBranchTip.value = trig != null && cur < trig && cur > Math.max(0, trig - 5)
    if (trig != null && !Number.isNaN(trig) && cur >= trig) {
      branchTriggered.value = true
      pauseVideo()
      choicePopupRef.value?.open()
    }
  }
  reportWatch(false)
}

function pauseVideo() {
  try {
    const ctx = uni.createVideoContext('dramaVideo')
    ctx.pause()
  } catch {
    /* ignore */
  }
}

function onEnded() {
  const n = node.value
  if (!n || !choices.value.length || branchTriggered.value) return
  if (!interactiveFlag(n)) return
  branchTriggered.value = true
  pauseVideo()
  choicePopupRef.value?.open()
}

function onPick(nextId: number) {
  const ch = choices.value.find((c) => Number(c.next_node_id ?? c.nextNodeId) === nextId)
  choicePopupRef.value?.close()
  const token = uni.getStorageSync('drama_token')
  if (token && dramaId.value && ch?.choice_id != null) {
    uni.request({
      url: appApi('/choice-logs'),
      method: 'POST',
      header: authHeaders(),
      data: {
        drama_id: dramaId.value,
        from_node_id: nodeId.value,
        choice_id: ch.choice_id,
        to_node_id: nextId,
      },
      complete: () => {
        reportWatch(true)
        uni.redirectTo({ url: `/pages/player/index?nodeId=${nextId}` })
      },
    })
  } else {
    reportWatch(true)
    uni.redirectTo({ url: `/pages/player/index?nodeId=${nextId}` })
  }
}

onLoad((q: any) => {
  nodeId.value = Number(q?.nodeId || q?.id || 0)
  branchTriggered.value = false
  showBranchTip.value = false
  loadNodeBundle()
})

onUnload(() => {
  reportWatch(true)
})
</script>

<style scoped>
::-webkit-scrollbar {
  display: none;
}
</style>
