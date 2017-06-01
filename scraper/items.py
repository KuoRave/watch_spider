# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Dictionary(scrapy.Item):
    """Watch Dictionary"""
    # Refer to fields of the watch_dictionary table
    brand = scrapy.Field(serializer=str)
    series = scrapy.Field(serializer=str)
    number = scrapy.Field(serializer=str)
    sex = scrapy.Field()
    cny = scrapy.Field(serializer=int)
    cny_date = scrapy.Field(serializer=str)
    euro = scrapy.Field(serializer=int)
    euro_date = scrapy.Field(serializer=str)
    dollor = scrapy.Field(serializer=int)
    dollor_date = scrapy.Field(serializer=str)
    hkd = scrapy.Field(serializer=int)
    hkd_date = scrapy.Field(serializer=str)
    mm_id = scrapy.Field(serializer=int)
    total_diameter = scrapy.Field(serializer=float)
    shell_thickness = scrapy.Field(serializer=float)
    shell_material = scrapy.Field(serializer=float)
    dial_color = scrapy.Field(serializer=str)
    dial_shape = scrapy.Field(serializer=str)
    dial_material = scrapy.Field(serializer=str)
    glass_material = scrapy.Field(serializer=str)
    crown_material = scrapy.Field(serializer=str)
    band_color = scrapy.Field(serializer=str)
    band_material = scrapy.Field(serializer=str)
    clasp_type = scrapy.Field(serializer=str)
    clasp_material = scrapy.Field(serializer=str)
    back_through = scrapy.Field(serializer=str)
    weight = scrapy.Field(serializer=float)
    diving_depth = scrapy.Field(serializer=int)
    feature = scrapy.Field(serializer=str)
    mm_obj = scrapy.Field()
    brand_obj = scrapy.Field()
    brand_id = scrapy.Field()

class Movement(scrapy.Item):
    """Watch Movement"""
    # Refer to fields of the watch_movement table
    name = scrapy.Field(serializer=str)
    type = scrapy.Field()
    manufacture = scrapy.Field(serializer=str)
    basic = scrapy.Field(serializer=str)
    diameter = scrapy.Field(serializer=float)
    thickness = scrapy.Field(serializer=float)
    vibration = scrapy.Field(serializer=str)
    jewels = scrapy.Field(serializer=int)
    part_number = scrapy.Field(serializer=int)
    power_reserve = scrapy.Field(serializer=int)
    introduction = scrapy.Field(serializer=str)
    battery_life = scrapy.Field(serializer=str)
    wobbler = scrapy.Field(serializer=str)
    hairspring = scrapy.Field(serializer=str)
    suspension = scrapy.Field(serializer=str)
    token = scrapy.Field(serializer=str)
    
class Brand(scrapy.Item):
    """Watch Brand"""
    name = scrapy.Field(serializer=str)
    name_en = scrapy.Field(serializer=str)
    img_uri = scrapy.Field(serializer=str)