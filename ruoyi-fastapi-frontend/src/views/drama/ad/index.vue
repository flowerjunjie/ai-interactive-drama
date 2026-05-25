<template>
  <div class="app-container">
    <el-button type="primary" class="mb" @click="openForm()" v-hasPermi="['sdrama:ad:add']">新增广告</el-button>
    <el-form :inline="true" class="mb">
      <el-form-item>
        <el-button plain @click="getList">刷新</el-button>
      </el-form-item>
    </el-form>
    <el-table v-loading="loading" :data="list" border>
      <el-table-column label="ID" prop="adId" width="80" />
      <el-table-column label="标题" prop="title" min-width="140" />
      <el-table-column label="类型" prop="mediaType" width="90" />
      <el-table-column label="slot" prop="slotType" width="110" />
      <el-table-column label="曝光" prop="impressionCount" width="100" />
      <el-table-column label="点击" prop="clickCount" width="100" />
      <el-table-column label="权重" prop="weight" width="80" />
      <el-table-column label="状态" prop="status" width="80" />
      <el-table-column label="操作" width="160" align="center">
        <template #default="{ row }">
          <el-button link type="primary" @click="openForm(row)" v-hasPermi="['sdrama:ad:list']">编辑</el-button>
          <el-button link type="danger" @click="del(row)" v-hasPermi="['sdrama:ad:remove']">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <pagination v-show="total > 0" :total="total" v-model:page="query.pageNum" v-model:limit="query.pageSize" @pagination="getList" />

    <el-dialog :title="form.adId ? '编辑广告' : '新增广告'" v-model="open" width="520px">
      <el-form :model="form" label-width="100px">
        <el-form-item label="标题"><el-input v-model="form.title" /></el-form-item>
        <el-form-item label="媒体类型">
          <el-select v-model="form.mediaType">
            <el-option label="图片" value="image" />
            <el-option label="视频" value="video" />
          </el-select>
        </el-form-item>
        <el-form-item label="媒体URL"><el-input v-model="form.mediaUrl" /></el-form-item>
        <el-form-item label="封面URL"><el-input v-model="form.coverUrl" /></el-form-item>
        <el-form-item label="跳转链接"><el-input v-model="form.linkUrl" /></el-form-item>
        <el-form-item label="广告位">
          <el-select v-model="form.slotType">
            <el-option label="信息流 feed" value="feed" />
            <el-option label="贴片 pre_roll" value="pre_roll" />
            <el-option label="暂停 pause" value="pause" />
            <el-option label="详情 detail" value="detail" />
            <el-option label="我的 mine" value="mine" />
            <el-option label="播放页 player" value="player" />
          </el-select>
        </el-form-item>
        <el-form-item label="权重"><el-input-number v-model="form.weight" :min="0" /></el-form-item>
        <el-form-item label="开始"><el-date-picker v-model="form.startTime" type="datetime" value-format="YYYY-MM-DD HH:mm:ss" /></el-form-item>
        <el-form-item label="结束"><el-date-picker v-model="form.endTime" type="datetime" value-format="YYYY-MM-DD HH:mm:ss" /></el-form-item>
        <el-form-item label="状态">
          <el-select v-model="form.status">
            <el-option label="启用" value="0" />
            <el-option label="停用" value="1" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="open = false">取消</el-button>
        <el-button type="primary" @click="submit">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { addAd, delAd, listAds, updateAd } from '@/api/drama'
import { getCurrentInstance, reactive, ref } from 'vue'

const { proxy } = getCurrentInstance()
const loading = ref(false)
const list = ref([])
const total = ref(0)
const query = reactive({ pageNum: 1, pageSize: 10 })
const open = ref(false)
const form = reactive({
  adId: undefined,
  title: '',
  mediaType: 'image',
  mediaUrl: '',
  coverUrl: '',
  linkUrl: '',
  slotType: 'feed',
  weight: 0,
  startTime: '',
  endTime: '',
  status: '0'
})

function getList() {
  loading.value = true
  listAds(query).then(res => {
    list.value = res.rows || []
    total.value = res.total ?? 0
  }).finally(() => { loading.value = false })
}

function openForm(row) {
  if (row) {
    Object.assign(form, {
      adId: row.adId,
      title: row.title,
      mediaType: row.mediaType || 'image',
      mediaUrl: row.mediaUrl || row.imageUrl || '',
      coverUrl: row.coverUrl || '',
      linkUrl: row.linkUrl || '',
      slotType: row.slotType || 'feed',
      weight: row.weight ?? 0,
      startTime: row.startTime || '',
      endTime: row.endTime || '',
      status: row.status ?? '0'
    })
  } else {
    Object.assign(form, {
      adId: undefined,
      title: '',
      mediaType: 'image',
      mediaUrl: '',
      coverUrl: '',
      linkUrl: '',
      slotType: 'feed',
      weight: 0,
      startTime: '',
      endTime: '',
      status: '0'
    })
  }
  open.value = true
}

function submit() {
  const payload = {
    title: form.title,
    media_type: form.mediaType,
    media_url: form.mediaUrl || null,
    image_url: form.mediaUrl || null,
    cover_url: form.coverUrl || null,
    link_url: form.linkUrl || null,
    slot_type: form.slotType,
    weight: form.weight ?? 0,
    start_time: form.startTime || null,
    end_time: form.endTime || null,
    status: form.status
  }
  const req = form.adId ? updateAd(form.adId, payload) : addAd(payload)
  req.then(() => {
    proxy.$modal.msgSuccess('保存成功')
    open.value = false
    getList()
  })
}

function del(row) {
  proxy.$modal.confirm('删除该广告？').then(() => delAd(row.adId)).then(() => {
    proxy.$modal.msgSuccess('已删除')
    getList()
  }).catch(() => {})
}

getList()
</script>

<style scoped>
.mb { margin-bottom: 12px; }
</style>
