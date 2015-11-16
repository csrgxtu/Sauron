# coding=utf-8
#
# Author: Archer Reilly
# File: VisitedRes.py
# Date: 16/Nov/2015
# Desc: Visited Url collection
#
# Produced By BR
import pymongo
from flask import request
from flask_restful import Resource

from ReturnFormat import UrlReturn
from MongoHelper import MongoHelper

class VisitedRes(Resource):
    def put(self):
        # wanting {'urls': ['url']}
        Json = request.get_json(force=True)
        documents = []
        for url in Json['urls']:
            documents.append({'url': url})

        MH = MongoHelper('localhost', 27017)
        UrlReturn['data'] = MH.insertVisited({'documents': documents})
        return UrlReturn

    def get(self):
        MH = MongoHelper('localhost', 27017)
        documents = MH.readVisited(0, 10)
        UrlReturn['data'] = documents
        return UrlReturn

    def post(self):
        MH = MongoHelper('localhost', 27017)
        documents = MH.retrieveVisited(0, 10)
        UrlReturn['data'] = documents
        return UrlReturn

    def delete(self):
        MH = MongoHelper('localhost', 27017)
        MH.deleteVisited(['5649bb49f38544370e656295'])
        return UrlReturn
