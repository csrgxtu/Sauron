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
import Init

class UnvisitedRes(Resource):
    def put(self):
        # wanting {'urls': ['url']}
        Json = request.get_json(force=True)
        # print Json
        documents = []
        for url in Json['urls']:
            documents.append({'url': url})

        inserted_ids = Init.DB.unvisited.insert_many(documents).inserted_ids
        UrlReturn['data'] = inserted_ids
        return UrlReturn

    def get(self):
        UrlReturn['data'] = [
            'http://book.douban.com/isbn/3223132232',
            'http://book.dobuan.com/isbn/7892873728'
        ]

        return UrlReturn
