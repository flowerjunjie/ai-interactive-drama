<template>
  <div class="app-container">
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card shadow="hover"><div class="stat-title">短剧数</div><div class="stat-num">{{ stats.drama_count }}</div></el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover"><div class="stat-title">视频节点</div><div class="stat-num">{{ stats.video_node_count }}</div></el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover"><div class="stat-title">用户评价待审</div><div class="stat-num">{{ stats.pending_review_count }}</div></el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover"><div class="stat-title">视频待审</div><div class="stat-num">{{ stats.pending_video_node_count }}</div></el-card>
      </el-col>
    </el-row>
    <el-row :gutter="20" class="mt">
      <el-col :span="6">
        <el-card shadow="hover"><div class="stat-title">今日播放量(进度上报)</div><div class="stat-num">{{ stats.today_watch_events }}</div></el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover"><div class="stat-title">今日新增用户</div><div class="stat-num">{{ stats.today_new_users }}</div></el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover"><div class="stat-title">广告曝光(累计)</div><div class="stat-num">{{ stats.ad_impressions_total }}</div></el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover"><div class="stat-title">广告点击(累计)</div><div class="stat-num">{{ stats.ad_clicks_total }}</div></el-card>
      </el-col>
    </el-row>
    <el-row :gutter="20" class="mt">
      <el-col :span="6">
        <el-card shadow="hover"><div class="stat-title">C端用户</div><div class="stat-num">{{ stats.app_user_count }}</div></el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { dramaDashboard } from '@/api/drama'
import { onMounted, ref } from 'vue'

const stats = ref({
  drama_count: 0,
  video_node_count: 0,
  pending_review_count: 0,
  pending_video_node_count: 0,
  today_watch_events: 0,
  today_new_users: 0,
  ad_impressions_total: 0,
  ad_clicks_total: 0,
  app_user_count: 0
})

function load() {
  dramaDashboard().then(res => {
    if (res.data) Object.assign(stats.value, res.data)
  })
}

onMounted(load)
</script>

<style scoped>
.stat-title { color: #909399; font-size: 14px; }
.stat-num { font-size: 28px; font-weight: 600; margin-top: 8px; }
.mt { margin-top: 16px; }
</style>
