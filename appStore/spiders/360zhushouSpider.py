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
import inspect

#分为主题topic和帖子post。无法显示图片内容
class appStoreSpider(CrawlSpider):
    #用于区别Spider。 该名字必须是唯一的，不可以为不同的Spider设定相同的名字。
    name = "360zhushou"
    start_urls = ['http://zhushou.360.cn/list/index/cid/2','http://zhushou.360.cn/list/index/cid/1']
    baseurl = "http://zhushou.360.cn"

    #获取1级分类的链接
    def parse(self,response):
        print '[START LINK]:',response.url
        print '[now executing:]',inspect.stack()[1][1],' line:',inspect.stack()[1][2]
        #获取不同类型链接
        for type_href in response.xpath('//ul[@class="select"]/li[1]/a')[1:]:
            type_link = self.baseurl+type_href.xpath('@href').extract()[0]
            app_type = type_href.xpath('text()').extract()[0]
            type_page = scrapy.Request(type_link,callback=self.parse_type_page)
            type_page.meta['app_type'] = app_type
            yield type_page

    def parse_type_page(self,response):
        #获取分页链接
        print '[PAGE LINK]:',response.url
        print '[now executing:]',inspect.stack()[1][1],' line:',inspect.stack()[1][2]
        app_type = response.meta['app_type']
        if re.search(r'page=',response.url):
            pass
        else:
            driver = webdriver.PhantomJS()
            driver.get(response.url)
            content = driver.page_source
            max_page = Selector(text = content).xpath('//div[@id="pages_pg_2"]/div[@class="number"]/div[7]/a/text()').extract()[0]
            for i in range(2,int(max_page)+61):
                next_link = response.url+'?page='+ str(i)
                next_page = scrapy.Request(next_link,callback=self.parse_type_page)
                next_page.meta['app_type'] = app_type
                yield next_page
            driver.quit()
        #获取游戏链接
        for game in response.xpath('//*[@id="iconList"]/li'):
            game_link = self.baseurl+game.xpath('a[1]/@href').extract()[0]
            game_info = scrapy.Request(game_link,callback=self.parse_game_info)
            game_info.meta['app_type'] = app_type
            yield game_info

    #获取app的信息
    def parse_game_info(self,response):
        print '[GAME LINK]:',response.url
        print '[now executing:]',inspect.stack()[1][1],' line:',inspect.stack()[1][2]
        #获取评论数量http://comment.mobilem.360.cn/comment/getComments?baike=%E5%BC%80%E5%BF%83%E6%B6%88%E6%B6%88%E4%B9%90+Android_com.happyelements.AndroidAnimal
        app_game = ''
        game_name = response.xpath('//*[@id="app-name"]/span/text()').extract()[0]
        download_link = ','.join(response.xpath('//*[@id="app-info-panel"]/div/dl/dd/a/@href').extract()).strip()
        app_package =  download_link.split('/')[-1].split('_')[0]
        if response.xpath('/html/body/div[2]/ul/li[@class="cur"]/a/text()').extract()[0] == u'装软件':
            app_game = 'app'
        if response.xpath('/html/body/div[2]/ul/li[@class="cur"]/a/text()').extract()[0] == u'玩游戏':
            app_game = 'game'
        comments_link = "http://comment.mobilem.360.cn/comment/getComments?baike="+urllib.quote(game_name.strip().encode('utf8'))+'+Android_'+app_package
        user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.101 Safari/537.36"
        headers = { 'User-Agent' : user_agent }
        req = urllib2.Request(comments_link, headers = headers)
        content = urllib2.urlopen(req,timeout=10).read()
        comments = json.loads(content)['data']['total']

        appDataItem = AppDataItem()
        appInfoItem = AppInfoItem()

        appDataItem['app_name'] = response.xpath('//*[@id="app-name"]/span/text()').extract()[0]
        appDataItem['app_link'] = response.url
        appDataItem['app_source'] = '360手机助手'
        appDataItem['app_game'] = app_game
        appDataItem['app_size'] = response.xpath('//*[@id="app-info-panel"]/div/dl/dd/div/span[4]/text()').extract()[0]
        appDataItem['app_rate'] = response.xpath('//*[@id="app-info-panel"]/div/dl/dd/div/span[1]/text()').extract()[0]
        appDataItem['app_comment'] = comments
        download_num = response.xpath('//*[@id="app-info-panel"]/div/dl/dd/div/span[3]/text()').extract()[0]
        appDataItem['app_download'] = download_num
        appDataItem['record_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        yield appDataItem

        appInfoItem['app_name'] = response.xpath('//*[@id="app-name"]/span/text()').extract()[0]
        appInfoItem['app_link'] = response.url
        appInfoItem['app_source'] = '360手机助手'
        appInfoItem['app_game'] = app_game
        appInfoItem['app_type'] = response.meta['app_type']
        appInfoItem['app_tag'] = ','.join(response.xpath('//div[@class="app-tags"]/a/text()').extract()).strip()
        appInfoItem['app_desc'] = ','.join(response.xpath('//*[@id="html-brief"]/p[1]/text()').extract()).strip()+','.join(response.xpath('//*[@id="sdesc"]/div/text()').extract()).strip()
        appInfoItem['app_package'] = app_package
        appInfoItem['app_developer'] = ''.join(response.xpath('//*[@id="sdesc"]/div/div/table/tbody/tr[1]/td[1]/text()').extract()).strip()
        appInfoItem['app_img'] = ''.join(response.xpath('//*[@id="app-info-panel"]/div/dl/dt/img/@src').extract())
        #添加数据信息
        appInfoItem['app_size'] = response.xpath('//*[@id="app-info-panel"]/div/dl/dd/div/span[4]/text()').extract()[0]
        appInfoItem['app_rate'] = response.xpath('//*[@id="app-info-panel"]/div/dl/dd/div/span[1]/text()').extract()[0]
        appInfoItem['app_comment'] = comments
        appInfoItem['app_download'] = download_num
        appInfoItem['record_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        yield appInfoItem


