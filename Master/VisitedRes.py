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
    MH = None

    def __init__(self, MH):
        self.MH = MH

    def put(self):
        # wanting {'urls': [{'url': 'http://go.com', 'spider': 'google'}]}
        Json = request.get_json(force=True)
        documents = []
        for url in Json['urls']:
            documents.append(url)

        UrlReturn['data'] = self.MH.insertVisited({'documents': documents})
        return UrlReturn

    def get(self):
        args = request.args
        documents = self.MH.readVisited(args['spider'], args['start'], args['offset'])
        UrlReturn['data'] = documents
        return UrlReturn

    def post(self):
        args = request.args
        documents = self.MH.retrieveVisited(args['spider'], args['start'], args['offset'])
        UrlReturn['data'] = documents
        return UrlReturn

    def delete(self):
        Json = request.get_json(force=True)
        self.MH.deleteVisited(Json['ids'])
        return UrlReturn
