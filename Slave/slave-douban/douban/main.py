#!/usr/local/bin/python
#-*- encoding:utf-8 -*-

import os

if (__name__=='__main__'):

    command = "scrapy crawl douban -a url='http://192.168.100.3:5000/unvisitedurls?start=0&offset=10&spider=douban' -s JOBDIR=crawls/douban"
    isbnset = [i for i in xrange(0, 2666972, 1000)]

    for index in xrange(len(isbnset)-1):
        start = 'start='+str(isbnset[index])
        offset = 'offset='+str(isbnset[index+1])
        newcommand = command.replace('start=0', start).replace('offset=10', offset)
        #os.system(newcommand)
        #print newcommand


    if (isbnset[-1] < 2666971):
        start = 'start='+str(isbnset[-1])
        offset= 'offset='+str(2666971)
        newcommand = command.replace('start=0', start).replace('offset=10', offset)
        #os.system(newcommand)
        #print newcommand
