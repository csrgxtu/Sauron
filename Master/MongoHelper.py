# coding=utf-8
# Author: Archer Reilly
# Date: 16/Nov/2015
# File: MongoHelper.py
# Desc: DB operations here
#
# Produced By BR
from pymongo import MongoClient
from bson import ObjectId

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

    def readUnvisited(self, start, offset):
        documents = []
        for doc in self.DB['unvisited'].find():
            doc['_id'] = str(doc['_id'])
            documents.append(doc)

        return documents

    def retrieveUnvisited(self, start, offset):
        documents = []
        ids = []
        for doc in self.DB['unvisited'].find():
            doc['_id'] = str(doc['_id'])
            ids.append(str(doc['_id']))
            documents.append(doc)

        self.deleteUnvisited(ids)

        return documents

    def deleteUnvisited(self, ids):
        for id in ids:
            self.DB['unvisited'].remove({'_id': ObjectId(id)})
