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
        # first, check if unvisited, visited, dead contains the document, if yes,
        # remove this document, else prepare insert it into unvisited
        newDocuments = []
        for document in documents['documents']:
            if self.isUnique(document['url']):
                newDocuments.append(document)

        if len(newDocuments) == 0:
            return []

        inserted_ids = self.DB['unvisited'].insert_many(newDocuments).inserted_ids
        return [str(id) for id in inserted_ids]

    def insertVisited(self, documents):
        newDocuments = []
        for document in documents['documents']:
            if self.isUnique(document['url']):
                newDocuments.append(document)

        if len(newDocuments) == 0:
            return []

        inserted_ids = self.DB['visited'].insert_many(newDocuments).inserted_ids
        return [str(id) for id in inserted_ids]

    def insertDead(self, documents):
        newDocuments = []
        for document in documents['documents']:
            if self.isUnique(document['url']):
                newDocuments.append(document)

        if len(newDocuments) == 0:
            return []

        inserted_ids = self.DB['dead'].insert_many(newDocuments).inserted_ids
        return [str(id) for id in inserted_ids]

    def insertData(self, documents):
        inserted_ids = self.DB['data'].insert_many(documents['documents']).inserted_ids
        return [str(id) for id in inserted_ids]

    def insertFile(self, documents):
        inserted_ids = self.DB['file'].insert_many(documents['documents']).inserted_ids
        return [str(id) for id in inserted_ids]

    def readUnvisited(self, start, offset):
        documents = []
        for doc in self.DB['unvisited'].find():
            doc['_id'] = str(doc['_id'])
            documents.append(doc)

        return documents

    def readVisited(self, start, offset):
        documents = []
        print "fuck wired"
        for doc in self.DB['visited'].find():
            print doc
            doc['_id'] = str(doc['_id'])
            documents.append(doc)

        return documents

    def readDead(self, start, offset):
        documents = []
        for doc in self.DB['dead'].find():
            doc['_id'] = str(doc['_id'])
            documents.append(doc)

        return documents

    def readData(self, start, offset):
        documents = []
        for doc in self.DB['data'].find():
            doc['_id'] = str(doc['_id'])
            documents.append(doc)

        return documents

    def readFile(self, start, offset):
        documents = []
        for doc in self.DB['file'].find():
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

    def retrieveVisited(self, start, offfset):
        documents = []
        ids = []
        for doc in self.DB['visited'].find():
            doc['_id'] = str(doc['_id'])
            ids.append(str(doc['_id']))
            documents.append(doc)

        self.deleteVisited(ids)

        return documents

    def retrieveDead(self, start, offfset):
        documents = []
        ids = []
        for doc in self.DB['dead'].find():
            doc['_id'] = str(doc['_id'])
            ids.append(str(doc['_id']))
            documents.append(doc)

        self.deleteDead(ids)

        return documents

    def retrieveData(self, start, offfset):
        documents = []
        ids = []
        for doc in self.DB['data'].find():
            doc['_id'] = str(doc['_id'])
            ids.append(str(doc['_id']))
            documents.append(doc)

        self.deleteData(ids)

        return documents

    def deleteUnvisited(self, ids):
        for id in ids:
            self.DB['unvisited'].remove({'_id': ObjectId(id)})

    def deleteVisited(self, ids):
        for id in ids:
            self.DB['visited'].remove({'_id': ObjectId(id)})

    def deleteDead(self, ids):
        for id in ids:
            self.DB['dead'].remove({'_id': ObjectId(id)})

    def deleteData(self, ids):
        for id in ids:
            self.DB['data'].remove({'_id': ObjectId(id)})

    def isUnique(self, url):
        if self.inUnvisited(url):
            return False
        elif self.inVisited(url):
            return False
        elif self.inDead(url):
            return False
        else:
            return True

    def inUnvisited(self, url):
        count = self.DB['unvisited'].count({'url': url})
        if count == 0:
            return False

        return True

    def inVisited(self, url):
        count = self.DB['visited'].count({'url': url})
        if count == 0:
            return False

        return True

    def inDead(self, url):
        count = self.DB['dead'].count({'url': url})
        if count == 0:
            return False

        return True
