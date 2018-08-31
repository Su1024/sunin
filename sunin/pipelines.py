# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import *


class SuninPipeline(object):

    def open_spider(self, spider):
        client = MongoClient(host='127.0.0.1', port=27017)
        sunin = client.sunin
        self.book = sunin.book

    def process_item(self, item, spider):
        self.book.insert(dict(item))
        return item
