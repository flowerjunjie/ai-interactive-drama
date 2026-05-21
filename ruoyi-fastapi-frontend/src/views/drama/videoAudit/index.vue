<template>
  <div class="app-container">
    <el-alert type="warning" :closable="false" title="待审核视频节点（上传完成或编辑后 review_status=pending）" class="mb2" />
    <el-table v-loading="loading" :data="list" border>
      <el-table-column label="节点ID" prop="nodeId" width="90" />
      <el-table-column label="短剧ID" prop="dramaId" width="90" />
      <el-table-column label="标题" prop="title" min-width="140" />
      <el-table-column label="视频" min-width="220" show-overflow-tooltip prop="videoUrl" />
      <el-table-column label="审核" prop="reviewStatus" width="100" />
      <el-table-column label="操作" width="220" align="center">
        <template #default="{ row }">
          <el-button link type="success" @click="approve(row)" v-hasPermi="['sdrama:node:edit']">通过</el-button>
          <el-button link type="danger" @click="openReject(row)" v-hasPermi="['sdrama:node:edit']">拒绝</el-button>
        </template>
      </el-table-column>
    </el-table>
    <pagination v-show="total > 0" :total="total" v-model:page="query.pageNum" v-model:limit="query.pageSize" @pagination="getList" />

    <el-dialog title="拒绝原因" v-model="rjOpen" width="420px">
      <div v-if="rjRow" class="mb-3 text-sm text-gray-500">
        节点 #{{ rjRow.nodeId }} · {{ rjRow.title || '未命名' }}
      </div>
      <el-input type="textarea" v-model="rjReason" rows="3" placeholder="请输入拒绝原因（可选）" />
      <template #footer>
        <el-button @click="rjOpen = false">取消</el-button>
        <el-button type="danger" @click="reject">确定拒绝</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { approveVideoNode, listPendingVideoNodes, rejectVideoNode } from '@/api/drama'
import { getCurrentInstance, reactive, ref } from 'vue'

const { proxy } = getCurrentInstance()
const loading = ref(false)
const list = ref([])
const total = ref(0)
const query = reactive({ pageNum: 1, pageSize: 10 })
const rjOpen = ref(false)
const rjReason = ref('')
const rjRow = ref(null)

function getList() {
  loading.value = true
  listPendingVideoNodes(query)
    .then(res => {
      list.value = res.rows || []
      total.value = res.total ?? 0
    })
    .finally(() => { loading.value = false })
}

function approve(row) {
  approveVideoNode(row.nodeId).then(() => {
    proxy.$modal.msgSuccess('已通过')
    getList()
  })
}

function openReject(row) {
  rjRow.value = row
  rjReason.value = ''
  rjOpen.value = true
}

function reject() {
  rejectVideoNode(rjRow.value.nodeId, { reject_reason: rjReason.value || null }).then(() => {
    proxy.$modal.msgSuccess('已拒绝')
    rjOpen.value = false
    getList()
  })
}

getList()
</script>

<style scoped>
.mb2 { margin-bottom: 12px; }
</style>
