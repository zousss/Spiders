# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider
import scrapy
from appStore.items import AppstoreItem,AppmarketItem
import time

#分为主题topic和帖子post。无法显示图片内容
class appStoreSpider(CrawlSpider):
    #用于区别Spider。 该名字必须是唯一的，不可以为不同的Spider设定相同的名字。
    name = "appmarket"
    start_urls = ['http://www.wandoujia.com/search/8781697664906646329']
    baseurl = "http://www.wandoujia.com/search/8781697664906646329"

    #获取1级分类的链接
    def parse(self,response):
        print '[page link]:',response.url
        #print response.xpath('//*[@id="j-search-list"]/li/@class').extract()
        for class_Names in response.xpath('//*[@id="j-search-list"]/li[@class="search-item"]'):
            app_link = class_Names.xpath('div[@class="app-desc"]/h2/a/@href').extract()[0]
            app = scrapy.Request(app_link,callback=self.get_app_info)
            yield app
        for i in range(2,10):
            next_link = self.baseurl+'_page'+str(i)
            next_page = scrapy.Request(next_link,callback=self.parse)
            yield next_page

    #获取app的信息
    def get_app_info(self,response):
        print response.url
        app = AppmarketItem()
        app['app_package'] = response.url.split('/')[-1]
        app_info = response.xpath('//div[@class="container"]/div[@class="detail-wrap "]/div[@class="detail-top clearfix"]')
        app['app_name'] = ''.join(app_info.xpath('div[@class="app-info"]/p/span/text()').extract())
        app['app_download_num'] = ''.join(app_info.xpath('div[@class="num-list"]/span[@class = "item"]/i/@content').extract()).replace('UserDownloads:','')
        app_info_detail = response.xpath('//div[@class="container"]/div[@class="detail-wrap "]/div[@class="cols clearfix"]/div[@class="col-right"]')
        app['app_category'] = ','.join(app_info_detail.xpath('div[@class = "infos"]/dl[@class = "infos-list"]/dd[@class = "tag-box"]/a/text()').extract()).replace(' ','').replace('\n','')
        app['app_update_time'] = ''.join(app_info_detail.xpath('div[@class = "infos"]/dl[@class = "infos-list"]/dd/time/text()').extract())
        app['record_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        yield app