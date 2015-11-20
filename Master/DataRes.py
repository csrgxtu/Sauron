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
    MH = None

    def __init__(self, MH):
        self.MH = MH

    def put(self):
        # wanting {'datas': [data]}
        # data: {'url': url, data: 'json or str', 'spider': 'google'}
        Json = request.get_json(force=True)
        documents = []
        for data in Json['datas']:
            documents.append(data)

        UrlReturn['data'] = self.MH.insertData({'documents': documents})
        return UrlReturn

    def get(self):
        args = request.args
        documents = self.MH.readData(args['spider'], args['start'], args['offset'])
        UrlReturn['data'] = documents
        return UrlReturn

    def post(self):
        args = request.args
        documents = self.MH.retrieveData(args['spider'], args['start'], args['offset'])
        UrlReturn['data'] = documents
        return UrlReturn

    def delete(self):
        Json = request.get_json(force=True)
        self.MH.deleteData(Json['ids'])
        return UrlReturn
