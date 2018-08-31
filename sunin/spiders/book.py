# -*- coding: utf-8 -*-
import scrapy


class BookSpider(scrapy.Spider):
    name = 'book'
    allowed_domains = ['book.suning.com']
    start_urls = ['http://book.suning.com/']

    def parse(self, response):
        pass
