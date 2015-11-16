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
        # wanting {'urls': ['url']}
        Json = request.get_json(force=True)
        # print Json
        documents = []
        for url in Json['urls']:
            documents.append({'url': url})

        MH = MongoHelper('localhost', 27017)
        UrlReturn['data'] = MH.insertUnvisited({'documents': documents})
        return UrlReturn

    def get(self):
        MH = MongoHelper('localhost', 27017)
        documents = MH.readUnvisited(0, 10)
        UrlReturn['data'] = documents
        return UrlReturn

    def post(self):
        MH = MongoHelper('localhost', 27017)
        documents = MH.retrieveUnvisited(0, 10)
        UrlReturn['data'] = documents
        return UrlReturn

    def delete(self):
        MH = MongoHelper('localhost', 27017)
        MH.deleteUnvisited(['5649bb49f38544370e656295'])
        return UrlReturn
