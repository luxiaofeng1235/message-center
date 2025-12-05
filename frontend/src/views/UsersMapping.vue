<template>
  <el-card>
    <div class="toolbar">
      <el-button type="primary" @click="openForm()">新增业务用户</el-button>
    </div>
    <el-table :data="items">
      <el-table-column prop="id" label="ID" width="70" />
      <el-table-column prop="app_id" label="AppID" />
      <el-table-column prop="external_user_id" label="外部用户ID" />
      <el-table-column prop="nickname" label="昵称" />
    </el-table>
    <el-pagination
      class="mt"
      layout="prev, pager, next"
      :total="meta.total"
      :page-size="meta.page_size"
      @current-change="pageChange"
    />

    <el-dialog v-model="visible" title="业务用户">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="90px">
        <el-form-item label="AppID" prop="app_id">
          <el-input v-model.number="form.app_id" />
        </el-form-item>
        <el-form-item label="外部用户ID" prop="external_user_id">
          <el-input v-model="form.external_user_id" />
        </el-form-item>
        <el-form-item label="昵称">
          <el-input v-model="form.nickname" />
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
import { listUsers, createUser } from '../api'

const items = ref([])
const meta = reactive({ total: 0, page: 1, page_size: 20 })
const visible = ref(false)
const formRef = ref()
const form = reactive({
  id: null,
  app_id: null,
  external_user_id: '',
  nickname: '',
})
const rules = {
  app_id: [{ required: true, message: '请输入AppID', trigger: 'blur' }],
  external_user_id: [{ required: true, message: '请输入外部用户ID', trigger: 'blur' }],
}

const fetchData = async () => {
  const res = await listUsers({ page: meta.page, page_size: meta.page_size })
  items.value = res.items
  Object.assign(meta, res.meta)
}

const openForm = (row = null) => {
  visible.value = true
  formRef.value?.clearValidate()
  if (row) {
    Object.assign(form, row)
  } else {
    Object.assign(form, { id: null, app_id: null, external_user_id: '', nickname: '' })
  }
}

const save = async () => {
  try {
    await formRef.value.validate()
    await createUser(form)
    ElMessage.success('保存成功')
    visible.value = false
    fetchData()
  } catch (err) {
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
