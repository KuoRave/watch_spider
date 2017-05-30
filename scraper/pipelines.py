# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
# import scrapy
import MySQLdb

class ScraperPipeline(object):
    mmSql = """INSERT INTO watch_movement (name, type, manufacture, basic,
            diameter, thickness, vibration, jewels, power_reserve, introduction,
            battery_life, wobbler, hairspring, suspension, part_number) 
            VALUE ("%s", "%s", "%s", "%s", %s, %s, "%s", %s, %s, "%s", "%s", "%s", "%s", "%s", %s)"""
    watchSql = """INSERT INTO watch_dictionary (brand, series, number, sex,
            cny, cny_date, euro, euro_date, dollor, dollor_date,
            hkd, hkd_date, mm_id, total_diameter, shell_thickness, shell_material,
            dial_color, dial_shape, dial_material, glass_material,
            crown_material, band_color, band_material, clasp_type,
            clasp_material, back_through, weight, diving_depth,
            feature) 
            VALUE (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    watchUpdateSql = """UPDATE watch_dictionary set brand=%s, series=%s, number=%s, sex=%s,
            cny=%s, cny_date=%s, euro=%s, euro_date=%s, dollor=%s, dollor_date=%s,
            hkd=%s, hkd_date=%s, mm_id=%s, total_diameter=%s, shell_thickness=%s, shell_material=%s,
            dial_color=%s, dial_shape=%s, dial_material=%s, glass_material=%s,
            crown_material=%s, band_color=%s, band_material=%s, clasp_type=%s,
            clasp_material=%s, back_through=%s, weight=%s, diving_depth=%s,
            feature=%s) WHERE id=%s"""
    mmSqlList, watchSqlList = [], []
    db = MySQLdb.connect(host='127.0.0.1', user='root', db="local", use_unicode=True, charset="utf8")

    def process_item(self, item, spider):
        cursor = self.db.cursor()
        # deal with movement data
        self.dealMovementData(cursor, item)
        self.dealWatch(cursor, item)
        return item
    
    def close_spider(self, spider):
        pass
        # c = self.db.cursor()
        # for sql in self.watchSqlList:
        #     print(self.watchSql % sql)
        # c.executemany(self.watchSql, self.watchSqlList)
        
    def dealMovementData(self, cursor, item):
        mm_obj = item['mm_obj']
        cursor.execute("SELECT id FROM watch_movement WHERE `name`='%s'" % mm_obj['name'])
        mm_result = cursor.fetchone()
        mm_line = []
        # 添加
        if mm_result is None:
            mm_line.append('暂无') if ('name' in mm_obj) is False else mm_line.append(mm_obj['name'])
            mm_line.append('暂无') if ('type' in mm_obj) is False else mm_line.append(mm_obj['type'])
            mm_line.append('暂无') if ('manufacture' in mm_obj) is False else mm_line.append(mm_obj['manufacture'])
            mm_line.append('暂无') if ('basic' in mm_obj) is False else mm_line.append(mm_obj['basic'])
            mm_line.append(0) if ('diameter' in mm_obj) is False else mm_line.append(mm_obj['diameter'])
            mm_line.append(0) if ('thickness' in mm_obj) is False else mm_line.append(mm_obj['thickness'])
            mm_line.append('暂无') if ('vibration' in mm_obj) is False else mm_line.append(mm_obj['vibration'])
            mm_line.append(0) if ('jewels' in mm_obj) is False else mm_line.append(mm_obj['jewels'])
            mm_line.append(0) if ('power_reserve' in mm_obj) is False else mm_line.append(mm_obj['power_reserve'])
            mm_line.append('暂无') if ('introduction' in mm_obj) is False else mm_line.append(mm_obj['introduction'])
            mm_line.append('暂无') if ('battery_life' in mm_obj) is False else mm_line.append(mm_obj['battery_life'])
            mm_line.append('暂无') if ('wobbler' in mm_obj) is False else mm_line.append(mm_obj['wobbler'])
            mm_line.append('暂无') if ('hairspring' in mm_obj) is False else mm_line.append(mm_obj['hairspring'])
            mm_line.append('暂无') if ('suspension' in mm_obj) is False else mm_line.append(mm_obj['suspension'])
            mm_line.append(0) if ('part_number' in mm_obj) is False else mm_line.append(mm_obj['part_number'])
            cursor.execute(self.mmSql % tuple(mm_line))
            cursor.execute("SELECT id FROM watch_movement WHERE `name`='%s'" % mm_obj['name'])
            mm_result = cursor.fetchone()
        # 编辑
        # else:
        #     pass
        item['mm_id'] = mm_result[0]

    def dealWatch(self, cursor, item):
        cursor.execute("SELECT id FROM watch_dictionary WHERE `number`='%s'" % item['number'])
        watch_result = cursor.fetchone()
        watch_line = []
        watch_line.append('暂无') if ('brand' in item) is False else watch_line.append(item['brand'])
        watch_line.append('暂无') if ('series' in item) is False else watch_line.append(item['series'])
        watch_line.append('暂无') if ('number' in item) is False else watch_line.append(item['number'])
        watch_line.append('暂无') if ('sex' in item) is False else watch_line.append(item['sex'])
        watch_line.append(0) if ('cny' in item) is False else watch_line.append(item['cny'])
        watch_line.append('暂无') if ('cny_date' in item) is False else watch_line.append(item['cny_date'])
        watch_line.append(0) if ('euro' in item) is False else watch_line.append(item['euro'])
        watch_line.append('暂无') if ('euro_date' in item) is False else watch_line.append(item['euro_date'])
        watch_line.append(0) if ('dollor' in item) is False else watch_line.append(item['dollor'])
        watch_line.append('暂无') if ('dollor_date' in item) is False else watch_line.append(item['dollor_date'])
        watch_line.append(0) if ('hkd' in item) is False else watch_line.append(item['hkd'])
        watch_line.append('暂无') if ('hkd_date' in item) is False else watch_line.append(item['hkd_date'])
        watch_line.append(0) if ('mm_id' in item) is False else watch_line.append(item['mm_id'])
        watch_line.append(0) if ('total_diameter' in item) is False else watch_line.append(item['total_diameter'])
        watch_line.append(0) if ('shell_thickness' in item) is False else watch_line.append(item['shell_thickness'])
        watch_line.append('暂无') if ('shell_material' in item) is False else watch_line.append(item['shell_material'])
        watch_line.append('暂无') if ('dial_color' in item) is False else watch_line.append(item['dial_color'])
        watch_line.append('暂无') if ('dial_shape' in item) is False else watch_line.append(item['dial_shape'])
        watch_line.append('暂无') if ('dial_material' in item) is False else watch_line.append(item['dial_material'])
        watch_line.append('暂无') if ('glass_material' in item) is False else watch_line.append(item['glass_material'])
        watch_line.append('暂无') if ('crown_material' in item) is False else watch_line.append(item['crown_material'])
        watch_line.append('暂无') if ('band_color' in item) is False else watch_line.append(item['band_color'])
        watch_line.append('暂无') if ('band_material' in item) is False else watch_line.append(item['band_material'])
        watch_line.append('暂无') if ('clasp_type' in item) is False else watch_line.append(item['clasp_type'])
        watch_line.append('暂无') if ('clasp_material' in item) is False else watch_line.append(item['clasp_material'])
        watch_line.append('暂无') if ('back_through' in item) is False else watch_line.append(item['back_through'])
        watch_line.append(0) if ('weight' in item) is False else watch_line.append(item['weight'])
        watch_line.append(0) if ('diving_depth' in item) is False else watch_line.append(item['diving_depth'])
        watch_line.append('暂无') if ('feature' in item) is False else watch_line.append(item['feature'])
        if watch_result is None:
            cursor.execute(self.watchSql % tuple(watch_line))
            # self.watchSqlList.append(tuple(watch_line))
        else:
            watch_line.append(watch_result[0])
            cursor.execute(self.watchUpdateSql % tuple(watch_line))
