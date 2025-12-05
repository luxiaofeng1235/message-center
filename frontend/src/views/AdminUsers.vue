<template>
  <el-card>
    <div class="toolbar">
      <el-button type="primary" @click="openForm()">新增管理员</el-button>
    </div>
    <el-table :data="items" style="width: 100%">
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="username" label="用户名" />
      <el-table-column prop="display_name" label="名称" />
      <el-table-column prop="is_super" label="超级">
        <template #default="scope">
          <el-tag v-if="scope.row.is_super" type="success">是</el-tag>
          <el-tag v-else type="info">否</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="is_active" label="启用">
        <template #default="scope">
          <el-switch v-model="scope.row.is_active" @change="toggleActive(scope.row)" />
        </template>
      </el-table-column>
      <el-table-column label="操作" width="160">
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

    <el-dialog v-model="visible" title="管理员">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username" :disabled="!!form.id" />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="form.password" type="password" autocomplete="new-password" />
        </el-form-item>
        <el-form-item label="名称">
          <el-input v-model="form.display_name" />
        </el-form-item>
        <el-form-item label="手机号">
          <el-input v-model="form.phone" />
        </el-form-item>
        <el-form-item label="超级">
          <el-switch v-model="form.is_super" :disabled="!auth.user?.is_super || form.id === auth.user?.id" />
        </el-form-item>
        <el-form-item label="启用">
          <el-switch v-model="form.is_active" :disabled="form.id === auth.user?.id || !auth.user?.is_super" />
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
import { listAdminUsers, createAdminUser, updateAdminUser } from '../api'
import { useAuthStore } from '../stores/auth'

const items = ref([])
const meta = reactive({ total: 0, page: 1, page_size: 20 })
const visible = ref(false)
const formRef = ref()
const form = reactive({
  id: null,
  username: '',
  password: '',
  display_name: '',
  phone: '',
  is_super: false,
  is_active: true,
})
const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [
    {
      trigger: 'blur',
      validator: (_, value, cb) => {
        if (!form.id && !value) return cb(new Error('请输入密码'))
        cb()
      },
    },
  ],
}
const auth = useAuthStore()

const fetchData = async () => {
  const res = await listAdminUsers({ page: meta.page, page_size: meta.page_size })
  items.value = res.items
  Object.assign(meta, res.meta)
}

const openForm = (row = null) => {
  visible.value = true
  formRef.value?.clearValidate()
  if (row) {
    Object.assign(form, { ...row, password: '' })
  } else {
    Object.assign(form, {
      id: null,
      username: '',
      password: '',
      display_name: '',
      phone: '',
      is_super: false,
      is_active: true,
    })
  }
}

const save = async () => {
  try {
    await formRef.value.validate()
    const payload = { ...form }
    if (payload.id && !payload.password) delete payload.password
    if (payload.id) await updateAdminUser(payload.id, payload)
    else await createAdminUser(payload)
    ElMessage.success('保存成功')
    visible.value = false
    fetchData()
  } catch (err) {
    if (err?.msg || err?.detail) {
      ElMessage.error(err.msg || err.detail)
    } else {
      ElMessage.error(err.response?.data?.detail || err.message || '保存失败')
    }
  }
}

const toggleActive = async (row) => {
  if (row.id === auth.user?.id || !auth.user?.is_super) {
    row.is_active = !row.is_active
    return
  }
  await updateAdminUser(row.id, { is_active: row.is_active })
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
