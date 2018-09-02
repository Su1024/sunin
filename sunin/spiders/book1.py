# -*- coding: utf-8 -*-
import scrapy
import re
from sunin.items import SuninItem
import json


class BookSpider(scrapy.Spider):
    name = 'book1'
    allowed_domains = ['book.suning.com', 'list.suning.com', 'product.suning.com', 'suning.cn']
    start_urls = ['https://book.suning.com/']
    count = 0
    result = []

    def parse(self, response):
        # 分类获取 列表url
        a_list = response.xpath('//div[@class="menu-item"]//dd/a')
        for a in a_list:
            # 分类 链接
            category_url = a.xpath('./@href').extract_first()
            yield scrapy.Request(
                url=category_url,
                callback=self.parse_list
            )

    #
    def parse_list(self, response):
        a_list = response.xpath('//a[@class="full cart-btn"]')
        vendor = response.xpath('//ul[@class="clearfix"]//li[1]//input[1][@class="hidenInfo"]/@vendor').extract_first()
        url_param_list_1 = []
        url_param_list_2 = []
        goods_list = []

        # https://ds.suning.cn/ds/generalForTile/000000000670439473__2_0070118772,000000000103526450__2_0070078847_-021-2-0070121210-1--ds
        for i, a in enumerate(a_list):
            a_href = a.xpath('./@href').extract_first()

            goods_dict = {}
            res = re.match(r"javascript:addMiniShoppingCart\('(\d+)',(\d+),'(\d+)'", a_href).groups()
            url_param = res[0] + "__2_" + res[2]
            if i % 2 == 0:
                url_param_list_1.append(url_param)
            else:
                url_param_list_2.append(url_param)

            book_name = a.xpath('./../../div[@class="res-info"]//a[@class="sellPoint"]/text()').extract_first().strip()
            goods_dict['name'] = book_name
            goods_dict['id'] = res[0]
            goods_list.append(goods_dict)

        base_url = "https://ds.suning.cn/ds/generalForTile/"

        url_price_str_1 = self.get_url_params(url_param_list_1, vendor)
        url_price_str_2 = self.get_url_params(url_param_list_2, vendor)

        yield scrapy.Request(
            url=base_url + url_price_str_1,
            callback=self.parse_price,
            meta={
                'goods_list': goods_list
            }
        )

        yield scrapy.Request(
            url=base_url + url_price_str_2,
            callback=self.parse_price,
            meta={
                'goods_list': goods_list
            }
        )

    def parse_price(self, response):
        self.count += 1
        text = response.text
        result_dict = json.loads(text)
        self.result.extend(result_dict.get('rs'))
        if self.count > 1:
            good_list = response.meta['goods_list']
            a = {resu['cmmdtyCode']: resu for resu in self.result}
            for good in good_list:
                if good.get('id'):
                    good['price'] = a[good.get("id")]['price']
                    book = SuninItem()
                    book['id'] = good.get('id')
                    book['name'] = good.get('name')
                    book['price'] = good.get('price')
                    yield book

    def get_url_params(self, url_param_list, vendor):
        url_param_str = ",".join(url_param_list)
        url_param_str += '_-021-2-' + vendor + '-1--ds'
        return url_param_str
