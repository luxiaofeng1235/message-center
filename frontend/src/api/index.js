import api from './http'

// Auth
export const login = (payload) => api.post('/api/v1/admin/auth/login', payload)
export const getProfile = () => api.get('/api/v1/admin/auth/me')
export const updateProfile = (payload) => api.put('/api/v1/admin/auth/profile', payload)

// Admin users
export const listAdminUsers = (params) => api.get('/api/v1/admin/users', { params })
export const createAdminUser = (payload) => api.post('/api/v1/admin/users', payload)
export const updateAdminUser = (id, payload) => api.put(`/api/v1/admin/users/${id}`, payload)
export const deactivateAdminUser = (id) => api.delete(`/api/v1/admin/users/${id}`)
export const uploadAdminAvatar = (formData) =>
  api.post('/api/v1/admin/users/avatar', formData, { headers: { 'Content-Type': 'multipart/form-data' } })

// Roles
export const listRoles = (params) => api.get('/api/v1/admin/roles', { params })
export const createRole = (payload) => api.post('/api/v1/admin/roles', payload)
export const updateRole = (id, payload) => api.put(`/api/v1/admin/roles/${id}`, payload)

// Apps
export const listApps = (params) => api.get('/api/v1/admin/apps', { params })
export const createApp = (payload) => api.post('/api/v1/admin/apps', payload)
export const updateApp = (id, payload) => api.put(`/api/v1/admin/apps/${id}`, payload)

// Channels
export const listChannels = (params) => api.get('/api/v1/admin/channels', { params })
export const createChannel = (payload) => api.post('/api/v1/admin/channels', payload)
export const updateChannel = (id, payload) => api.put(`/api/v1/admin/channels/${id}`, payload)

// Message Types
export const listMessageTypes = (params) => api.get('/api/v1/admin/message-types', { params })
export const createMessageType = (payload) => api.post('/api/v1/admin/message-types', payload)
export const updateMessageType = (id, payload) => api.put(`/api/v1/admin/message-types/${id}`, payload)

// Channel Message Types
export const listChannelMessageTypes = (params) => api.get('/api/v1/admin/channel-message-types', { params })
export const createChannelMessageType = (payload) => api.post('/api/v1/admin/channel-message-types', payload)
export const updateChannelMessageType = (id, payload) =>
  api.put(`/api/v1/admin/channel-message-types/${id}`, payload)

// Templates
export const listTemplates = (params) => api.get('/api/v1/admin/templates', { params })
export const createTemplate = (payload) => api.post('/api/v1/admin/templates', payload)
export const updateTemplate = (id, payload) => api.put(`/api/v1/admin/templates/${id}`, payload)

// Subscriptions
export const listSubscriptions = (params) => api.get('/api/v1/admin/subscriptions', { params })
export const createSubscription = (payload) => api.post('/api/v1/admin/subscriptions', payload)
export const updateSubscription = (id, payload) => api.put(`/api/v1/admin/subscriptions/${id}`, payload)

// Users mapping
export const listUsers = (params) => api.get('/api/v1/admin/users-mapping', { params })
export const createUser = (payload) => api.post('/api/v1/admin/users-mapping', payload)

// Messages
export const listMessages = (params) => api.get('/api/v1/messages', { params })
export const listDeliveries = (params) => api.get('/api/v1/messages/deliveries', { params })

// Business send message (for测试)
export const sendMessage = (payload, appSecret) =>
  api.post('/api/v1/messages', payload, { headers: { 'X-App-Secret': appSecret } })

// Instances heartbeat
export const heartbeat = (payload) => api.post('/api/v1/instances/heartbeat', payload)
