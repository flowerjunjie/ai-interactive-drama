<template>
  <div class="app-container">
    <el-alert type="info" :closable="false" title="维护节点、互动分支；审核请在「视频审核」或通过 moderation 接口。" />
    <el-form :inline="true" class="mt">
      <el-form-item label="短剧ID"><el-input-number v-model="query.dramaId" :min="1" /></el-form-item>
      <el-form-item label="审核">
        <el-select v-model="query.reviewStatus" clearable placeholder="全部" style="width:140px">
          <el-option label="pending" value="pending" />
          <el-option label="approved" value="approved" />
          <el-option label="rejected" value="rejected" />
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="getList" v-hasPermi="['sdrama:node:list']">搜索</el-button>
        <el-button type="success" plain @click="openForm()" v-hasPermi="['sdrama:node:add']">新增节点</el-button>
      </el-form-item>
    </el-form>
    <el-table v-loading="loading" :data="list" border>
      <el-table-column label="节点ID" prop="nodeId" width="90" />
      <el-table-column label="短剧ID" prop="dramaId" width="90" />
      <el-table-column label="集" prop="episodeNo" width="70" />
      <el-table-column label="标题" prop="title" min-width="120" />
      <el-table-column label="入口" prop="isEntry" width="70" />
      <el-table-column label="互动" prop="isInteractive" width="70" />
      <el-table-column label="触发秒" prop="choiceTriggerSec" width="90" />
      <el-table-column label="审核" prop="reviewStatus" width="100" />
      <el-table-column label="状态" prop="status" width="100" />
      <el-table-column label="视频" min-width="160" show-overflow-tooltip prop="videoUrl" />
      <el-table-column label="操作" width="220" align="center">
        <template #default="{ row }">
          <el-button link type="primary" @click="openBranch(row)" v-hasPermi="['sdrama:choice:list']">分支</el-button>
          <el-button link type="primary" @click="openForm(row)" v-hasPermi="['sdrama:node:edit']">编辑</el-button>
          <el-button link type="danger" @click="handleDel(row)" v-hasPermi="['sdrama:node:remove']">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <pagination v-show="total > 0" :total="total" v-model:page="query.pageNum" v-model:limit="query.pageSize" @pagination="getList" />

    <el-dialog :title="form.nodeId ? '编辑节点' : '新增节点'" v-model="open" width="560px" append-to-body>
      <el-form :model="form" label-width="108px">
        <el-form-item label="短剧ID"><el-input-number v-model="form.dramaId" :min="1" /></el-form-item>
        <el-form-item label="父节点ID"><el-input-number v-model="form.parentNodeId" :min="1" controls-position="right" /></el-form-item>
        <el-form-item label="标题"><el-input v-model="form.title" /></el-form-item>
        <el-form-item label="视频">
          <VideoUploader
            v-model="form.videoUrl"
            object-kind="videos"
            content-type="video/mp4"
            :accept-ext="['mp4','mov','avi','webm']"
            :file-size="500"
            :drama-id="form.dramaId"
            :node-id="form.nodeId"
            btn-label="上传视频"
            @success="(payload) => { form.tosKey = payload.objectKey }"
          />
        </el-form-item>
        <el-form-item label="封面">
          <VideoUploader
            v-model="form.coverUrl"
            object-kind="covers"
            content-type="image/jpeg"
            :accept-ext="['jpg','jpeg','png','webp']"
            :file-size="10"
            :drama-id="form.dramaId"
            :node-id="form.nodeId"
            btn-label="上传封面"
            @success="(payload) => { form.tosKey = payload.objectKey }"
          />
        </el-form-item>
        <el-form-item label="时长(秒)"><el-input-number v-model="form.durationSec" :min="0" /></el-form-item>
        <el-form-item label="集序号"><el-input-number v-model="form.episodeNo" :min="0" /></el-form-item>
        <el-form-item label="排序"><el-input-number v-model="form.sort" :min="0" /></el-form-item>
        <el-form-item label="入口"><el-switch v-model="form.isEntry" active-value="1" inactive-value="0" /></el-form-item>
        <el-form-item label="互动节点"><el-switch v-model="form.isInteractive" active-value="1" inactive-value="0" /></el-form-item>
        <el-form-item label="分支触发(秒)"><el-input-number v-model="form.choiceTriggerSec" :min="0" :step="0.5" /></el-form-item>
        <el-form-item label="上架状态">
          <el-select v-model="form.status">
            <el-option label="草稿" value="draft" />
            <el-option label="已发布" value="published" />
            <el-option label="下架" value="offline" />
          </el-select>
        </el-form-item>
        <el-form-item label="审核状态">
          <el-select v-model="form.reviewStatus">
            <el-option label="pending" value="pending" />
            <el-option label="approved" value="approved" />
            <el-option label="rejected" value="rejected" />
          </el-select>
        </el-form-item>
        <el-form-item label="拒绝原因"><el-input v-model="form.rejectReason" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="open = false">取消</el-button>
        <el-button type="primary" @click="submitNode">保存</el-button>
      </template>
    </el-dialog>

    <el-dialog title="剧情分支" v-model="brOpen" width="640px">
      <div class="mb">
        <el-button size="small" type="primary" @click="addChoiceRow">新增选项</el-button>
      </div>
      <el-table :data="choices" border size="small">
        <el-table-column label="编码" width="90"><template #default="{ row }"><el-input v-model="row.choiceCode" /></template></el-table-column>
        <el-table-column label="文案"><template #default="{ row }"><el-input v-model="row.label" /></template></el-table-column>
        <el-table-column label="下一节点" width="120"><template #default="{ row }"><el-input-number v-model="row.nextNodeId" :min="1" /></template></el-table-column>
        <el-table-column label="排序" width="90"><template #default="{ row }"><el-input-number v-model="row.sort" :min="0" /></template></el-table-column>
        <el-table-column label="操作" width="120" align="center">
          <template #default="{ row }">
            <el-button link type="primary" @click="saveChoice(row)">保存</el-button>
            <el-button link type="danger" @click="removeChoice(row)" v-if="row.choiceId">删</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-dialog>
  </div>
