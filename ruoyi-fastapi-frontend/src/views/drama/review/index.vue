<template>
  <div class="app-container">
    <el-alert type="info" :closable="false" title="用户评价（影评）审核，与「视频审核」中的节点上架审核不同。" class="mb2" />
    <el-table v-loading="loading" :data="list" border>
      <el-table-column label="ID" prop="reviewId" width="80" />
      <el-table-column label="用户" prop="appUserId" width="90" />
      <el-table-column label="短剧" prop="dramaId" width="90" />
      <el-table-column label="评分" prop="rating" width="70" />
      <el-table-column label="内容" prop="content" min-width="200" show-overflow-tooltip />
      <el-table-column label="操作" width="220" align="center">
        <template #default="scope">
          <el-button link type="success" @click="audit(scope.row, 'approved')"
            v-hasPermi="['sdrama:review:audit']">通过</el-button>
          <el-button link type="danger" @click="audit(scope.row, 'rejected')"
            v-hasPermi="['sdrama:review:audit']">拒绝</el-button>
        </template>
      </el-table-column>
    </el-table>
    <pagination v-show="total > 0" :total="total" v-model:page="query.pageNum" v-model:limit="query.pageSize" @pagination="getList" />
  </div>
</template>

<script setup>
import { listPendingReviews, auditReview } from '@/api/drama'
import { getCurrentInstance, reactive, ref } from 'vue'

const { proxy } = getCurrentInstance()
const loading = ref(false)
const list = ref([])
const total = ref(0)
const query = reactive({ pageNum: 1, pageSize: 10 })

function getList() {
  loading.value = true
  listPendingReviews(query).then(res => {
    list.value = res.rows || []
    total.value = res.total ?? 0
  }).finally(() => { loading.value = false })
}

function audit(row, status) {
  auditReview(row.reviewId, { status, admin_remark: '' }).then(() => {
    proxy.$modal.msgSuccess('已更新')
    getList()
  })
}

getList()
</script>

<style scoped>
.mb2 { margin-bottom: 12px; }
</style>
