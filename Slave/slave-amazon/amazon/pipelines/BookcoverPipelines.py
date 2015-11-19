# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import requests,urllib,time,socket
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
import os

def get_page(imgurl):
    """Obtain page from imgurl. """

    if (imgurl==None)or(imgurl==''):
        raise "url error."
    try:
        page = requests.get(imgurl)
    except requests.RequestException as e:
        return get_page(imgurl)
    except requests.exceptions:
        return get_page(imgurl)
    except socket.error:
        return get_page(imgurl)
    else:
        return page

def get_bookcover(imgurl,dest_path):
    """ Downloads book cover image and saves it to 'dest_path'."""

    #page = requests.get(imgurl)
    page = get_page(imgurl)
    with open(dest_path,'wb') as f:
        try:
            content = page.content
        except:
            content = urllib.urlopen(imgurl).read().decode('utf8')
        f.write(content)
    f.close()

class BookcoverPipeline(object):

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        index = str()
        orderdict = item['bookinfo']
        bookkeys = orderdict.keys()
        if ('ISBN' in bookkeys):
            index = orderdict['ISBN']
        elif ('条形码' in bookkeys):
            index = orderdict['条形码'] # ISBN or ASIN or something else...
        elif ('ASIN' in bookkeys):
            index = orderdict['ASIN'] # Kindle books' ASIN or some books' ASIN
        else:
            raise 'Not find unique index.'

        if index in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(index)
            dest_path = './bookcovers/' + index + '.jpg'
            if not os.path.exists(dest_path):
                imgurl    = item['bookinfo']['coverurl']
                if (imgurl != None):
                    get_bookcover(imgurl, dest_path)
                else:
                    raise "***Coverurl invalid.***"
                return item
