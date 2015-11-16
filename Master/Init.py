# coding=utf-8
#
# Author: Archer Reilly
# File: Init.py
# Date: 16/Nov/2015
# Desc: Database Initialization
#
# Produced By BR
from pymongo import MongoClient

DB = None
UnvisitedCollection = None
VisitedCollection = None
DeadCollection = None
DataCollection = None

def InitDB():
    host = 'localhost'
    port = 27017

    client = MongoClient(host, port)
    DB = client['master']
    UnvisitedCollection = DB['unvisted']
    VisitedCollection = DB['visited']
