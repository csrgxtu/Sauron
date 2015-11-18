# coding=utf-8
#
# Author: Archer Reilly
# File: DataRes.py
# Date: 17/Nov/2015
# Desc: File collection
#
# Produced By BR
import pymongo
from flask import request
from flask_restful import Resource
import uuid

from ReturnFormat import UrlReturn
from MongoHelper import MongoHelper

class FileRes(Resource):
    def put(self):
        # wanting {'files': [file]}
        # file: {'url': url, 'head': 'http head', 'body': 'html', 'spider': 'google'}
        Json = request.get_json(force=True)
        documents = []

        for doc in Json['files']:
            u = uuid.uuid4()
            documents.append({'url': doc['url'], 'filename': u.hex + '.html', 'spider': doc['spider']})
            self.save(doc['head'] + '\n\n' + doc['body'], u.hex + '.html')

        MH = MongoHelper('localhost', 27017)
        UrlReturn['data'] = MH.insertFile({"documents": documents})
        MH.close()
        return UrlReturn

    def get(self):
        args = request.args
        MH = MongoHelper('localhost', 27017)
        documents = MH.readFile(args['spider'], args['start'], args['offset'])
        MH.close()
        UrlReturn['data'] = documents
        return UrlReturn

    def save(self, string, filename):
        with open('/tmp/' + filename, 'w') as myFile:
            myFile.write(string)

        return
