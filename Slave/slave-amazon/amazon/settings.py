# -*- coding: utf-8 -*-

BOT_NAME = 'amazon'
SPIDER_MODULES = ['amazon.spiders']
NEWSPIDER_MODULE = 'amazon.spiders'

# -------------------------------------------------scrapy-log setting ------------------------------------------------
LOG_ENABLED = True
#LOG_LEVEL = 'INFO'
#LOG_FILE = './logs/amazon.log'

# The maximum limit for Twisted Reactor thread pool size. Default: 10.
REACTOR_THREADPOOL_MAXSIZE = 50

# ---------------------------------------------------CONCURRENT-------------------------------------------------------
# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS=32
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN=32
CONCURRENT_REQUESTS_PER_IP=32
#Item Processor(即 Item Pipeline) 同时处理(每个response的)item的最大值。默认:100
CONCURRENT_ITEMS=500

# -----------------------------------------------------DOWNLOAD---------------------------------------------------------
# 默认情况下，Scrapy在两个请求间不等待一个固定的值， 而是使用0.5到1.5之间的一个随机值
# *DOWNLOAD_DELAY 的结果作为等待间隔。
#DOWNLOAD_DELAY=2.0

# Disable cookies (enabled by default)
COOKIES_ENABLED=True

# To make RotateUserAgentMiddleware enable.
USER_AGENT  = ''

# ---------------------------------------DOWNLOADER_MIDDLEWARES setting ------------------------------------------------
#RETRY_ENABLED = True
# https://github.com/aivarsk/scrapy-proxies
# Retry many times since proxies often fail
#RETRY_TIMES = 10
# Retry on most error codes since proxies fail for different reasons
#RETRY_HTTP_CODES = [400, 403, 404, 408, 429, 500, 501, 502, 503, 504]
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
#CRAWLERA_USER = '***'     # add your CRAWLERA_USER string value !!!
CRAWLERA_PASS = ''
AUTOTHROTTLE_ENABLED = False

DOWNLOAD_TIMEOUT = 180
#CrawleraMiddleware: disabling download delays on Scrapy side to optimize delays introduced by Crawlera.
#To avoid this behaviour you can use the CRAWLERA_PRESERVE_DELAY setting
#but keep in mind that this may slow down the crawl significantly

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    #'amazon.downloadmiddlewares.googlecache.GoogleCache':50,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'amazon.downloadmiddlewares.randomuseragent.RandomUserAgent':400,
    #'scrapy.downloadermiddlewares.retry.RetryMiddleware': 500,               # RETRY_HTTP_CODES 500
    #'amazon.downloadmiddlewares.randomproxy.RandomProxy':100,                # Proxy
    #'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
    #'scrapy_crawlera.CrawleraMiddleware': 600,                               # crawlera
}


# -------------------------------------------------Other setting-------------------------------------------------------
# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
#scrapy's item pipelines have orders!!!!!,it will go through all the pipelines by the order of the list;
#So if you change the item and return it,the new item will transfer to the next pipeline.
#ITEM_PIPELINES = {'amazon.pipelines.MongoPipelines.MongoPipeline':0,
                  #'amazon.pipelines.BookcoverPipelines.BookcoverPipeline':1,
                  #'amazon.pipelines.DowncoverPipelines.DowncoverPipeline':2,
                  #}


#!< add DEPTH_LIMIT DEPTH_PRIORITY DNSCACHE_ENABLED
#爬取网站最大允许的深度(depth)值。如果为0，则没有限制。默认值0
#DEPTH_LIMIT = 0
#整数值。用于根据深度调整request优先级。如果为0，则不根据深度进行优先级调整。默认值0
#DEPTH_PRIORITY = 0
#是否启用DNS内存缓存(DNS in-memory cache)。默认值True
#DNSCACHE_ENABLED = True

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.telnet.TelnetConsole': None,
#}

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED=False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'amazoncrawl.middlewares.MyCustomSpiderMiddleware': 543,
#}

# --------------------------------------------------AutoThrottle setting -----------------------------------------------
# 该扩展能根据Scrapy服务器及您爬取的网站的负载自动限制爬取速度。http://docs.pythontab.com/scrapy/scrapy0.24/topics/autothrottle.html
# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# AutoThrottle will honour the standard settings for concurrency and delay
# 启用AutoThrottle扩展, 默认 False
#AUTOTHROTTLE_ENABLED=True

# 初始下载延迟(单位:秒), 默认 5.0
#AUTOTHROTTLE_START_DELAY=5.0

#How many responses should pass to perform concurrency adjustments.
#AUTOTHROTTLE_CONCURRENCY_CHECK_PERIOD = 10

# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY=60

# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG=False


# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED=True
#HTTPCACHE_EXPIRATION_SECS=0
#HTTPCACHE_DIR='httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES=[]
#HTTPCACHE_STORAGE='scrapy.extensions.httpcache.FilesystemCacheStorage'
