<template>
  <div class="video-uploader">
    <!-- 上传按钮 -->
    <div v-if="!disabled">
      <el-button :type="btnType" :size="btnSize" :loading="uploading" @click="triggerFile">
        <el-icon v-if="!uploading"><upload-filled /></el-icon>
        {{ uploading ? '上传中...' : btnLabel }}
      </el-button>
      <input ref="fileInput" type="file" :accept="accept" class="hidden" @change="onFileChange" />
    </div>

    <!-- 上传进度 -->
    <div v-if="uploading && progress > 0" class="mt-2">
      <el-progress :percentage="Math.round(progress)" :stroke-width="6" />
    </div>

    <!-- 当前值预览 -->
    <div v-if="modelValue && !uploading" class="current-url mt-2 text-sm text-gray-500 truncate">
      当前: {{ modelValue }}
    </div>

    <!-- 提示 -->
    <div v-if="showTip && !disabled" class="el-upload__tip">
      请上传<span style="color:#f56c6c">{{ acceptLabel }}</span> 格式
      <template v-if="fileSize">, 大小不超过 <b style="color:#f56c6c">{{ fileSize }}MB</b></template>
    </div>
  </div>
</template>

<script setup>
import { getCurrentInstance } from 'vue'
import axios from 'axios'
import { UploadFilled } from '@element-plus/icons-vue'
import { uploadSign, uploadComplete } from '@/api/drama'

const props = defineProps({
  modelValue: { type: String, default: null },
  // 'videos' | 'covers' | 'ads'
  objectKind: { type: String, default: 'videos' },
  // 'video/mp4' | 'image/jpeg' | etc
  contentType: { type: String, default: 'video/mp4' },
  // 接受的后缀
  acceptExt: { type: Array, default: () => ['mp4', 'mov', 'avi', 'webm'] },
  fileSize: { type: Number, default: 500 }, // MB
  showTip: { type: Boolean, default: true },
  disabled: { type: Boolean, default: false },
  btnLabel: { type: String, default: '选择文件' },
  btnType: { type: String, default: 'primary' },
  btnSize: { type: String, default: 'default' },
  dramaId: { type: Number, default: null },
  nodeId: { type: Number, default: null },
})

const emit = defineEmits(['update:modelValue', 'success', 'error'])

const { proxy } = getCurrentInstance()
const fileInput = ref(null)
const uploading = ref(false)
const progress = ref(0)

const accept = computed(() => {
  const map = {
    'video/mp4': 'video/mp4,video/quicktime,video/x-msvideo,video/webm',
    'image/jpeg': 'image/jpeg,image/png,image/webp',
  }
  return map[props.contentType] || props.contentType
})

const acceptLabel = computed(() => props.acceptExt.join('/'))

function triggerFile() {
  fileInput.value?.click()
}

async function onFileChange(e) {
  const file = e.target.files?.[0]
  if (!file) return

  // 前端校检
  const ext = file.name.split('.').pop().toLowerCase()
  if (!props.acceptExt.includes(ext)) {
    proxy.$modal.msgError(`文件格式不正确，请上传 ${acceptLabel.value} 格式`)
    e.target.value = ''
    return
  }
  if (props.fileSize && file.size / 1024 / 1024 > props.fileSize) {
    proxy.$modal.msgError(`上传文件大小不能超过 ${props.fileSize} MB`)
    e.target.value = ''
    return
  }

  await doUpload(file)
  e.target.value = ''
}

async function doUpload(file) {
  uploading.value = true
  progress.value = 0

  let fileId = null
  let objectKey = null
  let signedUrl = null

  try {
    // Step 1: get pre-signed URL
    const signRes = await uploadSign(
      file.name,
      props.contentType,
      props.dramaId,
      props.nodeId,
      props.objectKind
    )
    if (signRes.code !== 200 || !signRes.data) {
      throw new Error(signRes.msg || '获取上传签名失败')
    }
    signedUrl = signRes.data.uploadUrl
    objectKey = signRes.data.objectKey
    fileId = signRes.data.fileId

    // Step 2: PUT directly to TOS using pre-signed URL
    await axios.put(signedUrl, file, {
      headers: { 'Content-Type': props.contentType },
      onUploadProgress: (evt) => {
        if (evt.total) {
          progress.value = (evt.loaded / evt.total) * 100
        }
      },
    })

    // Step 3: notify backend upload complete
    const completePayload = { file_id: fileId }
    if (props.objectKind === 'videos') {
      completePayload.video_url = signedUrl.split('?')[0] // use signed URL without query params
      completePayload.tos_key = objectKey
    } else if (props.objectKind === 'covers') {
      completePayload.cover_url = signedUrl.split('?')[0]
      completePayload.tos_key = objectKey
    }

    const completeRes = await uploadComplete(
      completePayload.file_id,
      completePayload.video_url,
      completePayload.cover_url,
      completePayload.tos_key
    )

    if (completeRes.code !== 200) {
      throw new Error(completeRes.msg || '完成上传失败')
    }

    // Step 4: emit final URL
    const finalUrl = signedUrl.split('?')[0]
    emit('update:modelValue', finalUrl)
    emit('success', { url: finalUrl, objectKey, fileId })

    proxy.$modal.msgSuccess('上传成功')
  } catch (err) {
    proxy.$modal.msgError('上传失败: ' + (err.message || err))
    emit('error', err)
  } finally {
    uploading.value = false
    progress.value = 0
  }
}
</script>

<style scoped>
.hidden { display: none; }
.mt-2 { margin-top: 8px; }
.truncate { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
</style>