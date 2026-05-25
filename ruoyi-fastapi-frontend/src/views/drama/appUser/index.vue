<template>
  <div class="app-container">
    <el-table v-loading="loading" :data="list" border>
      <el-table-column label="用户ID" prop="userId" width="90" />
      <el-table-column label="账号" prop="userName" />
      <el-table-column label="昵称" prop="nickName" />
      <el-table-column label="状态" prop="status" width="80" />
      <el-table-column label="操作" width="140" align="center">
        <template #default="{ row }">
          <el-button link type="primary" @click="openDetail(row)" v-hasPermi="['sdrama:appuser:list']">明细</el-button>
        </template>
      </el-table-column>
    </el-table>
    <pagination v-show="total > 0" :total="total" v-model:page="query.pageNum" v-model:limit="query.pageSize" @pagination="getList" />

    <el-drawer v-model="drawer" title="用户行为" size="40%">
      <el-tabs>
        <el-tab-pane label="观看历史">
          <el-table :data="watchRows" size="small">
            <el-table-column label="短剧">
              <template #default="{ row }">{{ row.dramaTitle || row.drama_title }}</template>
            </el-table-column>
            <el-table-column label="节点" width="80">
              <template #default="{ row }">{{ row.nodeId ?? row.node_id }}</template>
            </el-table-column>
            <el-table-column label="进度秒" width="90">
              <template #default="{ row }">{{ row.progressSec ?? row.progress_sec }}</template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
        <el-tab-pane label="收藏">
          <el-table :data="favRows" size="small">
            <el-table-column label="标题">
              <template #default="{ row }">{{ row.title }}</template>
            </el-table-column>
            <el-table-column label="短剧ID" width="90">
              <template #default="{ row }">{{ row.dramaId ?? row.drama_id }}</template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
      </el-tabs>
    </el-drawer>
  </div>
</template>

<script setup>
import { appUserFavorites, appUserWatchHistory, listAppUsers } from '@/api/drama'
import { reactive, ref } from 'vue'

const loading = ref(false)
const list = ref([])
const total = ref(0)
const query = reactive({ pageNum: 1, pageSize: 10 })
const drawer = ref(false)
const watchRows = ref([])
const favRows = ref([])

function getList() {
  loading.value = true
  listAppUsers(query).then(res => {
    list.value = res.rows || []
    total.value = res.total ?? 0
  }).finally(() => { loading.value = false })
}

function openDetail(row) {
  curUserId.value = row.userId
  drawer.value = true
  appUserWatchHistory(row.userId).then(res => {
    watchRows.value = res.rows || res.data || []
  })
  appUserFavorites(row.userId).then(res => {
    favRows.value = res.rows || res.data || []
  })
}

getList()
</script>
