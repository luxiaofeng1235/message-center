<template>
  <div class="login-container">
    <div class="left-panel">
      <div class="brand">
        <div class="logo">MC</div>
        <div>
          <h1>消息中台管理</h1>
          <p>统一接入 · 实时推送 · 可靠投递</p>
        </div>
      </div>
      <ul class="features">
        <li><el-icon><ChatDotRound /></el-icon><span>多业务系统接入</span></li>
        <li><el-icon><Share /></el-icon><span>Redis Pub/Sub 实时分发</span></li>
        <li><el-icon><Bell /></el-icon><span>WebSocket 推送与投递跟踪</span></li>
      </ul>
    </div>
    <div class="form-panel">
      <h2>欢迎登录</h2>
      <p class="subtitle">请使用管理员账号登录后台</p>
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        @submit.prevent="onSubmit"
        label-position="top"
        class="form"
      >
        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username" size="large" autocomplete="username" />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="form.password" size="large" type="password" autocomplete="current-password" />
        </el-form-item>
        <el-button type="primary" size="large" @click="onSubmit" :loading="loading" class="full-btn">登录</el-button>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { ChatDotRound, Share, Bell } from '@element-plus/icons-vue'
import { login, getProfile } from '../api'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const auth = useAuthStore()
const loading = ref(false)
const formRef = ref()
const form = reactive({
  username: '',
  password: '',
})
const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
}

const onSubmit = async () => {
  loading.value = true
  try {
    await formRef.value.validate()
    // 先登录拿 token，再带 token 获取个人信息
    const data = await login(form)
    auth.setAuth(data.access_token, null) // 先写入 token，让后续请求带上 Authorization
    const profile = await getProfile()
    auth.setAuth(data.access_token, profile)
    router.push('/')
  } catch (err) {
    const msg = err?.msg || err?.response?.data?.detail || err?.detail || '登录失败'
    ElMessage.error(msg)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  display: grid;
  grid-template-columns: 1.1fr 1fr;
  height: 100vh;
  background: linear-gradient(135deg, #1f7ae0, #62b0ff);
  color: #fff;
}
.left-panel {
  padding: 80px 60px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 32px;
}
.brand {
  display: flex;
  align-items: center;
  gap: 16px;
}
.logo {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.18);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 22px;
}
.brand h1 {
  margin: 0;
}
.brand p {
  margin: 4px 0 0;
  opacity: 0.9;
}
.features {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.features li {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 15px;
}
.form-panel {
  background: #fff;
  color: #333;
  border-radius: 16px 0 0 16px;
  padding: 60px 70px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  box-shadow: -8px 0 30px rgba(0, 0, 0, 0.08);
}
.subtitle {
  color: #888;
  margin-top: 6px;
  margin-bottom: 28px;
}
.form {
  width: 100%;
}
.full-btn {
  width: 100%;
  margin-top: 8px;
}
@media (max-width: 900px) {
  .login-container {
    grid-template-columns: 1fr;
  }
  .left-panel {
    display: none;
  }
  .form-panel {
    border-radius: 0;
  }
}
</style>
