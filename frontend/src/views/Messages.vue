<template>
  <el-card>
    <el-form :inline="true" :model="filters" class="toolbar">
      <el-form-item label="AppID">
        <el-input v-model="filters.app_id" style="width: 120px" />
      </el-form-item>
      <el-form-item label="通道ID">
        <el-input v-model="filters.channel_id" style="width: 120px" />
      </el-form-item>
      <el-button type="primary" @click="fetchData">查询</el-button>
    </el-form>

    <el-table :data="items">
      <el-table-column prop="id" label="ID" width="70" />
      <el-table-column prop="app_id" label="AppID" width="80" />
      <el-table-column prop="channel_id" label="通道ID" />
      <el-table-column prop="message_type_id" label="类型ID" />
      <el-table-column prop="title" label="标题" />
      <el-table-column prop="priority" label="优先级" width="80" />
      <el-table-column prop="status" label="状态" width="80" />
      <el-table-column prop="created_at" label="创建时间" />
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
import { listMessages } from '../api'

const items = ref([])
const meta = reactive({ total: 0, page: 1, page_size: 20 })
const filters = reactive({ app_id: '', channel_id: '' })

const fetchData = async () => {
  const params = { page: meta.page, page_size: meta.page_size }
  if (filters.app_id) params.app_id = filters.app_id
  if (filters.channel_id) params.channel_id = filters.channel_id
  const res = await listMessages(params)
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
