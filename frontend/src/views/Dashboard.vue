<template>
  <el-card>
    <h3 class="title">欢迎使用消息中台后台</h3>
    <el-descriptions :column="2" border>
      <el-descriptions-item label="当前时间">{{ now }}</el-descriptions-item>
      <el-descriptions-item label="操作系统">{{ osInfo || '-' }}</el-descriptions-item>
      <el-descriptions-item label="当前登录IP">{{ ip || '-' }}</el-descriptions-item>
      <el-descriptions-item label="管理员账号">{{ auth.user?.username || '-' }}</el-descriptions-item>
    </el-descriptions>
  </el-card>
</template>

<script setup>
import { onMounted, onUnmounted, ref } from 'vue'
import { useAuthStore } from '../stores/auth'
import api from '../api/http'

const auth = useAuthStore()
const now = ref('')
const osInfo = ref('')
const ip = ref('')
let timer = null

const updateTime = () => {
  now.value = new Date().toLocaleString()
}

onMounted(async () => {
  updateTime()
  timer = setInterval(updateTime, 1000)
  try {
    const data = await api.get('/api/v1/health')
    osInfo.value = data.os || ''
    ip.value = data.ip || ''
  } catch (e) {
    osInfo.value = ''
    ip.value = ''
  }
})

onUnmounted(() => {
  if (timer) clearInterval(timer)
})
</script>

<style scoped>
.title {
  margin-bottom: 12px;
}
</style>
