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
import Init

app = Flask(__name__)
api = Api(app)

# Database Initialization
Init.InitDB()

api.add_resource(DefaultRes, '/')
api.add_resource(UnvisitedRes, '/unvisitedurls')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
