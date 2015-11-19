#!/bin/bash

while :
do
    scrapy crawl douban -a url='http://192.168.100.3:5000/unvisitedurls?start=0&offset=50&spider=douban' -s JOBDIR=crawls/douban
done
