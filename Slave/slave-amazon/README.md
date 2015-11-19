
![spider icon](./spiderman.png)

# Spider based on scrapy

==========

## Overview

**Spider** based on **scrapy** is create for **crawl useful information**.

==========

## Structure
1. **Needs**

2. **Usage**

3. **Note**


==========

### Needs
* [python](https://www.python.org/downloads/)
* [scrapy](http://doc.scrapy.org/en/latest/)
* [pymongo](http://api.mongodb.org/python/current/)
* [MongoDB](https://www.mongodb.org/)
* [unirest](http://unirest.io/python.html)


### Usage

[JOBDIR](http://doc.scrapy.org/en/latest/topics/jobs.html) Jobs: pausing and resuming crawls.

	在含有.cfg文件的目录下,输入以下命令,
	$scrapy crawl amazon -a url='http://192.168.100.3:5000/unvisitedurls?start=0&offset=10&spider=douban' -s JOBDIR=crawls/amazon


### Note
* '.idea'文件夹是我用Pycharm创建工程时，自动生成的工程配置信息。
* '.UserAgentString.json'文件里面包含有**9502**个[PC浏览器](http://www.useragentstring.com/pages/Browserlist/)代理信息和**512**个[Mobile浏览器](http://www.useragentstring.com/pages/Mobile%20Browserlist/)代理信息。
* 默认启用[Crawlera](http://scrapinghub.com/crawlera/)Proxy服务, 需要自己设置 CRAWLERA_USER 的值。(具体如何设置CRAWLERA_USER，请参考官网)
* GoogleCache和RandomUserAgent, 参考[gnemoug](https://github.com/gnemoug/distribute_crawler/tree/master/woaidu_crawler/woaidu_crawler/contrib/downloadmiddleware)
* RandomProxy 参考[aivarsk](https://github.com/aivarsk/scrapy-proxies).
* 我对RandomUserAgent和RandomProxy做了相应的修改。如果，启用RandomProxy, 请重新设置randomproxy.py中的代理地址**url**, 并重新分析实现**updateIPs**函数。
