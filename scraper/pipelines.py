# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
# import scrapy
import MySQLdb
import hashlib
import json
import requests
import re
import html

class ScraperPipeline(object):
    brandSql = """INSERT INTO watch_brand (name, name_en, img_uri) 
                VALUE("%s", "%s", "%s")"""
    mmSql = """INSERT INTO watch_movement (name, type, manufacture, basic,
            diameter, thickness, vibration, jewels, power_reserve, introduction,
            battery_life, wobbler, hairspring, suspension, part_number, token) 
            VALUE ("%s", "%s", "%s", "%s", %s, %s, "%s", %s, %s, "%s", "%s", "%s", "%s", "%s", %s, "%s")"""
    watchSql = """INSERT INTO watch_dictionary (brand_id, series, number, sex,
            cny, cny_date, euro, euro_date, dollor, dollor_date,
            hkd, hkd_date, mm_id, total_diameter, shell_thickness, shell_material,
            dial_color, dial_shape, dial_material, glass_material,
            crown_material, band_color, band_material, clasp_type,
            clasp_material, back_through, weight, diving_depth,
            feature) 
            VALUE (%s, '%s', '%s', '%s', %s, '%s', %s, '%s', %s, '%s', %s, '%s', %s, %s, %s, '%s', '%s','%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', %s, %s, '%s')"""
    watchUpdateSql = """UPDATE watch_dictionary set brand_id=%s, series='%s', number='%s', sex='%s',
            cny=%s, cny_date='%s', euro=%s, euro_date='%s', dollor=%s, dollor_date='%s',
            hkd=%s, hkd_date='%s', mm_id=%s, total_diameter=%s, shell_thickness=%s, shell_material='%s',
            dial_color='%s', dial_shape='%s', dial_material='%s', glass_material='%s',
            crown_material='%s', band_color='%s', band_material='%s', clasp_type='%s',
            clasp_material='%s', back_through='%s', weight=%s, diving_depth=%s,
            feature='%s' WHERE id=%s"""
    mmSqlList, watchSqlList = [], []
    db = MySQLdb.connect(host='127.0.0.1', user='root', db="local", use_unicode=True, charset="utf8")
    f = open('../log/log.txt', 'a', encoding='utf8')


    def process_item(self, item, spider):
        cursor = self.db.cursor()
        # deal with movement data
        self.dealMovementData(cursor, item)
        self.dealBrand(cursor, item)
        self.dealWatch(cursor, item)
        # return None
    
    def close_spider(self, spider):
        pass
        # c = self.db.cursor()
        # for sql in self.watchSqlList:
        #     print(self.watchSql % sql)
        # c.executemany(self.watchSql, self.watchSqlList)
        
    def dealBrand(self, cursor, item):
        brand_obj = item['brand_obj']
        brand_result = None
        brand_line = []
        if ('name' in brand_obj) is False:
            brand_obj['name'] = '暂无'
        if ('name_en' in brand_obj) is False:
            brand_obj['name_en'] = '暂无'
        cursor.execute("SELECT id,img_uri FROM watch_brand WHERE `name`='%s' OR `name_en`='%s'" % (brand_obj['name'].replace("'", "&apos;").replace('"', "&quot;"), brand_obj['name_en'].replace("'", "&apos;").replace('"', "&quot;")))
        brand_result = cursor.fetchone()
        if brand_result is None:
            suffix= ''
            path = '../images/'
            if brand_obj['img_uri'] is not None:
                # suffix_pattern = re.compile(r'\.(.*)')
                suffix = brand_obj['img_uri'].rsplit('.')[-1]
                filename = hashlib.md5(brand_obj['img_uri'].encode()).hexdigest() + '.' + suffix
                image = requests.get(brand_obj['img_uri'])
                with open(path + filename, 'wb') as img_file:
                    img_file.write(image.content)
                    brand_obj['img_uri'] = filename
                brand_line.append(brand_obj['name'].replace("'", "&apos;").replace('"', "&quot;"))
                brand_line.append(brand_obj['name_en'].replace("'", "&apos;").replace('"', "&quot;"))
                brand_line.append('') if ('img_uri' in brand_obj) is False else brand_line.append(brand_obj['img_uri'])
                cursor.execute(self.brandSql % tuple(brand_line))
                cursor.execute("SELECT id FROM watch_brand WHERE `name`='%s' OR `name_en`='%s'" % (brand_obj['name'].replace("'", "&apos;").replace('"', "&quot;"), brand_obj['name_en'].replace("'", "&apos;").replace('"', "&quot;")))
                brand_result = cursor.fetchone()
        item['brand_id'] = brand_result[0]

    def dealMovementData(self, cursor, item):
        mm_obj = item['mm_obj']
        mm_result = None
        if 'name' in mm_obj and mm_obj['name'] != '暂无':
            cursor.execute("SELECT id FROM watch_movement WHERE `name`='%s'" % mm_obj['name'].replace("'", "&apos;").replace('"', "&quot;"))
            mm_result = cursor.fetchone()
        mm_line = []
        mm_line.append('暂无') if ('name' in mm_obj) is False else mm_line.append(mm_obj['name'].replace("'", "&apos;").replace('"', "&quot;"))
        mm_line.append('暂无') if ('type' in mm_obj) is False else mm_line.append(mm_obj['type'].replace("'", "&apos;").replace('"', "&quot;"))
        mm_line.append('暂无') if ('manufacture' in mm_obj) is False else mm_line.append(mm_obj['manufacture'].replace("'", "&apos;").replace('"', "&quot;"))
        mm_line.append('暂无') if ('basic' in mm_obj) is False else mm_line.append(mm_obj['basic'].replace("'", "&apos;").replace('"', "&quot;"))
        mm_line.append(0) if ('diameter' in mm_obj) is False else mm_line.append(mm_obj['diameter'])
        mm_line.append(0) if ('thickness' in mm_obj) is False else mm_line.append(mm_obj['thickness'])
        mm_line.append('暂无') if ('vibration' in mm_obj) is False else mm_line.append(mm_obj['vibration'].replace("'", "&apos;").replace('"', "&quot;"))
        mm_line.append(0) if ('jewels' in mm_obj) is False else mm_line.append(mm_obj['jewels'])
        mm_line.append(0) if ('power_reserve' in mm_obj) is False else mm_line.append(mm_obj['power_reserve'])
        mm_line.append('暂无') if ('introduction' in mm_obj) is False else mm_line.append(mm_obj['introduction'].replace("'", "&apos;").replace('"', "&quot;"))
        mm_line.append('暂无') if ('battery_life' in mm_obj) is False else mm_line.append(mm_obj['battery_life'].replace("'", "&apos;").replace('"', "&quot;"))
        mm_line.append('暂无') if ('wobbler' in mm_obj) is False else mm_line.append(mm_obj['wobbler'].replace("'", "&apos;").replace('"', "&quot;"))
        mm_line.append('暂无') if ('hairspring' in mm_obj) is False else mm_line.append(mm_obj['hairspring'].replace("'", "&apos;").replace('"', "&quot;"))
        mm_line.append('暂无') if ('suspension' in mm_obj) is False else mm_line.append(mm_obj['suspension'].replace("'", "&apos;").replace('"', "&quot;"))
        mm_line.append(0) if ('part_number' in mm_obj) is False else mm_line.append(mm_obj['part_number'])
        token = hashlib.md5(json.dumps(mm_line).encode()).hexdigest()
        if mm_result is None:
            cursor.execute("SELECT id FROM watch_movement WHERE `token`='%s'" % token)
            mm_result = cursor.fetchone()
        mm_line.append(token)
        # 添加
        if mm_result is None:
            try:
                cursor.execute(self.mmSql % tuple(mm_line))
            except:
                print(self.mmSql % tuple(mm_line))
                self.f.write(self.mmSql % tuple(mm_line))
            cursor.execute("SELECT id FROM watch_movement WHERE `token`='%s'" % token)
            mm_result = cursor.fetchone()
        # 编辑
        # else:
        #     pass
        item['mm_id'] = mm_result[0]

    def dealWatch(self, cursor, item):
        cursor.execute("SELECT id FROM watch_dictionary WHERE `number`='%s'" % item['number'].replace("'", "&apos;").replace('"', "&quot;"))
        watch_result = cursor.fetchone()
        watch_line = []
        watch_line.append(0) if ('brand_id' in item) is False else watch_line.append(item['brand_id'])
        watch_line.append('暂无') if ('series' in item) is False else watch_line.append(item['series'].replace("'", "&apos;").replace('"', "&quot;"))
        watch_line.append('暂无') if ('number' in item) is False else watch_line.append(item['number'].replace("'", "&apos;").replace('"', "&quot;"))
        watch_line.append('暂无') if ('sex' in item) is False else watch_line.append(item['sex'].replace("'", "&apos;").replace('"', "&quot;"))
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
        watch_line.append('暂无') if ('shell_material' in item) is False else watch_line.append(item['shell_material'].replace("'", "&apos;").replace('"', "&quot;"))
        watch_line.append('暂无') if ('dial_color' in item) is False else watch_line.append(item['dial_color'].replace("'", "&apos;").replace('"', "&quot;"))
        watch_line.append('暂无') if ('dial_shape' in item) is False else watch_line.append(item['dial_shape'].replace("'", "&apos;").replace('"', "&quot;"))
        watch_line.append('暂无') if ('dial_material' in item) is False else watch_line.append(item['dial_material'].replace("'", "&apos;").replace('"', "&quot;"))
        watch_line.append('暂无') if ('glass_material' in item) is False else watch_line.append(item['glass_material'].replace("'", "&apos;").replace('"', "&quot;"))
        watch_line.append('暂无') if ('crown_material' in item) is False else watch_line.append(item['crown_material'].replace("'", "&apos;").replace('"', "&quot;"))
        watch_line.append('暂无') if ('band_color' in item) is False else watch_line.append(item['band_color'].replace("'", "&apos;").replace('"', "&quot;"))
        watch_line.append('暂无') if ('band_material' in item) is False else watch_line.append(item['band_material'].replace("'", "&apos;").replace('"', "&quot;"))
        watch_line.append('暂无') if ('clasp_type' in item) is False else watch_line.append(item['clasp_type'].replace("'", "&apos;").replace('"', "&quot;"))
        watch_line.append('暂无') if ('clasp_material' in item) is False else watch_line.append(item['clasp_material'].replace("'", "&apos;").replace('"', "&quot;"))
        watch_line.append('暂无') if ('back_through' in item) is False else watch_line.append(item['back_through'].replace("'", "&apos;").replace('"', "&quot;"))
        watch_line.append(0) if ('weight' in item) is False else watch_line.append(item['weight'])
        watch_line.append(0) if ('diving_depth' in item) is False else watch_line.append(item['diving_depth'])
        watch_line.append('暂无') if ('feature' in item) is False else watch_line.append(item['feature'].replace("'", "&apos;").replace('"', "&quot;"))
        if watch_result is None:
            try:
                cursor.execute(self.watchSql % tuple(watch_line))
            except:
                print(self.watchSql % tuple(watch_line))
                self.f.write(self.watchSql % tuple(watch_line))
                # error_str = self.watchSql % tuple(watch_line)
                # logging.log(logging.ERROR, "INSERT: " + error_str)
        else:
            try:
                watch_line.append(watch_result[0])
                cursor.execute(self.watchUpdateSql % tuple(watch_line))
            except:
                self.f.write(self.watchUpdateSql % tuple(watch_line))
                print(self.watchSql % tuple(watch_line))
