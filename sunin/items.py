# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SuninItem(scrapy.Item):
    # 图书分类
    category = scrapy.Field()
    # 分类链接
    category_url = scrapy.Field()
    # 书名
    book_info_list = scrapy.Field()

