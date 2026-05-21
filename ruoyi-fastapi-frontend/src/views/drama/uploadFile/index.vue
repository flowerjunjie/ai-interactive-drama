<template>
  <div class="app-container">
    <el-form :inline="true" class="mt">
      <el-form-item label="短剧ID"><el-input-number v-model="query.dramaId" :min="1" /></el-form-item>
      <el-form-item>
        <el-button type="primary" @click="getList">搜索</el-button>
      </el-form-item>
    </el-form>
    <el-table v-loading="loading" :data="list" border>
      <el-table-column label="fileId" prop="fileId" width="90" />
      <el-table-column label="bucket" prop="bucket" width="140" />
      <el-table-column label="objectKey" prop="objectKey" min-width="240" show-overflow-tooltip />
      <el-table-column label="状态" prop="status" width="100" />
      <el-table-column label="短剧" prop="dramaId" width="90" />
      <el-table-column label="节点" prop="nodeId" width="90" />
      <el-table-column label="创建" prop="createTime" width="170" />
    </el-table>
    <pagination v-show="total > 0" :total="total" v-model:page="query.pageNum" v-model:limit="query.pageSize" @pagination="getList" />
  </div>
</template>

<script setup>
import { listUploadFiles } from '@/api/drama'
import { getCurrentInstance, reactive, ref } from 'vue'

const { proxy } = getCurrentInstance()
const loading = ref(false)
const list = ref([])
const total = ref(0)
const query = reactive({ pageNum: 1, pageSize: 10, dramaId: undefined })

function getList() {
  loading.value = true
  listUploadFiles(query)
    .then(res => {
      list.value = res.rows || []
      total.value = res.total ?? 0
    })
    .finally(() => { loading.value = false })
}

getList()
</script>
