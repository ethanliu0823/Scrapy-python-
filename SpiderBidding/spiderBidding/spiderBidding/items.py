# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderbiddingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Id = scrapy.Field()
    CompanyId = scrapy.Field()
    OriginId = scrapy.Field()
    ForenoticeTitle = scrapy.Field()
    ContactMan = scrapy.Field()
    ContactPhone = scrapy.Field()
    Email = scrapy.Field()
    InviteBidScopeDes = scrapy.Field()
    publishTime = scrapy.Field()
    BmEndDate = scrapy.Field()
    source = scrapy.Field()
    OriginalUrl = scrapy.Field()
    YGText = scrapy.Field()
    EnterCondition = scrapy.Field()
    pass
