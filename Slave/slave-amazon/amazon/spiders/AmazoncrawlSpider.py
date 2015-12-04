#!/usr/local/bin/python
#-*- encoding:utf-8 -*-

import scrapy, re, unirest
from scrapy import Request
from scrapy.spiders import  Spider,Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor as sle
from collections import OrderedDict
import logging, json

from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher

#!< 运行spider
# scrapy crawl amazon -a url='http://192.168.100.3:5000/unvisitedurls?start=0&offset=10&spider=amazon' -s JOBDIR=crawls/amazon
def checkXpathResult(rlist):
    if rlist != []:
        return rlist[0]
    else:
        return []

class AmazoncrawlSpider(Spider):
    #!< spider name
    name            = "amazon"
    allowed_domains = ["amazon.cn"]

    handle_httpstatus_list = [\
    400, 401, 402, 403, 404, 405, 406, 407, 408, 409,\
    410, 411, 412, 413, 414, 415, 416, 417, 418, 419,\
    420, 421, 422, 423, 424, 426, 428, 429, 431,\
    440, 444, 449,\
    450, 451,\
    494, 495, 496, 496, 497, 498, 499,\
    500, 501, 502, 503, 504, 505, 506, 507, 508, 509,\
    510, 511,\
    520, 522,\
    598, 599\
    ]

    #!< load bookurl file.
    def __init__(self, url=None):

        if url:
            # retrieve with post method, put for create, get for read, delete for delete
            # unvisitedurls http://localhost:5000/unvisitedurls?start=0&offset=10&spider=amazon
            req = unirest.post(url, headers={"Accept":"application/json"})
            self.start_urls = [data['url'] for data in req.body['data']]
            self.name = url[url.find('spider=')+7:]

            self.visitedurldict = OrderedDict()
            self.datadict       = OrderedDict()
            self.filedict       = OrderedDict()
            self.deadurldict    = OrderedDict()

            self.visitedurldict['urls'] = []
            self.datadict['datas']      = []
            self.filedict['files']      = []
            self.deadurldict['urls']    = []
            rules = (
                Rule(sle(allow=("http://www.amazon.cn/dp/[\w]{10,10}$")), callback="parse", follow=True),
            )

        # def __del__(self) work
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    #!< 单独处理每一本书籍信息
    def parse(self, response):
        # scrapy shell 'http://www.amazon.cn/gp/product/B00VWVAFAG/ref=s9_acsd_ri_bw_rw_r0_p2_i?pf_rd_m=
        # A1AJ19PSB66TGU&pf_rd_s=merchandised-search-5&pf_rd_r=156N8PK0A79FQS9N3NQQ&pf_rd_t=101&pf_rd_p=
        # 249960232&pf_rd_i=658390051'

        sel = Selector(text=response.body)
        orderdict = OrderedDict()

        #!< ---------------------------------------书名，书籍封面URL，评分-----------------------------------------------
        #!< 书名
        name = ''
        bookname = sel.xpath('//span[@id="productTitle"]/text()').extract()
        kindlename = sel.xpath('//h1[@class="parseasinTitle"]/span/span/text()').extract()
        if (bookname != None) and (bookname != []):
            name = bookname[0]
        elif (kindlename != None and (kindlename != [])):
            name = kindlename[0]
        orderdict[u'书名'] = name.strip()

        #!< 书籍封面URL
        #1.books
        texturl = response.body
        #Re = r"http://ec4.images-amazon.com/images/I/[\w]+-?%?_?.?[\w]+.jpg"
        Re = r'''"mainUrl":"http://ec4.images-amazon.com/images/I/[\w]+.+[\w]+.jpg"'''
        imgurls = re.findall(Re, texturl)

        #2.kindle books
        kindleRe = r'''"large":"http://ec4.images-amazon.com/images/I/[\w]+.+[\w]+.jpg"'''
        kimgurls = re.findall(kindleRe, texturl)

        imgurl = str()
        if (imgurls != []):# be sure mainUrl in imgurls
            #imgurl = imgurls[0]
            endindex = imgurls[0].find('''","dimensions"''')
            imgurl = imgurls[0][11:endindex]

        elif(kimgurls != []):# be sure large in imgurls
            endindex = kimgurls[0].find('''","variant"''')
            imgurl = kimgurls[0][9:endindex]
        else:
            #raise ("Not cover!")
            imgurl = ''

        if (imgurl.startswith('http://ec4.images-amazon.com/images/I/')):
            #'http://ec8.images-amazon.com/images/I/91bpj-PbL1L.jpg'
            orderdict[u'书籍封面'] = imgurl
        else:
            orderdict[u'书籍封面'] = ''

        #!< 用户评分
        score = ''
        try:
            #score = sel.xpath('//span[@id="acrPopover"]/@title').extract()
            score = sel.xpath('//div[@id="avgRating"]/span/text()').extract()
            if (score != []):
                score = score[0].strip()
            else: # kindle
                score = sel.xpath('//div[@class="gry txtnormal acrRating"]/text()').extract()
                if (score != []):
                    score = score[0].strip()
        except:
            score = ''
        orderdict[u'用户评分'] = score

        #!< 亚马逊热销商品排名
        rank =''
        try: # book and kindle
            ranks = sel.xpath('//li[@id="SalesRank"]/text()').extract()
            if (ranks != []) and (len(ranks)>=2):
                for i in ranks[1]:
                    if (' ' not in i) and ('\n' not in i) and ('(' not in i):
                        rank += i
        except:
            rank = ''
        orderdict[u'亚马逊热销商品排名'] = rank

        #!< 作者，出版社，原书名，译者，出版年，页数，定价，装帧，丛书，ISBN
        #!< 作者
        author = sel.xpath('//span[@class="author notFaded"]/a[@class="a-link-normal"]/text()').extract()
        authorlocation = sel.xpath('//span[@class="author notFaded"]/span/span[@class="a-color-secondary"]/text()').extract()
        authors = ''
        for i in range(len(author)):
            name0 = author[i]+authorlocation[i]
            authors += name0
        if (authors == ''):
            kindleauthor         = sel.xpath('//div[@class="buying"]/span/a/text()').extract()
            kindlelocationauthor = sel.xpath('//div[@class="buying"]/span/text()').extract()
            kindlelocation = ''
            if (kindlelocationauthor != None) and (kindlelocationauthor != []):
                kindlelocation = kindlelocationauthor[1].strip()
            for i in range(len(kindleauthor)):
                name1 = kindleauthor[i] + kindlelocation[i]
                authors += name1
        orderdict[u'作者'] = authors

        #!< 书籍其它信息
        detailNameTmp = sel.xpath('//div[@class="content"]/ul/li/b/text()').extract()
        detailName = [i.strip('\n :') for i in detailNameTmp]
        Name = detailName[:-2]

        detailValueTmp = sel.xpath('//div[@class="content"]/ul/li/text() | //div[@class="content"]/ul/li/a/text()').extract()
        detailValue = []
        for vt in detailValueTmp:
            vt = vt.strip('\n >')
            if (vt != '') and (vt != u'\xa0'):
                detailValue.append(vt)
        Value = detailValue[:len(Name)]

        Num = len(Name)
        for i in xrange(Num):
            key = Name[i]
            val = Value[i]
            if (':' in key):
                key = key.strip(':')
            if (':' in val):
                val = val.strip(':')
            val = val.strip(' ')
            orderdict[key] = val
        #!< kindle
        try:
            xray = sel.xpath('//a[@id="xrayPop"]/span/text()').extract()
            orderdict['xRay'] = xray[0]
        except:
            orderdict['xRay'] = ''

        #!< 书籍价格
        PZprice = sel.xpath('//span[@class="a-button-inner"]/a/span/span/text()').extract()
        if (PZprice != []): # book
            if(len(PZprice)==1):
                price = PZprice[0].strip()
                orderdict[u'平装'] = price
            else:
                price = [s.strip() for s in PZprice]
                orderdict[u'精装'] = price[0]
                orderdict[u'平装'] = price[1]
        else:
            PZprice = sel.xpath('//b[@class="priceLarge"]/text()').extract()
            if (PZprice != []):
                price = PZprice[0].strip()
                orderdict[u'Kindle电子书价格'] = price

        #!< 内容简介 & 作者简介
        trees = sel.xpath('//div[@id="s_contents"]/div')
        infotitlelist = []
        infotitlevaluelist = []
        for tree in trees:
            #infotitle
            infotitle = checkXpathResult(tree.xpath('h3/text()').extract())
            infotitlelist.append(infotitle)

            #infotitlevalue
            infotitlevalue = checkXpathResult(tree.xpath('p').extract())
            infotitlevalue = infotitlevalue.strip().encode('utf-8')
            if ('<p>' in infotitlevalue) or ('</p>' in infotitlevalue):
                infotitlevalue = infotitlevalue.replace('<p>','')
                infotitlevalue = infotitlevalue.replace('</p>','')
            if ('<br>' in infotitlevalue):
                infotitlevalue = infotitlevalue.replace('<br>','')
            infotitlevaluelist.append(infotitlevalue)
        #(k,v)
        if (infotitlelist != []) and (infotitlevaluelist != []):
            lenth = len(infotitlelist)
            for i in xrange(lenth-1):
                k, v = infotitlelist[i], infotitlevaluelist[i]
                orderdict[k] = v.strip()

        #!< 相关推荐书目
        simsbook = sel.xpath('//div[@id="purchase-sims-feature"]/div/@data-a-carousel-options').extract()
        bookasins = ''
        if (simsbook != []):
            data = simsbook[0]
            dataencode = data.encode('utf-8')
            r = re.compile('B\w{9,9}')
            bookasins = re.findall(r, dataencode)
        orderdict[u'相关推荐书目'] = bookasins

        #!< 书籍链接
        bookurl  = response.url
        urlstate = response.status

        #!< 书籍购买来源
        orderdict[u'书籍购买来源'] = bookurl
        orderdict[u'书籍链接'] = bookurl

        #!< return data to 192.168.100.3:5000 !!! !!! !!!
        #posturl = str()
        if (200<=urlstate<400):
            #!< visitedurls !!!
            urldt = {}
            urldt = {'url':bookurl, 'spider':self.name}
            self.visitedurldict['urls'].append(urldt)

            #!< datas !!!
            bookdt = {}
            bookdt = {'url':bookurl, 'data':orderdict, 'spider':self.name}
            self.datadict['datas'].append(bookdt)

            #!< file !!!
            filedt = {}
            filedt = {
                        'url':bookurl,
                        'head':response.headers.to_string(),
                        'body':response.body,
                        'spider':self.name
                    }
            self.filedict['files'].append(filedt)
        else:
            #!< deadurls !!!
            urldt = {}
            urldt = {'url':bookurl, 'spider':self.name}
            self.deadurldict['urls'].append(urldt)


    # !< overwrite!
    def spider_closed(self, spider):
        """
        Put visitedurldict, datadict, filedict,  deadurldict to Master.
        Format:
        visitedurldict['urls'] = [ {'url':'', 'spider':self.name},  {'url':'', 'spider':self.name} ]

        datadict['datas']      = [ {'url':'', 'data':{}, 'spider':self.name},  {'url':'', 'data':{}, 'spider':self.name} ]

        filedict['files']      = [ {'url':'', 'head':'', 'body':'', 'spider':self.name},  {'url':'', 'head':'', 'body':'', 'spider':self.name} ]

        deadurldict['urls']    = [ {'url':'', 'spider':self.name},  {'url':'', 'spider':self.name} ]
        """
        lenOfdeadUrls = len(self.deadurldict['urls'])
        logging.info('spidername ' + self.name + '!!!')
        logging.info('visitedurls' + str(len(self.visitedurldict['urls'])))
        logging.info('datadict   ' + str(len(self.datadict['datas'])))
        logging.info('filedict   ' + str(len(self.filedict['files'])))
        logging.info('deadurls   ' + str(len(self.deadurldict['urls'])))

        if (lenOfdeadUrls==10):
            unirest.timeout(180)
            resdeadurl = unirest.put(
                            "http://192.168.100.3:5000/deadurls",
                            headers={ "Accept": "application/json", "Content-Type": "application/json" },
                            params=json.dumps(self.deadurldict)
                        )

        elif(lenOfdeadUrls==0):
            unirest.timeout(180)
            resvisitedurl = unirest.put(
                            "http://192.168.100.3:5000/visitedurls",
                            headers={ "Accept": "application/json", "Content-Type": "application/json" },
                            params=json.dumps(self.visitedurldict)
                        )
            unirest.timeout(180)
            resdata = unirest.put(
                            "http://192.168.100.3:5000/data",
                            headers={ "Accept": "application/json", "Content-Type": "application/json" },
                            params=json.dumps(self.datadict)
                         )
            unirest.timeout(180)
            resfile = unirest.put(
                            "http://192.168.100.3:5000/file",
                            headers={ "Accept": "application/json", "Content-Type": "application/json" },
                            params=json.dumps(self.filedict)
                         )

        else:# lenOfdeadUrls in (0,10)
            unirest.timeout(180)
            resvisitedurl = unirest.put(
                            "http://192.168.100.3:5000/visitedurls",
                            headers={ "Accept": "application/json", "Content-Type": "application/json" },
                            params=json.dumps(self.visitedurldict)
                        )
            unirest.timeout(180)
            resdata = unirest.put(
                            "http://192.168.100.3:5000/data",
                            headers={ "Accept": "application/json", "Content-Type": "application/json" },
                            params=json.dumps(self.datadict)
                         )
            unirest.timeout(180)
            resfile = unirest.put(
                            "http://192.168.100.3:5000/file",
                            headers={ "Accept": "application/json", "Content-Type": "application/json" },
                            params=json.dumps(self.filedict)
                         )
            unirest.timeout(180)
            resdeadurl = unirest.put(
                            "http://192.168.100.3:5000/deadurls",
                            headers={ "Accept": "application/json", "Content-Type": "application/json" },
                            params=json.dumps(self.deadurldict)
                        )
