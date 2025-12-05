import axios from 'axios'
import { useAuthStore } from '../stores/auth'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:9000',
  timeout: 10000,
})

api.interceptors.request.use((config) => {
  const auth = useAuthStore()
  if (auth.token) {
    config.headers.Authorization = `Bearer ${auth.token}`
  }
  // 确保最新 user 注入到请求配置（可用于后续条件展示）
  if (auth.user) {
    config.headers['X-Admin-User'] = auth.user.username || ''
  }
  return config
})

api.interceptors.response.use(
  (resp) => {
    const data = resp.data
    if (data && typeof data === 'object' && 'code' in data) {
      if (data.code === 1) {
        return data.data
      }
      return Promise.reject(data)
    }
    return resp
  },
  (error) => {
    const url = error?.config?.url || ''
    // 登录接口的 401 不触发登出重定向，交给页面处理
    if (url.includes('/api/v1/admin/auth/login')) {
      return Promise.reject(error.response?.data || error)
    }
    if (error.response && error.response.status === 401) {
      const auth = useAuthStore()
      auth.logout()
      window.location.href = '/login'
    }
    return Promise.reject(error.response?.data || error)
  }
)

export default api
