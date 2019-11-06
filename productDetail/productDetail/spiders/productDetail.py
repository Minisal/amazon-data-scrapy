#! /usr/local/bin/python3

from scrapy import Spider
from scrapy import Request
from scrapy.selector import Selector
from scrapy.shell import inspect_response
from scrapy.crawler import CrawlerProcess
from scrapy_proxies import *
from datetime import datetime
import csv
import numpy

import redis
from productDetail import settings
from productDetail.items import ProductdetailItem

# Open Redis connection
redis_conn = redis.StrictRedis(host=settings.redis_host,
                               port=settings.redis_port,
                               db=settings.redis_db)




class ProductDetailSpider(Spider):
    name = "productDetail"
    allowed_urls = ['https://www.amazon.com']
    start_urls = []

    def start_requests(self):


        while redis_conn.scard('Product_URL') > 0:
            product_url = redis_conn.spop('Product_URL').decode("utf-8")
            print("=" * 30)
            print("Product_URL: ", product_url)
            first_page_product_detail_URL = product_url
            yield Request(first_page_product_detail_URL, self.parse, meta={'cookiejar': numpy.random.randint(1000)})


    def parse(self, response):


        ASIN = response.xpath('//*[@id="ASIN"]/@value').extract()  # 'B075XLWML4'


        try:
            listedDate = response.xpath('//*[@id="productDetailsTable"]/tbody/tr/td/div/ul/li[2]/text()').extract() 
        except:
            print("=" * 30)
            print("No listed date for product: ", ASIN)
            listedDate = " "

        try:
            title = response.xpath('//*[@id="productTitle"]/text()').extract()
        except:
            print("=" * 30)
            print("No Title for product: ", ASIN)
            title = " "

        try:
            bestSellersRank = response.xpath('//*[@id="productDetails_detailBullets_sections1"]/tbody/tr[10]/td/span/span[1]/text()').extract()[1]  # first element is 'by' (by Arris)
        except:
            try:
                bestSellersRank = response.xpath('//*[@id="SalesRank"]/text()').extract()
            except:
                print("=" * 30) 
                print("No best sellers rank for product: ", ASIN)
                bestSellersRank = " "

#        ranklist = response.xpath('//*[@id="SalesRank"]/ul')
#        print (ranklist)
#        for index in range(5):
#            rank = rank.xpath('/li['+index+']/span[1]/text()').extract() 
#            category = rank.xpath('/li['+index+']span[2]/a/text()').extract()
#            categoryRank = rank + " in " + category + ";"
#            categorySellersRank = categorySellersRank + categoryRank
        

            
        item = ProductdetailItem()
        item['ASIN'] = ASIN
        item['listedDate'] = listedDate
        item['title'] = title
        item['bestSellersRank'] = bestSellersRank
#        item['categorySellersRank'] = categorySellersRank
        yield item
