# -*- coding: utf-8 -*-
import scrapy
import extractor


HEAD = "https://www.midlandici.com.hk/ics/property/find/office/lease?dist_code[]=TST&dist_code[]=MOK&dist_code[]=TSE&dist_code[]=TSI&dist_code[]=JOR&dist_code[]=PRE&dist_code[]=YMT&dist_code[]=TKT&dist_code[]=CSW&dist_code[]=LCK&dist_code[]=HUH&dist_code[]=SPK&dist_code[]=KWT&dist_code[]=KOB&page="

END = 72
CONFIG = {
    'results': '//div[contains(@class,"list-group-item")]',
    'fields':{
        'building_name':['//span[@class="building"]/a[1]/text()'],
        'location': ['//span[@class="district"]/a/text()'],
        'area': ['//p[@class="list-group-item-area"]/a/text()'],
        'price':['//p[@class="list-group-item-rent"]//span[@class="rent"]/text()'],
    }
}

class MidlandSpider(scrapy.Spider):
    def __init__(self):
        self.output = "midland.jl"
    name = 'midland'
    allowed_domains = ['midlandici.com']

    def start_requests(self):
        for page in range(1, END):
            item = {}
            url = HEAD + str(page)
            request = scrapy.Request(url=url, callback=self.parse, dont_filter=True)
            item["page"] = page
            request.meta['item'] = dict(item)
            yield request

    def parse(self, response):
        item = response.request.meta['item']
        nodes = response.xpath(CONFIG['results']).extract()
        print("Total Nodes: ", len(nodes))
        for node in nodes:
            item = extractor.fetch_dict(CONFIG, item, node)
            yield item
