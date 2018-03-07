# -*- coding: utf-8 -*-

import scrapy
import urlparse
from rosi.items import RosiItem


class Rosmm8picSpider(scrapy.Spider):
    name = 'rosmm8pic'
    allowed_domains = ['rosmm8.com']
    start_urls = ['https://www.rosmm8.com/rosimm/']

    def parse(self, response):
        nextPage = response.xpath('//script/text()').re(r'\w+\d+\.\w+')[-2:-1]  # 下一页主题链接
        for line in response.xpath('//ul[@id="sliding"]/li/a'):
            topicUrl = line.xpath('@href').extract()
            # title = line.xpath('@title').extract()
            if topicUrl:
                yield scrapy.Request(response.urljoin(topicUrl[0]), callback=self.parseImageUrl)
        if nextPage:
            yield scrapy.Request(response.urljoin(nextPage[0]), callback=self.parse)  # 主题翻页操作

    def parseImageUrl(self, response):
        nextSubPage = response.xpath('//ul/li').re(r'\d+\_\d+\.\w+')[-2:-1]  # 项目内下一页链接
        for line in response.xpath('//p[@id="imgString"]/img'):
            item = RosiItem()
            item['projectName'] = self.name
            item['topicName'] = urlparse.urlparse(response.url).path.split('/')[-1].split('.')[0]
            item['picUrlList'] = line.xpath('@src').extract()
            yield item
        if nextSubPage:
            yield scrapy.Request(response.urljoin(nextSubPage[0]), callback=self.parseImageUrl)  # 项目内翻页操作
