# -*- coding: utf-8 -*-
"""
    for description
"""
import pymysql

class Base:

    def __init__(self):
        pass

    def  connDB(self):                              #连接数据库
        conn=pymysql.connect(host="10.5.7.109",port=3306, user="mytst",passwd="mytst",db="dotnet_operation");
        #conn=pymysql.connect(host="127.0.0.1",port=3306, user="root",passwd="123456",db="dotnet_operation");
        cur=conn.cursor();
        return (conn,cur);

    def exeUpdate(self,conn, cur, sql):  # 更新或插入操作
        sta = cur.execute(sql);
        conn.commit();
        return (sta);

    def exeDelete(self,conn, cur, IDs):  # 删除操作
        sta = 0;
        for eachID in IDs.split(' '):
            sta += cur.execute("delete from dotnet_operation.dc_InviteBidForenotice where Id=%d" % (int(eachID)));
        conn.commit();
        return (sta);

    def exeQuery(self,cur, sql):  # 查找操作
        cur.execute(sql);
        return (cur);

    def connClose(self,conn, cur):  # 关闭连接，释放资源
        cur.close();
        conn.close();