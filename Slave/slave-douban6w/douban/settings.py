# -*- coding: utf-8 -*-
BOT_NAME = 'douban'

SPIDER_MODULES = ['douban.spiders']
NEWSPIDER_MODULE = 'douban.spiders'

# LOG_ENABLED default: True
LOG_ENABLED = True
#LOG_LEVEL = 'INFO'
#LOG_FILE = './logs/booksisbn.log'

# The maximum limit for Twisted Reactor thread pool size. Default: 10.
REACTOR_THREADPOOL_MAXSIZE = 50

# Scrapy downloader 并发请求(concurrent requests)的最大值。 (default: 16)
CONCURRENT_REQUESTS=50             #32

# The download delay setting will honor only one of CONCURRENT_REQUESTS_PER_DOMAIN and CONCURRENT_REQUESTS_PER_IP.
# 对单个网站进行并发请求的最大值。(default: 8)
CONCURRENT_REQUESTS_PER_DOMAIN=50 #32

# 当 CONCURRENT_REQUESTS_PER_IP 非0时，延迟针对的是每个ip而不是网站。
#CONCURRENT_REQUESTS_PER_IP=40

#Item Processor(即 Item Pipeline) 同时处理(每个response的)item的最大值。默认:100
CONCURRENT_ITEMS=100

# 默认情况下，Scrapy在两个请求间不等待一个固定的值， 而是使用0.5到1.5之间的一个随机值, DOWNLOAD_DELAY 的结果作为等待间隔。
#DOWNLOAD_DELAY=2.0

# Disable cookies (default True)
COOKIES_ENABLED = True

#!< http://scrapinghub.com/crawlera/
CRAWLERA_ENABLED = True
CRAWLERA_USER = '8e8fb8e3fd8e476ab383a447b8dd1509'
CRAWLERA_PASS = ''
AUTOTHROTTLE_ENABLED = False
DOWNLOAD_TIMEOUT = 180
DOWNLOAD_DELAY = 0

#CrawleraMiddleware: disabling download delays on Scrapy side to optimize delays introduced by Crawlera.
#To avoid this behaviour you can use the CRAWLERA_PRESERVE_DELAY setting
#but keep in mind that this may slow down the crawl significantly

DEFAULT_REQUEST_HEADERS = {
    'X-Crawlera-UA': 'desktop'
}

# 保存项目中启用的下载中间件及其顺序的字典
# check if non-standard middlewares are used
DOWNLOADER_MIDDLEWARES = {
    #'downloadmiddlewares.googlecache.GoogleCache':50,
    #'downloadmiddlewares.randomuseragent.RandomUserAgent':400,
    #'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    #'scrapy.downloadermiddlewares.retry.RetryMiddleware': 600,
    #'downloadmiddlewares.randomproxy.RandomProxy':100,
    #'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
    'scrapy_crawlera.CrawleraMiddleware': 500,
}
# To make RotateUserAgentMiddleware enable.
#USER_AGENT = ''
