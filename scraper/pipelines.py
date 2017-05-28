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
            VALUE ('%s', '%s', '%s', '%s', %s, %s, '%s', %s, %s, '%s', '%s', '%s', '%s', '%s', %s)"""
    watchSql = """INSERT INTO watch_dictionary (brand, series, number, sex,
            cny, cny_date, euro, euro_date, dollor, dollor_date,
            hkd, hkd_date, mm_id, total_diameter, shell_thickness, shell_material,
            dial_color, dial_shape, dial_material, glass_material,
            crown_material, band_color, band_material, clasp_type,
            clasp_material, back_through, weight, diving_depth,
            feature) 
            VALUE (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    mmSqlList, watchSqlList = [], []
    db = MySQLdb.connect(host='localhost', user='root', db="local", use_unicode=True, charset="utf8")

    def process_item(self, item, spider):
        cursor = self.db.cursor()
        # foscrapy crawl watch
        self.dealMovementData(cursor, item)
        return item
    
    def close_spider(self, spider):
        # c = self.db.cursor()
        # c.execute("""SELECT * from watch_dictionary""")
        
        pass
        
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