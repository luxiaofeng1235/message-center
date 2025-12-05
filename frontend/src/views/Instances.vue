<template>
  <el-card>
    <div class="toolbar">
      <el-button type="primary" @click="sendHeartbeat">发送心跳</el-button>
    </div>
    <el-table :data="items">
      <el-table-column prop="id" label="ID" width="70" />
      <el-table-column prop="instance_key" label="实例Key" />
      <el-table-column prop="host" label="主机" />
      <el-table-column prop="pid" label="PID" width="90" />
      <el-table-column prop="is_active" label="活跃">
        <template #default="scope">
          <el-tag v-if="scope.row.is_active" type="success">是</el-tag>
          <el-tag v-else type="info">否</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="started_at" label="启动时间" />
      <el-table-column prop="last_heartbeat" label="最近心跳" />
    </el-table>
  </el-card>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { heartbeat } from '../api'

const items = ref([])

const fetchData = async () => {
  // 后端未提供列表接口，暂不展示现有实例
  items.value = []
}

const sendHeartbeat = async () => {
  try {
    const payload = {
      instance_key: `frontend-${Date.now()}`,
      host: window.location.hostname,
      pid: Math.floor(Math.random() * 10000),
    }
    const { data } = await heartbeat(payload)
    ElMessage.success('心跳已发送')
    items.value = [data, ...items.value]
  } catch (err) {
    ElMessage.error(err.response?.data?.detail || '发送失败')
  }
}

onMounted(fetchData)
</script>

<style scoped>
.toolbar {
  margin-bottom: 12px;
}
</style>
