<template>
  <el-card>
    <el-form ref="formRef" :model="form" :rules="rules" label-width="120px">
      <el-form-item label="AppID" prop="app_id">
        <el-input v-model.number="form.app_id" />
      </el-form-item>
      <el-form-item label="通道ID" prop="channel_id">
        <el-input v-model.number="form.channel_id" />
      </el-form-item>
      <el-form-item label="消息类型ID" prop="message_type_id">
        <el-input v-model.number="form.message_type_id" />
      </el-form-item>
      <el-form-item label="标题">
        <el-input v-model="form.title" />
      </el-form-item>
      <el-form-item label="内容" prop="content">
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
      <el-form-item label="X-App-Secret" prop="app_secret">
        <el-input v-model="form.app_secret" />
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
  app_secret: '',
})
const payloadStr = ref('')
const result = ref(null)
const loading = ref(false)
const formRef = ref()
const rules = {
  app_id: [{ required: true, message: '请输入AppID', trigger: 'blur' }],
  channel_id: [{ required: true, message: '请输入通道ID', trigger: 'blur' }],
  message_type_id: [{ required: true, message: '请输入消息类型ID', trigger: 'blur' }],
  content: [{ required: true, message: '请输入内容', trigger: 'blur' }],
  app_secret: [{ required: true, message: '请输入X-App-Secret', trigger: 'blur' }],
}

const send = async () => {
  loading.value = true
  try {
    await formRef.value.validate()
    const payload = { ...form, payload: payloadStr.value ? JSON.parse(payloadStr.value) : null }
    const res = await sendMessage(payload, form.app_secret)
    result.value = res
    ElMessage.success('发送成功')
  } catch (err) {
    if (err instanceof SyntaxError) {
      ElMessage.error('Payload 必须是合法 JSON')
    } else {
      ElMessage.error(err.response?.data?.detail || err.msg || '发送失败')
    }
  } finally {
    loading.value = false
  }
}
</script>
