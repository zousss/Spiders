# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider
import scrapy
from appStore.items import AppstoreItem,AppInfoItem,AppDataItem
import re
import time

#分为主题topic和帖子post。无法显示图片内容
class wandoujiaSpider(CrawlSpider):
    #用于区别Spider。 该名字必须是唯一的，不可以为不同的Spider设定相同的名字。
    name = "wandoujia"
    start_urls = ['http://www.wandoujia.com/category/app','http://www.wandoujia.com/category/game']
    baseurl = "http://www.wandoujia.com"
    
    #获取分类的链接
    def parse(self,response):
        for type_href in response.xpath('//div[@class="container"]/ul[@class="clearfix tag-box"]/li'):
            type_link  = type_href.xpath('a/@href').extract()[0]
            type_page = scrapy.Request(type_link,callback=self.parse_app_link)
            yield type_page

    #获取app的链接
    def parse_app_link(self,response):
        print '[PAGE LINK]:',response.url
        type_href = response.xpath('//div[@class="container"]/div[@class="crumb"]/div[@class="second"]/a/@href').extract()[0]
        app_game = type_href.split('/')[-1]
        for link in response.xpath('//div[@class="col-left"]/ul[@id="j-tag-list"]/li'):
            if link.xpath('div[@class="app-desc"]/h2/a/@href').extract():
                app_link = link.xpath('div[@class="app-desc"]/h2/a/@href').extract()[0]
                app = scrapy.Request(app_link,callback=self.get_app_info)
                app.meta['app_game'] = app_game
                yield app
        if re.search(r'\d+\/\d+$',response.url):
            pass
        else:
            pages = response.xpath('//div[@class="pagination"]/div[@class="page-wp roboto"]/a')[-2]
            max_page = pages.xpath('text()').extract()[0]
            for i in range(2,int(max_page)+1):
                page_link = response.url+'/'+str(i)
                page = scrapy.Request(page_link,callback=self.parse_app_link)
                yield page

    #获取app的信息
    def get_app_info(self,response):

        print '[GAME LINK]:',response.url
        app_game = response.meta['app_game']
        appDataItem = AppDataItem()
        appInfoItem = AppInfoItem()

        app_info = response.xpath('//div[@class="container"]/div[@class="detail-wrap "]/div[@class="detail-top clearfix"]')
        app_name = ''.join(app_info.xpath('div[@class="app-info"]/p/span/text()').extract())
        appInfoItem['app_link'] = response.url
        appInfoItem['app_source'] = '豌豆荚'
        appInfoItem['app_game'] = app_game
        appInfoItem['app_package'] = response.url.split('/')[-1]
        appInfoItem['app_img'] = ''.join(app_info.xpath('div[@class="app-icon"]/img/@src').extract())
        appInfoItem['app_name'] = app_name
        app_info_detail = response.xpath('//div[@class="container"]/div[@class="detail-wrap "]/div[@class="cols clearfix"]/div[@class="col-right"]')
        appInfoItem['app_type'] = app_info_detail.xpath('div[@class = "infos"]/dl[@class = "infos-list"]/dd[@class = "tag-box"]/a/text()').extract()[0].strip()
        app_tag = ','.join(app_info_detail.xpath('div[@class = "infos"]/dl[@class = "infos-list"]/dd[3]/div/div[@class="tag-box"]/a/text()').extract()).strip().replace(' ','')
        if app_tag:
            appInfoItem['app_tag'] = ','.join(app_info_detail.xpath('div[@class = "infos"]/dl[@class = "infos-list"]/dd[3]/div/div[@class="tag-box"]/a/text()').extract()).strip().replace(' ','')
        else:
            appInfoItem['app_tag'] = appInfoItem['app_type']
        appInfoItem['app_desc'] = ','.join(response.xpath('//div[@class="container"]/div[@class="detail-wrap "]/div[@class="cols clearfix"]/div[@class="col-left"]/div[@class="desc-info"]/div[@itemprop="description"]/text()').extract()).strip()
        appInfoItem['app_developer']  = ''.join(app_info_detail.xpath('div[@class = "infos"]/dl[@class = "infos-list"]/dd[7]/a/span/text()').extract()) \
            if len(app_info_detail.xpath('div[@class = "infos"]/dl[@class = "infos-list"]/dd[7]/a/span/text()').extract()) \
            else ''.join(app_info_detail.xpath('div[@class = "infos"]/dl[@class = "infos-list"]/dd[7]/span/text()').extract()) \
            + ''.join(app_info_detail.xpath('div[@class = "infos"]/dl[@class = "infos-list"]/dd[7]/a/text()').extract())
        #抓取时间
        appInfoItem['app_size'] = ''.join(app_info_detail.xpath('div[@class = "infos"]/dl[@class = "infos-list"]/dd/text()').extract()[0]).replace(' ','').strip() \
            if len(app_info_detail.xpath('div[@class = "infos"]/dl[@class = "infos-list"]/dd/text()').extract()) \
            else ''
        appInfoItem['app_rate'] = '0'
        appInfoItem['app_download'] = ''.join(app_info.xpath('div[@class="num-list"]/span[@class = "item"]/i/@content').extract()).replace('UserDownloads:','')
        appInfoItem['app_comment'] = ''.join(app_info.xpath('div[@class="num-list"]/a/i/text()').extract())
        appInfoItem['record_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        yield appInfoItem

        appDataItem['app_name'] = app_name
        appDataItem['app_link'] = response.url
        appDataItem['app_source'] = '豌豆荚'
        appDataItem['app_game'] = app_game
        appDataItem['app_size'] = ''.join(app_info_detail.xpath('div[@class = "infos"]/dl[@class = "infos-list"]/dd/text()').extract()[0]).replace(' ','').strip() \
            if len(app_info_detail.xpath('div[@class = "infos"]/dl[@class = "infos-list"]/dd/text()').extract()) \
            else ''
        appDataItem['app_rate'] = '0'
        appDataItem['app_download'] = ''.join(app_info.xpath('div[@class="num-list"]/span[@class = "item"]/i/@content').extract()).replace('UserDownloads:','')
        appDataItem['app_comment'] = ''.join(app_info.xpath('div[@class="num-list"]/a/i/text()').extract())
        appDataItem['record_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        yield appDataItem