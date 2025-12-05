<template>
  <el-card>
    <el-form :model="form" label-width="120px">
      <el-form-item label="AppID">
        <el-input v-model.number="form.app_id" />
      </el-form-item>
      <el-form-item label="通道ID">
        <el-input v-model.number="form.channel_id" />
      </el-form-item>
      <el-form-item label="消息类型ID">
        <el-input v-model.number="form.message_type_id" />
      </el-form-item>
      <el-form-item label="标题">
        <el-input v-model="form.title" />
      </el-form-item>
      <el-form-item label="内容">
        <el-input type="textarea" v-model="form.content" />
      </el-form-item>
      <el-form-item label="Payload(JSON)">
        <el-input type="textarea" v-model="payloadStr" placeholder='{"foo":"bar"}' />
      </el-form-item>
      <el-form-item label="优先级">
        <el-input v-model.number="form.priority" />
      </el-form-item>
      <el-form-item label="MessageKey(可选)">
        <el-input v-model="form.message_key" />
      </el-form-item>
      <el-form-item label="X-App-Secret">
        <el-input v-model="appSecret" />
      </el-form-item>
      <el-button type="primary" @click="send" :loading="loading">发送</el-button>
    </el-form>
    <el-divider />
    <div v-if="result">
      <p>发送结果：ID {{ result.id }}，状态 {{ result.status }}，创建时间 {{ result.created_at }}</p>
    </div>
  </el-card>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { sendMessage } from '../api'

const form = reactive({
  app_id: null,
  channel_id: null,
  message_type_id: null,
  title: '',
  content: '',
  priority: 0,
  message_key: '',
})
const payloadStr = ref('')
const appSecret = ref('')
const result = ref(null)
const loading = ref(false)

const send = async () => {
  loading.value = true
  try {
    const payload = { ...form, payload: payloadStr.value ? JSON.parse(payloadStr.value) : null }
    const { data } = await sendMessage(payload, appSecret.value)
    result.value = data
    ElMessage.success('发送成功')
  } catch (err) {
    ElMessage.error(err.response?.data?.detail || '发送失败')
  } finally {
    loading.value = false
  }
}
</script>
