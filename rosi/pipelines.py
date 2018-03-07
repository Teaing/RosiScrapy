# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem


class RosiPipeline(object):
    def process_item(self, item, spider):
        return item


class RosiImgDownloadPipeline(ImagesPipeline):
    defaultHeaders = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
    }

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        projectName = item['projectName']
        topicPath = item['topicName'].split('_')[0]
        imageName = request.url.split('/')[-1]
        fullPath = '{0}/{1}/{2}'.format(projectName, topicPath, imageName)
        return fullPath

    def get_media_requests(self, item, info):
        for image_url in item['picUrlList']:
            yield scrapy.Request(image_url, headers=self.defaultHeaders, meta={'item': item})  # 传入item

    def item_completed(self, results, item, info):
        imagePaths = [x['path'] for ok, x in results if ok]
        if not imagePaths:
            raise DropItem("Item contains no images")
        item['picPath'] = imagePaths
        return item
