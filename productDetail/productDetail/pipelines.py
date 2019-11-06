# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from datetime import datetime
from scrapy.exceptions import DropItem
from scrapy.exporters import CsvItemExporter
import redis  # TO DO remove redis
from productDetail import settings
import psycopg2

# Open Redis connection
print("Opening Redis connection")
redis_conn = redis.StrictRedis(host=settings.redis_host,
                               port=settings.redis_port,
                               db=settings.redis_db)

class WriteItemPipeline(object):

    def __init__(self):
        self.filename = self.filename = str(datetime.now()) + 'Amazon_product_detial_reviews.csv'
        try:
            self.connection = psycopg2.connect(**settings.DATABASE)
            self.cursor = self.connection.cursor()
        except Exception as error:
            print("=" * 30)
            print("Connection Error: %s" % error)

    def open_spider(self, spider):
        self.csvfile = open(self.filename, 'wb')
        self.exporter = CsvItemExporter(self.csvfile)
        self.exporter.start_exporting()
        pass

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.csvfile.close()
        if self.connection is not None:
            print("=" * 30)
            print("Closing connection: %s" % self.connection)
            self.connection.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        try:
            self.cursor.execute(
                """INSERT INTO product_detail (asin, listed_date, title, best_sellers_rank, category_sellers_rank) VALUES(%s, %s, %s, %s, %s)""",
                (item['ASIN'], item['listedDate'], item['title'], item['bestSellersRank'], item['categorySellersRank']))
            self.connection.commit()
        except Exception as error:
            self.connection.rollback()
            redis_conn.sadd('ASIN_detail_err', item['ASIN']) # easier to reprocess with the ASIN number
            print("=" * 30)
            print("DatabaseError: %s" % error)
            print(item['ASIN'], item['listedDate'], item['title'], item['bestSellersRank'], item['categorySellersRank'])
        return item
