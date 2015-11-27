# -*- coding: utf-8 -*-
BOT_NAME = 'douban'

SPIDER_MODULES = ['douban.spiders']
NEWSPIDER_MODULE = 'douban.spiders'

#!< http://stackoverflow.com/questions/17029752/speed-up-web-scraper
# --------------------------------------------------------LOG_Thread----------------------------------------------------
# LOG_ENABLED default: True
LOG_ENABLED = True
LOG_LEVEL = 'INFO'
#LOG_FILE = './logs/booksisbn.log'

# The maximum limit for Twisted Reactor thread pool size. Default: 10.
REACTOR_THREADPOOL_MAXSIZE = 32

# ------------------------------------------------------CONCURRENT------------------------------------------------------
#!< http://docs.pythontab.com/scrapy/scrapy0.24/topics/settings.html
# Scrapy downloader 并发请求(concurrent requests)的最大值。 (default: 16)
CONCURRENT_REQUESTS=32             #32

# The download delay setting will honor only one of CONCURRENT_REQUESTS_PER_DOMAIN and CONCURRENT_REQUESTS_PER_IP.
# 对单个网站进行并发请求的最大值。(default: 8)
CONCURRENT_REQUESTS_PER_DOMAIN=32 #32

# 当 CONCURRENT_REQUESTS_PER_IP 非0时，延迟针对的是每个ip而不是网站。
CONCURRENT_REQUESTS_PER_IP=32

#Item Processor(即 Item Pipeline) 同时处理(每个response的)item的最大值。默认:100
CONCURRENT_ITEMS=100


# --------------------------------------------------------DOWNLOAD------------------------------------------------------
# 默认情况下，Scrapy在两个请求间不等待一个固定的值， 而是使用0.5到1.5之间的一个随机值
# *DOWNLOAD_DELAY 的结果作为等待间隔。
#DOWNLOAD_DELAY=2.0
#DOWNLOAD_TIMEOUT = 300
#DOWNLOAD_DELAY = 0

# Disable cookies (default True)
COOKIES_ENABLED = True

# ---------------------------------------DOWNLOADER_MIDDLEWARES setting ------------------------------------------------
#RETRY_ENABLED = True
# https://github.com/aivarsk/scrapy-proxies
# Retry many times since proxies often fail
#RETRY_TIMES = 10
# Retry on most error codes since proxies fail for different reasons
#RETRY_HTTP_CODES = [400, 403, 408, 429, 500, 501, 502, 503, 504] # 404,
"""
400:请求出错-->由于语法格式有误，服务器无法理解此请求。不作修改，客户程序就无法重复此请求。
403:禁止访问
404:找不到
408:请求超时
429:Too many connections.-->http://doc.scrapinghub.com/crawlera.html

500:服务器的内部错误-->Web 服务器不能执行此请求。请稍后重试此请求。
501:未实现-->Web 服务器不支持实现此请求所需的功能。
502:网关出错-->当用作网关或代理时，服务器将从试图实现此请求时所访问的upstream 服务器中接收无效的响应。
503:Service Unavailable-->
504:（网关超时） 服务器作为网关或代理，但是没有及时从上游服务器收到请求。
"""

#!< http://scrapinghub.com/crawlera/
CRAWLERA_ENABLED = True
CRAWLERA_USER = ''     # add your CRAWLERA_USER string value !!!
CRAWLERA_PASS = ''
AUTOTHROTTLE_ENABLED = False
DOWNLOAD_TIMEOUT = 180

#CrawleraMiddleware: disabling download delays on Scrapy side to optimize delays introduced by Crawlera.
#To avoid this behaviour you can use the CRAWLERA_PRESERVE_DELAY setting
#but keep in mind that this may slow down the crawl significantly

# 保存项目中启用的下载中间件及其顺序的字典
# check if non-standard middlewares are used
DOWNLOADER_MIDDLEWARES = {
    #'douban.downloadmiddlewares.googlecache.GoogleCache':50,
    #'downloadmiddlewares.randomuseragent.RandomUserAgent':400,       # UserAgent 400
    #'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    #'scrapy.downloadermiddlewares.retry.RetryMiddleware': 600,               # RETRY_HTTP_CODES 500
    #'douban.downloadmiddlewares.randomproxy.RandomProxy':100,               # Proxy
    #'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
    'scrapy_crawlera.CrawleraMiddleware': 500,                               # crawlera
}
# To make RotateUserAgentMiddleware enable.
#USER_AGENT = ''
