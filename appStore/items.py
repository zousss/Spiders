# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AppstoreItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    app_first_link = scrapy.Field()
    app_second_link = scrapy.Field()
    app_third_link = scrapy.Field()
    app_link = scrapy.Field()
    app_name = scrapy.Field()
    app_package = scrapy.Field()
    app_category = scrapy.Field()
    app_tag = scrapy.Field()
    app_icon = scrapy.Field()
    app_size = scrapy.Field()
    app_request = scrapy.Field()
    app_from = scrapy.Field()
    app_download_num = scrapy.Field()
    app_install_num = scrapy.Field()
    app_love_num = scrapy.Field()
    app_comment_num = scrapy.Field()
    app_update_time = scrapy.Field()
    record_time = scrapy.Field()

class AppmarketItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    app_link = scrapy.Field()
    app_name = scrapy.Field()
    app_package = scrapy.Field()
    app_category = scrapy.Field()
    app_tag = scrapy.Field()
    app_icon = scrapy.Field()
    app_size = scrapy.Field()
    app_request = scrapy.Field()
    app_from = scrapy.Field()
    app_download_num = scrapy.Field()
    app_install_num = scrapy.Field()
    app_love_num = scrapy.Field()
    app_comment_num = scrapy.Field()
    app_update_time = scrapy.Field()
    record_time = scrapy.Field()

class AppInfoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    app_source = scrapy.Field()
    app_game = scrapy.Field()
    app_link = scrapy.Field()
    app_name = scrapy.Field()
    app_type = scrapy.Field()
    app_tag = scrapy.Field()
    app_desc = scrapy.Field()
    app_package = scrapy.Field()
    app_developer = scrapy.Field()
    app_img = scrapy.Field()
    app_size = scrapy.Field()
    app_rate = scrapy.Field()
    app_comment = scrapy.Field()
    app_download = scrapy.Field()
    record_time = scrapy.Field()

class AppDataItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    app_source = scrapy.Field()
    app_game = scrapy.Field()
    app_link = scrapy.Field()
    app_name = scrapy.Field()
    app_size = scrapy.Field()
    app_rate = scrapy.Field()
    app_comment = scrapy.Field()
    app_download = scrapy.Field()
    record_time = scrapy.Field()