/*
Navicat MySQL Data Transfer

Source Server         : GD
Source Server Version : 80026
Source Host           : localhost:3306
Source Database       : use_test

Target Server Type    : MYSQL
Target Server Version : 80026
File Encoding         : 65001

Date: 2025-01-06 23:40:20
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `dt1`
-- ----------------------------
DROP TABLE IF EXISTS `dt1`;
CREATE TABLE `dt1` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `start_name` varchar(32) DEFAULT NULL,
  `end_name` varchar(32) DEFAULT NULL,
  `money` int DEFAULT NULL,
  `exit_zhuangtai` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `date` date DEFAULT NULL,
  `time` time DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of dt1
-- ----------------------------

-- ----------------------------
-- Table structure for `information`
-- ----------------------------
DROP TABLE IF EXISTS `information`;
CREATE TABLE `information` (
  `id_card` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `name` varchar(32) NOT NULL,
  `age` smallint NOT NULL,
  `number` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `sex` varchar(12) NOT NULL,
  `xuehao` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`id_card`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of information
-- ----------------------------
INSERT INTO `information` VALUES ('410223200312298511', '周嘉诚', '19', '16627528621', '男', null);
INSERT INTO `information` VALUES ('411526200405013825', '蔡宜桐', '19', '15637699170\r\n1563769917015637699170', '女', '202178030201\r\n202178030201\r\n');

-- ----------------------------
-- Table structure for `vul_detection`
-- ----------------------------
DROP TABLE IF EXISTS `vul_detection`;
CREATE TABLE `vul_detection` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'id',
  `script_name` smallint NOT NULL COMMENT '脚本名称',
  `serial_num` int NOT NULL COMMENT '漏洞点序号',
  `description` text NOT NULL COMMENT '漏洞描述',
  `ip` varchar(100) NOT NULL COMMENT 'IP',
  `port` int NOT NULL COMMENT 'PORT',
  `user_id` varchar(100) NOT NULL COMMENT '用户id',
  `create_time` int NOT NULL COMMENT '创建时间',
  `status` smallint NOT NULL COMMENT '数据状态',
  `is_alive` smallint NOT NULL COMMENT '靶机是否可访问',
  `is_index_404` smallint NOT NULL,
  `is_vuln` smallint NOT NULL COMMENT '漏洞是否可利⽤',
  `is_vuln_404` smallint NOT NULL COMMENT '漏洞点是否404',
  `vul_detection_id` smallint NOT NULL COMMENT '漏洞检测id',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='单脚本测试结果记录表';

-- ----------------------------
-- Records of vul_detection
-- ----------------------------

-- ----------------------------
-- Table structure for `vul_detection_all`
-- ----------------------------
DROP TABLE IF EXISTS `vul_detection_all`;
CREATE TABLE `vul_detection_all` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'id',
  `match_name` varchar(1000) NOT NULL COMMENT '轮次名称',
  `match_id` varchar(50) NOT NULL COMMENT '轮次id',
  `team_name` int NOT NULL COMMENT '队伍名称',
  `script_name` smallint NOT NULL COMMENT '脚本名称',
  `serial_num` int NOT NULL COMMENT '漏洞点序号',
  `description` text NOT NULL COMMENT '漏洞描述',
  `ip` varchar(100) NOT NULL COMMENT 'IP',
  `port` int NOT NULL COMMENT 'PORT',
  `user_id` varchar(100) NOT NULL COMMENT '用户id',
  `create_time` int NOT NULL COMMENT '创建时间',
  `status` smallint NOT NULL COMMENT '数据状态',
  `is_alive` smallint NOT NULL COMMENT '靶机是否可访问',
  `is_index_404` smallint NOT NULL COMMENT '主页是否404',
  `is_vuln` smallint NOT NULL COMMENT '漏洞是否可利用',
  `is_vuln_404` smallint NOT NULL COMMENT '漏洞点是否404',
  `test_id` smallint NOT NULL COMMENT '轮次ID',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='某轮次测试详细结果表';

-- ----------------------------
-- Records of vul_detection_all
-- ----------------------------

-- ----------------------------
-- Table structure for `vul_ip`
-- ----------------------------
DROP TABLE IF EXISTS `vul_ip`;
CREATE TABLE `vul_ip` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'id',
  `match_name` varchar(1000) NOT NULL COMMENT '轮次名称',
  `match_id` varchar(50) NOT NULL COMMENT '轮次id',
  `team_name` int NOT NULL COMMENT '队伍名称',
  `script_name` smallint NOT NULL COMMENT '脚本名称',
  `serial_num` int NOT NULL COMMENT '漏洞点序号',
  `ip` varchar(100) NOT NULL COMMENT 'IP',
  `port` int NOT NULL COMMENT 'PORT',
  `user_id` varchar(100) NOT NULL COMMENT '用户id',
  `create_time` int NOT NULL COMMENT '创建时间',
  `status` smallint NOT NULL COMMENT '数据状态',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='某轮次测试 IP 信息表';

-- ----------------------------
-- Records of vul_ip
-- ----------------------------

-- ----------------------------
-- Table structure for `vul_msg`
-- ----------------------------
DROP TABLE IF EXISTS `vul_msg`;
CREATE TABLE `vul_msg` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '脚本id、主键',
  `script_name` varchar(255) NOT NULL COMMENT '脚本名',
  `vul_point_id` varchar(100) NOT NULL COMMENT '漏洞检测点',
  `create_time` int NOT NULL COMMENT '数据创建时间',
  `status` smallint NOT NULL COMMENT '数据状态',
  `user_id` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '⽤户id',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='脚本信息表';

-- ----------------------------
-- Records of vul_msg
-- ----------------------------

-- ----------------------------
-- Table structure for `vul_point_msg`
-- ----------------------------
DROP TABLE IF EXISTS `vul_point_msg`;
CREATE TABLE `vul_point_msg` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '检测点id',
  `serial_num` int NOT NULL COMMENT '检测点序号',
  `description` text NOT NULL COMMENT '检测点说明',
  `vul_point_id` varchar(100) NOT NULL COMMENT '漏洞检测点id',
  `create_time` int NOT NULL COMMENT '数据创建时间',
  `status` smallint NOT NULL COMMENT '数据状态',
  `user_id` varchar(100) NOT NULL COMMENT '用户id',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='漏洞检测点表';

-- ----------------------------
-- Records of vul_point_msg
-- ----------------------------

-- ----------------------------
-- Table structure for `vul_single_test`
-- ----------------------------
DROP TABLE IF EXISTS `vul_single_test`;
CREATE TABLE `vul_single_test` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'id',
  `vul_detection_id` varchar(100) NOT NULL COMMENT '测试结果id',
  `script_name` varchar(255) NOT NULL COMMENT '脚本名',
  `create_time` int NOT NULL COMMENT '数据创建时间',
  `status` smallint NOT NULL COMMENT '数据状态',
  `user_id` varchar(100) NOT NULL COMMENT '用户id',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='单脚本测试记录表';

-- ----------------------------
-- Records of vul_single_test
-- ----------------------------

-- ----------------------------
-- Table structure for `vul_test`
-- ----------------------------
DROP TABLE IF EXISTS `vul_test`;
CREATE TABLE `vul_test` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '中间表id',
  `test_id` varchar(255) NOT NULL COMMENT '测试id',
  `user_id` varchar(50) NOT NULL COMMENT '用户id',
  `match_name` varchar(1000) NOT NULL COMMENT '某轮次IP、PORT信息',
  `create_time` int NOT NULL COMMENT '数据创建时间',
  `status` smallint NOT NULL COMMENT '数据状态',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='某一轮测试结果记录表';

-- ----------------------------
-- Records of vul_test
-- ----------------------------

-- ----------------------------
-- Table structure for `vul_users`
-- ----------------------------
DROP TABLE IF EXISTS `vul_users`;
CREATE TABLE `vul_users` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '用户id',
  `user_id` varchar(100) NOT NULL COMMENT '用户user_id',
  `username` varchar(255) NOT NULL COMMENT '用户名',
  `password` varchar(255) NOT NULL COMMENT '密码',
  `auth` smallint NOT NULL COMMENT '权限',
  `create_time` int NOT NULL COMMENT '创建时间（时间戳）',
  `status` smallint NOT NULL COMMENT '数据状态',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='用户表';

-- ----------------------------
-- Records of vul_users
-- ----------------------------
