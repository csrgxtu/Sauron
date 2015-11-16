# coding=utf-8
#
# Author: Archer Reilly
# File: DataRes.py
# Date: 16/Nov/2015
# Desc: Data collection
#
# Produced By BR
import pymongo
from flask import request
from flask_restful import Resource

from ReturnFormat import UrlReturn
from MongoHelper import MongoHelper

class DataRes(Resource):
    def put(self):
        # wanting {'datas': [data]}
        # data: {'url': url, data: 'json or str'}
        Json = request.get_json(force=True)
        documents = []
        for data in Json['datas']:
            documents.append({'data': data})

        MH = MongoHelper('localhost', 27017)
        UrlReturn['data'] = MH.insertData({'documents': documents})
        return UrlReturn

    def get(self):
        MH = MongoHelper('localhost', 27017)
        documents = MH.readData(0, 10)
        UrlReturn['data'] = documents
        return UrlReturn

    def post(self):
        MH = MongoHelper('localhost', 27017)
        documents = MH.retrieveData(0, 10)
        UrlReturn['data'] = documents
        return UrlReturn

    def delete(self):
        MH = MongoHelper('localhost', 27017)
        MH.deleteData(['5649bb49f38544370e656295'])
        return UrlReturn
