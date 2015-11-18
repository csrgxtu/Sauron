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
        # data: {'url': url, data: 'json or str', 'spider': 'google'}
        Json = request.get_json(force=True)
        documents = []
        for data in Json['datas']:
            documents.append(data)

        MH = MongoHelper('localhost', 27017)
        UrlReturn['data'] = MH.insertData({'documents': documents})
        MH.close()
        return UrlReturn

    def get(self):
        args = request.args
        MH = MongoHelper('localhost', 27017)
        documents = MH.readData(args['spider'], args['start'], args['offset'])
        MH.close()
        UrlReturn['data'] = documents
        return UrlReturn

    def post(self):
        args = request.args
        MH = MongoHelper('localhost', 27017)
        documents = MH.retrieveData(args['spider'], args['start'], args['offset'])
        MH.close()
        UrlReturn['data'] = documents
        return UrlReturn

    def delete(self):
        Json = request.get_json(force=True)
        MH = MongoHelper('localhost', 27017)
        MH.deleteData(Json['ids'])
        MH.close()
        return UrlReturn
