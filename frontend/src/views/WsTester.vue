<template>
  <el-card>
    <el-form :inline="true" :model="form" class="toolbar">
      <el-form-item label="WS 地址">
        <el-input v-model="form.url" style="width: 320px" placeholder="ws://localhost:8000/ws" />
      </el-form-item>
      <el-form-item label="用户ID">
        <el-input v-model="form.user_id" style="width: 120px" />
      </el-form-item>
      <el-form-item label="实例ID">
        <el-input v-model="form.instance_id" style="width: 120px" />
      </el-form-item>
      <el-form-item label="ClientID">
        <el-input v-model="form.client_id" style="width: 120px" />
      </el-form-item>
      <el-button type="primary" @click="connect" :disabled="connected">连接</el-button>
      <el-button @click="close" :disabled="!connected">断开</el-button>
    </el-form>
    <el-input v-model="ackJson" type="textarea" rows="3" placeholder='{"delivery_id":1,"status":2}' />
    <el-button class="mt" type="primary" @click="sendAck" :disabled="!connected">发送 ACK</el-button>

    <el-divider />
    <div class="log">
      <p v-for="(l, idx) in logs" :key="idx">{{ l }}</p>
    </div>
  </el-card>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'

const form = reactive({
  url: 'ws://localhost:8000/ws',
  user_id: '',
  instance_id: '',
  client_id: '',
})
const connected = ref(false)
const socket = ref(null)
const logs = ref([])
const ackJson = ref('{"delivery_id":1,"status":2}')

const log = (msg) => {
  logs.value.unshift(`${new Date().toLocaleTimeString()} - ${msg}`)
}

const connect = () => {
  if (!form.user_id || !form.instance_id) {
    ElMessage.error('user_id 和 instance_id 必填')
    return
  }
  const url = `${form.url}?user_id=${form.user_id}&instance_id=${form.instance_id}&client_id=${form.client_id}`
  socket.value = new WebSocket(url)
  socket.value.onopen = () => {
    connected.value = true
    log('WebSocket 连接已建立')
  }
  socket.value.onmessage = (evt) => {
    log(`收到: ${evt.data}`)
  }
  socket.value.onclose = () => {
    connected.value = false
    log('连接已关闭')
  }
  socket.value.onerror = (err) => {
    log(`错误: ${err.message || err}`)
  }
}

const close = () => {
  if (socket.value) {
    socket.value.close()
  }
}

const sendAck = () => {
  try {
    const data = JSON.parse(ackJson.value)
    socket.value?.send(JSON.stringify(data))
    log(`发送 ACK: ${ackJson.value}`)
  } catch {
    ElMessage.error('ACK 必须是合法 JSON')
  }
}
</script>

<style scoped>
.toolbar {
  margin-bottom: 12px;
}
.mt {
  margin-top: 8px;
}
.log {
  max-height: 300px;
  overflow-y: auto;
  background: #f7f7f7;
  padding: 8px;
}
</style>
