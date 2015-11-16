# coding=utf-8
#
# Author: Archer Reilly
# File: UnvisitedRes.py
# Date: 16/Nov/2015
# Desc: Unvisited Url collection
#
# Produced By BR
from flask import request
from flask_restful import Resource

from ReturnFormat import UrlReturn

class UnvisitedRes(Resource):
    def put(self):
        Json = request.get_json(force=True)
        print Json
        return UrlReturn

    def get(self):
        UrlReturn['data'] = [
            'http://book.douban.com/isbn/3223132232',
            'http://book.dobuan.com/isbn/7892873728'
        ]

        return UrlReturn
