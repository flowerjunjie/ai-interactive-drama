<template>
  <div class="app-container">
    <el-form :inline="true">
      <el-form-item label="短剧ID"><el-input-number v-model="query.dramaId" :min="1" controls-position="right" /></el-form-item>
      <el-form-item>
        <el-button type="primary" @click="getList" v-hasPermi="['sdrama:comment:list']">搜索</el-button>
        <el-button plain @click="() => { query.dramaId = undefined; getList() }" v-hasPermi="['sdrama:comment:list']">重置</el-button>
      </el-form-item>
    </el-form>
    <el-table v-loading="loading" :data="list" border>
      <el-table-column label="ID" prop="commentId" width="80" />
      <el-table-column label="短剧" prop="dramaId" width="90" />
      <el-table-column label="用户" prop="appUserId" width="90" />
      <el-table-column label="内容" prop="content" min-width="200" show-overflow-tooltip />
      <el-table-column label="状态" prop="status" width="80" />
      <el-table-column label="操作" width="200" align="center">
        <template #default="{ row }">
          <el-button link type="warning" @click="hide(row)" v-hasPermi="['sdrama:comment:hide']">屏蔽</el-button>
          <el-button link type="danger" @click="del(row)" v-hasPermi="['sdrama:comment:remove']">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <pagination v-show="total > 0" :total="total" v-model:page="query.pageNum" v-model:limit="query.pageSize" @pagination="getList" />
  </div>
</template>

<script setup>
import { delDramaComment, hideDramaComment, listDramaComments } from '@/api/drama'
import { getCurrentInstance, reactive, ref } from 'vue'

const { proxy } = getCurrentInstance()
const loading = ref(false)
const list = ref([])
const total = ref(0)
const query = reactive({ pageNum: 1, pageSize: 10, dramaId: undefined })

function getList() {
  loading.value = true
  listDramaComments(query)
    .then(res => {
      list.value = res.rows || []
      total.value = res.total ?? 0
    })
    .finally(() => { loading.value = false })
}

function hide(row) {
  hideDramaComment(row.commentId, true).then(() => {
    proxy.$modal.msgSuccess('已屏蔽')
    getList()
  })
}

function del(row) {
  proxy.$modal.confirm('确认删除？').then(() => delDramaComment(row.commentId)).then(() => {
    proxy.$modal.msgSuccess('已删除')
    getList()
  }).catch(() => {})
}

getList()
</script>
