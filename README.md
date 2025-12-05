# 消息中台（FastAPI + Vue）说明（更新：2025-12-05）

## 架构与技术栈
- 后端：FastAPI（Python 3.12）、SQLAlchemy(异步) + MySQL 8、Redis Pub/Sub、JWT 认证、bcrypt 密码哈希。
- 前端：Vue 3 + Vite + Element Plus，Pinia 状态管理，Axios 封装。
- 部署：uvicorn（可 --reload 开发模式），可选单独消费者进程处理推送/重试。
- 统一返回格式：`{"code":1,"msg":"ok","data":...}`；失败 `{"code":0,"msg":"错误", "data":null}`。

## 功能概览
- 管理端：登录、管理员/角色、业务系统、通道、消息类型、通道-类型映射、模板、业务用户映射、订阅管理（均分页）。
- 业务接口：消息发送（校验 App Secret，入库+投递+发布 Redis）、消息/投递查询。
- WebSocket：`/ws` 连接（user_id/instance_id），补发未送达，ACK 更新投递状态。
- 消费者：订阅 Redis，向在线用户推送并重试未送达/失败投递。

## 目录
- 后端：`app/`（FastAPI）、`message_center_schema.sql`（表结构）
- 前端：`frontend/`（Vue3 + Element Plus + Vite）

## 环境与配置
1) Python 3.12（推荐 conda/venv），Node.js 18+。  
2) `.env` 示例（已提供）：  
```
mysql_dsn="mysql+asyncmy://root:root@localhost:3306/message_center?charset=utf8mb4"
redis_url="redis://localhost:6379/0"
jwt_secret_key="change-me-secret"
```
3) 初始化数据库：执行 `message_center_schema.sql`。  
4) 创建后台账号：手工插入 `mc_admin_user`，密码用 bcrypt hash（例 admin/admin 的 hash `$2b$12$oaobiIPoFhjcLJexAUgyce4luAWJ53iXoG10PzL/.sjoNVxjBkt7W`）。

## 启动后端
```bash
conda activate msg-center  # 或 source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 9000 --reload
# Redis 消费者（推送/重试，可选）：python -m app.workers.message_consumer
```

## 启动前端
```bash
cd frontend
npm install
npm run dev  # 默认 http://localhost:5173，API 默认 http://localhost:9000
```

##前后端地址

- 后端：http://0.0.0.0:9000（已启用统一返回格式）
- 前端：http://localhost:5173（默认 API 指向 9000，可在 .env 调整）

## 接口速览
- 登录：`POST /api/v1/admin/auth/login` -> `{"code":1,"data":{"access_token":...}}`
- 管理端 CRUD：`/api/v1/admin/roles|apps|channels|message-types|channel-message-types|templates|subscriptions|users-mapping`（分页 `page/page_size`）
- 消息：`POST /api/v1/messages`（Header `X-App-Secret`），`GET /api/v1/messages`，`GET /api/v1/messages/deliveries`
- 实例心跳：`POST /api/v1/instances/heartbeat`
- WebSocket：`/ws?user_id=...&instance_id=...`，ACK `{"delivery_id":x,"status":2}`

## 返回格式约定
- 成功：`{"code":1,"msg":"ok","data":...}`
- 失败：`{"code":0,"msg":"错误描述","data":null}`（HTTP 状态码按场景返回 4xx/5xx）

## 数据表（示例）
- mc_admin_user / mc_admin_role / mc_admin_user_role
- mc_app / mc_user / mc_channel / mc_message_type / mc_channel_message_type
- mc_message_template / mc_subscription / mc_message / mc_message_delivery
- mc_instance / mc_client_connection

## 备注
- Alembic 迁移未生成；当前通过 SQL 初始化，后续可基于 `app.db.base.Base` 补迁移。
- WebSocket 安全未加 token 校验，如需可按需增强。
