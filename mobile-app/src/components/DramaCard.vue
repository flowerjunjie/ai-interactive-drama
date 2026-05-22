<template>
  <view class="group mb-5 px-0.5 active:opacity-95" @click="go">
    <view
      class="overflow-hidden rounded-2xl border border-white/[0.07] bg-drama-850/40 shadow-drama ring-1 ring-white/[0.04]"
    >
      <view class="relative">
        <image
          v-if="drama.cover_url"
          :src="drama.cover_url"
          class="h-44 w-full object-cover"
          mode="aspectFill"
        />
        <view
          v-else
          class="flex h-44 w-full items-center justify-center bg-gradient-to-br from-drama-800 to-drama-950"
        >
          <text class="text-3xl text-drama-accent/40">▶</text>
        </view>
        <view
          class="absolute bottom-3 left-3 rounded-full border border-white/15 bg-black/45 px-3 py-1 backdrop-blur-md"
        >
          <text class="text-[10px] font-semibold uppercase tracking-wider text-drama-accent">{{
            typeLabel(drama.drama_type)
          }}</text>
        </view>
      </view>
      <view class="px-4 pb-4 pt-3">
        <text class="line-clamp-2 text-[17px] font-semibold leading-snug text-white">{{ drama.title }}</text>
        <view class="mt-2 flex items-center gap-2">
          <view class="h-px flex-1 bg-gradient-to-r from-drama-accent/50 to-transparent" />
          <text class="text-[11px] font-medium tracking-wide text-drama-muted">立即观看</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
const props = defineProps<{ drama: Record<string, any> }>()

function typeLabel(t: string | null | undefined): string {
  const map: Record<string, string> = {
    urban: '都市', fantasy: '玄幻', romance: '言情',
    horror: '悬疑', comedy: '喜剧', sci_fi: '科幻',
    costume: '古风',
  }
  return map[t ?? ''] || '短剧'
}

function go() {
  uni.navigateTo({ url: `/pages/drama-detail/index?id=${props.drama.drama_id}` })
}
</script>
