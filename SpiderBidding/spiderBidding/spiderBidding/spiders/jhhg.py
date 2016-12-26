# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from spiderBidding.items import SpiderbiddingItem
from time import sleep
import re
import time

#济高控股
class JhhgSpider(CrawlSpider):
    name = 'jhhg'
    allowed_domains = ['jhhg.net.cn']

    def start_requests(self):
        url = 'http://www.jhhg.net.cn/xwzx/tzgg/index.htm'
        yield scrapy.Request(url, self.parse_list)

        max_page = 10
        for i in range(1, max_page):
            url = 'http://www.jhhg.net.cn/xwzx/tzgg/index' + str(i) + '.htm'
            yield scrapy.Request(url, self.parse_list)
        yield scrapy.Request(url, self.parse_list)

    def parse_list(self, response):
        detail_titles = response.xpath('//a[@title]/@title').extract()
        detail_urls = response.xpath('//a[@title]/@onclick').re(r"window.open\('(.*?)'")
        detail_publish_times=response.xpath("//td[@width='89']/text()").extract()

        for i in range(0, len(detail_urls)):
            #sleep(1)
            title = detail_titles[i]
            url = detail_urls[i]
            oid = re.compile('\d+').findall(url)[0]
            yield scrapy.Request(response.urljoin(url), self.parse_detail,
                                 meta={'bidding_title': title, 'id': oid, 'publist_time':detail_publish_times[i].strip()})

    def parse_detail(self, response):
        meta = response.meta
        i = SpiderbiddingItem()
        try:
            i['CompanyId'] = 'dba22fcb-c36e-11e6-9dab-005056a66c04'
            i['OriginId'] = meta['id']
            i['ForenoticeTitle'] = meta['bidding_title']

            #联系人
            contact=response.xpath("//table[@id='table32']/tr[position()=2]/td[position()=1]").re('联[\s|&nbsp;]*系[\s|&nbsp;]*人：[\s|&nbsp;|]*?[<U>]*(.*?)<')
            str_contact=''
            for j in range(0,len(contact)):
                temp=contact[j].encode('gbk', 'ignore').decode('gbk', 'ignore').replace('联系人','').replace('：','')
                str_contact+=" "+ temp
            i['ContactMan'] = str_contact.replace('u>','')

            #电话
            contact_phone = response.xpath("//table[@id='table32']/tr[position()=2]/td[position()=1]").re(
                '电[\s|&nbsp;]*话：[\s|&nbsp;]*?[<U>]*(.*?)<')
            str_contact_phone=''
            for k in range(0,len(contact_phone)):
                temp2=contact_phone[k].encode('gbk', 'ignore').decode('gbk', 'ignore').replace('电话','').replace('：','')
                str_contact_phone+=" "+ temp2
            i['ContactPhone']=str_contact_phone.replace('u>','')


            i['Email'] = ''
            i['OriginalUrl'] = response.url
            list_yg = response.xpath("//table[@id='table32']/tr[position()=2]/td[position()=1]").extract()
            str_yg=''
            for k in range(0,len(list_yg)):
                str_yg += list_yg[j].encode('gbk', 'ignore').decode('gbk', 'ignore').strip().replace('\r', '').replace(
                    '\n', '')
                str_yg = re.sub('<[^>]+>', '', str_yg)

            i['YGText'] = str_yg
            i['InviteBidScopeDes'] = ''
            i['EnterCondition']=''
            i['publishTime'] = meta['publist_time']
            #截止报名时间
            end_time = response.xpath("//table[@id='table32']/tr[position()=2]/td[position()=1]").re_first(
                '[\d|\s|&nbsp;]+日至([\d|\s|&nbsp;]+年[\d|\s|&nbsp;]+月[\d|\s|&nbsp;]+日)')

            if(end_time is not None and end_time !=''):
                i['BmEndDate']=end_time.replace('年','-').replace('月','-').replace('日','')+" 18:00:00"
            else:
                i['BmEndDate']=''
                i['ForenoticeTitle']=''

            if(i['BmEndDate'] is None or i['BmEndDate']=='' or time.mktime(time.strptime(i['BmEndDate'],'%Y-%m-%d %H:%M:%S'))<time.time()):
                i['ForenoticeTitle'] = ''
        except Exception as ex:
            print(ex)
            i['ForenoticeTitle'] = ''

        yield i
