<template>
  <view class="min-h-screen bg-[#050505]">
    <!-- Simple nav bar -->
    <view class="flex items-center justify-between px-4 pt-[calc(env(safe-area-inset-top)+10px)] pb-3 bg-[#050505] border-b border-white/5">
      <view class="flex h-8 w-8 items-center justify-center active:opacity-70" @click="goBack">
        <view class="i-mdi-chevron-left text-[28px] text-white" />
      </view>
      <text class="text-[15px] font-medium text-white">我的收藏</text>
      <view class="h-8 w-8" />
    </view>
    <scroll-view scroll-y class="pb-[env(safe-area-inset-bottom)]">
      <view v-if="loaded && !rows.length" class="py-24 text-center">
        <text class="text-[14px] text-white/45">暂无收藏记录</text>
      </view>
      <view
        v-for="(row, idx) in rows"
        :key="`${row.drama_id}-${idx}`"
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
          <view class="i-mdi-star text-[20px] text-[#eec787]" />
        </view>
      </view>
    </scroll-view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { onShow } from '@dcloudio/uni-app'
import { appApi } from '@/config'
import { authHeaders, needLogin } from '@/utils/app-http'

const placeholderCover =
  'https://images.unsplash.com/photo-1618331835717-801e976710b2?q=80&w=300&auto=format&fit=crop'

const rows = ref<Record<string, any>[]>([])
const loaded = ref(false)

function dramaTypeLabel(t: string | null | undefined): string {
  const map: Record<string, string> = {
    urban: '都市', fantasy: '玄幻', romance: '言情',
    horror: '悬疑', comedy: '喜剧', sci_fi: '科幻',
    costume: '古风',
  }
  return map[t ?? ''] || '短剧'
}

function fetchList() {
  if (!needLogin()) {
    loaded.value = true
    rows.value = []
    return
  }
  loaded.value = false
  uni.request({
    url: appApi('/favorites'),
    header: authHeaders(),
    success: (res: any) => {
      const b = res.data as any
      loaded.value = true
      if (b.code === 200 && Array.isArray(b.rows)) rows.value = b.rows
      else if (b.code === 200 && Array.isArray(b.data)) rows.value = b.data
      else rows.value = []
    },
    fail: () => {
      loaded.value = true
      rows.value = []
    },
  })
}

function goDrama(row: Record<string, any>) {
  const did = row.drama_id ?? row.dramaId
  if (!did) {
    uni.showToast({ title: '数据异常', icon: 'none' })
    return
  }
  uni.navigateTo({ url: `/pages/drama-detail/index?id=${did}` })
}

function goBack() {
  uni.navigateBack()
}

onShow(() => {
  fetchList()
})
</script>