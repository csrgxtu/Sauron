
![spider icon](./spiderman.png)

# Douban Spider based on scrapy for 6W data.

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
* [unirest](http://unirest.io/python.html)


### Usage

	在含有.cfg文件的目录下,输入以下命令,douban 6w data.
	$scrapy crawl douban -a url='http://192.168.100.3:5000/unvisitedurls?start=0&offset=10&spider=6w'


### Note
* '.UserAgentString.json'文件里面包含有**9502**个[PC浏览器](http://www.useragentstring.com/pages/Browserlist/)代理信息和**512**个[Mobile浏览器](http://www.useragentstring.com/pages/Mobile%20Browserlist/)代理信息。
* 默认启用[Crawlera](http://scrapinghub.com/crawlera/)Proxy服务, 需要自己设置 CRAWLERA_USER 的值。(具体如何设置CRAWLERA_USER，请参考官网)
* GoogleCache和RandomUserAgent, 参考[gnemoug](https://github.com/gnemoug/distribute_crawler/tree/master/woaidu_crawler/woaidu_crawler/contrib/downloadmiddleware)
* RandomProxy 参考[aivarsk](https://github.com/aivarsk/scrapy-proxies).
* 我对RandomUserAgent和RandomProxy做了相应的修改。如果，启用RandomProxy, 请重新设置randomproxy.py中的代理地址**url**, 并重新分析实现**updateIPs**函数。
