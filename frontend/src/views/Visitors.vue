<template>
  <el-card>
    <div class="toolbar">
      <el-form :inline="true" :model="filters" class="filters">
        <el-form-item label="业务系统">
          <el-select v-model="filters.app_id" clearable placeholder="全部">
            <el-option v-for="app in appOptions" :key="app.id" :label="app.name" :value="app.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="角色">
          <el-select v-model="filters.role" clearable placeholder="全部">
            <el-option label="admin" value="admin" />
            <el-option label="visitor" value="visitor" />
          </el-select>
        </el-form-item>
        <el-form-item label="时间范围">
          <el-date-picker
            v-model="filters.range"
            type="datetimerange"
            start-placeholder="开始时间"
            end-placeholder="结束时间"
            value-format="YYYY-MM-DDTHH:mm:ssZ"
          />
        </el-form-item>
        <el-form-item label="条数">
          <el-input-number v-model="filters.limit" :min="10" :max="1000" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="fetchData" :loading="loading">查询</el-button>
          <el-button @click="resetFilters">重置</el-button>
        </el-form-item>
      </el-form>
    </div>
    <el-table :data="items" v-loading="loading" size="small" :border="false">
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="user_id" label="用户ID" width="100" />
      <el-table-column prop="app_id" label="AppID" width="90" />
      <el-table-column prop="role" label="角色" width="90" />
      <el-table-column label="在线" width="90">
        <template #default="{ row }">
          <el-tag :type="row.disconnected_at ? 'info' : 'success'">
            {{ row.disconnected_at ? '离线' : '在线' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="client_id" label="ClientID" min-width="140" show-overflow-tooltip />
      <el-table-column prop="token" label="Token" min-width="160" show-overflow-tooltip />
      <el-table-column prop="ip" label="IP" width="130" />
      <el-table-column prop="user_agent" label="UA" min-width="200" show-overflow-tooltip />
      <el-table-column prop="connected_at" label="上线时间" min-width="170" />
      <el-table-column prop="last_active_at" label="最后活跃" min-width="170" />
      <el-table-column prop="disconnected_at" label="下线时间" min-width="170" />
    </el-table>
  </el-card>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { listVisitors, listApps } from '../api'

const loading = ref(false)
const items = ref([])
const appOptions = ref([])

const filters = ref({
  app_id: null,
  role: '',
  range: [],
  limit: 200,
})

const resetFilters = () => {
  filters.value = { app_id: null, role: '', range: [], limit: 200 }
  fetchData()
}

const fetchApps = async () => {
  try {
    const { data } = await listApps({ page: 1, page_size: 1000 })
    appOptions.value = data.items || []
  } catch (err) {
    console.error(err)
  }
}

const fetchData = async () => {
  loading.value = true
  try {
    const params = {
      limit: filters.value.limit,
    }
    if (filters.value.app_id) params.app_id = filters.value.app_id
    if (filters.value.role) params.role = filters.value.role
    if (filters.value.range && filters.value.range.length === 2) {
      params.start_time = filters.value.range[0]
      params.end_time = filters.value.range[1]
    }
    const { data } = await listVisitors(params)
    items.value = data || []
  } catch (err) {
    ElMessage.error(err.response?.data?.detail || '查询失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchApps()
  fetchData()
})
</script>

<style scoped>
.toolbar {
  margin-bottom: 12px;
}
.filters :deep(.el-form-item) {
  margin-right: 12px;
  margin-bottom: 8px;
}
</style>
