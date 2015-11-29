# -*- coding: utf-8 -*-
import scrapy


class ElsevierSpider(scrapy.Spider):
    name = "Elsevier"
    allowed_domains = ["www.elsevier.com"]
    start_urls = (
        'http://www.www.elsevier.com/',
    )

    def parse(self, response):
        pass
