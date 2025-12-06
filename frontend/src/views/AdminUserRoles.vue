<template>
  <el-card>
    <div class="toolbar">
      <el-button type="primary" @click="openForm()">新增绑定</el-button>
    </div>
    <el-table :data="items">
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="user_id" label="用户ID" />
      <el-table-column prop="role_id" label="角色ID" />
      <el-table-column label="操作" width="120">
        <template #default="scope">
          <el-button size="small" type="danger" @click="remove(scope.row.id)">删除</el-button>
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

    <el-dialog v-model="visible" title="绑定角色">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="90px">
        <el-form-item label="用户ID" prop="user_id">
          <el-input v-model.number="form.user_id" />
        </el-form-item>
        <el-form-item label="角色ID" prop="role_id">
          <el-input v-model.number="form.role_id" />
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
import { ElMessage, ElMessageBox } from 'element-plus'
import { listAdminUserRoles, createAdminUserRole, deleteAdminUserRole } from '../api'

const items = ref([])
const meta = reactive({ total: 0, page: 1, page_size: 20 })
const visible = ref(false)
const formRef = ref()
const form = reactive({
  user_id: null,
  role_id: null,
})
const rules = {
  user_id: [{ required: true, message: '请输入用户ID', trigger: 'blur' }],
  role_id: [{ required: true, message: '请输入角色ID', trigger: 'blur' }],
}

const fetchData = async () => {
  const res = await listAdminUserRoles({ page: meta.page, page_size: meta.page_size })
  items.value = res.items
  Object.assign(meta, res.meta)
}

const openForm = () => {
  visible.value = true
  formRef.value?.clearValidate()
  Object.assign(form, { user_id: null, role_id: null })
}

const save = async () => {
  try {
    await formRef.value.validate()
    await createAdminUserRole(form)
    ElMessage.success('保存成功')
    visible.value = false
    fetchData()
  } catch (err) {
    if (!err?.response && err?.name === 'Error' && !err?.msg) return
    ElMessage.error(err.response?.data?.detail || '保存失败')
  }
}

const remove = async (id) => {
  try {
    await ElMessageBox.confirm('确认删除该绑定吗？', '提示', { type: 'warning' })
    await deleteAdminUserRole(id)
    ElMessage.success('删除成功')
    fetchData()
  } catch (err) {
    if (err !== 'cancel') {
      ElMessage.error(err?.response?.data?.detail || '删除失败')
    }
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
