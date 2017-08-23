# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from scrapy.conf import settings
from appStore.items import AppstoreItem,AppmarketItem,AppInfoItem,AppDataItem

class AppstorePipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            use_unicode= True,
        )
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        if item.__class__ == AppstoreItem:
            try:
                sql = 'INSERT INTO appstoredata VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                param = (item['app_first_link'],item['app_second_link'],item['app_third_link'],item['app_link'],item['app_name'],item['app_package'], \
                         item['app_category'],item['app_tag'],item['app_icon'],\
                         item['app_size'],item['app_request'],item['app_from'],item['app_download_num'],item['app_install_num'],\
                         item['app_love_num'],item['app_comment_num'],item['app_update_time'],item['record_time'])
                self.cursor.execute(sql,param)
                self.connect.commit()
            except pymysql.Warning,w:
                print "Warning:%s" % str(w)
            except pymysql.Error, e:
                print "Error:%s" % str(e)
        if item.__class__ == AppmarketItem:
            try:
                sql = 'INSERT INTO appmarketdata VALUES(%s,%s,%s,%s,%s,%s)'
                param = (item['app_name'],item['app_package'], \
                         item['app_category'], \
                         item['app_download_num'], \
                         item['app_update_time'],item['record_time'])
                self.cursor.execute(sql,param)
                self.connect.commit()
            except pymysql.Warning,w:
                print "Warning:%s" % str(w)
            except pymysql.Error, e:
                print "Error:%s" % str(e)
        if item.__class__ == AppInfoItem:
            try:
                sql = 'REPLACE INTO appstore_appinfo VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                param = (item['app_source'],item['app_game'],item['app_link'],item['app_name'], \
                         item['app_type'],item['app_tag'],item['app_package'], \
                         item['app_desc'],item['app_developer'],item['app_img'], \
                         item['app_size'],item['app_rate'],item['app_comment'],item['app_download'],item['record_time'])
                self.cursor.execute(sql,param)
                self.connect.commit()
            except pymysql.Warning,w:
                print "Warning:%s" % str(w)
            except pymysql.Error, e:
                print "Error:%s" % str(e)
        if item.__class__ == AppDataItem:
            try:
                sql = 'INSERT INTO appstore_appdata VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                param = (item['app_source'],item['app_game'],item['app_link'],item['app_name'], \
                         item['app_size'],item['app_rate'],item['app_comment'], \
                         item['app_download'],item['record_time'])
                self.cursor.execute(sql,param)
                self.connect.commit()
            except pymysql.Warning,w:
                print "Warning:%s" % str(w)
            except pymysql.Error, e:
                print "Error:%s" % str(e)
        return item