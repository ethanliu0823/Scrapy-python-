# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from time import sleep
import re
from spiderBidding.items import SpiderbiddingItem
import time

#朗诗绿色地产
class LangseaSpider(CrawlSpider):
    name = 'langsea'
    allowed_domains = ['landsea.cn'] # NO port

    # start_urls = [
    #     'http://pr.landsea.cn:38080/ccenrun-front/release/toReleaseTender.htm',
    # ]

    def start_requests(self):
        url = 'http://pr.landsea.cn:38080/ccenrun-front/release/toReleaseTender.htm'
        yield scrapy.Request(url, self.parse_list)

    def parse_list(self, response):
        detail_titles = response.xpath('//div[@class="list-dv"]/ul/li/a/@title').extract()
        detail_urls = response.xpath('//div[@class="list-dv"]/ul/li/a/@href').extract()
        max_page = int(response.xpath('//div[@class="top-page"]/span[position()=2]/text()').re_first(r'共(\d*?)页'))
        # print('page: '+str(max_page))
        for i in range(0, len(detail_urls)):
            sleep(1)
            url = detail_urls[i].strip()
            id = re.compile(r'=(.*)').findall(url)[0]
            bidding_title=detail_titles[i].strip()
            yield scrapy.Request(response.urljoin(url), self.parse_detail,
                                 meta={'bidding_title': bidding_title, 'url': url, 'id': id})

        next_page_url = response.xpath('//div[@class="top-page"]/a[position()=3]/@href').extract_first()
        next_page_id = int(
            response.xpath('//div[@class="top-page"]/a[position()=3]/@href').re_first(r'.*?currentnumber=(\d*?)&'))
        if next_page_url is not None:
            if (next_page_id <= max_page):
                yield scrapy.Request(response.urljoin(next_page_url), self.parse_list)

    def parse_detail(self, response):
        meta = response.meta
        i = SpiderbiddingItem()
        try:
            #/html/body/div[3]/div[2]/div[2]/div[2]/p[14]
            i['CompanyId'] = '8f623599-c26d-11e6-9dab-005056a66c04'
            i['OriginId'] = meta['id']
            i['ForenoticeTitle'] = meta['bidding_title']
            i['ContactMan']=str(response.xpath('//div[@class="detail-dv"]/div[2]/p[13]/text()').re_first(r"联系人：(.*)")).strip()
            i['ContactPhone'] = str(response.xpath('//div[@class="detail-dv"]/div[2]/p[14]/text()').re_first(r"联系电话：(.*)")).strip()
            #/html/body/div[3]/div[2]/div[2]/div[2]/p[15]
            i['Email'] = str(response.xpath('//div[@class="detail-dv"]/div[2]/p[15]/text()').re_first(r"邮箱：(.*)")).strip()
            i['OriginalUrl'] = meta['url']
            # /html/body/div[3]/div[2]/div[2]/div[2]/div[1]
            listYG = response.xpath('//div[@class="detail-dv"]/div[2]/div[1]/text()').extract()
            strYG=''
            for j in range(0, len(listYG)):
                strYG = strYG + listYG[j].encode('gbk', 'ignore').decode('gbk', 'ignore').strip()
            i['YGText'] = strYG
            i['InviteBidScopeDes'] = ''
            # /html/body/div[3]/div[2]/div[2]/div[2]/ul[1]
            #i['EnterCondition'] = str(response.xpath("//div[@class='detail-dv']/div[2]/ul[1]/text()").extract()).strip()
            i['EnterCondition']=''
            i['publishTime'] = str(response.xpath('//div[@class="fb-time"]/text()').re_first(r"发布时间：(.*)")).strip()
            i['BmEndDate'] = str(response.xpath('//div[@class="detail-dv"]/div[2]/p[12]/text()').re_first(r"报名截止时间：(.*)")).strip()

            if(i['BmEndDate'] is None or i['BmEndDate']=='' or time.mktime(time.strptime(i['BmEndDate'],'%Y-%m-%d %H:%M:%S'))<time.time()):
                i['ForenoticeTitle'] = ''
        except Exception as ex:
            print(ex)
            i['ForenoticeTitle'] = ''

        yield i
