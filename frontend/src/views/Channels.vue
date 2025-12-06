<template>
  <el-card>
    <div class="toolbar">
      <el-button type="primary" @click="openForm()">新增通道</el-button>
    </div>
    <el-table :data="items">
      <el-table-column prop="id" label="ID" width="70" />
      <el-table-column prop="app_id" label="AppID" width="80" />
      <el-table-column prop="channel_key" label="Key" />
      <el-table-column prop="name" label="名称" />
      <el-table-column prop="dispatch_mode" label="模式" width="120">
        <template #default="scope">
          <el-tag type="info">{{ modeLabel(scope.row.dispatch_mode) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="is_active" label="启用">
        <template #default="scope">
          <el-switch v-model="scope.row.is_active" @change="toggleActive(scope.row)" />
        </template>
      </el-table-column>
      <el-table-column label="操作" width="120">
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

    <el-dialog v-model="visible" title="通道">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="90px">
        <el-form-item label="AppID" prop="app_id">
          <el-input v-model.number="form.app_id" />
        </el-form-item>
        <el-form-item label="Key" prop="channel_key">
          <el-input v-model="form.channel_key" :disabled="!!form.id" />
        </el-form-item>
        <el-form-item label="名称" prop="name">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="form.description" />
        </el-form-item>
        <el-form-item label="投递模式" prop="dispatch_mode">
          <el-radio-group v-model="form.dispatch_mode">
            <el-radio :label="0">按订阅</el-radio>
            <el-radio :label="1">广播在线用户</el-radio>
            <el-radio :label="2">广播所有用户</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="广播过滤(JSON)">
          <el-input type="textarea" v-model="form.broadcast_filter_str" placeholder="可选，JSON 结构" />
        </el-form-item>
        <el-form-item label="启用">
          <el-switch v-model="form.is_active" />
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
import { listChannels, createChannel, updateChannel } from '../api'

const items = ref([])
const meta = reactive({ total: 0, page: 1, page_size: 20 })
const visible = ref(false)
const formRef = ref()
const form = reactive({
  id: null,
  app_id: null,
  channel_key: '',
  name: '',
  description: '',
  dispatch_mode: 0,
  broadcast_filter_str: '',
  is_active: true,
})
const rules = {
  app_id: [{ required: true, message: '请输入AppID', trigger: 'blur' }],
  channel_key: [{ required: true, message: '请输入通道Key', trigger: 'blur' }],
  name: [{ required: true, message: '请输入通道名称', trigger: 'blur' }],
  dispatch_mode: [{ required: true, message: '请选择投递模式', trigger: 'change' }],
}

const fetchData = async () => {
  const res = await listChannels({ page: meta.page, page_size: meta.page_size })
  items.value = res.items
  Object.assign(meta, res.meta)
}

const openForm = (row = null) => {
  visible.value = true
  formRef.value?.clearValidate()
  if (row) {
    Object.assign(form, {
      ...row,
      broadcast_filter_str: row.broadcast_filter ? JSON.stringify(row.broadcast_filter) : '',
    })
  } else {
    Object.assign(form, {
      id: null,
      app_id: null,
      channel_key: '',
      name: '',
      description: '',
      dispatch_mode: 0,
      broadcast_filter_str: '',
      is_active: true,
    })
  }
}

const save = async () => {
  try {
    await formRef.value.validate()
    let broadcast_filter = null
    if (form.broadcast_filter_str) {
      try {
        broadcast_filter = JSON.parse(form.broadcast_filter_str)
      } catch (e) {
        ElMessage.error('广播过滤必须是合法 JSON')
        return
      }
    }
    if (form.id) {
      await updateChannel(form.id, {
        name: form.name,
        description: form.description,
        is_active: form.is_active,
        dispatch_mode: form.dispatch_mode,
        broadcast_filter,
      })
    } else {
      await createChannel({
        app_id: form.app_id,
        channel_key: form.channel_key,
        name: form.name,
        description: form.description,
        is_active: form.is_active,
        dispatch_mode: form.dispatch_mode,
        broadcast_filter,
      })
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
  await updateChannel(row.id, { is_active: row.is_active })
}

const pageChange = (p) => {
  meta.page = p
  fetchData()
}

const modeLabel = (mode) => {
  if (mode === 1) return '单播（一对一）'
  if (mode === 2) return '广播（全部）'
  return '订阅模式'
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
