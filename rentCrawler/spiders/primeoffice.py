# -*- coding: utf-8 -*-
import scrapy
from lxml import html
import pudb
pudb.set_trace()

# Define Website Paring Configuration
END = 148
END = 10

HEAD = "http://www.primeoffice.com.hk/rent-office-"
TAIL = ".html?pvc_ids[]=522,523,524,525,573,528,17,552,670,530,689,680,531,533,561,563,538,535,536,602,596,541,0,%20522,%20523,%20524,%20525,%20573,%20528,%2017,%20552,%20670,%20530,%20689,%20680,%20531,%20533,%20561,%20563,%20538,%20535,%20536,%20602,%20596,%20541&size_fr=&size_to=&lease_fr=&lease_to=&sale_fr=&sale_to=&view1=&view2=&view3=&view4=&view5=&deco_fullyfitted=&deco_partialfitted=&deco_ceiling=&deco_ceilingcarpet=&deco_bareshell=&aircon_central=&aircon_independent=&et="
CONFIG = {
    'pages': ['(//a[@class="netvigate"]/text())[last]'],
    'results':'//div[@class="divbox"]',
    'fields':{
        'building_name':['//div[@class="contentlist_address"]//h2/text()'],
        'location': ['//div[@class="contentlist_address"]//h2/following-sibling::div/text()'],
        'floors_views': ['//div[@class="contentlist_unit"]/ul/li/text()'],
        'area':['//div[@class="contentlist_area"]/text()'],
        'reference':['//div[@class="contentlist_address"]/following-sibling::div/text()'],
        'rent':['//p[@class="items rent"]/text()'],
        'price':['//p[@class="items price"]/text()'],

        'rent_at':['(//p[@class="items rent"]/following-sibling::p/text())[1]'],
        'price_at':['(//p[@class="items price"]/following-sibling::p/text())[1]']
    }
}

def fetch_dict(CONFIG, item, _selector):
    '''
    extracts dict data from single row
    '''
    for key,value in CONFIG['fields'].items():
       for x in value:
           x_val = _selector.xpath(x)
           if len(x_val)>0:
               if key == 'floors_views':
                   item[key] = ', '.join(x_val)
                   break
               item[key] = x_val[0].strip()
               break
           else:
               item[key] = None
    return item

class PrimeofficeSpider(scrapy.Spider):
    def __init__(self):
        self.output = "primeoffice.jl"
    name = 'primeoffice'
    allowed_domains = ['primeoffice.com']

    def start_requests(self):
        for page in range(1, END):
            item = {}
            url = HEAD + str(page)+TAIL
            request = scrapy.Request(url=url, callback=self.parse, dont_filter=True)
            item["page"] = page
            request.meta['item'] = dict(item)
            yield request
            
    def parse(self, response):
        item = response.request.meta['item']
        nodes = response.xpath(CONFIG['results']).extract()
        print("Total Nodes: ", len(nodes))
        for node in nodes:
            sel = html.fromstring(node)
            item = fetch_dict(CONFIG, item, sel)
            yield item
