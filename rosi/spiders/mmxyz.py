# -*- coding: utf-8 -*-

import scrapy
import urlparse
from rosi.items import RosiItem


class MmxyzSpider(scrapy.Spider):
    name = 'mmxyz'
    allowed_domains = ['mmxyz.net']
    start_urls = ['http://mmxyz.net/']

    def parse(self, response):
        nextLink = response.xpath('//link[@rel="next"]/@href').extract()  # 下一页主题链接
        for line in response.xpath('//a[@class="inimg"]'):
            topicUrl = line.xpath('@href').extract()
            # title = line.xpath('@title').extract()
            if topicUrl:
                yield scrapy.Request(topicUrl[0], callback=self.parseImageUrl)
        if nextLink:
            yield scrapy.Request(response.urljoin(nextLink[0]), callback=self.parse)  # 主题翻页操作

    def parseImageUrl(self, response):
        for line in response.xpath('//dt[@class="gallery-icon"]'):
            item = RosiItem()
            item['projectName'] = self.name
            item['topicName'] = urlparse.urlparse(response.url).path.replace('/', '')
            item['picUrlList'] = line.xpath('a/@href').extract()
            yield item
