# -*- coding: utf-8 -*-
import scrapy
from lxml import html
import csv
import re

import pudb
#pudb.set_trace()

START = 0
STEP = 1
END = 157
HEAD = "http://oir.centanet.com/office/result?postType=rent&distIds="
HEAD1 = "http://oir.centanet.com/office/ptresult?postType=rent&distIDs=129,1,4,51,140,2,3,53,49,9,60,63,58,52,57,54,62,55,59,61,24&floor=0&minPrice=20000&priceType=total&pageIndex="
TAIL = "&priceType=total&minPrice=20000&pageIndex="
_TEST_ID = 1
CAT_FILE = 'configs/kln.config'
CONFIG = {
    'pages':'//div[@class="inputDiv"]/input/@max',
    'results':'//div[contains(@class,"list-iso property")]',
    'fields':{
        'building_name':['//div[@class="name font-std-13 font-mbl-31 bold"]/a/@title'],
        'location': ['//div[@class="street font-std-11"]/text()'],
        'area': ['//div[contains(@class,"dimension")]/text()'],
        'rent':['//div[@class="rent-info"]/span[2]/text()'],
        'rent_unit':['//div[@class="rent-info"]/span[2]/span/text()'],
        'unique_id':['//div[@class="code font-std-11 font-mbl-21"]/text()']

    }
}

def get_url_cat(filepath):
    urls = []
    cats = []
    subcats = []
    with open(filepath, 'rb') as cat_file:
        _content = cat_file.readlines()
        for content in _content:
            content = content.decode('utf-8')
            #content = str(content)
            if content.strip()!='':
                _url = content.split('$')[0]
                _cat = content.split('$')[-1].split('|')[0]
                _sub = content.split('$')[-1].split('|')[0]
                urls.append(_url)
                cats.append(_cat)
                subcats.append(_sub)
    return urls, cats, subcats

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

def extract_digit(element):
    '''
    '''
    try:
        element = int(re.sub("\D", "", element))
    except:
        element = 0
    return element


class CentanetSpider(scrapy.Spider):
    def __init__(self):
        self.output = "centanet.jl"
    name = 'centanet'
    allowed_domains = ['centanet.com']
    start_urls = ['http://centanet.com/']

    def start_requests(self):
        _ids, _locations, _names = get_url_cat(CAT_FILE)
        for _id, _loc, _name in zip(_ids, _locations, _names):
            item = {}
            url = HEAD + str(_id)+TAIL+str(0)
            request = scrapy.Request(url=url, callback=self.parse_mid, dont_filter=True)
            item["city_name"] = _name
            item["location"] = _loc
            item["_id"] = _id
            request.meta['item'] = dict(item)
            yield request
            
    def parse_mid(self, response):
        _item = response.request.meta['item']
        total_pages = response.xpath(CONFIG['pages']).extract()
        if len(total_pages)>0:
            total_pages = extract_digit(total_pages[0])
            total_pages += 1
        else:
            total_pages = 0
        for page in range(0, total_pages):
            item = dict(_item)
            url = HEAD + item["_id"]+TAIL+str(page)
            request = scrapy.Request(url=url, callback=self.parse, dont_filter=True)
            item["page"] = page
            item["location"] = page
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
