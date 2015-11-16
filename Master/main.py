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

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World"

if __name__ == "__main__":
    app.run()
