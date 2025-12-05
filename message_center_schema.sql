-- 消息中台数据库结构设计（MySQL 8+）
-- 结合架构图：业务系统(A/B 等) 通过 HTTP/gRPC 推送消息到 FastAPI 消息中台，
-- 中台经 Redis Pub/Sub 分发到多实例，再通过 WebSocket 推送到客户端。

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS `mc_client_connection`;
DROP TABLE IF EXISTS `mc_instance`;
DROP TABLE IF EXISTS `mc_message_delivery`;
DROP TABLE IF EXISTS `mc_message`;
DROP TABLE IF EXISTS `mc_subscription`;
DROP TABLE IF EXISTS `mc_message_template`;
DROP TABLE IF EXISTS `mc_channel_message_type`;
DROP TABLE IF EXISTS `mc_message_type`;
DROP TABLE IF EXISTS `mc_channel`;
DROP TABLE IF EXISTS `mc_user`;
DROP TABLE IF EXISTS `mc_app`;
DROP TABLE IF EXISTS `mc_admin_user_role`;
DROP TABLE IF EXISTS `mc_admin_role`;
DROP TABLE IF EXISTS `mc_admin_user`;

-- 后台管理用户（登录账号）
CREATE TABLE `mc_admin_user` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键',
  `username` VARCHAR(64) NOT NULL COMMENT '登录名',
  `password_hash` VARCHAR(255) NOT NULL COMMENT '密码哈希（如 bcrypt/argon2）',
  `display_name` VARCHAR(128) NULL COMMENT '展示名称',
  `phone` VARCHAR(32) NULL COMMENT '手机号',
  `is_super` TINYINT(1) NOT NULL DEFAULT 0 COMMENT '是否超级管理员 1=是 0=否',
  `is_active` TINYINT(1) NOT NULL DEFAULT 1 COMMENT '是否启用 1=是 0=否',
  `last_login_ip` VARCHAR(45) NULL COMMENT '最近登录IP',
  `last_login_at` TIMESTAMP NULL DEFAULT NULL COMMENT '最近登录时间',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_mc_admin_user_username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='后台管理用户';


