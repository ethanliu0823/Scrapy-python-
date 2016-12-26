# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from spiderBidding.items import SpiderbiddingItem
from time import sleep
import re
import time

# SOHO中国
class SohochinaSpider(CrawlSpider):
    name = 'sohochina'
    allowed_domains = ['sohochina.com']
    start_urls = ['http://pp.sohochina.com/prerfp/index']

    rules = (
        Rule(LinkExtractor(allow=r'/prerfp/index/'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/prerfp/details/id/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        i = SpiderbiddingItem()
        current_url=response.url
        try:
            if(current_url.find('/details/id/')>=0):
                sleep(1)
                i['CompanyId']='415a62f1-c5c5-11e6-8a18-005056a66c04'
                i['OriginId'] = re.compile(r'/details/id/(.*)').findall(current_url)[0]
                i['ForenoticeTitle']=response.xpath('//div[@class="cg_con_l_rwxq_text"]/h1[1]/text()').extract()[0]
                i['ContactMan']=response.xpath('//*[@id="soho_cg"]/div[2]/div/div[2]/p[3]/span[2]/text()').extract()[0]
                i['ContactPhone']=response.xpath('//*[@id="soho_cg"]/div[2]/div/div[2]/p[4]/span[2]/text()').extract()[0]
                i['Email']=response.xpath('//*[@id="soho_cg"]/div[2]/div/div[2]/p[6]/span[2]/text()').extract()[0]
                i['OriginalUrl']=current_url
                info=response.xpath('//pre[1]/text()').extract()
                str_info=''
                for j in range(0,len(info)):
                    str_info+=info[j].encode('gbk', 'ignore').decode('gbk', 'ignore').strip()+'\n'
                print(str_info)
                i['YGText'] =str_info
                i['InviteBidScopeDes'] = ''
                i['EnterCondition']=''
                i['publishTime'] = response.xpath('//*[@id="soho_cg"]/div[2]/div/div[2]/p[2]/span[2]/text()').extract()[0]
                i['BmEndDate'] = response.xpath('//*[@id="soho_cg"]/div[2]/div/div[2]/p[7]/span[2]/text()').extract()[0]+" 18:00:00"
                if(i['BmEndDate'] is None or i['BmEndDate']=='' or time.mktime(time.strptime(i['BmEndDate'],'%Y-%m-%d %H:%M:%S'))<time.time()):
                    i['ForenoticeTitle'] = ''
            else:
                i['ForenoticeTitle']=''
        except Exception as ex:
            i['ForenoticeTitle'] = ''

        yield i
