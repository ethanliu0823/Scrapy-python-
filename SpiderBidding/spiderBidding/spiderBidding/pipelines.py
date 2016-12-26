# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging
from services.base import Base

base = Base()
class SpiderbiddingPipeline(object):
    def process_item(self, item, spider):
        conn, cor = base.connDB()
        try:
            o_id=item['OriginId']
            sql="""select OriginId From dotnet_operation.dc_InviteBidForenotice where OriginId=%s"""
            cor.execute(sql,o_id)
            result=cor.fetchall()

            if(len(result)==0):
                insertSql="""INSERT INTO dotnet_operation.dc_InviteBidForenotice(Id,CompanyId,OriginId,ForenoticeTitle,
                          ContactMan,ContactPhone,Email,OriginalUrl,YGText,InviteBidScopeDes,
                          EnterCondition,PublishTime,BmEndDate)
                          VALUES(UUID(),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                cor.execute(insertSql,(item['CompanyId'],item['OriginId'],str(item['ForenoticeTitle']).encode('utf8','ignore'),
                                       item['ContactMan'],item['ContactPhone'],item['Email'],item['OriginalUrl'],str(item['YGText']).encode('utf8','ignore'),str(item['InviteBidScopeDes']).encode('utf8','ignore'),
                                       item['EnterCondition'],item['publishTime'],item['BmEndDate'] ))
                conn.commit()
                base.connClose(conn, cor)
                print('inserting operation is successfull!!!!')
        except Exception as e:
            logging.exception(e)
            conn.rollback()
            base.connClose(conn,cor)
        return item

    # def process_item(self, item, spider):
    #     # return item
    #
    #     print(item["contact"])
    #     print(item['publishTime'])
    #     print(item['registerEndTime'])
    #     print(item['title'])
    #     # print(item['info'])
    #     # print(item['url'])