-- 后台角色（简单 RBAC，可在代码中绑定权限）
CREATE TABLE `mc_admin_role` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键',
  `name` VARCHAR(64) NOT NULL COMMENT '角色名称',
  `code` VARCHAR(64) NOT NULL COMMENT '角色编码',
  `description` VARCHAR(255) NULL COMMENT '说明',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_mc_admin_role_code` (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='后台角色';


-- 后台用户与角色关系
CREATE TABLE `mc_admin_user_role` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键',
  `user_id` BIGINT UNSIGNED NOT NULL COMMENT '后台用户 mc_admin_user.id',
  `role_id` BIGINT UNSIGNED NOT NULL COMMENT '后台角色 mc_admin_role.id',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_mc_admin_user_role` (`user_id`, `role_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='后台用户-角色关系';


-- 业务接入系统（如：业务系统A-PHP、业务系统B-Java）
CREATE TABLE `mc_app` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键',
  `name` VARCHAR(128) NOT NULL COMMENT '业务系统名称',
  `code` VARCHAR(64) NOT NULL COMMENT '业务系统编码，HTTP/gRPC 调用方标识',
  `secret` VARCHAR(128) NOT NULL COMMENT '签名密钥，用于鉴权',
  `description` VARCHAR(255) NULL COMMENT '说明',
  `is_active` TINYINT(1) NOT NULL DEFAULT 1 COMMENT '是否启用 1=是 0=否',
  `created_by` BIGINT UNSIGNED NULL COMMENT '创建人 mc_admin_user.id',
  `updated_by` BIGINT UNSIGNED NULL COMMENT '最后修改人 mc_admin_user.id',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_mc_app_code` (`code`),
  KEY `idx_mc_app_active` (`is_active`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='接入的业务系统';


-- 业务用户（由各业务系统的 user_id 映射而来）
CREATE TABLE `mc_user` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键',
  `app_id` BIGINT UNSIGNED NOT NULL COMMENT '所属业务系统 mc_app.id',
  `external_user_id` VARCHAR(128) NOT NULL COMMENT '业务系统中的用户ID',
  `nickname` VARCHAR(128) NULL COMMENT '显示名称/昵称',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_mc_user_app_external` (`app_id`, `external_user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='消息中台用户映射';


-- 消息通道（主题）
CREATE TABLE `mc_channel` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键',
  `app_id` BIGINT UNSIGNED NOT NULL COMMENT '所属业务系统 mc_app.id',
  `channel_key` VARCHAR(128) NOT NULL COMMENT '通道标识，作为 Redis channel 名称',
  `name` VARCHAR(128) NOT NULL COMMENT '通道名称',
  `description` VARCHAR(255) NULL COMMENT '说明',
  `is_active` TINYINT(1) NOT NULL DEFAULT 1 COMMENT '是否启用 1=是 0=否',
  `created_by` BIGINT UNSIGNED NULL COMMENT '创建人 mc_admin_user.id',
  `updated_by` BIGINT UNSIGNED NULL COMMENT '最后修改人 mc_admin_user.id',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_mc_channel_app_key` (`app_id`, `channel_key`),
  KEY `idx_mc_channel_app_active` (`app_id`, `is_active`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='消息通道（主题）';

-- 消息类型定义
CREATE TABLE `mc_message_type` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键',
  `code` VARCHAR(64) NOT NULL COMMENT '消息类型编码（如：text, image, video, audio）',
  `name` VARCHAR(128) NOT NULL COMMENT '消息类型名称',
  `description` VARCHAR(255) NULL COMMENT '消息类型描述',
  `is_active` TINYINT(1) NOT NULL DEFAULT 1 COMMENT '是否启用 1=是 0=否',
  `created_by` BIGINT UNSIGNED NULL COMMENT '创建人 mc_admin_user.id',
  `updated_by` BIGINT UNSIGNED NULL COMMENT '最后修改人 mc_admin_user.id',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_mc_message_type_code` (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='消息类型定义表';

-- 通道消息类型配置（通道支持的消息类型）
CREATE TABLE `mc_channel_message_type` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键',
  `channel_id` BIGINT UNSIGNED NOT NULL COMMENT '通道ID mc_channel.id',
  `message_type_id` BIGINT UNSIGNED NOT NULL COMMENT '消息类型ID mc_message_type.id',
  `is_default` TINYINT(1) NOT NULL DEFAULT 0 COMMENT '是否为默认类型 1=是 0=否',
  `config` JSON NULL COMMENT '通道特定的消息类型配置参数(JSON)',
  `is_active` TINYINT(1) NOT NULL DEFAULT 1 COMMENT '是否启用 1=是 0=否',
  `created_by` BIGINT UNSIGNED NULL COMMENT '创建人 mc_admin_user.id',
  `updated_by` BIGINT UNSIGNED NULL COMMENT '最后修改人 mc_admin_user.id',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_mc_channel_message_type` (`channel_id`, `message_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='通道消息类型配置表';


-- 消息模板（可配置默认消息/模板）
CREATE TABLE `mc_message_template` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键',
  `app_id` BIGINT UNSIGNED NOT NULL COMMENT '所属业务系统 mc_app.id',
  `channel_id` BIGINT UNSIGNED NULL COMMENT '默认所属通道 mc_channel.id，可为空表示跨通道',
  `template_key` VARCHAR(64) NOT NULL COMMENT '模板编码，用于业务调用',
  `name` VARCHAR(128) NOT NULL COMMENT '模板名称',
  `title_template` VARCHAR(255) NULL COMMENT '标题模板，可为空',
  `content_template` TEXT NOT NULL COMMENT '内容模板，支持占位符',
  `payload_template` JSON NULL COMMENT 'payload 模板(JSON)，用于前端自定义渲染',
  `is_default` TINYINT(1) NOT NULL DEFAULT 0 COMMENT '是否为对应通道默认模板 1=是 0=否',
  `created_by` BIGINT UNSIGNED NULL COMMENT '创建人 mc_admin_user.id',
  `updated_by` BIGINT UNSIGNED NULL COMMENT '最后修改人 mc_admin_user.id',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_mc_template_key` (`template_key`),
  KEY `idx_mc_template_app_channel` (`app_id`, `channel_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='后台配置的消息模板';


-- 用户订阅关系：哪个用户订阅了哪些通道
CREATE TABLE `mc_subscription` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键',
  `user_id` BIGINT UNSIGNED NOT NULL COMMENT '用户 mc_user.id',
  `channel_id` BIGINT UNSIGNED NOT NULL COMMENT '通道 mc_channel.id',
  `message_type_id` BIGINT UNSIGNED NULL COMMENT '订阅的消息类型 mc_message_type.id',
  `is_active` TINYINT(1) NOT NULL DEFAULT 1 COMMENT '是否有效 1=是 0=否',
  `source` TINYINT UNSIGNED NOT NULL DEFAULT 1 COMMENT '订阅来源 1=用户 2=后台 3=系统默认',
  `created_by` BIGINT UNSIGNED NULL COMMENT '后台创建人 mc_admin_user.id',
  `updated_by` BIGINT UNSIGNED NULL COMMENT '后台修改人 mc_admin_user.id',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '订阅时间',
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_mc_subscription_user_channel` (`user_id`, `channel_id`, `message_type_id`),
  KEY `idx_mc_subscription_channel` (`channel_id`, `is_active`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户与消息通道的订阅关系';


-- 消息主体（业务系统推送进来的消息）
CREATE TABLE `mc_message` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键',
  `app_id` BIGINT UNSIGNED NOT NULL COMMENT '来源业务系统 mc_app.id',
  `channel_id` BIGINT UNSIGNED NOT NULL COMMENT '所属通道 mc_channel.id',
  `message_type_id` BIGINT UNSIGNED NULL COMMENT '消息类型 mc_message_type.id',
  `message_key` VARCHAR(64) NULL COMMENT '业务方消息唯一键，便于去重',
  `title` VARCHAR(255) NULL COMMENT '标题',
  `content` TEXT NOT NULL COMMENT '消息文本内容',
  `payload` JSON NULL COMMENT '结构化数据(JSON)，可用于客户端自定义渲染',
  `priority` TINYINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '优先级 0-9，数值越大优先级越高',
  `status` TINYINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '状态 0=已接收 1=已入队/已发布 2=发送失败',
  `error_msg` VARCHAR(255) NULL COMMENT '失败原因',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间（接收时间）',
  `published_at` TIMESTAMP NULL DEFAULT NULL COMMENT '发布到 Redis 的时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_mc_message_key` (`message_key`),
  KEY `idx_mc_message_channel_created` (`channel_id`, `created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='消息记录';


-- 消息投递明细：每条消息对每个用户的投递与确认状态
CREATE TABLE `mc_message_delivery` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键',
  `message_id` BIGINT UNSIGNED NOT NULL COMMENT '消息 mc_message.id',
  `user_id` BIGINT UNSIGNED NOT NULL COMMENT '目标用户 mc_user.id',
  `instance_id` BIGINT UNSIGNED NULL COMMENT '负责推送的实例 mc_instance.id，可为空',
  `client_connection_id` BIGINT UNSIGNED NULL COMMENT '具体 WebSocket 连接 mc_client_connection.id',
  `status` TINYINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '投递状态 0=待发送 1=已推送 2=客户端已确认 3=发送失败 4=已过期',
  `retry_count` INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '重试次数',
  `last_error` VARCHAR(255) NULL COMMENT '最近一次失败原因',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `sent_at` TIMESTAMP NULL DEFAULT NULL COMMENT '第一次发送时间',
  `ack_at` TIMESTAMP NULL DEFAULT NULL COMMENT '客户端确认时间',
  PRIMARY KEY (`id`),
  KEY `idx_mc_delivery_user_status` (`user_id`, `status`, `created_at`),
  KEY `idx_mc_delivery_message` (`message_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='消息投递与确认明细';


-- 消息中台运行实例（FastAPI 部署的多个实例）
CREATE TABLE `mc_instance` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键',
  `instance_key` VARCHAR(64) NOT NULL COMMENT '实例标识，如 hostname+进程号',
  `host` VARCHAR(128) NULL COMMENT '主机名或IP',
  `pid` INT UNSIGNED NULL COMMENT '进程ID',
  `started_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '启动时间',
  `last_heartbeat` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最近心跳时间',
  `is_active` TINYINT(1) NOT NULL DEFAULT 1 COMMENT '是否活跃 1=是 0=否',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_mc_instance_key` (`instance_key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='消息中台运行实例';


-- WebSocket 客户端连接
CREATE TABLE `mc_client_connection` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键',
  `user_id` BIGINT UNSIGNED NOT NULL COMMENT '用户 mc_user.id',
  `instance_id` BIGINT UNSIGNED NOT NULL COMMENT '处理该连接的实例 mc_instance.id',
  `client_id` VARCHAR(128) NULL COMMENT '客户端标识，如设备ID/浏览器标识',
  `user_agent` VARCHAR(255) NULL COMMENT 'UA 信息',
  `ip` VARCHAR(45) NULL COMMENT '客户端IP',
  `connected_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '连接建立时间',
  `disconnected_at` TIMESTAMP NULL DEFAULT NULL COMMENT '连接关闭时间',
  PRIMARY KEY (`id`),
  KEY `idx_mc_connection_user` (`user_id`, `connected_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='WebSocket 客户端连接信息';


SET FOREIGN_KEY_CHECKS = 1;
