/*
 Navicat Premium Dump SQL

 Source Server         : GD
 Source Server Type    : MySQL
 Source Server Version : 80026 (8.0.26)
 Source Host           : localhost:3306
 Source Schema         : use_test

 Target Server Type    : MySQL
 Target Server Version : 80026 (8.0.26)
 File Encoding         : 65001

 Date: 10/01/2025 18:53:55
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for dt1
-- ----------------------------
DROP TABLE IF EXISTS `dt1`;
CREATE TABLE `dt1`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `start_name` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `end_name` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `money` int NULL DEFAULT NULL,
  `exit_zhuangtai` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `date` date NULL DEFAULT NULL,
  `time` time NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 9 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of dt1
-- ----------------------------

-- ----------------------------
-- Table structure for information
-- ----------------------------
DROP TABLE IF EXISTS `information`;
CREATE TABLE `information`  (
  `id_card` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `name` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `age` smallint NOT NULL,
  `number` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `sex` varchar(12) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `xuehao` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id_card`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of information
-- ----------------------------
INSERT INTO `information` VALUES ('410223200312298511', '周嘉诚', 19, '16627528621', '男', NULL);
INSERT INTO `information` VALUES ('411526200405013825', '蔡宜桐', 19, '15637699170\r\n1563769917015637699170', '女', '202178030201\r\n202178030201\r\n');

-- ----------------------------
-- Table structure for vul_detection
-- ----------------------------
DROP TABLE IF EXISTS `vul_detection`;
CREATE TABLE `vul_detection`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'id',
  `script_name` smallint NULL DEFAULT NULL COMMENT '脚本名称',
  `serial_num` int NULL DEFAULT NULL COMMENT '漏洞点序号',
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '漏洞描述',
  `ip` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT 'IP',
  `port` int NULL DEFAULT NULL COMMENT 'PORT',
  `user_id` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '用户id',
  `create_time` int NULL DEFAULT NULL COMMENT '创建时间',
  `status` smallint NULL DEFAULT NULL COMMENT '数据状态',
  `is_alive` smallint NULL DEFAULT NULL COMMENT '靶机是否可访问',
  `is_index_404` smallint NULL DEFAULT NULL,
  `is_vuln` smallint NULL DEFAULT NULL COMMENT '漏洞是否可利⽤',
  `is_vuln_404` smallint NULL DEFAULT NULL COMMENT '漏洞点是否404',
  `vul_detection_id` smallint NULL DEFAULT NULL COMMENT '漏洞检测id',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '单脚本测试结果记录表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of vul_detection
-- ----------------------------

-- ----------------------------
-- Table structure for vul_detection_all
-- ----------------------------
DROP TABLE IF EXISTS `vul_detection_all`;
CREATE TABLE `vul_detection_all`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'id',
  `match_name` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '轮次名称',
  `match_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '轮次id',
  `team_name` int NOT NULL COMMENT '队伍名称',
  `script_name` smallint NOT NULL COMMENT '脚本名称',
  `serial_num` int NOT NULL COMMENT '漏洞点序号',
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '漏洞描述',
  `ip` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT 'IP',
  `port` int NOT NULL COMMENT 'PORT',
  `user_id` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '用户id',
  `create_time` int NOT NULL COMMENT '创建时间',
  `status` smallint NOT NULL COMMENT '数据状态',
  `is_alive` smallint NOT NULL COMMENT '靶机是否可访问',
  `is_index_404` smallint NOT NULL COMMENT '主页是否404',
  `is_vuln` smallint NOT NULL COMMENT '漏洞是否可利用',
  `is_vuln_404` smallint NOT NULL COMMENT '漏洞点是否404',
  `test_id` smallint NOT NULL COMMENT '轮次ID',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '某轮次测试详细结果表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of vul_detection_all
-- ----------------------------

-- ----------------------------
-- Table structure for vul_ip
-- ----------------------------
DROP TABLE IF EXISTS `vul_ip`;
CREATE TABLE `vul_ip`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'id',
  `match_name` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '轮次名称',
  `match_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '轮次id',
  `team_name` int NULL DEFAULT NULL COMMENT '队伍名称',
  `script_name` smallint NULL DEFAULT NULL COMMENT '脚本名称',
  `serial_num` int NULL DEFAULT NULL COMMENT '漏洞点序号',
  `ip` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT 'IP',
  `port` int NULL DEFAULT NULL COMMENT 'PORT',
  `user_id` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '用户id',
  `create_time` int NULL DEFAULT NULL COMMENT '创建时间',
  `status` smallint NULL DEFAULT NULL COMMENT '数据状态',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '某轮次测试 IP 信息表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of vul_ip
-- ----------------------------

-- ----------------------------
-- Table structure for vul_msg
-- ----------------------------
DROP TABLE IF EXISTS `vul_msg`;
CREATE TABLE `vul_msg`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '脚本信息',
  `script_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '脚本名',
  `vul_point_id` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '漏洞检测点',
  `create_time` int NULL DEFAULT NULL COMMENT '数据创建时间',
  `status` smallint NULL DEFAULT NULL COMMENT '数据状态',
  `user_id` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '⽤户id',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '脚本信息表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of vul_msg
-- ----------------------------
INSERT INTO `vul_msg` VALUES (1, 'abc', '04ac25e0-ef6b-4839-97d3-cdeab0ea5a0b', 1736506169, 1, NULL);
INSERT INTO `vul_msg` VALUES (2, 'abc', '97b94139-907a-4502-be1d-660b1e2ebec1', 1736506187, 1, NULL);

-- ----------------------------
-- Table structure for vul_point_msg
-- ----------------------------
DROP TABLE IF EXISTS `vul_point_msg`;
CREATE TABLE `vul_point_msg`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '检测点id',
  `serial_num` int NULL DEFAULT NULL COMMENT '检测点序号',
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '检测点说明',
  `vul_point_id` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '漏洞检测点id',
  `create_time` int NULL DEFAULT NULL COMMENT '创建时间',
  `status` smallint NULL DEFAULT NULL COMMENT '数据状态',
  `user_id` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '用户id',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '漏洞检测点表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of vul_point_msg
-- ----------------------------

-- ----------------------------
-- Table structure for vul_single_test
-- ----------------------------
DROP TABLE IF EXISTS `vul_single_test`;
CREATE TABLE `vul_single_test`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'id',
  `vul_detection_id` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '测试结果id',
  `script_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '脚本名',
  `create_time` int NULL DEFAULT NULL COMMENT '数据创建时间',
  `status` smallint NULL DEFAULT NULL COMMENT '数据状态',
  `user_id` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '用户id',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '单脚本测试记录表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of vul_single_test
-- ----------------------------

-- ----------------------------
-- Table structure for vul_test
-- ----------------------------
DROP TABLE IF EXISTS `vul_test`;
CREATE TABLE `vul_test`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '中间表id',
  `test_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '测试id',
  `user_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '用户id',
  `match_name` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '某轮次IP、PORT信息',
  `create_time` int NULL DEFAULT NULL COMMENT '数据创建时间',
  `status` smallint NULL DEFAULT NULL COMMENT '数据状态',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '某一轮测试结果记录表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of vul_test
-- ----------------------------

-- ----------------------------
-- Table structure for vul_users
-- ----------------------------
DROP TABLE IF EXISTS `vul_users`;
CREATE TABLE `vul_users`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '用户id',
  `user_id` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '用户user_id',
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '用户名',
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '密码',
  `auth` smallint NULL DEFAULT NULL COMMENT '权限',
  `create_time` int NULL DEFAULT NULL COMMENT '创建时间（时间戳）',
  `status` smallint NULL DEFAULT NULL COMMENT '数据状态',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '用户表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of vul_users
-- ----------------------------
INSERT INTO `vul_users` VALUES (1, '123', 'John', 'secret', 1, 1234567890, 1);
INSERT INTO `vul_users` VALUES (2, '123', 'John', 'secret', 1, 1234567890, 1);

SET FOREIGN_KEY_CHECKS = 1;
