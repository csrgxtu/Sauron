# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import log
from scrapy.conf import settings
from scrapy.exceptions import DropItem
import pymongo,logging

class MongoPipeline(object):
    """pymongodb store data of every book. """
    def __init__(self):
        self.server = settings['MONGODB_SERVER']
        self.port   = settings['MONGODB_PORT']
        self.db     = settings['MONGODB_DB']
        self.col    = settings['MONGODB_COLLECTION']
        connection  = pymongo.MongoClient(self.server, self.port)
        db          = connection[self.db]
        self.collection = db[self.col]

    def process_item(self, item, spider):
        err_msg = ''
        for field, data in item.items():
            if not data:
                err_msg += 'Missing %s of poem from %s\n' % (field, item['bookinfo'])
        if err_msg:
            raise DropItem(err_msg)

        # self.collection.insert(dict(item)) # 可能存在重复数据
        # 我们要爬取更多的数据，所有我们希望避免向数据库中添加重复的问题。为了实现这一点，我们可以使用一个MongoDB的 upsert方法，
        # 它意味着如果一个问题已经存在数据库中，我们将更新它的标题；否则我们将新问题插入数据库中。
        self.collection.update({'bookinfo':item['bookinfo']}, dict(item), upsert=True)

        log.msg('Item written to MongoDB database %s/%s' % (self.db, self.col),level=log.DEBUG, spider=spider)

        return item
