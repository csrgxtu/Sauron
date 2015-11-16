# coding=utf-8
#
# Author: Archer Reilly
# File: DefaultRes.py
# Date: 16/Nov/2015
# Desc: Default Resource File
#
# Produced By BR
from flask_restful import Resource

from ReturnFormat import Welcom

class DefaultRes(Resource):
    def get(self):
        return Welcom
