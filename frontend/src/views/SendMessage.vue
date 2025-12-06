<template>
  <el-card>
    <el-form ref="formRef" :model="form" :rules="rules" label-width="120px">
      <el-form-item label="App" prop="app_id">
        <el-select v-model="form.app_id" placeholder="请选择" filterable clearable @change="onAppChange">
          <el-option v-for="app in appOptions" :key="app.value" :label="app.label" :value="app.value" />
        </el-select>
      </el-form-item>
      <el-form-item label="通道" prop="channel_id">
        <el-select v-model="form.channel_id" placeholder="请选择" filterable clearable @change="onChannelChange">
          <el-option
            v-for="ch in channelOptions"
            :key="ch.value"
            :label="ch.label"
            :value="ch.value"
          />
        </el-select>
        <div v-if="selectedChannelMode !== null" class="mode-hint">
          模式：{{ modeLabel(selectedChannelMode) }}
        </div>
      </el-form-item>
      <el-form-item label="消息类型" prop="message_type_id">
        <el-select v-model="form.message_type_id" placeholder="请选择" filterable clearable>
          <el-option
            v-for="mt in messageTypeOptions"
            :key="mt.value"
            :label="mt.label"
            :value="mt.value"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="标题">
        <el-input v-model="form.title" />
      </el-form-item>
      <el-form-item label="内容" prop="content">
        <el-input type="textarea" v-model="form.content" />
      </el-form-item>
      <el-form-item label="Payload(JSON)">
        <el-input type="textarea" v-model="payloadStr" placeholder='{"foo":"bar"}' />
      </el-form-item>
      <el-form-item label="优先级">
        <el-input v-model.number="form.priority" />
      </el-form-item>
      <el-form-item v-if="selectedChannelMode === 1" label="目标用户ID(逗号分隔)">
        <el-input v-model="targetUsersStr" placeholder="如：1,2,3" />
      </el-form-item>
      <el-form-item label="X-App-Secret" prop="app_secret">
        <el-input v-model="form.app_secret" />
      </el-form-item>
      <el-button type="primary" @click="send" :loading="loading">发送</el-button>
    </el-form>
    <el-divider />
    <div v-if="result">
      <p>发送结果：ID {{ result.id }}，状态 {{ result.status }}，创建时间 {{ result.created_at }}</p>
    </div>
  </el-card>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { sendMessage, listApps, listChannels, listChannelMessageTypes, listMessageTypesAll } from '../api'

const form = reactive({
  app_id: null,
  channel_id: null,
  message_type_id: null,
  title: '',
  content: '',
  priority: 0,
  app_secret: '',
})
const payloadStr = ref('')
const targetUsersStr = ref('')
const result = ref(null)
const loading = ref(false)
const formRef = ref()
const rules = {
  app_id: [{ required: true, message: '请选择App', trigger: 'change' }],
  channel_id: [{ required: true, message: '请选择通道', trigger: 'change' }],
  message_type_id: [{ required: true, message: '请选择消息类型', trigger: 'change' }],
  content: [{ required: true, message: '请输入内容', trigger: 'blur' }],
  app_secret: [{ required: true, message: '请输入X-App-Secret', trigger: 'blur' }],
}

const appOptions = ref([])
const channelOptions = ref([])
const messageTypeOptions = ref([])
const messageTypeDict = ref({})
const selectedChannelMode = ref(null)

const loadApps = async () => {
  const res = await listApps({ page: 1, page_size: 1000 })
  appOptions.value = (res.items || []).map((a) => ({
    value: a.id,
    label: `${a.name || ''} (ID:${a.id})`,
  }))
}

const loadChannels = async (appId) => {
  const res = await listChannels({ page: 1, page_size: 1000, app_id: appId || undefined })
  channelOptions.value = (res.items || []).map((c) => ({
    value: c.id,
    label: `${c.name || ''} (ID:${c.id})`,
    mode: c.dispatch_mode,
  }))
}

const loadMessageTypes = async (channelId) => {
  if (!channelId) {
    messageTypeOptions.value = []
    return
  }
  const res = await listChannelMessageTypes({ page: 1, page_size: 1000, channel_id: channelId })
  messageTypeOptions.value = (res.items || []).map((m) => {
    const mt = messageTypeDict.value[m.message_type_id]
    const name = mt?.name || ''
    return {
      value: m.message_type_id,
      label: `${name} (ID:${m.message_type_id})`,
    }
  })
}

const onAppChange = async (appId) => {
  form.channel_id = null
  form.message_type_id = null
  selectedChannelMode.value = null
  await loadChannels(appId)
  messageTypeOptions.value = []
}

const onChannelChange = async (channelId) => {
  form.message_type_id = null
  const found = channelOptions.value.find((c) => c.value === channelId)
  selectedChannelMode.value = found ? found.mode : null
  await loadMessageTypes(channelId)
}

const loadMessageTypeDict = async () => {
  const res = await listMessageTypesAll()
  const dict = {}
  for (const mt of res.items || []) {
    dict[mt.id] = mt
  }
  messageTypeDict.value = dict
}

const send = async () => {
  loading.value = true
  try {
    await formRef.value.validate()
    const payload = { ...form, payload: payloadStr.value ? JSON.parse(payloadStr.value) : null }
    if (selectedChannelMode.value === 1) {
      payload.target_user_ids = targetUsersStr.value
        ? targetUsersStr.value
            .split(',')
            .map((s) => s.trim())
            .filter(Boolean)
            .map((n) => Number(n))
            .filter((n) => !Number.isNaN(n))
        : []
    }
    const res = await sendMessage(payload, form.app_secret)
    result.value = res
    ElMessage.success('发送成功')
  } catch (err) {
    if (err instanceof SyntaxError) {
      ElMessage.error('Payload 必须是合法 JSON')
    } else {
      if (!err?.response && err?.name === 'Error' && !err?.msg) return
      ElMessage.error(err.response?.data?.detail || err.msg || '发送失败')
    }
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  await Promise.all([loadApps(), loadMessageTypeDict()])
})

const modeLabel = (mode) => {
  if (mode === 1) return '单播/定向'
  if (mode === 2) return '广播'
  return '订阅'
}
</script>

<style scoped>
.mode-hint {
  margin-top: 6px;
  color: #666;
}
</style>
