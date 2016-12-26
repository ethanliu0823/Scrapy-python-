# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from spiderBidding.items import SpiderbiddingItem
from time import sleep
import re
import time

class ZaztbSpider(CrawlSpider):
    name = 'zaztb'
    allowed_domains = ['zaztb.com']
    start_urls = ['http://www.zaztb.com/bidForetellList.asp']

    rules = (
        Rule(LinkExtractor(allow=r'bidForetellList.asp'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'bidView.asp'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        i = SpiderbiddingItem()
        current_url=response.url
        try:
            if(current_url.find('bidView.asp')>=0):
                #sleep(1)
                print(response.xpath('//table[@width="584"]/tr[7]/td[2]/text()').extract())
                print(response.xpath('//table[@width="584"]/tr[8]/td[2]/text()').extract())
                i['CompanyId']='3a5ff36f-c652-11e6-8a18-005056a66c04'
                i['OriginId'] = re.compile(r'bidView.asp\?id=(\d+)').findall(current_url)[0]
                i['ForenoticeTitle']=response.meta['link_text']
                i['ContactMan'] = response.xpath('//table[@width="584"]/tr[7]/td[2]/text()').extract()[0]
                i['ContactPhone'] = response.xpath('//table[@width="584"]/tr[8]/td[2]/text()').extract()[0]
                i['Email']=''
                i['OriginalUrl']=current_url

                list_yg=response.xpath('//table[@width="584"]/tr[9]/td[2]').extract()
                str_yg=''
                for j in range(0,len(list_yg)):
                    str_yg +=list_yg[j].encode('gbk', 'ignore').decode('gbk', 'ignore').strip().replace('\r','').replace('\n','')
                    str_yg = re.sub('<[^>]+>', '', str_yg)

                # print(str_yg)
                # rh = RemoveHtml()
                # str_yg=rh(str_yg)
                # print("1111111111111"+str_yg)
                str_yg = str_yg.replace(r'\u3000', '')
                i['YGText'] = str_yg
                i['InviteBidScopeDes'] = ''
                i['EnterCondition']=''
                i['publishTime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                date_ends=re.compile(r'报名截止[日|期|时|间]{2}：\s*(\d+年\d+月\d+日)').findall(str_yg)
                if(len(date_ends)>0):
                    i['BmEndDate'] = date_ends[0].replace('年','-').replace('月','-').replace('日','')+" 18:00:00"
                else:
                    i['BmEndDate'] = ''
                if(i['BmEndDate'] is None or i['BmEndDate']=='' or time.mktime(time.strptime(i['BmEndDate'],'%Y-%m-%d %H:%M:%S'))<time.time()):
                    i['ForenoticeTitle'] = ''
            else:
                i['ForenoticeTitle']=''
        except Exception as ex:
            i['ForenoticeTitle'] = ''

        yield i
