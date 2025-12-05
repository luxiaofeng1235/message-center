<template>
  <el-card>
    <div class="toolbar">
      <el-button type="primary" @click="openForm()">新增业务系统</el-button>
    </div>
    <el-table :data="items">
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="name" label="名称" />
      <el-table-column prop="code" label="编码" />
      <el-table-column prop="secret" label="密钥" />
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

    <el-dialog v-model="visible" title="业务系统">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="名称" prop="name">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="编码" prop="code">
          <el-input v-model="form.code" :disabled="!!form.id" />
        </el-form-item>
        <el-form-item label="密钥" prop="secret">
          <el-input v-model="form.secret" />
        </el-form-item>
        <el-form-item label="说明">
          <el-input v-model="form.description" />
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
import { listApps, createApp, updateApp } from '../api'

const items = ref([])
const meta = reactive({ total: 0, page: 1, page_size: 20 })
const visible = ref(false)
const formRef = ref()
const form = reactive({
  id: null,
  name: '',
  code: '',
  secret: '',
  description: '',
  is_active: true,
})
const rules = {
  name: [{ required: true, message: '请输入名称', trigger: 'blur' }],
  code: [{ required: true, message: '请输入编码', trigger: 'blur' }],
  secret: [{ required: true, message: '请输入密钥', trigger: 'blur' }],
}

const fetchData = async () => {
  const res = await listApps({ page: meta.page, page_size: meta.page_size })
  items.value = res.items
  Object.assign(meta, res.meta)
}

const openForm = (row = null) => {
  visible.value = true
  formRef.value?.clearValidate()
  if (row) {
    Object.assign(form, row)
  } else {
    Object.assign(form, { id: null, name: '', code: '', secret: '', description: '', is_active: true })
  }
}

const save = async () => {
  try {
    await formRef.value.validate()
    if (form.id) {
      await updateApp(form.id, form)
    } else {
      await createApp(form)
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
  await updateApp(row.id, { is_active: row.is_active })
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
