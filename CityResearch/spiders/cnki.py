# -*- coding: utf-8 -*-
import scrapy


class CnkiSpider(scrapy.Spider):
    name = "cnki"
    allowed_domains = ["http://www.cnki.net/"]
    start_urls = (
        'http://www.http://www.cnki.net//',
    )

    def parse(self, response):
        pass
