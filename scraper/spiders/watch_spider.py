import scrapy
from scraper.items import Dictionary, Movement
from scrapy.loader import ItemLoader
import re

class WatchSpider(scrapy.Spider):
    name = "watch"

    def start_requests(self):
        base_url = 'http://watch.xbiao.com/p{}_s0.html'
        urls = [base_url.format(i) for i in range(1, 2)] # 1393
        for url in urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        """Pagination pages"""
        try:
            # follow links to detail pages
            for li in response.css('div.watch.left > ul > li.watch-tile ul li'):
                # loader = ItemLoader(item=Dictionary(), response=li)
                try:
                    href = li.css('.watch-pic a::attr(href)').extract_first()
                    yield scrapy.Request(href, callback=self.parseDetail)
                except:
                    continue
        except:
            yield None

    def parseDetail(self, response):
        """Detail pages"""
        watch_obj = Dictionary()
        mm_obj = Movement()
        has_href = False
        cut_number = re.compile(r'\d+')
        cut_float = re.compile(r'(\d+(\.\d){0,1})')
        href = None
        valid_list = [ul for ul in response.css('.pro-attr') if len(ul.css('li')) > 0]
        for index, ul in enumerate(valid_list):
            try:
                lis = ul.css('li')
                # 基本信息
                if index is 0:
                    watch_obj['number'] = lis[0].css('::text')[1].extract().strip()
                    watch_obj['brand'] = lis[1].css('::text')[1].extract().strip()
                    watch_obj['series'] = lis[2].css('::text')[1].extract().strip()
                    watch_obj['sex'] = lis[4].css('::text')[1].extract().strip()
                # 价格
                elif index is 1:
                    price_types = ['cny', 'euro', 'dollor', 'hkd']
                    for index, li in enumerate(lis):
                        watch_obj[price_types[index]] = li.css('.price::text').extract_first()
                        # 是否有价格并截取评价日期
                        if watch_obj[price_types[index]] is not ' ':
                            watch_obj[price_types[index]] = cut_number\
                                .search(watch_obj[price_types[index]])
                            if watch_obj[price_types[index]] is not None:
                                watch_obj[price_types[index]] = watch_obj[price_types[index]].group(0).strip()
                            watch_obj[price_types[index] + '_date'] = li\
                                .css('.date::text').extract_first().strip()
                        else:
                            watch_obj[price_types[index]] = 0
                # 机芯
                elif index is 2:
                    # request = scrapy.Request('http://jewelry.xbiao.com/', callback=self.test)
                    # yield request
                    href = lis.css('a[href*=jixin]::attr(href)').extract_first()
                    # print(len(lis))
                    if href is not None:
                        has_href = True
                    for li in lis:
                        key = li.css('::text').extract_first().strip()
                        value = li.css('::text')[1].extract().strip()
                        if key.startswith('机芯型号'):
                            mm_obj['name'] = value
                        elif key.startswith('机芯类型'):
                            mm_obj['type'] = value
                        elif key.startswith('出产厂商'):
                            mm_obj['manufacture'] = value
                        elif key.startswith('基础机芯'):
                            mm_obj['basic'] = value
                        elif key.startswith('机芯直径'):
                            diameter = cut_float.search(value)
                            if diameter is not None:
                                mm_obj['diameter'] = diameter.group(0)
                            else:
                                mm_obj['diameter'] = 0
                        elif key.startswith('机芯厚度'):
                            thickness = cut_float.search(value)
                            if thickness is not None:
                                mm_obj['thickness'] = thickness.group(0)
                            else:
                                mm_obj['thickness'] = 0
                        elif key.startswith('振频'):
                            mm_obj['vibration'] = value
                        elif key.startswith('宝石数'):
                            jewels = cut_number.search(value)
                            if jewels is not None:
                                mm_obj['jewels'] = jewels.group(0)
                            else:
                                mm_obj['jewels'] = 0
                        elif key.startswith('动力储备'):
                            power_reserve = cut_number.search(value)
                            if power_reserve is not None:
                                mm_obj['power_reserve'] = power_reserve.group(0)
                            else:
                                mm_obj['power_reserve'] = 0
                        elif key.startswith('零件数'):
                            part_number = cut_number.search(value)
                            if part_number is not None:
                                mm_obj['part_number'] = part_number.group(0)
                            else:
                                mm_obj['part_number'] = 0
                        elif key.startswith('简介'):
                            mm_obj['introduction'] = value
                        elif key.startswith('电池寿命'):
                            mm_obj['battery_life'] = value
                        elif key.startswith('摆轮'):
                            mm_obj['wobbler'] = value
                        elif key.startswith('游丝'):
                            mm_obj['hairspring'] = value
                        elif key.startswith('避震'):
                            mm_obj['suspension'] = value
                elif index is 3:
                    # 手表直径
                    total_diameter = lis[0].css('::text')[1].extract().strip()
                    total_diameter = cut_float.search(total_diameter)
                    if total_diameter is not None:
                        watch_obj['total_diameter'] = total_diameter.group(0)
                    else:
                        watch_obj['total_diameter'] = 0
                    # 表壳
                    shell_thickness = lis[1].css('::text')[1].extract().strip()
                    shell_thickness = cut_float.search(shell_thickness)
                    if shell_thickness is not None:
                        watch_obj['shell_thickness'] = shell_thickness.group(0)
                    else:
                        watch_obj['shell_thickness'] = 0
                    watch_obj['shell_material'] = lis[2].css('::text')[1].extract().strip()
                    # 表盘
                    watch_obj['dial_color'] = lis[3].css('::text')[1].extract().strip()
                    watch_obj['dial_shape'] = lis[4].css('::text')[1].extract().strip()
                    watch_obj['dial_material'] = lis[5].css('::text')[1].extract().strip()
                    # 表镜
                    watch_obj['glass_material'] = lis[6].css('::text')[1].extract().strip()
                    # 表冠
                    watch_obj['crown_material'] = lis[7].css('::text')[1].extract().strip()
                    # 表带
                    watch_obj['band_color'] = lis[8].css('::text')[1].extract().strip()
                    watch_obj['band_material'] = lis[9].css('::text')[1].extract().strip()
                    # 表扣
                    watch_obj['clasp_type'] = lis[10].css('::text')[1].extract().strip()
                    watch_obj['clasp_material'] = lis[11].css('::text')[1].extract().strip()
                    # 背透
                    watch_obj['back_through'] = lis[12].css('::text')[1].extract().strip()
                    # 重量
                    weight = lis[13].css('::text')[1].extract().strip()
                    weight = cut_float.search(weight)
                    if weight is not None:
                        watch_obj['weight'] = shell_thickness.group(0)
                    else:
                        watch_obj['weight'] = 0
                    # 防水深度
                    diving_depth = lis[14].css('::text')[1].extract().strip()
                    diving_depth = cut_float.search(diving_depth)
                    if diving_depth is not None:
                        watch_obj['diving_depth'] = diving_depth.group(0)
                    else:
                        watch_obj['diving_depth'] = 0
            except Exception as e:
                print('Detail:', e, response.url)
                continue
        # 功能
        feature_list = response.css('.func-list span::text').extract()
        watch_obj['feature'] = ",".join(feature_list)
        watch_obj['mm_obj'] = mm_obj
        # 若机芯类型有detail页,则需要follow detail page获取其更详细的数据
        if has_href is True:
            request = scrapy.Request(href, callback=self.parseMovement)
            request.meta['item'] = watch_obj
            yield request
        yield watch_obj

    def parseMovement(self, response):
        """Movement Detail Page"""
        watch_obj = response.meta['item']
        mm_obj = watch_obj['mm_obj']
        cut_number = re.compile(r'\d+')
        cut_float = re.compile(r'(\d+(\.\d){0,1})')
        for ul in response.css('.pro-attr'):
            try:
                lis = ul.css('li')
                for li in lis:
                    key = li.css('::text').extract_first().strip()
                    value = li.css('::text')[1].extract().strip()
                    if key.startswith('出产厂商'):
                        mm_obj['manufacture'] = value
                    elif key.startswith('基础机芯'):
                        mm_obj['basic'] = value
                    elif key.startswith('机芯直径'):
                        diameter = cut_float.search(value)
                        if diameter is not None:
                            mm_obj['diameter'] = diameter.group(0)
                        else:
                            mm_obj['diameter'] = 0
                    elif key.startswith('机芯厚度'):
                        thickness = cut_float.search(value)
                        if thickness is not None:
                            mm_obj['thickness'] = thickness.group(0)
                        else:
                            mm_obj['thickness'] = 0
                    elif key.startswith('振频'):
                        mm_obj['vibration'] = value
                    elif key.startswith('宝石数'):
                        jewels = cut_number.search(value)
                        if jewels is not None:
                            mm_obj['jewels'] = jewels.group(0)
                        else:
                            mm_obj['jewels'] = 0
                    elif key.startswith('动力储备'):
                        power_reserve = cut_number.search(value)
                        if power_reserve is not None:
                            mm_obj['power_reserve'] = power_reserve.group(0)
                        else:
                            mm_obj['power_reserve'] = 0
                    elif key.startswith('零件数'):
                        part_number = cut_number.search(value)
                        if part_number is not None:
                            mm_obj['part_number'] = part_number.group(0)
                        else:
                            mm_obj['part_number'] = 0
                    elif key.startswith('电池寿命'):
                        mm_obj['battery_life'] = value
                    elif key.startswith('摆轮'):
                        mm_obj['wobbler'] = value
                    elif key.startswith('游丝'):
                        mm_obj['hairspring'] = value
                    elif key.startswith('避震'):
                        mm_obj['suspension'] = value
            except:
                print('Movement: Unknown Error!')
                continue
        mm_obj['introduction'] = response.css('.func-list::text').extract_first().strip()
        watch_obj['mm_obj'] = mm_obj
        yield watch_obj
