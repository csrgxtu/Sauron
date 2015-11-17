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

from DefaultRes import DefaultRes
from UnvisitedRes import UnvisitedRes
from VisitedRes import VisitedRes
from DeadRes import DeadRes
from DataRes import DataRes
# from FileRes import FileRes

app = Flask(__name__)
api = Api(app)

api.add_resource(DefaultRes, '/')
api.add_resource(UnvisitedRes, '/unvisitedurls')
api.add_resource(VisitedRes, '/visitedurls')
api.add_resource(DeadRes, '/deadurls')
api.add_resource(DataRes, '/data')
# api.add_resource(FileRes, '/file')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
