# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RosiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    projectName = scrapy.Field()  # 爬虫名称, 用于存储的时候归类
    topicName = scrapy.Field()  # 每个图片合集名称
    picUrlList = scrapy.Field()  # 图片链接
    picPath = scrapy.Field()
