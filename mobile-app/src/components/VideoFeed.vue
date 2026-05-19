<template>
  <view :class="embedded ? 'space-y-3' : 'mt-2 space-y-5'">
    <view
      v-for="(it, idx) in rows"
      :key="idx"
      class="overflow-hidden rounded-2xl border border-white/[0.06] bg-drama-850/35 shadow-drama ring-1 ring-white/[0.03]"
    >
      <AdCard v-if="it.kind === 'ad' && it.ad" :ad="it.ad" />
      <view v-else-if="it.kind === 'video' && it.node && it.drama" class="p-4 active:bg-white/[0.02]" @click="goPlay(it)">
        <view class="relative overflow-hidden rounded-xl">
          <image
            :src="it.node.cover_url || it.drama.cover_url"
            class="h-52 w-full object-cover"
            mode="aspectFill"
          />
          <view
            class="absolute inset-0 bg-gradient-to-t from-black/75 via-transparent to-black/20"
          />
          <view class="absolute bottom-3 left-3 right-3 flex items-end justify-between">
            <text class="line-clamp-2 flex-1 pr-2 text-[15px] font-semibold leading-snug text-white shadow-sm">{{
              it.drama.title
            }}</text>
            <view
              class="flex h-10 w-10 shrink-0 items-center justify-center rounded-full border border-white/25 bg-white/10 backdrop-blur-sm"
            >
              <text class="text-sm text-drama-accent">▶</text>
            </view>
          </view>
        </view>
        <text class="mt-3 block text-xs font-medium tracking-wide text-drama-muted">{{
          it.node.title || '#' + it.node.node_id
        }}</text>
      </view>
      <DramaCard v-else-if="it.kind === 'drama' && it.drama" :drama="it.drama" />
    </view>
    <view v-if="!rows.length" class="rounded-2xl border border-dashed border-white/[0.1] bg-drama-850/30 py-14 text-center">
      <text class="text-sm text-drama-muted">加载信息流…</text>
    </view>
  </view>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import AdCard from '@/components/AdCard.vue'
import DramaCard from '@/components/DramaCard.vue'
import { appApi } from '@/config'

withDefaults(defineProps<{ embedded?: boolean }>(), { embedded: false })

const rows = ref<any[]>([])

function goPlay(it: any) {
  const nid = it.node?.node_id
  if (nid) uni.navigateTo({ url: `/pages/player/index?nodeId=${nid}` })
}

onMounted(() => {
  uni.request({
    url: appApi('/feed'),
    data: { page_num: 1, page_size: 20 },
    success: (res: any) => {
      const body = res.data as any
      if (body.code === 200 && body.rows) rows.value = body.rows
    },
  })
})
</script>
