<template>
  <el-card>
    <el-form :inline="true" :model="filters" class="toolbar">
      <el-form-item label="用户ID">
        <el-input v-model="filters.user_id" style="width: 120px" />
      </el-form-item>
      <el-form-item label="状态">
        <el-select v-model="filters.status" style="width: 140px" clearable>
          <el-option :value="0" label="待发送" />
          <el-option :value="1" label="已推送" />
          <el-option :value="2" label="已确认" />
          <el-option :value="3" label="失败" />
          <el-option :value="4" label="过期" />
        </el-select>
      </el-form-item>
      <el-button type="primary" @click="fetchData">查询</el-button>
    </el-form>

    <el-table :data="items">
      <el-table-column prop="id" label="ID" width="70" />
      <el-table-column prop="message_id" label="消息ID" />
      <el-table-column prop="user_id" label="用户ID" />
      <el-table-column prop="status" label="状态" />
      <el-table-column prop="retry_count" label="重试" width="80" />
      <el-table-column prop="last_error" label="错误" />
      <el-table-column prop="created_at" label="创建" />
      <el-table-column prop="sent_at" label="发送" />
      <el-table-column prop="ack_at" label="确认" />
    </el-table>
    <el-pagination
      class="mt"
      layout="prev, pager, next"
      :total="meta.total"
      :page-size="meta.page_size"
      @current-change="pageChange"
    />
  </el-card>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue'
import { listDeliveries } from '../api'

const items = ref([])
const meta = reactive({ total: 0, page: 1, page_size: 20 })
const filters = reactive({ user_id: '', status: '' })

const fetchData = async () => {
  const params = { page: meta.page, page_size: meta.page_size }
  if (filters.user_id) params.user_id = filters.user_id
  if (filters.status !== '') params.status = filters.status
  const res = await listDeliveries(params)
  items.value = res.items
  Object.assign(meta, res.meta)
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
