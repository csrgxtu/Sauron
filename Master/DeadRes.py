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
    MH = None

    def __init__(self, MH):
        self.MH = MH

    def put(self):
        # wanting {'urls': [{'url': 'http://go.com', 'spider': 'google'}]}
        Json = request.get_json(force=True)
        documents = []
        for url in Json['urls']:
            documents.append(url)

        UrlReturn['data'] = self.MH.insertDead({'documents': documents})
        return UrlReturn

    def get(self):
        args = request.args
        documents = self.MH.readDead(args['spider'], args['start'], args['offset'])
        UrlReturn['data'] = documents
        return UrlReturn

    def post(self):
        args = request.args
        documents = self.MH.retrieveDead(args['spider'], args['start'], args['offset'])
        UrlReturn['data'] = documents
        return UrlReturn

    def delete(self):
        Json = request.get_json(force=True)
        self.MH.deleteDead(Json['ids'])
        return UrlReturn
