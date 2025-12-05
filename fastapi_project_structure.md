FastAPI 消息中台项目建议目录结构（手绘示意）

当前目录（message-center）
.
├── requirements.txt               # Python 依赖（pip install -r requirements.txt）
├── app/                             # 应用主代码
│   ├── main.py                      # FastAPI 入口（创建 app、挂载路由/中间件）
│   ├── core/                        # 核心配置 & 公共功能
│   │   ├── config.py                # 配置（数据库、Redis、JWT 等）
│   │   ├── security.py              # 登录、权限、RBAC 相关依赖
│   │   └── logging.py               # 日志配置
│   ├── db/                          # 数据库相关
│   │   ├── base.py                  # Base = declarative_base()，导入所有 models
│   │   ├── session.py               # async SessionLocal、依赖注入
│   │   └── init_db.py               # 初始化数据（创建超级管理员等）
│   ├── models/                      # SQLAlchemy ORM 模型（对应 SQL 表）
│   │   ├── admin.py                 # mc_admin_user / mc_admin_role / mc_admin_user_role
│   │   ├── app.py                   # mc_app
│   │   ├── user.py                  # mc_user
│   │   ├── channel.py               # mc_channel / mc_subscription / mc_message_template
│   │   ├── message.py               # mc_message / mc_message_delivery
│   │   ├── instance.py              # mc_instance
│   │   ├── client_connection.py     # mc_client_connection
│   │   └── __init__.py
│   ├── schemas/                     # Pydantic Schema（请求/响应模型）
│   │   ├── admin.py                 # 管理员、角色相关
│   │   ├── auth.py                  # 登录 / Token
│   │   ├── app.py                   # 项目配置
│   │   ├── channel.py               # 通道 & 订阅
│   │   ├── message.py               # 消息发送 / 消息模板 / 投递查询
│   │   └── __init__.py
│   ├── api/                         # 路由定义
│   │   ├── deps.py                  # 依赖（获取当前用户、权限校验等）
│   │   ├── v1/                      # REST 风格 HTTP 接口
│   │   │   ├── route_admin_auth.py          # 后台登录 / 刷新 Token
│   │   │   ├── route_admin_users.py         # 后台管理员管理
│   │   │   ├── route_admin_apps.py          # mc_app 管理
│   │   │   ├── route_admin_channels.py      # mc_channel 管理
│   │   │   ├── route_admin_templates.py     # mc_message_template 管理
│   │   │   ├── route_admin_subscriptions.py # mc_subscription 管理 / 查询
│   │   │   ├── route_messages.py            # 业务系统调用的消息发送接口
│   │   │   └── route_health.py              # 健康检查
│   │   └── websocket/               # WebSocket 相关路由
│   │       ├── connection_manager.py # 管理 user_id -> WebSocket 连接映射
│   │       └── routes.py            # /ws 连接入口，处理连接/断开/收发消息
│   ├── services/                    # 领域服务（业务逻辑）
│   │   ├── auth_service.py          # 登录验证、密码哈希、Token 生成
│   │   ├── message_service.py       # 消息持久化、生成 delivery、推送调度
│   │   ├── subscription_service.py  # 订阅管理逻辑
│   │   ├── template_service.py      # 模板渲染、默认消息逻辑
│   │   └── instance_service.py      # 实例注册、心跳上报
│   ├── workers/                     # 后台任务/消费者（可选）
│   │   └── message_consumer.py      # Redis Pub/Sub 消费、重试任务等
│   └── utils/                       # 工具类
│       ├── redis.py                 # Redis 连接、发布/订阅封装
│       ├── hashing.py               # 密码哈希/校验工具
│       └── common.py                # 其它通用辅助函数
├── alembic/                         # 数据库迁移（Alembic）
│   ├── env.py
│   ├── script.py.mako
│   └── versions/                    # 每次迁移生成的版本文件
├── tests/                           # 自动化测试
│   ├── test_auth.py
│   ├── test_messages.py
│   └── test_websocket_flow.py
├── message_center_schema.sql        # 当前已经设计好的 SQL 表结构
├── pyproject.toml                   # 使用 poetry 时的依赖和配置（或换成 requirements.txt）
└── README.md                        # 项目说明、启动方式、架构说明

说明：
- 这是一个“手画”的目标结构，实际开发时可以按需增删模块。
- 下一步可以从 app/main.py、core/config.py、db/session.py 开始，逐步把骨架代码搭起来。
