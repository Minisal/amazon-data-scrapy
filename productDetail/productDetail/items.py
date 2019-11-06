# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductdetailItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    ASIN = scrapy.Field()
    listedDate = scrapy.Field()
    bestSellersRank = scrapy.Field()
    categorySellersRank = scrapy.Field()
    title = scrapy.Field()
