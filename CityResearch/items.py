# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CityresearchItem(scrapy.Item):
    # define the fields for your item here like:

    name_Chinese = scrapy.Field()
    name_English = scrapy.Field()
    abstract = scrapy.Field()
    doi = scrapy.Field()
    authors_Chinese = scrapy.Field()
    authors_English = scrapy.Field()
    institutions = scrapy.Field()    
    journal_Chinese = scrapy.Field()
    journal_English = scrapy.Field()
    volume = scrapy.Field()
    classify_code = scrapy.Field()
    keywords_Chinese = scrapy.Field()
    keywords_English = scrapy.Field()
    machineclassify_code = scrapy.Field()
    date= scrapy.Field()
    fundings = scrapy.Field()
    pass
