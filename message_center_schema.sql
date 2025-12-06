/*
 Navicat MySQL Dump SQL

 Source Server         : 本机wsl环境
 Source Server Type    : MySQL
 Source Server Version : 80044 (8.0.44-0ubuntu0.24.04.1)
 Source Host           : 127.0.0.1:3306
 Source Schema         : message_center

 Target Server Type    : MySQL
 Target Server Version : 80044 (8.0.44-0ubuntu0.24.04.1)
 File Encoding         : 65001

 Date: 05/12/2025 18:48:58
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for mc_admin_role
-- ----------------------------
DROP TABLE IF EXISTS `mc_admin_role`;
CREATE TABLE `mc_admin_role`  (
  `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键',
  `name` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '角色名称',
  `code` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '角色编码',
  `description` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '说明',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `uk_mc_admin_role_code`(`code` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '后台角色' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of mc_admin_role
-- ----------------------------
INSERT INTO `mc_admin_role` VALUES (1, 'ops', 'ops', 'ops role', '2025-12-05 08:54:11');
INSERT INTO `mc_admin_role` VALUES (2, 'devops', '12345', '测试的', '2025-12-05 10:47:16');

-- ----------------------------
-- Table structure for mc_admin_user
-- ----------------------------
DROP TABLE IF EXISTS `mc_admin_user`;
CREATE TABLE `mc_admin_user`  (
  `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键',
  `username` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '登录名',
  `password_hash` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '密码哈希（如 bcrypt/argon2）',
  `avatar` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '用户头像',
  `display_name` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '展示名称',
  `phone` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '手机号',
  `is_super` tinyint(1) NOT NULL DEFAULT 0 COMMENT '是否超级管理员 1=是 0=否',
  `is_active` tinyint(1) NOT NULL DEFAULT 1 COMMENT '是否启用 1=是 0=否',
  `last_login_ip` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '最近登录IP',
  `last_login_at` timestamp NULL DEFAULT NULL COMMENT '最近登录时间',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `uk_mc_admin_user_username`(`username` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '后台管理用户' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of mc_admin_user
-- ----------------------------
INSERT INTO `mc_admin_user` VALUES (1, 'admin', '$2b$12$oaobiIPoFhjcLJexAUgyce4luAWJ53iXoG10PzL/.sjoNVxjBkt7W', NULL, '王掌柜', '15637928033', 1, 1, '127.0.0.1', '2025-12-05 09:58:13', '2025-12-05 16:32:18', '2025-12-05 09:58:13');

-- ----------------------------
-- Table structure for mc_admin_user_role
-- ----------------------------
DROP TABLE IF EXISTS `mc_admin_user_role`;
CREATE TABLE `mc_admin_user_role`  (
  `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键',
  `user_id` bigint UNSIGNED NOT NULL COMMENT '后台用户 mc_admin_user.id',
  `role_id` bigint UNSIGNED NOT NULL COMMENT '后台角色 mc_admin_role.id',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `uk_mc_admin_user_role`(`user_id` ASC, `role_id` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '后台用户-角色关系' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of mc_admin_user_role
-- ----------------------------

-- ----------------------------
-- Table structure for mc_app
-- ----------------------------
DROP TABLE IF EXISTS `mc_app`;
CREATE TABLE `mc_app`  (
  `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键',
  `name` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '业务系统名称',
  `code` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '业务系统编码，HTTP/gRPC 调用方标识',
  `secret` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '签名密钥，用于鉴权',
  `description` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '说明',
  `is_active` tinyint(1) NOT NULL DEFAULT 1 COMMENT '是否启用 1=是 0=否',
  `mode` tinyint(1) NOT NULL DEFAULT 0 COMMENT '运行模式：0=普通消息 1=客服模式 2=扩展',
  `mode_config` json NULL COMMENT '模式配置(JSON，可选)',
  `created_by` bigint UNSIGNED NULL DEFAULT NULL COMMENT '创建人 mc_admin_user.id',
  `updated_by` bigint UNSIGNED NULL DEFAULT NULL COMMENT '最后修改人 mc_admin_user.id',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `uk_mc_app_code`(`code` ASC) USING BTREE,
  INDEX `idx_mc_app_active`(`is_active` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '接入的业务系统' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of mc_app
-- ----------------------------
INSERT INTO `mc_app` VALUES (1, 'AppA', 'appa', 'secret123', 'demo', 1, NULL, NULL, '2025-12-05 08:54:32', '2025-12-05 08:54:32');
INSERT INTO `mc_app` VALUES (2, '', '', '', '', 1, NULL, NULL, '2025-12-05 09:58:28', '2025-12-05 09:58:28');

-- ----------------------------
-- Table structure for mc_channel
-- ----------------------------
DROP TABLE IF EXISTS `mc_channel`;
CREATE TABLE `mc_channel`  (
  `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键',
  `app_id` bigint UNSIGNED NOT NULL COMMENT '所属业务系统 mc_app.id',
  `channel_key` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '通道标识，作为 Redis channel 名称',
  `name` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '通道名称',
  `description` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '说明',
  `is_active` tinyint(1) NOT NULL DEFAULT 1 COMMENT '是否启用 1=是 0=否',
  `dispatch_mode` tinyint(1) NOT NULL DEFAULT 0 COMMENT '投递模式：0=按订阅(默认)、1=广播在线用户、2=广播所有用户',
  `broadcast_filter` json NULL COMMENT '广播过滤条件(JSON，可选)',
  `created_by` bigint UNSIGNED NULL DEFAULT NULL COMMENT '创建人 mc_admin_user.id',
  `updated_by` bigint UNSIGNED NULL DEFAULT NULL COMMENT '最后修改人 mc_admin_user.id',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `uk_mc_channel_app_key`(`app_id` ASC, `channel_key` ASC) USING BTREE,
  INDEX `idx_mc_channel_app_active`(`app_id` ASC, `is_active` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '消息通道（主题）' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of mc_channel
-- ----------------------------
INSERT INTO `mc_channel` VALUES (1, 1, 'news', '新闻', 'news channel', 1, 0, NULL, NULL, NULL, '2025-12-05 08:54:40', '2025-12-05 08:54:40');

-- ----------------------------
-- Table structure for mc_channel_message_type
-- ----------------------------
DROP TABLE IF EXISTS `mc_channel_message_type`;
CREATE TABLE `mc_channel_message_type`  (
  `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键',
  `channel_id` bigint UNSIGNED NOT NULL COMMENT '通道ID mc_channel.id',
  `message_type_id` bigint UNSIGNED NOT NULL COMMENT '消息类型ID mc_message_type.id',
  `is_default` tinyint(1) NOT NULL DEFAULT 0 COMMENT '是否为默认类型 1=是 0=否',
  `config` json NULL COMMENT '通道特定的消息类型配置参数(JSON)',
  `is_active` tinyint(1) NOT NULL DEFAULT 1 COMMENT '是否启用 1=是 0=否',
  `created_by` bigint UNSIGNED NULL DEFAULT NULL COMMENT '创建人 mc_admin_user.id',
  `updated_by` bigint UNSIGNED NULL DEFAULT NULL COMMENT '最后修改人 mc_admin_user.id',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `uk_mc_channel_message_type`(`channel_id` ASC, `message_type_id` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '通道消息类型配置表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of mc_channel_message_type
-- ----------------------------
INSERT INTO `mc_channel_message_type` VALUES (1, 1, 1, 1, 'null', 1, NULL, NULL, '2025-12-05 08:55:05', '2025-12-05 08:55:05');

-- ----------------------------
-- Table structure for mc_client_connection
-- ----------------------------
DROP TABLE IF EXISTS `mc_client_connection`;
CREATE TABLE `mc_client_connection`  (
  `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键',
  `user_id` bigint UNSIGNED NOT NULL COMMENT '用户 mc_user.id',
  `instance_id` bigint UNSIGNED NOT NULL COMMENT '处理该连接的实例 mc_instance.id',
  `client_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '客户端标识，如设备ID/浏览器标识',
  `role` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '角色（如 admin/visitor）',
  `token` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '接入 token/标识',
  `user_agent` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT 'UA 信息',
  `ip` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '客户端IP',
  `connected_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '连接建立时间',
  `disconnected_at` timestamp NULL DEFAULT NULL COMMENT '连接关闭时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_mc_connection_user`(`user_id` ASC, `connected_at` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = 'WebSocket 客户端连接信息' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of mc_client_connection
-- ----------------------------

-- ----------------------------
-- Table structure for mc_instance
-- ----------------------------
DROP TABLE IF EXISTS `mc_instance`;
CREATE TABLE `mc_instance`  (
  `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键',
  `instance_key` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '实例标识，如 hostname+进程号',
  `host` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '主机名或IP',
  `pid` int UNSIGNED NULL DEFAULT NULL COMMENT '进程ID',
  `started_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '启动时间',
  `last_heartbeat` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最近心跳时间',
  `is_active` tinyint(1) NOT NULL DEFAULT 1 COMMENT '是否活跃 1=是 0=否',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `uk_mc_instance_key`(`instance_key` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '消息中台运行实例' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of mc_instance
-- ----------------------------
INSERT INTO `mc_instance` VALUES (1, 'frontend-1764931697496', 'localhost', 7145, '2025-12-05 10:48:14', '2025-12-05 10:48:14', 1);
INSERT INTO `mc_instance` VALUES (2, 'frontend-1764931706151', 'localhost', 1992, '2025-12-05 10:48:24', '2025-12-05 10:48:24', 1);

-- ----------------------------
-- Table structure for mc_message
-- ----------------------------
DROP TABLE IF EXISTS `mc_message`;
CREATE TABLE `mc_message`  (
  `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键',
  `app_id` bigint UNSIGNED NOT NULL COMMENT '来源业务系统 mc_app.id',
  `channel_id` bigint UNSIGNED NOT NULL COMMENT '所属通道 mc_channel.id',
  `message_type_id` bigint UNSIGNED NULL DEFAULT NULL COMMENT '消息类型 mc_message_type.id',
  `message_key` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '业务方消息唯一键，便于去重',
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '标题',
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '消息文本内容',
  `payload` json NULL COMMENT '结构化数据(JSON)，可用于客户端自定义渲染',
  `priority` tinyint UNSIGNED NOT NULL DEFAULT 0 COMMENT '优先级 0-9，数值越大优先级越高',
  `dispatch_mode` tinyint(1) NOT NULL DEFAULT 0 COMMENT '派发模式：0=按订阅 1=单播/定向 2=广播',
  `target_user_ids` json NULL COMMENT '单播/定向目标用户ID数组',
  `status` tinyint UNSIGNED NOT NULL DEFAULT 0 COMMENT '状态 0=已接收 1=已入队/已发布 2=发送失败',
  `error_msg` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '失败原因',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间（接收时间）',
  `published_at` timestamp NULL DEFAULT NULL COMMENT '发布到 Redis 的时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `uk_mc_message_key`(`message_key` ASC) USING BTREE,
  INDEX `idx_mc_message_channel_created`(`channel_id` ASC, `created_at` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '消息记录' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of mc_message
-- ----------------------------

-- ----------------------------
-- Table structure for mc_message_delivery
-- ----------------------------
DROP TABLE IF EXISTS `mc_message_delivery`;
CREATE TABLE `mc_message_delivery`  (
  `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键',
  `message_id` bigint UNSIGNED NOT NULL COMMENT '消息 mc_message.id',
  `user_id` bigint UNSIGNED NOT NULL COMMENT '目标用户 mc_user.id',
  `instance_id` bigint UNSIGNED NULL DEFAULT NULL COMMENT '负责推送的实例 mc_instance.id，可为空',
  `client_connection_id` bigint UNSIGNED NULL DEFAULT NULL COMMENT '具体 WebSocket 连接 mc_client_connection.id',
  `status` tinyint UNSIGNED NOT NULL DEFAULT 0 COMMENT '投递状态 0=待发送 1=已推送 2=客户端已确认 3=发送失败 4=已过期',
  `retry_count` int UNSIGNED NOT NULL DEFAULT 0 COMMENT '重试次数',
  `last_error` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '最近一次失败原因',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `sent_at` timestamp NULL DEFAULT NULL COMMENT '第一次发送时间',
  `ack_at` timestamp NULL DEFAULT NULL COMMENT '客户端确认时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_mc_delivery_user_status`(`user_id` ASC, `status` ASC, `created_at` ASC) USING BTREE,
  INDEX `idx_mc_delivery_message`(`message_id` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '消息投递与确认明细' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of mc_message_delivery
-- ----------------------------

-- ----------------------------
-- Table structure for mc_message_template
-- ----------------------------
DROP TABLE IF EXISTS `mc_message_template`;
CREATE TABLE `mc_message_template`  (
  `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键',
  `app_id` bigint UNSIGNED NOT NULL COMMENT '所属业务系统 mc_app.id',
  `channel_id` bigint UNSIGNED NULL DEFAULT NULL COMMENT '默认所属通道 mc_channel.id，可为空表示跨通道',
  `template_key` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '模板编码，用于业务调用',
  `name` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '模板名称',
  `title_template` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '标题模板，可为空',
  `content_template` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '内容模板，支持占位符',
  `payload_template` json NULL COMMENT 'payload 模板(JSON)，用于前端自定义渲染',
  `is_default` tinyint(1) NOT NULL DEFAULT 0 COMMENT '是否为对应通道默认模板 1=是 0=否',
  `created_by` bigint UNSIGNED NULL DEFAULT NULL COMMENT '创建人 mc_admin_user.id',
  `updated_by` bigint UNSIGNED NULL DEFAULT NULL COMMENT '最后修改人 mc_admin_user.id',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `uk_mc_template_key`(`template_key` ASC) USING BTREE,
  INDEX `idx_mc_template_app_channel`(`app_id` ASC, `channel_id` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '后台配置的消息模板' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of mc_message_template
-- ----------------------------
INSERT INTO `mc_message_template` VALUES (1, 1, 1, 'welcome', '欢迎', NULL, 'Hello {{name}}', 'null', 1, NULL, NULL, '2025-12-05 08:55:18', '2025-12-05 10:11:19');

-- ----------------------------
-- Table structure for mc_message_type
-- ----------------------------
DROP TABLE IF EXISTS `mc_message_type`;
CREATE TABLE `mc_message_type`  (
  `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键',
  `code` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '消息类型编码（如：text, image, video, audio）',
  `name` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '消息类型名称',
  `description` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '消息类型描述',
  `is_active` tinyint(1) NOT NULL DEFAULT 1 COMMENT '是否启用 1=是 0=否',
  `created_by` bigint UNSIGNED NULL DEFAULT NULL COMMENT '创建人 mc_admin_user.id',
  `updated_by` bigint UNSIGNED NULL DEFAULT NULL COMMENT '最后修改人 mc_admin_user.id',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `uk_mc_message_type_code`(`code` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '消息类型定义表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of mc_message_type
-- ----------------------------
INSERT INTO `mc_message_type` VALUES (1, 'text', '文本', NULL, 1, NULL, NULL, '2025-12-05 08:54:53', '2025-12-05 08:54:53');

-- ----------------------------
-- Table structure for mc_subscription
-- ----------------------------
DROP TABLE IF EXISTS `mc_subscription`;
CREATE TABLE `mc_subscription`  (
  `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键',
  `user_id` bigint UNSIGNED NOT NULL COMMENT '用户 mc_user.id',
  `channel_id` bigint UNSIGNED NOT NULL COMMENT '通道 mc_channel.id',
  `message_type_id` bigint UNSIGNED NULL DEFAULT NULL COMMENT '订阅的消息类型 mc_message_type.id',
  `is_active` tinyint(1) NOT NULL DEFAULT 1 COMMENT '是否有效 1=是 0=否',
  `source` tinyint UNSIGNED NOT NULL DEFAULT 1 COMMENT '订阅来源 1=用户 2=后台 3=系统默认',
  `created_by` bigint UNSIGNED NULL DEFAULT NULL COMMENT '后台创建人 mc_admin_user.id',
  `updated_by` bigint UNSIGNED NULL DEFAULT NULL COMMENT '后台修改人 mc_admin_user.id',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '订阅时间',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `uk_mc_subscription_user_channel`(`user_id` ASC, `channel_id` ASC, `message_type_id` ASC) USING BTREE,
  INDEX `idx_mc_subscription_channel`(`channel_id` ASC, `is_active` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '用户与消息通道的订阅关系' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of mc_subscription
-- ----------------------------
INSERT INTO `mc_subscription` VALUES (1, 1, 1, 1, 1, 2, NULL, NULL, '2025-12-05 08:55:38', '2025-12-05 08:55:38');

-- ----------------------------
-- Table structure for mc_user
-- ----------------------------
DROP TABLE IF EXISTS `mc_user`;
CREATE TABLE `mc_user`  (
  `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键',
  `app_id` bigint UNSIGNED NOT NULL COMMENT '所属业务系统 mc_app.id',
  `external_user_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '业务系统中的用户ID',
  `nickname` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '显示名称/昵称',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `uk_mc_user_app_external`(`app_id` ASC, `external_user_id` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '消息中台用户映射' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of mc_user
-- ----------------------------
INSERT INTO `mc_user` VALUES (1, 1, 'u1', '用户1', '2025-12-05 08:55:29');

SET FOREIGN_KEY_CHECKS = 1;
