# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider
import scrapy
from selenium import webdriver
import re
from scrapy.selector import Selector
from appStore.items import AppInfoItem,AppDataItem
import time
import json
import urllib
import urllib2

#分为主题topic和帖子post。无法显示图片内容
class appStoreSpider(CrawlSpider):
    #用于区别Spider。 该名字必须是唯一的，不可以为不同的Spider设定相同的名字。
    name = "tencentapp"
    start_urls = ['http://sj.qq.com/myapp/category.htm?orgame=1','http://sj.qq.com/myapp/category.htm?orgame=2']
    appurl = "http://sj.qq.com/myapp/"
    typeurl = "http://sj.qq.com/myapp/category.htm"

    #获取1级分类的链接
    def parse(self,response):
        print '[START LINK]:',response.url
        #获取分页链接
        for type_href in response.xpath('//ul[@class="menu"]/li[1]/ul[@class="menu-junior"]/li')[1:-2]:
            type_link = self.typeurl+type_href.xpath('a/@href').extract()[0]
            if re.search(r'\?',type_link):
                type_page = scrapy.Request(type_link,callback=self.parse_type_page)
                yield type_page

    def parse_type_page(self,response):
        app_game = ''
        if re.search(r'orgame=1',response.url):
            app_game = 'app'
        else:
            app_game = 'game'
        for i in range(10):
            app_page_link = 'http://sj.qq.com/myapp/cate/appList.htm?'+re.search(r'\?(.*)',response.url).group(1)+'&pageSize=20&pageContext='+str(i*20+1)
            app_json_info = scrapy.Request(app_page_link,callback=self.parse_json_app_info)
            app_json_info.meta['app_game'] = app_game
            yield app_json_info

    #获取json的信息
    def parse_json_app_info(self,response):
        print '[JSON LINK]:',response.url
        app_game = response.meta['app_game']
        game_infos = json.loads(response.body_as_unicode())['obj']
        for game_info in game_infos:
            app_package = game_info['pkgName']
            app_download = game_info['appDownCount']
            app_comment = game_info['appRatingInfo']['ratingCount']
            app_name = game_info['appName']
            app_rate = game_info['averageRating']

            app_link = 'http://sj.qq.com/myapp/detail.htm?apkName='+app_package
            app_info = scrapy.Request(app_link,callback=self.parse_app_info)
            app_info.meta['app_game'] = app_game
            app_info.meta['app_download'] = app_download
            app_info.meta['app_comment'] = app_comment
            app_info.meta['app_package'] = app_package
            app_info.meta['app_name'] = app_name
            app_info.meta['app_rate'] = app_rate
            yield app_info

    #获取app的信息
    def parse_app_info(self,response):
        print '[GAME LINK]:',response.url
        app_game = response.meta['app_game']
        app_download = response.meta['app_download']
        app_comment = response.meta['app_comment']
        app_package = response.meta['app_package']
        app_name = response.meta['app_name']
        app_rate = response.meta['app_rate']

        appDataItem = AppDataItem()
        appInfoItem = AppInfoItem()

        appInfoItem['app_name'] = app_name
        appInfoItem['app_link'] = response.url
        appInfoItem['app_source'] = '应用宝'
        appInfoItem['app_game'] = app_game
        appInfoItem['app_type'] = ''.join(response.xpath('//*[@id="J_DetCate"]/text()').extract())
        appInfoItem['app_tag'] = ','.join(response.xpath('//*[@id="J_DetCate"]/text()').extract()).strip()
        appInfoItem['app_desc'] = ','.join(response.xpath('//*[@id="J_DetAppDataInfo"]/div[1]/text()').extract()).strip()
        appInfoItem['app_package'] = app_package
        appInfoItem['app_developer'] = ''.join(response.xpath('//*[@id="J_DetDataContainer"]/div/div[3]/div[6]/text()').extract()).strip()
        appInfoItem['app_img'] = ''.join(response.xpath('//*[@id="J_DetDataContainer"]/div/div[1]/div[1]/img/@src').extract())
        appInfoItem['app_size'] = response.xpath('//*[@id="J_DetDataContainer"]/div/div[1]/div[2]/div[3]/div[3]/text()').extract()[0]
        appInfoItem['app_rate'] = str(app_rate)
        appInfoItem['app_comment'] = str(app_comment)
        appInfoItem['app_download'] = app_download
        appInfoItem['record_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        yield appInfoItem

        appDataItem['app_name'] = app_name
        appDataItem['app_link'] = response.url
        appDataItem['app_source'] = '应用宝'
        appDataItem['app_game'] = app_game
        appDataItem['app_size'] = response.xpath('//*[@id="J_DetDataContainer"]/div/div[1]/div[2]/div[3]/div[3]/text()').extract()[0]
        appDataItem['app_rate'] = str(app_rate)
        appDataItem['app_comment'] = str(app_comment)
        appDataItem['app_download'] = app_download
        appDataItem['record_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        yield appDataItem


