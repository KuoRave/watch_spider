ALTER TABLE `watch_dictionary`
MODIFY COLUMN `dial_shape`  enum('暂无','圆形','方形','椭圆形','酒桶形','其他') CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '暂无' COMMENT '表盘形状' AFTER `dial_color`;
ALTER TABLE `watch_dictionary`
MODIFY COLUMN `sex`  enum('暂无','男士','女士','情侣','中性','其他') CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '暂无' COMMENT '性别' AFTER `number`;

ALTER TABLE `watch_dictionary`
DROP COLUMN `brand`;

ALTER TABLE `watch_movement`
MODIFY COLUMN `type`  varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '机芯类型' AFTER `name`;

ALTER TABLE `watch_dictionary`
MODIFY COLUMN `sex`  varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '性别' AFTER `number`,
MODIFY COLUMN `dial_shape`  varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '表盘形状' AFTER `dial_color`;

