<template>
  <el-card>
    <div class="toolbar">
      <el-button type="primary" @click="openForm()">新增通道消息类型</el-button>
    </div>
    <el-table :data="items">
      <el-table-column prop="id" label="ID" width="70" />
      <el-table-column prop="channel_name" label="通道" />
      <el-table-column prop="message_type_name" label="消息类型" />
      <el-table-column prop="is_default" label="默认">
        <template #default="scope">
          <el-tag v-if="scope.row.is_default">是</el-tag>
          <el-tag v-else type="info">否</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="is_active" label="启用">
        <template #default="scope">
          <el-switch v-model="scope.row.is_active" @change="toggleActive(scope.row)" />
        </template>
      </el-table-column>
      <el-table-column label="操作" width="140">
        <template #default="scope">
          <el-button size="small" @click="openForm(scope.row)">编辑</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
      class="mt"
      layout="prev, pager, next"
      :total="meta.total"
      :page-size="meta.page_size"
      @current-change="pageChange"
    />

    <el-dialog v-model="visible" title="通道消息类型">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="90px">
        <el-form-item label="通道" prop="channel_id">
          <el-select v-model="form.channel_id" placeholder="请选择" clearable>
            <el-option
              v-for="ch in channelOptions"
              :key="ch.value"
              :label="ch.label"
              :value="ch.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="消息类型" prop="message_type_id">
          <el-select v-model="form.message_type_id" placeholder="请选择" clearable>
            <el-option
              v-for="mt in messageTypeOptions"
              :key="mt.value"
              :label="mt.label"
              :value="mt.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="默认">
          <el-switch v-model="form.is_default" />
        </el-form-item>
        <el-form-item label="启用">
          <el-switch v-model="form.is_active" />
        </el-form-item>
        <el-form-item label="配置(JSON)">
          <el-input v-model="form.configStr" type="textarea" placeholder="可选 JSON" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="visible = false">取消</el-button>
        <el-button type="primary" @click="save">保存</el-button>
      </template>
    </el-dialog>
  </el-card>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import {
  listChannelMessageTypes,
  createChannelMessageType,
  updateChannelMessageType,
  listChannelsAll,
  listMessageTypesAll,
} from '../api'

const items = ref([])
const meta = reactive({ total: 0, page: 1, page_size: 20 })
const visible = ref(false)
const formRef = ref()
const form = reactive({
  id: null,
  channel_id: null,
  message_type_id: null,
  is_default: false,
  is_active: true,
  configStr: '',
})
const channelOptions = ref([])
const messageTypeOptions = ref([])
const rules = {
  channel_id: [{ required: true, message: '请选择通道', trigger: 'change' }],
  message_type_id: [{ required: true, message: '请选择消息类型', trigger: 'change' }],
}

const fetchData = async () => {
  const res = await listChannelMessageTypes({ page: meta.page, page_size: meta.page_size })
  items.value = res.items.map((i) => ({
    ...i,
    channel_name: channelOptions.value.find((c) => c.value === i.channel_id)?.label || i.channel_id,
    message_type_name:
      messageTypeOptions.value.find((m) => m.value === i.message_type_id)?.label || i.message_type_id,
  }))
  Object.assign(meta, res.meta)
}

const openForm = (row = null) => {
  visible.value = true
  formRef.value?.clearValidate()
  if (row) {
    Object.assign(form, {
      ...row,
      configStr: row.config ? JSON.stringify(row.config) : '',
    })
  } else {
    Object.assign(form, {
      id: null,
      channel_id: null,
      message_type_id: null,
      is_default: false,
      is_active: true,
      configStr: '',
    })
  }
}

const fetchOptions = async () => {
  const [channels, messageTypes] = await Promise.all([listChannelsAll(), listMessageTypesAll()])
  channelOptions.value = (channels.items || []).map((c) => ({
    value: c.id,
    label: `${c.name || ''} (ID:${c.id})`,
  }))
  messageTypeOptions.value = (messageTypes.items || []).map((m) => ({
    value: m.id,
    label: `${m.name || ''} (ID:${m.id})`,
  }))
}

const parseConfig = () => {
  if (!form.configStr) return null
  try {
    return JSON.parse(form.configStr)
  } catch (e) {
    ElMessage.error('配置必须是合法 JSON')
    throw e
  }
}

const save = async () => {
  try {
    await formRef.value.validate()
    const payload = {
      channel_id: form.channel_id,
      message_type_id: form.message_type_id,
      is_default: form.is_default,
      is_active: form.is_active,
      config: parseConfig(),
    }
    if (form.id) {
      await updateChannelMessageType(form.id, payload)
    } else {
      await createChannelMessageType(payload)
    }
    ElMessage.success('保存成功')
    visible.value = false
    fetchData()
  } catch (err) {
    if (!err?.response && err?.name === 'Error' && !err?.msg) return
    ElMessage.error(err.response?.data?.detail || '保存失败')
  }
}

const toggleActive = async (row) => {
  await updateChannelMessageType(row.id, { is_active: row.is_active })
}

const pageChange = (p) => {
  meta.page = p
  fetchData()
}

onMounted(async () => {
  await fetchOptions()
  await fetchData()
})
</script>

<style scoped>
.toolbar {
  margin-bottom: 12px;
}
.mt {
  margin-top: 12px;
  text-align: right;
}
</style>
