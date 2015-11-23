# coding=utf-8
#
# Author: Archer Reilly
# File: DataRes.py
# Date: 17/Nov/2015
# Desc: File collection
#
# Produced By BR
import pymongo
from flask import request
from flask_restful import Resource
import uuid
import codecs
import qiniu

from ReturnFormat import UrlReturn
from MongoHelper import MongoHelper

class FileRes(Resource):
    MH = None

    def __init__(self, MH):
        self.MH = MH

    def put(self):
        # wanting {'files': [file]}
        # file: {'url': url, 'head': 'http head', 'body': 'html', 'spider': 'google'}
        Json = request.get_json(force=True)
        documents = []

        for doc in Json['files']:
            u = uuid.uuid4()
            documents.append({'url': doc['url'], 'filename': u.hex + '.html', 'spider': doc['spider']})
            self.qiniuSave(doc['head'] + '\n\n' + doc['body'], u.hex + '.html')

        UrlReturn['data'] = self.MH.insertFile({"documents": documents})
        return UrlReturn

    def get(self):
        args = request.args
        documents = self.MH.readFile(args['spider'], args['start'], args['offset'])
        UrlReturn['data'] = documents
        return UrlReturn

    def save(self, string, filename):
        with codecs.open('/tmp/' + filename, 'w', 'utf-8') as myFile:
            myFile.write(string)

        return

    def qiniuSave(self, string, filename):
        access_key = '_4TUdWfMQGZ5f2DFFmXbARs7pQLWmiPK-IFbSsw5'
        secrect_key = '1x0lUvV11qxbWQO1G_XrMm6v-MSsDWJWNCJk2K67'
        bucket_name = 'brpublic'

        q = qiniu.Auth(access_key, secrect_key)
        token = q.upload_token(bucket_name)
        ret, info = qiniu.put_data(token, 'Saron/' + filename, string)

        return ret
