<template>
  <uni-popup ref="popupRef" type="center" :mask-click="false" background-color="rgba(0,0,0,0.72)">
    <view class="choice-panel">
      <text class="panel-title">请选择剧情走向</text>
      <view class="choice-btns">
        <button
          v-for="c in choices"
          :key="c.choice_id"
          class="choice-btn"
          @click="pick(c)"
        >
          <text v-if="c.choice_code || c.choiceCode" class="code">{{ c.choice_code || c.choiceCode }}</text>
          {{ c.choice_text || c.label }}
        </button>
      </view>
    </view>
  </uni-popup>
</template>

<script setup lang="ts">
import { ref } from 'vue'

defineProps<{
  choices: Array<Record<string, any>>
}>()

const emit = defineEmits<{
  (e: 'pick', nextNodeId: number): void
}>()

const popupRef = ref<any>(null)

function open() {
  popupRef.value?.open?.()
}

function close() {
  popupRef.value?.close?.()
}

function pick(c: Record<string, any>) {
  const next = c.next_node_id ?? c.nextNodeId
  if (next) emit('pick', Number(next))
}

defineExpose({ open, close })
</script>

<style scoped>
.choice-panel {
  width: 82vw;
  max-width: 420px;
  padding: 24rpx;
  border-radius: 24rpx;
  background: linear-gradient(155deg, rgba(26, 22, 14, 0.96) 0%, rgba(10, 11, 18, 0.98) 100%);
  border: 1px solid rgba(212, 168, 83, 0.35);
  box-shadow:
    0 24px 48px rgba(0, 0, 0, 0.65),
    0 0 36px rgba(212, 168, 83, 0.12);
}
.panel-title {
  display: block;
  font-size: 32rpx;
  font-weight: 600;
  color: #f5ede0;
  margin-bottom: 8rpx;
  letter-spacing: 0.02em;
}
.choice-btns {
  margin-top: 16rpx;
  display: flex;
  flex-direction: column;
  gap: 16rpx;
}
.choice-btn {
  border-radius: 20rpx;
  padding: 22rpx 28rpx;
  background: linear-gradient(90deg, #c9a54a, #d4a853);
  color: #1a1206;
  font-size: 28rpx;
  font-weight: 600;
}
.code {
  margin-right: 12rpx;
  font-weight: 800;
  opacity: 0.85;
}
</style>
