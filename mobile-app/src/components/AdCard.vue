<template>
  <view class="border-b border-white/[0.05] p-4">
    <view class="mb-3 flex items-start justify-between gap-2">
      <text class="text-[15px] font-semibold leading-snug text-white">{{ ad.title }}</text>
      <text class="shrink-0 rounded-md bg-drama-accent-soft px-2 py-0.5 text-[10px] font-semibold uppercase tracking-wider text-drama-accent">推广</text>
    </view>
    <video
      v-if="(ad.media_type || ad.mediaType) === 'video' && mediaSrc"
      :src="mediaSrc"
      class="mt-1 h-40 w-full overflow-hidden rounded-xl bg-black/40"
      controls
    />
    <image
      v-else-if="mediaSrc"
      :src="mediaSrc"
      class="mt-1 h-36 w-full rounded-xl ring-1 ring-white/[0.06]"
      mode="aspectFill"
      @click="open"
    />
  </view>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { appApi } from '@/config'

const props = defineProps<{ ad: Record<string, any> }>()

const mediaSrc = computed(
  () => props.ad.media_url || props.ad.mediaUrl || props.ad.image_url || props.ad.imageUrl || '',
)

onMounted(() => {
  const id = props.ad?.ad_id ?? props.ad?.adId
  if (id)
    uni.request({ url: appApi(`/ads/${id}/impression`), method: 'POST' })
})

function open() {
  const id = props.ad?.ad_id ?? props.ad?.adId
  if (id) uni.request({ url: appApi(`/ads/${id}/click`), method: 'POST' })
  const link = props.ad.link_url || props.ad.linkUrl
  if (link) {
    // #ifdef H5
    window.open(link)
    // #endif
  }
}
</script>
