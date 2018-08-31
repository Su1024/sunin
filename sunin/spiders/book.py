# -*- coding: utf-8 -*-
import scrapy


class BookSpider(scrapy.Spider):
    name = 'book'
    allowed_domains = ['book.suning.com']
    start_urls = ['https://book.suning.com/']

    def parse(self, response):
        # 分类获取 列表url
        div_list = response.xpath('//div[@class="menu-item"]')
        for div in div_list:
            div.xpath('')

        pass
