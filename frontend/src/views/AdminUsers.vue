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
      <el-form :model="form" label-width="80px">
        <el-form-item label="用户名">
          <el-input v-model="form.username" :disabled="!!form.id" />
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="form.password" type="password" />
        </el-form-item>
        <el-form-item label="名称">
          <el-input v-model="form.display_name" />
        </el-form-item>
        <el-form-item label="手机号">
          <el-input v-model="form.phone" />
        </el-form-item>
        <el-form-item label="超级">
          <el-switch v-model="form.is_super" />
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
import { listAdminUsers, createAdminUser, updateAdminUser } from '../api'

const items = ref([])
const meta = reactive({ total: 0, page: 1, page_size: 20 })
const visible = ref(false)
const form = reactive({
  id: null,
  username: '',
  password: '',
  display_name: '',
  phone: '',
  is_super: false,
  is_active: true,
})

const fetchData = async () => {
  const { data } = await listAdminUsers({ page: meta.page, page_size: meta.page_size })
  items.value = data.items
  Object.assign(meta, data.meta)
}

const openForm = (row = null) => {
  visible.value = true
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
    if (form.id) {
      await updateAdminUser(form.id, form)
    } else {
      await createAdminUser(form)
    }
    ElMessage.success('保存成功')
    visible.value = false
    fetchData()
  } catch (err) {
    ElMessage.error(err.response?.data?.detail || '保存失败')
  }
}

const toggleActive = async (row) => {
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
