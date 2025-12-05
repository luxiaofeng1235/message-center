<template>
  <el-card>
    <div class="toolbar">
      <el-button type="primary" @click="openForm()">新增订阅</el-button>
    </div>
    <el-table :data="items">
      <el-table-column prop="id" label="ID" width="70" />
      <el-table-column prop="user_id" label="用户ID" />
      <el-table-column prop="channel_id" label="通道ID" />
      <el-table-column prop="message_type_id" label="类型ID" />
      <el-table-column prop="is_active" label="启用">
        <template #default="scope">
          <el-switch v-model="scope.row.is_active" @change="toggleActive(scope.row)" />
        </template>
      </el-table-column>
      <el-table-column prop="source" label="来源" />
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

    <el-dialog v-model="visible" title="订阅">
      <el-form :model="form" label-width="90px">
        <el-form-item label="用户ID">
          <el-input v-model.number="form.user_id" />
        </el-form-item>
        <el-form-item label="通道ID">
          <el-input v-model.number="form.channel_id" />
        </el-form-item>
        <el-form-item label="类型ID">
          <el-input v-model.number="form.message_type_id" />
        </el-form-item>
        <el-form-item label="来源">
          <el-input v-model="form.source" />
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
import { listSubscriptions, createSubscription, updateSubscription } from '../api'

const items = ref([])
const meta = reactive({ total: 0, page: 1, page_size: 20 })
const visible = ref(false)
const form = reactive({
  id: null,
  user_id: null,
  channel_id: null,
  message_type_id: null,
  source: '1',
  is_active: true,
})

const fetchData = async () => {
  const res = await listSubscriptions({ page: meta.page, page_size: meta.page_size })
  items.value = res.items
  Object.assign(meta, res.meta)
}

const openForm = (row = null) => {
  visible.value = true
  if (row) {
    Object.assign(form, row)
  } else {
    Object.assign(form, { id: null, user_id: null, channel_id: null, message_type_id: null, source: '1', is_active: true })
  }
}

const save = async () => {
  try {
    if (form.id) {
      await updateSubscription(form.id, form)
    } else {
      await createSubscription(form)
    }
    ElMessage.success('保存成功')
    visible.value = false
    fetchData()
  } catch (err) {
    ElMessage.error(err.response?.data?.detail || '保存失败')
  }
}

const toggleActive = async (row) => {
  await updateSubscription(row.id, { is_active: row.is_active })
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
