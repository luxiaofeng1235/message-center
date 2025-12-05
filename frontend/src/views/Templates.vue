<template>
  <el-card>
    <div class="toolbar">
      <el-button type="primary" @click="openForm()">新增模板</el-button>
    </div>
    <el-table :data="items">
      <el-table-column prop="id" label="ID" width="70" />
      <el-table-column prop="app_id" label="AppID" width="80" />
      <el-table-column prop="channel_id" label="通道ID" width="90" />
      <el-table-column prop="template_key" label="Key" />
      <el-table-column prop="name" label="名称" />
      <el-table-column prop="is_default" label="默认">
        <template #default="scope">
          <el-tag v-if="scope.row.is_default">是</el-tag>
          <el-tag v-else type="info">否</el-tag>
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

    <el-dialog v-model="visible" title="模板">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="90px">
        <el-form-item label="AppID" prop="app_id">
          <el-input v-model.number="form.app_id" />
        </el-form-item>
        <el-form-item label="通道ID">
          <el-input v-model.number="form.channel_id" />
        </el-form-item>
        <el-form-item label="Key" prop="template_key">
          <el-input v-model="form.template_key" :disabled="!!form.id" />
        </el-form-item>
        <el-form-item label="名称" prop="name">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="标题模板">
          <el-input v-model="form.title_template" />
        </el-form-item>
        <el-form-item label="内容模板" prop="content_template">
          <el-input v-model="form.content_template" type="textarea" />
        </el-form-item>
        <el-form-item label="Payload模板">
          <el-input v-model="form.payloadStr" type="textarea" placeholder="可选 JSON" />
        </el-form-item>
        <el-form-item label="默认">
          <el-switch v-model="form.is_default" />
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
import { listTemplates, createTemplate, updateTemplate } from '../api'

const items = ref([])
const meta = reactive({ total: 0, page: 1, page_size: 20 })
const visible = ref(false)
const formRef = ref()
const form = reactive({
  id: null,
  app_id: null,
  channel_id: null,
  template_key: '',
  name: '',
  title_template: '',
  content_template: '',
  payloadStr: '',
  is_default: false,
})
const rules = {
  app_id: [{ required: true, message: '请输入AppID', trigger: 'blur' }],
  template_key: [{ required: true, message: '请输入模板Key', trigger: 'blur' }],
  name: [{ required: true, message: '请输入模板名称', trigger: 'blur' }],
  content_template: [{ required: true, message: '请输入内容模板', trigger: 'blur' }],
}

const fetchData = async () => {
  const res = await listTemplates({ page: meta.page, page_size: meta.page_size })
  items.value = res.items
  Object.assign(meta, res.meta)
}

const openForm = (row = null) => {
  visible.value = true
  formRef.value?.clearValidate()
  if (row) {
    Object.assign(form, {
      ...row,
      payloadStr: row.payload_template ? JSON.stringify(row.payload_template) : '',
    })
  } else {
    Object.assign(form, {
      id: null,
      app_id: null,
      channel_id: null,
      template_key: '',
      name: '',
      title_template: '',
      content_template: '',
      payloadStr: '',
      is_default: false,
    })
  }
}

const parsePayload = () => {
  if (!form.payloadStr) return null
  try {
    return JSON.parse(form.payloadStr)
  } catch (e) {
    ElMessage.error('Payload 必须是合法 JSON')
    throw e
  }
}

const save = async () => {
  try {
    await formRef.value.validate()
    const payload = {
      app_id: form.app_id,
      channel_id: form.channel_id,
      template_key: form.template_key,
      name: form.name,
      title_template: form.title_template,
      content_template: form.content_template,
      payload_template: parsePayload(),
      is_default: form.is_default,
    }
    if (form.id) {
      await updateTemplate(form.id, payload)
    } else {
      await createTemplate(payload)
    }
    ElMessage.success('保存成功')
    visible.value = false
    fetchData()
  } catch (err) {
    if (!err.response) return
    ElMessage.error(err.response?.data?.detail || '保存失败')
  }
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
