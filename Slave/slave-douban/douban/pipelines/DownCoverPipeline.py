# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import requests,urllib,socket,time
from scrapy.exceptions import DropItem
import os 

def get_page(imgurl):
    """Obtain page from imgurl. """

    if (imgurl==None)or(imgurl==''):
        raise "imgurl error."
    try:
        page = requests.get(imgurl)
    except requests.RequestException as e:
        return get_page(imgurl)
    except requests.exceptions:
        return get_page(imgurl)
    except socket.error: # error: [Errno 54] Connection reset by peer
        time.sleep(3)
        return get_page(imgurl)
    else:
        return page


def get_bookcover(imgurl,dest_path):
    """ Downloads book cover image and saves it to 'dest_path'."""
    page = get_page(imgurl)
    with open(dest_path,'wb') as f:
        try:
            content = page.content
        except:
            content = urllib.urlopen(imgurl).read().decode('utf8')
        f.write(content)
    f.close()


class DownCoverPipeline(object):
    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        try:
            isbn = item['bookinfo']['ISBN']
        except:
            isbn = item['bookinfo'][u'统一书号']

        if isbn in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(isbn)
            dest_path = './DoubanBookCovers/' + isbn + '.jpg'
            if not os.path.exists(dest_path):
                imgurl    = item['bookinfo']['coverurl']
                get_bookcover(imgurl, dest_path)
                return item
