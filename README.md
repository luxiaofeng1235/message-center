"""
Message Center 后端说明
更新日期: 2025-12-05
"""

# 启动步骤
1. 安装依赖：`pip install -r requirements.txt`
2. 初始化数据库：执行 `message_center_schema.sql`（当前去除外键，包含 DROP TABLE IF EXISTS）
3. 启动 API：`uvicorn app.main:app --reload`（默认端口 8000）
4. 启动 Redis 消费者（可选，处理实时推送）：`python -m app.workers.message_consumer`

# 配置
- 通过 `.env` 设置 `mysql_dsn`、`redis_url`、`jwt_secret_key` 等，详见 `app/core/config.py`
- App 调用时在 Header 中携带 `X-App-Secret` 用于校验调用方

# 管理端接口
- 登录：`POST /api/v1/admin/auth/login`
- 管理员/角色/应用/通道/消息类型/模板/订阅/业务用户：`/api/v1/admin/...` 系列，均支持分页参数 `page`、`page_size`

# 业务接口
- 发送消息：`POST /api/v1/messages`（Header: `X-App-Secret`），会入库、生成投递、发布 Redis
- 查询消息：`GET /api/v1/messages`
- 查询投递：`GET /api/v1/messages/deliveries`

# WebSocket
- 连接：`/ws?user_id=...&client_id=...&instance_id=...`，连接后收到消息时可回传 `{"delivery_id": ..., "status": 2}` 作为 ACK

# Alembic
- 尚未生成迁移文件，可后续通过 `alembic init alembic` 并在 `env.py` 中使用 `app.db.base.Base` 注册模型；当前可直接导入 SQL 脚本。
