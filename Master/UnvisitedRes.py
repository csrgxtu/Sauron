# coding=utf-8
#
# Author: Archer Reilly
# File: UnvisitedRes.py
# Date: 16/Nov/2015
# Desc: Unvisited Url collection
#
# Produced By BR
import pymongo
from flask import request
from flask_restful import Resource

from ReturnFormat import UrlReturn
from MongoHelper import MongoHelper

class UnvisitedRes(Resource):
    def put(self):
        # wanting {'urls': [{'url': 'http://go.com', 'spider': 'douban'}]}
        Json = request.get_json(force=True)
        # print Json
        documents = []
        for url in Json['urls']:
            documents.append(url)

        MH = MongoHelper('localhost', 27017)
        UrlReturn['data'] = MH.insertUnvisited({'documents': documents})
        MH.close()
        return UrlReturn

    def get(self):
        args = request.args
        MH = MongoHelper('localhost', 27017)
        documents = MH.readUnvisited(args['start'], args['offset'])
        UrlReturn['data'] = documents
        return UrlReturn

    def post(self):
        args = request.args
        MH = MongoHelper('localhost', 27017)
        documents = MH.retrieveUnvisited(args['start'], args['offset'])
        UrlReturn['data'] = documents
        return UrlReturn

    def delete(self):
        Json = request.get_json(force=True)
        MH = MongoHelper('localhost', 27017)
        MH.deleteUnvisited(Json['ids'])
        return UrlReturn
