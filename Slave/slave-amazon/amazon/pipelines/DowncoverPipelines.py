# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import Request
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline

# scrapy ImagesPipeline
class DowncoverPipeline(ImagesPipeline):

    #http://blog.csdn.net/php_fly/article/details/19688595
    def file_path(self, request, response=None, info=None):
        image_guid = request.url.split('/')[-1]
        return 'full/%s' % (image_guid)

    # 下载图片
    def get_media_requests(self, item, info):
        #isbn = item['bookinfo'][0]
        for image_url in item['bookinfo']['coverurl']:
            yield Request(image_url)

    # 当一个单独项目中的所有图片请求完成时(要么完成下载，要么因为某种原因下载失败),
    # ImagesPipeline.item_completed()方法将被调用。
    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        return item