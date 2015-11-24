#!/bin/bash

while :
do
    scrapy crawl douban -a url='http://192.168.100.3:5000/unvisitedurls?start=0&offset=10&spider=6w'
    sleep 8s
done


