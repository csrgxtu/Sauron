# coding=utf-8
# Author: Archer Reilly
# Date: 16/Nov/2015
# File: MongoHelper.py
# Desc: DB operations here
#
# Produced By BR
from pymongo import MongoClient

class MongoHelper(object):
    Host = None
    Port = None
    DB = None

    def __init__(self, host, port):
        self.Host = host
        self.Port = port

        client = MongoClient(self.Host, self.Port)
        self.DB = client['master']

    # expecting {'documents': [document, document]}
    # document: {'url': 'http://www.douban.com'}
    def insertUnvisited(self, documents):
        inserted_ids = self.DB['unvisited'].insert_many(documents['documents']).inserted_ids
        return [str(id) for id in inserted_ids]

    def readUnvisited(self):
        pass
