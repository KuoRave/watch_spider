/*
Navicat MySQL Data Transfer

Source Server         : locale
Source Server Version : 50714
Source Host           : localhost:3306
Source Database       : local

Target Server Type    : MYSQL
Target Server Version : 50714
File Encoding         : 65001

Date: 2017-05-28 22:45:22
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `watch_dictionary`
-- ----------------------------
DROP TABLE IF EXISTS `watch_dictionary`;
CREATE TABLE `watch_dictionary` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `brand` text NOT NULL COMMENT '品牌',
  `series` text NOT NULL COMMENT '系列',
  `number` text NOT NULL COMMENT '编号',
  `sex` enum('暂无','男士','女士') NOT NULL COMMENT '性别',
  `cny` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '人民币',
  `cny_date` text COMMENT '人民币评估日期',
  `euro` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '欧元',
  `euro_date` text COMMENT '欧元评估日期',
  `dollor` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '美元',
  `dollor_date` text COMMENT '美元评估日期',
  `hkd` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '港元',
  `hkd_date` text COMMENT '港元评估日期',
  `mm_id` int(10) unsigned NOT NULL COMMENT '机芯型号表主键',
  `total_diameter` float(11,1) unsigned NOT NULL DEFAULT '0.0' COMMENT '表直径(单位:毫米mm)',
  `shell_thickness` float(11,1) unsigned NOT NULL DEFAULT '0.0' COMMENT '表壳厚度(单位:毫米mm)',
  `shell_material` text NOT NULL COMMENT '表壳材质',
  `dial_color` text NOT NULL COMMENT '表盘颜色',
  `dial_shape` enum('暂无','圆形','方形','椭圆形','酒桶形') NOT NULL DEFAULT '暂无' COMMENT '表盘形状',
  `dial_material` text NOT NULL COMMENT '表盘材质',
  `glass_material` text NOT NULL COMMENT '表镜材质',
  `crown_material` text NOT NULL COMMENT '表冠材质',
  `band_color` text NOT NULL COMMENT '表带颜色',
  `band_material` text NOT NULL COMMENT '表带材质',
  `clasp_type` text NOT NULL COMMENT '表扣类型',
  `clasp_material` text NOT NULL COMMENT '表扣材质',
  `back_through` text NOT NULL COMMENT '背透',
  `weight` float(11,1) unsigned NOT NULL DEFAULT '0.0' COMMENT '重量(单位:克/g)',
  `diving_depth` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '防水深度',
  `feature` text NOT NULL COMMENT '功能',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COMMENT='腕表网手表字典';

-- ----------------------------
-- Table structure for `watch_image`
-- ----------------------------
DROP TABLE IF EXISTS `watch_image`;
CREATE TABLE `watch_image` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `watch_id` int(11) unsigned NOT NULL,
  `thumb_uri` varchar(200) NOT NULL COMMENT '缩略图uri',
  `origin_uri` varchar(200) NOT NULL COMMENT '原图uri',
  PRIMARY KEY (`id`),
  KEY `watch_id` (`watch_id`) USING BTREE
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COMMENT='手表图片';

-- ----------------------------
-- Table structure for `watch_movement`
-- ----------------------------
DROP TABLE IF EXISTS `watch_movement`;
CREATE TABLE `watch_movement` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` text NOT NULL COMMENT '机芯型号',
  `type` enum('暂无','石英','自动机械','手动机械') NOT NULL DEFAULT '暂无' COMMENT '机芯类型',
  `manufacture` text NOT NULL COMMENT '生产产商',
  `basic` text NOT NULL COMMENT '基础机芯',
  `diameter` float(11,2) unsigned NOT NULL DEFAULT '0.00' COMMENT '直径',
  `thickness` float(11,2) unsigned NOT NULL DEFAULT '0.00' COMMENT '厚度',
  `vibration` text NOT NULL COMMENT '振频',
  `jewels` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '宝石数',
  `power_reserve` int(5) NOT NULL DEFAULT '0' COMMENT '动力存储(单位:小时)',
  `introduction` text NOT NULL COMMENT '简介',
  `battery_life` text NOT NULL COMMENT '电池寿命',
  `wobbler` text NOT NULL COMMENT '摆轮',
  `hairspring` text NOT NULL COMMENT '游丝',
  `suspension` text NOT NULL COMMENT '避震',
  `part_number` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '零件数',
  `detail_url` text COMMENT '详情url',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COMMENT='腕表网机芯类型表';