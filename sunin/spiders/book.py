# -*- coding: utf-8 -*-
import scrapy

from sunin.items import SuninItem


class BookSpider(scrapy.Spider):
    name = 'book'
    allowed_domains = ['book.suning.com', 'list.suning.com', 'product.suning.com']
    start_urls = ['https://book.suning.com/']

    def parse(self, response):
        # 分类获取 列表url
        a_list = response.xpath('//div[@class="menu-item"]//dd/a')
        for a in a_list:
            item = SuninItem()
            # 分类
            item['category'] = a.xpath('./text()').extract_first()
            # 分类 链接
            category_url = a.xpath('./@href').extract_first()
            item['category_url'] = category_url

            yield scrapy.Request(
                url=category_url,
                callback=self.parse_detail,
                meta={
                    'item': item
                }
            )

    def parse_detail(self, response):
        item = response.meta['item']
        a_list = response.xpath('//div[@id="filter-results"]/ul[@class="clearfix"]//a[@class="sellPoint"]')
        item['book_info_list'] = []
        for a in a_list:
            book_url = "https:" + a.xpath('./@href').extract_first()
            yield scrapy.Request(
                url=book_url,
                callback=self.parse_book_detail,
                meta={
                    'item': item
                }
            )

    def parse_book_detail(self, response):
        item = response.meta['item']
        book_dict = {}

        title = response.xpath('//h1[@id="itemDisplayName"]/text()').extract_first().strip()
        # price = response.xpath('//span[@class="mainprice"]/text()').extract_first()
        book_dict['book_name'] = title
        # book_dict['price'] = price
        book_dict['book_url'] = response.url

        item.get('book_info_list').append(book_dict)

        price_url = "https://ds.suning.cn/ds/generalForTile/"

        yield scrapy.Request(
            
        )
