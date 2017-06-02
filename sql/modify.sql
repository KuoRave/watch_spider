ALTER TABLE `watch_dictionary`
MODIFY COLUMN `dial_shape`  enum('暂无','圆形','方形','椭圆形','酒桶形','其他') CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '暂无' COMMENT '表盘形状' AFTER `dial_color`;