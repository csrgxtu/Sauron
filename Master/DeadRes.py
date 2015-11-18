# coding=utf-8
#
# Author: Archer Reilly
# File: DeadRes.py
# Date: 16/Nov/2015
# Desc: Dead Url collection
#
# Produced By BR
import pymongo
from flask import request
from flask_restful import Resource

from ReturnFormat import UrlReturn
from MongoHelper import MongoHelper

class DeadRes(Resource):
    def put(self):
        # wanting {'urls': [{'url': 'http://go.com', 'spider': 'google'}]}
        Json = request.get_json(force=True)
        documents = []
        for url in Json['urls']:
            documents.append(url)

        MH = MongoHelper('localhost', 27017)
        UrlReturn['data'] = MH.insertDead({'documents': documents})
        MH.close()
        return UrlReturn

    def get(self):
        args = request.args
        MH = MongoHelper('localhost', 27017)
        documents = MH.readDead(args['spider'], args['start'], args['offset'])
        MH.close()
        UrlReturn['data'] = documents
        return UrlReturn

    def post(self):
        args = request.args
        MH = MongoHelper('localhost', 27017)
        documents = MH.retrieveDead(args['spider'], args['start'], args['offset'])
        MH.close()
        UrlReturn['data'] = documents
        return UrlReturn

    def delete(self):
        Json = request.get_json(force=True)
        MH = MongoHelper('localhost', 27017)
        MH.deleteDead(Json['ids'])
        MH.close()
        return UrlReturn
