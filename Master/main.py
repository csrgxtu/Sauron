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

app = Flask(__name__)
api = Api(app)

# class HelloWorld(Resource):
#     def get(self):
#         return {'hello': 'world'}

api.add_resource(DefaultRes, '/')

if __name__ == '__main__':
    app.run(debug=True)
