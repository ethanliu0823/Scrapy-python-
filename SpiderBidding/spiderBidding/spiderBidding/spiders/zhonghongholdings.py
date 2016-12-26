# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from spiderBidding.items import SpiderbiddingItem
from scrapy.http import Request
from time import sleep
import re


# 中弘控股股份有限公司
class ZhonghongholdingsSpider(CrawlSpider):
    name = 'zhonghongholdings'
    allowed_domains = ['zhonghongholdings.com']

    # start_urls = ['http://supplier.zhonghongholdings.com/index!zhaoBiaoList.do?type=&projectNameQuery=&start=0&page.size=10']

    def start_requests(self):
        for i in range(0, 10):
            url = 'http://supplier.zhonghongholdings.com/index!zhaoBiaoList.do?type=&projectNameQuery=&start=' + str(
                i) + '&page.size=10'
            yield scrapy.Request(url, self.parse_list)

    # rules = (
    #     Rule(LinkExtractor(allow=r'zhaoBiaoList.do'), callback='parse_item', follow=True),
    #     Rule(LinkExtractor(allow=r'detail.do'), callback='parse_item', follow=True),
    # )

    def parse_list(self, response):
        detail_page_urls = response.xpath("//tr[@class='zblist_new']/td[position()=1]/a/@onclick").re(
            "window.location.href='(.*?)'")
        publish_Time = response.xpath("//tr[@class='zblist_new']/td[position()=2]/text()").extract()
        end_Time = response.xpath("//tr[@class='zblist_new']/td[position()=3]/text()").extract()
        if detail_page_urls is not None:
            for i in range(0, len(detail_page_urls)):
                sleep(1)
                url = detail_page_urls[i]
                yield scrapy.Request(response.urljoin(url), self.parse_detail,
                                     meta={'url': url, 'publist_time': publish_Time[i], 'end_time': end_Time[i]})

    def parse_detail(self, response):
        meta = response.meta
        i = SpiderbiddingItem()
        try:
            i['CompanyId'] = '15791fe7-c047-11e6-9dab-005056a66c04'
            a = re.compile(r'id=(.*)').findall(meta['url'])[0]
            i['OriginId'] = a
            i['ForenoticeTitle'] = response.xpath("/html/body/div[3]/div[1]/h1/div/@title").extract_first()
            i['ContactMan'] = ''
            i['ContactPhone'] = ''
            i['Email'] = ''
            i['OriginalUrl'] = 'http://supplier.zhonghongholdings.com/' + meta['url']
            listYG = response.xpath("/html/body/div[3]/div[2]/p[1]/text()").extract()
            strYG=''
            for j in range(0, len(listYG)):
                strYG = strYG + listYG[j].encode('gbk', 'ignore').decode('gbk', 'ignore') + '\n'
            i['YGText'] = strYG
            i['InviteBidScopeDes']=''
            i['EnterCondition'] = ''
            i['publishTime'] = meta['publist_time']
            i['BmEndDate'] = meta['end_time']
        except Exception as ex:
            i['ForenoticeTitle']=''
        yield i
