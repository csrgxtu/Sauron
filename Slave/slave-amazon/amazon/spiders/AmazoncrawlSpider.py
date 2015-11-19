#!/usr/local/bin/python
#-*- encoding:utf-8 -*-

import scrapy, re, unirest
from scrapy import Request
from scrapy.spiders import  Spider,Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor as sle
from collections import OrderedDict

#!< 运行spider
# scrapy crawl amazon -a url='http://192.168.100.3:5000/unvisitedurls?start=0&offset=10&spider=amazon' -s JOBDIR=crawls/amazon

class AmazoncrawlSpider(Spider):
    #!< spider name
    name            = "amazon"
    allowed_domains = ["amazon.cn"]

    #!< load bookurl file.
    def __init__(self, url=None):
        if url:
            # retrieve with post method, put for create, get for read, delete for delete
            # unvisitedurls http://localhost:5000/unvisitedurls?start=0&offset=10&spider=amazon
            req = unirest.post(url, headers={"Accept":"application/json"})
            self.start_urls = [data['url'] for data in req.body['data']]

    rules = (
        Rule(sle(allow=("http://www.amazon.cn/gp/product/[\w]{10,10}$")), callback="parse", follow=True),
    )

    #!< 单独处理每一本书籍信息
    def parse(self, response):
        # scrapy shell 'http://www.amazon.cn/gp/product/B00VWVAFAG/ref=s9_acsd_ri_bw_rw_r0_p2_i?pf_rd_m=
        # A1AJ19PSB66TGU&pf_rd_s=merchandised-search-5&pf_rd_r=156N8PK0A79FQS9N3NQQ&pf_rd_t=101&pf_rd_p=
        # 249960232&pf_rd_i=658390051'

        sel = Selector(text=response.body)
        orderdict = OrderedDict()

        #!< 书名
        name = ''
        bookname = sel.xpath('//span[@id="productTitle"]/text()').extract()
        kindlename = sel.xpath('//h1[@class="parseasinTitle"]/span/span/text()').extract()
        if (bookname != None) and (bookname != []):
            name = bookname[0]
        elif (kindlename != None and (kindlename != [])):
            name = kindlename[0]
        orderdict[u'书名'] = name.strip()


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
            orderdict['xRay'] = None

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
            score = None


        #!< 亚马逊热销商品排名
        rank =''
        try: # book and kindle
            ranks = sel.xpath('//li[@id="SalesRank"]/text()').extract()
            if (ranks != []) and (len(ranks)>=2):
                for i in ranks[1]:
                    if (' ' not in i) and ('\n' not in i) and ('(' not in i):
                        rank += i
        except:
            rank = None
        orderdict[u'用户评分'] = score
        orderdict[u'亚马逊热销商品排名'] = rank


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


        #!< 书籍封面
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
            raise ("Not cover!")

        if (imgurl.startswith('http://ec4.images-amazon.com/images/I/')):
            #'http://ec8.images-amazon.com/images/I/91bpj-PbL1L.jpg'
            orderdict[u'书籍封面'] = imgurl
        else:
            orderdict[u'书籍封面'] = None


        #!< 书籍链接
        bookurl  = response.url
        orderdict[u'书籍链接'] = bookurl


        #!< return data to 192.168.100.3:5000 !!! !!! !!!
        urlstate = response.status
        posturl = str()
        if (urlstate==200):
            #!< book datas !!!
            bookdict = {}
            bookdict['datas'] = [{'url':bookurl, 'data':orderdict, 'spider':'amazon'}]
            resdata = unirest.put(
                            "http://192.168.100.3:5000/data",
                            headers={ "Accept": "application/json", "Content-Type": "application/json" },
                            params=json.dumps(bookdict)
                         )

            #!< file-->bookurl , headers, body, spider !!!
            filedict = {}
            filedict['files'] = [{
                                    'url':bookurl,
                                    'head':response.headers.to_string(),
                                    'body':response.body,
                                    'spider':'amazon'
                                }]
            resfile = unirest.put(
                            "http://192.168.100.3:5000/file",
                            headers={ "Accept": "application/json", "Content-Type": "application/json" },
                            params=json.dumps(filedict)
                         )

            #!< visitedurls !!!
            posturl = "http://192.168.100.3:5000/visitedurls"

        else:
            #!< deadurls !!!
            posturl = "http://192.168.100.3:5000/deadurls"

        #!< visitedurls or deadurls and spider !!!
        urldict = {}
        urldict['urls'] = [{'url':bookurl, 'spider':'amazon'}]
        resurl = unirest.put(
                        posturl,
                        headers={ "Accept": "application/json", "Content-Type": "application/json" },
                        params=json.dumps(urldict)
                    )
