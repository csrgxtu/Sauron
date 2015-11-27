#!/usr/bin/env python
# coding=utf-8
#
# Author: Archer Reilly
# File: main.py
# Date: 16/Nov/2015
# Desc: Sauron Master端服务器主入口文件
#
# Produced By BR
from flask import Flask
from flask_restful import Api

from MongoHelper import MongoHelper

from DefaultRes import DefaultRes
from UnvisitedRes import UnvisitedRes
from VisitedRes import VisitedRes
from DeadRes import DeadRes
from DataRes import DataRes
from FileRes import FileRes

app = Flask(__name__)
api = Api(app)

MH = MongoHelper('192.168.100.3', 27019)

api.add_resource(DefaultRes, '/')
api.add_resource(UnvisitedRes, '/unvisitedurls', resource_class_kwargs={'MH': MH})
api.add_resource(VisitedRes, '/visitedurls', resource_class_kwargs={'MH': MH})
api.add_resource(DeadRes, '/deadurls', resource_class_kwargs={'MH': MH})
api.add_resource(DataRes, '/data', resource_class_kwargs={'MH': MH})
api.add_resource(FileRes, '/file', resource_class_kwargs={'MH': MH})

if __name__ == '__main__':
    #app.run(debug=True, host='0.0.0.0', port=5001)
    app.run()
