# -*- coding: utf-8 -*-
import scrapy


class WanfangSpider(scrapy.Spider):
    name = "wanfang"
    allowed_domains = ["http://www.wanfangdata.com.cn/"]
    start_urls = (
        'http://www.http://www.wanfangdata.com.cn//',
    )

    def parse(self, response):
        pass
