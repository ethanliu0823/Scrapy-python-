# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from spiderBidding.items import SpiderbiddingItem
from scrapy.http import Request

# 金科需要post。。
class JinkeSpider(CrawlSpider):
    name = 'jinke'
    allowed_domains = ['jinke.com']
    #start_urls = ['http://cz.jinke.com:8000/']


    def start_requests(self):
        ua={"User-Agent":'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 Safari/537.36 SE 2.X MetaSr 1.0'}
        yield Request('http://cz.jinke.com:8000',headers=ua)

    rules = (
        Rule(LinkExtractor(allow=r'NoticeDetail.aspx'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'Notice.aspx'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        i = SpiderbiddingItem()
        
        # try:
        i["contact"]=response.xpath('//span[@id="ctl00_ContentPlaceHolder1_lblContactMan"]/text()')
        i['mobile']=response.xpath('//*[@id="ctl00_ContentPlaceHolder1_lblMobilePhone"]/text()')
        i['publishTime']=response.xpath('//*[@id="ctl00_ContentPlaceHolder1_lblBgnTime"]/text()')
        i['registerEndTime']=response.xpath('//*[@id="ctl00_ContentPlaceHolder1_lblBmEndDate"]/text()')
        i['title']=response.xpath('//*[@id="ctl00_ContentPlaceHolder1_lblForenoticeTitle"]/text()')
        # i['info']=response.xpath('//*[@id="aspnetForm"]/div[6]/div/div[1]/table/tbody/tr[7]/td[2]/text()')
        # except Exception as ex:
        #     yield i
        yield i