</template>

<script setup>
import {
  addVideoChoice,
  addVideoNode,
  delVideoChoice,
  delVideoNode,
  listVideoChoices,
  listVideoNode,
  updateVideoChoice,
  updateVideoNode
} from '@/api/drama'
import VideoUploader from '@/components/VideoUploader/index.vue'
import { getCurrentInstance, reactive, ref } from 'vue'

const { proxy } = getCurrentInstance()
const loading = ref(false)
const list = ref([])
const total = ref(0)
const query = reactive({ pageNum: 1, pageSize: 10, dramaId: undefined, reviewStatus: '' })
const open = ref(false)
const brOpen = ref(false)
const branchNodeId = ref(null)
const choices = ref([])
const form = reactive({
  nodeId: undefined,
  dramaId: 1,
  parentNodeId: undefined,
  title: '',
  videoUrl: '',
  coverUrl: '',
  tosKey: '',
  durationSec: undefined,
  episodeNo: undefined,
  sort: 0,
  isEntry: '0',
  isInteractive: '0',
  choiceTriggerSec: undefined,
  status: 'draft',
  reviewStatus: 'pending',
  rejectReason: ''
})

function getList() {
  loading.value = true
  listVideoNode(query).then(res => {
    list.value = res.rows || []
    total.value = res.total ?? 0
  }).finally(() => { loading.value = false })
}

function openForm(row) {
  if (row) {
    Object.assign(form, {
      nodeId: row.nodeId,
      dramaId: row.dramaId,
      parentNodeId: row.parentNodeId,
      title: row.title || '',
      videoUrl: row.videoUrl || '',
      coverUrl: row.coverUrl || '',
      tosKey: row.tosKey || '',
      durationSec: row.durationSec,
      episodeNo: row.episodeNo,
      sort: row.sort ?? 0,
      isEntry: row.isEntry || '0',
      isInteractive: row.isInteractive || '0',
      choiceTriggerSec: row.choiceTriggerSec,
      status: row.status || 'draft',
      reviewStatus: row.reviewStatus || 'pending',
      rejectReason: row.rejectReason || ''
    })
  } else {
    Object.assign(form, {
      nodeId: undefined,
      dramaId: query.dramaId || 1,
      parentNodeId: undefined,
      title: '',
      videoUrl: '',
      coverUrl: '',
      tosKey: '',
      durationSec: undefined,
      episodeNo: undefined,
      sort: 0,
      isEntry: '0',
      isInteractive: '0',
      choiceTriggerSec: undefined,
      status: 'draft',
      reviewStatus: 'pending',
      rejectReason: ''
    })
  }
  open.value = true
}

function payloadFromForm() {
  return {
    drama_id: form.dramaId,
    parent_node_id: form.parentNodeId || null,
    title: form.title || null,
    video_url: form.videoUrl || null,
    cover_url: form.coverUrl || null,
    tos_key: form.tosKey || null,
    duration_sec: form.durationSec ?? null,
    episode_no: form.episodeNo ?? null,
    sort: form.sort ?? 0,
    is_entry: form.isEntry,
    is_interactive: form.isInteractive,
    choice_trigger_sec: form.choiceTriggerSec ?? null,
    status: form.status,
    review_status: form.reviewStatus,
    reject_reason: form.rejectReason || null
  }
}

function submitNode() {
  const payload = payloadFromForm()
  const req = form.nodeId ? updateVideoNode(form.nodeId, payload) : addVideoNode(payload)
  req.then(() => {
    proxy.$modal.msgSuccess('保存成功')
    open.value = false
    getList()
  })
}

function handleDel(row) {
  proxy.$modal.confirm('确认删除节点及其分支？').then(() => {
    delVideoNode(row.nodeId).then(() => {
      proxy.$modal.msgSuccess('已删除')
      getList()
    })
  }).catch(() => {})
}

function loadChoices() {
  return listVideoChoices(branchNodeId.value).then(res => {
    choices.value = res.rows || []
    if (!choices.value.length) {
      choices.value.push({ choiceId: undefined, choiceCode: 'A', label: '', nextNodeId: undefined, sort: 0 })
    }
  })
}

function openBranch(row) {
  branchNodeId.value = row.nodeId
  loadChoices().then(() => {
    brOpen.value = true
  })
}

function addChoiceRow() {
  choices.value.push({ choiceId: undefined, choiceCode: '', label: '', nextNodeId: undefined, sort: 0 })
}

function saveChoice(row) {
  const body = {
    node_id: branchNodeId.value,
    choice_code: row.choiceCode || null,
    label: row.label,
    next_node_id: row.nextNodeId,
    sort: row.sort ?? 0
  }
  const req = row.choiceId ? updateVideoChoice(row.choiceId, body) : addVideoChoice(body)
  req.then(() => {
    proxy.$modal.msgSuccess('分支已保存')
    return loadChoices()
  })
}

function removeChoice(row) {
  delVideoChoice(row.choiceId).then(() => {
    proxy.$modal.msgSuccess('已删除')
    return loadChoices()
  })
}

getList()
</script>

<style scoped>
.mt { margin-top: 12px; }
.mb { margin-bottom: 8px; }
</style>
