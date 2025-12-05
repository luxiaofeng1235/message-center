<template>
  <el-card>
    <div class="toolbar">
      <el-button type="primary" @click="openForm()">新增通道消息类型</el-button>
    </div>
    <el-table :data="items">
      <el-table-column prop="id" label="ID" width="70" />
      <el-table-column prop="channel_id" label="通道ID" />
      <el-table-column prop="message_type_id" label="类型ID" />
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
      <el-form :model="form" label-width="90px">
        <el-form-item label="通道ID">
          <el-input v-model.number="form.channel_id" />
        </el-form-item>
        <el-form-item label="类型ID">
          <el-input v-model.number="form.message_type_id" />
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
} from '../api'

const items = ref([])
const meta = reactive({ total: 0, page: 1, page_size: 20 })
const visible = ref(false)
const form = reactive({
  id: null,
  channel_id: null,
  message_type_id: null,
  is_default: false,
  is_active: true,
  configStr: '',
})

const fetchData = async () => {
  const { data } = await listChannelMessageTypes({ page: meta.page, page_size: meta.page_size })
  items.value = data.items
  Object.assign(meta, data.meta)
}

const openForm = (row = null) => {
  visible.value = true
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
    if (!err.response) return
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

onMounted(fetchData)
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
