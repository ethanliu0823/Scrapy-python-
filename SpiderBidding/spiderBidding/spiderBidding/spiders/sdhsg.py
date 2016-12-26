# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from time import sleep
from spiderBidding.items import SpiderbiddingItem
from scrapy.http import Request
import uuid
import logging

#页面极不规律(列表中很多通知之类的，详情页也应该是随意格式)，没有规则 无法程序爬取
class SdhsgSpider(CrawlSpider):
    name = 'sdhsg'
    allowed_domains = ['sdhsg.com']

    #start_urls = ['http://www.sdhsg.com/']

    rules = (
        Rule(LinkExtractor(allow=r'media_tz.jsp'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'news/page.jsp'), callback='parse_item', follow=True),

    )

    def start_requests(self):
        ua={"User-Agent":'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 Safari/537.36 SE 2.X MetaSr 1.0'}
        yield Request('http://www.sdhsg.com/main/news/media_tz.jsp?page=1&id=12',headers=ua)

    def parse_item(self, response):
        i = SpiderbiddingItem()
        i['Id']=str(uuid.uuid1())
        i['CompanyId']='c1710467-c0e6-11e6-9dab-005056a66c04'
        try:
            i['ForenoticeTitle'] = response.xpath('//div[@class="corner"]/h2/text()').extract_first()
            if(i['ForenoticeTitle'].find('结果公示')<=0 or i['ForenoticeTitle'].find('招聘公告')<0):
                print(i['ForenoticeTitle'])
                i['ContactMan'] = response.xpath('//*[@id="content"]/table[8]/tbody/tr[5]/td[2]/p/span/text()').extract_first()
                i['ContactPhone'] = response.xpath('//*[@id="content"]/table[8]/tbody/tr[6]/td[2]/p/span').extract_first()
                i['publishTime'] = response.xpath('//div[@class="corner"]/div[first()]/h3/text()').extract_first().strip().replace('年','-').replace('月','-').replace('日','-')
                # i['publishTime']='2016-12-13'
                i['BmEndDate']='2016-12-23'
                i['source']=1
                yield i
        except Exception as msg:
            logging.error(msg)


        # 构造“下一页”
        next_page_urls = response.xpath('//table/tbody/tr/td/div/p/a/@href').extract()
        if next_page_urls is not None:
            for next_page_url in next_page_urls:
                if(next_page_url=='page.jsp?id=5887' or
                           next_page_url=='page.jsp?id=3675' or
                           next_page_url=='page.jsp?id=7176' or
                           next_page_url=='page.jsp?id=7171'):
                    continue;
                sleep(1)
                yield scrapy.Request(response.urljoin(next_page_url))
