<template>
  <div class="app-container">
    <el-form :inline="true">
      <el-form-item label="标题"><el-input v-model="query.title" clearable placeholder="模糊" style="width:180px" /></el-form-item>
      <el-form-item>
        <el-button type="primary" @click="getList" v-hasPermi="['sdrama:drama:list']">搜索</el-button>
        <el-button type="primary" plain @click="openForm()" v-hasPermi="['sdrama:drama:add']">新增</el-button>
      </el-form-item>
    </el-form>
    <el-table v-loading="loading" :data="list" border>
      <el-table-column label="ID" prop="dramaId" width="80" />
      <el-table-column label="标题" prop="title" min-width="160" />
      <el-table-column label="标签" prop="tags" width="140" show-overflow-tooltip />
      <el-table-column label="热度" prop="heat" width="80" />
      <el-table-column label="类型" prop="dramaType" width="120" />
      <el-table-column label="状态" prop="status" width="100" />
      <el-table-column label="操作" width="160" align="center">
        <template #default="scope">
          <el-button link type="primary" @click="openForm(scope.row)" v-hasPermi="['sdrama:drama:edit']">编辑</el-button>
          <el-button link type="danger" @click="handleDel(scope.row)" v-hasPermi="['sdrama:drama:remove']">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <pagination
      v-show="total > 0"
      :total="total"
      v-model:page="query.pageNum"
      v-model:limit="query.pageSize"
      @pagination="getList"
    />

    <el-dialog :title="form.dramaId ? '编辑短剧' : '新增短剧'" v-model="open" width="520px" append-to-body>
      <el-form :model="form" label-width="88px">
        <el-form-item label="标题"><el-input v-model="form.title" /></el-form-item>
        <el-form-item label="类型">
          <el-select v-model="form.dramaType">
            <el-option label="漫剧" value="comic_drama" />
            <el-option label="真人剧" value="live_action" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="form.status">
            <el-option label="草稿" value="draft" />
            <el-option label="已发布" value="published" />
            <el-option label="下架" value="offline" />
          </el-select>
        </el-form-item>
        <el-form-item label="封面URL"><el-input v-model="form.coverUrl" /></el-form-item>
        <el-form-item label="简介"><el-input type="textarea" v-model="form.description" /></el-form-item>
        <el-form-item label="标签"><el-input v-model="form.tags" placeholder="JSON数组或逗号分隔" /></el-form-item>
        <el-form-item label="热度"><el-input-number v-model="form.heat" :min="0" /></el-form-item>
        <el-form-item label="排序"><el-input-number v-model="form.sort" :min="0" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="open = false">取 消</el-button>
        <el-button type="primary" @click="submit">确 定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { addDrama, delDrama, listDrama, updateDrama } from '@/api/drama'
import { getCurrentInstance, reactive, ref } from 'vue'

const { proxy } = getCurrentInstance()
const loading = ref(false)
const list = ref([])
const total = ref(0)
const open = ref(false)
const query = reactive({ pageNum: 1, pageSize: 10, title: '' })
const form = reactive({
  dramaId: undefined,
  title: '',
  dramaType: 'comic_drama',
  status: 'draft',
  coverUrl: '',
  description: '',
  tags: '',
  heat: 0,
  sort: 0
})

function getList() {
  loading.value = true
  listDrama(query).then(res => {
    list.value = res.rows || []
    total.value = res.total ?? 0
  }).finally(() => { loading.value = false })
}

function openForm(row) {
  if (row) {
    Object.assign(form, {
      dramaId: row.dramaId,
      title: row.title,
      dramaType: row.dramaType,
      status: row.status,
      coverUrl: row.coverUrl,
      description: row.description,
      tags: row.tags || '',
      heat: row.heat ?? 0,
      sort: row.sort
    })
  } else {
    Object.assign(form, { dramaId: undefined, title: '', dramaType: 'comic_drama', status: 'draft', coverUrl: '', description: '', tags: '', heat: 0, sort: 0 })
  }
  open.value = true
}

function submit() {
  const payload = {
    title: form.title,
    drama_type: form.dramaType,
    status: form.status,
    cover_url: form.coverUrl || null,
    description: form.description || null,
    tags: form.tags || null,
    heat: form.heat ?? 0,
    sort: form.sort || 0
  }
  const req = form.dramaId ? updateDrama(form.dramaId, payload) : addDrama(payload)
  req.then(() => {
    proxy.$modal.msgSuccess('保存成功')
    open.value = false
    getList()
  })
}

function handleDel(row) {
  proxy.$modal.confirm('确认删除？').then(() => {
    delDrama(row.dramaId).then(() => {
      proxy.$modal.msgSuccess('删除成功')
      getList()
    })
  }).catch(() => {})
}

getList()
</script>
